from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QPen, QBrush
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt,pyqtSlot

class Graphics:

    def __init__(self, qpainter):
        self.qpainter = qpainter
        self.defFillColor = QColor(200,200,200,255)
        self.defBorderColor = QColor(0,0,0,255)
        self.defThickness = 1

    def setFillColor(color):
        self.defFillColor = color
        
    def setBorderColor(color):
        self.defBorderColor = color

    def setThickness(thickness):
        self.defThickness = thickness

    # None means default
    def line(self, x1, y1, x2, y2, color=None, thickness=None):
        if not color: color = self.defBorderColor
        if not thickness: thickness = self.defThickness

        pen = QPen(color)
        pen.setWidth(thickness)
        self.qpainter.setPen(pen)

        self.qpainter.drawLine(x1, y1, x2, y2)

    # TODO: border?
    def rect(self, x1, y1, width, height, color=None):
        if not color: color = self.defFillColor

        self.qpainter.fillRect(x1, y1, width, height, color)
