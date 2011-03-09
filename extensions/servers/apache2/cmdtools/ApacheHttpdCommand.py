# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>
import os
from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.enumerators import AppStatusType
import time

class ApacheHttpdCommand(CommandWrapper):
    """
    A basic ApachecommandWrapper to start/stop/restart the Apache server
    """

    def _getPidFile(self):
        return q.system.fs.joinPaths(os.sep, "var", "run","apache2.pid")
        
    def _getHttpdBinary(self):
#        return q.system.fs.joinPaths(os.sep,"etc", "init.d", "apache2")
        return q.system.fs.joinPaths(os.sep,"usr",  "sbin", "apache2ctl")
#        return q.system.fs.joinPaths(os.sep,"usr",  "sbin", "apache2")
        
    def _getDefaultConfigFile(self):
        return q.system.fs.joinPaths(os.sep, "etc", "apache2", "apache2.conf")
        
    def start(self, configFile=None, timeout=30):
        """
        Start Apache Server
        @param configFile: Absolute path of Apache httpd.conf
        @type  configFile: string
        @param timeout   : Failure if Apache is not started within <timeout> seconds
        @type  timeout   : integer
        """
        if configFile == None:
            configFile = self._getDefaultConfigFile()
           
        command =  "%(HTTPDCommand)s -f '%(configFile)s' -k start" % {"HTTPDCommand":self._getHttpdBinary(), "configFile":configFile}
        exitCode, output = q.system.process.execute(command)
        
        t = timeout
        started = False
        while t>0:
            if q.system.fs.exists(self._getPidFile()):
                pid = int(q.system.fs.fileGetContents(self._getPidFile()))
                if q.system.process.isPidAlive(pid):
                    if q.system.process.checkProcess('apache2') == 0:
                        started = True
                        break
            t = t - 1
            time.sleep(1)
        if not started:
            raise RuntimeError("Apache (pidfile [%s]) could not be started in %d seconds" % (self._getPidFile(), timeout))
            
        q.console.echo("Apache started")
           
    def stop(self, configFile=None, timeout=30):
        """
        Stop Apache Server
        @param configFile: Absolute path of Apache httpd.conf
        @type  configFile: string
        @param timeout   : Failure if Apache is not stopped within <timeout> seconds
        @type  timeout   : integer
        """
        if configFile == None:
            configFile = self._getDefaultConfigFile()
            
        command =  "%(HTTPDCommand)s -f \"%(configFile)s\" -k stop" % {"HTTPDCommand":self._getHttpdBinary(), "configFile":configFile}
        exitCode, output = q.system.process.execute(command)

        t = 30
        stopped = False
        while t>0:
            if not q.system.fs.exists(self._getPidFile()):
                stopped = True
                break
            time.sleep(1)
            t = t - 1

        if not stopped:
            raise RuntimeError("Apache (pidfile [%s]) could not be stopped in %d seconds" % (self._getPidFile(), timeout))
        
        # Check if process is still running
        if not q.system.process.checkProcess("apache2"):#self._getHttpdBinary()):
            raise RuntimeError("Apache process is still running")

        q.console.echo("Apache stopped")
    
    def restart(self, configFile=None):
        """
        Restart Apache Server
        """
        if configFile == None:
            configFile = self._getDefaultConfigFile()
            
        self.stop(configFile)
        self.start(configFile)
        
    def getStatus(self, pid = None):
        """
        Check the live status of the apache server
        """
        
        if pid == None:
            pid = self.getPidfile()
            
        if pid != None and q.system.process.isPidAlive(pid) == True and q.system.process.checkProcessForPid(int(pid), "apache2") == 0:
            return AppStatusType.RUNNING
            
        return AppStatusType.HALTED
    
    def getPidfile(self, configFile=None):
        if configFile == None:
            configFile = self._getDefaultConfigFile()
        
        pidLocation = q.system.fs.joinPaths(os.sep, "var", "run","apache2.pid")
        pid = None
        
        if q.system.fs.isFile(pidLocation):
            pid = q.system.fs.fileGetContents(pidLocation)
            pid = str(str(pid).splitlines()[0]).strip(" ")
            pid = int(pid)
            
        return pid
            
    def init(self, configFile=None):
        """
        Initialize Apache Server on the Windows platform
        """
        if configFile == None:
            configFile = self._getDefaultConfigFile()
        
        if q.platform.isWindows():
            installServiceCommand = "%s -k install"%self._getHttpdBinary()
            q.logger.log("Executing %s on Windows"%installServiceCommand)
            exitCode, output = q.system.process.execute(installServiceCommand, dieOnNonZeroExitCode=False)