from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()], render_kw={'class': "form-control"})
    text = TextAreaField('Текст статьи', validators=[DataRequired()], render_kw={'class': "form-control"})
    url = StringField('Адрес статьи', validators=[DataRequired()], render_kw={'class': "form-control"})


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': "form-control"})
    submit = SubmitField('Отправить', render_kw={'class': "btn btn-primary"})