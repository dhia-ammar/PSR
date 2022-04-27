import socket
HEADER = 64
PORT = 1313
#SERVER = "192.168.56.1"
# get the ip adress of the server machine dynamically
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
