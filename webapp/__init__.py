from flask import Flask, render_template

from webapp.article_model import db
from webapp.dtf_news import get_dtf_news

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Новости игр'
        # weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = get_dtf_news()
        return render_template('index.html', page_title = title, news_list = news_list)
    
    with app.app_context():
        db.create_all()

    return app