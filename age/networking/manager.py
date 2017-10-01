import time
import socket
from multiprocessing import Process, Queue
import traceback

from message import Message
import util


def clientSideConnectionEntryPoint(inputQueue, outputQueue):
    pass

class ClientSideConnection:
    def __init__(self, inputQueue, outputQueue):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: rest of connection stuff
        
        self.route()

    def route(self):
        running = True
        while running:
            try:
                msg = util.recv_msg(s)
                self.inputQueue.put(msg)
            except:
                pass
        


# can be started as a process target
def networkManagerEntryPoint(inputQueue, outputQueue):
    manager = NetworkManager(inputQueue, outputQueue)
    
# PROCESS
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

# PROCESS
def clientListener(queue, socket, addr):
    running = True
    while running:
        data = util.recv_msg(socket)
        queue.put(data)

class NetworkManager:
    def __init__(self, engineInputQueue, engineOutputQueue):
        self.clientInputQueues = []
        self.clientInputProcesses = []
        
        self.clientSockets = {}
        self.nextClientID = 0
        
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
            for clientID in self.clientSockets:
                sock = self.clientSockets[clientID]
                sock.close()
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
                    #self.clientSockets.append(self.acceptorWaitingSocket)
                    self.clientSockets[self.nextClientID] = self.acceptorWaitingSocket
                    self.nextClientID += 1
                    self.acceptorWaitingSocket = None
                    self.acceptorWaitingMode = 'socket'

                    # send along client id
                    

            # check each client queue
            for inputQueue in self.clientInputQueues:
                data = None
                try: data = inputQueue.get_nowait()
                except: pass
                if data: self.engineInputQueue.put(data)


            # TODO TODO: put handling of engine output inside try except INSIDE OF A LOOP
            # (keeps processing messages until queue is empty) and limit by
            # dynamic sleeping

            # check engine output
            data = None
            try: data = self.engineOutputQueue.get_nowait()
            except: pass
                       
            # if engine output, send that message to signified client
            if data:
                #message
                msg = Message.inflate(data)
                
                if msg.clientID == -1: # signifying broadcast
                    for clientID in self.clientSockets:
                        sock = self.clientSockets[clientID]
                        util.send_msg(sock, data)
                else:
                    sock = self.clientSockets[msg.clientID]
                    util.send_msg(sock, data)
        
        time.sleep(.1) # TODO: dynamic sleeping
    
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
