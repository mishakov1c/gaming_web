# import datetime
from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from webapp.article.views import blueprint as article_blueprint
from webapp.user.views import blueprint as user_blueprint
from webapp.likes.views import blueprint as likes_blueprint
from webapp.user.models import db, User


# Создание web приложения
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(article_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(likes_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        db.create_all()
    #     db.drop_all()

    return app
