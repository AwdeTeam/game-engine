import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"
port = 6789

s.connect((host,port))

tm = s.recv(1024)
s.close()
print("Received " + tm.decode('ascii'))
