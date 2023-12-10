from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint('local', __name__, url_prefix='/locais')

@bp.route('/')
def index():
    db = get_db()
    locais = db.execute('SELECT * FROM local_fisico').fetchall()
    return render_template('Local/index.html', locais=locais)

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
                'INSERT INTO local_fisico (nome)'
                ' VALUES (?)',
                (nome,)
            )
            db.commit()
            return redirect(url_for('local.index'))

    return render_template('Local/create.html')

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_required
def update(id):

    local = get_db().execute(
        'SELECT * FROM local_fisico WHERE id = ?',
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
                'UPDATE local_fisico SET nome = ?'
                ' WHERE id = ?',
                (nome, id)
            )
            db.commit()
            return redirect(url_for('local.index'))

    return render_template('Local/update.html', local=local)

@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
@admin_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM local_fisico WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('local.index'))