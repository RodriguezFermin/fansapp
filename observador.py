from datetime import datetime

class Observado:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self, accion):
        for observador in self.observadores:
            observador.update(accion)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ObservadorConcreto(Observador):
    def __init__(self, obj):
        self.observado = obj
        self.observado.agregar(self)

    def update(self, accion):
        log = open("hinchas_observador_logs.txt", "a")
        log.write(str(datetime.today()) + " Se realizo una " + accion + " en la Base de Datos.\n")
        log.close