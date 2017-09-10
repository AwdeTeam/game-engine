import events
import time

def run(gameLogicManager, gameGraphicsManager):
    gameRunning = True 
    centralEventManager = CentralEventManager()
    while(gameRunning):
        t0 = time.time()
        g_centralEventManager.update(g_gameLogicManager)
    gameLogicManager.update(time.time() - t0)
    gameGraphicsManager.update(time.time() - t0)
