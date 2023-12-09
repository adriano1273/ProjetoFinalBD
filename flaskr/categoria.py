from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint('categoria', __name__, url_prefix='/categorias')

@bp.route('/')
def index():
    db = get_db()
    categorias = db.execute('SELECT * FROM categoria').fetchall()
    return render_template('Categorias/index.html', categorias=categorias)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
@admin_required
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        error = None

        if not nome:
            error = 'nome is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO categoria (nome)'
                ' VALUES (?)',
                (nome,)
            )
            db.commit()
            return redirect(url_for('categoria.index'))

    return render_template('Categorias/create.html')

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_required
def update(id):

    categoria = get_db().execute(
        'SELECT * FROM categoria WHERE id = ?',
        (id,)
    ).fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        error = None

        if not nome:
            error = 'nome is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE categoria SET nome = ?'
                ' WHERE id = ?',
                (nome, id)
            )
            db.commit()
            return redirect(url_for('categoria.index'))

    return render_template('Categorias/update.html', categoria=categoria)

@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
@admin_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM categoria WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('categoria.index'))