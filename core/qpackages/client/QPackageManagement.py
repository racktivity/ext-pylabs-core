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

from pylabs import q,i
from pylabs.baseclasses import BaseType
from pylabs.enumerators.PlatformType import PlatformType

from pylabs.qpackages.client.QPackageDomain import QPackageDomains
from pylabs.qpackages.client.QPackageServerConnection import QPackageServerConnection, QPackageServerConnections
from pylabs.qpackages.common.QPackagePackagesDir import QPackagePackagesDir
from pylabs.qpackages.common.VLists import VLists
from pylabs.qpackages.common.QPackageObject import QPackageObject
from pylabs.qpackages.common.DomainObject import DomainObject
from pylabs.qpackages.common.enumerators import VListType
from pylabs.qpackages.common.QPackageDependencyHelper import QPackageDependencyHelper
from pylabs.qpackages.client.QPackageBuilder import QPackageBuilder
from pylabs.qpackages.client.QPackage import QPackage
from pylabs.qpackages.common.QPackageVersioning import QPackageVersioning

class QPackageManagement(BaseType):
    """
    User interface to a QPackage management mounted on q (q.qpackages) which
    connects all different components (PackageManager, QPackageClient, QPackageInstaller, QPackageBuilder)

    """
    qpackageServerConnections = q.basetype.object(QPackageServerConnections, doc="List of known repositories", allow_none=True, default=QPackageServerConnections())
    qpackageDomains           = q.basetype.object(QPackageDomains, doc='List of known domains', allow_none=False, default=QPackageDomains())
    qpackagePackagesDir       = q.basetype.object(QPackagePackagesDir,doc='QPackagePackagesDir', default=QPackagePackagesDir())
    vlists                = q.basetype.object(VLists, doc='The Vlists for the client', default=VLists(VListType.CLIENT))

    def __init__(self):
        """
        Initializes all properties (get sessions to all servers, lists domains)
        """
        q.logger.log('Initializing QPackageManagement', 5)

    def updateQPackageList(self):
        """
        Get and Load latest vlists
        """
        self.qpackageServerConnections.refresh()
        for connection in q.qpackages.qpackageServerConnections:
            try:
                if not connection.isConnected():
                    connection.connect()
                connection.getVLists(connection.domains)
            except Exception, e:
                q.eventhandler.raiseWarning("Failed to update qpackagelist for"
                "connection [%s] of repo [%s]\nError: %s"
                % (connection.name, connection.host, e))

        self.vlists.loadVLists()

    def listAllDomains(self):
        """
        Returns a list of all domains configured for all connections
        """
        listOfDomains = list()
        for serverConnection in self.qpackageServerConnections:
            for domain in serverConnection.domains:
                listOfDomains.append(domain)
        return listOfDomains

    def setQualityLevel(self, defaultQualityLevel="trunk"):
        """
        Set the default qualityLevel
        @param defaultQualityLevel: default quality level to set
        """
        q.qshellconfig.loadConfigFile('qpackageconfig')
        q.qshellconfig.qpackageconfig.setParam('main', 'defaultqualitylevel', defaultQualityLevel)

    def getDefaultQualityLevel(self):
        ''' Returns the qualityLevel for the environment.'''
        q.qshellconfig.loadConfigFile('qpackageconfig')
        return q.qshellconfig.qpackageconfig.getParam('main', 'defaultqualitylevel', defaultValue=None, forceDefaultValue=True)

    def _getDependenciesForInstalledQPackages(self, installedQPackages):
        """
        Calculates all runtime dependencies for installed qpackages
        @param installQPackages: dict of installedQPackage {domain: listOfQPackage}
        """
        dependencyList = list()
        for domain in installedQPackages.iterkeys():
            for qpackageInfo in installedQPackages[domain]:
                qpackage = self.qpackagePackagesDir.qpackageGetObject(name=qpackageInfo[0], version=qpackageInfo[1],domain=domain)
                if qpackage.getRuntimeDependencies(str(q.platform)):
                    dependencyList.extend(qpackage.getRuntimeDependencies())
        return dependencyList

    def updateAllQPackages(self):
        """
        Update all QPackages. Installs the latest for installed QPackages
        """
        failedUpdates = list()
        installedQPackages = self.listInstalledQPackages()
        dependencyList = self._getDependenciesForInstalledQPackages(installedQPackages)
        for domain in installedQPackages.iterkeys():
            for qpackageInfo in installedQPackages[domain]:
                qpackage = self.qpackageFindFirst(name=qpackageInfo[0], version=qpackageInfo[1], domain=domain, qualityLevels=self.getDefaultQualityLevel(),state='server')
                if not qpackage:
                    q.console.echo('Failed to find qpackage (%s,%s,%s)'%(qpackageInfo[0], qpackageInfo[1], domain))
                    continue
                ##only update a qpackage if it is not in the list of calculated dependencies,
                ##to avoid processing a qpackage multiple times
                if not any([dependency.name == qpackage.name for dependency in dependencyList]):
                    try:
                        qpackage.install()
                    except Exception, ex:
                        import traceback
                        q.logger.log('Failed to install QPackage %s. Exception: %s'%(qpackageInfo[0], traceback.format_exc()), 6)
                        q.console.echo(ex)
                        failedUpdates.append(qpackage)

        if failedUpdates:
            raise RuntimeError('Failed to update the following QPackages: %s' % ', '.join([qpackage.name for qpackages in failedUpdates]))

    def listInstalledQPackages(self):
        """
        List installed QPackages
        """
        q.logger.log('Listing Installed QPackages', 6)
        dictOfInstalledQPackages = dict()
        qpackageCfgDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages')
        if not q.system.fs.exists(qpackageCfgDir):
            q.logger.log('QPackages cfg directory does not exists. No QPackages installed', 6)
            return dictOfInstalledQPackages
        for domainDir in q.system.fs.listDirsInDir(qpackageCfgDir):
            domain = q.system.fs.getBaseName(domainDir)
            listOfInstalledQPackages = list()
            for qpackageDir in q.system.fs.listDirsInDir(domainDir):
                qpackageName = q.system.fs.getBaseName(qpackageDir)
                for version in self.qpackageGetInstalledVersions(qpackageName, domain):
                    listOfInstalledQPackages.append([qpackageName, version])
            dictOfInstalledQPackages[domain] = listOfInstalledQPackages
        return dictOfInstalledQPackages

    def qpackageGetInstalledVersions(self, name, domain):
        """
        Retrieves the list of installed version(s) of a QPackage
        @param name: name of the QPackage to check
        @param domain: domain of the QPackage to check
        """
        qpackageCfgDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages')
        if not q.system.fs.exists(qpackageCfgDir):
            q.logger.log('QPackages cfg directory does not exists. No QPackages installed', 6)
            return
        domainDir = q.system.fs.joinPaths(qpackageCfgDir, domain)
        if not domainDir in q.system.fs.listDirsInDir(qpackageCfgDir):
            return
        qpackageDir = q.system.fs.joinPaths(domainDir, name)
        if not qpackageDir in q.system.fs.listDirsInDir(domainDir):
            return
        return [q.system.fs.getBaseName(versionDir) for versionDir in q.system.fs.listDirsInDir(qpackageDir)]

    def qpackageIsInstalled(self, name, version, domain):
        """
        Check if QPackage is installed
        @param name: name of the QPackage to check
        @param version: version of the QPackage to check
        @param domain: domain of the QPackage to check
        @param qualityLevel: qualityLevel of the QPackage to check
        """
        if not self.qpackageGetInstalledBuildNr(name, version, domain) is None:
            return True
        return False

    def qpackageGetInstalledBuildNr(self, name, version, domain):
        """
        Get the buildNr of the QPackage currently installed
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        """
        qpackageInfo = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages', str(domain), name, version, 'qpackageinfo.cfg')
        if not q.system.fs.exists(qpackageInfo):
            return None
        iniFile = q.tools.inifile.open(qpackageInfo)

        return iniFile.getValue('main', 'buildnr')

    def qpackageBuild(self, name, version, domain=None, qualityLevel='trunk'):
        """
        Prepare a QPackage for a new build and checks if all build dependencies
        are installed.
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: quality level of the qpackage
        """
        if not qualityLevel:
            qualityLevel = self.getDefaultQualityLevel()
        try:
            ##try to call create new build which creates the required directories
            ##incase this is a new qpackage or a new version of a qpackage this call will fail as the
            ##directories already exists
            self.qpackagePrepare(name, version, qualityLevel, domain)

        except Exception, e:
            q.logger.log('Failed to create New Build', 7)
            pass
        try:
            ##try to retrieve the qpackage object, if this fails then we throw an exception. As this means
            ##that the qpackage doesnt exist in the packageDir
            q.logger.log('Retrieving QPackage <%s> Object'%name, 6)
            qpackageObject = self.qpackagePackagesDir.qpackageGetObject(name, version, domain, qualityLevel)

        except Exception, ex:
            q.logger.log('Failed to retrieve QPackageObject for %s' %str(self), 7)
            raise RuntimeError(e)

        self.qpackagePackagesDir.vlists.loadVLists()
        q.logger.log('Checking for build dependencies', 7)
        for dep in qpackageObject.getBuildDependencies():
            depQPackageObject = QPackageDependencyHelper().getMostApplicableQPackage(dep, q.platform)
            if not self.qpackagePackagesDir.qpackageExists(depQPackageObject.qpackageName, depQPackageObject.version, depQPackageObject.domain):
                raise RuntimeError('Please download build dependency <%s>'%depQPackageObject.qpackageName)
            if not self.qpackageIsInstalled(depQPackageObject.qpackageName, depQPackageObject.version, depQPackageObject.domain):
                raise RuntimeError('Please install build dependency <%s>'%depQPackageObject.qpackageName)

    def qpackageFind(self,name=None,version=None,domain=None,qualityLevels="",supportedPlatforms="",tags="",buildNr="", description="", state=None,exactMatch=True):
        """
        Search a QPackage on the server.
        @param name: name of the QPackage you are searching for
        @param version: version of the QPackage you are searching for
        @param domain: domain you wish to search
        @param qualityLevel is comma separated list of quality levels (short notation) or array of qualityleveltypes
        @param supportedPlatforms: list of supported platforms you are searching in
        @param tags: is comma separated list of tags
        @param buildNr: build number you are searching for
        @param state: state of the qpackage to search for (SERVER,LOCAL,NEW,MOD)
        @param exactMatch: flag to search for an exact match for given qpackage name
        """
        qpackagesList = list()
        if not str(state).upper() in ('LOCAL', 'MOD', 'NEW'):
            q.logger.log('Searching for a QPackage in client vlists', 6)
            listOfQPackages = self.vlists.find(name,version=version, domain=domain, qualityLevels=qualityLevels, supportedPlatforms=supportedPlatforms, tags=tags, buildNr=buildNr, description=description, exactMatch=exactMatch)
            for qpackage in listOfQPackages:
                if qpackage.qpackageName == 'template_qpackage':
                    continue
                qPackage = QPackage(qpackage.domain, qpackage.qpackageName, qpackage.version)
                qPackage.tags = qpackage.tags
                qPackage.description = qpackage.description
                qPackage.supportedPlatforms = qpackage.supportedPlatforms
                qPackage.qualityLevel = qpackage.qualityLevel
                qPackage.buildNr = str(qpackage.buildNr)
                qPackage.state = 'SERVER'
                qpackagesList.append(qPackage)
            q.logger.log('Done searching for a QPackage in client vlists', 6)

            if str(state).upper() == 'SERVER':
                qpackagesList.sort(key=lambda qpackage:qpackage.name)
                return qpackagesList

        self.qpackagePackagesDir.vlists.createVLists(domain, qualityLevels)
        self.qpackagePackagesDir.vlists.loadVLists(domain, qualityLevels)

        if str(state).upper() == 'MOD' or str(state).upper() == 'NEW':
            buildNr = state

        localQPackages = self._qpackageFindLocal(name, version=version, domain=domain, qualityLevels=qualityLevels, supportedPlatforms=supportedPlatforms, tags=tags, buildNr=buildNr, description=description, exactMatch=exactMatch)
        if str(state).upper() == 'LOCAL' or str(state).upper() =='MOD' or str(state).upper() =='NEW':
            localQPackages.sort(key=lambda qpackage:qpackage.name)
            return localQPackages

        qpackages = list(localQPackages)

        for qpackage in qpackagesList:
            if qpackage.buildNr == 'NEW':
                continue
            ##compare qpackages (server) with qpackages (local), and only add qpackage(server) if it is same version but newer buildNr, or different version
            if not any([local.name == qpackage.name and not str(local.state).lower() == 'server' and local.domain == qpackage.domain and (not QPackageVersioning.versionCompare(qpackage.version, local.version) and str(qpackage.qualityLevel) == str(local.qualityLevel) and int(qpackage.buildNr) == int(QPackageObject(local.domain, local.name, local.version).buildNr[local.qualityLevel])) for local in qpackages]):
                qpackages.append(qpackage)

        qpackages.sort(key=lambda qpackage:qpackage.name)
        return qpackages

    def qpackageFindFirst(self, name=None,version=None,domain=None,qualityLevels="",supportedPlatforms="",tags="",buildNr="", description="", state=None,exactMatch=True):
        """
        Searches for a QPackage on the server and returns the first QPackage found
        @param name: name of the QPackage you are searching for
        @param version: version of the QPackage you are searching for
        @param domain: domain you wish to search
        @param qualityLevel: comma separated list of quality levels (short notation) or array of qualityleveltypes
        @param supportedPlatforms: list of supported platforms you are searching in
        @param tags: comma separated list of tags
        @param buildNr: build number you are searching for
        @param state: state of the qpackage to search for (SERVER,LOCAL,NEW,MOD)
        @param exactMatch: flag to search for an exact match for given qpackage name
        """
        q.logger.log('Searching for a first match QPackage in client vlists', 6)
        listOfQPackages = self.qpackageFind(name, version, domain, qualityLevels, supportedPlatforms, tags, buildNr, description, state=state, exactMatch=exactMatch)
        if len(listOfQPackages) >= 1:
            q.logger.log('Found QPackage with given criteria', 6)
            return listOfQPackages[0]

    def _qpackageFindLocal(self, name=None, version=None, domain=None, qualityLevels="", supportedPlatforms="", tags="", buildNr="", description="", exactMatch=True):
        """
        Searches for a QPackage locally
        @param name: name of the QPackage you are searching for
        @param version: version of the QPackage you are searching for
        @param domain: domain you wish to search
        @param qualityLevel is comma separated list of quality levels (short notation) or array of qualityleveltypes
        @param supportedPlatforms: list of supported platforms you are searching in
        @param tags: is comma separated list of tags
        @param buildNr: build number you are searching for
        @param exactMatch: flag to search for an exact match for given qpackage name
        """
        qpackages = list()
        qpackages = self.qpackagePackagesDir.qpackageFind(name, version, domain, qualityLevels, supportedPlatforms, tags, buildNr, exactMatch=exactMatch)

        qpackagesList = list()

        for qpackage in qpackages:
            qPackage = QPackage(qpackage.domain, qpackage.name, qpackage.version)
            qPackage.tags = qpackage.tags
            qPackage.supportedPlatforms = qpackage.supportedPlatforms
            qPackage.description = qpackage.description
            qPackage.qualityLevel = str(qpackage.buildNr.keys()[0])
            if qpackage.buildNr.values()[0] == 'NEW' or qpackage.buildNr.values()[0]  == 'MOD':
                qPackage.state = str(q.enumerators.QPackageState.getByName(str(qpackage.buildNr.values()[0]).upper()))
                qPackage.buildNr = 'upload_%s'%str(qPackage.qualityLevel)
            else:
                qPackage.buildNr = qpackage.buildNr.values()[0]
                qPackage.state = 'LOCAL'

            qpackagesList.append(qPackage)
        qpackagesList.sort(key=lambda qpackage:qpackage.name)
        return qpackagesList

    def qpackageFindInDevelopmentMode(self, name="", version="", domain=""):
        """
        Find one or more qpackage in development mode
        param name: name of the QPackage you are searching for
        @param version: version of the QPackage you are searching for
        @param domain: domain you wish to search
        """
        qpackagesInDevMode = list()
        qpackagesInDevModeList = list()
        if not name and not domain and not version:
            qpackagesInDevMode = i.qpackageLocalConfig.listQPackagesInDevMode()
        else:
            if i.qpackageLocalConfig.isQPackageInDevMode(domain, name, version):
                qpackagesInDevMode.append((domain, name, version))

        for qpackage in qpackagesInDevMode:
            qpackagesList = self.qpackageFind(domain=qpackage[0], name=qpackage[1], version=qpackage[2], state='local')

            qpackagesInDevModeList.extend(qpackagesList)

        return qpackagesInDevModeList

    def qpackageExists(self,name,version=None,domain="",qualityLevels="",buildNr="",supportedPlatforms="", state='SERVER'):
        ''' Check whether QPackage exists on server

        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain where the QPackage is defined
        @param qualityLevels: list of qualityLevels where you should check
        @param buildNr: Number of the build
        @supportedPlatforms: list of supported platforms
        '''
        result = self.qpackageFind(name,version=version, domain=domain, qualityLevels=qualityLevels, supportedPlatforms=supportedPlatforms, buildNr=buildNr, state=state)
        if result:
            return True
        else:
            return False

    def qpackageDownload(self,name,version,domain="",qualityLevels="",supportedPlatforms=""):
        """ Download a QPackage

        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevels: list of qualityLevels you wish to download
        @param supportedPlatforms: list of platforms you wish to download, you can also specify the string ALL to download them all.
        if quality level not specified, use quality level as specified in qpackageconfig.cfg in [qbase]/cfg
        """
        q.logger.log('prepare downloading the QPackage %s with version %s'%(name, version),8)

        self.vlists.loadVLists(domain)

        if not qualityLevels:
            qualityLevels = [self.getDefaultQualityLevel()]

        if not isinstance(qualityLevels, list):
            qualityLevels = str(qualityLevels).split(',')

        qpackages = self.qpackageFind(name, version, domain=domain, qualityLevels=qualityLevels, state='server')
        if not qpackages:
            raise RuntimeError('Failed to find QPackage <%s> version <%s>'%(name, version))
        else:
            if len(qpackages)>1:
                if isinstance(qualityLevels, list) and len(qualityLevels) == len(qpackages):
                    q.logger.log('Found QPackage matching all quality Levels specified', 6)
                else:
                    raise RuntimeError('Found more than one QPackage matching, please specify more information..')

        qpackage = qpackages[0]

        # call the download
        qpackageServerConnection = self.qpackageServerConnections.getConnectionFromDomain(str(qpackage.domain))

        if not qpackageServerConnection.isConnected():
            qpackageServerConnection.connect()

        for qualityLevel in qualityLevels:
            qPackages = self.qpackageFind(name, version, domain, qualityLevels=qualityLevel, state='SERVER')
            if not qPackages:
                continue
            if supportedPlatforms == 'ALL':
                qpackageServerConnection.download(str(qpackage.domain),qpackage.name, qpackage.version, qualityLevel, downloadAllFiles=True, module='read')
            else:
                if not supportedPlatforms:
                    supportedPlatforms = q.platform
                qpackageServerConnection.download(str(qpackage.domain),qpackage.name, qpackage.version, qualityLevel, supportedPlatforms=supportedPlatforms, module='read')

        q.logger.log('downloaded the QPackage %s with version %s'%(name, version),8)
        self.qpackagePackagesDir.vlists.createVLists(domain)
        self.qpackagePackagesDir.vlists.loadVLists(domain)

    def qpackageCreate(self,name,version,domain, qualityLevel='trunk'):
        """ Create a QPackage

        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain where you wish to create the QPackage
        @param qualityLevel: quality level of the QPackage
        """
        q.logger.log('creating the QPackage %s with version %s'%(name, version),8)
        # Check qpackage not  exists in client vlist
        qpackageList = self.qpackageFind(name, domain=domain,state='SERVER')
        if qpackageList and len(qpackageList) > 0:
            raise RuntimeError('QPackage already exists')

        # QPackage does not exist. first we will contact the server and then prepare the local folders
        qpackageServerConnection = self.qpackageServerConnections.getConnectionFromDomain(str(domain))
        if not qpackageServerConnection:
            raise ValueError('Failed to find a QPackage Server Connection serving domain <%s>'%domain)
        if not qpackageServerConnection.isConnected():
            qpackageServerConnection.connect()
        if not qpackageServerConnection.createNew(str(domain), name, version, qualityLevel):
            raise RuntimeError('QPackage %s for domain %s with version %s could not be created on the server'%(name, str(domain), version))
        # QPackage created localy, so we will return the object.
        #qpackageObject = QPackageObject(domain, name, version)
        qpackage = QPackage(domain, name, version)
        qpackage.buildNr = 'upload_%s'%qualityLevel
        qpackage.qualityLevel = str(qualityLevel)
        q.logger.log('created the QPackage %s with version %s'%(name, version),8)
        return qpackage

    def qpackagePromoteToMasterRepo(self, name, version, domain, domainLogin='', domainPasswd='', qualityLevel='trunk'):
        """
        Promote QPackage tp master repo
        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param domainLogin:    The user's login for the given domain
        @param domainPasswd: The user's password for the given domain
        @param qualityLevel: quality level of the QPackage
        """
        q.logger.log('Promoting QPackage %s to master repo'%name, 6)
        qpackageServerConnection = self.qpackageServerConnections.getConnectionFromDomain(str(domain))

        if not qpackageServerConnection.isConnected():
            qpackageServerConnection.connect()

        qpackageServerConnection.getVLists(domain)
        # getting the domain credentials
        domainLogin = domainLogin or q.qshellconfig.qpackagedomainlist.getParam(str(domain), 'login', defaultValue=None, forceDefaultValue=False)
        domainPasswd = domainPasswd or q.qshellconfig.qpackagedomainlist.getParam(str(domain), 'passwd', defaultValue=None, forceDefaultValue=False)
        if not domainLogin or not domainPasswd:
            raise ValueError('Please specify a domain login and password.')

        qpackageList = self.qpackageFind(name, version=version, domain=domain, qualityLevels=[str(qualityLevel)])
        if not qpackageList:
            raise RuntimeError('QPackage %s was not found'%name)
        if qpackageList and len(qpackageList)>1:
            raise RuntimeError('multiple instances of the QPackage %s with version %s found!'%(name, version))

        qpackageServerConnection.promoteQPackageToMasterRepo(str(domain), name, version, str(qualityLevel), domainLogin, domainPasswd)
        qpackageServerConnection.getVLists(domain)

    def qpackagePromote(self, name, version, domain, buildNr, destQualityLevels, domainLogin="", domainPassword=""):
        """
        Promote a QPackage to a higher qualityLevel on the server.
        @param name:           Name of the QPackage
        @param version:        Version of the QPackage
        @param domain:         Domain of the QPackage
        @param buildNr:        From where you wish to promote the QPackage (empty for local QPackage)
        @param destQualityLevels:    List of qualityLevels to where you wish to promote
        @param domainLogin:    The user's login for the given domain
        @param domainPassword: The user's password for the given domain
        """
        q.logger.log('Promoting QPackage %s from %s to %s'%(name, buildNr, destQualityLevels), 6)
        qpackageServerConnection = self.qpackageServerConnections.getConnectionFromDomain(str(domain))

        if not qpackageServerConnection.isConnected():
            qpackageServerConnection.connect()

        qpackageServerConnection.getVLists(domain)
        # getting the domain credentials
        domainLogin = domainLogin or q.qshellconfig.qpackagedomainlist.getParam(str(domain), 'login', defaultValue=None, forceDefaultValue=False)
        domainPassword = domainPassword or q.qshellconfig.qpackagedomainlist.getParam(str(domain), 'passwd', defaultValue=None, forceDefaultValue=False)
        if not domainLogin or not domainPassword:
            raise ValueError('Please specify a domain login and password.')

        if not self.qpackageFindFirst(name, version=version, domain=domain, state='server'):
            raise RuntimeError('QPackage %s was not found'%name)

        qpackageServerConnection.promoteQPackage(domain, name, version, buildNr, destQualityLevels, domainLogin, domainPassword)
        qpackageServerConnection.getVLists(domain)

    def qpackageCreateNewVersion(self, name, version, domain, qualityLevel='trunk', copyDependencies=True,\
                             copySupportedPlatforms=True, copyDescription=True, copyTags=True, copyFiles=True):
        """ Create a QPackage version

        @param name: name of the QPackage
        @param version: version of the QPackage
        @param domain: domain where you wish to create the QPackage
        @param qualityLevel: quality level of the QPackage
        @param copyDependencies       :copy the dependencies of the QPackage
        @param copySupportedPlatforms :copy the supported platforms of the QPackage
        @param copyDescription        :copy description of the QPackage
        @param copyTags               :copy tags of the QPackage
        @param copyFiles              :copy files of the QPackage
        """
        q.logger.log('creating the QPackage %s with version %s'%(name, version),8)
        # Check qpackage not  exists in client vlist
        qpackageList = self.qpackageFind(name, version=version, domain=domain, state='SERVER')
        if qpackageList and len(qpackageList) > 0:
            raise RuntimeError('QPackage already exists')

        # QPackage does not exist. first we will contact the server and then prepare the local folders
        qpackageServerConnection = self.qpackageServerConnections.getConnectionFromDomain(str(domain))
        if not qpackageServerConnection.isConnected():
            qpackageServerConnection.connect()
        if not qpackageServerConnection.createNewVersion(str(domain), name, version, qualityLevel, copyDependencies=copyDependencies,\
                             copySupportedPlatforms=copySupportedPlatforms, copyDescription=copyDescription, \
                             copyTags=copyTags, copyFiles=copyFiles):
            raise RuntimeError('QPackage %s for domain %s with version %s could not be created on the server'%(name, str(domain), version))
        # QPackage created localy, so we will return the object.
        qpackageObj = QPackageObject(domain, name, version)
        qpackage = QPackage(domain, name, version)
        qpackage.qualityLevel = qualityLevel
        qpackage.description = qpackageObj.description
        qpackage.tags = qpackageObj.tags
        qpackage.supportedPlatforms = qpackageObj.supportedPlatforms
        qpackage.buildNr = 'upload_%s'%qualityLevel
        q.logger.log('created the QPackage %s with version %s'%(name, version),8)
        return qpackage

    def qpackageDelete(self, name, version, domain="", domainLogin="", domainPassword="", fromQPackageServer=False,fromQPackageMasterServer=False):
        """ Delete a QPackage

        @param name: Name of the QPackage
        @param version: Version of the QPackage
        @param domain: domain of the QPackage
        @param domainLogin:    The user's login for the given domain
        @param domainPassword: The user's password for the given domain
        @param fromQPackageServer: if True, delete it from the QPackage Server you connect to.
        @param fromQPackageMasterServer: if True delete it from the Master Server

        if domain not specified, look for appropriate domain (use vlists on packagedir)
        """
        q.logger.log('deleting QPackage %s with version %s'%(name, version), 8)
        # if fromQPackageServer is selected we will delete the QPackage from all the servers
        # check whether the QPackage exists on the server

        if fromQPackageMasterServer:
            domainLogin = domainLogin or q.qshellconfig.qpackagedomainlist.getParam(str(qpackage.domain), 'login', defaultValue=None, forceDefaultValue=False)
            domainPassword = domainPassword or q.qshellconfig.qpackagedomainlist.getParam(str(qpackage.domain), 'passwd', defaultValue=None, forceDefaultValue=False)
            if not domainLogin or not domainPassword:
                raise ValueError('Please specify a domain login and password.')

        if fromQPackageMasterServer or fromQPackageServer:
            qpackages = self.qpackageFind(name, version, domain=domain, qualityLevels=[self.getDefaultQualityLevel()], state='SERVER')
            if not qpackages:
                raise RuntimeError('No objects found, aborting...')
            else:
                if len(qpackages)>1:
                    raise RuntimeError('Multiple objects found, aborting...')
            qpackage = qpackages[0]
            # getting the domain credentials

            conn = self.qpackageServerConnections.getConnectionFromDomain(str(domain))
            if not conn.isConnected():
                conn.connect()
            conn.delete(name, version, str(qpackage.domain), domainLogin=domainLogin, domainPasswd=domainPassword, fromMaster=fromQPackageMasterServer)
            conn.getVLists(domain)

        ################### Local delete ###########################
        # check whether the QPackage exists.
        if self.qpackageFindFirst(name, version=version, domain=domain, state='local'):
            #delete Local is supported only at this time
            self.qpackagePackagesDir.qpackageDelete(name, version , domain)
        ################### Local delete #########################
        q.logger.log('deleted QPackage %s with version %s'%(name, version), 8)

    def publishToQPackageServer(self, name, version, domain, qualityLevel="", syncFiles=True):
        """ Sync the files of the local upload_<qualitylevel> folder to the server

        @param name: name of the QPackage
        @param version: version of the QPackage as string
        @param domain: string or DomainObject representation of the domain
        @param qualitylevel: qualitylevel of the QPackage you wish to sync
        @param syncFiles: if True, upload all files, otherwise only upload the cfg file, defaults to True
        """
        if not isinstance(domain, (basestring, DomainObject)):
            raise ValueError('domain must be a string or a DomainObject')

        if not self.getDefaultQualityLevel():
            raise ValueError('Please set the default quality level before publishing.. Use: i.qpackages.setQualityLevel()')

        # sync the files to the server
        qpackageServerConnection = self.qpackageServerConnections.getConnectionFromDomain(str(domain))
        if not qpackageServerConnection.isConnected():
            qpackageServerConnection.connect()

        qpackage = QPackageObject(domain, name, version)
        if not qualityLevel:
            path = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath())
            for dirPath in q.system.fs.listDirsInDir(path):
                if 'upload_' in q.system.fs.getBaseName(dirPath):
                    qualityLevel = q.system.fs.getBaseName(dirPath)[dirPath.rindex('_')+1:]

        if not qualityLevel:
            raise IOError('Failed to publish QPackage. Upload directory does not exists..')

        #####################################################################################
        if not str(qualityLevel) == 'trunk':
            raise RuntimeError('Publishing qpackage <%s> on quality level <%s> is not allowed.\nPlease use qualityLevel <trunk> to publish  your qpackage..'%(qpackage,qualityLevel))
        #####################################################################################

        uploadDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath(), 'upload_%s'%qualityLevel)
        if not q.system.fs.exists(uploadDir):
            raise IOError('Failed to publish QPackage. Upload directory does not exists..')

        action = None
        if self.qpackageExists(name, domain=domain):
            if self.qpackageExists(name, version, domain):
                action = 'build'
                qPackageLatest = self.qpackageFindFirst(name, version, domain, str(qualityLevel), state='SERVER')
                if not int(qpackage.buildNr[str(qualityLevel)]) == int(qPackageLatest.buildNr):
                    ignore = q.console.askYesNo('You are creating a new build of qpackage <%s, %s> not based on the latest available build <%s> !!\n(build number in package dir is <%s>)!!\nAre you sure you want to continue'%(qpackage.name, qpackage.version, str(qPackageLatest.buildNr), str(qpackage.buildNr[str(qualityLevel)])))
                    if not ignore: return
                qpackageServerConnection.createNewBuild(str(domain), name, version, qualityLevel)
            else:
                action = 'version'
        else:
            action = 'new'

        for directory in q.system.fs.listDirsInDir(uploadDir):
            if q.system.fs.getBaseName(directory) == '.cfg':
                continue
            platformDirs = [q.system.fs.getBaseName(d) for d in q.system.fs.listDirsInDir(directory)]

            for supportedPlatform in qpackage.supportedPlatforms:
                dirExists = False
                for platformDir in platformDirs:
                    try:
                        q.enumerators.PlatformType.getByName(str(platformDir))
                    except KeyError, e:
                        raise IOError('Please move/rename <%s> in upload_%s to a platform directory %s'%(q.system.fs.joinPaths(q.system.fs.getBaseName(directory),platformDir),qualityLevel, qpackage.supportedPlatforms))
                    if str(supportedPlatform) ==  str(platformDir) or supportedPlatform.has_parent(platformDir):
                        dirExists = True
                if not dirExists:
                    missingDirs = ''
                    for supportedPlatform in qpackage.supportedPlatforms:
                        missingDirs += str(supportedPlatform)
                        if supportedPlatform.parent:
                            missingDirs +=str(supportedPlatform.parent)
                            if supportedPlatform.parent.parent:
                                missingDirs += str(supportedPlatform.parent.parent)
                    raise IOError('Missing directories in %s. Please add a directory for each supported platform before syncing files to server. (%s)'\
                                  %(directory, missingDirs))

        qpackageServerConnection.syncToServer(qpackage, qualityLevel, syncFiles)

        # find out if the QPackage is new, has a new version or a new build.
        buildNr= 0
        if action == 'build':
            buildNr = qpackageServerConnection.createNewBuildSynced(domain, name, version, qualityLevel)
        elif action == 'version':
            buildNr = qpackageServerConnection.createNewVersionSynced(domain, name, version, qualityLevel)
        else:
            buildNr = qpackageServerConnection.createNewSynced(domain, name, version, qualityLevel)
        qpackageObj = QPackage(domain, name, version)
        qpackageObj.buildNr = str(buildNr)
        qpackageObj.qualityLevel = str(qualityLevel)
        qpackageObj.dependencies = qpackage.dependencies
        qpackageObj.supportedPlatforms  = qpackage.supportedPlatforms
        qpackageObj.description = qpackage.description
        qpackageObj.tags = qpackage.tags
        # syncing the VLists
        qpackageServerConnection.getVLists(domain)
        # reloading the client VLists
        self.vlists.loadVLists(domain)
        # reload the configuration
        qpackageServerConnection.downloadConfig(str(domain), name, version, qualityLevel)
        # regenerating the local VLists
        self.qpackagePackagesDir.createVlists(domain, qualityLevel)
        return qpackageObj

    def __str__(self):
        return 'QPackageManagement'

    def __repr__(self):
        return str(self)
