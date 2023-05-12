from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base
import click
from flask import current_app, g 

engine = create_engine('sqlite:////home/filip/PyFlora/instance/database.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

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