import unittest
from unittest import TestCase, mock
from unittest.mock import patch, MagicMock
from services.reconhecimento_service import ReconhecimentoService
from exceptions.no_face_detected_exception import NoFaceDetectedException
from services.mongoService import MongoService


class TestReconhecimentoService(TestCase):
    reconhecimento_service = ReconhecimentoService()

    def test_detect_face(self):

        self.assertEqual(self.reconhecimento_service.detect_face('../img/aria.jpg'), 1)

    def test_detect_face2(self):

        self.assertEqual(self.reconhecimento_service.detect_face('../img/alicia.jpg'), 1)

    def test_detect_face_no_face(self):

        with self.assertRaises(NoFaceDetectedException):
            self.reconhecimento_service.detect_face('../img/no_face.jpg')

    def test_comparar_faces(self):

        self.assertEqual(self.reconhecimento_service.comparar_faces('../img/aria.jpg', '../img/aria2.jpg'), [True])

    def test_comparar_faces2(self):

        self.assertEqual(self.reconhecimento_service.comparar_faces('../img/aria.jpg', '../img/alicia.jpg'), [False])

    # teste mocado
    @patch('services.reconhecimento_service.ReconhecimentoService.detect_face', return_value='teste_resposta')
    def test_recognize_mocado(self, mongo_mock):
        self.assertEqual(self.reconhecimento_service.detect_face('teste'), 'teste_resposta')

    def test_recognize(self):

        url = "https://i.pinimg.com/originals/d0/25/03/d02503e15294e9c578cb22be08d6faee.jpg"
        individuals = [
            {
                "_id": "f6b8c444-e843-44e9-93dd-ac0791dde4ad",
                "id": "f6b8c444-e843-44e9-93dd-ac0791dde4ad",
                "nome": "Olga Kurylenko",
                "url_foto": "https://i.pinimg.com/736x/b9/49/75/b949759c54692d7730ca3ad2322f9e7f.jpg",
                "sexo": "F",
                "data_nascimento": "14/11/1979",
                "nacionalidade": "UCRANIANA"
            },
            {
                "_id": "4283faa9-7da1-4cb5-a43a-22f73b6b448d",
                "id": "4283faa9-7da1-4cb5-a43a-22f73b6b448d",
                "nome": "Alicia Vikander",
                "url_foto": "https://mulhernocinema.com/wp-content/uploads/2016/04/alicia-vikander.jpg",
                "sexo": "F",
                "data_nascimento": "03/10/1988",
                "nacionalidade": "SUECA"
            }
        ]

        analise = self.reconhecimento_service.recognize(str(url), individuals)

        expected = [
            {
                "_id": "4283faa9-7da1-4cb5-a43a-22f73b6b448d",
                "data_nascimento": "03/10/1988",
                "id": "4283faa9-7da1-4cb5-a43a-22f73b6b448d",
                "nacionalidade": "SUECA",
                "nome": "Alicia Vikander",
                "sexo": "F",
                "url_foto": "https://mulhernocinema.com/wp-content/uploads/2016/04/alicia-vikander.jpg"
            }]

        self.assertEqual(analise, expected)


if __name__ == '__main__':
    unittest.main()
