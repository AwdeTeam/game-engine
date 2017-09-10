loggerInstance = None
loggerInitialized = False

def setLoggerInstance(logger):
    global loggerInstance
    global loggerInitialized
    loggerInstance = logger
    loggerInitialized = True
    
def log(msg, channel=0):
    global loggerInstance
    global loggerInitialized

    if not loggerInitialized: return -1 # TODO: should this raise an exception?
    loggerInstance.log(msg, channel)
    return 0

class Logger:
    def __init__(self):
        self.loggingSystems = []

    def __del__(self):
        self.halt()
        self.loggerInitialized = False

    def halt(self):
        for system in self.loggingSystems:
            system.rescue()

    def log(self, msg, channel=0):
        for system in self.loggingSystems:
            system.log(msg, channel)

    def addLogger(self, logger):
        self.loggingSystems.append(logger)
