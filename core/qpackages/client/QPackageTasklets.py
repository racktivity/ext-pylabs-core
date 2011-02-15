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

from pylabs import q, i
from pylabs.baseclasses import BaseType
from pylabs.qpackages.client.QPackageInstallerHelper import QPackageInstallerHelper
#from pylabs.qpackages.common.QPackageObject import QPackageObject
from pylabs.qpackages.common.QPackageDependencyHelper import QPackageDependencyHelper
from pylabs.qpackages.common.enumerators import DependencyType
from pylabs.tasklets import TaskletsEngine
import exceptions

class QPackageTasklets(BaseType):
    """
    Installer class which contains helper methods to install the content of a qpackage.
    This helper method is passed on as a parameter to the qpackage's install script.
    """
    _qpackages = q.basetype.dictionary(doc='dict of processed qpackages', default=dict())

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
        q.logger.log('Downloading QPackage <%s, %s , %s>' % (domain,name,version),4)
        if not qualityLevel:
            #q.logger.log('Retrieving the default quality level', 7)
            qpackageObject.qualityLevel = q.qpackages.getDefaultQualityLevel()

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
        skip = False
        if self._checkCurrentlyDownloadedBuildNr(name, version, domain, qualityLevel) and not downloadAllFiles:
            downloadQPackage = False
        if downloadQPackage:
            q.action.start('Downloading QPackage %s %s %s' % (domain, name , version))
            q.logger.log('Downloading QPackage <%s> version <%s> qualityLevel <%s> from domain <%s>'%(name, version, qualityLevel, domain), 6)
            q.qpackages.qpackageDownload(name, version, domain, qualityLevel, supportedPlatforms = 'ALL' if downloadAllFiles else q.platform)

        if (name, version, str(domain)) in self._qpackages:
            qpackageObject = self._qpackages[(name, version, str(domain))]
            skip = True
        else:
            qpackageObject = q.qpackages.qpackagePackagesDir.qpackageGetObject(name, version, domain)
            self._qpackages[(qpackageObject.name, qpackageObject.version, str(qpackageObject.domain))] = qpackageObject

        if not q.system.fs.exists(q.system.fs.joinPaths(q.dirs.packageDir, qpackageObject.getRelativeBuildPath(qualityLevel))) or \
           q.system.fs.exists(q.system.fs.joinPaths(q.dirs.packageDir, qpackageObject.getRelativeQPackagePath(), 'download')):
            raise QPackageDownloadException(qpackageObject)

        if skip: return
        buildNr = qpackageObject.buildNr[str(qualityLevel)]
        qpackageObject.buildNr = dict()
        qpackageObject.buildNr[str(qualityLevel)] = buildNr

        if processBuildDependencies:
            q.logger.log('Processing build dependencies', 6)
            self._downloadDependencies(qpackageObject, DependencyType.BUILD)
        if processRuntimeDependencies:
            q.logger.log('Processing runtime dependencies', 6)
            self._downloadDependencies(qpackageObject, DependencyType.RUNTIME)

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
            if not q.qpackages.vlists.find(dependencyDef.name):
                raise QPackageNotFoundException(str(dependencyDef.name))

            q.logger.log('Searching for the most suitable QPackage for dependency def <%s>'%dependencyDef, 6)
            vlistEntry = qpackageDependencyHelper.getMostApplicableQPackage(dependencyDef, q.platform)

            q.logger.log('Downloading QPackage <%s>'%vlistEntry.qpackageName, 6)
            self._download(vlistEntry.qpackageName, vlistEntry.version, str(vlistEntry.domain), str(vlistEntry.qualityLevel), processRuntimeDependencies=True, processBuildDependencies=False, downloadAllFiles=False)

    def install(self,qpackageObject, processRuntimeDependencies=True, downloadAllFiles=False, reInstall=False, devmode=False):
        """
        Installation step for the QPackage
        install from packagedir

        @param qpackageObject: qpackage object to install
        @param processRuntimeDependencies: if True install dependencies
        @param downloadAllFiles: download files for all platforms.
        @param reInstall: if true will reinstall even if latest buildnr is installed
        @param devmode: if True, package will be installed in development mode
        """
        if not qpackageObject.qualityLevel:
            qpackageObject.qualityLevel = q.qpackages.getDefaultQualityLevel()
        if not qpackageObject.domain:
            raise ValueError('Domain <%s> is not valid.Please specify a valid domain'%qpackageObject.domain)
        q.logger.log('Attempting to download QPackage <%s> version <%s>'%(qpackageObject.name, qpackageObject.version), 7)
        downloadException = None
        try:
            self._download(qpackageObject.name, qpackageObject.version, qpackageObject.domain, qpackageObject.qualityLevel, processRuntimeDependencies, False, downloadAllFiles)
        except RuntimeError, downloadException:
            q.logger.log('Failed to download QPackage. QPackage might be only available locally',7)

        ##try to instantiate a QPackage Object, qpackage could be available locally
        try:
            qpackageCfgObject = q.qpackages.qpackagePackagesDir.qpackageGetObject(qpackageObject.name, qpackageObject.version, qpackageObject.domain)
            if not q.system.fs.exists(q.system.fs.joinPaths(q.dirs.packageDir, qpackageCfgObject.getRelativeBuildPath(qpackageObject.qualityLevel))) or q.system.fs.exists(q.system.fs.joinPaths(q.dirs.packageDir, qpackageCfgObject.getRelativeQPackagePath(), 'download')):
                raise QPackageDownloadException(qpackageCfgObject)

            if not str(qpackageObject.buildNr).startswith('upload') and not int(qpackageObject.buildNr) == int(qpackageCfgObject.buildNr[str(qpackageObject.qualityLevel)]):
                qpackageObject.buildNr = str(qpackageCfgObject.buildNr[str(qpackageObject.qualityLevel)])

        except Exception, ex:
            raise downloadException if downloadException else ex

        if devmode:
            self.build(qpackageObject)

        self._installQPackage(qpackageObject, processRuntimeDependencies, reInstall=reInstall)

        from pylabs.qpackages.client.QPackageConfigure import QPackageConfigure
        configure = QPackageConfigure()
        reconfigureDict = configure.getIniFile().getFileAsDict()
        if len(reconfigureDict)>0:
            q.console.echo('')
            q.console.echo('************************************************************************')
            q.console.echo('%s qpackage(s) needs to be (re)configured.. Please restart your qshell..' % len(reconfigureDict))
            for priority in range(len(reconfigureDict)):
                if not str(priority) in reconfigureDict:
                    continue
                q.console.echo("* %(name)s %(version)s (%(domain)s)" % reconfigureDict[str(priority)])
            q.console.echo('************************************************************************')

    def _installQPackage(self, qpackageObject, processRuntimeDependencies, reInstall=False):
        """
        Install QPackage with dependencies
        @param qpackageObject: qpackage object
        @param reInstall: if true will reinstall even if latest buildnr is installed
        """
        if not processRuntimeDependencies:
            qpackage = self._install(qpackageObject, reInstall=reInstall)
            return
        helper = QPackageDependencyHelper()
        dependencies = helper.getFullDependency(qpackageObject.domain ,qpackageObject.name, qpackageObject.version)
        dependencies.reverse()
        reInstallQPackage = False
        for dependency in dependencies:
            domain,name,version = dependency
            qpackage = self._getQPackage(self._qpackages[(name,version, str(domain))]) if (name,version, str(domain)) in self._qpackages  else q.qpackages.qpackageFindFirst(name=name, version=version, domain=str(domain), qualityLevels=[qpackageObject.qualityLevel],state='LOCAL')
            if not qpackage:
                raise RuntimeError('QPackage <%s> was not found in package dir'%name)
            if (name, version, str(domain)) == (qpackageObject.name, qpackageObject.version, str(qpackageObject.domain)):
                reInstallQPackage = reInstall

            self._install(qpackage, reInstallQPackage)

    def _getQPackage(self,qpackage):
        """
        return a client.QPackage object based on common.QPackageObject object
        """
        from pylabs.qpackages.client.QPackage import QPackage
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
        q.logger.log('Retrieved QPackage %r'%qPackage)
        return qPackage

    def _install(self, qpackageObject, reInstall=False):
        """
        Install QPackage
        @param qpackageObject: qpackage object
        @param reInstall: if true will reinstall even if latest buildnr is installed
        """
        q.logger.log('Checking if QPackage is supported for current platform <%s>'%str(q.platform), 6)

        supported = False

        for platform in qpackageObject.supportedPlatforms:
            if q.platform.has_parent(platform):
                supported = True
                break

        if not supported:
            raise RuntimeError('Failed to install QPackage <%s>. QPackage is only supported on platform(s) %s'%(qpackageObject.name, qpackageObject.supportedPlatforms))

        if not reInstall and self._checkCurrentlyInstalledBuild(qpackageObject.name,qpackageObject.version, qpackageObject.domain, qpackageObject.buildNr):
            return

        engine = self._createTaskletEngine(qpackageObject)

        if i.qpackageLocalConfig.isQPackageInDevMode(qpackageObject.domain, qpackageObject.name, qpackageObject.version):
            self.build(qpackageObject)
            return

        if not engine.find(tags=('install',)):
            raise RuntimeError('No tasklets found with matching tags (\'install\',)')

        q.action.start('Installing QPackage %s'%qpackageObject.name)
        q.qshellconfig.interactive = True #allows interactive questions
        q.action.start('Executing Install Tasklet of QPackage %s'%qpackageObject.name)

        q.logger.log('Executing Install Tasklet of QPackage %s'%qpackageObject.name, 7)
        engine.execute(params={'qpackage':qpackageObject}, tags=('install',))

        q.logger.log('Updating QPackage inifile', 7)
        self._updateQPackageInifile(qpackageObject.domain, qpackageObject.name, qpackageObject.version, qpackageObject.buildNr if not str(qpackageObject.buildNr).startswith('upload') else 0 )

        q.logger.log('Loading new extensions (if any)', 7)
        q.extensions.pm_sync()

        q.action.stop()
        q.action.stop()

    def uninstall(self, qpackageObject):
        """
        Calls the stop-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        if not q.qpackages.qpackageIsInstalled(qpackageObject.name, qpackageObject.version, str(qpackageObject.domain)):
            raise RuntimeError('Failed to unistall: QPackage (%s, %s, %s) is not installed')

        q.action.start("Uninstall QPackage (%s, %s)"%(qpackageObject.name, qpackageObject.version))
        engine = self._createTaskletEngine(qpackageObject)
        if not engine.find(tags=('uninstall',)):
            q.logger.log('No tasklets found with matching tags (\'uninstall\',)', 6)
            return
        q.action.start("Executing Uninstall tasklet")
        engine.execute(params={'qpackage':qpackageObject}, tags=('uninstall',))
        q.action.stop()
        qpackageCfgDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages', qpackageObject.domain, qpackageObject.name, qpackageObject.version)

        if q.system.fs.exists(qpackageCfgDir):
            q.system.fs.removeDirTree(qpackageCfgDir)

        q.action.stop()

    def start(self, qpackageObject):
        """
        Calls the start-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'start')

    def stop(self, qpackageObject):
        """
        Calls the stop-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'stop')

    def _executeTasklet(self, qpackageObject, tag):
        engine = self._createTaskletEngine(qpackageObject)
        if not engine.find(tags=(tag,)):
            q.logger.log('No tasklets found with matching tags (\'%s\',)'%tag, 3)
            return
        engine.execute(params={'qpackage':qpackageObject}, tags=(tag,))

    def restart(self, qpackageObject):
        """
        Calls the stop-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'restart')

    def getStatus(self, qpackageObject):
        """
        Calls the stop-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'getStatus')

    def package(self, qpackageObject):
        """
        Execute the package-tasklet
        @param qpackageObject: qpackage object
        """
        engine = self._createTaskletEngine(qpackageObject)
        if not engine.find(tags=('package',)):
            raise RuntimeError('No tasklets found with matching tags (\'qpackage\',)')
        engine.execute(params={'qpackage':qpackageObject}, tags=('package',))

    def configure(self, qpackageObject):
        """
        Executes the configure tasklet of the qpackage
        @param qpackageObject: qpackage object
        """
        qpackageObject = self._getQPackage(qpackageObject)
        engine = self._createTaskletEngine(qpackageObject)
        engine.execute(params={'qpackage':qpackageObject}, tags=('configure',))

    def build(self, qpackageObject):
        """
        Execute getSource + compile
        """
        self.getSource(qpackageObject)
        self.compile(qpackageObject)

    def compile(self, qpackageObject):
        """
        Execute the compile-tasklet
        @param qpackageObject: qpackage object
        """
        engine = self._createTaskletEngine(qpackageObject)
        if engine.find(tags=('compile',)):
            # No error if no compile tasklet found (e.g. for trivial python packages)
            engine.execute(params={'qpackage':qpackageObject}, tags=('compile',))

    def getSource(self, qpackageObject):
        """
        Execute the codeManagement-tasklet with action==getSource
        @param qpackageObject: qpackage object
        """
        self._codeManagementAction(qpackageObject, 'getSource')

    def stat(self, qpackageObject):
        """
        Execute the codeManagement-tasklet with action == stat
        @param qpackageObject: qpackage object
        """
        self._codeManagementAction(qpackageObject, 'stat')

    def diff(self, qpackageObject):
        """
        Execute the codeManagement-tasklet with action == diff
        @param qpackageObject: qpackage object
        """
        self._codeManagementAction(qpackageObject, 'diff')

    def remove(self, qpackageObject):
        """
        Execute the codeManagement-tasklet with action == remove
        @param qpackageObject: qpackage object
        """
        self._codeManagementAction(qpackageObject, 'remove')

    def checkout(self, qpackageObject):
        """
        Calls the codeManagement-tasklet of the qpackage with action=checkout
        @param qpackage: qpackage object
        """
        self._codeManagementAction(qpackageObject, 'checkout')

    def checkin(self, qpackageObject):
        """
        Calls the codeManagement-tasklet of the qpackage with action=checkin
        @param qpackageObject: qpackage object
        """
        self._codeManagementAction(qpackageObject, 'checkin')

    def export(self, qpackageObject):
        """
        Calls the codeManagement-tasklet of the qpackage with action=export
        @param qpackageObject: qpackage object
        """
        self._codeManagementAction(qpackageObject, 'export')

    def _createTaskletEngine(self, qpackageObject):
        """
        Create tasklet engine for this qpackage object.
        It always prefers the upload_<qualityLevel> dir over the <buildNr> dir
        @param qpackageObject: qpackage object
        """
        taskletsDirs = self._getTaskletsPlatformDirs(qpackageObject.domain, qpackageObject.name, qpackageObject.version, qpackageObject.buildNr)

        q.logger.log("Instantiating tasklet engine", 9)
        engine = TaskletsEngine()
        for taskletDir in taskletsDirs:
            q.logger.log("Adding tasklet dir [%s] to tasklet engine" % taskletDir, 10)
            engine.addFromPath(taskletDir)
        return engine

    def _getLatestBuildNr(self, qpackageObject):
        """
        Get the latest buildNr from which tasklets can be executed.
        If there is an upload_<qualitylevel> dir then that will be used.
        Otherwise just the buildNr dir in the packagedir
        @param qpackageObject: QPackage object
        """
        ##retrieving qpackage configuration from package directory
        try:
            qpackageCfgObject = QPackageObject(qpackageObject.domain, qpackageObject.name, qpackageObject.version)
        except Exception, ex:
            raise RuntimeError(ex)

        buildNr = qpackageObject.buildNr
        ##Using upload_qualitylevel as buildNr if the upload dir exists or if there is a buildNr for quality level set in qpackageObject.
        if q.system.fs.isDir(qpackageObject.uploadDir) or not str(qpackageObject.qualityLevel) in qpackageCfgObject.buildNr:
            return 'upload_%s'%qpackageObject.qualityLevel

        return buildNr

    def _codeManagementAction(self, qpackageObject, action):
        """
        Calls the codeManagement-tasklet of the qpackage with an action
        @param qpackageObject: qpackage object
        @param action: action to pass to the tasklet. e.g. checkout, checkin, export
        """
        engine = self._createTaskletEngine(qpackageObject)
        if not engine.find(tags=('codeManagement',)):
            raise RuntimeError('No tasklets found with matching tags (\'codeManagement\',)')
        engine.execute(params={'qpackage':qpackageObject,'action':action}, tags=("codeManagement",))

    def _getDomainForQPackage(self, name, version, qualityLevel):
        """
        Get domain for a qpackage
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param qualityLevel: quality level of the qpackage
        """
        q.logger.log('Searching for QPackage in vlist to find suitable domain', 7)
        result = q.qpackages.vlists.find(name, version=version, qualityLevels=[qualityLevel])
        if not result:
            raise RuntimeError('Failed to find an available domain for QPackage <%s> version <%s>'%(name, version))
        ##take the first match
        return result[0].domain

    def _checkCurrentlyInstalledBuild(self, name, version, domain, newBuildNr):
        """
        Check if QPackage with given buildNr is already installed.
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param newBuildNr: new build nr to install
        """
        if not q.qpackages.qpackageIsInstalled(name, version, domain):
            return False
        currentBuildNr = q.qpackages.qpackageGetInstalledBuildNr(name, version, domain)

        if str(newBuildNr).startswith('upload'):
            return False
        if int(newBuildNr) == 0:
            return False
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
        #qpackage = q.qpackages.qpackageFindFirst(name, version, domain, [str(qualityLevel)], state='LOCAL')
        if (name, version, str(domain)) in self._qpackages:
            return True

        result =  q.qpackages.qpackagePackagesDir.vlists.find(name, domain, version, [str(qualityLevel)], exactMatch=True)
        if not result:
            return False

        if  newBuildNr is None:
            q.logger.log('Retrieving the QPackage build nr from clients vlists', 7)
            #result = q.qpackages.qpackageFind(name, version, str(domain), [str(qualityLevel)] if qualityLevel else q.qpackages.getDefaultQualityLevel(), state='SERVER')
            result = q.qpackages.vlists.find(name,version=version, domain=str(domain), qualityLevels=[str(qualityLevel)] if qualityLevel else q.qpackages.getDefaultQualityLevel(), exactMatch=True)
            if not result:
                raise RuntimeError('Failed to find QPackage %s'%name)
            newBuildNr = result[0].buildNr

        qpackageObject = q.qpackages.qpackagePackagesDir.qpackageGetObject(name, version, domain)
        q.logger.log('Checking if given quality level of QPackage already exists', 7)
        if not str(qualityLevel) in qpackageObject.buildNr:
            return False
        q.logger.log('Checking if buildNr downloaded for given quality level is older than given buildNr', 7)

        if not q.system.fs.exists(q.system.fs.joinPaths(q.dirs.packageDir, qpackageObject.getRelativeBuildPath(str(qualityLevel)))):
            return False
        if int(newBuildNr) == 0 and not int(qpackageObject.buildNr[str(qualityLevel)]) == 0:
            return False
        if int(qpackageObject.buildNr[str(qualityLevel)]) < int(newBuildNr):
            return False

        return True

    def _getTaskletsPlatformDirs(self, domain, name, version, buildNr):
        """
        Returns a list of directories with applicable tasklets
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        @param buildNr: build nr of the QPackage
        """
        qpackageInstallerHelper =  QPackageInstallerHelper(name, domain, version, buildNr)
        dirs = qpackageInstallerHelper.getPlatformDirsToCopy('tasklets')
        if len(dirs)==0:
            raise RuntimeError("No tasklet directories found for domain [%s] package [%s] version [%s] buildnr [%s]" % (domain, name, version, buildNr))
        return dirs

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

class QPackageNotFoundException(exceptions.Exception):
    def __init__(self, qpackageName):
        msg = self.handleException(qpackageName)
        self.errmsg = msg
        self.args=(msg, )

    def handleException(self, qpackageName):
        """
        Handle error message thrown.
        @param qpackageName: the name of the qpackage that was not found
        """
        return 'QPackage <%s> was not found'%qpackageName

class QPackageDownloadException(exceptions.Exception):
    def __init__(self, qpackageName):
        msg = self.handleException(qpackageName)
        self.errmsg = msg
        self.args=(msg, )

    def handleException(self, qpackageName):
        """
        Handle error message thrown.
        @param qpackageName: the name of the qpackage that was not found
        """
        return 'Failed to download QPackage <%s>'%qpackageName