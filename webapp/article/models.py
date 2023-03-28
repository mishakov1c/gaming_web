from webapp.db import db


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), index = True)
    url = db.Column(db.String, unique=True, nullable=False)
    written = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    is_published = db.Column(db.Boolean, default=0, nullable=False)
    text = db.Column(db.Text, nullable=True)
    number_of_seen = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.Text, nullable=True)
    pic = db.Column(db.String,  nullable=True)

    author = db.relationship('User', backref='articles')
    likes = db.relationship('Like', backref='article')

    def __repr__(self) -> str:
        return '<News {} {}>'.format(self.title, self.author)