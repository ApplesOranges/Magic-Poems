from flask import Flask, jsonify, request, make_response
from flask_expects_json import expects_json
from jsonschema import ValidationError
from flask_jwt import JWT, jwt_required, current_identity
from datetime import timedelta
from decouple import config as config_decouple

from Models import db, User
from schemas import signUpSchema
from config import configdic


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

app.config['SECRET_KEY'] = 'el-kevin-se-la-come'
app.config['JWT_AUTH_USERNAME_KEY']="email"
app.config['JWT_AUTH_URL_RULE']="/Login"
app.config['JWT_EXPIRATION_DELTA']=timedelta(days=2)



def authenticate(email,password):
    user=User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user

def identity(payload):
    id=payload['identity']
    return User.query.filter_by(id=id).first()

jwt = JWT(app, authenticate, identity)


# errores
@ app.errorhandler(400)
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


# main
if __name__ == "__main__":
    app.run(port=4000, debug=True)
