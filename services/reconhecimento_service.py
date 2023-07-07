import cv2
import face_recognition
from exceptions.no_face_detected_exception import NoFaceDetectedException
from services.imagem_binaria_service import ImagemService
from utils import Logger
from services.image_processor import ImageProcessor
from services.mongoService import MongoService

logger = Logger()


class ReconhecimentoService:

    def __init__(self):
        self.image_service = ImagemService()

    @staticmethod
    def comparar_faces(face_conhecida_path: str, face_desconhecida_path: str) -> list:
        """
        Compare the faces in the two picures
        """

        result = []
        # face conhecida
        face_conhecida_load = cv2.imread(face_conhecida_path)
        rgb_face_conhecida = cv2.cvtColor(face_conhecida_load, cv2.COLOR_BGR2RGB)
        encoding_face_conhecida = face_recognition.face_encodings(rgb_face_conhecida)[0]

        # Face desconhecida
        face_desconhecida_load = cv2.imread(face_desconhecida_path)
        rgb_face_desconhecida = cv2.cvtColor(face_desconhecida_load, cv2.COLOR_BGR2RGB)
        # in this case, the picture can have more than just nome face, so it's an array of faces
        encoding_face_desconhecida = face_recognition.face_encodings(rgb_face_desconhecida)

        for face in encoding_face_desconhecida:
            resultado = face_recognition.compare_faces([encoding_face_conhecida], face)
            result = result + resultado

        return result

    @staticmethod
    def detect_face(picture_path: str) -> None:
        """
        Detects if there is one or more faces in the picture
        """

        image_processor = ImageProcessor()
        face_locations = []

        for i in range(4):
            image = face_recognition.load_image_file(picture_path)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                image_processor.rotate_image(picture_path)
            else:
                break

        if len(face_locations) == 0:
            logger.warning("No face detected")
            raise NoFaceDetectedException("No face detected")

        logger.info(f"{len(face_locations)} face(s) detected")

    def validate_image(self, url_foto: str) -> None:
        logger.info("Validating image")
        image = self.image_service.carregar_face_desconhecida(self.image_service.encode_imagem(url_foto))
        self.detect_face(image)

    def recognize(self, payload):
        try:
            mongo_service = MongoService()
            modelos = mongo_service.find_all_individuals()
            document_analysis = mongo_service.find_analysis_by_processId(payload.get('processId'))
            lista_resposta = []

            imagem_service = ImagemService()
            face_desconhecida = imagem_service.carregar_face_desconhecida(imagem_service.encode_imagem(payload['foto']))


            self.detect_face(face_desconhecida)

            for modelo in modelos:

                face_conhecida = imagem_service.carregar_face_conhecida(
                    imagem_service.encode_imagem(modelo.get('url_foto')))

                resposta = self.comparar_faces(face_conhecida, face_desconhecida)

                for resp in resposta:
                    if resp:
                        lista_resposta.append(modelo)

            imagem_service.apagar_faces(['conhecida.jpg', 'desconhecida.jpg'])
            document_analysis["status"] = 'FINISHED'
            document_analysis["modelsMatched"] = lista_resposta
            mongo_service.update_analysis(document_analysis)
            logger.info({"Updated Document": document_analysis})
            print({"Matched Models": lista_resposta, "processId": payload.get('processId')})
        except Exception as e:
            raise e

