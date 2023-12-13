from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required, admin_required
from flaskr.db import get_db

bp = Blueprint('livro', __name__, url_prefix='/livros')

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    livros = db.execute('SELECT * FROM livro').fetchall()
    categorias = db.execute('SELECT * FROM categoria').fetchall()
    locais = db.execute('SELECT * FROM local_fisico').fetchall()
    filtrados = None

    if request.method == 'POST':
        filtroLabel = request.form.get('filtroLabel')
        filtro = request.form.get('filtro')

        if filtro and filtroLabel:
            query = f"SELECT * FROM livro WHERE {filtroLabel} LIKE ?"
            filtrados = db.execute(query, (f"%{filtro}%",)).fetchall()

        if not filtrados:
            flash("Nada encontrado com esses parâmetros")

    return render_template('Livros/index.html', livros=livros, categorias=categorias, locais=locais, filtrados=filtrados)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@admin_required
def create():
    categorias = get_db().execute(
        'SELECT * FROM categoria',
    ).fetchall()

    locais = get_db().execute(
        'SELECT * FROM local_fisico',
    ).fetchall()

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        descricao = request.form['descricao']
        data_aquisicao = request.form['data_aquisicao']
        estado_conservacao = request.form['estado_conservacao']
        url_foto_capa = request.form['url_foto_capa']
        localizacao_fisica = request.form['localizacao_fisica']
        categoria = request.form['categoria']

        error = None

        if not titulo:
            error = 'Title is required.'

        if not autor:
            error = 'Autor is required.'

        # Add similar checks for other fields as needed

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO livro (titulo, autor, descricao, data_aquisicao, estado_conservacao, url_foto_capa, localizacao_fisica, categoria)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (titulo, autor, descricao, data_aquisicao, estado_conservacao, url_foto_capa, localizacao_fisica, categoria)
            )
            db.commit()
            return redirect(url_for('livro.index'))

    return render_template('Livros/create.html', categorias=categorias, locais=locais)

@bp.route('/update/<int:ISBN>', methods=('GET', 'POST'))
@login_required
@admin_required
def update(ISBN):
    livro = get_db().execute(
        'SELECT * FROM livro WHERE ISBN = ?',
        (ISBN,)
    ).fetchone()

    categorias = get_db().execute(
        'SELECT * FROM categoria',
    ).fetchall()

    locais = get_db().execute(
        'SELECT * FROM local_fisico',
    ).fetchall()

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        descricao = request.form['descricao']
        data_aquisicao = request.form['data_aquisicao']
        estado_conservacao = request.form['estado_conservacao']
        url_foto_capa = request.form['url_foto_capa']
        localizacao_fisica = request.form['localizacao_fisica']
        categoria = request.form['categoria']

        error = None

        if not titulo:
            error = 'Title is required.'

        if not autor:
            error = 'Autor is required.'

        # Add similar checks for other fields as needed

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE livro SET titulo = ?, autor = ?, descricao = ?, data_aquisicao = ?, estado_conservacao = ?, url_foto_capa = ?, localizacao_fisica = ?, categoria = ?'
                ' WHERE ISBN = ?',
                (titulo, autor, descricao, data_aquisicao, estado_conservacao, url_foto_capa, localizacao_fisica, categoria, ISBN)
            )
            db.commit()
            return redirect(url_for('livro.index'))

    return render_template('Livros/update.html', livro=livro, categorias=categorias, locais=locais)

@bp.route('/delete/<int:ISBN>', methods=('POST',))
@login_required
@admin_required
def delete(ISBN):
    db = get_db()

    items_deleted = db.execute('SELECT * FROM item_emprestimo WHERE id_livro = ?', (ISBN,)).fetchall()

    for item in items_deleted:
        db.execute('DELETE FROM emprestimo WHERE id_item = ?', (item['id'],))
    
    db.execute('DELETE FROM livro WHERE ISBN = ?', (ISBN,))
    db.commit()
    return redirect(url_for('livro.index'))
