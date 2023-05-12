from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base
import click
from flask import current_app, g 
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('sqlite:////home/filip/PyFlora/instance/database.db', echo=True)
Base = declarative_base()

class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Plants(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    image = Column(LargeBinary, nullable=False)
    soil_moisture = Column(Integer, nullable=False)
    light = Column(Float, nullable=False)
    substrate = Column(String(50), nullable=True)

class FlowerPot(Base):
    __tablename__ = 'flower_pot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pot_name = Column(String(50), unique=True, nullable=False)
    plant = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)

class Measurements(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    soil_moisture = Column(Integer, nullable=False)
    acidity = Column(Float, nullable=False)
    lux = Column(Integer, nullable=False)

Base.metadata.create_all(engine)


def get_db():
    '''Uses scoped_session to reuse stored connection.'''
    if not hasattr(g, 'db'):
        g.db = (sessionmaker(bind=engine))
    return g.db