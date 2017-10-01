import struct
import traceback
import socket

# thanks to https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data 
def send_msg(sock, msg):
    try:
        msg = struct.pack('>I', len(msg)) + msg.encode('ascii')
        sock.sendall(msg)
    except Exception as e:
        traceback.print_exc()

# Read message length and unpack it into an integer
def recv_msg(sock):
    raw_msglen = sock.recv(4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

# Helper function to recv n bytes or return None if EOF is hit
def recvall(sock, n):
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet.decode('ascii')
    return data
