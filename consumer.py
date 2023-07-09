import pika
import json
from services.message_service import MessageConsumer


class Consumer:

    def do_consumer(self):

        consumer = MessageConsumer()
        print('Consuming')

        consumer.consume()

if __name__ == '__main__':
    Consumer().do_consumer()