import traceback
import sys, os
import pymonkey
from pymonkey import q
#from LogTypes import EventLevelType
#from EventObject import EventObject
from pymonkey.Shell import *

class EventHandler(object):
    '''
    The EventHandler class catches errors, messages or warnings and
    processes them
    '''
    def __init__(self):
        self._raise=q.errorconditionhandler._raise
        self.raiseCritical=q.errorconditionhandler.raiseCritical
        self.raiseUrgent=q.errorconditionhandler.raiseUrgent
        self.raiseWarning=q.errorconditionhandler.raiseWarning
        self.raiseInfo=q.errorconditionhandler.raiseInfo
        self.raiseError=q.errorconditionhandler.raiseError
        self.raiseCritical=q.errorconditionhandler.raiseCritical
        self.raiseCriticalError=q.errorconditionhandler.raiseCritical
        

    
    def logTryExcept(self,ttype, errorObject, tb):
        q.errorconditionhandler._exceptionhook(ttype, errorObject, tb,False)
                 

    def getCurrentExceptionString(self, header = None):
        """ Get description on exception currently being handled """
        if (header == None or header == ""):
            result = ""
        else:
            result = header + "\n"

        e1, e2, e3 = sys.exc_info()
        for x in traceback.format_exception(e1, e2, e3):
            result = result + x

        return result


