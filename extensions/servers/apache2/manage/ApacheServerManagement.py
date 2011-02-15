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
 
from pylabs import q
from pylabs.baseclasses.ManagementApplication import ManagementApplication, CMDBLockMixin
from pylabs.enumerators import AppStatusType
# Suppress warning by Cheetah about non-C NameMapper
import warnings
import urllib
warnings.simplefilter("ignore")
from ApacheServer import ApacheServer
warnings.filters.pop(0)

class ApacheServerManagement(ManagementApplication,CMDBLockMixin):
    """
    Apache Server configuration extension entry point
    """

    cmdb = ApacheServer()

    def printStatus(self):
        """
        Print the live status of the Apache Server
        """
        q.console.echo("Apache is %s"%self._getStatus())
    
    def getStatus(self):
        """
        Get the status of the Apache Server
        """
        return self._getStatus()
    
    def _getStatus(self):
        """
        check system what current status of the application is
        """
        pidLocation = q.system.fs.joinPaths(q.dirs.pidDir, "httpd.pid")
        pid = None
    
        if q.system.fs.isFile(pidLocation):
            pid = q.system.fs.fileGetContents(pidLocation)
            pid = str(str(pid).splitlines()[0]).strip(" ")
            pid = int(pid)
    
    
        if pid == None:
            return AppStatusType.HALTED
        else:
            status = q.cmdtools.apache.httpd.getStatus(pid)
            if status == AppStatusType.RUNNING and self.cmdb.virtualHosts:
                vHost = self.cmdb.virtualHosts[self.cmdb.virtualHosts.keys()[0]]
                url = urllib.urlopen('http://%s:%s/status' %(vHost.ipaddress, vHost.port))
                out = url.read()
                if out <> "RUNNING":
                    q.console.echo('Failed to retrieve http://%s:%s/status' %(vHost.ipaddress, vHost.port))
                    return AppStatusType.UNKNOWN
            return status

    def save(self):
        """
        If the configuration is dirty write it to the cmdb
        else return
        """
    
        q.console.echo("Writing changes to cmdb")
        self.cmdb.save()

    def start(self):
        """
        Starts the Apache Server based on the applied configuration
        if status is STARTED or STARTING return
        """
        if self._getStatus() == AppStatusType.RUNNING:
            q.console.echo("Apache is already running")
            return

        q.cmdtools.apache.httpd.start(self._getConfigFileName())
        
        if self._getStatus() == AppStatusType.RUNNING:
            q.console.echo('Apache started successfully')

    def stop(self):
        """
        Stops the Apache Server
        if status is STOPPED or STOPPING return
        """
        if self._getStatus() != AppStatusType.RUNNING:
            q.console.echo("Apache is not running")
            return
        
        q.cmdtools.apache.httpd.stop(self._getConfigFileName())
        
        if self._getStatus() == AppStatusType.HALTED:
            q.console.echo('Apache stopped successfully')

    def restart(self):
        """
        Restart the Apache Server
        """
        q.cmdtools.apache.httpd.restart(self._getConfigFileName())
        
        if self._getStatus() == AppStatusType.RUNNING:
            q.console.echo('Apache restarted successfully')

    def applyConfig(self, restart=True):
        """
        Generates the site configuration file and restarts the apache server

        This will clean out some config directories!
        """ 
        self.cmdb.pm_write()

        if not self.cmdb.initDone:
            if q.platform.isWindows():
                q.cmdtools.apache.httpd.init(self._getConfigFileName())

            self.startChanges()
            self.cmdb.initDone = True
            self.cmdb.save()

        if restart:
            self.restart()

    def listSiteNames(self):
        """
        List site names

        @return: list of sitenames
        @rtype: list of strings
        """
        siteNames = []
        for vhost in self.cmdb.virtualHosts.values():
            for siteName in vhost.sites:
                siteNames.append(siteName)

        return siteNames

    def _getConfigFileName(self):
        return q.system.fs.joinPaths(self.cmdb._configSubDir, self.cmdb.configFileName)