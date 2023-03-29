from datetime import datetime
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

    def comments_count(self):
        return Comment.query.filter(Comment.article_id == self.id).count()

    def __repr__(self) -> str:
        return '<News {} {}>'.format(self.title, self.author)
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    created = db.Column(db.DateTime, nullable = False, default = datetime.now())
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete = 'CASCADE'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), index = True)

    article = db.relationship('Articles', backref='comments')
    user = db.relationship('User', backref='comments')

    def __repr__(self) -> str:
        return '<Comment {}>'.format(self.id)
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    article = db.relationship('Articles', backref='likes')
    user = db.relationship('User', backref='likes')

    def __repr__(self):
        return f'<Like {self.user_id} -> {self.article_id}>'