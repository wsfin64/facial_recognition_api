import cv2
import face_recognition
from exceptions.no_face_detected_exception import NoFaceDetectedException
from service.imagem_binaria_service import ImagemService
from utils import Logger
from service.image_processor import ImageProcessor

logger = Logger()

class ReconhecimentoService:

    def __init__(self):
        self.image_service = ImagemService()

    @staticmethod
    def comparar_faces(face_conhecida, face_desconhecida):

        result = []
        # face conhecida
        face_conhecida_load = cv2.imread(face_conhecida)
        rgb_face_conhecida = cv2.cvtColor(face_conhecida_load, cv2.COLOR_BGR2RGB)
        encoding_face_conhecida = face_recognition.face_encodings(rgb_face_conhecida)[0]

        # Face desconhecida
        face_desconhecida_load = cv2.imread(face_desconhecida)
        rgb_face_desconhecida = cv2.cvtColor(face_desconhecida_load, cv2.COLOR_BGR2RGB)
        # in this case, the picture can have more than just nome face, so it's an array of faces
        encoding_face_desconhecida = face_recognition.face_encodings(rgb_face_desconhecida)

        for face in encoding_face_desconhecida:
            resultado = face_recognition.compare_faces([encoding_face_conhecida], face)
            result = result + resultado

        return result
    @staticmethod
    def detect_face(face):

        image_processor = ImageProcessor()

        for i in range(4):
            image = face_recognition.load_image_file(face)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                image_processor.rotate_image(face)
            else:
                break

        if len(face_locations) == 0:
            logger.error("No face detected")
            raise NoFaceDetectedException("No face detected")

        logger.info(f"{len(face_locations)} face(s) detected")

    def validate_image(self, url_foto):
        logger.info("Validating image")
        image = self.image_service.carregar_face_desconhecida(self.image_service.encode_imagem(url_foto))
        self.detect_face(image)


