from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint('didatico', __name__, url_prefix='/didaticos')

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    didaticos = db.execute('SELECT * FROM materiais_didaticos').fetchall()
    categorias = db.execute('SELECT * FROM categoria').fetchall()
    locais = db.execute('SELECT * FROM local_fisico').fetchall()
    filtrados = None

    if request.method == 'POST':
        filtroLabel = request.form.get('filtroLabel')
        filtro = request.form.get('filtro')

        if filtro and filtroLabel:
            query = f"SELECT * FROM materiais_didaticos WHERE {filtroLabel} = ?"
            filtrados = db.execute(query, (filtro,)).fetchall()

        if not filtrados:
            flash("Nada encontrado com esses parâmetros")

    return render_template('Didaticos/index.html', didaticos=didaticos, categorias=categorias, locais=locais, filtrados=filtrados)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
@admin_required
def create():
    locais = get_db().execute(
        'SELECT * FROM local_fisico',
    ).fetchall()

    categorias = get_db().execute(
        'SELECT * FROM categoria',
    ).fetchall()

    if request.method == 'POST':
        descricao = request.form['descricao']
        numero_serie = request.form['numero_serie']
        data_aquisicao = request.form['data_aquisicao']
        estado_conservacao = request.form['estado_conservacao']
        url_foto_material = request.form['url_foto_material']
        categoria = request.form['categoria']
        localizacao_fisica = request.form['localizacao_fisica']
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
        elif not categoria:
            error = 'categoria is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO materiais_didaticos (descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material, categoria, localizacao_fisica)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material, categoria, localizacao_fisica)
            )
            db.commit()
            return redirect(url_for('didatico.index'))

    return render_template('Didaticos/create.html', categorias=categorias, locais=locais)

@bp.route('/update/<int:ID>', methods=('GET', 'POST'))
@login_required
@admin_required
def update(ID):

    didatico = get_db().execute(
        'SELECT * FROM materiais_didaticos WHERE ID = ?',
        (ID,)
    ).fetchone()

    categorias = get_db().execute(
        'SELECT * FROM categoria',
    ).fetchall()

    locais = get_db().execute(
        'SELECT * FROM local_fisico',
    ).fetchall()
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        numero_serie = request.form['numero_serie']
        data_aquisicao = request.form['data_aquisicao']
        estado_conservacao = request.form['estado_conservacao']
        url_foto_material = request.form['url_foto_material']
        localizacao_fisica = request.form['localizacao_fisica']
        categoria = request.form['categoria']
        error = None

        if not descricao:
            error = 'descricao is required.'
        elif not numero_serie:
            error = 'numero_serie is required.'
        elif not data_aquisicao:
            error = 'data_aquisicao is required.'
        elif not estado_conservacao:
            error = 'estado_conservacao is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE materiais_didaticos SET descricao = ?, numero_serie = ?, data_aquisicao = ?, estado_conservacao = ?, url_foto_material = ?, localizacao_fisica = ?, categoria = ?'
                ' WHERE ID = ?',
                (descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material, localizacao_fisica, categoria, ID)
            )
            db.commit()
            return redirect(url_for('didatico.index'))

    return render_template('Didaticos/update.html', didatico=didatico, categorias=categorias, locais=locais)

@bp.route('/delete/<int:ID>', methods=('POST',))
@login_required
@admin_required
def delete(ID):
    db = get_db()

    items_deleted = db.execute('SELECT * FROM item_emprestimo WHERE id_material = ?', (ID,)).fetchall()

    for item in items_deleted:
        db.execute('DELETE FROM emprestimo WHERE id_item = ?', (item['id'],))

    db.execute('DELETE FROM materiais_didaticos WHERE ID = ?', (ID,))
    db.commit()
    return redirect(url_for('didatico.index'))