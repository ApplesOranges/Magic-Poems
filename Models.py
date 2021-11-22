from passlib.apps import custom_app_context as pwd_context
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

class Neruda(db.Model):
    __tablename__ = 'Neruda'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, nullable=False)
    sentence=db.Column(db.String(1000),nullable=False)

#class Benedetti(db.Model):
#    __tablename__ = 'Benedetti'
#    id = db.Column(db.Integer, primary_key=True)
#    doc_id = db.Column(db.Integer, nullable=False)
#    sentence=db.Column(db.String(1000),nullable=False)

class Borges(db.Model):
    __tablename__ = 'Borges'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, nullable=False)
    sentence=db.Column(db.String(2000),nullable=False)

#class GarciaLorca(db.Model):
#    __tablename__ = 'GarciaLorca'
#    id = db.Column(db.Integer, primary_key=True)
#    doc_id = db.Column(db.Integer, nullable=False)
#    sentence=db.Column(db.String(1000),nullable=False)

class OctavioPaz(db.Model):
    __tablename__ = 'OctavioPaz'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, nullable=False)
    sentence=db.Column(db.String(2000),nullable=False)

class UserPoem(db.Model):
    __tablename__='UserPoem'
    id = db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('User.id'),nullable=False)
    user=db.relationship('User')
    poem=db.Column(db.String(100000),nullable=False)
    title=db.Column(db.String(255),nullable=False)
    keyword=db.Column(db.String(255),nullable=False)