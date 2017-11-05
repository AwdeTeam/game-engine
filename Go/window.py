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


class Renderer:
    
    def __init__(self, widget):
        self.widget = widget

        self.xSquares = 8
        self.ySquares = 8

        self.gsHeight = 50
        self.gsWidth = 50

        self.offsetX = 10
        self.offsetY = 10

        self.lineColor = QColor(40, 100, 150)
        self.boardColor = QColor(40, 100, 150)


    def getWidgetSize(self):
        return self.widget.rect().width(), self.widget.rect().height()

    def autoCalcGSToScale(self):
        width, height = self.getWidgetSize()

        self.gsHeight = height / self.ySquares
        self.gsWidth = width / self.xSquares

    def fillSquare(self, qp, xSquare, ySquare):
        x0 = xSquare*self.gsWidth + self.offsetX + 1
        y0 = ySquare*self.gsHeight + self.offsetY + 1
        
        qp.fillRect(x0, y0, self.gsWidth - 1, self.gsHeight - 1, self.boardColor)

    def render(self):
        qp = QPainter()
        qp.begin(self.widget)

        #width, height = self.getWidgetSize()

        pen = QPen(self.lineColor)
        qp.setPen(pen)
        
        for y in range(0, self.ySquares):
            for x in range(0, self.xSquares):
                if (x + y) % 2 == 1:
                    self.fillSquare(qp, x, y)

        for i in range(0, self.ySquares + 1): # + 1 to draw ending line
            qp.drawLine(self.offsetX, i*self.gsHeight + self.offsetY, self.xSquares*self.gsWidth + self.offsetX, i*self.gsHeight + self.offsetY)

        for i in range(0, self.xSquares + 1):
            qp.drawLine(i*self.gsWidth + self.offsetX, self.offsetY, i*self.gsWidth + self.offsetX, self.ySquares*self.gsHeight + self.offsetY)


        qp.end()
    

class PongWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.x = 50
        self.y = 50
        self.mouseReleaseEvent = self.mouseReleaseEvent
        self.mousePressEvent = self.mousePressEvent
        self.mouseMoveEvent = self.mouseMoveEvent
        
        self.renderer = Renderer(self)

        self.dragging = False
        self.xOff = 0
        self.yOff = 0


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
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.renderer.offsetX = event.x() - self.xOff
            self.renderer.offsetY = event.y() - self.yOff
            self.repaint()
            

    def mousePressEvent(self, event):
        self.dragging = True
        self.xOff = event.x() - self.renderer.offsetX
        self.yOff = event.y() - self.renderer.offsetY
            
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
        #clicked = { "dtype" : "clicked", "clickX" : event.x(), "clickY" : event.y() }
        #print("ball: ({}, {}) vs click: ({}, {})".format(self.x, self.y, event.x(), event.y()))
        #data = message.Message("data", "CID", clicked)
        #data.deflate()
        #self.outputQueue.put(data.deflate())


    # color = [r, g, b]
    def drawRectangle(self, event, qp, x, y, width, height, color):
        qp.fillRect(x, y, width, height, QColor(color[0],color[1],color[2]))

if __name__ == '__main__':

    logInstance = Logger()
    logInstance.addLogger(loggers.StreamLogger([0]))
    setLoggerInstance(logInstance)
    
    log("Setting up window...")
    app = QApplication(sys.argv)
    ex = PongWindow()
    app.exec_()
    log("Done!")
