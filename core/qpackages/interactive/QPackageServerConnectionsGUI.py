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

from pymonkey import q

class QPackageServerConnectionsGUI(object):
    """
    Interactive Management of QPackage Server Connections
    mapped on i.qpackageServerConnections
    """
    def add(self, connectionName="", host="", port="", login=None, passwd=None, connect=None):
        """
        Add QPackage server connection
        @param connectionName:          Name for the new QPackage server connection.
        @param host:                    Host of the qpackage server.
        @param port:                    Port on which to connect to the server.
        @param domains:                 List of domains to use from the server.
        @param login:                   Login for the server.
        @param passwd:                  Password for the server.
        @param connect:                 If true will connect to the QPackage server
        """
        if not connectionName or not host or not port:
            q.console.echo('******************************')
            q.console.echo('Please provide the following:')
            q.console.echo('******************************')
        if not connectionName:
            connectionName = q.console.askString('Name of the new connection')
            connectionName = self._checkConnectionName(connectionName)
        if not host:
            host = q.console.askString('Host name (or ipaddress) of the new connection')
        if not port:
            port = q.console.askString('Port on which the new connection is running', defaultparam='8088')
        q.console.echo('*************************')
        q.console.echo('    Login Information    ')
        q.console.echo('*************************')
        if not login:
            login = q.console.askString('Username on this connection', defaultparam='guest')
            if login == 'guest':
                passwd='guest'
        if not passwd:
            passwd = q.console.askString('Password on this connection')
        domains = list()
        q.qpackages.qpackageServerConnections.qpackageServerConnectionAdd(connectionName, host, port, domains, login, passwd)
        if connect is None:
            connect = q.console.askYesNo('Connect to the new connection')
        if connect:
            self.connect(connectionName)

    def remove(self, connectionName=""):
        """
        Remove a QPackage server connection
        @param connectionName: Name for the QPackage server connection to delete
        """
        if not connectionName:
            config=q.qshellconfig.qpackageserverlist
            connectionName=config.chooseSectionInteractive("QPackage Server Repositories") 
            connectionName = self._checkConnectionName(connectionName)

        q.qpackages.qpackageServerConnections.qpackageServerConnectionRemove(connectionName)
    
    def list(self):
        """
        List all configured connections
        """
        return q.qpackages.qpackageServerConnections.listServerConnections()

    def review(self,connectionName=""):
        """
        Review a QPackage server connection configuration
        @param connectionName: name of the QPackage server connection to review
        """
        config=q.qshellconfig.qpackageserverlist
        if not connectionName:
            config=q.qshellconfig.qpackageserverlist
            connectionName=config.chooseSectionInteractive("QPackage Server Repository")
        login = q.qpackages.qpackageServerConnections[connectionName].login
        password = q.qpackages.qpackageServerConnections[connectionName].password
        host = q.qpackages.qpackageServerConnections[connectionName].host
        port = q.qpackages.qpackageServerConnections[connectionName].port
        self._checkQPackageServerConfigured(connectionName)
        config.validateSectionInteractive(connectionName)
        serverConnection = q.qpackages.qpackageServerConnections.getServerConnectionObject(connectionName)
        if not str(serverConnection.login) == str(login) \
           or not str(serverConnection.password) == str(password)\
           or not str(serverConnection.port) == str(port)\
           or not str(serverConnection.host) == str(host):

            serverConnection.disconnect()
            serverConnection.connect()

    def connect(self, connectionName=""):
        """
        Connect to a QPackage Server
        @param connectionName: name of the QPackage server connection to connect to
        """
        if not connectionName:
            config=q.qshellconfig.qpackageserverlist
            connectionName=config.chooseSectionInteractive("QPackage Server Repository")

        serverConnection = q.qpackages.qpackageServerConnections.getServerConnectionObject(connectionName)

        serverConnection.connect()

        if not serverConnection.domains:
            domainsList = serverConnection.getDomainsServed()
            if domainsList:
                q.console.echo('Domains serverd by this connection:')
                domainsToAdd = q.console.askChoiceMultiple(domainsList)
        
                q.qpackages.qpackageServerConnections.qpackageServerConnectionSetDomains(connectionName, domainsToAdd)

        setattr(self, str(serverConnection), serverConnection)
        serverConnection.getVLists(serverConnection.domains)
        q.qpackages.vlists.loadVLists()

    def disconnect(self,connectionName=""):
        """
        Disconnect from a QPackage Server
        @param connectionName: name of the QPackage server connection to disconnect from
        """
        if not connectionName:
            config=q.qshellconfig.qpackageserverlist
            connectionName=config.chooseSectionInteractive("QPackage Server Repository")

        serverConnection = q.qpackages.qpackageServerConnections.getServerConnectionObject(connectionName)

        if serverConnection.isConnected():
            serverConnection.disconnect()

        if hasattr(self, str(serverConnection)):
            delattr(self, str(serverConnection))

    def addDomain(self, connectionName="", domain=""):
        """
        Add a domain to a server connection
        @param connectionName: name of the QPackage server connection
        @param domain: name of the domain to add
        """
        if not connectionName:
            config=q.qshellconfig.qpackageserverlist
            connectionName=config.chooseSectionInteractive("QPackage Server Repository")

        serverConnection = q.qpackages.qpackageServerConnections.getServerConnectionObject(connectionName)
        serverConnection.connect()
        if not domain:
            q.console.echo("Please select a domain to add:")
            domainsList = list(set(serverConnection.getDomainsServed()).difference(set(serverConnection.domains)))
            if domainsList:
                domain = q.console.askChoice(domainsList)
            else:
                q.console.echo("All domains served are already added")

        serverConnection.domains.append(domain)
        q.qpackages.qpackageServerConnections.qpackageServerConnectionSetDomains(connectionName, serverConnection.domains)
        serverConnection.getVLists([domain])
        q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.packageDir, str(domain)))

    def removeDomain(self, connectionName="", domain=""):
        """
        Remove a domain from a server connection
        @param connectionName: name of the QPackage server connection
        @param domain: name of the domain to remove
        """
        if not connectionName:
            config=q.qshellconfig.qpackageserverlist
            connectionName=config.chooseSectionInteractive("QPackage Server Repository")
        serverConnection = q.qpackages.qpackageServerConnections.getServerConnectionObject(connectionName)
        if not domain:
            q.console.echo('Please select a domain to remove:')
            domain = q.console.askChoice(serverConnection.domains)
        serverConnection.domains.remove(domain)
        serverConnection.removeVlists([domain])
        q.qpackages.qpackageServerConnections.qpackageServerConnectionSetDomains(connectionName, serverConnection.domains)

    def _checkConnectionName(self, connectionName):
        """
        Check connection name
        @param connectionName: name of the QPackage server connection to check
        """
        if connectionName[0].isdigit():
            connectionName = 'connection_%s'%connectionName
        if str(connectionName[0]) == '_':
            connectionName = 'connection%s'%connectionName
        if str(connectionName).find('-') != -1:
            connectionName = str(connectionName).replace('-', '')

        return connectionName

    def _checkQPackageServerConfigured(self, connectionName):
        """
        Check QPackage Server configured
        @param connectionName: name of the QPackage server connection
        """
        path=q.system.fs.joinPaths(q.dirs.cfgDir,"qpackageserverlist.cfg" )
        if not q.system.fs.exists(path):
            raise RuntimeError("Cannot find qpackageserverlist.cfg in cfg dir.")
        config=q.qshellconfig.qpackageserverlist
        if not config.cfg.checkSection(connectionName):
            raise RuntimeError("Cannot find qpackage qpackageServer connection with name %s" % connectionName)