from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    written = db.Column(db.DateTime, nullable=False)
    is_published = db.Column(db.Integer, default=0, nullable=False)
    text = db.Column(db.Text, nullable=True)
    number_of_seen = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return '<News {} {}>'.format(self.title, self.author)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    regisration_date = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    birthday_date = db.Column(db.DateTime, nullable=True)
    avatar = db.Column(db.String, default='https://malvina-group.com/wp-content/uploads/2021/03/16.136.1-Pingvin-v-shapke-400x400.jpg')

    def __repr__(self):
        return '<User {} {} {}>'.format(self.username, self.email, self.id)