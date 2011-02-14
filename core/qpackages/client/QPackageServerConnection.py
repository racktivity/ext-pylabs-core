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

import time

from pymonkey import q
from pymonkey.baseclasses import BaseType
from pymonkey.enumerators import PlatformType
from pymonkey.qpackages.client.QPackageClient import QPackageClient
from pymonkey.qpackages.common.QPackageObject import QPackageObject
from pymonkey.qpackages.client.QPackageUtils import QPackageUtils
import os

class QPackageServerConnections(BaseType):
    """
    Wrapper class for a list of QPackageServerConnection objects.
    This class contains logic to populate itself based on the
    qpackageserverlist.cfg file
    """

    pm_QPackageServerConnections = q.basetype.dictionary(doc="Internal list of known repositories", allow_none=True, default=dict())

    def __init__(self):
        """
        Initialize the list, read from config file
        """
        self.pm_LoadServerConnections()
        pass

    def qpackageServerConnectionAdd(self, connectionName, host, port=None, domains=None, login=None, password=None):
        """
        Configures a new qpackage server connection and stores the configuration.

        @param connectionName:    Name for the new connection.
        @param host:                    Host of the qpackage server.
        @param port:                    Port on which to connect to the server.
        @param domains:                 List of domains to use from the server.
        @param login:                   Login for the server.
        @param password:                Password for the server.
        """

        # Make sure the config file exists and is loaded
        q.qshellconfig.loadConfigFile('qpackageserverlist')

        # Check if connection does not exits already
        for connection in self.pm_QPackageServerConnections.itervalues():
            if connection.name == connectionName or connection.host == host:
                raise ValueError('Connection already exists!')

        q.qshellconfig.qpackageserverlist.setParam(connectionName, 'ipaddr', host)

        if login:
            q.qshellconfig.qpackageserverlist.setParam(connectionName, 'login', login)
        if password:
            q.qshellconfig.qpackageserverlist.setParam(connectionName, 'password', password )
        if port:
            q.qshellconfig.qpackageserverlist.setParam(connectionName, 'port', port)

        self.qpackageServerConnectionSetDomains(connectionName, domains)
        # Refresh configuration
        q.qshellconfig.refresh()
        self.refresh()

    def qpackageServerConnectionSetDomains(self, connectionName, domains):
        """
        Add domains to a QPackage Server connection
        @param connectionName:  Name of the connection to add domains to.
        @param domains: domains to add to the connection. (list or comma separated string)
        """
        if not connectionName in q.qshellconfig.qpackageserverlist.getSections():
            raise ValueError('Connection does not exists!')

        if not domains:
            q.qshellconfig.qpackageserverlist.setParam(connectionName, 'domains', '*NONE*')
        else:
            if isinstance(domains, basestring):
                domains = str(domains).split(',')
            for domain in domains:
                self._domainAlreadyExists(connectionName, domain)
            q.qshellconfig.qpackageserverlist.setParam(connectionName, 'domains', ','.join(domains))

        self.refresh()

    def _domainAlreadyExists(self, connectionName, domain):
        """
        Check if a domain served by a connection is already configured
        @param connectionName: name of the connection serving the domain to add
        @param domain: domain name to check
        """
        for connection in self.pm_QPackageServerConnections.itervalues():
            if domain in connection.domains and not connection.name == connectionName:
                raise ValueError('Domain <%s> is already configured for connection <%s>'%(domain, str(connection)))

    def qpackageServerConnectionRemove(self, connectionName):
        """
        Deletes a connection from the configured connections
        @param connectionName:  Name of the connection to remove.
        """
        q.logger.log('Removing connection %s from pymonkey.qpackageserverlist' % connectionName)

        if not connectionName in q.qshellconfig.qpackageserverlist.getSections():
            raise ValueError('Connection does not exists!')

        self.pm_QPackageServerConnections[connectionName].removeVlists()
        q.qshellconfig.qpackageserverlist.removeSection(connectionName)
        self.refresh()

    def getConnectionFromDomain(self, domain):
        ''' Get the correct connection for the domain given.

        @param domain: domain string you need the connection
        @return: QPackageServerConnection of the domain you gave
        '''
        q.logger.log('getting the connection for domain %s'%domain, 8)
        self.refresh()
        connectionForDomain = None
        for connection in self.pm_QPackageServerConnections.itervalues():
            if domain in connection.domains:
                if connectionForDomain:
                    raise RuntimeError('Found more than one configured connection serving the same domain.. Please review your connections')
                q.logger.log('found connection %s for domain %s'%(connection.name, domain), 8)
                connectionForDomain = connection
        q.logger.log('no connection found for domain %s'%(domain), 8)
        return connectionForDomain

    def getServerConnectionObject(self, connectionName):
        """
        Get QPackage server connection by name
        @param connectionName: name of the connection to retrieve
        """
        self.refresh()
        if connectionName in self.pm_QPackageServerConnections:
            return self.pm_QPackageServerConnections[connectionName]

        raise ValueError('Connection <%s> does not exist'%connectionName)

    def listServerConnections(self):
        """
        List all server connections
        """
        return self.pm_QPackageServerConnections.keys()

    def refresh(self):
        self.pm_LoadServerConnections()

    def __iter__(self):
        return self.pm_QPackageServerConnections.values().__iter__()

    def __len__(self):
        return self.pm_QPackageServerConnections.__len__()

    def __contains__(self, v):
        if isinstance(v, str):
            return v in self.pm_QPackageServerConnections.keys()
        elif isinstance(v, QPackageServerConnection):
            return v in self.pm_QPackageServerConnections.values()

    def __getitem__(self, v):
        if isinstance(v, int):
            return self.pm_QPackageServerConnections.__getitem__(self.pm_QPackageServerConnections.keys()[v])
        elif isinstance(v, str):
            return self.pm_QPackageServerConnections.__getitem__(v)

    def __str__(self):
        return self.pm_QPackageServerConnections.__str__()

    def __repr__(self):
        return self.pm_QPackageServerConnections.__repr__()

    def pm_LoadServerConnections(self):
        """
        Loads all serverconnections defined in qpackageserverlist.cfg

        @todo: test if domain not already served!
        """

        q.logger.log('Loading configured server connections', 5)

        connections = dict()

        # Make sure the config file exists and is loaded
        q.qshellconfig.loadConfigFile('qpackageserverlist')

        for connectionName in q.qshellconfig.qpackageserverlist.getSections():
            try:
                host = q.qshellconfig.qpackageserverlist.getParam(connectionName, 'ipaddr',  defaultValue=None, forceDefaultValue=False)
                login = q.qshellconfig.qpackageserverlist.getParam(connectionName, 'login',  defaultValue='*NONE*', forceDefaultValue=False)
                password = q.qshellconfig.qpackageserverlist.getParam(connectionName, 'password',  defaultValue='*NONE*', forceDefaultValue=False)
                domains = q.qshellconfig.qpackageserverlist.getParam(connectionName, 'domains',  defaultValue=None, forceDefaultValue=False)
                port = q.qshellconfig.qpackageserverlist.getParam(connectionName, 'port', defaultValue=8088, forceDefaultValue=False)

                if not connectionName in self.pm_QPackageServerConnections:
                    connection = QPackageServerConnection(connectionName, host, port=int(port))
                else:
                    connection = self.pm_QPackageServerConnections[connectionName]

                connection.domains = domains.replace(' ', '').split(',') if domains else list()
                connection.login = login if login else '*NONE*'
                connection.password = password if password else '*NONE*'

                connections[connection.name] = connection

                q.logger.log('Added connection %s' % connection.name, 5)
            except Exception, e:
                q.logger.log('Failed to add connection %s: %s' % (connectionName, e.message), 5)

        self.pm_QPackageServerConnections = connections

class QPackageServerConnection(BaseType):
    """
    ...Connection towards one of your QPackageservers
    """

    name              = q.basetype.string(doc='Name of your connection', allow_none=False)
    host              = q.basetype.string(doc='IP/dns of your qpackageserver', allow_none=False)
    port              = q.basetype.integer(doc='Port on which to connect to the server', allow_none=False, default=0)
    login             = q.basetype.string(doc='Login for your connection', allow_none=True)
    password          = q.basetype.string(doc='Password for your connection', allow_none=True)
    domains           = q.basetype.list(doc='List of domains we consume on this server', allow_none=False, default=list())
    pm_lastUpdateTime = q.basetype.integer(doc='The epoch when the VLists have been updated', allow_none=False, default=0)
    pm_client         = q.basetype.object(QPackageClient, doc='Actual QPackage server client', allow_none=True, default=None)
    pm_sessionId      = q.basetype.guid(doc='The connection\'s unique session id', default=None,allow_none=True)

    def __init__(self, connectionName, host, port=None, login=None, password=None):
        """
        @param connectionName: Name of your connection
        @param host:           IP/dns of your qpackageserver

        optional
        @param port:           Port on which to connect to the server.
        @param login:          Username for your connection.
        @param password:       Password for your connection.
        """
        self.name = connectionName
        self.host = host
        self.port = port
        self.login= login
        self.password = password

    def connect(self):
        ''' Initialize the connection to the server, this means that we fetch a session id'''
        q.logger.log('connect to the QPackageServer %s'%self.name, 8)
        self.pm_client = QPackageClient(self.host, self.port)
        self.pm_sessionId = self.pm_client.connect(self.login, self.password)
        if not self.isConnected():
            raise RuntimeError('cannot connect to QPackageServer %s'%self.name)

        self.getVLists(self.domains)
        q.logger.log('connected to the QPackageServer %s, got session id %s'%(self.name, self.pm_sessionId), 8)

    def disconnect(self):
        ''' Disconnect from the server, and remove the session id '''
        q.logger.log('disconnect from QPackageServer %s'%self.name, 8)
        if not self.pm_client or not self.pm_sessionId:
            return
        self.pm_client.disconnect(self.pm_sessionId)
        self.pm_sessionId = None
        q.logger.log('disconnect from QPackageServer %s'%self.name, 8)

    def isConnected(self):
        ''' Returns True when the sessionId is available otherwise returns False '''
        q.logger.log('check if connected to QPackageServer %s'%self.name, 8)
        if not self.pm_client or not self.pm_sessionId:
            return False
        if self.pm_client.isConnected(self.pm_sessionId):
            q.logger.log('connected to QPackageServer %s'%self.name, 8)
            return True
        q.logger.log('not connected to QPackageServer %s'%self.name, 8)
        return False

    def getDomainsServed(self):
        """
        Retrieving list of domains served by QPackage Server
        """
        q.logger.log('Retrieving list of domains served by QPackage Server', 8)
        if not self.isConnected():
            raise RuntimeError('Please connect first to QPackage Server')
        domainsList = self.pm_client.getDomainsServed(self.pm_sessionId)
        return domainsList

    def downloadSynced(self, domain, name, version, qualityLevel):
        ''' Close the downloadsession after the download

        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        '''
        q.logger.log('asking the server to close the download session for QPackage %s in domain %s'%(name, str(domain)),8)
        self.pm_client.downloadSynced(self.pm_sessionId, domain, name, version, qualityLevel)
        q.logger.log('asked the server to close the download session for QPackage %s in domain %s'%(name, str(domain)),8)

    def createNew(self, domain, name, version, qualityLevel='trunk', download=True):
        ''' Create a new QPackage on the server
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: quality level of the QPackage
        @param download: if True will download qpackage from server
        '''
        q.logger.log('asking the server to create QPackage %s on domain %s with session %s'%(name, domain, self.pm_sessionId), 8)
        retval =  self.pm_client.createNewQPackage(self.pm_sessionId, domain, name, version, qualityLevel)
        q.logger.log('create QPackage returns %s'%retval, 8)
        if retval:
            q.logger.log('created QPackage %s for domain %s on the server'%(name, domain), 8)
            if download:
                qpackage = QPackageObject(domain, name, version, new=True)
                self._download(qpackage, qualityLevel, downloadAllFiles=True, module='write')
                qpackagePath = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath())
                if q.system.fs.exists(q.system.fs.joinPaths(qpackagePath, 'download')):
                    q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackagePath, 'download'), q.system.fs.joinPaths(qpackagePath, 'upload_%s'%qualityLevel))
                    QPackageUtils.removeDir(q.system.fs.joinPaths(qpackagePath, 'download'))
                else:
                    q.system.fs.createDir(q.system.fs.joinPaths(qpackagePath, 'upload_%s'%qualityLevel))
        else:
            raise RuntimeError('could not create QPackage %s on domain %s'%(name, domain))
        return True

    def createNewVersion(self, domain, name, version, qualityLevel='trunk', download=True, copyDependencies=True,\
                             copySupportedPlatforms=True, copyDescription=True, copyTags=True, copyFiles=True):
        ''' Create a new QPackage version on the server
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param download: if True will download qpackage from server
        @param copyDependencies       :copy the dependencies of the QPackage
        @param copySupportedPlatforms :copy the supported platforms of the QPackage
        @param copyDescription        :copy description of the QPackage
        @param copyTags               :copy tags of the QPackage
        @param copyFiles              :copy files of the QPackage
        '''
        q.logger.log('asking the server to create QPackage version %s on domain %s'%(name, domain), 8)
        retval =  self.pm_client.createNewQPackageVersion(self.pm_sessionId, domain, name, version, qualityLevel, copyDependencies,\
                             copySupportedPlatforms, copyDescription, copyTags, copyFiles)
        q.logger.log('create QPackage version returns %s'%retval, 8)
        if retval:
            q.logger.log('created QPackage %s with version %s for domain %s on the server'%(name, version, domain), 8)
            if download:
                qpackage = QPackageObject(domain, name, version, new=True)
                self._download(qpackage, qualityLevel, downloadAllFiles=True, module='write')
                qpackagePath = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath())
                if q.system.fs.exists(q.system.fs.joinPaths(qpackagePath, 'download')):
                    q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackagePath, 'download'), q.system.fs.joinPaths(qpackagePath, 'upload_%s'%qualityLevel))
                    QPackageUtils.removeDir(q.system.fs.joinPaths(qpackagePath, 'download'))
                else:
                    q.system.fs.createDir(q.system.fs.joinPaths(qpackagePath, 'upload_%s'%qualityLevel))
        else:
            raise RuntimeError('could not create QPackage %s with version %s on domain %s'%(name, version, domain))
        return True

    def promoteQPackageToMasterRepo(self, domain, name, version, qualityLevel, domainLogin, domainPasswd):
        """
        Promote QPackage tp master repo
        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel
        @param domainLogin:    The user's login for the given domain
        @param domainPasswd: The user's password for the given domain
        """
        q.logger.log('Calling the server to promote QPackage %s to master repo'%name, 6)
        retval = self.pm_client.promoteQPackageToMaster(self.pm_sessionId, domain, name, version, qualityLevel, domainLogin, domainPasswd)
        if retval:
            q.logger.log('QPackage %s promoted successfully to master repo'%name, 6)
        else:
            raise RuntimeError('Failed to promote QPackage %s to master repo'%name)

        return True

    def promoteQPackage(self, domain, name, version, buildNr, destQualityLevels, domainLogin, domainPassword):
        """
        Promote a QPackage to a higher qualityLevel on the server.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain of the QPackage
        @param name:           Name of the QPackage
        @param version:        Version of the QPackage
        @param buildNr:        buildNr you wish to promote
        @param destQualityLevels:    List of qualityLevels to where you wish to promote
        @param domainLogin:    The user's login for the given domain
        @param domainPassword: The user's password for the given domain
        """
        q.logger.log('Calling the server to promote QPackage %s'%name, 8)
        retval = self.pm_client.promoteQPackage(self.pm_sessionId, domain, name, version, buildNr, destQualityLevels, domainLogin, domainPassword)
        if not retval:
            raise RuntimeError('Failed to promote QPackage <%s>'%name)
        q.logger.log('QPackage <%s> buildNr <%s> promoted successfully to <%s>'%(name, str(buildNr), destQualityLevels), 8)

        return True

    def createNewBuild(self, domain, name, version, qualityLevel):
        ''' Create a new QPackage build on the server
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: qualityLevel where you wish to create the build.
        '''
        q.logger.log('asking the server to create QPackage build %s on domain %s'%(name, domain), 8)
        retval =  self.pm_client.createNewQPackageBuild(self.pm_sessionId, domain, name, version, qualityLevel)
        q.logger.log('create QPackage build returns %s'%retval, 8)
        if retval:
            q.logger.log('created new build for QPackage %s with version %s for domain %s on the server'%(name, version, domain), 8)
        else:
            raise RuntimeError('could not create new build for QPackage %s with version %s on domain %s'%(name, version, domain))
        return True

    def downloadConfig(self, domain, name, version, qualityLevel='trunk'):
        ''' Download a QPackage's config

        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        '''
        q.logger.log('prepare to download configuration of the QPackage %s with version %s'%(name, version),8)
        if not self.isConnected():
            self.connect()
        fullModule = '%s_read'%(self.pm_sessionId)
        qpackage = self.pm_client.prepareDownload(self.pm_sessionId, domain, name, version, qualityLevel)
        remoteDirs = self.pm_client.getRemoteDirs('qpackages/%s/'%qpackage.getRelativeQPackagePath(), fullModule)
        q.logger.log('prepare to download configuration of the QPackage %s with version %s'%(name, version),8)
        if 'cfg' in remoteDirs:
            q.logger.log('downloading configuration of the QPackage %s with version %s'%(name, version),8)
            self.pm_client.syncFolderFromServer('qpackages/%s/cfg'%(qpackage.getRelativeQPackagePath()), q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath()), fullModule)
        else:
            raise RuntimeError('config files have not been found')
        self.downloadSynced(domain, name, version, qualityLevel)

    def download(self, domain, name, version, qualityLevel, supportedPlatforms=None, downloadAllFiles=False, module='read'):
        ''' Download a QPackage

        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel you wish to download
        @param supportedPlatforms: The supportedPlatforms you wish to download
        @param downloadAllFiles: defaults to False, if True it will download all files in the build.
        '''
        q.logger.log('prepare to download the QPackage %s with version %s'%(name, version),8)
        if not self.isConnected():
            self.connect()
        qpackage = self.pm_client.prepareDownload(self.pm_sessionId, domain, name, version, qualityLevel)
        q.logger.log('received qpackageobject %s with version %s'%(name, version),8)
        # prepare the downloadfolder (depending on archive parameter is set) by moving old buildnr if exists, or create new download folder
        qpackagePath = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath())
        downloadFolder = q.system.fs.joinPaths(qpackagePath, 'download')
        if q.system.fs.exists(downloadFolder):
            QPackageUtils.removeDir(downloadFolder)
        if not q.system.fs.exists(qpackagePath):
            q.system.fs.createDir(qpackagePath)
        if qpackage and qualityLevel in qpackage.buildNr.iterkeys():
            if q.system.fs.exists(q.system.fs.joinPaths(qpackagePath, qpackage.buildNr[qualityLevel])):
                q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackagePath, qpackage.buildNr[qualityLevel]), downloadFolder)
                QPackageUtils.removeDir(q.system.fs.joinPaths(qpackagePath, qpackage.buildNr[qualityLevel]))
        if not q.system.fs.exists(downloadFolder):
            q.system.fs.createDir(downloadFolder)
        self._download(qpackage, qualityLevel, supportedPlatforms=supportedPlatforms, downloadAllFiles=downloadAllFiles, module=module)

        q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackagePath, 'download') , q.system.fs.joinPaths(qpackagePath, str(qpackage.buildNr[str(qualityLevel)])))
        QPackageUtils.removeDir(q.system.fs.joinPaths(qpackagePath, 'download'))

        q.logger.log('notifying the server that the download is done', 8)
        self.pm_client.downloadSynced(self.pm_sessionId, domain, name, version, qualityLevel)

    def _download(self, qpackage, qualityLevel, supportedPlatforms=None, downloadAllFiles=False, module='read'):
        """ Download a QPackage

        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: qualityLevel you wish to download
        @param supportedPlatforms: The supportedPlatforms you wish to download
        @param downloadAllFiles: defaults to False, if True it will download all files in the build.
        """
        q.logger.log('start downloading the QPackage %s with version %s'%(qpackage.name, qpackage.version),8)
        fullModule = '%s_%s'%(self.pm_sessionId, module)
        # logic for copying the files of the QPackage.
        # download the cfg folder
        remoteDirs = self.pm_client.getRemoteDirs('qpackages/%s/'%qpackage.getRelativeQPackagePath(), fullModule)
        if 'cfg' in remoteDirs:
            self.pm_client.syncFolderFromServer('qpackages/%s/cfg'%(qpackage.getRelativeQPackagePath()), q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath()), fullModule)
        if 'installer' in remoteDirs:
            self.pm_client.syncFolderFromServer('qpackages/%s/installer'%(qpackage.getRelativeQPackagePath()), q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath()), fullModule)
        if 'LICENSES' in remoteDirs:
            self.pm_client.syncFolderFromServer('qpackages/%s/LICENSES'%(qpackage.getRelativeQPackagePath()), q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath()), fullModule)
        downloadDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'download')

        if downloadAllFiles:
            remoteDirs = self.pm_client.getRemoteDirs('qpackages/%s'%qpackage.getRelativeQPackagePath(), fullModule)
            buildPath = qpackage.getRelativeBuildPath(qualityLevel)
            if buildPath[buildPath.rfind(os.sep)+1:] in remoteDirs:
                listOfDirs = self.pm_client.getRemoteDirs('qpackages/%s/'%qpackage.getRelativeBuildPath(qualityLevel), fullModule)
                if listOfDirs:
                    self.pm_client.syncFolderFromServer('qpackages/%s/'%qpackage.getRelativeBuildPath(qualityLevel), downloadDir, fullModule)
        else:
            # get the remote dirs and run over them
            remoteDirs = self.pm_client.getRemoteDirs('qpackages/%s'%qpackage.getRelativeBuildPath(qualityLevel), fullModule)
            for remoteDir in remoteDirs:
                # whithin the remote dir the folders should be the string representation of the PlatformType, others are ignored.
                platformDirs = self.pm_client.getRemoteDirs('qpackages/%s/%s'%(qpackage.getRelativeBuildPath(qualityLevel), remoteDir), fullModule)
                if supportedPlatforms and not isinstance(supportedPlatforms, list):
                    supportedPlatforms = str(supportedPlatforms).split(',')
                for plat in supportedPlatforms:
                    for platDir in platformDirs:
                        try:
                            PlatformType.getByName(platDir)
                        except KeyError:
                            continue
                        if PlatformType.getByName(str(platDir)) in [key for key in PlatformType.ALL] and PlatformType.getByName(str(plat)).has_parent(platDir):
                            localDir = q.system.fs.joinPaths(downloadDir, remoteDir)
                            if not q.system.fs.exists(localDir):
                                q.system.fs.createDir(localDir)
                            self.pm_client.syncFolderFromServer('qpackages/%s/%s/%s'%(qpackage.getRelativeBuildPath(qualityLevel), remoteDir, platDir), localDir, fullModule)
        q.logger.log('finished downloading the QPackage %s with version %s'%(qpackage.name, qpackage.version),8)

    def syncToServer(self, qpackage, qualityLevel, syncFiles):
        ''' Sync files to the server.

        @param qpackage: QPackageObject that you wish to sync
        @param qualityLevel: qualitylevel you wish to sync
        @param syncFiles: if True you will sync all the files, if False you will only sync the cfg files
        '''
        def addConfigSnapshotToBuild(remoteFolder, module):
            tmpdir = q.system.fs.getTmpFilePath()
            q.system.fs.removeFile(tmpdir)
            q.system.fs.createDir(tmpdir)
            try:
                configFile = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'cfg', 'qpackage.cfg')
                tmpConfigFile = q.system.fs.joinPaths(tmpdir, 'build.cfg')
                q.system.fs.copyFile(configFile, tmpConfigFile)
                ini = q.tools.inifile.open(tmpConfigFile)
                for section in ini.getSections():
                    if section.startswith('ql_'):
                        ini.removeSection(section)
                ini.write()
                self.pm_client.syncFolderToServer(q.system.fs.joinPaths(tmpdir, ''), '%s/upload_%s/.cfg/'%(remoteFolder,qualityLevel), module)
            finally:
                q.system.fs.removeDirTree(tmpdir)

            
        q.logger.log('started uploading the QPackage %s with version %s'%(qpackage.name, qpackage.version),8)
        if syncFiles:
            localFolder = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'upload_%s'%str(qualityLevel), '')
            remoteFolder = 'qpackages/%s'%qpackage.getRelativeQPackagePath()
            module = '%s_write'%self.pm_sessionId
            self.pm_client.syncFolderToServer(localFolder, '%s/upload_%s/'%(remoteFolder,qualityLevel), module)
            localFolder = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'cfg', '')
            if q.system.fs.exists(localFolder):
                addConfigSnapshotToBuild(remoteFolder, module)
                self.pm_client.syncFolderToServer(localFolder, '%s/cfg/'%(remoteFolder), module)
            localFolder = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'installer', '')
            if q.system.fs.exists(localFolder):
                self.pm_client.syncFolderToServer(localFolder, '%s/installer/'%(remoteFolder), module)
            localFolder = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'LICENSES', '')
            if q.system.fs.exists(localFolder):
                self.pm_client.syncFolderToServer(localFolder, '%s/LICENSES/'%(remoteFolder), module)
        else:
            localFolder = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'cfg', '')
            remoteFolder = 'qpackages/%s/'%qpackage.getRelativeQPackagePath()
            module = '%s_write'%self.pm_sessionId
            self.pm_client.syncFolderToServer(localFolder, remoteFolder, module)
        q.logger.log('finished uploading the QPackage %s with version %s'%(qpackage.name, qpackage.version),8)

    def createNewSynced(self, domain, name, version, qualityLevel='trunk'):
        ''' Finish the sync to the server, so the server can process the new QPackage

        @param domain: name of the domain
        @param name: name of the QPackage
        @param version: version of the  QPackage
        '''
        q.logger.log('closing the upload session for QPackage %s with version %s'%(name, version), 8)
        retval = self.pm_client.createNewQPackageSynced(self.pm_sessionId, str(domain), name, version, qualityLevel)
        if retval >= 0:
            q.logger.log('successfully closed the upload session for QPackage %s with version %s'%(name, version), 8)
            fromDir = q.system.fs.joinPaths(q.dirs.packageDir, str(domain), name, version, 'upload_%s'%qualityLevel)
            toDir = q.system.fs.joinPaths(q.dirs.packageDir, str(domain), name, version, str(retval))
            q.system.fs.copyDirTree(fromDir, toDir)
            QPackageUtils.removeDir(fromDir)
        else:
            q.logger.log('unsuccessfully closed the upload session for QPackage %s with version %s'%(name, version), 8)

        return retval

    def createNewVersionSynced(self, domain, name, version, qualityLevel='trunk'):
        ''' Finish the sync to the server, so the server can process the new QPackage

        @param domain: name of the domain
        @param name: name of the QPackage
        @param version: version of the  QPackage
        '''
        q.logger.log('closing the upload session for QPackage %s with version %s'%(name, version), 8)
        retval = self.pm_client.createNewQPackageVersionSynced(self.pm_sessionId, str(domain), name, version, qualityLevel)
        if retval >= 0:
            q.logger.log('successfully closed the upload session for QPackage %s with version %s'%(name, version), 8)
            fromDir = q.system.fs.joinPaths(q.dirs.packageDir, str(domain), name, version, 'upload_%s'%qualityLevel)
            toDir = q.system.fs.joinPaths(q.dirs.packageDir, str(domain), name, version, str(retval))
            q.system.fs.copyDirTree(fromDir, toDir)
            QPackageUtils.removeDir(fromDir)
        else:
            q.logger.log('unsuccessfully closed the upload session for QPackage %s with version %s'%(name, version), 8)

        return retval

    def createNewBuildSynced(self, domain, name, version, qualityLevel):
        ''' Finish the sync to the server, so the server can process the new QPackage

        @param domain: name of the domain
        @param name: name of the QPackage
        @param version: version of the  QPackage
        @param qualityLevel: qualityLevel of the QPackage
        '''
        q.logger.log('closing the upload session for QPackage %s with version %s'%(name, version), 8)
        retval = self.pm_client.createNewQPackageBuildSynced(self.pm_sessionId, str(domain), name, version, qualityLevel)
        if retval >= 0:
            q.logger.log('successfully closed the upload session for QPackage %s with version %s'%(name, version), 8)
            fromDir = q.system.fs.joinPaths(q.dirs.packageDir, str(domain), name, version, 'upload_%s'%str(qualityLevel))
            toDir = q.system.fs.joinPaths(q.dirs.packageDir, str(domain), name, version, str(retval))
            if q.system.fs.exists(toDir):
                QPackageUtils.removeDir(toDir)
            q.system.fs.copyDirTree(fromDir, toDir)
            QPackageUtils.removeDir(fromDir)
        else:
            q.logger.log('unsuccessfully closed the upload session for QPackage %s with version %s'%(name, version), 8)

        return retval

    def getVLists(self, domains=None):
        """
        Sync the VLists to the local VLists folder
        @param domains: list of domains to retrieve vlists for
        """
        q.logger.log('syncing the VLists', 8)
        if not self.isConnected():
            raise RuntimeError('Please connect first to QPackage Server ' \
                    '(%s, %s@%s:%s)'
                    % (self.name, self.login, self.host, self.port))
        self.pm_client.getVLists(self.pm_sessionId, domains if domains else self.domains)
        q.logger.log('synced the VLists', 8)

    def removeVlists(self, domains=None):
        """
        Remove vlists received from the server
        """
        for domain in domains or self.domains:
            domainVlists = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageclient', 'vlists', domain)
            if q.system.fs.exists(domainVlists):
                q.system.fs.removeDirTree(domainVlists)

    def delete(self, name, version, domain, domainLogin, domainPasswd, fromMaster=False):
        '''Delete the QPackage on the server(s).

        @param name:                name of the QPackage
        @param version:             version of the QPackage
        @param domain:              string representation of the domain
        @param fromMaster:          if True the QPackage will be deleted from the master server
        @param domainLogin:         The user's login for the given domain
        @param domainPasswd:      The user's password for the given domain
        '''
        q.logger.log('deleting the QPackage %s with version %s'%(name, version), 8)

        if not self.pm_client.delete(self.pm_sessionId, domain, name, version, domainLogin, domainPasswd, fromMaster):
            raise RuntimeError('failed to delete the QPackage on the server')
        q.logger.log('deleted the QPackage %s with version %s'%(name, version), 8)

    def __str__(self):
        return '%s'%(self.name)

    def __repr__(self):
        return str(self)

