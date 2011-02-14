DEFAULT_PORT = 9998
import time
import itertools
from collections import defaultdict
import signal
import sys
import socket
import SocketServer
from pymonkey import q

from logtargets.LogTargetToPylabsLogConsole import LogTargetToPylabsLogConsole
from LogConsoleServer import LogConsoleServer, ManagementProtocol

from pymonkey.Shell import *

class LogConsoleController(object):
    """
    controle the LogConsoleServer
    bound on ...
    """
    
    #spec see http://bitbucket.org/despiegk/ssospecs/src/27f4782d7135/1.1/concepts/EventManagement/4.%20pylabsLogConsole.wiki
    
    def __init__(self, serverip="localhost", serverport=DEFAULT_PORT):
        self.connected = False
        self._serverip = serverip
        # Luckily gethostbyname returns the IP if an IP is given
        self._serverport = serverport
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._logConsole = None            

    def _disconnect(self):
        self._sock.close()

    def _connect(self):
        if self.connected==False:
            self._server_real_ip = socket.gethostbyname(self._serverip)
            self._sock.connect((self._server_real_ip, self._serverport))
            self.connected = True
            return self.connected

    def _send(self, data):
        if not self.connected:
            if not self._connect():
                return#message lost
        try:                
            self._sock.sendall(data)
        except:
            # reconnect , otherwise connected = false
            if not self._connect():
                self.connected = False
            else:
                self._sock.sendall(data)
                    

    def _findConsoleTarget(self, consoleTarget):
        try:
            idx = q.logger.logTargets.index(consoleTarget)
            return q.logger.logTargets[idx]
        except ValueError:
            return None
        
        
    def start(self, ip='localhost', port=DEFAULT_PORT):
        if not self._logConsole:
            self._logConsole = LogConsoleServer(ip, port)
        if self._logConsole.started:
            return
        try:
            self._logConsole.start()
        except KeyboardInterrupt:
            print "Interrupted by user"
            self._logConsole.stop()
        
        
    def activate(self, serverip="localhost", serverport=DEFAULT_PORT):
        newConsoleTarget = LogTargetToPylabsLogConsole(serverip, serverport)
        if not self._findConsoleTarget(newConsoleTarget):
            q.logger.addLogTarget(newConsoleTarget)
        raise RuntimeError('oppaaa:colon in the message|anotherfield in the message\nand a new line', typeid='9002', tags='opatag:opatag')
    
    def deactivate(self, serverip="localhost", serverport=DEFAULT_PORT):
        #NOTE: we have overriden __eq__ in LogTargetToPylabsLogConsole class, otherwise the following logic won't work
        templateTarget = LogTargetToPylabsLogConsole(serverip, serverport)
        if self._findConsoleTarget(templateTarget):
            q.logger.logTargets.remove(templateTarget)
        
    def log(self, message):
        self._send('1|%s|%s|5||%s'%(time.time(), q.application.appname, message) + ManagementProtocol.MSG_TERMINATOR)

            
    def _sendCommand(self, command, params=None):
        self._connect()
        paramString = ''
        if params:
            for param in params:
                paramString = '%s %s' % (paramString, param)
        command = '%s %s%s%s' % (ManagementProtocol.CMD_TOKEN, command, paramString, ManagementProtocol.MSG_TERMINATOR)
        self._send(command) 

    def showSourceApplications(self, sinceXNrMinutes=0):
        """
        show list of all applications found so far in active logserver session
        allow selection of apps        
        """
        self._sendCommand(ManagementProtocol.SHOW_SOURCE_APPLICATIONS, (sinceXNrMinutes,))

        
    def filterSourceApplications(self, apps=None):
        """
        filter on specified apps
        """
        if apps is None:
            apps = tuple()
        self._sendCommand(ManagementProtocol.FILTER_SOURCE_APPLICATIONS, '%s'%str(apps).replace(' ', ''))

    def setMinLevel(self, minLevel):
        """
        set min visible verbosity level
        
        @param minLevel: min verbosity level to show
        @type minLevel: int 
        """
        self._sendCommand(ManagementProtocol.SET_MIN_LEVEL, (minLevel,))

                    
    def setMaxLevel(self, maxLevel):
        """
        set max visible verbosity level
        
        @param maxLevel: max verbosity level to show
        @type maxLevel: int 
        
        """
        self._sendCommand(ManagementProtocol.SET_MAX_LEVEL, (maxLevel,))
        
    def setScreenWidth(self, screenWidth):
        """
        set Console screen width
        
        @param screenWidth: Console screen width
        @type screenWidth: int 
        
        """
        self._sendCommand(ManagementProtocol.SET_SCREEN_WIDTH, (screenWidth,))        
    
    
    def disableEvents(self):
        """
        don't show events
        """
        self._sendCommand(ManagementProtocol.ENABLE_EVENTS, (False,))
        

    def enableEvents(self):
        """
        show events
        """
        self._sendCommand(ManagementProtocol.ENABLE_EVENTS, (True,))


    def filterOnTags(self, includes=None, excludes=None):
        """
        filter on tags pass in the form of array of strings to filter for e.g. customer:* customer customer:kri* customer:kristof        
        """
        if includes is None:
            includes = tuple()
        if excludes is None:
            excludes = tuple()
        self._sendCommand(ManagementProtocol.FILTER_ON_TAGS, '%s,%s' % (str(includes).replace(' ', ''), str(excludes).replace(' ', '')))

        
    def showFoundTags(self, sinceXNrMinutes=0):
        """
        show list of all tags found so far in active logserver session
        """
        self._sendCommand(ManagementProtocol.SHOW_FOUND_TAGS, (sinceXNrMinutes,))
            
    def enablePrettyPrint(self):
        """
        enables console pretty printing
        """
        self._sendCommand(ManagementProtocol.PPRINT, (True,))
    
    def disablePrettyPrint(self):
        """
        disables console pretty printing
        """
        self._sendCommand(ManagementProtocol.PPRINT, (False,))    
    
