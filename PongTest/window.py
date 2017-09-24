import sys
import struct
sys.path.append("../")

from age.logger.logger import *
from age.logger import loggers

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

import socket


from multiprocessing import Process, Queue

def connect(communicationQueue):
    log("Setting up socket...")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "localhost"
    port = 6789

    s.connect((host,port))

    running = True
    while running:
        #log("Socket listening...")
        msg = recv_msg(s)
        log("Received a message: " + str(msg))
        if msg == "!STOP":
            running = False
    log("Shutting down socket")
    s.close()

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

class PongWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        log("Initializing...")
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle("test")
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangle(event, qp, 5, 5, 20, 20, [0, 150, 250])
        qp.end()

    # color = [r, g, b]
    def drawRectangle(self, event, qp, x, y, width, height, color):
        qp.fillRect(x, y, width, height, QColor(color[0],color[1],color[2]))

if __name__ == '__main__':

    logInstance = Logger()
    logInstance.addLogger(loggers.StreamLogger([0]))
    setLoggerInstance(logInstance)

    q = Queue()
    p = Process(target=connect, args=(q,))
    p.start()
    
    log("Setting up window...")
    app = QApplication(sys.argv)
    ex = PongWindow()
    #sys.exit(app.exec_())
    app.exec_()
    p.join()
    log("Done!")
