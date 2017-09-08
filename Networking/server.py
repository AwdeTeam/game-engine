import socket
import datetime

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"
port = 6789

serverSocket.bind((host, port))
serverSocket.listen(5)

try:
    running = True
    while running:
        clientSocket,addr = serverSocket.accept()

        print("Obtained connection from " + str(addr))
        current = datetime.datetime.now()

        clientSocket.send(str(current).encode('ascii'))
        clientSocket.close()
except:
    serverSocket.close()
