import loggers
from logger import *

print("Running manual logging test...")
logInstance = Logger()
logInstance.addLogger(loggers.StreamLogger([0]))
setLoggerInstance(logInstance)
log("Hello world!")
print("Manual test complete")
