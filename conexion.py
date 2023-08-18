"""
conexion.py:
    Modulo de conexion con la base de datos. Utiliza peewee como ORM 
"""
from peewee import *

db = SqliteDatabase('hinchas.db')

class BaseModel(Model):
    class Meta:
        database = db

class Hincha(BaseModel):
    nombre = CharField(unique=False)
    apellido = CharField()
    club = CharField()
    
class Conectar():
    def __init__(self) -> None:
        db.connect()
        db.create_tables([Hincha])

