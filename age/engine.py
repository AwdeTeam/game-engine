#import networking.manager as net

from multiprocessing import Process, Queue

from networking import manager, message.Message

class Engine:
    def __init__(self):
        self.netInQueue = None
        self.netOutQueue = None

    # TODO: pass in port/other info stuffs
    def startServerNetworking(self, ip, port):
        print("Starting network I/O...")
        self.netInQueue = Queue()
        self.netOutQueue = Queue()

        # TODO: process needs to be saved so can be closed?
        p = Process(target=manager.networkManagerEntryPoint, args=(self.netInQueue, self.netOutQueue, ip, port))
        p.start()
        print("Network I/O running")

    def startServerGameLoop(self):
        print("Starting server game loop...")
        # TODO: start game loop

    def startServer(self, ip, port):
        print("Starting server...")
        self.startServerNetworking(ip, port)
        self.startServerGameLoop()

    # TODO: allow to specify allotted time (elsewhere, in an engine
    # variable/constraint to process network messages (for
    # looping through network I/O)

    # get any collected network input messages and return them in a list
    def getMessages(self):
        msgList = []

        # TODO: loop
        try:
            data = self.netInQueue.get_nowwait()
            msg = Message.inflate(data)
            msgList.append(msg)
        except Exception as e: 
            traceback.print_exc()

        return msgList

    def sendMessage(self, msg): self.netOutQueue.put(msg) 
    
    
    # TODO: ip/port other stuffs
    def connectToServer(self, ip, port):
        print("Connecting to server...")
        self.netInQueue = Queue()
        self.netOutQueue = Queue()

        p = Process(target=manager.clientSideConnectionEntryPoint, args=(self.netInQueue, self.netOutQueue, ip, port))
        p.start()
        
