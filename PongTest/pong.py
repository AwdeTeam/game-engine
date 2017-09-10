import sys
sys.path.append("..")
import age
import age.events
import age.networkmanager.manager

import socket
from multiprocessing import Process, Queue

INITIAL_POSITION = ( 50, 50)
INITIAL_VELOCITY = (  1,  3)

def startServer(inputQueue, outputQueue):
    p = Process(target=age.networkmanager.manager.startNetworkManager(inputQueue, outputQueue))
    p.start()
    

class PongGameLogic:
    def __init__(self, pos, vel):
        self.ballpos = pos
        self.ballvel = vel
        self.inputQueue = Queue()
        self.outputQueue = Queue()
        startServer(self.inputQueue, self.outputQueue)
    
    def update(self, dt):
        self.ballpos[0] += self.ballvel[0]*dt
        self.ballpos[1] += self.ballvel[1]*dt
    
    def registerClick(self):
        self.ballvel[0] *= -1


class OnClickEvent(age.events.AbstractEvent):
    def __str__(self):
        return "On Click Event"

pongGameLogic = PongGameLogic(INITIAL_POSITION, INITIAL_VELOCITY)
onClickEvent = OnClickEvent()
onClickEvent.listen(pongGameLogic.registerClick)

#pongGameGraphics = '''Nathan's Graphics Thingy goes here, make sure it can call the 'onClickEvent' '''
   
loop.run(pongGameLogic, pongGameGraphics)
