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