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
from pylabs import q
from pylabs.baseclasses import BaseType
from pylabs.qpackages.common.QPackageObject import QPackageObject
from pylabs.qpackages.server.ServerManagement import ServerManagement
from pylabs.qpackages.client.QPackageServerConnection import QPackageServerConnection, QPackageServerConnections
from pylabs.qpackages.common.QPackageVersioning import QPackageVersioning
import logging, logging.handlers

class QPackageServer(BaseType):
    """
    The QPackageServer is the interface for all QPackage clients. It is an XMLRPC exposed interface combined
    with a set of rsync modules used for file transfer.
    """
    pm_ServerManagement = q.basetype.object(ServerManagement, doc='ServerManagement', default=ServerManagement())
    #############################
    ## Session Related Methods ##
    #############################

    def _initLogging(self):
        """
        Initialize logging
        """
        qpackageserverLogDir = q.system.fs.joinPaths(q.dirs.logDir, 'qpackageServer')
        if not q.system.fs.exists(qpackageserverLogDir):
            q.system.fs.createDir(qpackageserverLogDir)

        self.auditingLogger = logging.getLogger('QPackageServer_Auditing')
        self.auditingLogger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(message)s")
        auditingHandler = logging.handlers.TimedRotatingFileHandler(\
            q.system.fs.joinPaths(qpackageserverLogDir, 'qpackageserver.audit'), when='D', backupCount=365)

        auditingHandler.setFormatter(formatter)
        auditingHandler.setLevel(logging.INFO)

        self.auditingLogger.addHandler(auditingHandler)

    def __init__(self, taskletPath=None):
        self._initLogging()

        if not taskletPath:
            # Calculate 'default' path
            components = (pylabs.q.dirs.baseDir, 'apps',
                          'applicationServer', 'services', 'qpackageserver',
                          'tasklets', )
            taskletPath = pylabs.q.system.fs.joinPaths(*components)

        # Just in case...
        pylabs.q.system.fs.createDir(taskletPath)

        self._taskletEngine = pylabs.q.getTaskletEngine(taskletPath)

    @q.manage.applicationserver.expose
    def sessionLogin(self, login, password, applicationserver_request):
        """
        Checks the credentials and creates a new session for the client on the server.
        All actions on the QPackageServer are authenticated using the returned guid.

        @param login:          The client's login
        @param password:       The client's password
        @param xmlrpc_request: The XMLRPC request object
        @return:               The client's unique session id (guid)
        """

        ipAddress = applicationserver_request.client_ip
        self.auditingLogger.info('(login=%s,password=%s,ipAddress=%s)'%(login,password,ipAddress))
        q.logger.log('Login request for user %s from ip %s' % (login, ipAddress), 6)

        if not self.pm_ServerManagement.authenticate(login, password):
            q.logger.log('Login failed for user %s' % login, 5)
            raise ValueError('Authentication failed!')

        q.logger.log('Login successful for user %s, creating session...' % login, 5)
        session = self.pm_ServerManagement.sessions.sessionCreate(login, ipAddress=ipAddress)

        q.logger.log('Session  with id %s created successful for user %s' % (session.id, login), 5)
        self.auditingLogger.info('%s - Done successfully'%session.id)
        return session.id

    @q.manage.applicationserver.expose
    def sessionLogout(self, sessionId):
        """
        Closes a client's session.
        If a session is not closed explicitly it will be closed automatically after a time-out period.

        @param sessionId: The client's authenticated session id.
        """
        self.auditingLogger.info('%s - (sessionId=%s)' % (sessionId, sessionId))
        q.logger.log('Logout request for session %s' % sessionId, 5)

        self.pm_ServerManagement.sessions.sessionDelete(sessionId)

        q.logger.log('Session with id %s deleted successfully' % sessionId, 5)
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return True

    @q.manage.applicationserver.expose
    def sessionValidate(self, sessionId):
        """
        Checks if a session is still valid.

        @param sessionId: The client's authenticated session id.

        @return:          Boolean indicating if session is valid or not.
        """
        self.auditingLogger.info('Validation request for session %s' % sessionId)
        q.logger.log('Validation request for session %s' % sessionId, 5)
        return self.pm_ServerManagement.sessions.sessionValidate(sessionId)

    @q.manage.applicationserver.cronjob(10800)
    def sessionsCleanUp(self):
        """
        Clean up un used sessions
        """
        self.auditingLogger.info('Cleaning up unused sessions. Sessions = %s'%str(self.pm_ServerManagement.sessions.sessions))
        self.pm_ServerManagement.sessions.sessionsCleanUp()
        self.auditingLogger.info('Sessions Cleaned up successfully. Sessions = %s'%str(self.pm_ServerManagement.sessions.sessions))

    ############################
    ## Domain Related Methods ##
    ############################

    @q.manage.applicationserver.expose
    def listDomains(self, sessionId):
        """
        Return the list of domains served
        """
        q.logger.log('Listing domains served', 6)
        self.auditingLogger.info('%s - (sessionId=%s)'%(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId))
        self._checkIfSessionIsValid(sessionId)
        domainList = self.pm_ServerManagement.packagesDir.vlists.getDomains()
        listOfDomains = list()
        for domain in domainList:
            listOfDomains.append(str(domain))
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return listOfDomains

    @q.manage.applicationserver.expose
    def qpackageCreateNew(self, sessionId, domain, qpackageName, version, qualityLevel='trunk'):
        """
        Creates a new QPackage in a given domain on the server.

        The content of the QPackage will be copied from a template QPackage, and the newly
        created QPackage will be available for download for the creator (client) using rsync.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage should be created
        @param qpackageName:       Name for the new QPackage
        @param version:        Version for the new QPackage
        @param qualityLevel:   quality level of the QPackage
        @return:               Boolean indicating if the QPackage was created successfully
        """

        self.auditingLogger.info('%s - qpackageCreateNew(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, qualityLevel))

        q.logger.log('Creating new QPackage <%s>'%(qpackageName), 6)

        self._checkIfSessionIsValid(sessionId)

        q.logger.log('Checking that user is authorized to create qpackages', 6)
        if not self.pm_ServerManagement.authorize(domain, qualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, permissionType=q.enumerators.ACLPermission.RW):
            raise RuntimeError('User <%s> is not authorized to create qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        self._checkIfQPackageExists(qpackageName, exists=False)

        self._createNewQPackageFromTemplate(sessionId, qpackageName, domain, version)
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return True

    @q.manage.applicationserver.expose
    def qpackageCreateNewSynced(self, sessionId, domain, qpackageName, version, qualityLevel='trunk'):
        """
        Notifies the server the files of a newly created QPackage are available on the server.

        The server will perform some checks on the files and create the new version and
        build number if successful.

        If server is authoritative for domain, build 1 will be created, else build 0.

        The QPackage.cfg will be updated and new vlists for the domain will be re-generated.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage is synced
        @param qpackageName:       Name for the synced QPackage
        @param version:        Version for the synced QPackage
        @param qualityLevel:   quality level of the QPackage
        @return:               New build number
        """
        self.auditingLogger.info('%s - qpackageCreateNewSynced(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, qualityLevel))
        q.logger.log('Creating the QPackage locally after successful sync from client', 6)

        self._checkIfSessionIsValid(sessionId)

        sessionQPackagesDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'write', 'qpackages')
        qpackageDir = q.system.fs.joinPaths(sessionQPackagesDir, domain, qpackageName, version)

        if not q.system.fs.exists(qpackageDir):
            raise IOError('QPackage directory <%s> does not exist'%qpackageDir)

        q.logger.log('Checking that user is authorized to create qpackages', 6)
        if not self.pm_ServerManagement.authorize(domain, qualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, permissionType=q.enumerators.ACLPermission.RW):
            raise RuntimeError('User <%s> is not authorized to create qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        buildNr = self._checkIfServerIsAuthoritative(qpackageName, domain=domain, checkDomain=False, qpackageExists=False)

        self._createQPackageLocally(sessionId, domain, qpackageName, version, buildNr, qualityLevel)

        self.runTasklets(('new', 'created'), {
            'domain': domain,
            'name': qpackageName,
            'version': version,
            'build': buildNr,
            'qualitylevel': qualityLevel,
            'session': sessionId,
        })

        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return buildNr

    @q.manage.applicationserver.expose
    def qpackagePromoteLocalToMaster(self, sessionId, domain, qpackageName, version, domainLogin, domainPassword, qualityLevel='trunk'):
        """
        Promotes a local build on the server to the master domain's server.
        This is only supported if the server is a direct client of the master domain's server.
        The server will act as client and create the the QPackage on the master domain's server.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain from which the QPackage should be promoted
        @param qpackageName:       Name of the QPackage to promote
        @param version:        Version of the QPackage to promote
        @param domainLogin:    The user's login for the given domain
        @param domainPassword: The user's password for the given domain
        @param qualityLevel:   quality level of the QPackage

        @return:               Boolean indicating if the QPackage was promoted successfully
        """
        self.auditingLogger.info('%s - qpackagePromoteLocalToMaster(sessionId=%s, domain=%s, qpackageName=%s, version=%s, domainLogin=%s, domainPassword=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, domainLogin, domainPassword, qualityLevel))
        q.logger.log('Promoting qpackage <%s> to master repo', 6)

        serverConnection = self._getServerConnectionToMaster(domain, domainLogin, domainPassword)

        self.pm_ServerManagement.vlists.loadVLists(domain)
        action = 'new'
        if self.pm_ServerManagement.vlists.find(qpackageName):
            if self.pm_ServerManagement.vlists.find(qpackageName, domain=domain, version=version):
                q.logger.log('Creating new build on master repo for QPackage <%s>'%qpackageName, 6)
                serverConnection.createNewBuild(domain, qpackageName, version, qualityLevel)
                action='build'
            else:
                q.logger.log('Creating new version on master repo for QPackage <%s>'%qpackageName, 6)
                serverConnection.createNewVersion(domain, qpackageName, version, qualityLevel, download=False)
                action='version'
        else:
            q.logger.log('Creating new QPackage <%s> on master repo'%qpackageName, 6)
            serverConnection.createNew(domain, qpackageName, version,qualityLevel, download=False)

        qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageName, version, domain=domain, qualityLevel=qualityLevel)
        qpackageDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackageObject.getRelativeQPackagePath())

        buildDir = q.system.fs.joinPaths(qpackageDir, '%s_%s'%(str(qpackageObject.buildNr[qualityLevel]), qualityLevel))
        q.logger.log('Checking if build directory exists <%s>'%buildDir, 6)
        if not q.system.fs.exists(buildDir):
            raise IOError('Directory <%s> does not exist'%buildDir)
        q.logger.log('Moving build dir <%s> to upload_%s directory'%(buildDir, qualityLevel), 6)
        q.system.fs.moveDir(buildDir, q.system.fs.joinPaths(qpackageDir, 'upload_%s'%qualityLevel))
        q.logger.log('Syncing QPackage <%s> to server'%qpackageName, 6)
        serverConnection.syncToServer(qpackageObject, qualityLevel, syncFiles=True)
        buildNr = None
        if action == 'new':
            buildNr = serverConnection.createNewSynced(domain, qpackageName, version, qualityLevel)
        elif action == 'version':
            buildNr = serverConnection.createNewVersionSynced(domain, qpackageName, version, qualityLevel)
        elif action == 'build':
            buildNr = serverConnection.createNewBuildSynced(domain, qpackageName, version, qualityLevel)

        uploadDir = q.system.fs.joinPaths(qpackageDir, 'upload_%s'%qualityLevel)
        q.logger.log('Checking if upload directory <%s> still exists'%uploadDir, 6)
        if q.system.fs.exists(uploadDir):
            q.system.fs.moveDir(uploadDir, buildDir)
            raise RuntimeError('Failed to sync to master repo')

        q.logger.log('Checking buildNr returned is not None', 6)
        if not buildNr is None:
            newBuildDir = q.system.fs.joinPaths(qpackageDir, str(buildNr))
            q.logger.log('Checking if new build directory <%s> exists'%newBuildDir, 6)
            if not q.system.fs.exists(newBuildDir):
                raise IOError('Directory <%s> does not exist'%newBuildDir)
            qpackageObject.buildNr[qualityLevel] = buildNr
            q.logger.log('Generating configuration for QPackage <%s>'%qpackageObject.name, 6)
            qpackageObject.createConfig()

        q.logger.log('Updating vlists', 6)
        self.pm_ServerManagement.packagesDir.createVlists(domain, qualityLevel)
        q.logger.log('Retrieving the latest vlist from master repo', 6)
        serverConnection.getVLists(domain)
        q.logger.log('Disconnecting from master repo', 6)
        serverConnection.disconnect()
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return True

    ############################
    ## Server Related Methods ##
    ############################

    @q.manage.applicationserver.expose
    def qpackageCreateNewVersion(self, sessionId, domain, qpackageName, version, qualityLevel='trunk', \
                             copyDependencies=True, copySupportedPlatforms=True, copyDescription=True,\
                             copyTags=True, copyFiles=True):
        """
        Creates a new version of a QPackage in a given domain on the server.

        The content of the QPackage will be copied from the previous version of the QPackage, and the newly
        created QPackage version will be available for download for the creator (client) using rsync.

        @param sessionId              :The client's authenticated session id.
        @param domain                 :Domain in which the QPackage exists
        @param qpackageName               :Name of the QPackage
        @param version                :New version for the QPackage
        @param qualityLevel:   quality level of the QPackage
        @param copyDependencies       :copy the dependencies of the QPackage
        @param copySupportedPlatforms :copy the supported platforms of the QPackage
        @param copyDescription        :copy description of the QPackage
        @param copyTags               :copy tags of the QPackage
        @param copyFiles              :copy files of the QPackage
        @return                       :Boolean indicating if the version was created successfully
        """
        self.auditingLogger.info('%s - qpackageCreateNewVersion(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s, copyDependencies=%s, copySupportedPlatforms%s, copyDescription=%s, copyTags=%s, copyFiles=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), \
                       sessionId, domain, qpackageName, version, qualityLevel, copyDependencies, \
                       copySupportedPlatforms, copyDescription, copyTags, copyFiles))

        q.logger.log('Creating new QPackage Version <%s, %s>'%(qpackageName, version), 6)

        self._checkIfSessionIsValid(sessionId)

        q.logger.log('Checking that user is authorized to create qpackages', 6)
        if not self.pm_ServerManagement.authorize(domain, qualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName=qpackageName, permissionType=q.enumerators.ACLPermission.RW):
            raise RuntimeError('User <%s> is not authorized to create new version of qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        self._checkIfQPackageExists(qpackageName, domain, version, exists=False)

        qpackageObject = self._getLatestVersionQPackageObject(qpackageName, domain)

        self._createQPackageNew(sessionId, qpackageObject, version, qualityLevel, newVersion=True, \
                            copyDependencies=copyDependencies, copySupportedPlatforms=copySupportedPlatforms, \
                            copyDescription=copyDescription, copyTags=copyTags, copyFiles=copyFiles)
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return True

    @q.manage.applicationserver.expose
    def qpackageCreateNewVersionSynced(self, sessionId, domain, qpackageName, version, qualityLevel='trunk'):
        """
        Notifies the server the files of a newly created version of a QPackage are available on the server.

        The server will perform some checks on the files and create build a build number if
        successful.

        If server is authoritative for domain, build 1 will be created, else build 0.

        The QPackage.cfg will be updated and new vlists for the domain will be re-generated.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage is synced
        @param qpackageName:       Name for the synced QPackage
        @param version:        Version for the synced QPackage
        @param qualityLevel:   quality level of the QPackage
        @return:               New build number
        """
        self.auditingLogger.info('%s - qpackageCreateNewVersionSynced(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, qualityLevel))

        q.logger.log('Creating the new QPackage version locally after successful sync from client', 6)

        self._checkIfSessionIsValid(sessionId)

        sessionQPackagesDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'write', 'qpackages')
        qpackageDir = q.system.fs.joinPaths(sessionQPackagesDir, domain, qpackageName, version)

        if not q.system.fs.exists(qpackageDir):
            raise IOError('QPackage directory <%s> does not exist'%qpackageDir)

        q.logger.log('Checking that user is authorized to create qpackages', 6)
        if not self.pm_ServerManagement.authorize(domain, qualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName=qpackageName, permissionType=q.enumerators.ACLPermission.RW):
            raise RuntimeError('User <%s> is not authorized to create new version of qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        buildNr = self._checkIfServerIsAuthoritative(qpackageName, domain, version, qpackageExists=False)

        self._createQPackageLocally(sessionId, domain, qpackageName, version, buildNr, qualityLevel, create=False)

        self.runTasklets(('version', 'created'), {
            'domain': domain,
            'name': qpackageName,
            'version': version,
            'build': buildNr,
            'qualitylevel': qualityLevel,
            'session': sessionId,
        })

        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return buildNr

    @q.manage.applicationserver.expose
    def qpackageCreateNewBuild(self, sessionId, domain, qpackageName, version, qualityLevel):
        """
        Creates a new build of a version of a QPackage in a given domain on the server.

        The content of the QPackage build will be copied from the previous build of the same version
        of the QPackage, and the newly created build QPackage will be available for download for the
        creator (client) using rsync.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage should be created
        @param qpackageName:       Name for the new QPackage
        @param version:        Version for the new QPackage
        @param qualityLevel:   quality level of the QPackage
        @return:               Boolean indicating if the build was created successfully
        """
        self.auditingLogger.info('%s - qpackageCreateNewBuild(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, qualityLevel))

        q.logger.log('Creating the new build of <%s>'%(qpackageName), 6)

        self._checkIfSessionIsValid(sessionId)

        q.logger.log('Checking that user is authorized to create qpackages', 6)
        if not self.pm_ServerManagement.authorize(domain, qualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName=qpackageName, permissionType=q.enumerators.ACLPermission.RW):
            raise RuntimeError('User <%s> is not authorized to update qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        self._checkIfQPackageExists(qpackageName, domain, version, exists=True)

        qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageName, version, domain, qualityLevel)

        self._createQPackageNew(sessionId, qpackageObject, version, qualityLevel, newVersion=False)
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return True

    @q.manage.applicationserver.expose
    def qpackageCreateNewBuildSynced(self, sessionId, domain, qpackageName, version, qualityLevel):
        """
        Notifies the server the files of a newly created build of a version of QPackage are available on the server.

        The server will perform some checks on the files and create build a build number if
        successful.

        If server is authoritative for domain, build is last build + 1, else build 0.

        The QPackage.cfg will be updated and new vlists for the domain will be generated.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage is synced
        @param qpackageName:       Name for the synced QPackage
        @param version:        Version for the synced QPackage
        @param qualityLevel:   quality level of the QPackage
        @return:               New build number
        """
        self.auditingLogger.info('%s - qpackageCreateNewBuildSynced(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, qualityLevel))

        q.logger.log('Creating the new build of QPackage <%s> locally after successful sync from client'%(qpackageName), 6)

        self._checkIfSessionIsValid(sessionId)

        sessionQPackagesDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'write', 'qpackages')
        qpackageDir = q.system.fs.joinPaths(sessionQPackagesDir, domain, qpackageName, version)

        if not q.system.fs.exists(qpackageDir):
            raise IOError('QPackage directory <%s> does not exist'%qpackageDir)

        q.logger.log('Checking that user is authorized to create qpackages', 6)
        if not self.pm_ServerManagement.authorize(domain, qualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName=qpackageName, permissionType=q.enumerators.ACLPermission.RW):
            raise RuntimeError('User <%s> is not authorized to update qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        buildNr = self._checkIfServerIsAuthoritative(qpackageName, domain, version, qualityLevel, qpackageExists=True, createNewBuild=True)

        self._createQPackageLocally(sessionId, domain, qpackageName, version, buildNr, qualityLevel, create=False)

        self.runTasklets(('build', 'created'), {
            'domain': domain,
            'name': qpackageName,
            'version': version,
            'build': buildNr,
            'qualitylevel': qualityLevel,
            'session': sessionId,
        })

        self.auditingLogger.info('%s - NewBuildCreated(domain=%s, qpackageName=%s, version=%s, buildNr=%s, qualityLevel=%s) - Done successfully'
                                 % (str(self.pm_ServerManagement.sessions.sessions[sessionId]), domain, qpackageName, version, buildNr, qualityLevel))
        return buildNr

    @q.manage.applicationserver.expose
    def qpackageDownload(self, sessionId, domain, qpackageName, version, qualityLevel):
        """
        Prepares a QPackage for download for the given session.

        Will link the requested QPackage to the readable rsync module of this session.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage should be download from
        @param qpackageName:       Name of the qpackage to download
        @param version:        Version of the qpackage to download
        @param qualityLevel:   quality level of the qpackage to download
        """
        self.auditingLogger.info('%s - qpackageDownload(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, qualityLevel))

        q.logger.log('Downloading QPackage <%s>'%(qpackageName), 6)

        self.pm_ServerManagement.packagesDir.vlists.loadVLists(domain)

        qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageName, version, domain, qualityLevel)

        if not self.pm_ServerManagement.authorize(domain, qualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName):
            raise RuntimeError('User <%s> is not authorized to download qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        buildNr = qpackageObject.buildNr[qualityLevel]
        if int(buildNr) == 0:
            buildNr = '0_%s'%qualityLevel
        buildDir = q.system.fs.joinPaths(qpackageObject.getRelativeQPackagePath(), str(buildNr))

        packageDir = q.system.fs.joinPaths(q.dirs.packageDir, buildDir)
        sessionDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'read')
        qpackageRelativePath = qpackageObject.getRelativeQPackagePath()

        if q.system.fs.isDir(sessionDir):
            q.system.fs.createDir(q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageRelativePath))

            cfgDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackageRelativePath, 'cfg')
            installDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackageRelativePath, 'installer')
            licenseDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackageRelativePath, 'LICENSES')

            if q.system.fs.isDir(cfgDir):
                q.logger.log('Creating symlink for <%s>'%cfgDir, 6)
                if not q.system.fs.isLink(q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageRelativePath,'cfg')):
                    q.system.fs.symlink(cfgDir, q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageRelativePath,'cfg'))
            if q.system.fs.isDir(installDir):
                q.logger.log('Creating symlink for <%s>'%installDir, 6)
                if not q.system.fs.isLink(q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageRelativePath,'installer')):
                    q.system.fs.symlink(installDir, q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageRelativePath,'installer'))
            if q.system.fs.isDir(licenseDir):
                q.logger.log('Creating symlink for <%s>'%licenseDir, 6)
                if not q.system.fs.isLink(q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageRelativePath, 'LICENSES')):
                    q.system.fs.symlink(licenseDir, q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageRelativePath,'LICENSES'))

            q.logger.log('Creating symlink for <%s>'%packageDir, 6)

            if not q.system.fs.isLink(q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageObject.getRelativeBuildPath(qualityLevel))):
                q.system.fs.symlink(packageDir, q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageObject.getRelativeBuildPath(qualityLevel)))
            q.logger.log('QPackage <%s> downloaded successfully'%qpackageName, 6)
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return self._pickleObject(qpackageObject)

    @q.manage.applicationserver.expose
    def qpackageDownloadSynced(self, sessionId, domain, qpackageName, version, qualityLevel):
        """
        Notifies the server the files of a qpackage are downloaded.

        The server will perform remove the link to this qpackage from the module.

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage should be created
        @param qpackageName:       Name for the new QPackage
        @param version:        Version for the new QPackage
        """
        self.auditingLogger.info('%s - qpackageDownloadSynced(sessionId=%s, domain=%s, qpackageName=%s, version=%s, qualityLevel=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, qualityLevel))

        q.logger.log('QPackage <%s, %s> download Synced'%(qpackageName, version), 6)
        self._checkIfSessionIsValid(sessionId)

        q.logger.log('Removing the linked qpackage', 8)

        qpackageObject = self.pm_ServerManagement.sessions.qpackageGetObject(sessionId, qpackageName, version, domain)

        qpackageRelativePath = qpackageObject.getRelativeQPackagePath()
        qpackageDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'read', 'qpackages', qpackageObject.getRelativeBuildPath(qualityLevel))

        if q.system.fs.isDir(qpackageDir):
            q.logger.log('Unlink directory <%s>'%qpackageDir, 6)
            q.system.fs.unlink(qpackageDir)

        cfgDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'read', 'qpackages',qpackageRelativePath,'cfg')
        installDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'read',  'qpackages',qpackageRelativePath, 'installer')
        licenseDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'read', 'qpackages', qpackageRelativePath, 'LICENSES')

        if q.system.fs.isDir(cfgDir):
            q.logger.log('Unlink directory <%s>'%cfgDir, 6)
            q.system.fs.unlink(cfgDir)

        if q.system.fs.isDir(installDir):
            q.logger.log('Unlink directory <%s>'%installDir, 6)
            q.system.fs.unlink(installDir)

        if q.system.fs.isDir(licenseDir):
            q.logger.log('Unlink directory <%s>'%licenseDir, 6)
            q.system.fs.unlink(licenseDir)
        self.auditingLogger.info('Done successfully')
        return True

    @q.manage.applicationserver.expose
    def qpackageGetObject(self, sessionId, domain, qpackageName, version):
        """
        Retrieve qpackageObject representing the qpackage requested

        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage should be download from
        @param qpackageName:       Name of the qpackage to download
        @param version:        Version of the qpackage to download
        """
        self.auditingLogger.info('%s - qpackageGetObject(sessionId=%s, domain=%s, qpackageName=%s, version=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version))

        q.logger.log('Retrieving qpackage object of qpackage %s'%(qpackageName), 6)

        self._checkIfSessionIsValid(sessionId)

        qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageName, version, domain)
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return self._pickleObject(qpackageObject)

    @q.manage.applicationserver.expose
    def qpackageDelete(self, sessionId, domain, qpackageName, version, domainLogin, domainPasswd, fromMaster):
        """
        Delete a QPackage
        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain in which the QPackage should be download from
        @param qpackageName:       Name of the qpackage to download
        @param version:        Version of the qpackage to download
        @param domainLogin:    The user's login for the given domain
        @param domainPasswd: The user's password for the given domain
        """
        self.auditingLogger.info('%s - qpackageDelete(sessionId=%s, domain=%s, qpackageName=%s, version=%s, domainLogin=%s, domainPasswd=%s, fromMaster=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), sessionId, domain, qpackageName, version, domainLogin,\
                       domainPasswd, fromMaster))

        q.logger.log('Delete QPackage %s'%(qpackageName), 6)

        self._checkIfSessionIsValid(sessionId)

        q.logger.log('Checking if QPackage %s exists in package dir'%qpackageName, 6)
        self._checkIfQPackageExists(qpackageName, domain, version, exists=True)

        qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageName, version, domain)

        q.logger.log('Checking that user is authorized to delete (RW) QPackage for all qualityLevels', 6)
        for qualityLevel in qpackageObject.buildNr:
            if not self.pm_ServerManagement.authorize(domain, str(qualityLevel), self.pm_ServerManagement.sessions.sessions[sessionId].login, permissionType=q.enumerators.ACLPermission.RW, qpackageName=qpackageName):
                raise RuntimeError('User <%s> is not authorized to delete qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        q.logger.log('Checking if domain is authoritative', 7)
        isAuthoritative = self._isDomainAuthoritative(domain)

        if not int(isAuthoritative) == 1 and fromMaster:
            q.logger.log('Checking on Master Repo if QPackage %s exists'%qpackageName, 6)

            q.logger.log('Get connection to master repo', 6)
            serverConnection = self._getServerConnectionToMaster(domain, domainLogin, domainPasswd)
            self._checkIfQPackageExistsOnMaster(qpackageName, domain, version, qpackageExists=True)
            q.logger.log('Calling Delete QPackage from master repo', 6)
            serverConnection.delete(qpackageName, version, domain, domainLogin, domainPasswd, fromMaster)

        q.logger.log('Deleting QPackage %s from package Dir'%qpackageName, 6)

        self.pm_ServerManagement.packagesDir.qpackageDelete(qpackageName, version, domain)
        self.auditingLogger.info('%s - Done successfully'%sessionId)
        return True

    @q.manage.applicationserver.expose
    def qpackagePromote(self, sessionId, domain, qpackageName, version, buildNr, destQualityLevels, domainLogin, domainPassword):
        """
        Promote a QPackage to a higher qualityLevel.

        @param sessionId:            The client's authenticated session id.
        @param domain:               Domain of the QPackage
        @param qpackageName:         Name of the QPackage
        @param version:              Version of the QPackage
        @param buildNr:              buildNr you wish to promote
        @param destQualityLevels:    List of qualityLevels to where you wish to promote
        @param domainLogin:          The user's login for the given domain
        @param domainPassword:       The user's password for the given domain
        """
        self.auditingLogger.info('%s - qpackagePromote(sessionId=%s, domain=%s, qpackageName=%s, version=%s, buildNr=%s, destQualityLevels=%s, domainLogin=%s, domainPassword=%s)'\
                     %(str(self.pm_ServerManagement.sessions.sessions[sessionId]), \
                       sessionId, domain, qpackageName, version, str(buildNr), str(destQualityLevels), domainLogin, domainPassword))

        q.logger.log('Promoting QPackage %s buildNr %s to qualityLevel %s'%(qpackageName, str(buildNr), destQualityLevels), 6)

        self._checkIfSessionIsValid(sessionId)

        for destQualityLevel in destQualityLevels:
            if not self.pm_ServerManagement.authorize(domain, destQualityLevel, self.pm_ServerManagement.sessions.sessions[sessionId].login, permissionType=q.enumerators.ACLPermission.RW, qpackageName=qpackageName):
                raise RuntimeError('User <%s> is not authorized to promote qpackage <%s> in domain <%s>'%(self.pm_ServerManagement.sessions.sessions[sessionId].login, qpackageName, domain))

        q.logger.log('Checking if QPackage %s exists in package dir'%qpackageName, 6)
        self._checkIfQPackageExists(qpackageName, domain, version, exists=True)

        q.logger.log('Checking if domain is authoritative', 7)
        isAuthoritative = self._isDomainAuthoritative(domain)

        if not isinstance(destQualityLevels, list):
            destQualityLevels = destQualityLevels.split(',')

        if not int(isAuthoritative) == 1:
            q.logger.log('Checking on Master Repo if QPackage %s exists'%qpackageName, 6)
            self._checkIfQPackageExistsOnMaster(qpackageName, domain, version, qpackageExists=True)

            q.logger.log('Get connection to master repo', 6)
            serverConnection = self._getServerConnectionToMaster(domain, domainLogin, domainPassword)
            serverConnection.promoteQPackage(domain, qpackageName, version, buildNr, destQualityLevels, domainLogin, domainPassword)

        else:
            qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageName, version, domain)
            if not q.system.fs.exists(q.system.fs.joinPaths(q.dirs.packageDir, qpackageObject.getRelativeQPackagePath(), str(buildNr))):
                raise IOError('Failed to find build directory.<%s>'%q.system.fs.joinPaths(qpackageObject.getRelativeQPackagePath(), str(buildNr)))

            for destQualityLevel in destQualityLevels:
                if not str(destQualityLevel) in qpackageObject.buildNr:
                    continue
                if int(qpackageObject.buildNr[str(destQualityLevel)]) >  int(buildNr):
                    raise ValueError('Failed to promote buildNr <%(newBuildNr)s> to qualityLevel \"%(destQualityLevel)s\". QualityLevel \"%(destQualityLevel)s\" has higher buildNr <%(destBuildNr)s>..'%{'newBuildNr':buildNr, 'destQualityLevel':destQualityLevel, 'destBuildNr':qpackageObject.buildNr[str(destQualityLevel)]})

            for destQualityLevel in destQualityLevels:
                qpackageObject.buildNr[destQualityLevel] = buildNr

            q.logger.log('Updating configuration for qpackage %s'%qpackageName, 6)
            qpackageObject.updateQualityLevels()

        self.pm_ServerManagement.packagesDir.createVlists(domain, destQualityLevels)
        self.pm_ServerManagement.packagesDir.vlists.loadVLists(domain, destQualityLevels)
        self.auditingLogger.info('%s - Done Successfully'%sessionId)

        return True

    def _getServerConnectionToMaster(self, domain, domainLogin, domainPassword):
        """
        Connect to master repo
        @param domain: name of the domain to get connection for
        @param domainLogin:    The user's login for the given domain
        @param domainPassword: The user's password for the given domain
        """
        connectionFromDomain = QPackageServerConnections().getConnectionFromDomain(domain)
        if not connectionFromDomain:
            raise RuntimeError('No connections configured serving domain <%s>'%domain)
        serverConnection = QPackageServerConnection('connectionToMaster', connectionFromDomain.host, connectionFromDomain.port, domainLogin, domainPassword)
        q.logger.log('Connecting to master repo <%s:%s>'%(connectionFromDomain.host, connectionFromDomain.port), 6)
        serverConnection.connect()
        self.auditingLogger.info('Done successfully')
        return serverConnection

    def _createQPackageLocally(self, sessionId, domain, qpackageName, version, buildNr, qualityLevel, create=True):
        """
        Create the new qpackage locally in package dir
        @param sessionId:      The client's authenticated session id.
        @param domain:         Domain of the new qpackage
        @param qpackageName:       Name of the new QPackage
        @param version:        Version of the new QPackage
        @param buildNr:        new build number of the new qpackage
        @param qualityLevel:   quality level of the new qpackage
        """
        sessionQPackagesDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'write', 'qpackages')
        qpackageDir = q.system.fs.joinPaths(sessionQPackagesDir, domain, qpackageName, version)
        q.logger.log('Instantiating qpackage object for the new qpackage created by the client', 6)
        qpackageObject = QPackageObject(domain, qpackageName, version, rootPath=sessionQPackagesDir)

        q.logger.log('Checking that the qpackage created has at least one supported platform', 6)
        if not qpackageObject.supportedPlatforms:
            raise ValueError('No Supported platforms were specified for qpackage <%s>'%qpackageName)
        qpackagePath = q.system.fs.joinPaths(q.dirs.packageDir, domain, qpackageName, version)
        if create:
            q.logger.log('Creating new qpackage %s from template'%qpackageName, 6)
            newQPackageObject = self.pm_ServerManagement.packagesDir.qpackageCreate(qpackageName, version, domain, qpackageObject.supportedPlatforms)
            self._copyMainDirs(qpackageDir, qpackagePath)
        else:
            self._copyMainDirs(qpackageDir, qpackagePath)

            newQPackageObject = QPackageObject(domain, qpackageName, version)

        newQPackageObject.buildNr[qualityLevel] = buildNr

        q.logger.log('Updating configuration for qpackage %s'%qpackageName, 6)
        newQPackageObject.dependencies = qpackageObject.dependencies
        newQPackageObject.updateConfig()

        newDir = q.system.fs.joinPaths(q.dirs.packageDir, newQPackageObject.getRelativeQPackagePath(), str(buildNr))
        if buildNr == 0:
            newDir = q.system.fs.joinPaths(q.dirs.packageDir, newQPackageObject.getRelativeQPackagePath(), '%s_%s'%(buildNr,qualityLevel ))
            if q.system.fs.exists(newDir):
                q.system.fs.removeDirTree(newDir)

        q.system.fs.moveDir(q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'write', 'qpackages', qpackageObject.getRelativeQPackagePath(), 'upload_%s'%qualityLevel), newDir)
        self.pm_ServerManagement.packagesDir.createVlists(domain, qualityLevel)
        self.auditingLogger.info('%s - Done successfully'%sessionId)

    def _getLatestVersionQPackageObject(self, qpackageName, domain, qualityLevel=None):
        """
        Retrieve a qpackage object with the latest version of a qpackage
        @param qpackageName: name of the qpackage
        @param domain: domain of the qpackage
        """
        q.logger.log('Getting the latest version of qpackage <%s>'%qpackageName, 6)
        result = self.pm_ServerManagement.packagesDir.qpackageFind(qpackageName, domain=domain, qualityLevels=[qualityLevel] if qualityLevel else None)
        if not result:
            raise RuntimeError('QPackage <%s> does not exist'%qpackageName)

        ##sort qpackages found to get latest qpackage
        result.sort(cmp=QPackageVersioning.versionCompare,key=lambda qpackageObject:qpackageObject.version)

        qpackageObject = result[len(result)-1]
        qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageObject.name, qpackageObject.version, qpackageObject.domain)
        self.auditingLogger.info('Done successfully')
        return qpackageObject

    def _getLatestBuildQPackageObject(self, qpackageObject, qualityLevel):
        """
        Retrieve the latest buildNr of a qpackageObject
        @param qpackageObject: qpackage object to retrieve latest buildNr for
        """
        q.logger.log('Getting the latest buildnr for qpackage <%s> of qualityLevel <%s> if exists'%(qpackageObject.name,qualityLevel), 6)
        if qualityLevel in qpackageObject.buildNr:
            self.auditingLogger.info('Done successfully')
            return qpackageObject.buildNr[qualityLevel]
        self.auditingLogger.info('Done successfully')
        return None

    def _pickleObject(self, objectToPickle):
        """
        Pickle the given object
        @param objectToPickle: given object to pickle
        """
        q.logger.log('Pickling a qpackageObject', 6)
        try:
            import cPickle as pickle
        except ImportError:
            import pickle
        self.auditingLogger.info('Done successfully')
        return pickle.dumps(objectToPickle)

    def _checkIfSessionIsValid(self, sessionId):
        q.logger.log('Validating session <%s>'%sessionId, 6)
        self.pm_ServerManagement.sessions.sessionUpdate(sessionId)
        if not self.pm_ServerManagement.sessions.sessionValidate(sessionId):
            raise RuntimeError('This session is no longer valid')
        self.auditingLogger.info('%s - Done successfully'%sessionId)

    def _checkIfQPackageExists(self, qpackageName, domain=None, version=None, qualityLevel=None, exists=True):
        """
        Check if QPackage exists in package Dir
        @param domain:         Domain in which the QPackage should be download from
        @param qpackageName:       Name of the qpackage to download
        @param version:        Version of the qpackage to download
        @param qualityLevel:   quality level of the QPackage to check
        @param exists:         if True will check if QPackage exists
        """
        q.logger.log('Check if QPackage <%s> exists'%qpackageName, 6)
        self.pm_ServerManagement.packagesDir.createVlists(domain, qualityLevel)
        self.pm_ServerManagement.packagesDir.vlists.loadVLists(domain, qualityLevel)

        qpackageExists = self.pm_ServerManagement.packagesDir.qpackageExists(qpackageName, version, domain, qualityLevels=None if not qualityLevel else [qualityLevel] if not isinstance(qualityLevel, list) else qualityLevel)
        if qpackageExists:
            if exists:
                self.auditingLogger.info('Done successfully')
                return True
            else:
                raise RuntimeError('QPackage<%s> already exists'%(qpackageName))
        else:
            if exists:
                raise RuntimeError('QPackage<%s> does not exist'%(qpackageName))
            else:
                self.auditingLogger.info('Done successfully')
                return True
        self.auditingLogger.info('Done successfully')
        return False

    def _checkIfServerIsAuthoritative(self, qpackageName, domain, version=None, qualityLevel=None, checkDomain=True, qpackageExists=True, createNewBuild=False):
        """
        Determines whether server is authoritative
        @param qpackageName: name of the QPackage
        @param domain: domain of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: quality level of the QPackage
        @param checkDomain: if True will check if QPackage exists on this domain
        @param qpackageExists: if True will check if QPackage exists
        @param createNewBuild: if True will create a new build of QPackage (if authoritative)
        """
        q.logger.log('Checking if domain <%s> is authoritative'%domain, 6)
        isAuthoritative = self._isDomainAuthoritative(domain)
        if isAuthoritative is None:
            raise ValueError('Failed to get authoritative value for domain %s. (Value should be 1 or 0)'%domain)

        if int(isAuthoritative) == 1:
            self._checkIfQPackageExists(qpackageName, domain if checkDomain else None, version, qualityLevel, exists=qpackageExists)
            buildNr = 1
            if createNewBuild:
                qpackageObject = self.pm_ServerManagement.packagesDir.qpackageGetObject(qpackageName, version, domain, qualityLevel)
                buildNr = int(self._getLatestBuildQPackageObject(qpackageObject, qualityLevel))+ 1
        else:
            self._checkIfQPackageExistsOnMaster(qpackageName, domain, version, qpackageExists=qpackageExists)
            buildNr = 0
        self.auditingLogger.info('Done successfully')

        return buildNr

    def _checkIfQPackageExistsOnMaster(self, qpackageName, domain, version, qualityLevels=None, qpackageExists=True):
        """
        Check if a QPackage exists on master repo
        @param qpackageName: name of the QPackage
        @param domain: domain of the QPackage
        @param version: version of the QPackage
        @param qpackageExists: if True will check if QPackage exists
        """
        q.logger.log('Loading (client) vlists of master repo', 6)
        self.pm_ServerManagement.vlists.loadVLists(domain)
        q.logger.log('Checking if QPackage %s exists'%qpackageName, 6)
        result = self.pm_ServerManagement.vlists.find(qpackageName, version=version, domain=domain, qualityLevels=qualityLevels)
        if result:
            if not qpackageExists:
                raise RuntimeError('QPackage <%s> already exists on master repo'%qpackageName)
        else:
            if qpackageExists:
                raise RuntimeError('QPackage <%s> does not exist on master repo'%qpackageName)
        self.auditingLogger.info('Done successfully')

    def _isDomainAuthoritative(self, domain):
        """
        Get Authoritative value of domain
        @param domain: name of the domain to check authoritative for
        """
        q.logger.log('Loading domain config file to check if server is authoritative', 6)
        iniFileLocation  = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', str(domain), 'domainconfig.cfg')

        if not q.system.fs.exists(iniFileLocation):
            raise IOError('File %s does not exists'%iniFileLocation)
        q.logger.log('Checking if domain <%s> is authoritative'%domain, 6)

        domainconfig = q.tools.inifile.open(iniFileLocation)

        isAuthoritative =domainconfig.getValue('main', 'authoritative')
        self.auditingLogger.info('Done successfully')
        return isAuthoritative

    def _createNewQPackageFromTemplate(self, sessionId, qpackageName, domain, version):
        """
        Create a new QPackage from template
        @param sessionId:      The client's authenticated session id.
        @param qpackageName:       Name of the qpackage to download
        @param domain:         Domain in which the QPackage should be download from
        @param version:        Version of the qpackage to download
        """
        templateQPackage = q.system.fs.joinPaths(q.dirs.packageDir, domain, 'template_qpackage')
        sessionDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'write')
        qpackagePath = q.system.fs.joinPaths(sessionDir, 'qpackages', domain, qpackageName)

        q.logger.log('Create qpackages directory in write module if it does not exist', 6)
        q.system.fs.createDir(q.system.fs.joinPaths(sessionDir, 'qpackages', domain))

        if q.system.fs.exists(templateQPackage):
            q.logger.log('Creating new qpackage <%s> based on template_qpackage'%qpackageName, 6)
            q.logger.log('Copying template_qpackage to new qpackage. <%s>'%qpackagePath, 6)
            q.system.fs.copyDirTree(templateQPackage, qpackagePath)
            q.logger.log('Moving qpackage version directory to the correct version <%s>'%version, 6)
            if q.system.fs.exists(q.system.fs.joinPaths(qpackagePath, '0.0')) and not q.system.fs.exists(q.system.fs.joinPaths(qpackagePath, version)):
                q.system.fs.moveDir(q.system.fs.joinPaths(qpackagePath, '0.0'), q.system.fs.joinPaths(qpackagePath, version))
        else:
            q.logger.log('Creating a new QPackage', 6)
            q.system.fs.createDir(q.system.fs.joinPaths(qpackagePath, version))
            q.system.fs.createDir(q.system.fs.joinPaths(qpackagePath, version, 'cfg' ))

        q.logger.log('Updating configuration file for the new qpackage <%s>' %qpackageName, 6)
        qpackageObject = QPackageObject(domain, qpackageName, version, rootPath=q.system.fs.joinPaths(sessionDir, 'qpackages'), new=True)
        self.auditingLogger.info('%s - Done successfully'%sessionId)

    def _createQPackageNew(self, sessionId, qpackageObject, version, qualityLevel, newVersion=True, copyDependencies=True,\
                       copySupportedPlatforms=True, copyDescription=True,copyTags=True, copyFiles=True):
        """
        Create a new QPackage version or build
        @param sessionId:      The client's authenticated session id.
        @param qpackageObject:     QPackageObject
        @param version:        Version of the qpackage to download
        @param qualityLevel:   quality level of the qpackage to create
        @param newVersion:     if True will create a new version
        """
        qpackageDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackageObject.getRelativeQPackagePath())
        sessionDir = q.system.fs.joinPaths(self.pm_ServerManagement.sessions.getSessionPath(sessionId), 'write')
        qpackagePath = q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageObject.getRelativeQPackagePath())
        if newVersion:
            qpackagePath = q.system.fs.joinPaths(sessionDir, 'qpackages', qpackageObject.domain.name, qpackageObject.name, version)

        q.logger.log('Create qpackages directory in write module if it does not exist', 6)
        q.system.fs.createDir(qpackagePath)

        self._copyMainDirs(qpackageDir, qpackagePath)

        latestBuildNr = self._getLatestBuildQPackageObject(qpackageObject, qualityLevel)
        if newVersion:
            if latestBuildNr >= 0 and copyFiles:
                q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackageDir, latestBuildNr if int(latestBuildNr) != 0 else '0_%s'%qualityLevel), q.system.fs.joinPaths(qpackagePath, 'upload_%s'%qualityLevel))
            else:
                q.system.fs.createDir(q.system.fs.joinPaths(qpackagePath, 'upload_%s'%qualityLevel))

            q.logger.log('Updating configuration file for the new qpackage <%s>' %qpackageObject.name, 6)
            newQPackageObject = QPackageObject(qpackageObject.domain.name, qpackageObject.name, version, rootPath=q.system.fs.joinPaths(sessionDir, 'qpackages'))
            newQPackageObject.buildNr = dict()
            newQPackageObject.tags = list()
            newQPackageObject.description = ""
            newQPackageObject.supportedPlatforms = list()
            newQPackageObject.dependencies = list()
            if copyTags:
                newQPackageObject.tags = qpackageObject.tags
            if copyDescription:
                newQPackageObject.description = qpackageObject.description
            if copySupportedPlatforms:
                newQPackageObject.supportedPlatforms = qpackageObject.supportedPlatforms
            if copyDependencies:
                newQPackageObject.dependencies = qpackageObject.dependencies

            newQPackageObject.updateConfig()

        else:
            if latestBuildNr is None:
                raise RuntimeError('QPackage <%s> does not have a build on quality level <%s> on domain <%s>'%(qpackageObject.name, qualityLevel, qpackageObject.domain))
            q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackageDir, latestBuildNr if int(latestBuildNr) != 0 else '0_%s'%qualityLevel), q.system.fs.joinPaths(qpackagePath, 'upload_%s'%qualityLevel))
        self.auditingLogger.info('%s - Done successfully'%sessionId)

    def _copyMainDirs(self, qpackageDir, qpackagePath):
        """
        Copies main QPackage directories e.g. cfg, installer, license
        @param qpackageDir: original location of QPackage to copy from
        @param qpackagePath: new QPackage path to copy to
        """
        q.logger.log('Copying qpackage files to <%s>'%qpackagePath, 6)
        q.system.fs.copyDirTree(q.system.fs.joinPaths(qpackageDir, 'cfg'), q.system.fs.joinPaths(qpackagePath, 'cfg'))
        installerDir = q.system.fs.joinPaths(qpackageDir, 'installer')
        if q.system.fs.exists(installerDir):
            q.system.fs.copyDirTree(installerDir, q.system.fs.joinPaths(qpackagePath, 'installer'))
        licenseDir = q.system.fs.joinPaths(qpackageDir,'LICENSES')
        if q.system.fs.exists(licenseDir):
            q.system.fs.copyDirTree(licenseDir, q.system.fs.joinPaths(qpackagePath,'LICENSES'))
        self.auditingLogger.info('Done successfully')


    def runTasklets(self, tags, params):
        '''Execute a tasklet run to provide hooks in the QPackage server

        @param tags: Set of tags to pass to the tasklet engine
                     This set is extended with a set of standard tags
        @type tags: iterable
        @param params: Dict of params to pass to tasklets
                       Some more parameters are calculated based on these values
                       and passed to tasklets as well
        '''
        # Calculate final set of tags
        final_tags = ['qpackages', 'server']
        final_tags.extend(tags)
        final_tags = tuple(set(final_tags))

        final_params = params.copy()

        domain = params['domain']
        name = params['name']
        version = params['version']
        build = str(params['build'])
        qualitylevel = params['qualitylevel']

        # Retrieve and pass session data
        session = final_params.pop('session', None)
        if session is not None:
            if 'remote_ip' in final_params or 'username' in final_params:
                raise RuntimeError(
                    'Invalid key found in params passed to runTasklets')

            session = self.pm_ServerManagement.sessions.sessions[session]
            username = session.login
            ip = session.ipAddress

            final_params['username'] = username
            final_params['remote_ip'] = ip

        # Figure out on-disk path of package files
        if build != 0:
            build_folder = str(build)
        else:
            build_folder = '%s_%s' % (build, qualitylevel)

        container = pylabs.q.system.fs.joinPaths(q.dirs.packageDir, domain,
                                                   name, version, build_folder)

        final_params['path'] = container

        # Call tasklets
        pylabs.q.logger.log('Executing tasklets for package %s %s '
                              'build %s' % (name, version, build, ))
        self._taskletEngine.execute(params=final_params, tags=final_tags)