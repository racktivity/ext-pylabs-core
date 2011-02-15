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

import sys
import os
import time
import re

if sys.platform.startswith('linux') or sys.platform.startswith('sunos'):
    import fcntl

import pylabs

# THIS METHOD IS NOT THREADSAFE

#TODO Fixup singleton-like behaviour
class Util:

    _LOCKPATHLINUX = "/tmp/run"
    __LOCKDICTIONARY = {}

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self._LOCKPATHWIN = os.getcwd()+os.sep+'tmp'+os.sep+'run'+os.sep

    def cleanupString(self, string, replacewith="_", regex="([^A-Za-z0-9])"):
        # Please don't use the logging system here. The logging system
        # needs this method, using the logging system here would
        # introduce a circular dependency. Be careful not to call other
        # functions that use the logging system.

        """ remove all non numeric or alphanumeric characters """
        return re.sub(regex, replacewith, string)

    def lock(self, lockname, locktimeout=60):
        """ Take a system-wide interprocess exclusive lock. Default timeout is 60 seconds """

        if locktimeout < 0:
            raise RuntimeError("Cannot take lock [%s] with negative timeout [%d]" % (lockname, locktimeout))

        if pylabs.q.platform.isUnix():
            # linux implementation
            lockfile = self._LOCKPATHLINUX + os.sep + self.cleanupString(lockname)
            pylabs.q.system.fs.createDir(Util._LOCKPATHLINUX)
            pylabs.q.system.fs.createEmptyFile(lockfile)

            # Do the locking
            lockAcquired = False
            for i in range(locktimeout+1):
                try:
                    myfile = open(lockfile, "r+")
                    fcntl.flock(myfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lockAcquired = True
                    self.__LOCKDICTIONARY[lockname] = myfile
                    break
                except IOError:
                    # Did not get the lock :( Sleep 1 second and then retry
                    time.sleep(1)
            if not lockAcquired:
                myfile.close()
                raise RuntimeError("Cannot acquire lock [%s]" % (lockname))

        elif pylabs.q.platform.isWindows():
            raise NotImplementedError

    def unlock(self, lockname):
        """ Unlock system-wide interprocess lock """
        if pylabs.q.platform.isUnix():
            try:
                myfile = self.__LOCKDICTIONARY.pop(lockname)
                fcntl.flock(myfile.fileno(), fcntl.LOCK_UN)
                myfile.close()
            except Exception, exc:
                raise RuntimeError("Cannot unlock [%s] with ERROR:%s" % (lockname, str(exc)))

        elif pylabs.q.platform.isWindows():
            raise NotImplementedError