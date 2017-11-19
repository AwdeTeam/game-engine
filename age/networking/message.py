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
    def inflate(cls, msg):
        print("About to inflate")
        print(msg)
        msgData = json.loads(msg)
        type = msgData["type"]
        clientID = msgData["clientID"]
        data = msgData["data"]
        print("Finished loading json")
        
        message = cls(type, clientID, data)
        print("Made the message")
        return message
    
    @classmethod
    def generate(cls, cid, type="state diff", **kwargs):
        message = cls(type, cid, str(kwargs))
        #return message.deflate()
        return message
