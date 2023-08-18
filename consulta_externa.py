import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# print(data)
# ################################################333
#mensaje = "BOCA JUNIORS"

# ===== ENVIO Y RECEPCIÓN DE DATOS =================
# ===== ENVIO DE DATOS =================
sock.sendto(data.encode("UTF-8"), (HOST, PORT))
received = sock.recv(1024)


# ===== RECEPCIÓN DE DATOS =================
print("Cantidad de Hinchas: " + received.decode("UTF-8"))

# ===== FIN ENVIO Y RECEPCIÓN DE DATOS =================
