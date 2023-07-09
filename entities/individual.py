from marshmallow import Schema, ValidationError, post_load, pre_load
from dataclasses import dataclass

@dataclass
class Individual:

    def __init__(self, id, nome, url_foto, sexo, data_nascimento, nacionalidade):
        self.__id = id
        self.__nome = nome
        self.__url_foto = url_foto
        self.__sexo = sexo
        self.__data_nascimento = data_nascimento
        self.__nacionalidade = str(nacionalidade).upper()

    def to_json(self):

        return {
            "id": self.__id,
            "nome": self.__nome,
            "url_foto": self.__url_foto,
            "sexo": self.__sexo,
            "data_nascimento": self.__data_nascimento,
            "nacionalidade": self.__nacionalidade
        }

