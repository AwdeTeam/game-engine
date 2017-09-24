import json

class Message:
    def __init__(self, msgType="", clientID=0, data=""):
        self.type = msgType
        self.clientID = clientID
        self.data = data
     
    def deflate(self)
        self.msgData = {"type":self.msgType, "clientID":self.client, "data":self.data
        return json.dumps(self.msgData)

    def inflate(self, msg):
        self.msgData = json.loads(msg)
        self.type = self.msgData["type"]
        self.clientID = self.msgData["clientID"]
        self.data = self.msgData["data"]
