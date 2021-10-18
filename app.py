from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy

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
    crated_at = db.Column(db.DateTime)


@app.route('/')
def hello():
    return jsonify({'msg': 'Hello world'})

@app.route("/singUp")
def signUp():
    userData=request.get_json()
    print(userData)
    return "caca"

if __name__ == "__main__":
    app.run(port=4000, debug=True)
