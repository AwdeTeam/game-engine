import sys
import time
import struct
sys.path.append("../")

from age.logger.logger import *
from age.logger import loggers
from age.networkmanager import message

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt,pyqtSlot

import socket


from multiprocessing import Process, Queue

def connect(inputQueue, outputQueue):
    log("Setting up socket...")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "localhost"
    port = 6789

    s.connect((host,port))
    s.setblocking(False)

    running = True
    while running:
        msg = ""
        #log("Socket listening...")
        try: 
            msg = recv_msg(s)
            log("Received a message: " + str(msg))
            if msg == "!STOP":
                running = False
            inputQueue.put(msg)
        except: pass

            
        #log("Socket sending...")
        try: 
            data = outputQueue.get_nowait()
            #print("SENDING: ", data)
            send_msg(s, data)
        except: pass
        
        time.sleep(.1)
    log("Shutting down socket")
    s.close()
    
def send_msg(sock, msg):
    try:
        msg = struct.pack('>I', len(msg)) + msg.encode('ascii')
        sock.sendall(msg)
    except Exception as e:
        traceback.print_exc()

# thanks to https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data 
# Read message length and unpack it into an integer
def recv_msg(sock):
    #raw_msglen = recvall(sock, 4)
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

class RenderLoop(QtCore.QThread):
    #renderNeeded = QtCore.pyqtSignal(object)
    #renderNeeded = QtCore.pyqtSignal(float, float)
    renderNeeded = QtCore.pyqtSignal()

    x = 50
    y = 50

    def __init__(self, queue):
        QtCore.QThread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            try:
                data = self.queue.get_nowait()
                m = message.Message()
                m.inflate(data)
                self.x = m.data["ballX"]
                self.y = m.data["ballY"]
                print("POS RECIEVED: {}, {}".format(self.x, self.y))
                try: self.renderNeeded.emit()
                except Exception as e:
                    traceback.print_exc()
            except: pass
            time.sleep(.001)

class PongWindow(QWidget):

    def __init__(self, inputQueue, outputQueue):
        super().__init__()
        self.initUI()
        self.x = 50
        self.y = 50
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue
        self.mouseReleaseEvent = self.clickEvent
        
        self.loop = RenderLoop(self.inputQueue)
        #self.loop.renderNeeded.connect(self.positionUpdated)
        self.loop.renderNeeded.connect(self.positionUpdated)
        print(self.loop.renderNeeded)
        self.loop.start()


    #@pyqtSlot(float, float)
    def positionUpdated(self):
        #print("POSITION")
        self.x = self.loop.x
        self.y = self.loop.y
        self.repaint()

    def initUI(self):
        log("Initializing...")
        self.setGeometry(300, 300, 480, 270)
        self.setWindowTitle("test")
        self.show()

    def paintEvent(self, event):
        #print("painting")
        qp = QPainter()
        qp.begin(self)
        self.drawRectangle(event, qp, self.x, self.y, 20, 20, [0, 150, 250])
        qp.end()
    
    def clickEvent(self, event):
        clicked = { "dtype" : "clicked", "clickX" : event.x(), "clickY" : event.y() }
        print("ball: ({}, {}) vs click: ({}, {})".format(self.x, self.y, event.x(), event.y()))
        data = message.Message("data", "CID", clicked)
        #data.deflate()
        self.outputQueue.put(data.deflate())

    # color = [r, g, b]
    def drawRectangle(self, event, qp, x, y, width, height, color):
        qp.fillRect(x, y, width, height, QColor(color[0],color[1],color[2]))

if __name__ == '__main__':

    logInstance = Logger()
    logInstance.addLogger(loggers.StreamLogger([0]))
    setLoggerInstance(logInstance)

    inputQueue = Queue()
    outputQueue = Queue()
    p = Process(target=connect, args=(inputQueue,outputQueue))
    p.start()
    
    log("Setting up window...")
    app = QApplication(sys.argv)
    ex = PongWindow(inputQueue, outputQueue)
    #sys.exit(app.exec_())
    app.exec_()
    p.join()
    log("Done!")
