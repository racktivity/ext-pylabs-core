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
from pylabs.baseclasses import BaseType
from pylabs.enumerators.PlatformType import PlatformType
from pylabs.qpackages.client.QPackageExecuterHelper import QPackageExecuterHelper
from pylabs.qpackages.client.QPackageInstallerHelper import QPackageInstallerHelper
from pylabs.qpackages.common.QPackageObject import QPackageObject
from pylabs.qpackages.client.QPackageManagement import QPackageManagement
from pylabs.qpackages.common.QPackageDependencyHelper import QPackageDependencyHelper
from pylabs.qpackages.common.enumerators import DependencyType

class QPackageInstaller(BaseType):
    """
    Installer class which contains helper methods to install the content of a qpackage.
    This helper method is passed on as a parameter to the qpackage's install script.
    """
    pm_QPackageManagement = q.basetype.object(QPackageManagement, default=QPackageManagement())
    _buildDependecies = q.basetype.list(doc='List of build dependencies to download/install', default=list())
    _runtimeDependencies = q.basetype.list(doc='List of runtime dependencies to download/install', default=list())
    
    def download(self, name, version, domain="", qualityLevel="", processRuntimeDependencies=True, processBuildDependencies=False, downloadAllFiles=False):
        """
        Download QPackage
        @param name: Name of the QPackage
        @param domain: domain of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: quality level of the qpackage
        @param processRuntimeDependencies: if True install dependencies
        @param processBuildDependencies: if True install dependencies
        @param downloadAllFiles: download files for all platforms.
        """
        q.logger.log('Downloading QPackage <%s>'%name, 6)
        if not qualityLevel:
            q.logger.log('Retrieving the default quality level', 7)
            q.qshellconfig.loadConfigFile('qpackageconfig')
            qualityLevel = q.qshellconfig.qpackageconfig.getParam('main', 'defaultqualitylevel', defaultValue=None, forceDefaultValue=True)

        if not domain:
            domain = self._getDomainForQPackage(name, version, qualityLevel)

        self._download(name, version, domain, qualityLevel, processRuntimeDependencies, processBuildDependencies, downloadAllFiles)

    def _download(self, name, version, domain, qualityLevel, processRuntimeDependencies, processBuildDependencies, downloadAllFiles):
        """
        Download QPackage
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: quality level of the qpackage
        @param processRuntimeDependencies: if True install dependencies
        @param processBuildDependencies: if True install dependencies
        @param downloadAllFiles: download files for all platforms.
        @param checkIfQPackageExists: if true will check if QPackage with given criteria is already downloaded
        """
        downloadQPackage = True
        if self._checkCurrentlyDownloadedBuildNr(name, version, domain, qualityLevel):
            downloadQPackage = False
        if downloadQPackage:
            q.action.start('Downloading QPackage %s'%name)
            q.logger.log('Downloading QPackage <%s> version <%s> qualityLevel <%s> from domain <%s>'%(name, version, qualityLevel, domain), 6)
            self.pm_QPackageManagement.qpackageDownload(name, version, domain, qualityLevel, supportedPlatforms = 'ALL' if downloadAllFiles else q.platform)

        qpackageObject = QPackageObject(domain, name, version)
        if processBuildDependencies:
            q.logger.log('Processing build dependencies', 6)
            self._downloadDependencies(qpackageObject, DependencyType.BUILD)
        if processRuntimeDependencies:
            q.logger.log('Processing runtime dependencies', 6)
            self._downloadDependencies(qpackageObject, DependencyType.RUNTIME)

        self.pm_QPackageManagement.qpackagePackagesDir.createVlists(domain)
        if downloadQPackage:
            q.action.stop()

    def _downloadDependencies(self, qpackageObject, dependencyType):
        """
        Download qpackage dependencies
        @param qpackageObject: QPackageObject instance
        @param dependencyType: type of the dependencies to install e.g. DependencyType.BUILD
        """
        q.logger.log('Downloading QPackage %s %s dependencies'%(qpackageObject.name, str(dependencyType)), 6)
        qpackageDependencyHelper = QPackageDependencyHelper()
        dependencies = qpackageObject.getBuildDependencies(str(q.platform)) if dependencyType == DependencyType.BUILD else qpackageObject.getRuntimeDependencies(str(q.platform))
        for dependencyDef in dependencies:
            q.logger.log('Checking if QPackage exists in vlist', 6)
            if not self.pm_QPackageManagement.vlists.find(dependencyDef.name):
                raise RuntimeError('QPackage <%s> was not found'%dependencyDef.name)

            q.logger.log('Searching for the most suitable QPackage for dependency def <%s>'%dependencyDef, 6)
            vlistEntry = qpackageDependencyHelper.getMostApplicableQPackage(dependencyDef, q.platform)
            self._buildDependecies.append(vlistEntry) if dependencyType == DependencyType.BUILD else self._runtimeDependencies.append(vlistEntry)

            q.logger.log('Downloading QPackage <%s>'%vlistEntry.qpackageName, 6)
            self._download(vlistEntry.qpackageName, vlistEntry.version, str(vlistEntry.domain), str(vlistEntry.qualityLevel), processRuntimeDependencies=True, processBuildDependencies=False, downloadAllFiles=False)
            self.pm_QPackageManagement.qpackagePackagesDir.createVlists(vlistEntry.domain, vlistEntry.qualityLevel)
            self.pm_QPackageManagement.qpackagePackagesDir.vlists.loadVLists(vlistEntry.domain,str(vlistEntry.qualityLevel))

    def _getDomainForQPackage(self, name, version, qualityLevel):
        """
        Get domain for a qpackage
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: quality level of the qpackage
        """
        q.logger.log('Searching for QPackage in vlist to find suitable domain', 7)
        result = self.pm_QPackageManagement.vlists.find(name, version=version, qualityLevels=[qualityLevel])
        if not result:
            raise RuntimeError('Failed to find an available domain for QPackage <%s> version <%s>'%(name, version))
        ##take the first match
        return result[0].domain

    def _checkCurrentlyInstalledBuild(self, name, version, domain, qualityLevel, newBuildNr):
        """
        Check if QPackage with given buildNr is already installed.
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: quality level of the qpackage
        @param newBuildNr: new build nr to install
        """
        if not self.pm_QPackageManagement.qpackageIsInstalled(name, version, domain):
            return False
        currentBuildNr = self.pm_QPackageManagement.qpackageGetInstalledBuildNr(name, version, domain)

        if currentBuildNr and int(currentBuildNr) < int(newBuildNr):
            return False
        return True

    def _checkCurrentlyDownloadedBuildNr(self, name, version, domain, qualityLevel, newBuildNr=None):
        """
        Check if QPackage with given buildNr is already downloaded.
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: quality level of the qpackage
        @param newBuildNr: new build nr to download
        """
        q.logger.log('Checking if QPackage exists in package dir', 7)
        qpackageExists = self.pm_QPackageManagement.qpackagePackagesDir.qpackageExists(name, version, domain)
        if not qpackageExists:
            return False

        if  newBuildNr is None:
            q.logger.log('Retrieving the QPackage build nr from clients vlists', 7)
            result = self.pm_QPackageManagement.qpackageFind(name, version, str(domain), [str(qualityLevel)] if qualityLevel else None)
            if not result:
                raise RuntimeError('Failed to find QPackage %s'%name)
            newBuildNr = result[0].buildNr
        
        qpackageObject = self.pm_QPackageManagement.qpackagePackagesDir.qpackageGetObject(name, version, domain)
        q.logger.log('Checking if given quality level of QPackage already exists', 7)
        if not str(qualityLevel) in qpackageObject.buildNr:
            return False
        q.logger.log('Checking if buildNr downloaded for given quality level is older than given buildNr', 7)
        if int(qpackageObject.buildNr[str(qualityLevel)]) < int(newBuildNr):
            return False

        return True
    
    def install(self, name, version, domain, qualityLevel="", processRuntimeDependencies=True, processBuildDependencies=False, downloadAllFiles=False, reInstall=False):
        """
        Installation step for the QPackage
        install from packagedir
        if quality level not specified, use quality level as specified in qpackageconfig.cfg in [qbase]/cfg

        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage if empty search the QPackage in your domains
        @param qualityLevel: quality level of the qpackage
        @param processRuntimeDependencies: if True install dependencies
        @param processBuildDependencies: if True install dependencies
        @param downloadAllFiles: download files for all platforms.
        @param reInstall: if true will reinstall even if latest buildnr is installed
        """
        if not qualityLevel:
            q.qshellconfig.loadConfigFile('qpackageconfig')
            qualityLevel = q.qshellconfig.qpackageconfig.getParam('main', 'defaultqualitylevel', defaultValue=None, forceDefaultValue=True)

        if not domain:
            raise ValueError('Domain <%s> is not valid.Please specify a valid domain'%domain)
        q.logger.log('Attempting to download QPackage <%s> version <%s>'%(name, version), 7)

        try:
            self._download(name, version, domain, qualityLevel, processRuntimeDependencies, processBuildDependencies, downloadAllFiles)
        except Exception, e:
            q.logger.log('Failed to download QPackage. QPackage might be only available locally', 8)
            pass
        ##try to instantiate a QPackage Object, qpackage could be available locally
        try:
            qpackageObject = QPackageObject(domain, name, version)
        except Exception, ex:
            raise RuntimeError(e)

        q.action.start('Installing QPackage %s'%name)
        if processBuildDependencies:
            self._installDependencies(qpackageObject, DependencyType.BUILD)
        if processRuntimeDependencies:
            self._installDependencies(qpackageObject, DependencyType.RUNTIME)

        if not qualityLevel in qpackageObject.buildNr:
            buildNr = 'upload_%s'%qualityLevel
        else:
            buildNr = qpackageObject.buildNr[qualityLevel]
        self._install(name, version, buildNr, domain, qualityLevel, reInstall=reInstall)
        q.action.stop()

    def _installDependencies(self, qpackageObject, dependencyType):
        """
        Install QPackage dependencies
        @param qpackageObject: QPackageObject
        @param dependencyType: type of dependencies to install. e.g DependencyType.BUILD or DependencyType.RUNTIME
        """
        self._buildDependecies.reverse()
        self._runtimeDependencies.reverse()
        dependencies = self._buildDependecies if dependencyType == DependencyType.BUILD else self._runtimeDependencies
        for dependency in dependencies:
            if not self.pm_QPackageManagement.qpackagePackagesDir.qpackageExists(dependency.qpackageName, dependency.version, dependency.domain, qualityLevels=[str(dependency.qualityLevel)]):
                raise RuntimeError('QPackage <%s> was not found in package dir'%dependency.qpackageName)
            
            qpackageObject = QPackageObject(dependency.domain, dependency.qpackageName, dependency.version)

            self._install(qpackageObject.name, qpackageObject.version, qpackageObject.buildNr[str(dependency.qualityLevel)], str(qpackageObject.domain), str(dependency.qualityLevel))

    def _install(self, name, version, buildNr, domain, qualityLevel, reInstall=False):
        """
        Install QPackage
        @param name: Name of the QPackage 
        @param version: version of the QPackage 
        @param buildNr: build number of the QPackage
        @param domain: domain of the QPackage
        @param qualityLevel: quality level of the qpackage         
        @param reInstall: if true will reinstall even if latest buildnr is installed
        """
        q.logger.log('Checking if QPackage is supported for current platform <%s>'%str(q.platform), 6)
        qpackageObject = QPackageObject(domain, name, version)
        supported = False
        
        for platform in qpackageObject.supportedPlatforms:
            if q.platform.has_parent(platform):
                supported = True
                break
        if not supported:
            raise RuntimeError('Failed to install QPackage <%s>. QPackage is only supported on platform(s) %s'%(name, qpackageObject.supportedPlatforms))

        if not reInstall and self._checkCurrentlyInstalledBuild(name, version, domain, qualityLevel, buildNr):
            return
        q.action.start('Executing install script of QPackage %s'%name)

        qpackageInstallerHelper = QPackageInstallerHelper(name, domain, version, buildNr)

        installScriptLocation = q.system.fs.joinPaths(q.dirs.packageDir, domain, name, version, 'installer' , 'install.qshell')

        if q.system.fs.isFile(installScriptLocation):
            result = QPackageExecuterHelper.executeMainMethodInScript(installScriptLocation, qpackageInstallerHelper)
        self._updateQPackageInifile(domain, name, version, buildNr)

        q.extensions.pm_sync()

        q.action.stop()

    def _updateQPackageInifile(self, domain, name, version, buildNr):
        """
        Update qpackageinfo.cfg with the latest installed build nr
        """
        qpackageCfgDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages', domain, name, version)
        if not q.system.fs.exists(qpackageCfgDir):
            q.system.fs.createDir(qpackageCfgDir)

        qpackageInfo = q.system.fs.joinPaths(qpackageCfgDir,'qpackageinfo.cfg')
        
        if not q.system.fs.exists(qpackageInfo):
            iniFile = q.tools.inifile.new(qpackageInfo)
            iniFile.addSection('main')
            iniFile.addParam('main', 'buildnr', buildNr)
        else:
            iniFile = q.tools.inifile.open(qpackageInfo)
            iniFile.setParam('main', 'buildnr', buildNr)