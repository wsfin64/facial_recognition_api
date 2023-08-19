import unittest
from unittest import TestCase
from entities.individual import IndividualSchema
from marshmallow import ValidationError


class TestSchemas(TestCase):

    individual_payload = {
        "nome": "Teste",
        "url_foto": "teste.jpg",
        "sexo": 'f',
        "nacionalidade": "Brasileira",
        "data_nascimento": "02/02/2002"
    }

    def test_individual_load(self):

        individual = IndividualSchema().load(self.individual_payload)

        expected_individual = {
            "_id": None,
            "id": None,
            "nome": "Teste",
            "url_foto": "teste.jpg",
            "sexo": 'F',
            "nacionalidade": "BRASILEIRA",
            "data_nascimento": "02/02/2002"
        }

        self.assertEqual(individual, expected_individual)

    def test_invalid_sex(self):

        self.individual_payload["sexo"] = 'p'

        with self.assertRaises(ValidationError):
            individual = IndividualSchema().load(self.individual_payload)

        self.individual_payload["sexo"] = 'Masculino'

        with self.assertRaises(ValidationError):
            individual = IndividualSchema().load(self.individual_payload)

    def test_missing_individual_fields(self):

        # Missing nationality
        individual_payload = {
            "nome": "Teste",
            "url_foto": "teste.jpg",
            "sexo": 'F',
            "data_nascimento": "02/02/2002"
        }

        # Missing url_foto
        individual_payload_2 = {
            "nome": "Teste",
            "sexo": 'F',
            "nacionalidade": "BRASILEIRA",
            "data_nascimento": "02/02/2002"
        }

        with self.assertRaises(ValidationError):
            individual = IndividualSchema().load(individual_payload)

        with self.assertRaises(ValidationError):
            individual = IndividualSchema().load(individual_payload_2)


if __name__ == '__main__':
    unittest.main()
