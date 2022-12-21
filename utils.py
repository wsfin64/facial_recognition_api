import logging


class Logger:

    def __init__(self) -> None:
        self.config = logging.basicConfig(filename='./logs/teste.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')


    @staticmethod
    def info(message):
        return logging.info(message)
    
    @staticmethod
    def error(message):
        return logging.error(message)
    
    @staticmethod
    def warning(message):
        return logging.warning(message)
    
    @staticmethod
    def debug(message):
        return logging.debug(message)

