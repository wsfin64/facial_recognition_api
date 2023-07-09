import io
import time

from PIL import Image, ImageFile
from services.file_types import is_jpeg
import face_recognition
import cv2
# import pytesseract

from utils import Logger

logger = Logger()


class ImageProcessor(object):
    def __init__(self):
        self.image_modified = ''
        self.image_type = ''

    @staticmethod
    def rotate_image(image_path: str) -> None:

        logger.info("Rotate Image Function")

        with open(image_path, 'rb') as file:
            imagem_binaria = file.read()

        img = Image.open(io.BytesIO(imagem_binaria))
        img = img.convert('RGB')

        img.rotate(angle=90.0, expand=1).save(image_path)



if __name__ == '__main__':
    import cv2

    # face_conhecida_load = cv2.imread('../skin.jpg')
    # rgb_face_conhecida = cv2.cvtColor(face_conhecida_load, cv2.COLOR_BGR2RGB)
    # encoding_face_conhecida = face_recognition.face_encodings(rgb_face_conhecida)[0]

    # image_path = '../teste2.jpg'

    # image = face_recognition.load_image_file(image_path)
    # face_landmarks_list = face_recognition.face_locations(image)
    # print(face_landmarks_list)

    # for face in face_landmarks_list:
        # face_desconhecida_load = cv2.imread(face)
        # rgb_face_desconhecida = cv2.cvtColor(face_desconhecida_load, cv2.COLOR_BGR2RGB)
        # encoding_face_desconhecida = face_recognition.face_encodings(rgb_face_desconhecida)[0]



    # if len(face_landmarks_list) == 0:
        # raise Exception("No face detected")

    # cascade_path = '../cascade.xml'
    #
    # carrega_algoritmo = cv2.CascadeClassifier(cascade_path)  # Carregando o algoritomo
    #
    # img = cv2.imread(image_path)  # Carregando a imagem
    #
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convertendo a imagem para preto e branco
    #
    # faces = carrega_algoritmo.detectMultiScale(gray, 1.3, 10, minSize=(100, 100))
    #
    # print(faces)
    # # [[351 103 232 232]]
    #
    # if len(faces) == 0:
    #     raise Exception("No faces detected")
    #
    # for (x, y, w, h) in faces:
    #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
    #
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    for i in range(1):
        print("start")

        with open('../img/aria.jpg', 'rb') as file:
            imagem_binaria = file.read()

        img = Image.open(io.BytesIO(imagem_binaria))
        img = img.convert('RGB')
        # params = '--psm 0 -c min_characters_to_try=25'
        # osd = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT, config=params)
        # print(str(osd))

        img.rotate(angle=90.0, expand=1).save("../img/aria.jpg")
        print(f"Rotated {i}")




        # with open("../teste.jpg", 'wb') as file:
        #     file.write(rotated)

        # rotated.show()
