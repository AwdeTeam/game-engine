#import networking.manager as net

from multiprocessing import Process, Queue

from networking import manager, message

class Engine:
    def __init__(self):
        self.netInQueue = None
        self.netOutQueue = None
        pass


    # TODO: pass in port/other info stuffs
    def startServerNetworking(self):
        print("Starting network I/O...")
        self.netInQueue = Queue()
        self.netOutQueue = Queue()

        p = Process(target=manager.networkManagerEntryPoint, args=(self.netInQueue, self.netOutQueue))
        p.start()
        print("Network I/O running")

    def startServer(self):
        print("Starting server...")
        self.startServerNetworking()


    # TODO: ip/port other stuffs
    def connectToServer(self):
        pass
