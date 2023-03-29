from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()], render_kw={'class': "form-control"})
    text = TextAreaField('Текст статьи', validators=[DataRequired()], render_kw={'class': "form-control"})
    url = StringField('Адрес статьи', validators=[DataRequired()], render_kw={'class': "form-control"})


class CommentForm(FlaskForm):
    article_id = HiddenField('ID статьи', validators=[DataRequired()])
    comment_text = StringField('Ваш комментарий', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-primary"})
