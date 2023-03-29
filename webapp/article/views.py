import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import  current_user
from webapp.article.forms import CommentForm
from webapp.article.models import db, Articles, Comment
from webapp.config import MAIN_PAGE
from webapp.user.models import User

blueprint = Blueprint('article', __name__)


def get_post(post_id):
    post = Articles.query.get_or_404(post_id)
    return post


def new_post_url():
    max_id = db.session.query(db.func.max(Articles.id)).first()[0]
    new_id = 1 if max_id == None else max_id + 1
    new_url = f'{MAIN_PAGE}{new_id}'

    return new_url

# Переход на главную страницу
@blueprint.route('/')
def index():
    news_list = Articles.query.filter(Articles.is_published == True).order_by(Articles.edited.desc())
    return render_template('articles/index.html', news_list = news_list, current_user=current_user)


@blueprint.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    comment_form = CommentForm(article_id = post_id)
    return render_template('articles/post.html', post=post, comment_form=comment_form)


@blueprint.route('/articles/comment', methods=['POST'])
def add_comment():
    pass


@blueprint.route('/create_post', methods=('GET', 'POST'))
def create_post():
    author_id = current_user.id
    written = datetime.date.today()
    written_string = datetime.date.strftime(written, '%Y-%m-%d')
    url = new_post_url()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        description = request.form['description']
        is_published = True if type(request.form.get('is_published')) == str else False

        if not title:
            flash('Title is required!')
        else:
            new_article = Articles(title=title, url=url, written=written,
            author_id=author_id, text=content, description=description, edited=written, is_published=is_published)
            db.session.add(new_article)
            db.session.commit()
        return redirect(url_for('article.index'))

    return render_template('articles/create_post.html', author=current_user.username, written=written_string, url=url)


@blueprint.route('/<int:id>/edit_post', methods=('GET', 'POST'))
def edit_post(id):
    post = get_post(id)
    written = post.written
    written_string = datetime.date.strftime(written, '%Y-%m-%d')
    edited = datetime.date.strftime(post.edited, '%Y-%m-%d')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        description = request.form['description']
        is_published = True if type(request.form.get('is_published')) == str else False 
        
        url = request.form['url']

        if not title:
            flash('Title is required!')
        else:
            post.title = title
            post.url = url
            post.written = written
            post.edited = datetime.date.today()
            post.text = content
            post.description = description
            post.is_published = is_published
            db.session.commit()
            
            return redirect(url_for('article.index'))

    return render_template('articles/edit_post.html', post=post, written = written_string, edited = edited)