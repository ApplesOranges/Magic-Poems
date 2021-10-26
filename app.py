from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_expects_json import expects_json
from jsonschema import ValidationError
from passlib.apps import custom_app_context as pwd_context


from schemas import signUpSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:teemo230@localhost:5432/magic-poems"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    @classmethod
    def hash_password(self, password):
        return pwd_context.encrypt(password)

    @classmethod
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


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
    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "email adress already taken"}), 400
    else:
        user = Users(
            name=name,
            lastName=lastName,
            email=email,
            password=Users.hash_password(password),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "Success"}), 200


# main
if __name__ == "__main__":
    app.run(port=4000, debug=True)
