from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Post')
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.__create_password(password)


    def __create_password(self, password):
        return generate_password_hash(password)

    
    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    __tablename__ = 'posts'


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
