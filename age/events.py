class AbstractEvent:
    def __init__(self):
        self.listeners = []
    
    def __str__(self):
        return "abstract event"
    
    def __repr__(self):
        return self.__str__()
    
    #The idea is that an event object can be 'called' like a function. This might be terrible.
    def __call__(self, *args):
        #Maybe add a log option here
        for listener in self.listeners:
            listener(self, *args)
    
    def listen(self, listener):
        self.listeners.append(listener)
    
    def stopListening(self, listener):
        self.listeners.remove(listener)

class CentralEventManager:
    def __init__(self):
        self.eventPollPair = []
    
    def addEvent(self, event, poll):
        self.eventPollPair.append((event, poll))
    
    def update(self, state):
        for pair in self.eventPollPair:
            if(pair[1]()):
                pair[0](state)
        self.eventPollPair = []

