from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QPen, QBrush
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt.pyqtSlot

from age.gui.graphics import Graphics

import time

# TODO: system of renderers? (Each type of renderer, like grid renderer, gets
# its own class?)

# window has a list of renderers to use

# each renderer needs to know about click events so they can know whether to be
# handled by it or not in some way


# renderer = displayHandler


# TODO: entities will have to keep track of whether they are supposed to "snap"
# or not? (for pieces within grids) (function for get nearest snap location,
# given two coords?)


# TODO: interpolation engine for handling simple linear animations

class ProcessingThread(QtCore.QThread):
    stateChanged = QtCore.pyqtSignal()

    def __init__(self, window, processingLoop):
        QtCore.QThread.__init__(self)
        self.window = window
        self.processingLoop = processingLoop
        
    def run(self):
        while True:
            fireChange = self.processingLoop(self.window)
            if fireChange:
                try: self.stateChanged.emit()
                except: pass
            
            time.sleep(.001)

class Window(QWidget):
    
    # NOTE: processingLoop is a function, that should accept Window as an
    # object, that returns true if state is update, and false if not
    # TODO: also pass in framerate stuff, so processingthread can handle for
    # sleep?
    def __init__(self, width, height, title, posx=100, posy=100, processingLoop):
        super().__init__()
        self.setGeometry(posx, posy, width, height)
        self.setWindowTitle(title)
        self.visualEntities = [] # expects anything with a certain set of functions (.render() etc)

        self.mouseDown = False
        self.mouseDownX = 0 # sort of acts like an offset? (visualEntities with historical access to this can use it to calc offset)
        self.mouseDownY = 0 

        self.processingThread = ProcessingThread(self, processingLoop)
        self.processingThread.stateChanged.connect(self.stateChange)

        self.qp = QPainter()
        self.graphics = Graphics(self.qp)

    def display(self):
        self.show()
        self.processingThread.start()

    def stateChange(self):
        self.repaint()

    def preMouseMoveEvent(self, event): pass
    def postMouseMoveEvent(self, event): pass
    def mouseMoveEvent(self, event):
        self.preMouseMoveEvent(event)
        
        self.postMouseMoveEvent(event)

    def preMousePressEvent(self, event): pass
    def postMousePressEvent(self, event): pass
    def mousePressEvent(self, event):
        self.preMouseMoveEvent(event)
        
        self.mouseDown = True
        self.mouseDownX = event.x()
        self.mouseDownY = event.y()
        
        self.postMouseMoveEvent(event)

    def preMouseReleaseEvent(self, event): pass
    def postMouseReleaseEvent(self, event): pass
    def mouseReleaseEvent(self, event):
        self.preMouseReleaseEvent(event)
        
        self.mouseDown = False
        
        self.preMouseReleaseEvent(event)

    def paintEvent(self, event):
        qp.begin(self)
        for visualEntity in visualEntities:
            visualEntity.render(event, self.graphics)
        qp.end()
