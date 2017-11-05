import sys
import time
import struct
sys.path.append("../")

from age.logger.logger import *
from age.logger import loggers

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QPen, QBrush
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt,pyqtSlot

from multiprocessing import Process, Queue


'''
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
'''



class Renderer:
    
    def __init__(self, widget):
        self.widget = widget

        self.xSquares = 8
        self.ySquares = 8

        self.gsHeight = 50
        self.gsWidth = 50

        self.offsetX = 10
        self.offsetY = 10

        self.boardColor = QColor(40, 100, 150)


    def getWidgetSize(self):
        return self.widget.rect().width(), self.widget.rect().height()

    def autoCalcGSToScale(self):
        width, height = self.getWidgetSize()

        self.gsHeight = height / self.ySquares
        self.gsWidth = width / self.xSquares

    def fillSquare(self, qp, xSquare, ySquare):
        x0 = xSquare*self.gsWidth + self.offsetX
        y0 = ySquare*self.gsHeight + self.offsetY
        
        qp.fillRect(x0, y0, self.gsWidth, self.gsHeight, self.boardColor)

    def render(self):
        qp = QPainter()
        qp.begin(self.widget)

        #width, height = self.getWidgetSize()

        pen = QPen(self.boardColor)
        qp.setPen(pen)

        for i in range(0, self.ySquares + 1): # + 1 to draw ending line
            qp.drawLine(self.offsetX, i*self.gsHeight + self.offsetY, self.xSquares*self.gsWidth + self.offsetX, i*self.gsHeight + self.offsetY)

        for i in range(0, self.xSquares + 1):
            qp.drawLine(i*self.gsWidth + self.offsetX, self.offsetY, i*self.gsWidth + self.offsetY, self.ySquares*self.gsHeight + self.offsetY)

        for y in range(0, self.ySquares):
            for x in range(0, self.xSquares):
                if (x + y) % 2 == 1:
                    self.fillSquare(qp, x, y)

        qp.end()
    

class PongWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.x = 50
        self.y = 50
        self.mouseReleaseEvent = self.clickEvent
        
        #self.loop = RenderLoop(self.inputQueue)
        #self.loop.renderNeeded.connect(self.positionUpdated)
        #self.loop.renderNeeded.connect(self.positionUpdated)
        #print(self.loop.renderNeeded)
        #self.loop.start()

        self.renderer = Renderer(self)



    #@pyqtSlot(float, float)
    def positionUpdated(self):
        #print("POSITION")
        self.x = self.loop.x
        self.y = self.loop.y
        self.repaint()

    def initUI(self):
        log("Initializing...")
        self.setGeometry(300, 300, 480, 480)
        self.setWindowTitle("test")
        self.show()

    def paintEvent(self, event):

        self.renderer.render()
        
        #print("painting")
        #qp = QPainter()
        #qp.begin(self)
        #self.drawRectangle(event, qp, self.x, self.y, 20, 20, [0, 150, 250])

        #for i in range(0, int(self.rect().height() / 10)):
            #i += 1
            #qp.drawLine(0,i*10,self.rect().width(),i*10)
#
        #for i in range(0, int(self.rect().width() / 10)):
            #i += 1
            #qp.drawLine(i*10,0,i*10,self.rect().height())
            #
        #
        #qp.end()
    
    def clickEvent(self, event):
        #clicked = { "dtype" : "clicked", "clickX" : event.x(), "clickY" : event.y() }
        #print("ball: ({}, {}) vs click: ({}, {})".format(self.x, self.y, event.x(), event.y()))
        #data = message.Message("data", "CID", clicked)
        #data.deflate()
        #self.outputQueue.put(data.deflate())
        pass

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
    
    log("Setting up window...")
    app = QApplication(sys.argv)
    #ex = PongWindow(inputQueue, outputQueue)
    ex = PongWindow()
    #sys.exit(app.exec_())
    app.exec_()
    #p.join()
    log("Done!")
