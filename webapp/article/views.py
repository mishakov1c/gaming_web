import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from webapp.article.forms import CommentForm
from webapp.article.models import db, Articles, Comment, Like
from webapp.config import MAIN_PAGE

blueprint = Blueprint('article', __name__)
likes_blueprint = Blueprint('likes', __name__)


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
    news_list = Articles.query.filter(Articles.is_published == True).order_by(Articles.written.desc())
    return render_template('articles/index.html', news_list = news_list, current_user=current_user)


@blueprint.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    comment_form = CommentForm(article_id = post_id)
    return render_template('articles/post.html', post=post, comment_form=comment_form)


@blueprint.route('/articles/comment', methods=['POST'])
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        if Articles.query.filter(Articles.id == form.article_id.data).first():
            comment = Comment(text=form.comment_text.data, article_id=form.article_id.data, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            flash('Комментарий успешно добавлен.')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error    
                ))
    return redirect(request.referrer) 


@blueprint.route('/create_post', methods=('GET', 'POST'))
def create_post():
    author_id = current_user.id
    written = datetime.datetime.now()
    written_string = datetime.datetime.strftime(written, '%Y-%m-%d %H:%M:%S')
    url = new_post_url()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        description = request.form['description']
        pic = request.form['pic']
        is_published = True if type(request.form.get('is_published')) == str else False

        if not title:
            flash('Title is required!')
        else:
            new_article = Articles(title=title, url=url, written=written,
            author_id=author_id, text=content, description=description, edited=written, is_published=is_published, pic=pic)
            db.session.add(new_article)
            db.session.commit()
        return redirect(url_for('article.index'))

    return render_template('articles/create_post.html', author=current_user.username, written=written_string, url=url)


@blueprint.route('/<int:id>/edit_post', methods=('GET', 'POST'))
def edit_post(id):
    post = get_post(id)
    written = post.written
    written_string = datetime.datetime.strftime(written, '%Y-%m-%d %H:%M:%S')
    edited = datetime.date.strftime(post.edited, '%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        description = request.form['description']
        is_published = True if type(request.form.get('is_published')) == str else False
        pic = request.form['pic'] 
        
        url = request.form['url']

        if not title:
            flash('Title is required!')
        else:
            post.title = title
            post.url = url
            post.written = written
            post.edited = datetime.datetime.now()
            post.text = content
            post.description = description
            post.is_published = is_published
            post.pic = pic
            db.session.commit()
            
            return redirect(url_for('article.index'))

    return render_template('articles/edit_post.html', post=post, written = written_string, edited = edited)

@blueprint.route('/like/<int:article_id>', methods=['POST'])
@login_required
def like_toggle(article_id):
    article = Articles.query.get_or_404(article_id)
    like = Like.query.filter_by(user_id=current_user.id, article_id=article_id).first()

    if not like:
        new_like = Like(user_id=current_user.id, article_id=article_id)
        db.session.add(new_like)
        db.session.commit()
    else:
        db.session.delete(like)
        db.session.commit()
    return redirect(request.referrer)

@blueprint.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query'].lower()
        if len(search_query) >= 3:
            results_list = Articles.query.filter(db.func.lower(Articles.title).like(f'%{search_query}%'))
            return render_template('articles/search_results.html', results_list=results_list)
        else:
            flash('Длина искомой строки должна быть больше 3 символов!')
    return redirect(url_for('article.index'))
