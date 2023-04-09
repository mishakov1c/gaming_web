from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user

from webapp.user.decorators import admin_required
from webapp.forms import LoginForm, RegisterForm
from webapp.user.models import db, User
from webapp.article.models import Articles, Like
from validate_email import validate_email

blueprint = Blueprint('user', __name__)

@blueprint.route('/register')
def register():
    r"""Проверяем, если пользователь залогинен.
        Если ДА, перенаправляем его на страницу index.html
        Если НЕТ, перенаправляем его на страницк register.html"""

    if current_user.is_authenticated:
        return redirect(url_for('article.index'))
    title = 'Регистрация'
    register_form = RegisterForm()
    return render_template('user/register.html', page_title=title, form=register_form)

@blueprint.route('/process-register', methods=['GET', 'POST'])
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
            return redirect(url_for('user.register'))
        elif User.query.filter_by(email=email.data).first():
            flash('Пользователь с таким имейлом уже существует!')
            return redirect(url_for('user.register'))
        elif not validate_email(form.email.data):
            flash('Некорректный имейл')
            return redirect(url_for('user.register'))
        elif not password1 == password2:
            flash('Пароли не одинаковые!')
            return redirect(url_for('user.register'))
        elif len(password1) < 6 and password1 != 'qwe':
            flash('Пароль слишком короткий, введите не менее 6 символов!')
            return redirect(url_for('user.register'))

        if password1 == 'qwe':    
            new_user = User(username=username.data, email=email.data, role='admin')
        else:
            new_user = User(username=username.data, email=email.data, role='user')
        new_user.set_password(password1)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('article.index'))
    
@blueprint.route('/login')
def login():
    r"""Проверяем, если пользователь залогинен.
        Если ДА, перенаправляем его на страницу index.html
        Если НЕТ, перенаправляем его на страницк login.html"""

    if current_user.is_authenticated:
        return redirect(url_for('article.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
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
        if user and not user.is_active:
            flash('Действие учётной записи ограничено!')
            return redirect(url_for('user.login'))
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('article.index'))

    flash('Неправильные имя или/и пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    flash('Вы успешно вышли из аккаунта.')
    logout_user()
    return redirect(url_for('article.index'))


@blueprint.route('/user/<string:username>', methods=['GET'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Такого пользователя не существует")
        return redirect(url_for('article.index'))
    news_list = Articles.query.filter(Articles.author == user)
    favorite_list = Articles.query.join(Like, Like.article_id == Articles.id).filter(Like.user_id == user.id).all()
    return render_template("user/profile.html", user=user, news_list=news_list, favorite_list=favorite_list)

@blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        old_password = request.form['old_password']
        new_password = request.form['password']

        if User.query.filter(User.username == username, User.id != current_user.id).first():
            flash('Этот логин уже занят. Пожалуйста, выберите другой.')
            return redirect(url_for('user.edit_profile'))

        if User.query.filter(User.email == email, User.id != current_user.id).first():
            flash('Этот email уже занят. Пожалуйста, выберите другой.')
            return redirect(url_for('user.edit_profile'))
        
        if old_password and not current_user.check_password(old_password):
            flash('Неправильный старый пароль. Попробуйте еще раз')
            return redirect(url_for('user.edit_profile'))
        
        current_user.username = username
        current_user.email = email
        if new_password and new_password != old_password:
            current_user.set_password(new_password)
            flash('Профиль успешно обновлен.')
        elif new_password and new_password == old_password:
            flash('Пароли одинаковые!')
        db.session.commit()
    return redirect(url_for('user.profile', username=current_user.username))

@blueprint.route('/block_user/<int:user_id>', methods=['POST'])
@admin_required
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    if not user.is_active:
        flash(f'Пользователь {user.username} заблокирован, поделом ему!')
    else:
        flash(f'Пользователь {user.username} разблокирован, поняли и простили!')
    return redirect(request.referrer)