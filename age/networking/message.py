import json

class Message:
    def __init__(self, msgType="", clientID=0, data=""):
        self.type = msgType
        self.clientID = clientID
        self.data = data
     
    def deflate(self):
        self.msgData = { "type":self.type, "clientID":self.clientID, "data":self.data }
        return json.dumps(self.msgData)

    @classmethod
    def inflate(self, msg):
        msgData = json.loads(msg)
        type = self.msgData["type"]
        clientID = self.msgData["clientID"]
        data = self.msgData["data"]
        
        message = cls(type, clientID, data)
        return message
    
    @classmethod
    def generate(cls, cid, type="state diff", **kwargs):
        message = cls(type, cid, str(kwargs))
        return message.deflate()
