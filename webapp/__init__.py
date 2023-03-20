import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from webapp.config import MAIN_PAGE
from webapp.forms import LoginForm, ArticleForm, RegisterForm
from webapp.model import db, Articles, User


def get_post(post_id):
    post = Articles.query.get_or_404(post_id)
    return post

# Создание web приложения
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

# Переход на главную страницу
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
        max_id = db.session.query(db.func.max(Articles.id)).first()[0]
        new_id = 1 if max_id == None else max_id + 1
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
    
    @app.route('/register')
    def register():
        r"""Проверяем, если пользователь залогинен.
            Если ДА, перенаправляем его на страницу index.html
            Если НЕТ, перенаправляем его на страницк register.html"""

        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Регистрация'
        register_form = RegisterForm()
        return render_template('register.html', page_title=title, form=register_form)
    @app.route('/process-register', methods=['GET', 'POST'])
    def process_register():

        form = RegisterForm()

        if form.validate_on_submit():
            username = form.username
            email = form.email
            password1 = form.password.data
            password2 = form.confirm_password.data

            if User.query.filter_by(username=username.data).first():
                flash('Пользователь с таким именем уже существует!')
                print(User.username)
                return redirect(url_for('register'))
            elif User.query.filter_by(email=email.data).first():
                flash('Пользователь с таким имейлом уже существует!')
                return redirect(url_for('register'))
            elif not password1 == password2:
                flash('Пароли не одинаковые!')
                return redirect(url_for('register'))
                
            new_user = User(username=username.data, email=email.data, role='user')
            new_user.set_password(password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('index'))
        
    @app.route('/login')
    def login():
        r"""Проверяем, если пользователь залогинен.
            Если ДА, перенаправляем его на страницу index.html
            Если НЕТ, перенаправляем его на страницк login.html"""

        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        r"""Маршрут, который обрабатывает информацию, полученную из полей
        данных для входа в аккаунт в login.html. Создается форма из flask-login,
        Потом проверяем, была ли отправлена форма и прошла ли она валидацию.
        Мы берем пользователя из баззы данных, чей юзернейм нам передали и 
        проверяем схожесть паролей. Если всё ОК, то пользователь заходит в 
        сеть под этим ником и остается онлайн с помощью flask-login"""

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

    with app.app_context():
        db.create_all()
    #     db.drop_all()

    return app
