# TODO: add prefixes table

import datetime
import sys

def timestamp():
    return datetime.datetime.now()
    
class StreamLogger:
    def __init__(self, channels, outstream=sys.stdout):
        self.channels = channels
        self.outstream = outstream

    def log(self, msg, channel):
        if channel in self.channels:
            print(msg)
            #self.outstream.write(str(msg) + "\n")

    def rescue(self): pass # not really needed
        
class FileLogger:
    def __init__(self, path, channels, includeTime=True, append=False):
        self.channels = channels
        if append: self.file = open(path, 'a')
        else: self.file = open(path, 'w')
        self.includeTime = includeTime
        #self.includePrefix = 
        
    def __del__(self):
        self.rescue()
        pass

    def rescue(self):
        self.file.close()
        
    def log(self, msg, channel):
        if channel in self.channels:
            msg = msg + "\n"
            if self.includeTime:
                msg = str(timestamp()) + " :: " + msg
            self.file.write(msg)
