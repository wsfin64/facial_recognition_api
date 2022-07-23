import cv2
import face_recognition


class ReconhecimentoService:

    @staticmethod
    def comparar_faces(face_conhecida, face_desconhecida):
        # face conhecida
        face_conhecida_load = cv2.imread(face_conhecida)
        rgb_face_conhecida = cv2.cvtColor(face_conhecida_load, cv2.COLOR_BGR2RGB)
        encoding_face_conhecida = face_recognition.face_encodings(rgb_face_conhecida)[0]

        # Face desconhecida
        face_desconhecida_load = cv2.imread(face_desconhecida)
        rgb_face_desconhecida = cv2.cvtColor(face_desconhecida_load, cv2.COLOR_BGR2RGB)
        encoding_face_desconhecida = face_recognition.face_encodings(rgb_face_desconhecida)[0]

        resultado = face_recognition.compare_faces([encoding_face_conhecida], encoding_face_desconhecida)

        return resultado[0]

