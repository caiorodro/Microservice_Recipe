   
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import String, Table, Integer, Numeric, DateTime, BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
import json
from app.base.mapTable import mapUser, mapRecipe
import datetime
from decimal import Decimal
from venv.config import DevelopmentConfig as config

strConn = ''.join((config.DB_USERNAME, ':', config.DB_PASSWORD, '@', config.DB_SERVER_NAME, '/', config.DB_NAME))

engine = create_engine('mysql+pymysql://' + strConn, isolation_level="READ UNCOMMITTED")

metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

tables = []

user = Table('tb_user', metadata,
    Column('ID_USER', Integer, primary_key=True, autoincrement='auto'),
    Column('NAME_USER', String(60), nullable=False),
    Column('PASSWORD1', String(150), nullable=True),
    Column('EMAIL', String(100), nullable=True),
    Column('USER_ENABLED', Numeric, nullable=True),
    Column('KIND_OF_USER', Integer, nullable=True))

recipe = Table('tb_recipe', metadata,
    Column('ID_RECIPE', Integer, primary_key=True, autoincrement='auto'),
    Column('TITLE', String(120), nullable=False),
    Column('INGREDIENTS', String(1000), nullable=True),
    Column('INSTRUCTIONS', String(2000), nullable=True),
    Column('IMAGE_NAME', String(150), nullable=True),
    Column('IMAGE', BLOB, nullable=True),
    Column('MASK', String(20), nullable=True),
    Column('READY_IN_MIN', Integer, nullable=True),
    Column('SERVING', Integer, nullable=True))

tables.append([mapRecipe, recipe])
tables.append([mapUser, user])

def mapAllTables():

    [mapper(table[0], table[1]) for table in tables]

def connect():
    try:
        return engine.connect()
    except Exception:
        raise Exception('Cannot connect on database')

def close():
    try:
        engine.close()
    except Exception:
        pass

conn = connect()
mapAllTables()
