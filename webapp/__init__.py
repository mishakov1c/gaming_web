import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from webapp.config import MAIN_PAGE
from webapp.forms import LoginForm, ArticleForm
from webapp.model import db, Articles, User


def get_post(post_id):
    post = Articles.query.get_or_404(post_id)
    return post


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        news_list = Articles.query.order_by(Articles.written.desc()).all()
        print(news_list)
        return render_template('index.html', news_list = news_list, current_user=current_user)
    

    @app.route('/<int:post_id>')
    def post(post_id):
        post = get_post(post_id)
        return render_template('post.html', post=post)

    def new_post_url():
        new_id = db.session.query(db.func.max(Articles.id)).first()[0] + 1
        new_url = f'{MAIN_PAGE}{new_id}'

        return new_url

    @app.route('/create_post', methods=('GET', 'POST'))
    def create_post():
        author = current_user.username
        written = datetime.date.today()
        written_string = datetime.date.strftime(written, '%Y-%m-%d')
        url = new_post_url()

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            description = request.form['description']
            # print(request.form)

            if not title:
                flash('Title is required!')
            else:
                new_article = Articles(title=title, url=url, written=written,
                author=author, text=content, description=description, edited=written)
                # , is_published=is_published)
                db.session.add(new_article)
                db.session.commit()
            return redirect(url_for('index'))

        return render_template('create_post.html', author=author, written=written_string, url=url)


    @app.route('/<int:id>/edit_post', methods=('GET', 'POST'))
    def edit_post(id):
        post = get_post(id)
        written = post.written
        written_string = datetime.date.strftime(written, '%Y-%m-%d')
        edited = datetime.date.strftime(post.edited, '%Y-%m-%d')

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            description = request.form['description']
            author = request.form['author']
            # is_published = request.form['is_published']
            
            url = request.form['url']

            if not title:
                flash('Title is required!')
            else:
                post.title = title
                post.url = url
                post.written = written
                post.edited = datetime.date.today()
                post.author = author
                post.text = content
                post.description = description
                # post.is_published = is_published
                db.session.commit()
                
                return redirect(url_for('index'))

        return render_template('edit_post.html', post=post, written = written_string, edited = edited)
    

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

    # with app.app_context():
    #     db.create_all()
    #     db.drop_all()

    return app
