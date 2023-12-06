from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('livro', __name__, url_prefix='/livros')

@bp.route('/')
def index():
    db = get_db()
    livros = db.execute('SELECT * FROM livro').fetchall()
    return render_template('Livros/index.html', livros=livros)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        error = None

        if not titulo:
            error = 'Title is required.'

        if not autor:
            error = 'Autor is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO livro (titulo, autor)'
                ' VALUES (?, ?)',
                (titulo, autor)
            )
            db.commit()
            return redirect(url_for('livro.index'))

    return render_template('Livros/create.html')

@bp.route('/update/<int:ISBN>', methods=('GET', 'POST'))
def update(ISBN):

    livro = get_db().execute(
        'SELECT * FROM livro WHERE ISBN = ?',
        (ISBN,)
    ).fetchone()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        descricao = request.form['descricao']

        error = None

        if not titulo:
            error = 'Title is required.'

        if not autor:
            error = 'Autor is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE livro SET titulo = ?, autor = ?, descricao = ?'
                ' WHERE ISBN = ?',
                (titulo, autor, descricao, ISBN)
            )
            db.commit()
            return redirect(url_for('livro.index'))

    return render_template('Livros/update.html', livro=livro)

@bp.route('/delete/<int:ISBN>', methods=('POST',))
def delete(ISBN):
    db = get_db()
    db.execute('DELETE FROM livro WHERE ISBN = ?', (ISBN,))
    db.commit()
    return redirect(url_for('livro.index'))