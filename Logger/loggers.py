# TODO: add prefixes table

class ConsoleLogger:
    def __init__(self, channels):
        self.channels = channels

    def log(self, msg, channel):
        if channel in self.channels:
            print(msg)
        
class FileLogger:
    def __init__(self, path, channels):
        self.channels = channels
        self.file = open(path, 'w')
        
    def __del__(self):
        self.file.close()
        pass
        
    def log(self, msg, channel):
        if channel in self.channels:
            self.file.write(msg)
        
