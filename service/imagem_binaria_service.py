import base64
import os.path
from base64 import b64encode, b64decode
import requests
from PIL import Image
from io import BytesIO


class ImagemService:

    @staticmethod
    def encode_imagem(url_imagem):
        requisicao = requests.get(url_imagem).content
        imagem = b64encode(requisicao)
        return imagem

    @staticmethod
    def decode_imagem(imagem_binaria):
        imagem_decoded = BytesIO(b64decode(imagem_binaria))
        return imagem_decoded

    @staticmethod
    def carregar_face_conhecida(image_binaria):
        with open('conhecida.jpg', 'wb') as file:
            file.write(base64.b64decode(image_binaria))
            return 'conhecida.jpg'

    @staticmethod
    def carregar_face_desconhecida(image_binaria):
        with open('desconhecida.jpg', 'wb') as file:
            file.write(base64.b64decode(image_binaria))
            return 'desconhecida.jpg'

    @staticmethod
    def apagar_faces(path):
        if os.path.exists(path):
            os.remove(path)
