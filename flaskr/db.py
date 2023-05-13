from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#Defining classes to be used for database
class User(db.Model):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(20), unique=True, nullable=False)
    password = sa.Column(sa.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Plants(db.Model):
    __tablename__ = 'plants'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name =sa.Column(sa.String(50), unique=True, nullable=False)
    image =sa.Column(sa.LargeBinary, nullable=False)
    soil_moisture =sa.Column(sa.Integer, nullable=False)
    light =sa.Column(sa.Float, nullable=False)
    substrate =sa.Column(sa.String(50), nullable=True)

class FlowerPot(db.Model):
    __tablename__ = 'flower_pot'
    id =sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    pot_name =sa.Column(sa.String(50), unique=True, nullable=False)
    plant =sa.Column(sa.String(50), nullable=True)
    status =sa.Column(sa.String(50), nullable=True)

class Measurements(db.Model):
    __tablename__ = 'measurements'
    id =sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    soil_moisture =sa.Column(sa.Integer, nullable=False)
    acidity =sa.Column(sa.Float, nullable=False)
    lux =sa.Column(sa.Integer, nullable=False)

#Defining functions to be used for database    
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


