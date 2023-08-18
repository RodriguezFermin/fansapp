
import socketserver
from peewee import *
from conexion import Hincha



# global HOST
global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        consulta=data.decode("UTF-8")
        mensaje = str((Hincha.select().where(Hincha.club==consulta).count()))
        socket.sendto(mensaje.encode("UTF-8"), self.client_address)

'''
class startServer():
    HOST = "localhost"
    PORT = 9999
    with socketserver.UDPServer((HOST,PORT), MyUDPHandler) as server:
        server.serve_forever()
'''



if __name__ == "__main__":
    db = SqliteDatabase('hinchas.db')
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
