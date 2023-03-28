from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class ArticleForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()], render_kw={'class': "form-control"})
    text = TextAreaField('Текст статьи', validators=[DataRequired()], render_kw={'class': "form-control"})
    url = StringField('Адрес статьи', validators=[DataRequired()], render_kw={'class': "form-control"})


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={'class': "form-check-input"})
    submit = SubmitField('Отправить', render_kw={'class': "btn btn-primary"})


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': "form-control"})
    email = StringField('Имейл', validators=[DataRequired(), Email()], render_kw={'class': "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': "form-control"})
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={'class': "form-control"})
    submit = SubmitField('Зарегистрироваться', render_kw={'class': "btn btn-primary"})
