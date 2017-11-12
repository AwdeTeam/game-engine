import sys
sys.path.append("..")
import age
import age.events
#import age.networkmanager.manager
import age.loop
from age.networking import message

from age.engine import Engine

import socket
from multiprocessing import Process, Queue

INITIAL_POSITION = [ 50, 50]
INITIAL_VELOCITY = [  1,  3]
BALL_SIZE = 20

class PongGameLogic:
    #def __init__(self, pos, vel, inputQueue, outputQueue):
    def __init__(self, pos, vel, siz):
        print("Initializing game")
        self.ballpos = pos
        self.ballvel = vel
        self.ballsiz = siz
        self.engine = Engine()
        
        self.engine.startServer("127.0.0.1", 6788, self)
        print("Server started")
    
    def update(self, dt):
        #print("Running game update")
        #self.outputQueue.put("Hi!")
        #self.ballpos[0] += self.ballvel[0]*dt
        #self.ballpos[1] += self.ballvel[1]*dt
        self.ballpos[0] += self.ballvel[0]*.1
        self.ballpos[1] += self.ballvel[1]*.1
        
        state = { "dtype" : "gameState", "ballX" : self.ballpos[0], "ballY" : self.ballpos[1], "size" : self.ballsiz }
        stateMsg = message.Message("data", "CID", state)
        #stateMsg.deflate()
        print("POS SENT: {}, {}".format(self.ballpos[0], self.ballpos[1]))
        #self.outputQueue.put(stateMsg.deflate())

        self.engine.sendMessage(stateMsg)

        msgList = self.engine.getMessages()
        for msg in msgList:
            if msg.type == "data":
                print("Incoming data: {}\t\tBall Position: ({},{})".format(data.data,self.ballpos[0],self.ballpos[1]))
                if(msg.data["dtype"] == "clicked"):
                    print("Clicked on Ball!")
                    self.checkClick(int(msg.data["clickX"]), int(msg.data["clickY"]))

        
        
        #try:
            #inData = self.inputQueue.get_nowait()
            ##print("SERVER GOT DATA!!!!")
            #data = message.Message()
            #data.inflate(inData)
            #if(data.type == "data"):
                #print("Incoming data: {}\t\tBall Position: ({},{})".format(data.data,self.ballpos[0],self.ballpos[1]))
                #if(data.data["dtype"] == "clicked"):
                    #print("Clicked on Ball!")
                    #self.checkClick(int(data["data"]["clickX"]), int(data["data"]["clickY"]))
        #except:
            #pass
    
    def checkClick(self, x, y):
        if(x > self.ballpos[0] and x < self.ballpos[0]+self.ballsiz and \
           y > self.ballpos[1] and y < self.ballpos[1]+self.ballsiz):
           self.registerClick()
    
    def registerClick(self):
        self.ballvel[0] *= -1


class OnClickEvent(age.events.AbstractEvent):
    def __str__(self):
        return "On Click Event"

if __name__ == '__main__':
    pongGameLogic = PongGameLogic(INITIAL_POSITION, INITIAL_VELOCITY, BALL_SIZE)
    onClickEvent = OnClickEvent()
    onClickEvent.listen(pongGameLogic.registerClick)

    pongGameGraphics = None #Nathan's Graphics Thingy goes here, make sure it can call the 'onClickEvent'
       
    #print("Just before loop")
    #age.loop.run(pongGameLogic, pongGameGraphics)
    #age.loop.run(pongGameLogic)
