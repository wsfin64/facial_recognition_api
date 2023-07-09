import pika
import json
from os import environ
from services.imagem_binaria_service import ImagemService
from services.reconhecimento_service import ReconhecimentoService
from utils import Logger
from services.mongoService import MongoService

logger = Logger()


class MessagePublisher(object):
    def __init__(self):
        self.rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.rabbit_connection.channel()

        self.channel.exchange_declare(
            exchange="recognition",
            exchange_type='direct',
            durable=True
        )

    def send_message(self, payload:dict):
        self.channel.basic_publish(
            exchange="recognition",
            routing_key='face-recognition',
            body=json.dumps(payload)
        )
        self.rabbit_connection.close()
        print('Message sent')


class MessageConsumer(object):
    def __init__(self):
        self.rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.rabbit_connection.channel()

        self.queue = self.channel.queue_declare('recognition_queue')
        self.queue_name = self.queue.method.queue

        self.channel.queue_bind(
            exchange='recognition',
            queue=self.queue_name,
            routing_key='face-recognition'  # binding key
        )

        self.mongo_service = MongoService()

    def callback(self, ch, method, properties, body):
        payload = json.loads(body)
        logger.info({"Message received": payload})
        print({'Message Received - processid': payload.get("processId")})
        recognize_service = ReconhecimentoService()


        modelos = self.mongo_service.find_all_individuals()
        document_analysis = self.mongo_service.find_analysis_by_processId(payload.get('processId'))

        lista_resposta = recognize_service.recognize(payload.get('foto'), modelos)

        document_analysis["status"] = 'FINISHED'
        document_analysis["modelsMatched"] = lista_resposta
        self.mongo_service.update_analysis(document_analysis)
        logger.info({"Updated Document": document_analysis})
        print({"Matched Models": lista_resposta, "processId": payload.get('processId')})

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        self.channel.basic_consume(on_message_callback=self.callback, queue=self.queue_name)
        self.channel.start_consuming()

