from flask import Flask, jsonify, Response, request
from flask_sqlalchemy import SQLAlchemy
from service.imagem_binaria_service import ImagemService
from service.reconhecimento_service import ReconhecimentoService


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:wlfc@localhost:5432/faces'
db = SQLAlchemy(app)

imagem_service = ImagemService()
reconhecimento_service = ReconhecimentoService()


# Entidade
class Modelo(db.Model):
    __tablename__ = 'tb_modelo'
    id = db.Column(db.INTEGER, primary_key=True)
    nome = db.Column(db.String(50))
    url_foto = db.Column(db.String)
    foto_binaria = db.Column(db.BINARY)

    # Formato de retorno
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "url_foto": self.url_foto}


# Cadastrar
@app.route("/modelo", methods=["POST"])
def criar_modelo():
    body = request.get_json()
    imagem_binaria = imagem_service.encode_imagem(body['url_foto'])

    try:
        modelo = Modelo(nome=body['nome'], url_foto=body['url_foto'], foto_binaria=imagem_binaria)
        db.session.add(modelo)
        db.session.commit()

        return jsonify({"modelo": modelo.to_json(), "mensagem": "Criado com sucesso!"}), 201
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"Erro ao criar modelo"}), 400


# Selecionar tudo
@app.route("/modelos", methods=["GET"])
def listar_modelos():
    lista_modelos = Modelo.query.all()
    #print(lista_modelos)

    modelos_json = [modelo.to_json() for modelo in lista_modelos]

    return jsonify(modelos_json), 200


@app.route("/modelo/<id_modelo>")
def get_modelo_by_id(id_modelo):
    modelo = Modelo.query.filter_by(id=id_modelo).first()

    modelo_json = modelo.to_json()

    return jsonify(modelo_json), 200


@app.route('/reconhecimento', methods=['POST'])
def reconhecimento():
    try:
        body = request.get_json()
        modelos = Modelo.query.all()
        lista_resposta = []

        for modelo in modelos:

            face_conhecida = imagem_service.carregar_face_conhecida(modelo.foto_binaria)
            face_desconhecida = imagem_service.carregar_face_desconhecida(imagem_service.encode_imagem(body['foto']))

            resposta = reconhecimento_service.comparar_faces(face_conhecida, face_desconhecida)
            if resposta:
                lista_resposta.append(modelo.to_json())

        imagem_service.apagar_faces('conhecida.jpg')
        imagem_service.apagar_faces('desconhecida.jpg')
        return jsonify({"Result": lista_resposta}), 200

    except IndexError as err:
        return jsonify({"Result": "Não foi possível fazer analise com imagem informada"}), 403


if __name__ == '__main__':
    app.run()
