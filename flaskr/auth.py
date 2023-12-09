import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['funcao'] != 'admin':
            return render_template('Authentication/accessDenied.html')

        return view(**kwargs)

    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
@admin_required
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        funcao = request.form['funcao']
        login = request.form['login']
        senha = request.form['senha']
        db = get_db()
        error = None

        if not nome:
            error = 'Nome is required.'
        elif not funcao:
            error = 'Função is required.'
        elif not login:
            error = 'Login is required.'
        elif not senha:
            error = 'Senha is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Usuario (nome, funcao, login, senha) VALUES (?, ?, ?, ?)",
                    (nome, funcao, login, generate_password_hash(senha)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {nome} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('Authentication/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        db = get_db()
        error = None
        usuario = db.execute(
            'SELECT * FROM usuario WHERE login = ?', (login,)
        ).fetchone()

        if usuario is None:
            error = 'Incorrect login.'
        elif not check_password_hash(usuario['senha'], senha):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = usuario['ID']
            return redirect(url_for('home.home'))

        flash(error)

    return render_template('Authentication/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuario WHERE ID = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return render_template('base.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


