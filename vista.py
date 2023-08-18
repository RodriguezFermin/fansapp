"""
vista.py:
    Es el archivo de vistas, donde se da inicio a la ventana principal, que se conecta con el modelo, y a la ventana de actualizacion (VentanaNueva)
"""
from tkinter import StringVar
from tkinter import Button
from tkinter import Label 
from tkinter import Entry 
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from modelo import HinchasModel
import subprocess
import sys
import threading

theproc=""

class Ventana():
    def __init__(self, windows):
        self.hincha=HinchasModel()
        self.master=windows
        #self.master.iconbitmap("favicon.ico")
        self.master.geometry('700x350')
        self.master.title("APLICACION HINCHAS")
        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_club = StringVar()
        ''' SE LEVANTA EL SERVIDOR PARA ATENDER PETICIONES EXTERNAS'''
        threading.Thread(target=self.start_server, args=(True,), daemon=True).start()
        self.nombre = Label(self.master, text="Nombre")
        self.nombre.grid(row=0, column=0, sticky="w")

        self.apellido = Label(self.master, text="Apellido")
        self.apellido.grid(row=1, column=0, sticky="w")

        self.club = Label(self.master, text="Club del que es hincha")
        self.club.grid(row=2, column=0, sticky="w")

        self.entry_nombre = Entry(self.master, textvariable=self.var_nombre, width=50)
        self.entry_nombre.grid(row=0, column=1)

        self.entry_apellido = Entry(self.master, textvariable=self.var_apellido, width=50)
        self.entry_apellido.grid(row=1, column=1)

        self.combo = ttk.Combobox(
            state="readonly",
            values=["BOCA JUNIORS", "RIVER PLATE", "RACING", "INDEPENDIENTE", "SAN LORENZO"],
            textvariable=self.var_club
        )
        self.combo.grid(row=2, column=1)

        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("col1", "col2","col3")
        self.tree.column("#0", width=100, minwidth=50, anchor="w")
        self.tree.column("col1", width=200, minwidth=80, anchor="w")
        self.tree.column("col2", width=200, minwidth=80, anchor="w")
        self.tree.column("col3", width=200, minwidth=80, anchor="w")

        self.tree.grid(column=0, row=7, columnspan=4)

        self.tree.heading("col1", text="NOMBRE")
        self.tree.heading("col2", text="APELLIDO")
        self.tree.heading("col3", text="CLUB")

        self.boton_g = Button(self.master, text="Cargar", command=lambda:self.hincha.cargar(self.var_nombre,self.var_apellido,self.var_club,self.tree))
        self.boton_g.grid(row=5, column=0)

        self.boton_f = Button(self.master, text="Actualizar", command=lambda:self.actualizar(self.tree,self.master))
        self.boton_f.grid(row=5, column=1)

        self.boton_f = Button(self.master, text="Borrar", command=lambda:self.hincha.borrar(self.tree))
        self.boton_f.grid(row=5, column=2)

        self.boton_f = Button(self.master, text="Graficar", command=self.hincha.graficar)
        self.boton_f.grid(row=8, column=0)

        self.boton_f = Button(self.master, text="Salir", command=lambda:self.salir(self.master))
        self.boton_f.grid(row=8, column=2)

        self.hincha.leer(self.tree)
    
    def ventanaNueva(self,id,master,tree,nombre,club,apellido):
        """
        Despliega la ventana de actualizar
        :param id: El ID del hincha.
        :param tree: El arbol de la vista principal.
        :param master: La vista principal.
        :param nombre: El nombre del hincha.
        :param club: El club del hincha.
        :param apellido: El apellido del hincha.
        """
        var_nombre1 = StringVar(value=nombre) 
        var_apellido1 = StringVar(value=apellido)
        var_club1 = StringVar(value=club)
        id_e = str(id)
        ventanaNueva = Toplevel(master)
        ventanaNueva.title("Actualizar")
        ventanaNueva.geometry("450x120")
        ventanaNueva.iconbitmap("favicon.ico")

        Label(ventanaNueva, text="INGRESE LOS NUEVOS VALORES PARA EL ID: "+id_e).grid(row=0, column=1, sticky="w")  
        nombre1 = Label(ventanaNueva, text="Nombre")
        nombre1.grid(row=1, column=0, sticky="w")

        apellido1 = Label(ventanaNueva, text="Apellido")
        apellido1.grid(row=2, column=0, sticky="w")

        club1 = Label(ventanaNueva, text="Club del que es hincha")
        club1.grid(row=3, column=0, sticky="w")

        entry_nombre1 = Entry(ventanaNueva, textvariable=var_nombre1, width=50)
        entry_nombre1.grid(row=1, column=1, columnspan=2, sticky="w")

        entry_apellido1 = Entry(ventanaNueva, textvariable=var_apellido1, width=50)
        entry_apellido1.grid(row=2, column=1, columnspan=2, sticky="w")

        combo1 = ttk.Combobox(
            ventanaNueva,
            state="readonly",
            values=["BOCA JUNIORS", "RIVER PLATE", "RACING", "INDEPENDIENTE", "SAN LORENZO"],
            textvariable=var_club1
        )
        combo1.grid(row=3, column=1, columnspan=2, sticky="w")
        boton_g = Button(ventanaNueva, text="Guardar", command=lambda:self.hincha.actualizarHincha(tree,var_nombre1,var_apellido1,var_club1,ventanaNueva,id_e))
        boton_g.grid(row=4, column=0)
        boton_s = Button(ventanaNueva, text="Salir", command=ventanaNueva.destroy)
        boton_s.grid(row=4, column=1)

    def actualizar(self,tree,master):
        """
        Recibe informacion de la ventana principal y la envia a la ventana nueva.
        :param tree: El arbol de la ventana principal.
        :param master: La ventana principal.
        """
        if tree.focus()!='':
            item = tree.focus()
            id = tree.item(item)['text']
            nombre = tree.item(item)['values'][0]
            apellido = tree.item(item)['values'][1]
            club = tree.item(item)['values'][2]
            self.ventanaNueva(id,master,tree,nombre,club,apellido)
        else:
            messagebox.showerror(message="Debe seleccionar un hincha para actualizar", title="ERROR")

    def start_server(self, var):
        global theproc
        if(var):
            theproc = subprocess.Popen([sys.executable,'server_udp.py'])
            theproc.communicate()
    

    
    def salir(self, master):
        global theproc
        if theproc != "":
            theproc.kill()
        master.destroy()

