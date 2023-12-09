import sqlite3

import click
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('seed.sql') as f:
        db.executescript(f.read().decode('utf8'))

    nome = 'admin'
    funcao = 'admin'
    login = 'admin'
    senha = 'admin'

    db.execute(
    "INSERT INTO Usuario (nome, funcao, login, senha) VALUES (?, ?, ?, ?)",
    (nome, funcao, login, generate_password_hash(senha)),
    )
    db.commit()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



