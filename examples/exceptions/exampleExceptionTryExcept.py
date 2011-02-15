

from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="exceptions"

q.application.start()
q.qshellconfig.interactive=True

def cause_error():
    e="d"
    f=5/0

def main():
    x = 33
    cause_error()

r="1"
try:
    main()
    print "DID NOT STOP"
except Exception as exceptionObject:
    #DO THIS ALWAYS WHEN HANDLING WITH YOUR TRY EXCEPT, THIS WILL MAKE SURE THE ERROR IS PROPERLY LOGGED
    t,v,tb = sys.exc_info()
    q.eventhandler.logTryExcept(t,v,tb)  
    print "I am now in exception, and ignored the error"    
  

print "APPLICATION DID NOT STOP, but proper logging was done and detailed stacktrace has been created."

#list of exceptions see: http://docs.python.org/library/exceptions    
    
q.application.stop()