from marshmallow import Schema, ValidationError, post_load, pre_load, EXCLUDE, fields
from dataclasses import dataclass

def sex_validation(value):
    if not len(value) == 1 or value not in ['F', 'M', 'f', 'm']:
        raise ValidationError("Valor inválido, apenas os valores 'M' e 'F' são permitidos")


class IndividualSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    _id = fields.Str(load_default=None)
    id = fields.Str(load_default=None)
    nome = fields.Str(required=True)
    url_foto = fields.Str(required=True)
    sexo = fields.Str(validate=sex_validation, required=True)
    nacionalidade = fields.Str(required=True)
    data_nascimento = fields.Str(required=True)

    @post_load
    def process_data(self, data, **kwargs):

        data['sexo'] = data['sexo'].upper()
        data['nacionalidade'] = data['nacionalidade'].upper()
        return data
