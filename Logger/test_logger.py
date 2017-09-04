import unittest
import imp

import logger # only for global testing
from logger import *

import logger_console

class TestGlobalLoggerFunctions(unittest.TestCase):
    def setUp(self):
        imp.reload(logger)
    
    def test_uninitializedLog(self):
        self.assertEqual(logger.log(''), -1)

    def test_initalizedLog(self):
        log = logger.Logger()
        logger.setLoggerInstance(log)
        
        self.assertTrue(logger.loggerInitialized, "logger isn't initialized")
        self.assertEqual(logger.log(''), 0, "global log failed")

class TestConsoleLogger(unittest.TestCase):
    def setUp(self):
        log = Logger()
        log.addLogger(logger_console.ConsoleLogger([0]))
        setLoggerInstance(log)

    def test_logging(self):
        log("")

if __name__ == '__main__':
    unittest.main()
