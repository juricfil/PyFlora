from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    '''Registering functions with the application.'''
    db.init_app(app)

def get_db():
    '''Returns a SQLAlchemy database session.'''
    return db.session

def close_db(e=None):
    '''Closes the database connection.'''
    db.session.close()

def init_db():
    '''Initializes the database based on schema.'''
    db.create_all()