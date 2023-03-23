from flask_login import UserMixin
from webapp.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    regisration_date = db.Column(db.DateTime)
    role = db.Column(db.String(20), index=True)
    rating = db.Column(db.Integer, default=0)
    email = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(128))
    birthday_date = db.Column(db.DateTime)
    avatar = db.Column(db.String, default='https://malvina-group.com/wp-content/uploads/2021/03/16.136.1-Pingvin-v-shapke-400x400.jpg')
    
    r"""Первая функция меняет пароль на переданный
        перед этим его зашифровав.

        Вторая - проверяет с помощью той же генерации шифровки,
        если пароли одинаковые.
        
        Третья - проверяет, является ли пользователь адвминистратором"""
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    def __repr__(self):
        return '<User {} {} {}>'.format(self.username, self.email, self.id)
