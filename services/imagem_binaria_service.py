import base64
import os.path
from base64 import b64encode, b64decode
import requests
from io import BytesIO


class ImagemService:

    @staticmethod
    def encode_imagem(url_imagem: str) -> bytes:
        """Get the bytes of the picture"""
        requisicao = requests.get(url_imagem).content
        imagem = b64encode(requisicao)
        return imagem

    @staticmethod
    def carregar_face_conhecida(image_binaria: bytes) -> str:
        """Write the bytes into a .jpg file"""
        with open('conhecida.jpg', 'wb') as file:
            file.write(base64.b64decode(image_binaria))
            return 'conhecida.jpg'

    @staticmethod
    def carregar_face_desconhecida(image_binaria: bytes) -> str:
        """Write the bytes into a .jpg file"""
        with open('desconhecida.jpg', 'wb') as file:
            file.write(base64.b64decode(image_binaria))
            return 'desconhecida.jpg'

    @staticmethod
    def apagar_faces(path) -> None:
        if isinstance(path, str):
            if os.path.exists(path):
                os.remove(path)
        if isinstance(path, list):
            for p in path:
                if os.path.exists(p):
                    os.remove(p)
