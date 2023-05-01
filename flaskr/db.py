import sqlite3
import click
from flask import current_app, g 

def get_db():
    '''Uses g to reuse stored connection.'''
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'],
                               detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row # returns row as dicts   
    return g.db

def close_db(e=None):
    '''Checks if connection is created by checking g.db. IF it exists close the connection'''
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    ''' Initializes db based on schema'''
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    '''Clear the existing data and create new tables.'''
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    '''Registering functions with the application.'''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)