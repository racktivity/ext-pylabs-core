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
import os
import re
import time
import signal
if pylabs.q.platform.isWindows():
    import win32process

class PMApp(object):
    name = None##string
    state = None ##PMAppType
    starttime = None ##epoch
    processid = 0 ##int
    processname = None ##string
    
        
    def kill(self):
        """Attempts to stop a pylabs application gracefully
        
        Attempts to stop a pylabs application in a nice way, waits for two seconds.
        If the attempt fails, the application is killed the hard way.
        """
        self.shutdown()
        if self.state != PMAppType.HALTED:
            time.sleep(2)
            os.kill(self.processid, signal.SIGTERM)
        
    def shutdown(self):
        """Attempts to stop a pylabs application gracefully"""
        stopcommand = os.path.join(pylabs.q.dirs.baseDir,'control',self.name,'stop.')
        if pylabs.q.platform.isUnix():
            stopcommand+='py'
        elif pylabs.q.platform.isWindows():
            stopcommand+='bat'
        pylabs.q.system.process.execute(stopcommand)
    
    def _get_state(self):
        '''Retrieves the status of a pylabs application'''
        if pylabs.q.platform.isUnix():
            if pylabs.q.system.fs.exists(os.path.join(os.sep,'proc','%d' % (self.processid))):
                return PMAppType.RUNNING
            else:
                return PMAppType.HALTED
        elif pylabs.q.platform.isWindows():
            if self.processid in win32process.EnumProcesses():
                return PMAppType.RUNNING
            else:
                return PMAppType.HALTED
                 
            
    
    state = property(fget=_get_state)

class PMAppType:
    HALTED = 1
    RUNNING = 2