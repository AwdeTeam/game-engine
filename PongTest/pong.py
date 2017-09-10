import sys
sys.path.append("..")
import age
import events

INITIAL_POSITION = ( 50, 50)
INITIAL_VELOCITY = (  1,  3)

class PongGameLogic:
    def __init__(self, pos, vel):
        self.ballpos = pos
        self.ballvel = vel
    
    def update(self, dt):
        self.ballpos[0] += self.ballvel[0]*dt
        self.ballpos[1] += self.ballvel[1]*dt
    
    def registerClick(self):
        self.ballvel[0] *= -1


class OnClickEvent(AbstractEvent):
    def __str__(self):
        return "On Click Event"

pongGameLogic = PongGameLogic(INITIAL_POSITION, INITIAL_VELOCITY)
onClickEvent = OnClickEvent()
onClickEvent.listen(pongGameLogic.registerClick)

pongGameGraphics = '''Nathan's Graphics Thingy goes here, make sure it can call the 'onClickEvent' '''
   
loop.run(pongGameLogic, pongGameGraphics)
        