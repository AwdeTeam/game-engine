#import networking.manager as net
import traceback

from multiprocessing import Process, Queue

from age.networking import manager
from age.networking.message import Message
import age.loop

class Engine:
    def __init__(self):
        self.netInQueue = None
        self.netOutQueue = None

    def startServerNetworking(self, ip, port):
        print("Starting network I/O...")
        self.netInQueue = Queue()
        self.netOutQueue = Queue()

        # TODO: process needs to be saved so can be closed?
        p = Process(target=manager.networkManagerEntryPoint, args=(self.netInQueue, self.netOutQueue, ip, port))
        p.start()
        print("Network I/O running")

    def startServerGameLoop(self, gameLogicManager):
        print("Starting server game loop...")
        age.loop.run(gameLogicManager)
        

    # TODO: check if gameLogicManager is really necessary?
    def startServer(self, ip, port, gameLogicManager):
        print("Starting server...")
        self.startServerNetworking(ip, port)
        self.startServerGameLoop(gameLogicManager) # TODO: comment out if this ends up blocking (pretty sure it does)

    # TODO: allow to specify allotted time (elsewhere, in an engine
    # variable/constraint to process network messages (for
    # looping through network I/O)

    # get any collected network input messages and return them in a list
    def getMessages(self):
        msgList = []

        # TODO: loop? Maybe have another version of this function that "blocks"
        # (loops until gets message)
        try:
            data = self.netInQueue.get_nowait()
            msg = Message.inflate(data)
            msgList.append(msg)
        except Exception as e: 
            #traceback.print_exc()
            pass

        return msgList

    def sendMessage(self, msg): self.netOutQueue.put(msg) 
    
    
    # TODO: ip/port other stuffs
    def connectToServer(self, ip, port):
        print("Connecting to server...")
        self.netInQueue = Queue()
        self.netOutQueue = Queue()

        p = Process(target=manager.clientSideConnectionEntryPoint, args=(self.netInQueue, self.netOutQueue, ip, port))
        p.start()
        
