from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from portal.auth import login_required
from portal.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, tittle, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, tittle, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] !=g.user['id']:
        abort(403)

    return post

@bp.route('/create', methods=(['GET', 'POST']))
@login_required
def create():
    if request.method == 'POST':
        tittle = request.form['tittle']
        body = request.form['body']
        error = None

        if not tittle:
            error = 'Tittle is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (tittle, body, author_id)'
                ' VALUE (?, ?, ?)',
                (tittle, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        tittle = request.form['tittle']
        body = request.form['body']
        error = None

        if not tittle:
            error = 'Tittle is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                ' UPDATE post SET tittle = ?, body = ?'
                ' WHERE id = ?',
                (tittle, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for("blog.index"))