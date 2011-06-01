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

from pylabs.cmdb.cmdb import MAX_LOCK_TIMEOUT, DEFAULT_LOCK_TIMEOUT, DEFAULT_WAIT_TIMEOUT
from ManagementConfiguration import ManagementConfiguration

try:
    import cPickle as pickle
except ImportError:
    import pickle

class ManagementApplication(ManagementConfiguration):
    """
    Management base class for a server or an application
    
    This class is the bridge between the application's configuration stored in the cmdb and the management
    and configuration off the application on the system.
    
    The management class applies the configuration stored in the cmdb to the system and controls the application
    on the system using e.g. cmdtools
    """
    
    #status = pylabs.q.basetype.enumeration()
    
    def __init__(self):
        ManagementConfiguration.__init__(self)
        self.getStatus()
    
    def getStatus(self):
        """
        check system what current status of application is
        """
        pass
    
    def start(self):
        """
        If status is RUNNING or STARTING, return.
        
        @TODO: TBD implicitly call applyconfig ????
        Call applyConfig
        Start the server
        """
        raise NotImplementedError("%s.start()" % self.cmdb.cmdbtypename)

    def stop(self):
        """
        If status is STOPPING or STOPPED, return.
        Stop the server
        """
        raise NotImplementedError("%s.stop()" % self.cmdb.cmdbtypename)

    def restart(self):
        # Need base implementation here, just call self.stop() and self.start()
        """
        Restart the server
        """
        raise NotImplementedError("%s.restart()" % self.cmdb.cmdbtypename)


class CMDBLockMixin:

    def startChanges(self, locktimeout=None, waittimeout=DEFAULT_WAIT_TIMEOUT):
        '''
        Locks the CMDB object so it can be changed. When calling this method,
        the CMDB attribute is updated from the database and holds the latest
        configuration data.

        @param locktimeout: Lifetime of the lock in seconds
        @type locktimeout: number
        @param waittimeout: Maximum time to wait before the lock can be acquired
        @type waittimeout: number
        '''

        if locktimeout is None:
            if pylabs.q.qshellconfig.interactive:
                locktimeout = MAX_LOCK_TIMEOUT
            else:
                locktimeout = DEFAULT_LOCK_TIMEOUT

        self.reloadCMDB(True, locktimeout, waittimeout)

    def reloadCMDB(self, lock=False, locktimeout=None, waittimeout=DEFAULT_WAIT_TIMEOUT):
        if not pylabs.q.cmdb.existsObject(self.cmdb.cmdbtypename):
            # The SAL CMDB object wasn't created yet, save it
            self.cmdb.save()
        if lock:
            self.cmdb = pylabs.q.cmdb.getObjectWithLock(self.cmdb.cmdbtypename, locktimeout, waittimeout)
        else:
            self.cmdb = pylabs.q.cmdb.getObject(self.cmdb.cmdbtypename)
