import pdb

import sys
sys.path.append("..")
import age
import age.events
import age.networkmanager.manager
import age.loop

import socket
from multiprocessing import Process, Queue

INITIAL_POSITION = [ 50, 50]
INITIAL_VELOCITY = [  1,  3]

def startServer(inputQueue, outputQueue):
    print("Starting server")
    p = Process(target=age.networkmanager.manager.startNetworkManager, args=(inputQueue, outputQueue))
    p.start()

class PongGameLogic:
    #def __init__(self, pos, vel, inputQueue, outputQueue):
    def __init__(self, pos, vel):
        print("Initializing game")
        self.ballpos = pos
        self.ballvel = vel
        self.inputQueue = Queue()
        self.outputQueue = Queue()
        #pdb.set_trace()
        startServer(self.inputQueue, self.outputQueue)
        print("Server started")
    
    def update(self, dt):
        print("Running game update")
        self.outputQueue.put("Hi!")
        self.ballpos[0] += self.ballvel[0]*dt
        self.ballpos[1] += self.ballvel[1]*dt
    
    def registerClick(self):
        self.ballvel[0] *= -1


class OnClickEvent(age.events.AbstractEvent):
    def __str__(self):
        return "On Click Event"

if __name__ == '__main__':
    pongGameLogic = PongGameLogic(INITIAL_POSITION, INITIAL_VELOCITY)
    onClickEvent = OnClickEvent()
    onClickEvent.listen(pongGameLogic.registerClick)

    pongGameGraphics = None #Nathan's Graphics Thingy goes here, make sure it can call the 'onClickEvent'
       
    print("Just before loop")
    age.loop.run(pongGameLogic, pongGameGraphics)
