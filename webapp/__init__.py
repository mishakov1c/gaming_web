from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from webapp.forms import LoginForm
from webapp.model import db, Articles, User
# from webapp.dtf_news import get_dtf_news

def get_post(post_id):
    post = Articles.query.get_or_404(post_id)
    return post

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    @app.route('/')
    def index():
        title = 'Geek Space'
        text = request.args.get('button_text')
        print()
        print('Button_text = ', text)
        print()
        news_list = Articles.query.order_by(Articles.written.desc()).all()
        # news_list = get_dtf_news()
        return render_template('index.html', page_title = title, news_list = news_list)
    
    @app.route('/edit/<int:post_id>')
    def edit_post(post_id):
        text = request.args.get('button_text')
        print()
        print('Button_text = ', text)
        print()
        post = get_post(post_id)
        return render_template('edit_post.html', page_title = post.title, post_text=post.text, post_id=post_id)

    @app.route('/<int:post_id>')
    def post(post_id):
        post = get_post(post_id)
        return render_template('post.html', page_title = post.title, post_text=post.text) 

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
    
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))
            
        flash('Неправильные имя или/и пароль')
        return redirect(url_for('login'))
    
    @app.route('/logout')
    def logout():
        flash('Вы успешно вышли из аккаунта.')
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет, Админ!'
        else:
            return 'Ты не Админ!'

    @app.route('/save_article', methods=['POST'])
    def save_article():
        title = 'Сохранение статьи'
        return title
        # new_articles = Articles(title=title, url=url, written=written, author='unknown', is_published = 1)
        # db.session.add(new_articles)
        # db.session.commit()
        # return render_template('login.html', page_title=title, form=login_form)
    

    with app.app_context():
        db.create_all()

    return app