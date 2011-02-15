import time
import itertools
from collections import defaultdict
import signal
import sys
import socket
import SocketServer
import pprint

from pylabs.logging.LogObject import LogObject
from pylabs.logging.LogTypes import LogType
from pylabs import q

DEFAULT_PORT = 9998


class ManagementProtocol(object):
    SET_SCREEN_WIDTH = "setScreenWidth"
    SET_MIN_LEVEL = "setMinLevel"
    SET_MAX_LEVEL = "setMaxLevel"
    SET_SCREEN_WIDTH = "setScreenWidth"
    ENABLE_EVENTS = "enableEvents"
    FILTER_ON_TAGS = "filterOnTags"
    FILTER_SOURCE_APPLICATIONS = "filterSourceApplications"
    SHOW_SOURCE_APPLICATIONS = "showSourceApplications"
    SHOW_FOUND_TAGS = "showFoundTags"
    PPRINT = "prettyPrint"
    CMD_TOKEN = "::cmd::"
    MSG_TERMINATOR = '$$'
    
        
        
class BaseLogConsole(object):
    
    RECIEVING_BUFFER_SIZE = 8192
    DEFAULT_SCREENWIDTH = 120
     
    def __init__(self, ip='localhost', port=DEFAULT_PORT):
        self.ip = ip
        self.port = int(port)                
        self.started = False
        self._screenWidth = self.DEFAULT_SCREENWIDTH
        self._enableEvents = True
        self._pprint = True
        self._minLevel = 0
        self._maxLevel = 11
        self._includedTags = set()
        self._excludedTags = set()
        self._foundLabels = set()
        self._labelLastSeenAt = dict()
        self._foundTags = dict()
        self._tagLastSeenAt = dict()
        self._includedApps = set()
        self._foundApplications = set()
        self._applicationLastSeenAt = dict()
                
    def start(self, screenWidth=DEFAULT_SCREENWIDTH):
        if self.started:
            return
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.ip, self.port))
            sock.listen(5)
            self.started = True
            recievedData = ''
            try:
                while True:
                    newSocket, address = sock.accept()
                    q.console.echo( 'Got a Connection from ', address)
                    while True:
                        recievedData = '%s%s'%(recievedData, newSocket.recv(self.RECIEVING_BUFFER_SIZE))
                        if not recievedData:
                            q.console.echo( 'Lost connection from ', address)
                            break
                        else:
                            recievedData = self.proccessData(recievedData)
                    newSocket.close()
            finally:
                sock.close()
            
    def proccessData(self, recievedData):
        """
        splits the data based the msg separator and add them as nodes in zookeeper
        """
        messages = recievedData.split(ManagementProtocol.MSG_TERMINATOR)
        if len(messages) == 1:
            return recievedData
        lastMessage = messages.pop(-1)        
        for message in messages:
            self.printMessage(message, self._pprint)
    
        return lastMessage
    
    
    def showFoundApplications(self, sinceXNrMinutes=0):
        q.console.echo( self._filterSince(self._applicationLastSeenAt, sinceXNrMinutes))
    
    
    def showFoundTags(self, sinceXNrMinutes=0):
        self.showFoundLabels(sinceXNrMinutes)
        q.console.echo( self._filterSince(self._tagLastSeenAt, sinceXNrMinutes))
        
    def showFoundLabels(self, sinceXNrMinutes=0):
        q.console.echo( self._filterSince(self._labelLastSeenAt, sinceXNrMinutes))


    def _filterSince(self, itemsWithEpoch, nrMinutes):
        sinceSeconds = (nrMinutes + 1) * 60
        now = time.time()
        startTime = now -sinceSeconds
        items = itemsWithEpoch.items()
        return map(lambda tup: tup[0], filter(lambda tup: tup[1] >= startTime, items))

        
    def processCommandMessage(self, message):
        cmdargs = message.split()
        if len(cmdargs) < 2:
            q.console.echo( "Invalid command received: %s"%message)
            return
        command = cmdargs[1]
        cmdargs = cmdargs[2:]
        
        if command == ManagementProtocol.SET_SCREEN_WIDTH:
            if len(cmdargs) < 1:
                q.console.echo( "Wrong number of arguments, usage ::cmd:: %s 70 "%ManagementProtocol.SET_SCREEN_WIDTH)
            self._screenWidth = int(cmdargs[0])
            
        if command == ManagementProtocol.SET_MIN_LEVEL:
            if len(cmdargs) < 1:
                q.console.echo( "Wrong number of arguments, usage ::cmd:: %s 7 "%ManagementProtocol.SET_MIN_LEVEL  )              
            self._minLevel = int(cmdargs[0])
                
        if command == ManagementProtocol.SET_MAX_LEVEL:
            if len(cmdargs) < 1:
                q.console.echo( "Wrong number of arguments, usage ::cmd:: %s 7 "%ManagementProtocol.SET_MAX_LEVEL)
            self._maxLevel = int(cmdargs[0])    
            
        if command == ManagementProtocol.SET_SCREEN_WIDTH:
            if len(cmdargs) < 1:
                q.console.echo( "Wrong number of arguments, usage ::cmd:: %s 120 "%ManagementProtocol.SET_SCREEN_WIDTH)
            self._screenWidth = int(cmdargs[0])                
            
        if command == ManagementProtocol.ENABLE_EVENTS:
            if len(cmdargs) < 1:
                q.console.echo( "Wrong number of arguments, usage ::cmd:: %s True"%ManagementProtocol.ENABLE_EVENTS)
            self._enableEvents = ('True' == cmdargs[0].capitalize())
                                                 
        if command == ManagementProtocol.FILTER_ON_TAGS:
            if len(cmdargs) < 1:
                q.console.echo( "Wrong number of arguments, usage ::cmd:: %s "%ManagementProtocol.FILTER_ON_TAGS)
            try:
                self._includedTags, self._excludedTags = map(set, eval(''.join(cmdargs)))#converts the tuples to sets
            except:
                #handle any exception from eval gracefully
                self._includedTags, self._excludedTags = set(), set()
        
        if command == ManagementProtocol.SHOW_SOURCE_APPLICATIONS:
            if len(cmdargs) < 1:
                q.console.echo( "Wrong number of arguments, usage ::cmd:: %s 5"%ManagementProtocol.SHOW_SOURCE_APPLICATIONS)
            self.showFoundApplications(int(cmdargs[0]))
            
        if command == ManagementProtocol.FILTER_SOURCE_APPLICATIONS:
            if len(cmdargs) < 1:
                print "Wrong number of arguments, usage ::cmd:: %s applicationserver"%ManagementProtocol.FILTER_SOURCE_APPLICATIONS
            self._includedApps = set(eval(''.join(cmdargs)))
        

        if command == ManagementProtocol.SHOW_FOUND_TAGS:
            if len(cmdargs) < 1:
                print "Wrong number of arguments, usage ::cmd:: %s 5"%ManagementProtocol.SHOW_FOUND_TAGS
            self.showFoundTags(int(cmdargs[0]))

        if command == ManagementProtocol.PPRINT:
            if len(cmdargs) < 1:
                print "Wrong number of arguments, usage ::cmd:: %s True"%ManagementProtocol.PPRINT            
            self._pprint = ('True' == cmdargs[0].capitalize())

            
    def analyzeMessage(self, message):
        info = LogObject(None)
        try:
            info = LogObject(message)
        except Exception, ex:
            print ex
            info.message = '<INVALID LOG RECORD>'
            return info
                
        for label in info.tags.split():
            tagwithvalue = label.split(':')
            if len(tagwithvalue) > 1:
                info.tagsDict[tagwithvalue[0]] = tagwithvalue[1]
                info.tagswithvalues.append(':'.join(tagwithvalue))
            else:
                info.labels.extend(tagwithvalue) #simple label
            
        info.isevent = info.type == int(LogType.EVENT)
        now = time.time()
        self._foundTags.update(info.tagsDict)
        self._tagLastSeenAt.update(zip(info.tagswithvalues, itertools.repeat(now, len(info.tagswithvalues))))
        self._foundLabels.union(info.labels)
        self._labelLastSeenAt.update(zip(info.labels, itertools.repeat(now, len(info.labels))))
        appname = info.source
        self._foundApplications.add(appname)
        self._applicationLastSeenAt.update(((appname, now),))
        return info
        
        
    def getLevel(self, message):          
        fields = message.split('|')        

    
    def printMessage(self, message, prettyPrint=True):
        if message.startswith(ManagementProtocol.CMD_TOKEN):
            self.processCommandMessage(message)
            return

        info = self.analyzeMessage(message)
        
        if info.isevent and not self._enableEvents:
            return
        
        if not (self._minLevel <= info.level <= self._maxLevel):
            return        

        if self._includedApps and not self._includedApps.intersection((info.source,)):
            return
        
        #if exclusion filters are active, and the message is tagged by one of them, it's ignored
        if self._excludedTags and info.tagswithvalues and set(info.tagswithvalues).intersection(set(self._excludedTags)):
            return
        
        #if inclusion filters are active and the message is not tagged by any of them, it's ignored
        if self._includedTags and info.tagswithvalues and not set(info.tagswithvalues).intersection(set(self._includedTags)):
            return
        
        if prettyPrint:
            message = str(info)
            
        wholeMsg = message
        finalFormattedOut = ''
        for message in wholeMsg.split('\n'):    
            formattedOut = screenline = message[:self._screenWidth]
            message = message[self._screenWidth:]
            tabLength = len(pprint.pformat('\t'))
            tabLength = tabLength if tabLength < self._screenWidth else 0
            indent = ' ' * tabLength  
            extraLinesLength = self._screenWidth - tabLength
            
            screenline = message[:extraLinesLength]
            message = message[extraLinesLength:]
            while screenline:            
                formattedOut = '%s\n%s%s'%(formattedOut, indent, screenline)
                screenline = message[:extraLinesLength]
                message = message[extraLinesLength:]
            finalFormattedOut += "%s\n" % formattedOut 
              

        print finalFormattedOut[:-1]
        
        
class LogConsoleRequestHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        print "Connected from ", self.client_address
        recievedData = ''
        while True:
            recievedData = '%s%s'%(recievedData, self.request.recv(self.logconsole.RECIEVING_BUFFER_SIZE))
            if not recievedData:
                print 'Lost connection from ', self.client_address
                break
            else:
                recievedData = self.logconsole.proccessData(recievedData)
        self.request.close()
        
class LogConsoleServer(BaseLogConsole):
    """
    socket server which shows logs & events to screen
    """
    
    #spec see http://bitbucket.org/despiegk/ssospecs/src/27f4782d7135/1.1/concepts/EventManagement/4.%20pylabsLogConsole.wiki
    
    def __init__(self,  ip='localhost', port=DEFAULT_PORT):
        LogConsoleRequestHandler.logconsole = self
        BaseLogConsole.__init__(self, ip, port)

        
    def start(self):
        """
        start the server and list on default port
        """
        if self.started:
            return
        SocketServer.ThreadingTCPServer.allow_reuse_address = True
        self.server = SocketServer.ThreadingTCPServer((self.ip, self.port), LogConsoleRequestHandler)
        self.started = True
        self.server.serve_forever()
        
    def stop(self):
        self.server.server_close() 
        self.started = False  
        