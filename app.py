
from utils import Logger
from flask import Flask, jsonify, Response, request
from services.imagem_binaria_service import ImagemService
from services.reconhecimento_service import ReconhecimentoService
from os import environ
from exceptions.no_face_detected_exception import NoFaceDetectedException
import uuid
from services.message_service import MessagePublisher
from services.mongoService import MongoService
from entities.individual import IndividualSchema
from marshmallow.exceptions import ValidationError


app = Flask(__name__)


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{environ.get("DB_USER")}:{environ.get("DB_PASS")}@{environ.get("DB_HOST")}:5432/{environ.get("DB_NAME")}'
# db = SQLAlchemy(app)

imagem_service = ImagemService()
reconhecimento_service = ReconhecimentoService()
mongo_service = MongoService()

logger = Logger()

# Cadastrar
@app.route("/modelo", methods=["POST"])
def criar_modelo():

    logger.info("Create Model Function")
    body = request.get_json()

    logger.info({"Data Received": body})

    try:

        reconhecimento_service.validate_image(body["url_foto"])

        individual = IndividualSchema().load(body)
        individual['id'] = str(uuid.uuid4())
        mongo_service.save_individual(individual)

        return jsonify({"modelo": individual, "mensagem": "Criado com sucesso!"}), 201

    except NoFaceDetectedException as err:
        print(err)
        return jsonify({"Result": f"Cannot save this picture, {err}"}), 403
    except ValidationError as err:
        return jsonify({"Error ao criar modelo": str(err)})
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"Erro ao criar modelo"}), 400


# Selecionar tudo
@app.route("/modelos", methods=["GET"])
def listar_modelos():
    try:
        logger.info("Listing models function")

        lista_modelos = mongo_service.find_all_individuals()

        modelos_json = [modelo for modelo in lista_modelos]

        return jsonify(modelos_json), 200
    except Exception as e:
        logger.error(e)
        return jsonify({"Error": e}), 500


@app.route("/modelo/<id_modelo>")
def get_modelo_by_id(id_modelo):
    logger.info("Get model by id function")

    try:

        modelo = mongo_service.find_individual_by_id(id_modelo)

        logger.info({"Model Found": modelo})

        return jsonify(modelo), 200
    except Exception as e:
        print(e)
        logger.error(e)
        return jsonify({"Error": e}), 500


@app.route('/reconhecimento', methods=['POST'])
def reconhecimento():

    logger.info("Recognition Function")
    try:
        body = request.get_json()
        print({"Data received": body})

        foto = imagem_service.carregar_face_desconhecida(imagem_service.encode_imagem(body.get('foto')))

        faces = reconhecimento_service.detect_face(foto)


        body['processId'] = str(uuid.uuid4())
        body['facesDetected'] = faces
        body['status'] = 'PENDING'

        mongo_service.save_analysis(body)
        print(body)

        message = MessagePublisher()
        message.send_message(body)


        return jsonify({"processId": body.get("processId"), "status": body.get('status')}), 200

        ##### criar consumer #########

        # modelos = Modelo.query.all()
        # lista_resposta = []
        # face_desconhecida = imagem_service.carregar_face_desconhecida(imagem_service.encode_imagem(body['foto']))
        #
        # reconhecimento_service.detect_face(face_desconhecida)
        #
        # for modelo in modelos:
        #
        #     face_conhecida = imagem_service.carregar_face_conhecida(imagem_service.encode_imagem(modelo.url_foto))
        #
        #     resposta = reconhecimento_service.comparar_faces(face_conhecida, face_desconhecida)
        #
        #     for resp in resposta:
        #         if resp:
        #             lista_resposta.append(modelo.to_json())
        #
        # imagem_service.apagar_faces(['conhecida.jpg', 'desconhecida.jpg'])
        # logger.info({"Matched Models": lista_resposta})
        # return jsonify({"Result": lista_resposta}), 200

    except IndexError as err:
        logger.error(err)
        return jsonify({"Result": "Não foi possível fazer analise com imagem informada"}), 403
    except NoFaceDetectedException as err:
        print(err)
        return jsonify({"Result": f"{err}"}), 403
    except Exception as err:
        logger.error(err)
        print(err)
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


@app.route('/analysis/<processId>', methods=['GET'])
def get_analysis_result(processId: str) -> dict:

    try:
        analysis = mongo_service.find_analysis_by_processId(processId)

        if analysis:
            return jsonify({"Result": analysis}), 200

        return jsonify({"Result": "No process was found with the informed processId"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "algo deu errado"}), 500


if __name__ == '__main__':
    app.run()
