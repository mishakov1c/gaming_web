from flask import Flask, render_template

from webapp.article_model import db, Articles
from webapp.dtf_news import get_dtf_news

def get_post(post_id):
    post = Articles.query.get_or_404(post_id)
    return post


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Новости игр'
        news_list = Articles.query.order_by(Articles.written.desc()).all()
        # news_list = get_dtf_news()
        return render_template('index.html', page_title = title, news_list = news_list)
    
    
    @app.route('/edit/<int:post_id>')
    def edit_post(post_id):
        post = get_post(post_id)
        return render_template('edit_post.html', page_title = post.title, post_text=post.text, post_id=post_id)
    
    
    @app.route('/<int:post_id>')
    def post(post_id):
        post = get_post(post_id)
        return render_template('post.html', page_title = post.title, post_text=post.text) 

    with app.app_context():
        db.create_all()

    return app
 

    

    

    