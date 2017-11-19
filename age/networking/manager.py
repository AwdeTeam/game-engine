import time
import socket
from multiprocessing import Process, Queue
import traceback

from age.networking.message import Message
import age.networking.util as util


def clientSideConnectionEntryPoint(inputQueue, outputQueue, ip, port):
    connection = ClientSideConnection(inputQueue, outputQueue, ip, port)
    # TODO: return connection? IDK if that's necessary, it's not the process
    # reference, but might be nice for gracefully shutting down?

class ClientSideConnection:
    def __init__(self, inputQueue, outputQueue, ip, port):
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((ip, port))
        self.socket.setblocking(False)
        
        self.route()

    def route(self):
        running = True
        while running:
            print("Client Listening")
            try:
                data = util.recv_msg(self.socket)
                msg = Message.inflate(data)
                self.inputQueue.put(msg)
                print("GOT DATA")
            except:
                #traceback.print_exc()
                pass

            try:
                data = self.outputQueue.get_nowait()
                util.send_msg(self.socket, data.deflate())
                print("SENDING")
            except: 
                #traceback.print_exc()
                pass
        
            # TODO: dynamic timing here? 
            time.sleep(.1)


# can be started as a process target
def networkManagerEntryPoint(inputQueue, outputQueue, ip, port):
    manager = NetworkManager(inputQueue, outputQueue, ip, port)
    
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
        msg = Message.inflate(data)
        queue.put(msg)

class NetworkManager:
    def __init__(self, engineInputQueue, engineOutputQueue, ip, port):
        self.clientInputQueues = []
        self.clientInputProcesses = []
        
        self.clientSockets = {}
        self.nextClientID = 0
        
        self.acceptorQueue = None
        self.acceptorProcess = None
        self.acceptorWaitingMode = 'socket'
        self.acceptorWaitingSocket = None
        self.engineInputQueue = engineInputQueue
        self.engineOutputQueue = engineOutputQueue
        self.startConnectionAcceptor(ip, port)
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
                print("CHECKING INPUT")
                data = None
                try: data = inputQueue.get_nowait()
                except: pass
                if data: 
                    print("YES, I GOT DATA")
                    self.engineInputQueue.put(data)


            # TODO TODO: put handling of engine output inside try except INSIDE OF A LOOP
            # (keeps processing messages until queue is empty) and limit by
            # dynamic sleeping

            # check engine output
            data = None
            try: data = self.engineOutputQueue.get_nowait()
            except: pass
            
            if data:
                #message
                print("SENDING DATA")
                #msg = Message.inflate(data)
                
                if data.clientID == -1: # signifying broadcast
                    rawdata = data.deflate()
                    for clientID in self.clientSockets.keys():
                        print("Sending stuff to client ", str(clientID))
                        sock = self.clientSockets[clientID]
                        util.send_msg(sock, rawdata)
                else:
                    sock = self.clientSockets[data.clientID]
                    util.send_msg(sock, rawdata)

                print("Message should have been sent")

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
