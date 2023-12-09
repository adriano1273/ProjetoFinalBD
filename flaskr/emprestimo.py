from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint('emprestimo', __name__, url_prefix='/emprestimos')

@bp.route('/')
@login_required
@admin_required
def index():
    db = get_db()
    emprestimos = db.execute('SELECT * FROM emprestimo').fetchall()

    item_nomes = {}
    usuarios_nomes = {}
    for emprestimo in emprestimos:
        id_item = emprestimo['id_item'] 
        id_usuario = emprestimo['id_usuario'] 
        usuario = db.execute('SELECT * FROM usuario WHERE ID = ?', (id_usuario,)).fetchone()
        item_emprestimo = db.execute('SELECT * FROM item_emprestimo WHERE id = ?', (id_item,)).fetchone()
        item = db.execute('SELECT * FROM item_emprestimo WHERE id = ?', (id_item,)).fetchone()

        if item['id_material'] is None:
            id_livro = item['id_livro']
            result = db.execute('SELECT * FROM livro WHERE ISBN = ?', (id_livro,)).fetchone()
            nome = result['titulo']
        
        else:
            id_diatico = item['id_material']
            result = db.execute('SELECT * FROM materiais_didaticos WHERE ID = ?', (id_diatico,)).fetchone()
            nome = result ['descricao']

        item_nomes[id_item] = nome if result else 'Unknown'
        usuarios_nomes[id_item] = usuario['nome'] if usuario else 'Unknown'


    return render_template('Emprestimos/index.html', emprestimos=emprestimos, item_nomes=item_nomes, usuarios_nomes=usuarios_nomes)

@bp.route('/select', methods=('GET', 'POST'))
@login_required
@admin_required
def select():
    db = get_db()
    usuarios = db.execute('SELECT * FROM usuario').fetchall()

    if request.method == 'POST':
        id_usuario = request.form['usuario']
        item = request.form['item']
        error = None

        if not id_usuario:
            error = 'User is required.'

        if not item:
            error = 'Item is required.'

        if error is not None:
            flash(error)
        else:
            if item == '1':
                return redirect(url_for('emprestimo.createBookBorrow', id_usuario=id_usuario))
            return redirect(url_for('emprestimo.createDidaticoBorrow', id_usuario=id_usuario))

    return render_template('Emprestimos/select.html', usuarios=usuarios)

@bp.route('/createBookBorrow/<int:id_usuario>', methods=('GET', 'POST'))
@login_required
@admin_required
def createBookBorrow(id_usuario):
    db = get_db()
    cursor = db.cursor()
    livros = db.execute('SELECT * FROM livro').fetchall()

    if request.method == 'POST':
        id_livro = request.form['id_livro']
        data_emprestimo = request.form['data_emprestimo']
        data_devolucao = request.form['data_devolucao']
        status = request.form['status']
        error = None

        if not id_livro:
            error = 'Livro is required.'

        if not data_emprestimo:
            error = 'Data de emprestimno is required.'

        if not data_devolucao:
            error = 'Data de devolucao is required.'

        if not status:
            error = 'Status is required.'

        if error is not None:
            flash(error)
        else:

            # verificar se ja exitem items_emprestimos com o id do livro em questao

            itens_emprestados = db.execute('SELECT * FROM item_emprestimo WHERE livro_id = ?',
            (id_livro,)).fetchall()

            for item_emprestado in itens_emprestados


            db.execute(
                'INSERT INTO item_emprestimo (id_livro, id_material)'
                ' VALUES (?, ?)',
                (id_livro, None)
            )

            last_inserted_id = cursor.lastrowid
            item_id = last_inserted_id

            db.execute(
                'INSERT INTO emprestimo (id_item, id_usuario, data_emprestimo, data_devolucao, status)'
                ' VALUES (?, ?, ?, ?, ?)',
                (id_item, id_usuario, data_emprestimo, data_devolucao, status)
            )
            db.commit()
            return redirect(url_for('emprestimo.index'))

    return render_template('Emprestimos/createBookBorrow.html', id_usuario=id_usuario, livros=livros)

@bp.route('/createDidaticoBorrow/<int:id_usuario>', methods=('GET', 'POST'))
@login_required
@admin_required
def createDidaticoBorrow(id_usuario):
    db = get_db()
    didaticos = db.execute('SELECT * FROM materiais_didaticos').fetchall()

    if request.method == 'POST':
        id_didatico = request.form['id_livro']
        data_emprestimo = request.form['data_emprestimo']
        data_devolucao = request.form['data_devolucao']
        status = request.form['status']
        error = None

        if not id_livro:
            error = 'Material is required.'

        if not data_emprestimo:
            error = 'Data de emprestimo is required.'

        if not data_devolucao:
            error = 'Data de devolucao is required.'

        if not status:
            error = 'Status is required.'

        if error is not None:
            flash(error)
        else:
            id_item = id_didatico 
            db.execute(
                'INSERT INTO emprestimo (id_item, id_usuario, data_emprestimo, data_devolucao, status)'
                ' VALUES (?, ?, ?, ?, ?)',
                (id_item, id_usuario, data_emprestimo, data_devolucao, status)
            )
            db.commit()
            return redirect(url_for('emprestimo.index'))

    return render_template('Emprestimos/createDidaticoBorrow.html', id_usuario=id_usuario, didaticos=didaticos)