"""
validacion.py:
    Modulo de validacion de campos, utiliza re para asegurar que los caracteres ingresados esten dentro de un patron.
"""
import re

class Validacion():
    def __init__(self) -> None:
        self.patron ="^[A-Za-z]+(?i:[ _-][A-Za-z]+)*$"
    
    def validar(self,nombre,apellido):
        if (re.match(self.patron,nombre)) and (re.match(self.patron,apellido)):
            return True
        else:
            return False
