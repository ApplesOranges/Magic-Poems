from flask import Flask, jsonify, request, make_response
from flask_expects_json import expects_json
from jsonschema import ValidationError
from flask_jwt import JWT, jwt_required, current_identity

from schemas import signUpSchema


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:teemo230@localhost:5432/magic-poems"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'super-secret'

from Models import db, User

def authenticate(email,password):
    user=User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user

def identity(payload):
    id,name, lastName, email, password=payload.values()
    return User.query.filter_by(id=5).first()

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
        print(password)
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

@app.route("/test")
def test():
    user=authenticate("ivanwhitetest@gmail.com","Test1234&&")
    print(user)
    return jsonify({"msg":"simon"}),200

# main
if __name__ == "__main__":
    db.create_all()
    app.run(port=4000, debug=True)
