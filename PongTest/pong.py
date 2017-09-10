import sys
sys.path.append("..")
import age
import events

import socket
from multiprocessing import Process, Queue

INITIAL_POSITION = ( 50, 50)
INITIAL_VELOCITY = (  1,  3)

# thanks to https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data 
# Read message length and unpack it into an integer
def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
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
        data += packet
    return data

def listenTo(queue, connection, addr):
    while True:
        data = recv_msg(connection)

def writeTo(queue, connectionList):
    while True:
        data = queue.get()   

def startServer(queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = 'localhost'
    port = 6789

    s.bind((host, port))
    s.listen(10)
    
    

class PongGameLogic:
    def __init__(self, pos, vel):
        self.ballpos = pos
        self.ballvel = vel
    
    def update(self, dt):

        
        
        self.ballpos[0] += self.ballvel[0]*dt
        self.ballpos[1] += self.ballvel[1]*dt
    
    def registerClick(self):
        self.ballvel[0] *= -1


class OnClickEvent(AbstractEvent):
    def __str__(self):
        return "On Click Event"

pongGameLogic = PongGameLogic(INITIAL_POSITION, INITIAL_VELOCITY)
onClickEvent = OnClickEvent()
onClickEvent.listen(pongGameLogic.registerClick)

pongGameGraphics = '''Nathan's Graphics Thingy goes here, make sure it can call the 'onClickEvent' '''
   
loop.run(pongGameLogic, pongGameGraphics)
