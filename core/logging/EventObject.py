import time, traceback

from LogTypes import LogType
from LogTypes import *
from pymonkey import q

class EventObject(object):
    @classmethod
    def fromLog(cls, logObj):
        if logObj.type != int(LogType.EVENT):
            raise TypeError("not an event object")        
        message=logObj.message
        level=logObj.level
        typeid=logObj.getTagObject().tagGet('eventtype')
        tags=logObj.tags
        source=logObj.source        
        backtrace, messageprivate, message = message.split('>>>')
        return EventObject(message, messageprivate, level, typeid, tags, source, backtrace)

    def __init__(self, message, messageprivate='', level=None, typeid='', tags='', source='', backtrace=None):
        """
        this object represents an event
        """
        self.time = time.time()
        self.source = source 
        self.tags = tags
        self.errormessagepublic= message
        self.errormessageprivate = messageprivate
        self.backtrace = ''
        self.agentguid = ''
        self.level = level or EventLevelType.WARNING
        self.eventtype = typeid
        if backtrace is None and int(self.level) < 4:
            stack=""
            for x in traceback.format_stack():
                ignore=False
                if x.find("IPython")<>-1 or x.find("EventHandler")<>-1 or x.find("EventObject")<>-1 or x.find("traceback.format")<>-1 or x.find("ipython console")<>-1:
                    ignore=True
                stack = "%s"%(stack+x if not ignore else stack)
            self.backtrace = stack
        else:
            self.backtrace = backtrace
    def getBacktrace(self):
        """
        get backtrace and put in appropriate field
        """
        return self.backtrace
        
        
    def getTagObject(self):
        """
        return event tags represented as a tagobject
        """
        return q.base.tags.getObject(self.tags)
        
    def getLogMessageString(self):
        """
        translate to log string
        format see: http://bitbucket.org/despiegk/ssospecs/src/tip/1.1/concepts/EventManagement/1.%20pylabsLogEventMgmt.wiki
        @return message string in format time(epoch)|source(string)|level(0-10)|tags|logmessage\n 
        """
        now = time.time()
        self.source = self.source.strip().replace("\r\n", "/n").replace("\n", "/n").replace("|","/|").replace(":","/:")
        message = '%s>>>%s>>>%s\n'%(self.backtrace, self.errormessageprivate, self.errormessagepublic)
        tags = 'sourceapplication:%s eventtype:%s eventlevel:%s eventagent:%s%s'%(self.source, self.eventtype, int(self.level), self.agentguid, ' ' + self.tags if self.tags else '')
        message = message.strip().replace("\r\n", "/n").replace("\n", "/n").replace("|","/|").replace(":","/:")
        
        return '%s|%s|%s|%s|%s|%s\n'%(int(LogType.EVENT), now, self.source, int(self.level), tags, message)

    def __str__(self):
        """
        nice formatting of event, human readable
        """
        return '%s\n*************************\n%s\n*************************\n%s\n'%(self.backtrace, self.errormessageprivate, self.errormessagepublic)
    
    __repr__ = __str__
