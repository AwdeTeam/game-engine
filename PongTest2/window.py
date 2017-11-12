import sys
import time
import struct
sys.path.append("../")

from age.logger.logger import *
from age.logger import loggers
from age.networking import message
from age.engine import Engine

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt,pyqtSlot

import socket


#from multiprocessing import Process, Queue


class RenderLoop(QtCore.QThread):
    #renderNeeded = QtCore.pyqtSignal(object)
    #renderNeeded = QtCore.pyqtSignal(float, float)
    renderNeeded = QtCore.pyqtSignal()

    x = 50
    y = 50

    def __init__(self, engine):
        QtCore.QThread.__init__(self)
        self.engine = engine

    def run(self):
        while True:
            msgList = self.engine.getMessages()
            for msg in msgList:
                self.x = msg.data["ballX"]
                self.y = msg.data["ballY"]
                print("POS RECIEVED: {}, {}".format(self.x, self.y))
                
                try: self.renderNeeded.emit()
                except Exception as e:
                    traceback.print_exc()
                    
            time.sleep(.001)
        

class PongWindow(QWidget):

    def __init__(self, engine):
        super().__init__()
        self.initUI()
        self.x = 50
        self.y = 50
        self.mouseReleaseEvent = self.clickEvent
        self.engine = engine
        
        self.loop = RenderLoop(self.engine)
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
        #self.outputQueue.put(data.deflate())
        self.engine.sendMessage(data.deflate())

    # color = [r, g, b]
    def drawRectangle(self, event, qp, x, y, width, height, color):
        qp.fillRect(x, y, width, height, QColor(color[0],color[1],color[2]))

if __name__ == '__main__':

    logInstance = Logger()
    logInstance.addLogger(loggers.StreamLogger([0]))
    setLoggerInstance(logInstance)

    #inputQueue = Queue()
    #outputQueue = Queue()
    #p = Process(target=connect, args=(inputQueue,outputQueue))
    #p.start()
    
    e = Engine()
    e.connectToServer("127.0.0.1", 6788)
    
    log("Setting up window...")
    app = QApplication(sys.argv)
    ex = PongWindow(e)
    #sys.exit(app.exec_())
    app.exec_()
    log("Done!")
