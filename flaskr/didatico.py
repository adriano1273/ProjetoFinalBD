from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint('didatico', __name__, url_prefix='/didaticos')

@bp.route('/')
def index():
    db = get_db()
    didaticos = db.execute('SELECT * FROM materiais_didaticos').fetchall()
    return render_template('Didaticos/index.html', didaticos=didaticos)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
@admin_required
def create():
    if request.method == 'POST':
        descricao = request.form['descricao']
        numero_serie = request.form['numero_serie']
        data_aquisicao = request.form['data_aquisicao']
        estado_conservacao = request.form['estado_conservacao']
        url_foto_material = request.form['url_foto_material']
        error = None

        if not descricao:
            error = 'descricao is required.'
        elif not numero_serie:
            error = 'numero_serie is required.'
        elif not data_aquisicao:
            error = 'data_aquisicao is required.'
        elif not estado_conservacao:
            error = 'estado_conservacao is required.'
        elif not url_foto_material:
            error = 'url_foto_material is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO materiais_didaticos (descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material)'
                ' VALUES (?, ?, ?, ?, ?)',
                (descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material)
            )
            db.commit()
            return redirect(url_for('didatico.index'))

    return render_template('Didaticos/create.html')

@bp.route('/update/<int:ID>', methods=('GET', 'POST'))
@login_required
@admin_required
def update(ID):

    didatico = get_db().execute(
        'SELECT * FROM materiais_didaticos WHERE ID = ?',
        (ID,)
    ).fetchone()
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        numero_serie = request.form['numero_serie']
        data_aquisicao = request.form['data_aquisicao']
        estado_conservacao = request.form['estado_conservacao']
        url_foto_material = request.form['url_foto_material']
        error = None

        if not descricao:
            error = 'descricao is required.'
        elif not numero_serie:
            error = 'numero_serie is required.'
        elif not data_aquisicao:
            error = 'data_aquisicao is required.'
        elif not estado_conservacao:
            error = 'estado_conservacao is required.'
        elif not url_foto_material:
            error = 'url_foto_material is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE materiais_didaticos SET descricao = ?, numero_serie = ?, data_aquisicao = ?, estado_conservacao = ?, url_foto_material = ?'
                ' WHERE ID = ?',
                (descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material, ID)
            )
            db.commit()
            return redirect(url_for('didatico.index'))

    return render_template('Didaticos/update.html', didatico=didatico)

@bp.route('/delete/<int:ID>', methods=('POST',))
@login_required
@admin_required
def delete(ID):
    db = get_db()
    db.execute('DELETE FROM materiais_didaticos WHERE ID = ?', (ID,))
    db.commit()
    return redirect(url_for('didatico.index'))