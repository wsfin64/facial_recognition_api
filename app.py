
from utils import Logger
from flask import Flask, jsonify, Response, request
from flask_sqlalchemy import SQLAlchemy
from service.imagem_binaria_service import ImagemService
from service.reconhecimento_service import ReconhecimentoService
from os import environ
from exceptions.no_face_detected_exception import NoFaceDetectedException


app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@{environ.get("DB_HOST")}:5432/{environ.get("DB_NAME")}'
db = SQLAlchemy(app)

imagem_service = ImagemService()
reconhecimento_service = ReconhecimentoService()

logger = Logger()


# Entidade
class Modelo(db.Model):
    __tablename__ = 'tb_modelo'
    id = db.Column(db.INTEGER, primary_key=True)
    nome = db.Column(db.String(50))
    url_foto = db.Column(db.String)

    # Formato de retorno
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "url_foto": self.url_foto}


# Cadastrar
@app.route("/modelo", methods=["POST"])
def criar_modelo():

    logger.info("Create Model Function")
    body = request.get_json()

    logger.info({"Data Received": body})

    try:

        reconhecimento_service.validate_image(body["url_foto"])

        modelo = Modelo(nome=body['nome'], url_foto=body['url_foto'])
        db.session.add(modelo)
        db.session.commit()

        logger.info(f"Model {modelo.nome} saved")

        return jsonify({"modelo": modelo.to_json(), "mensagem": "Criado com sucesso!"}), 201

    except NoFaceDetectedException as err:
        print(err)
        return jsonify({"Result": f"Cannot save this picture, {err}"}), 403
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"Erro ao criar modelo"}), 400


# Selecionar tudo
@app.route("/modelos", methods=["GET"])
def listar_modelos():
    logger.info("Listing models function")
    lista_modelos = Modelo.query.all()
    #print(lista_modelos)

    modelos_json = [modelo.to_json() for modelo in lista_modelos]

    return jsonify(modelos_json), 200


@app.route("/modelo/<id_modelo>")
def get_modelo_by_id(id_modelo):
    logger.info("Get model by id function")
    modelo = Modelo.query.filter_by(id=id_modelo).first()

    modelo_json = modelo.to_json()

    logger.info({"Model Found": modelo_json})

    return jsonify(modelo_json), 200


@app.route('/reconhecimento', methods=['POST'])
def reconhecimento():
    logger.info("Recognition Function")
    try:
        body = request.get_json()
        logger.info({"Data received": body})
        modelos = Modelo.query.all()
        lista_resposta = []
        face_desconhecida = imagem_service.carregar_face_desconhecida(imagem_service.encode_imagem(body['foto']))

        reconhecimento_service.detect_face(face_desconhecida)

        for modelo in modelos:

            face_conhecida = imagem_service.carregar_face_conhecida(imagem_service.encode_imagem(modelo.url_foto))

            resposta = reconhecimento_service.comparar_faces(face_conhecida, face_desconhecida)

            for resp in resposta:
                if resp:
                    lista_resposta.append(modelo.to_json())

        imagem_service.apagar_faces(['conhecida.jpg', 'desconhecida.jpg'])
        logger.info({"Matched Models": lista_resposta})
        return jsonify({"Result": lista_resposta}), 200

    except IndexError as err:
        logger.error(err)
        return jsonify({"Result": "Não foi possível fazer analise com imagem informada"}), 403
    except NoFaceDetectedException as err:
        print(err)
        return jsonify({"Result": f"{err}"}), 403
    except Exception as err:
        logger.error(err)
        return jsonify({"Result": "Não foi possível fazer analise com imagem informada"}), 403


# Reconhecimento específico
@app.route('/reconhecimento/individual', methods=['POST'])
def reconhecimento_por_id():

    logger.info("Recognition By Id function")

    try:

        body = request.get_json()

        logger.info({"Data received": body})

        modelo = Modelo.query.filter_by(id=body.get('id')).first()

        if modelo:

            face_conhecida = imagem_service.carregar_face_conhecida(imagem_service.encode_imagem(modelo.url_foto))
            face_desconhecida = imagem_service.carregar_face_desconhecida(imagem_service.encode_imagem(body['foto']))

            reconhecimento_service.detect_face(face_desconhecida)

            resposta = reconhecimento_service.comparar_faces(face_conhecida, face_desconhecida)

            imagem_service.apagar_faces(['conhecida.jpg', 'desconhecida.jpg'])

            for resp in resposta:
                if resp:
                    logger.info({"Model matched": modelo.nome})
                    return jsonify({"Result": True}), 200

            logger.info({"Model not matched": modelo.nome})

            return jsonify({"Result": False}), 200

        return jsonify({"Result": "Não existe modelo com o id informado"}), 404

    except NoFaceDetectedException as err:
        return jsonify({"Result": f"{err}"}), 403
    except Exception as err:
        logger.error(err)
        return jsonify({"Result": "Não foi possível fazer analise com imagem informada"}), 403


# Atualizar
@app.route("/modelo/<modelo_id>", methods=["PUT"])
def atualizar_modelo(modelo_id):
    dados_modelo = request.get_json()

    modelo = Modelo.query.filter_by(id=modelo_id).first()

    try:
        for atributo in dados_modelo.keys():
            if dados_modelo[atributo] != "":
                if atributo == 'url_foto':
                    modelo.url_foto = dados_modelo[atributo]
                if atributo == 'nome':
                    modelo.nome = dados_modelo[atributo]

        db.session.add(modelo)
        db.session.commit()
        return jsonify({"modelo": modelo.to_json(), "message": "Modelo atualizada com sucesso"}), 200
    except Exception as e:
        print(f"Erro {e}")
        return jsonify({"modelo": {}, "message": "erro ao atualizar modelo"}), 400


# Deletar
@app.route("/modelo/<modelo_id>", methods=["DELETE"])
def deletar_modelo(modelo_id):
    try:
        modelo = Modelo.query.filter_by(id=modelo_id).first()
        logger.info({"Model do delete": modelo.nome})
        db.session.delete(modelo)
        db.session.commit()

        logger.info("Model deleted")
        return jsonify({"modelo": modelo.to_json(), "message": "Modelo excluida com sucesso"}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"modelo": {}, "message": "modelo não encontrada"}), 404


if __name__ == '__main__':
    app.run()
