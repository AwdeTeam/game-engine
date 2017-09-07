import unittest
import imp
import os
import sys
from io import StringIO

import logger # only for global testing
from logger import *

import loggers

class TestGlobalLoggerFunctions(unittest.TestCase):
    def setUp(self):
        imp.reload(logger)
    
    def test_uninitializedLog(self):
        self.assertEqual(logger.log(''), -1)

    def test_initalizedLog(self):
        logInstance = logger.Logger()
        logger.setLoggerInstance(logInstance)
        
        self.assertTrue(logger.loggerInitialized, "logger isn't initialized")
        self.assertEqual(logger.log(''), 0, "global log failed")

class TestStreamLogger(unittest.TestCase):
    def setUp(self):
        logInstance = Logger()
        self.out = StringIO()
        logInstance.addLogger(loggers.StreamLogger([0], self.out))
        setLoggerInstance(logInstance)

    def test_streamLog(self):
        msg = "hello world"
        log(msg)
        output = self.out.getvalue().strip()
        self.assertEqual(output, msg, "Stream output wasn't correct")

class TestFileLogger(unittest.TestCase):
    def setUp(self):
        try: os.remove("testlogs/test.log")
        except: pass
        self.logInstance = Logger()
        self.logInstance.addLogger(loggers.FileLogger("testlogs/test.log", [0]))
        setLoggerInstance(self.logInstance)

    def countLines(self, path):
        with open(path) as f:
            return len(f.readlines())

    def test_logCreated(self):
        log("hi there")
        #del self.logInstance
        self.logInstance.halt()
        self.assertTrue(os.path.isfile("testlogs/test.log"), "Log file wasn't created")
        self.assertEqual(self.countLines("testlogs/test.log"), 1, "Log had more than one line written to it")

    def test_append(self):
        log("hi there")
        self.logInstance.halt()
        self.logInstance = Logger()
        self.logInstance.addLogger(loggers.FileLogger("testlogs/test.log", [0], append=True))
        setLoggerInstance(self.logInstance)
        log("hi again!")
        self.logInstance.halt()
        self.assertEqual(self.countLines("testlogs/test.log"), 2, "Log didn't successfully append")
        

    #def tearDown(self):
        #del log


if __name__ == '__main__':
    unittest.main()
