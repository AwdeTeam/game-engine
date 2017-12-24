import sys
import time
import struct
sys.path.append("../")

from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsItem

from age.gui.window import Window
from age.logger.logger import *
from age.logger import loggers

from age.gui.objects.grid import Grid


def loop(window):
    #print("Greetings from the loop")
    pass


if __name__ == '__main__':
    logInstance = Logger()
    logInstance.addLogger(loggers.StreamLogger([0]))
    setLoggerInstance(logInstance)

    log("Setting up window...")
    app = QApplication(sys.argv)
    #ex = GoWindow()
    #app.exec_()
    #log("Done!")
    w = Window(500,500,"test", processingLoop=loop)

    # create a scene
    scene = QGraphicsScene()
    
    scene.addLine(10,10,500,500)
    g = Grid(10, 10, 10, 10)
    scene.addItem(g)


    
    w.addScene(scene)
    w.setScene(0)

    
    app.exec_()
    #w.display()
    
    
