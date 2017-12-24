from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QPen, QBrush
from PyQt5.QtCore import QRectF


class Grid(QGraphicsItem):
    
    def __init__(self, xSquares, ySquares, gsHeight, gsWidth):
        #super.__init__(self)
        super(Grid, self).__init__()
        self.xSquares = xSquares
        self.ySquares = ySquares
        self.gsHeight = gsHeight
        self.gsWidth = gsWidth
        self.paintCount = 0

    def paint(self, painter, option, widget):
        print("I am painting!", self.paintCount)
        self.paintCount += 1


        for i in range(0, self.ySquares+1):
            painter.drawLine(0, i*self.gsHeight, self.xSquares*self.gsWidth, i*self.gsHeight)
        for i in range(0, self.xSquares+1):
            painter.drawLine(i*self.gsWidth, 0, i*self.gsWidth, self.ySquares*self.gsHeight)
            
        
    def boundingRect(self):
        return QRectF(0.0, 0.0, float(self.xSquares*self.gsWidth), float(self.ySquares*self.gsHeight))

# NOTE: this is for testing only
class GUIElement(QGraphicsItem):
    def __init__(self):
        super(GUIElement, self).__init__()
        self.setFlag(self.ItemIgnoresTransformations, True)
        self.setFlag(self.ItemIsMovable, False)


    def paint(self, painter, option, widget):
        painter.fillRect(150, 0, 40, 20, QBrush(QColor(30,60,120)))
        
    def boundingRect(self):
        return QRectF(150.0, 0.0, 40.0, 20.0)
