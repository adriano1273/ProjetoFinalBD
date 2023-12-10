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
            error = 'Data de emprestimo is required.'

        if not data_devolucao:
            error = 'Data de devolucao is required.'

        if not status:
            error = 'Status is required.'

        if error is not None:
            flash(error)

        else:

            ultimo_item_emprestado = db.execute(
                'SELECT * FROM item_emprestimo WHERE id_livro = ? ORDER BY id DESC LIMIT 1',
                (int(id_livro),)
            ).fetchone()

            if ultimo_item_emprestado != None:

                ultimo_emprestimo = db.execute(
                    'SELECT * FROM emprestimo WHERE id_item = ?',
                    (int(ultimo_item_emprestado['id']),)
                ).fetchone()
                
                if (ultimo_emprestimo['status'] == 'Emprestado' or ultimo_emprestimo['status'] == 'Atrasado'):
                    flash('O item selecionado nao esta disponivel')
                    return redirect(url_for('emprestimo.index'))

            # caso o item esteja diposnivel

            cursor.execute(
                'INSERT INTO item_emprestimo (id_livro)'
                ' VALUES (?)',
                (int(id_livro),)
            )

            last_inserted_id = cursor.lastrowid
            id_item = last_inserted_id

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
    cursor = db.cursor()
    didaticos = db.execute('SELECT * FROM materiais_didaticos').fetchall()

    if request.method == 'POST':
        id_material = request.form['id_material']
        data_emprestimo = request.form['data_emprestimo']
        data_devolucao = request.form['data_devolucao']
        status = request.form['status']
        error = None

        if not id_material:
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

            print(id_material)
        
            ultimo_item_emprestado = db.execute(
                'SELECT * FROM item_emprestimo WHERE id_material = ? ORDER BY id DESC LIMIT 1',
                (int(id_material),)
            ).fetchone()

            if ultimo_item_emprestado != None:

                ultimo_emprestimo = db.execute(
                    'SELECT * FROM emprestimo WHERE id_item = ?',
                    (int(ultimo_item_emprestado['id']),)
                ).fetchone()
                
                if (ultimo_emprestimo['status'] == 'Emprestado' or ultimo_emprestimo['status'] == 'Atrasado'):
                    flash('O item selecionado nao esta disponivel')
                    return redirect(url_for('emprestimo.index'))

            # caso o item esteja diposnivel

            cursor.execute(
                'INSERT INTO item_emprestimo (id_material)'
                ' VALUES (?)',
                (int(id_material),)
            )

            last_inserted_id = cursor.lastrowid
            id_item = last_inserted_id

            db.execute(
                'INSERT INTO emprestimo (id_item, id_usuario, data_emprestimo, data_devolucao, status)'
                ' VALUES (?, ?, ?, ?, ?)',
                (id_item, id_usuario, data_emprestimo, data_devolucao, status)
            )
            db.commit()
            return redirect(url_for('emprestimo.index')) 

    
    return render_template('Emprestimos/createDidaticoBorrow.html', id_usuario=id_usuario, didaticos=didaticos)


@bp.route('/update/<int:id_usuario>/<int:id_item>', methods=('GET', 'POST'))
@login_required
@admin_required
def update(id_usuario, id_item):

    emprestimo = get_db().execute(
        'SELECT * FROM emprestimo WHERE id_usuario = ? AND id_item = ?',
        (id_usuario, id_item)
    ).fetchone() 

    if request.method == 'POST':
        status = request.form['status']
        data_emprestimo = request.form['data_emprestimo']
        data_devolucao = request.form['data_devolucao']

        error = None

        if not status:
            error = 'Status is required.'

        if not data_emprestimo:
            error = 'Data de emprestimo is required.'

        if not data_devolucao:
            error = 'Data de devolucao is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE emprestimo SET status = ?, data_emprestimo = ?, data_devolucao = ?'
                ' WHERE id_usuario = ? AND id_item = ?',
                (status, data_emprestimo, data_devolucao, id_usuario, id_item)
            )
            db.commit()
            return redirect(url_for('emprestimo.index'))

    return render_template('Emprestimos/update.html', emprestimo=emprestimo)

@bp.route('/delete/<int:id_usuario>/<int:id_item>', methods=('POST',))
@login_required 
@admin_required
def delete(id_usuario, id_item):
    db = get_db()
    db.execute('DELETE FROM emprestimo WHERE id_usuario = ? AND id_item = ?', (id_usuario, id_item))
    db.commit()
    return redirect(url_for('emprestimo.index'))