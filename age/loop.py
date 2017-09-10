import age.events
import time

def run(gameLogicManager, gameGraphicsManager):
    print("Loop - run")
    gameRunning = True 
    centralEventManager = age.events.CentralEventManager()
    while(gameRunning):
        t0 = time.time()
        centralEventManager.update(gameLogicManager)
        gameLogicManager.update(time.time() - t0)
        #gameGraphicsManager.update(time.time() - t0)
        time.sleep(1) # TODO: dynamic sleeping

