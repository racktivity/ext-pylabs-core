# Exceptions

## Python Exception

[[code]]
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
    raise RuntimeError("test raise")

r="1"
main()

q.application.stop()
[[/code]]

above example will raise an error and show how the stacktrace mechanism works


## Using Transactions

[[code]]
from pylabs.InitBase import *
#from pylabs.Shell import *

q.application.appname="exceptions"

q.application.start()
q.qshellconfig.interactive=True

def cause_error():
    e="d"
    f=5/0

def main():
    x = 33
    cause_error()

##Definition:   q.action.start(self, description, errormessage=None, resolutionmessage=None, show=DEPRECATED, messageLevel=DEPRECATED)
##Documentation:
    ##Start a new action       
    ##Parameters:    
    ##- description: Description of the action
    ##- errormessage: Error message displayed to the user when the action
    ##- resolutionmessage: Resolution message displayed to the user when
 
r="1"

print "First demonstrate how actions work"
print "FOR NOW: output is not shown when in an action, this behaviour will be changed because only logging will be made available on different levels"
q.action.start("first action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("1")
q.action.start("2nd action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("2")
q.action.start("3e action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("3")
q.action.stop()
q.action.stop()
q.action.stop()

print "\n\n\n"
print "what if you want to print a clean errormessage even when error happens 5 levels deep"
q.action.start("first action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("1")
q.action.start("2nd action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("2")
q.action.start("3e action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("3")
main()#main()#is going to throw an error
q.action.stop()
q.action.stop()
q.action.stop()

q.application.stop()
[[/code]]

## Try/Except Example 

WE DO NOT RECOMMEND TO USE TRY EXCEPTS BUT IF YOU HAVE NO CHOICE FOLLOW THE FOLLOWING SCHEME

[[code]]
from pylabs.InitBase import *
#from pylabs.Shell import *

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
[[/code]]
