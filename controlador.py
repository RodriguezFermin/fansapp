"""
controlador.py:
    Es el controlador de la aplicación, desde aquí se da inicio a la misma.
"""
__author__= "Fermín Rodriguez"
__maintainer__= "Fermín Rodriguez"
__email__= "ferminrodriguez.90@gmail.com"
__copyright__= "Copyright 2023"
__version__= "0.0.2"

from tkinter import Tk
from vista import Ventana
import observador





if __name__ == "__main__":
    
    master_tk = Tk()
    ventana = Ventana(master_tk)
    ''' ACA INSTANCIO EL OBSERVADOR PARA QUE OBSERVE A LA CLASE HINCHA EN VENTANA'''
    observador1 = observador.ObservadorConcreto(ventana.hincha)

    
    master_tk.mainloop()


