import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


class PongWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
    app = QApplication(sys.argv)
    ex = PongWindow()
    sys.exit(app.exec_())
