import events
import time

MAIN_GAME_RUNNING = True
CENTRAL_EVENT_MANAGER = CentralEventManager()
GAME_LOGIC_MANAGER = None
GAME_GRAPHICS_MANAGER = None

while(MAIN_GAME_RUNNING):
    t0 = time.time()
    CENTRAL_EVENT_MANAGER.update(GAME_LOGIC_MANAGER)
    GAME_LOGIC_MANAGER.update(time.time() - t0)
    GAME_GRAPHICS_MANAGER.update(time.time() - t0)
    