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

class ManagementConfiguration(object):
    """
    This class is a base class for managin configuration stored in the cmdb.
    
    It is a bridge between configuration (= cmdb) and the system that uses the configuration
    """
    
    def init(self, configdir=""):
        """
        If cmdb._initDone Then return
        Do global initialization of this vapp - Setup paths, permissions, user account, ...
        Set  self.cmdb.initDone := True
        self.save()
        """
        raise NotImplementedError("%s.init()" % self.cmdb.cmdbtypename)

    def save(self):
        """
        If configuration not dirty (i.e. configuration is in sync with cmdb), then
        return. Otherwise save the configuration in the cmdb and clear the dirty flag
        """
        raise NotImplementedError("%s.save()" % self.cmdb.cmdbtypename)

    def applyConfig(self):
        """
        Call self.init
        Call self.save()
        Apply the configuration to the server
          - The status must be identical before and after the applyConfig command
              (a RUNNING server is again RUNNING, a STOPPED server is again STOPPED)
          - Ideally, a RUNNING server can be runtime reconfigured
          - for some servers a stop - modify config - start must be implemented
        """
        raise NotImplementedError("%s.applyConfig()" % self.cmdb.cmdbtypename)

    def exportConfig(self, version=None):
        """
        If config is dirty and version is None, throw error and tell user to save his config first.
        Export configuration of this server to a string which is returned.
        If version is None, export latest.
        If version is not None, take that config version from cmdb
        """
        # TODO: must implement this generically at this level
        raise NotImplementedError("%s.exportConfig()" % self.cmdb.cmdbtypename)

    def importConfig(self, configstring):
        """
        previousinitdone = self._initdone
        Import configuration from configstring.
        self._initdone = previousinitdone
        self.save()
        """ 
        # TODO: must implement this generically at this level
        raise NotImplementedError("%s.importConfig()" % self.cmdb.cmdbtypename)

    def listConfigs(self):
        # TODO implement as a generator, going from last config version to first config version
        """
        List all known configurations of this server, latest config first.
        """
        pass

    def printConfig(self):
        """
        Show userfriendly textual version of configuration
        """
        raise NotImplementedError("%s.printConfig()" % self.cmdb.cmdbtypename)

    def __str__(self):
        return str(self.cmdb)
            
    def __repr__(self):
        return self.__str__()