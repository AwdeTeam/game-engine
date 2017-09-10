import events
import time

g_mainGameRunning = True
g_centralEventManager = CentralEventManager()
g_gameLogicManager = None
g_gameGraphicsManager = None

while(g_mainGameRunning):
    t0 = time.time()
    g_centralEventManager.update(g_gameLogicManager)
    g_gameLogicManager.update(time.time() - t0)
    g_gameGraphicsManager.update(time.time() - t0)
    
