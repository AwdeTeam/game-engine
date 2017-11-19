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

import gameboard as gb


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

        self.darkPiece = QColor(20, 20, 20)
        self.lightPiece = QColor(200, 200, 200)

        self.selection = QColor(255, 0, 0)

        self.darkBrush = QBrush(self.darkPiece)
        self.lightBrush = QBrush(self.lightPiece)
        self.selectedBrush = QBrush(self.selection)

        self.pieceWidth = 40
        self.pieceHeight = 40


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

    # side = "white" "black"
    # TODO: this would end up in user code, outside engine
    def drawPiece(self, qp, xSquare, ySquare, side, king):
        pieceOffX = (self.gsWidth - self.pieceWidth) / 2
        pieceOffY = (self.gsHeight - self.pieceHeight) / 2

        x0 = xSquare*self.gsWidth + self.offsetX + pieceOffX
        y0 = ySquare*self.gsHeight + self.offsetY + pieceOffY

        if side == "black": qp.setBrush(self.darkBrush)
        elif side == "white": qp.setBrush(self.lightBrush)
        else: qp.setBrush(self.selectedBrush)

        qp.drawEllipse(x0, y0, self.pieceWidth, self.pieceHeight)

    # TODO: this would go outside engine as well
    def drawBoard(self, qp, gameboard, selectedX, selectedY):
        for x in range(8):
            for y in range(8):
                token = gameboard.getToken(x, y)
                if("empty" not in token):
                    if selectedX == x and selectedY == y: self.drawPiece(qp, x, y, "select", "K" in token)
                    else: self.drawPiece(qp, x, y, token.split()[0], "K" in token)

    def render(self, gameboard, selectedX, selectedY):
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

        self.drawBoard(qp, gameboard, selectedX, selectedY)

        qp.end()


class GoWindow(QWidget):

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

        self.pieceSelected = False
        self.selectedPieceX = -1
        self.selectedPieceY = -1

        self.targetX = 0
        self.targetY = 0

        self.board = gb.Gameboard()


    #@pyqtSlot(float, float)
    def positionUpdated(self):
        #print("POSITION")
        self.x = self.loop.x
        self.y = self.loop.y
        self.repaint()

    def initUI(self):
        log("Initializing...")
        self.setGeometry(10, 300, 280, 480)
        self.setWindowTitle("test")
        self.show()

    def paintEvent(self, event):
        self.renderer.render(self.board, self.selectedPieceX, self.selectedPieceY)

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.renderer.offsetX = event.x() - self.xOff
            self.renderer.offsetY = event.y() - self.yOff
            self.repaint()



    def mousePressEvent(self, event):
        # check if clicking on the board or not
        if event.x() > self.renderer.offsetX and event.x() < (self.renderer.offsetX + self.renderer.gsWidth * self.renderer.xSquares) and event.y() > self.renderer.offsetY and event.y() < (self.renderer.offsetY + self.renderer.gsHeight * self.renderer.ySquares):
                
            board_x = int((event.x() - self.renderer.offsetX)/(self.renderer.gsWidth))
            board_y = int((event.y() - self.renderer.offsetY)/(self.renderer.gsHeight))

            if not self.pieceSelected:
                if(self.board.getToken(board_x, board_y != "empty")):
                    self.pieceSelected = True
                    self.selectedPieceX = board_x
                    self.selectedPieceY = board_y
            else:
                print("Attempting move...")
                thing = self.board.move(self.selectedPieceX, self.selectedPieceY, board_x, board_y)
                print(thing)
                self.pieceSelected = False
                self.selectedPieceX = -1
                self.selectedPieceY = -1
                
            self.repaint()
        else:
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
    ex = GoWindow()
    app.exec_()
    log("Done!")

