import age.events
import time

def run(gameLogicManager, gameGraphicsManager):
    print("Loop - run")
    gameRunning = True 
    centralEventManager = age.events.CentralEventManager()
    while(gameRunning):
        t0 = time.time()
        centralEventManager.update(gameLogicManager)
        dt = time.time() - t0
        #dt *= 100000
        gameLogicManager.update(dt)
        #gameGraphicsManager.update(time.time() - t0)
        time.sleep(.3) # TODO: dynamic sleeping

