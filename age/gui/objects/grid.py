from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem


class Grid(QGraphicsItem):
    
    def __init__(self, xSquares, ySquares, gsHeight, gsWidth):
        #super.__init__(self)
        super(Grid, self).__init__()
        self.xSquares = xSquares
        self.ySquares = ySquares
        self.gsHeight = gsHeight
        self.gsWidth = gsWidth

    def paint(self, painter, option, widget):


        for i in range(0, self.ySquares+1):
            painter.drawLine(0, i*self.gsHeight, self.xSquares*self.gsWidth, i*self.gsHeight)
        for i in range(0, self.xSquares+1):
            painter.drawLine(i*self.gsWidth, 0, i*self.gsWidth, self.ySquares*self.gsHeight)
            
        
