import time
import socket
import struct
from multiprocessing import Process, Queue
import traceback

# thanks to https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data 
def send_msg(sock, msg):
    try:
        msg = struct.pack('>I', len(msg)) + msg.encode('ascii')
        sock.sendall(msg)
    except Exception as e:
        traceback.print_exc()

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
        data += packet.decode('ascii')
    return data

def connectionAcceptor(queue, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(100)

    running = True
    while running:
        clientSocket,addr = s.accept()
        print("New client connecting...")
        queue.put(clientSocket)
        queue.put(addr)

def clientListener(queue, socket, addr):
    running = True
    while running:
        data = recv_msg(socket)
        queue.put(data)

# can be started as a process target
def startNetworkManager(inputQueue, outputQueue):
    manager = NetworkManager(inputQueue, outputQueue)
    
class NetworkManager:
    def __init__(self, engineInputQueue, engineOutputQueue):
        self.clientInputQueues = []
        self.clientInputProcesses = []
        self.clientSockets = []
        self.acceptorQueue = None
        self.acceptorProces = None
        self.acceptorWaitingMode = 'socket'
        self.acceptorWaitingSocket = None
        self.engineInputQueue = engineInputQueue
        self.engineOutputQueue = engineOutputQueue
        self.startConnectionAcceptor('localhost', 6789)
        self.route()

    def __del__(self):
        try:
            for s in self.clientSockets: s.close()
        except: pass

    def route(self):
        running = True
        while running:

            # check acceptor queue
            data = None
            try: data = self.acceptorQueue.get_nowait()
            except: pass
            if data:
                if self.acceptorWaitingMode == 'socket':
                    self.acceptorWaitingSocket = data
                    self.acceptorWaitingMode = 'addr'
                else:
                    self.startClientListener(self.acceptorWaitingSocket, data)
                    self.clientSockets.append(self.acceptorWaitingSocket)
                    self.acceptorWaitingSocket = None
                    self.acceptorWaitingMode = 'socket'

            # check each client queue
            for inputQueue in self.clientInputQueues:
                data = None
                try: data = inputQueue.get_nowait()
                except: pass
                if data: self.engineInputQueue.put(data)

            # check engine output
            data = None
            try: data = self.engineOutputQueue.get_nowait()
            except: pass
                       
            # if engine output, broadcast to every socket # TODO: eventually change this obviously
            if data:
                for s in self.clientSockets:
                    send_msg(s, data)
        
        time.sleep(.5) # TODO: dynamic sleeping
    
    def startConnectionAcceptor(self, host, port):
        self.acceptorQueue = Queue()
        self.acceptorProcess = Process(target=connectionAcceptor, args=(self.acceptorQueue, host, port))
        self.acceptorProcess.start()
        
    def startClientListener(self, socket, addr):
        print("Listening to client from ", addr)
        q = Queue()
        self.clientInputQueues.append(q)
        p = Process(target=clientListener, args=(q, socket, addr))
        self.clientInputProcesses.append(p)
        p.start()
