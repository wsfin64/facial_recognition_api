import unittest
from unittest import TestCase, mock
from services.reconhecimento_service import ReconhecimentoService
from exceptions.no_face_detected_exception import NoFaceDetectedException


class TestReconhecimentoService(TestCase):
    reconhecimento_service = ReconhecimentoService()

    def test_detect_face(self):

        self.assertEqual(self.reconhecimento_service.detect_face('../img/aria.jpg'), None)

    def test_detect_face2(self):

        self.assertEqual(self.reconhecimento_service.detect_face('../img/alicia.jpg'), None)

    def test_detect_face_no_face(self):

        with self.assertRaises(NoFaceDetectedException):
            self.reconhecimento_service.detect_face('../img/no_face.jpg')

    def test_comparar_faces(self):

        self.assertEqual(self.reconhecimento_service.comparar_faces('../img/aria.jpg', '../img/aria2.jpg'), [True])

    def test_comparar_faces2(self):

        self.assertEqual(self.reconhecimento_service.comparar_faces('../img/aria.jpg', '../img/alicia.jpg'), [False])


if __name__ == '__main__':
    unittest.main()
