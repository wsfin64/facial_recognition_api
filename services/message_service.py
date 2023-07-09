import pika
import json
from os import environ
from services.imagem_binaria_service import ImagemService
from services.reconhecimento_service import ReconhecimentoService
from utils import Logger

logger = Logger()


class MessagePublisher(object):
    def __init__(self):
        self.rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.rabbit_connection.channel()

        self.channel.exchange_declare(
            exchange="recognition",
            exchange_type='direct'
        )

    def send_message(self, payload:dict):
        self.channel.basic_publish(
            exchange="recognition",
            routing_key='face-recognition',
            body=json.dumps(payload)
        )
        self.rabbit_connection.close()


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

    def callback(self, ch, method, properties, body):
        payload = json.loads(body)
        logger.info({"Message received": payload})
        recognize_service = ReconhecimentoService()
        recognize_service.recognize(payload)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        self.channel.basic_consume(on_message_callback=self.callback, queue=self.queue_name)
        self.channel.start_consuming()

