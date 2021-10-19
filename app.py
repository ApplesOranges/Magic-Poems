from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_expects_json import expects_json
from sqlalchemy.orm import session

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



signUpSchema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', "maxLength": 255},
        'lastName': {'type': 'string', "maxLength": 255},
        'email': {'type': 'string', "pattern": "[^@]+@[^@]+\.[^@]"},
        'password': {'type': 'string', "pattern": "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=]).*$"}
    },
    'required': ['name', 'lastName', 'email', 'password']
}


@app.route('/')
def hello():
    return jsonify({'msg': 'Hello world'})


@app.route("/singUp",methods=['POST'])
@expects_json(signUpSchema)
def signUp():
    userData = request.get_json()
    user=Users(
        name=userData['name'],
        lastName=userData['lastName'],
        email=userData['email'],
        password=userData['password'],
        )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg":"Success"}),200

if __name__ == "__main__":
    app.run(port=4000, debug=True)
