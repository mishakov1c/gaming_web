import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import  current_user
from webapp.article.models import db, Articles
from webapp.config import MAIN_PAGE

blueprint = Blueprint('article', __name__)

def get_post(post_id):
    post = Articles.query.get_or_404(post_id)
    return post

# Переход на главную страницу
@blueprint.route('/')
def index():
    news_list = Articles.query.filter(Articles.is_published == True)
    return render_template('news/index.html', news_list = news_list, current_user=current_user)


@blueprint.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('news/post.html', post=post)

def new_post_url():
    max_id = db.session.query(db.func.max(Articles.id)).first()[0]
    new_id = 1 if max_id == None else max_id + 1
    new_url = f'{MAIN_PAGE}{new_id}'

    return new_url

@blueprint.route('/create_post', methods=('GET', 'POST'))
def create_post():
    author = current_user.username
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
            author=author, text=content, description=description, edited=written, is_published=is_published)
            db.session.add(new_article)
            db.session.commit()
        return redirect(url_for('article.index'))

    return render_template('news/create_post.html', author=author, written=written_string, url=url)


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
        author = request.form['author']
        is_published = True if type(request.form.get('is_published')) == str else False 
        
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
            post.is_published = is_published
            db.session.commit()
            
            return redirect(url_for('article.index'))

    return render_template('news/edit_post.html', post=post, written = written_string, edited = edited)