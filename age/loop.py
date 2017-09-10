import events
import time

def run(gameLogicManager, gameGraphicsManager):
    gameRunning = True 
    centralEventManager = CentralEventManager()
    while(gameRunning):
        t0 = time.time()
        centralEventManager.update(gameLogicManager)
        gameLogicManager.update(time.time() - t0)
        gameGraphicsManager.update(time.time() - t0)

    time.sleep(.1) # TODO: dynamic sleeping
