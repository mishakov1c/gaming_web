from flask_sqlalchemy import SQLAlchemy

user_db = SQLAlchemy()

class User(user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key=True)
    nickname = user_db.Column(user_db.String, unique=True, nullable=False)
    regisration_date = user_db.Column(user_db.DateTime, nullable=False)
    is_admin = user_db.Column(user_db.Boolean, unique=False, default=True)
    rating = user_db.Column(user_db.Integer, nullable=False, default=0)
    email = user_db.Column(user_db.String, unique=True, nullable=False)
    password = user_db.Column(user_db.String, nullable=False)
    birthday_date = user_db.Column(user_db.DateTime, nullable=False)
    avatar = user_db.Column(user_db.String, default='https://malvina-group.com/wp-content/uploads/2021/03/16.136.1-Pingvin-v-shapke-400x400.jpg')

    def __repr__(self):
        return '<User {} {} {}>'.format(self.nickname, self.email, self.id)