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
from pymonkey.baseclasses import BaseType
from pymonkey.sync.Sync import SyncFromServer, SyncToServer
import xmlrpclib
import exceptions

QPACKAGESERVER_ENDPOINT = 'qpackageserver'
QPACKAGESERVER_PORT     = 8088

class QPackageServerSideException(exceptions.Exception):
    def __init__(self, msg):
        msg = self.handleException(msg)
        self.errmsg = msg
        self.args=(msg, )

    def handleException(self, error):
        """
        Handle error message thrown. Parses the error msg
        to retrieve the relevant error message
        @param error: the error message thrown by the server
        """
        msg = error
        if hasattr(error, 'faultString'):
            msg = error.faultString
            if len(msg) > 100:
                msg = msg[:100]
                if msg.split('||') >= 1:
                    msg = msg.split('||')[0]

        return msg
    
class QPackageClient(BaseType):
    """
    Client for the qpackage server. (XMLRPC + RSYNC)
    Handles all communication with a qpackage repo server.

    Contains wrappers for all methods exposed on the qpackage server and helper
    methods for uploading/downloading files to and from the server.

    This class is not exposed to the interface (qshell)
    """

    host = q.basetype.string(doc='Host / IPAddress of the QPackage server', allow_none=False)
    port = q.basetype.integer(doc='Name of the QPackage should be lowercase', allow_none=False)
    server = q.basetype.object(xmlrpclib.ServerProxy, doc='Name of the QPackage should be lowercase', allow_none=False)

    ####################################
    ## QPackageServer exposed methods ##
    ####################################
    def __init__(self, host, port=QPACKAGESERVER_PORT):
        self.host = host
        self.port = port
        self.server = xmlrpclib.ServerProxy('http://%s:%s/'%(self.host, self.port))

    #############################
    ## QPackage XMLRPC calls   ##
    #############################

    def connect(self, login, password):
        ''' Initialize the connection to the server, this means that a session is initialized on the serverside.
        Then a sessionId is returned by the server and is returned to the caller.

        @param login: login used to connect to the server
        @param password: password used to connect to the server
        @return: sessionId received by the server
        '''
        q.logger.log('calling the XMLRPC sessionLogin method', 8)
        sessionId = None
        try:
            sessionId = self.server.qpackageserver.sessionLogin(login, password)
        except Exception, e:
            raise QPackageServerSideException(e)
        if sessionId:
            q.logger.log('successfully called the XMLRPC sessionLogin method', 8)
        return sessionId

    def getDomainsServed(self, sessionId):
        """
        Request the domains server by QPackage Server
        @param sessionId: the sessionId used to identify the session.
        """
        q.logger.log('calling the XMLRPC listDomains method', 8)
        try:
            domainsList = self.server.qpackageserver.listDomains(sessionId)
            return domainsList

        except Exception, e:
            raise QPackageServerSideException(e)
        q.logger.log('successfully called the XMLRPC listDomains method', 8)    

    def disconnect(self, sessionId):
        ''' invalidate the connection to the server

        @param sessionId: the sessionId used to identify the session.
        '''
        q.logger.log('calling the XMLRPC sessionLogout method', 8)
        try:
            self.server.qpackageserver.sessionLogout(sessionId)
        except Exception, e:
            raise QPackageServerSideException(e)
        q.logger.log('successfully called the XMLRPC sessionLogout method', 8)

    def isConnected(self, sessionId):
        ''' check whether the session is still valid.

        @param sessionId: sessionId used to identify the session
        '''
        q.logger.log('calling the XMLRPC sessionValidate method', 8)
        #try:
        if self.server.qpackageserver.sessionValidate(sessionId):
            q.logger.log('successfully called the sessionValidate method', 8)
            return True
        else:
            q.logger.log('unsuccessfully called the sessionValidate method',8)
            return False
        #except Exception, e:
        #    raise QPackageServerSideException(e)

    def prepareDownload(self, sessionId, domain, name, version, qualityLevel):
        ''' Prepare for download a QPackage

        @param sessionId: sessionId to identify the session
        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel you wish to download
        @return: QPackageObject received by the server.
        '''
        q.logger.log('calling the XMLRPC qpackageDownload method',8)
        try:
            import cPickle as pickle
        except ImportError:
            import pickle

        pickledObj = None
        try:
            pickledObj = self.server.qpackageserver.qpackageDownload(sessionId, domain, name, version, str(qualityLevel))
        except Exception, e:
            raise QPackageServerSideException(e)

        qpackage = pickle.loads(pickledObj) if pickledObj else None

        q.logger.log('successfully called the XMLRPC qpackageDownload method',8)
        return qpackage

    def downloadSynced(self, sessionId, domain, name, version, qualityLevel):
        ''' Finish download  of a QPackage

        @param sessionId: sessionId to identify the session
        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel of the QPackage
        '''
        q.logger.log('calling the XMLRPC qpackageDownloadSynced', 8)
        try:
            if not self.server.qpackageserver.qpackageDownloadSynced(sessionId, domain, name, version, str(qualityLevel)):
                q.logger.log('unsuccessfully called the XMRPC qpackageDownloadSynced', 8)
                raise RuntimeError('XMLRPC call <qpackageDownloadSynced> failed')
        except Exception, e:
            raise QPackageServerSideException(e)
        q.logger.log('successfuly called the XMLRPC qpackageDownloadSynced', 8)

    def createNewQPackage(self, sessionId, domain, name, version, qualityLevel='trunk'):
        ''' Create a new QPackage
        @param sessionId: sessionId to identify the session
        @param domain: domain where you wish to create the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel of the QPackage
        '''
        q.logger.log('calling the XMLRPC qpackageCreateNew', 8)
        try:
            if self.server.qpackageserver.qpackageCreateNew(sessionId, domain, name, version, str(qualityLevel)):
                q.logger.log('successfuly called the XMLRPC qpackageCreateNew', 8)
                return True

        except Exception, e:
            raise QPackageServerSideException(e)

        q.logger.log('unsuccessfuly called the XMLRPC qpackageCreateNew', 8)
        return False

    def createNewQPackageVersion(self, sessionId, domain, name, version, qualityLevel='trunk', copyDependencies=True,\
                             copySupportedPlatforms=True, copyDescription=True, copyTags=True, copyFiles=True):
        ''' Create a new QPackage version
        @param sessionId: sessionId to identify the session
        @param domain: domain where you wish to create the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: quality level of the QPackage
        @param copyDependencies       :copy the dependencies of the QPackage
        @param copySupportedPlatforms :copy the supported platforms of the QPackage
        @param copyDescription        :copy description of the QPackage
        @param copyTags               :copy tags of the QPackage
        @param copyFiles              :copy files of the QPackage
        '''
        q.logger.log('calling the XMLRPC qpackageCreateNewVersion', 8)
        try:
            if self.server.qpackageserver.qpackageCreateNewVersion(sessionId, domain, name, version, str(qualityLevel),\
                                                           copyDependencies, copySupportedPlatforms, copyDescription,\
                                                           copyTags, copyFiles):
                q.logger.log('successfuly called the XMLRPC qpackageCreateNewVersion', 8)
                return True
        except Exception, e:
            raise QPackageServerSideException(e)

        q.logger.log('unsuccessfuly called the XMLRPC qpackageCreateNewVersion', 8)
        return False

    def createNewQPackageBuild(self, sessionId, domain, name, version, qualityLevel):
        ''' Create a new QPackage version
        @param sessionId: sessionId to identify the session
        @param domain: domain where you wish to create the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel for the new build
        '''
        q.logger.log('calling the XMLRPC qpackageCreateNewBuild', 8)
        try:
            if self.server.qpackageserver.qpackageCreateNewBuild(sessionId, domain, name, version, str(qualityLevel)):
                q.logger.log('successfuly called the XMLRPC qpackageCreateNewBuild', 8)
                return True
        except Exception, e:
            raise QPackageServerSideException(e)

        q.logger.log('unsuccessfuly called the XMLRPC qpackageCreateNewBuild', 8)
        return False

    def promoteQPackageToMaster(self, sessionId, domain, name, version, qualityLevel, domainLogin, domainPasswd):
        """
        Promote QPackage to Master Repo
        @param sessionId: id of the session
        @param domain: domain where you wish to create the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel for the new build
        @param domainLogin:    The user's login for the given domain
        @param domainPasswd: The user's password for the given domain
        """
        try:
            if self.server.qpackageserver.qpackagePromoteLocalToMaster(sessionId, domain, name, version, domainLogin, domainPasswd, qualityLevel):
                q.logger.log('QPackage %s promoted successfully to master repo'%name, 8)
                return True
        except Exception, e:
            raise QPackageServerSideException(e)
        q.logger.log('Failed to promote QPackage %s to master repo'%name, 8)

        return False

    def promoteQPackage(self, sessionId, domain, name, version, buildNr, destQualityLevels, domainLogin, domainPassword):
        """
        Promote a QPackage to a higher qualityLevel on the server.

        @param sessionId:            The client's authenticated session id.
        @param domain:               Domain of the QPackage
        @param name:                 Name of the QPackage
        @param version:              Version of the QPackage 
        @param buildNr:              buildNr you wish to promote
        @param destQualityLevels:    List of qualityLevels to where you wish to promote
        @param domainLogin:          The user's login for the given domain
        @param domainPassword:       The user's password for the given domain
        """
        q.logger.log('Calling XMLRPC qpackagePromote', 8)
        try:
            if self.server.qpackageserver.qpackagePromote(sessionId, domain, name, version, buildNr, destQualityLevels, domainLogin, domainPassword):
                return True
        except Exception, e:
            raise QPackageServerSideException(e)

        q.logger.log('Failed to promote QPackage %s'%name, 8)

        return False

    def createNewQPackageSynced(self, sessionId, domain, name, version, qualityLevel='trunk'):
        ''' Finish upload  of a QPackage

        @param sessionId: sessionId to identify the session
        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel of the QPackage
        '''
        q.logger.log('calling the XMLRPC qpackageCreateNewSynced', 8)
        retval = None
        try:
            retval =  self.server.qpackageserver.qpackageCreateNewSynced(sessionId, domain, name, version, str(qualityLevel))
        except Exception, e:
            raise QPackageServerSideException(e)

        q.logger.log('successfuly called the XMLRPC qpackageCreateNewSynced', 8)
        return retval

    def createNewQPackageVersionSynced(self, sessionId, domain, name, version, qualityLevel='trunk'):
        ''' Finish upload  of a QPackage
        @param sessionId: sessionId to identify the session
        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel of the QPackage
        '''
        q.logger.log('calling the XMLRPC qpackageCreateNewVersionSynced', 8)
        retval = None
        try:
            retval =  self.server.qpackageserver.qpackageCreateNewVersionSynced(sessionId, domain, name, version, str(qualityLevel))
        except Exception, e:
            raise QPackageServerSideException(e)

        q.logger.log('successfuly called the XMLRPC qpackageCreateNewVersionSynced', 8)
        return retval

    def createNewQPackageBuildSynced(self, sessionId, domain, name, version, qualityLevel):
        ''' Finish upload  of a QPackage

        @param sessionId: sessionId to identify the session
        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: qualityLevel of the QPackage
        '''
        q.logger.log('calling the XMLRPC qpackageCreateNewBuildSynced', 8)
        retval = None
        try:
            retval = self.server.qpackageserver.qpackageCreateNewBuildSynced(sessionId, domain, name, version, str(qualityLevel))
        except Exception, e:
            raise QPackageServerSideException(e)
        q.logger.log('successfuly called the XMLRPC qpackageCreateNewBuildSynced', 8)
        return retval

    def qpackageGetObject(self, sessionId, domain, name, version):
        ''' Returns the QPackageObject for the requested QPackage

        @param sessionId: sessionId to identify the session
        @param domain: domain of the QPackage
        @param name: name of the QPackage
        @param version: version of the QPackage
        '''
        q.logger.log('requesting QPackageObject for QPackage %s, version %s'%(name, version), 8)
        qpackageObject = None
        try:
            qpackageObject = self.server.qpackageserver.qpackageGetObject(sessionId, domain, name, version)
        except Exception, e:
            raise QPackageServerSideException(e)
        return qpackagepObject

    def delete(self, sessionId, domain, name, version, domainLogin, domainPasswd, fromMaster):
        '''Delete the QPackage on the server(s).

        @param sessionId: sessionId to identify the session
        @param domain:              string representation of the domain
        @param name:                name of the QPackage
        @param version:             version of the QPackage
        @param qualityLevels:       list of qualityLevels to delete (if none then remove the QPackage completely)
        @param fromMaster:          if True the QPackage will be deleted from the master server.
        @param domainLogin:    The user's login for the given domain
        @param domainPasswd: The user's password for the given domain
        '''
        q.logger.log('asking server to delete QPackage %s with version %s'%(name, version), 8)
        retval = None
        try:
            retval = self.server.qpackageserver.qpackageDelete(sessionId, domain, name, version, domainLogin, domainPasswd, fromMaster)
        except Exception, e:
            raise QPackageServerSideException(e)
        return retval

    #############################
    ## QPackage rsync methods  ##
    #############################

    def syncFolderFromServer(self, source, destination, module):
        ''' method to help downloading the folders of the QPackage

        @param source: relative path on the server of the QPackage you wish to download (without the supportedPlatform!)
        @param destination: absolute path to where you wish to download the folder
        @param module: module where you need to download from (format: sessionId_{read,write}
        '''
        q.logger.log('started sync from %s:%s to %s'%(self.host, source, destination), 9)
        syncer = SyncFromServer(self.host, module, 873)
        syncer.setSourceDir(source)
        syncer.setDestinationDir(destination)
        syncer.enableDelete()
        syncer.enableSkipBasedOnCRC()
        syncer.disableKeepPermissionsOwnerGroup()
        syncer.do()
        syncer.clearFilters()
        q.logger.log('synced from %s:%s to %s'%(self.host, source, destination), 9)

    def syncFolderToServer(self, source, destination, module):
        ''' method to help uploading the folders of the QPackage

        @param source: relative path on the server of the QPackage you wish to download (without the supportedPlatform!)
        @param destination: absolute path to where you wish to download the folder
        @param module: module where you need to sync to(format: sessionId_{read,write}
        '''
        q.logger.log('started sync from %s:%s to %s'%(self.host, source, destination), 9)
        syncer = SyncToServer(self.host, module, 873)
        syncer.setSourceDir(source)
        syncer.setDestinationDir(destination)
        syncer.enableDelete()
        syncer.enableSkipBasedOnCRC()
        syncer.disableKeepPermissionsOwnerGroup()
        syncer.do()
        q.logger.log('synced from %s:%s to %s'%(self.host, source, destination), 9)

    def getRemoteDirs(self, remoteDir, module):
        """
        Retrieves all subDirs from the path on the server.
        @param remoteDir: path from which you wish to see the dirs
        @param module: rsync module where you want to list dirs from (format: sessionId_{read,write}
        """
        syncer = SyncFromServer(self.host, module, 873)
        return syncer.dir(remoteDir, listSymlinks=True)

    def getVLists(self, sessionId, domains):
        ''' 
        Get the Vlists form the connection
        @param sessionId: id of the session to identify rsync module
        @param domains: list of domains to get vlists for
        '''
        if not domains is None:
            if not isinstance(domains, list):
                domains = str(domains).split(',')
            q.logger.log('Retrieving VLists from server for domains: %s' %domains, 6)
            for domain in domains:
                domainVlists = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageclient', 'vlists')
                if not q.system.fs.exists(domainVlists):
                    q.system.fs.createDir(domainVlists)
                self._syncVlists(sessionId, 'vlists/%s'%domain, domainVlists)

    def _syncVlists(self, sessionId, source, destination):
        """
        Sync VLists from server
        @param sessionId: id of the session to identify rsync module
        @param source: source dir on the server
        @param destination: location to sync vlist to
        """
        syncer = SyncFromServer(self.host, '%s_read'%sessionId, 873)
        syncer.setSourceDir(source)
        syncer.setDestinationDir(destination)
        syncer.enableSkipBasedOnCRC()
        syncer.do()