"""
modelo.py:
    Es el archivo que guarda la logica de la aplicación, se conecta con la base de datos a traves del modulo conexion, tambien utiliza el modulo de validacion para controlar los campos
"""
import matplotlib.pyplot as plt
from validacion import Validacion
from conexion import Hincha,Conectar
from tkinter import messagebox
from datetime import datetime
from observador import Observado
'''ACA GENERAMOS UN DECORADOR PARA INFORMAR LAS ACCIONES'''
def logeadorDeAcciones(func):
    '''REALIZAMOS UN PRINT CON EL ACCESO A BASE DE DATOS'''
    def informar(*args):
        print( str(datetime.today()) + " el decorador avisa que se esta accediendo a la Base de Datos")
        func(*args)
    
    return informar

class HinchasModel(Observado):

    def __init__(self) -> None:
        self.validar = Validacion()
        Conectar()

    #DEFINICIÓN DE FUNCIONES
    @logeadorDeAcciones
    def cargar(self,nombre1,apellido1,club1,tree):
        """
        Realiza el alta de un hincha
        :param nombre1: El nombre del hincha.
        :param apellido1: El apellido del hincha.
        :param club1: El club del hincha.
        :param tree: El arbol de la ventana principal.
        """
        nombre = nombre1.get()
        apellido = apellido1.get()
        club = club1.get()
        if nombre!="" and apellido!="" and club!="":
            if (self.validar.validar(nombre,apellido)):
                hincha=Hincha()
                hincha.nombre=nombre
                hincha.apellido=apellido
                hincha.club=club
                hincha.save()
                self.notificar("Alta")
                self.leer(tree)
            else:
                messagebox.showerror(message="Cadena de caracteres no válida", title="ERROR")            
        else:
            messagebox.showerror(message="Debe ingresar todos los datos", title="ERROR")

    def leer(self,tree):
        """
        Se encarga de leer en la base de datos y actualizar el arbol de la ventana principal con los registros que esten cargados en ella.
        :param tree: El arbol de la ventana principal.
        """
        tree.delete(*tree.get_children())
        for row in Hincha.select():
            tree.insert("", "end", text=row.id, values=(row.nombre, row.apellido, row.club))
    
    @logeadorDeAcciones     
    def borrar(self,tree):
        """
        Realiza la baja de un hincha.
        :param tree: El arbol de la ventana principal.
        """
        if tree.focus()!="":
            item = tree.focus()
            id = tree.item(item)['text']
            mi_id = int(id)
            borrar=Hincha.get(Hincha.id==mi_id)
            borrar.delete_instance()
            self.leer(tree)
        else:
            messagebox.showerror(message="Debe seleccionar un hincha para eliminar", title="ERROR")
        self.notificar("Baja")

    @logeadorDeAcciones
    def actualizarHincha(self,tree,var_nombre1,var_apellido1,var_club1,ventanaNueva,id_e):
            """
            Realiza la actualizacion de un hincha.
            :param tree: El arbol de la ventana principal.
            :param var_nombre1: El nombre del hincha.
            :param var_apellido1: El apellido del hincha.
            :param var_club1: El club del hincha.
            :param ventanaNueva: La ventana actualizar.
            :param id_e: El ID del hincha.
            """
            nombre = var_nombre1.get()
            apellido = var_apellido1.get()
            club = var_club1.get()
            if nombre!="" and apellido!="" and club!="":
                if (self.validar.validar(nombre,apellido)):
                    actualizar=Hincha.update(nombre=nombre,apellido=apellido,club=club).where(Hincha.id==id_e)
                    actualizar.execute()
                    messagebox.showinfo(message="El hincha ha sido editado correctamente", title="CARGADO")
                    ventanaNueva.destroy()
                    self.leer(tree)
                else:
                    messagebox.showerror(message="Cadena de caracteres no válida", title="ERROR")
                    ventanaNueva.destroy()
            else:
                messagebox.showerror(message="Debe ingresar todos los datos", title="ERROR")
            self.notificar("Modificación")

    def graficar(self,):
        """
        Grafica la cantidad de hinchas por club haciendo uso de la biblioteca matplotlib
        """
        boca,river,independiente,racing,sanlorenzo = 0,0,0,0,0
        hinchas = Hincha.select()
        for hincha in hinchas:
            if hincha.club == "BOCA JUNIORS":
                    boca += 1
            if hincha.club == "RIVER PLATE":
                    river += 1
            if hincha.club == "INDEPENDIENTE":
                    independiente += 1
            if hincha.club == "RACING":
                    racing += 1
            if hincha.club == "SAN LORENZO":
                    sanlorenzo += 1
            '''
            match hincha.club:
                case "BOCA JUNIORS":
                    boca += 1
                case "RIVER PLATE":
                    river += 1
                case "INDEPENDIENTE":
                    independiente += 1
                case "RACING":
                    racing += 1
                case "SAN LORENZO":
                    sanlorenzo += 1
            '''
        y = [boca,river,independiente,racing,sanlorenzo]
        x = ["BOCA JUNIORS", "RIVER PLATE", "INDEPENDIENTE", "RACING", "SAN LORENZO"]
        plt.rcParams['figure.figsize'] = [10, 6]
        plt.title("Hinchas por club")
        plt.bar(x,y)
        plt.show()
