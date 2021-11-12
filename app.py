from flask import Flask, jsonify, request, make_response
from flask.json import dumps
from flask_expects_json import expects_json
from jsonschema import ValidationError
from flask_jwt import JWT, jwt_required, current_identity
from datetime import timedelta
from decouple import config as config_decouple
import json

from Models import db, User, Neruda, Benedetti, Borges, GarciaLorca, OctavioPaz,UserPoem
from schemas import signUpSchema, newPoem,savePoem
from config import configdic
from flask_cors import CORS

from utils.wordEmbedding import poem_generator


def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


enviroment = configdic['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = configdic['production']

app = create_app(enviroment)
CORS(app)

app.config['SECRET_KEY'] = 'Esto es super secreto , por favor no lo leas'
app.config['JWT_AUTH_USERNAME_KEY'] = "email"
app.config['JWT_AUTH_URL_RULE'] = "/Login"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=2)


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user


def identity(payload):
    id = payload['identity']
    return User.query.filter_by(id=id).first()


jwt = JWT(app, authenticate, identity)


# errores
@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    return error

# rutas


@app.route("/singUp", methods=['POST'])
@expects_json(signUpSchema)
def signUp():
    userData = request.get_json()
    name, lastName, email, password = userData.values()
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "email adress already taken"}), 400
    else:
        user = User(
            name=name,
            lastName=lastName,
            email=email,
            password=User.hash_password(password),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "Success"}), 200


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/new-poem')
@jwt_required()
@expects_json(newPoem)
def newPoem():
    userData = request.get_json()
    keyword, author = userData.values()
    if author == 'Octavio Paz':
        result=OctavioPaz.query.with_entities(OctavioPaz.doc_id, OctavioPaz.sentence)
        verses=[dict(i) for i in result]
        poem=poem_generator(verses,keyword)
        return jsonify({"msg": "Success",
                        "poem":poem}), 200
    elif author == 'Pablo Neruda':
        result=Neruda.query.with_entities(Neruda.doc_id, Neruda.sentence)
        verses=[dict(i) for i in result]
        poem=poem_generator(verses,keyword)
        return jsonify({"msg": "Success",
                        "poem":poem}), 200
    elif author == 'Mario Benedetti':
        result=Benedetti.query.with_entities(Benedetti.doc_id, Benedetti.sentence)
        verses=[dict(i) for i in result]
        poem=poem_generator(verses,keyword)
        return jsonify({"msg": "Success",
                        "poem":poem}), 200
    elif author == 'Garcia Lorca':
        result=GarciaLorca.query.with_entities(GarciaLorca.doc_id, GarciaLorca.sentence)
        verses=[dict(i) for i in result]
        poem=poem_generator(verses,keyword)
        return jsonify({"msg": "Success",
                        "poem":poem}), 200
    elif author == 'Jose Luis Borges':
        result=Borges.query.with_entities(Borges.doc_id, Borges.sentence)
        verses=[dict(i) for i in result]
        poem=poem_generator(verses,keyword)
        return jsonify({"msg": "Success",
                        "poem":poem}), 200

@app.route('/save-poem',methods=['POST'])
@jwt_required()
@expects_json(savePoem)
def savePoem():
    userData = request.get_json()
    poem=userData["poem"]
    keyword=userData["keyword"]
    title=userData["title"]
    userid=int('%s' % current_identity)
    userPoem=UserPoem(
        user_id=userid,
        poem=json.dumps(poem),
        title=title,
        keyword=keyword
    )
    db.session.add(userPoem)
    db.session.commit()
    return jsonify({"msg": "Success"}), 200

# main
if __name__ == "__main__":
    app.run(port=4000, debug=True)
