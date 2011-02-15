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

import pylabs
import sys, os, atexit, types

from pylabs.enumerators import AppStatusType

#@todo Need much more protection: cannot change much of the state (e.g. dirs) once the app is running!
#@todo Need to think through - when do we update the qpidfile (e.g. only when app is started ?)
#@todo can we make this a singleton? Then need to change __init__ to avoid clearing the content
#@todo need to implement QApplication.getVar()

class Application:

    def __init__(self):
        self.state = AppStatusType.UNKNOWN
        #self.state = None
        self.appname = 'starting'
        self.agentid= "starting"
        self._calledexit=False


    def start(self):
        '''Start the application

        You can only stop the application with return code 0 by calling
        q.Application.stop(). Don't call sys.exit yourself, don't try to run
        to end-of-script, I will find you anyway!
        '''
        if self.state == AppStatusType.RUNNING:
            raise RuntimeError("Application %s already started" % self.appname)

        # Register exit handler for sys.exit and for script termination
        atexit.register(self._exithandler)


        # Set state
        self.state = AppStatusType.RUNNING
        pylabs.q.logger.log("Application %s started" % self.appname, 8)

    def stop(self, exitcode=0):
        
        '''Stop the application cleanly using a given exitcode

        @param exitcode: Exit code to use
        @type exitcode: number
        '''
        import sys

        #@todo should we check the status (e.g. if application wasnt started, we shouldnt call this method)
        if self.state == AppStatusType.UNKNOWN:
            # Consider this a normal exit
            self.state = AppStatusType.HALTED
            pylabs.q.logger.close()
            sys.exit(exitcode)

        
        # Since we call os._exit, the exithandler of IPython is not called.
        # We need it to save command history, and to clean up temp files used by
        # IPython itself.
        pylabs.q.logger.log("Stopping Application %s" % self.appname, 8)
        try:
            __IPYTHON__.atexit_operations()
        except:
            pass

        # Write exitcode
        if self.writeExitcodeOnExit:
            exitcodefilename= pylabs.q.system.fs.joinPaths(pylabs.q.dirs.tmpDir, 'qapplication.%d.exitcode'%os.getpid())
            pylabs.q.logger.log("Writing exitcode to %s" % exitcodefilename, 5)
            pylabs.q.system.fs.writeFile(exitcodefilename, str(exitcode))

        # Closing the LogTargets
        pylabs.q.logger.close()

        # was probably done like this so we dont end up in the _exithandler
        #os._exit(exitcode) Exit to the system with status n, without calling cleanup handlers, flushing stdio buffers, etc. Availability: Unix, Windows.
        
        self._calledexit=True # exit will raise an exception, this will bring us to _exithandler
                              # to remember that this is correct behaviour we set this flag
        sys.exit(exitcode) ## ?? why previously os._exit(exitcode) ?? Caused output to dissapear!!


    def _exithandler(self):
        # Abnormal exit
        # You can only come here if an application has been started, and if
        # an abnormal exit happened, i.e. somebody called sys.exit or the end of script was reached
        # Both are wrong! One should call pylabs.q.application.stop(<exitcode>)
        #@todo can we get the line of code which called sys.exit here?
        pylabs.q.logger.log("UNCLEAN EXIT OF APPLICATION, SHOULD HAVE USED q.application.stop()", 4)
        pylabs.q.logger.close()
        if not self._calledexit:
            self.stop(1)


    def getCPUUsage(self):
        """
        try to get cpu usage, if it doesn't work will return 0
        By default 0 for windows
        """
        try:
            pid = os.getpid()
            if pylabs.q.platform.isWindows():
                return 0
            if pylabs.q.platform.isLinux():
                command = "ps -o pcpu %d | grep -E --regex=\"[0.9]\""%pid
                pylabs.q.logger.log("getCPUusage on linux with: %s" %command,8)
                exitcode,output = pylabs.q.system.process.execute(command, True, False)
                return output
            elif pylabs.q.platform.isSolaris():
                command = 'ps -efo pcpu,pid |grep %d'%pid
                pylabs.q.logger.log("getCPUusage on linux with: %s" %command,8)
                exitcode,output = pylabs.q.system.process.execute(command, True, False)
                cpuUsage = output.split(' ')[1]
                return cpuUsage
        except Exception, e:
            pass
        return 0

    def getMemoryUsage(self):
        """
        try to get memory usage, if it doesn't work will return 0i
        By default 0 for windows
        """
        try:
            pid = os.getpid()
            if pylabs.q.platform.isWindows():
                # Not supported on windows
                return "0 K"
            elif pylabs.q.platform.isLinux():
                command = "ps -o pmem %d | grep -E --regex=\"[0.9]\""%pid
                pylabs.q.logger.log("getMemoryUsage on linux with: %s" %command,8)
                exitcode,output = pylabs.q.system.process.execute(command, True, False)
                return output
            elif pylabs.q.platform.isSolaris():
                command = "ps -efo pcpu,pid |grep %d"%pid
                pylabs.q.logger.log("getMemoryUsage on linux with: %s" %command,8)
                exitcode, output = pylabs.q.system.process.execute(command, True, False)
                memUsage = output.split(' ')[1]
                return memUsage
        except Exception, e:
            pass
        return 0
    
    def _setWriteExitcodeOnExit(self, value):
        if not pylabs.q.basetype.boolean.check(value):
            raise TypeError
        pylabs.q.logger.log("Setting q.application.writeExitcodeOnExit = %s"%str(value), 5)
        exitcodefilename = pylabs.q.system.fs.joinPaths(pylabs.q.dirs.tmpDir, 'qapplication.%d.exitcode'%os.getpid())
        if value and pylabs.q.system.fs.exists(exitcodefilename):
            pylabs.q.system.fs.remove(exitcodefilename)
        self._writeExitcodeOnExit = value
        
    def _getWriteExitcodeOnExit(self):
        if not hasattr(self, '_writeExitcodeOnExit'):
            return False
        return self._writeExitcodeOnExit
        
    writeExitcodeOnExit = property(fset=_setWriteExitcodeOnExit, fget=_getWriteExitcodeOnExit, doc="Gets / sets if the exitcode has to be persisted on disk")