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
 
import re
import sys

import pymonkey
from pymonkey import q
from pymonkey.baseclasses.CMDBServerObject import CMDBServerObject

# Make sure we find the server
sys.path.insert(0, q.system.fs.joinPaths(q.dirs.appDir, "applicationserver",
                                         'lib'))
from applicationserver.pymonkey_bindings import Server, SubscriberException
from applicationserver import pymonkey_bindings, CRON_JOB_STOP

# Defines
SERVERNAME_REGEX = re.compile('^[a-z_]+$')
APPLICATIONSERVER_CONFIGDIR = q.system.fs.joinPaths(q.dirs.cfgDir, 'applicationserver')

class PortNotUnique(Exception):
    """
    Raised when two or more servers are enabled and have the same XMLRPC port.
    """
    def __init__(self):
        super(Exception, self).__init__("Multiple servers with the same XMLRPC port are enabled")

class ApplicationserverDict(dict):
    """Dict that checks it keys for uniqueness and with a regex before setting"""
    def __init__(self, key_regex, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.key_regex = key_regex

    def __setitem__(self, key, value):
        # Check key first
        self.check(key)
        # Proceed
        dict.__setitem__(self, key, value)

    def check(self, key):
        # Should raise exception if something is wrong
        def value_error(message):
            q.logger.log(message, 2)
            raise ValueError(message)
        # Check if server exists
        if key in self:
            value_error("Server name already exists")
        # Check if the server name is valid
        elif not self.key_regex.match(key):
            value_error("Server name not valid, only lower case letters and "
                        "underscores are allowed.")
        return True

class ApplicationserverCmdb(CMDBServerObject):
    cmdbtypename ='applicationserver'
    name = 'Applicationserver'

    def __str__(self):
        return self.cmdbtypename

Applicationserver = pymonkey_bindings.Server

ApplicationserverConfig = pymonkey_bindings.ApplicationserverConfigManagement
