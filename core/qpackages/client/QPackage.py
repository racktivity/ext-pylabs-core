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
from pylabs.qpackages.common.QPackageObject import QPackageObject
from pylabs.qpackages.common.DependencyDef import DependencyDef
from pylabs.qpackages.common.QPackageDependencyHelper import QPackageDependencyHelper
from pylabs.qpackages.client.QPackageTasklets import QPackageTasklets
from pylabs.qpackages.common.enumerators import QPackageState
from pylabs.qpackages.client.QPackageUtils import QPackageUtils
import string

class QPackage(BaseType):
    """
    gives access to users in manipulating the qpackage like download, install, ...
    All actions on the QPackage will call their equivalent(s) on q using
    """
    def _get_name(self):
        return self.__name

    def _get_domain(self):
        return self.__domain

    def _get_version(self):
        return self.__version

    def _setSourceManagement(self):
        setattr(self, 'source', SourceManagement(self))

    def _getPackageDir(self):
        return q.system.fs.joinPaths(q.dirs.packageDir, self.domain, self.name, self.version, self._getBuildNr() or 'upload_%s'%self.qualityLevel)

    def _setBuildNr(self, value):
        yield value
        self._setPackageDir()

    def _setQualityLevel(self, value):
        yield value
        self._setUploadDir()

    def _getBuildNr(self):
        return self.buildNr

    def _setPackageDir(self):
        self.packageDir = self._getPackageDir()

    def _setUploadDir(self):
        self.uploadDir = self._getUploadDir()

    def _getUploadDir(self):
        return self.packageDir if str(self._getBuildNr()).startswith('upload') else q.system.fs.joinPaths(q.dirs.packageDir, self.domain, self.name, self.version, 'upload_%s'%self.qualityLevel)

    def _getState(self):
        """
        Update the state and buildNr of the qpackage
        """
        state = self.state
        buildNr = None
        try:
            qpackage = QPackageObject(domain=self.domain, name=self.name, version=self.version)
            if str(self.qualityLevel):
                buildNr = qpackage.buildNr[str(self.qualityLevel)]
        except:
            q.logger.log('QPackage not available locally', 8)

        if not buildNr:
            state = 'SERVER'
            qpackage = q.qpackages.qpackageFindFirst(name=self.name, domain=self.domain, version=self.version, qualityLevels=[self.qualityLevel], state=state)
            if not qpackage:
                if self.state == 'DELETED':
                    state = 'DELETED'
                    self.buildNr = ""
            else:
                self.buildNr = qpackage.buildNr

        if buildNr or str(self.buildNr).startswith('upload'):
            if not str(self.buildNr).startswith('upload') and int(buildNr) < int(self.buildNr):
                state = 'SERVER'
            else:
                state = 'LOCAL'

        if state in ('LOCAL', 'MOD', 'NEW'):
            if q.system.fs.exists(self.uploadDir):
                if not buildNr:
                    state = 'NEW'
                else:
                    state = 'MOD'
                self.buildNr = 'upload_%s'%self.qualityLevel
            else:
                if buildNr:
                    state = 'LOCAL'
                    self.buildNr = buildNr
                else:
                    state = 'NEW'
                    self.buildNr = 'upload_%s'%self.qualityLevel

        self.state = state
        return state

    _VALID_NAME_CHARACTERS = set('%s%s_' % (string.ascii_lowercase, string.digits))
    name                   = q.basetype.string(doc="Official name of the QPackage, is part of unique identifier of QPackage", default=_get_name, readonly=True)
    version                = q.basetype.string(doc="Version of QPackage normally x.x format, is part of unique identifier of QPackage", default=_get_version, readonly=True)
    domain                 = q.basetype.string(doc="Domain of the QPackage, is part of unique identifier of QPackage", default=_get_domain, readonly=True)
    buildNr                = q.basetype.string(doc="Unique build nr for QPackage.",allow_none=True, default=None, fset = _setBuildNr)
    description            = q.basetype.string(doc="Short description of QPackage.",allow_none=True)
    tags                   = q.basetype.list(doc='List of tags describing the QPackage', default=list())
    supportedPlatforms     = q.basetype.list(doc="Supported platforms, see q.enumerators.platformtypes.", default=list())
    packageDir             = q.basetype.dirpath(doc='Path top the package dir', default = _getPackageDir)
    uploadDir              = q.basetype.dirpath(doc='Path top the upload dir', default = _getUploadDir)
    state                  = q.basetype.string(doc='State of qpackage', default='')

    def __init__(self, domain, name, version):
        self.__name = name
        self.__domain = str(domain)
        self.__version = str(version)
        self._setSourceManagement()

    ############################
    ## QPackageObject related ##
    ## = local                ##
    ############################

    def addDependency(self, qpackageName=None, domain=None, dependencyType=None, minVersion=None, maxVersion=None, supportedPlatforms=None):
        """
        Add a dependencies to the QPackage

        @param qpackageName:           Name of the QPackage that is a dependency
        @param domain:             Name of the domain which is responsible for the dependency. Same domain as this qpackage by default.
        @param dependencyType:     Type of dependency as q.enumerators.QPackageDependencyType. Runtime dependency by default
        @param minVersion:         If specified this will be the minimal version that the dependency van be.
        @param maxVersion:         If specified this will be the maximal version that the dependency can be.
        @param supportedPlatforms: List of supported platforms for which the dependency is required.
        """
        if qpackageName and domain:
            qpackages = q.qpackages.qpackageFind(name=qpackageName, domain=domain, qualityLevels=[self.qualityLevel])
        else:
            qpackages = i.qpackages.find(qpackageName, retQPackages=True)
        if not qpackages:
            raise RuntimeError('Failed to find QPackage')

        qpackage = qpackages[0]
        self._checkIfQPackageInPackageDir()
        if not dependencyType:
            dependencyType = q.enumerators.DependencyType.RUNTIME
        if minVersion is None:
            minVersion = q.console.askString('Minimum Version for the dependency')
        if maxVersion is None:
            maxVersion = q.console.askString('Maximum Version for the dependency')
        if not supportedPlatforms:
            q.console.echo('Supported platforms for this dependency')
            supportedPlatforms = q.console.askChoiceMultiple(q.enumerators.PlatformType.ALL)

        dependency = DependencyDef()
        dependency.name = qpackage.name
        dependency.domain = str(qpackage.domain)
        dependency.minversion = minVersion
        dependency.maxversion = maxVersion
        dependency.dependencyType = dependencyType

        mostApplQPackage = QPackageDependencyHelper().getMostApplicableQPackage(dependency, supportedPlatforms)
        if not mostApplQPackage:
            raise RuntimeError('Failed to find <%s>'%dependency.name)

        qpackageObject = QPackageObject(self.domain, self.name, self.version)
        qpackageObject.addDependency(mostApplQPackage.domain, mostApplQPackage.qpackageName, supportedPlatforms, minVersion, maxVersion, dependencyType)
        self.dependencies = qpackageObject.dependencies

    def deleteDependency(self, dependencyDef=None):
        """
        Deletes the given dependency definition
        """
        self._checkIfQPackageInPackageDir()

        qpackageObject = QPackageObject(self.domain, self.name, self.version)
        if not qpackageObject.getRuntimeDependencies():
            q.gui.dialog.message('QPackage <%s> does not have any dependency defined'%self)
            return
        if not dependencyDef:
            q.console.echo('Which dependency you wish to remove?')
            dependencyDef = q.console.askChoice(qpackageObject.getRuntimeDependencies())

        qpackageObject.removeDependency(dependencyDef.name, dependencyDef.dependencyType)
        self.dependencies = qpackageObject.dependencies

    def reviewDependency(self, dependencyDef=None, supportedPlatforms = None, newMinVersion=None, newMaxVersion=None):
        """
        Review dependency
        """
        self._checkIfQPackageInPackageDir()

        qpackageObject = QPackageObject(self.domain, self.name, self.version)

        q.console.echo('Which dependency you wish to modify?')
        dependencyDef = dependencyDef or q.console.askChoice(qpackageObject.getRuntimeDependencies())
        dependencyDef.supportedPlatforms = supportedPlatforms or q.gui.dialog.askChoiceMultiple('Supported platforms for this dependency', list(q.enumerators.PlatformType.ALL), defaultValue=','.join([str(supportedPlatform) for supportedPlatform in dependencyDef.supportedPlatforms]))
        dependencyDef.minversion = newMinVersion or q.gui.dialog.askString('Minimum Version for the dependency', dependencyDef.minversion)
        dependencyDef.maxversion = newMaxVersion or q.gui.dialog.askString('Maximum Version for the dependency', dependencyDef.maxversion)

        mostApplQPackage = QPackageDependencyHelper().getMostApplicableQPackage(dependencyDef, dependencyDef.supportedPlatforms)
        if not mostApplQPackage:
            raise RuntimeError('Failed to find an applicable qpackage for <%s>'%dependencyDef.name)

        qpackageObject.removeDependency(dependencyDef.name, dependencyDef.dependencyType)
        qpackageObject.addDependency(dependencyDef.domain, dependencyDef.name, dependencyDef.supportedPlatforms, dependencyDef.minversion, dependencyDef.maxversion, dependencyDef.dependencyType)

    def setDescription(self, description):
        """
        Sets the description of the QPackage
        @param description: Description for the QPackage
        """
        qpackageObject = QPackageObject(self.domain, self.name, self.version)
        qpackageObject.setDescription(description)
        self.description = qpackageObject.description

    def setTags(self, tags):
        """
        Set the tags to the QPackage
        @param tag:list of tags to set
        """
        if not isinstance(tags, list):
            tags = tags.split(',')
        qpackageObject = QPackageObject(self.domain, self.name, self.version)
        for tag in tags:
            qpackageObject.addTag(tag)

        self.tags = qpackageObject.tags

    def setSupportedPlatforms(self, platforms=None):
        '''
        Will set the supported platforms for the QPackage

        @param platforms: list of platforms that you support (can be platformtype or string)
        '''
        qpackageObject = QPackageObject(self.domain, self.name, self.version)
        supportedPlatforms = list(qpackageObject.supportedPlatforms)
        for supportedPlatform in supportedPlatforms:
            qpackageObject.removeSupportedPlatform(supportedPlatform)
        if not platforms:
            platforms = q.console.askChoiceMultiple(q.enumerators.PlatformType.ALL, 'Supported platform(s) for your QPackage:')

        if not isinstance(platforms, (list, tuple)):
            platforms = str(platforms).split(',')

        for platform in platforms:
            qpackageObject.addSupportedPlatform(str(platform))

        self.supportedPlatforms = qpackageObject.supportedPlatforms

    def getDependencies(self, platform=q.platform):
        """
        Returns a list of the dependency definitions of this QPackage. It will not run over the DependencyTree
        @param platform: platform to retrieve dependencies for or 'ALL' for all dependencies on all platforms
        """
        self._checkIfQPackageInPackageDir()
        qpackageObject = QPackageObject(self.domain, self.name, self.version)
        return qpackageObject.getRuntimeDependencies(None if str(platform) == 'ALL' or not platform else str(platform))

    def getDependencyQPackageNames(self):
        """
        Returns a list of QPackage names.
        """
        listOfDependencies = self.getDependencies()
        listOfDepNames = list()
        for dep in listOfDependencies:
            listOfDepNames.append(dep.name)
        return listOfDepNames

    def getDependencyTree(self, platform=q.platform):
        '''
        Calculate and print the dependency tree
        '''
        for dep in self.getDependencies(platform):
            if not q.qpackages.qpackageExists(dep.name, state='LOCAL'):
                raise RuntimeError('Please download all dependencies first')
        QPackageDependencyHelper().exportDependencyTree(self.domain, self.name, self.version, platform)

    def _checkIfQPackageInPackageDir(self):
        """
        Checks if the QPackage is downloaded
        """
        q.logger.log('Checking if QPackage exists in package dir', 6)
        try:
            ##QPackage could be a new QPackage, checking if we can instantiate a QPackage object
            q.logger.log('Checking if QPackage Object can be instantiated' , 7)
            QPackageObject(self.domain, self.name, self.version)
        except Exception, e:
            raise RuntimeError('Please download QPackage <%s> first'%self.name)

    ############################
    ## QPackageClient related ##
    ############################

    def download(self, processRuntimeDependencies=None, downloadAllPlatformFiles=None):
        '''
        Download the files for this QPackage

        @param processRuntimeDependencies: if True the QPackage will download all te dependencies, default True
        @param downloadAllPlatformFiles:   if True the QPackage will download all files
        '''
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to download qpackage %s. QPackage is deleted..')
        if self._getState() == 'NEW':
            raise RuntimeError('Your qpackage is not published yet on the server. Aborting..')
        trials = 0
        removed = False
        while self._getState() == 'MOD' and trials < 5:
            trials+=1
            removed  = self._removeUploadDir()
            if removed == None:
                return

        if processRuntimeDependencies is None:
            processRuntimeDependencies = q.console.askYesNo('Do you want to download Dependencies')
        if downloadAllPlatformFiles is None:
            downloadAllPlatformFiles = q.console.askYesNo('Do you want to download all platforms files')

        qpackageTasklets = QPackageTasklets()
        qpackageTasklets.download(self.name, self.version, self.domain, str(self.qualityLevel),
                               processRuntimeDependencies, False, downloadAllPlatformFiles)
        q.logger.log('Successfully downloaded qPackage %r'%self, 6)

    def _removeUploadDir(self):
        remove = q.gui.dialog.askYesNo('\nDo you want to remove <%s> (Please note that you will loose your work.)?'%self.uploadDir)
        if remove:
            QPackageUtils.removeDir(self.uploadDir)
            return True
        else:
            manually = q.gui.dialog.askYesNo('Do you want to remove <%s> manually'%self.uploadDir)
            if not manually:
                q.gui.dialog.message('\nAborting..')
                return None
        return False

    def publish(self):
        """
        Sync the files to the qpackageserver
        sync all changes from local syncdir qpackage to repository
        will use your active username & password
        will look for domain credential if required
        """
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to publish qpackage %s. QPackage is deleted..')
        while (not str(self._getState()) == 'MOD' and not str(self._getState()) =='NEW'):
            q.gui.dialog.message('\nNo modification found (Upload directory <%s> does not exist)'%self.uploadDir)
            if not q.qshellconfig.interactive:
                raise IOError('Please call prepare or add upload dir <%s> manually and try again. Aborting..'%self.uploadDir)
            prepare = q.gui.dialog.askYesNo('\nDo you want to prepare your qpackage?')
            if prepare:
                self.prepare()
            else:
                manual = q.gui.dialog.askYesNo('\nDo you wish to add the upload directory manually?')
                if not manual:
                    q.gui.dialog.message('Please call prepare or add upload dir <%s> manually and try again. Aborting..'%self.uploadDir)
                    return
        publish = q.gui.dialog.askYesNo('Please make sure you added/modified your files and tasklets in <%s> before publishing.. \nPublish?'%self.uploadDir)
        if not publish:
            q.gui.dialog.message('Aborting..')
            return
        qpackage = q.qpackages.publishToQPackageServer(self.name, self.version, self.domain, str(self.qualityLevel))
        self.buildNr  = qpackage.buildNr
        q.logger.log('Successfully published qPackage %r'%self, 6)

    def clone(self, newVersion=None, copyDependencies=None, copySupportedPlatforms=None, copyDescription=None, copyTags=None, copyFiles=None):
        """
        Create a new version of a QPackage
        @param newVersion             :new version of the QPackage
        @param copyDependencies       :copy the dependencies of the QPackage
        @param copySupportedPlatforms :copy the supported platforms of the QPackage
        @param copyDescription        :copy description of the QPackage
        @param copyTags               :copy tags of the QPackage
        @param copyFiles              :copy files of the QPackage
        """
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to clone qpackage %s. QPackage is deleted..')
        q.logger.log('Creating a new version of qPackage %r'%self, 6)
        if newVersion is None:
            newVersion = q.console.askString('New version of the QPackage')
        if copyDependencies is None:
            copyDependencies = q.console.askYesNo('Do you want to copy dependencies')
        if copySupportedPlatforms is None:
            copySupportedPlatforms = q.console.askYesNo('Do you want to copy supported platforms')
        if copyDescription is None:
            copyDescription = q.console.askYesNo('Do you want to copy description')
        if copyTags is None:
            copyTags = q.console.askYesNo('Do you want to copy tags')
        if copyFiles is None:
            copyFiles = q.console.askYesNo('Do you want to copy files')

        qpackage = q.qpackages.qpackageCreateNewVersion(self.name, newVersion, self.domain, str(self.qualityLevel), copyDependencies,\
                             copySupportedPlatforms, copyDescription, copyTags, copyFiles)

        qpackage.qualityLevel = self.qualityLevel
        if hasattr(i.qpackages, 'lastQPackages'):
            setattr(i.qpackages.lastQPackages, qpackage.name, qpackage)
            setattr(i.qpackages, 'lastQPackage', qpackage)
        q.logger.log('Successfully created new version of qPackage %r'%self, 6)

    def promoteToMaster(self, domainLogin=None, domainPasswd=None):
        """
        Promote QPackage tp master repo
        @param domainLogin:    The user's login for the given domain
        @param domainPasswd: The user's password for the given domain
        """
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to promote qpackage %s to master. QPackage is deleted..')
        q.logger.log('Promoting qPackage %r to master Repo'%self, 6)
        if domainLogin is None:
            domainLogin = q.console.askString('Please provide your domain login')
        if domainPasswd is None:
            domainPasswd = q.console.askString('Please provide your domain password')
        q.qpackages.qpackagePromoteToMasterRepo(self.name, self.version, self.domain, domainLogin, domainPasswd, str(self.qualityLevel))
        q.logger.log('Successfully promoted qPackage %r to master repo'%self, 6)

    def promote(self, domainLogin=None, domainPasswd=None, destinationQualityLevels=None):
        """
        Promote a QPackage to a higher qualityLevel on the server.
        @param domainLogin:    The user's login for the given domain
        @param domainPasswd: The user's password for the given domain
        @destQualityLevels:    List of qualityLevels to where you wish to promote
        """
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to promote qpackage %s. QPackage is deleted..')
        if self._getState() == 'NEW':
            raise RuntimeError('Your qpackage is not published yet on the server. Aborting..')

        trials = 0
        removed = False
        while self._getState() == 'MOD' and trials < 5:
            trials+=1
            removed  = self._removeUploadDir()
            if removed == None:
                return

        q.logger.log('Promoting qPackage %r'%self, 6)
        if domainLogin is None:
            domainLogin = q.console.askString('Please provide your domain login')
        if domainPasswd is None:
            domainPasswd = q.console.askString('Please provide your domain password')
        if not destinationQualityLevels:
            qualityLevels = ['trunk', 'test', 'unstable', 'beta', 'stable']
            if str(self.qualityLevel) in qualityLevels:
                qualityLevels.remove(str(self.qualityLevel))

            destinationQualityLevels = q.console.askChoiceMultiple(qualityLevels)

        promote = q.gui.dialog.askYesNo('Are you sure you wish to promote build nr <%s> to quality level(s) %s'%(self.buildNr, destinationQualityLevels))
        if not promote:
            return
        q.qpackages.qpackagePromote(self.name, self.version, self.domain, self.buildNr, destinationQualityLevels, domainLogin, domainPasswd)
        q.logger.log('Successfully promoted qPackage %r'%self, 6)

    def delete(self, domainLogin=None, domainPassword=None, deleteQPackage=None, fromQPackageServer=None, fromQPackageMasterServer=None):
        """
        Delete the QPackage, depending on the params given also delete on server and in domain.
        @param domainLogin:    The user's login for the given domain
        @param domainPassword: The user's password for the given domain
        @param fromQPackageServer: specifies whether the QPackage should be removed from pylabs.qpackageserver (when qpackageserver is not the master for the domain), default False
        @param fromQPackageMasterServer: specifies whether the QPackage should be removed from the domain (when server is the master for the domain), default False
        @param qualityLevels: list of qualityLevels where the QPackage should be removed from.
        """
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to delete qpackage %s. QPackage is deleted..')
        q.logger.log('Deleting qPackage %r'%self, 6)
        if fromQPackageServer is None:
            fromQPackageServer = q.console.askYesNo('Delete QPackage from QPackage Server')
        if fromQPackageMasterServer is None:
            fromQPackageMasterServer = q.console.askYesNo('Delete QPackage from QPackage Master Server.')
        if fromQPackageMasterServer == True:
            if domainLogin is None:
                domainLogin = q.console.askString('Please provide your domain login')
            if domainPassword is None:
                domainPassword = q.console.askString('Please provide your domain password')
        delete = q.console.askYesNo('Are you sure you wish to delete QPackage \"%s,%s,%s\"?\nThis will delete version %s completely'%(self.name, self.version, self.domain, self.version))
        if not delete:
            return

        q.qpackages.qpackageDelete(self.name, self.version, self.domain, domainLogin=domainLogin if not domainLogin is None else '', domainPassword=domainPassword if not domainPassword is None else '', fromQPackageServer=fromQPackageServer, fromQPackageMasterServer=fromQPackageMasterServer)

        self.state = 'DELETED'
        q.logger.log('Successfully deleted qPackage %r'%self, 6)

    def quickPublish(self):
        """
        Prepares, exports, compiles, packages and publishes a qpackage
        """
        self.prepare()
        self.source.export()
        self.source.compile()
        self.package()
        self.publish()

    ##############################
    ## QPackageTasklets related ##
    ##############################

    def install(self, processRuntimeDependencies=True, downloadAllFiles=False):
        """
        Install QPackage and its dependencies.
        Already installed dependencies which are already installed will be upgraded if
        newer version available.
        @param processRuntimeDependencies: if True install dependencies
        @param downloadAllFiles: download files for all platforms.
        """
        self._install(processRuntimeDependencies, downloadAllFiles, reInstall=False)
        if self._getState()  == 'SERVER':
            raise RuntimeError('Failed to install QPackage %s'%self)
        q.logger.log('Successfully installed qPackage %r'%self, 6)

    def reInstall(self, processRuntimeDependencies=True, downloadAllFiles=False):
        """
        Install QPackage and its dependencies.
        Already installed dependencies which are already installed will be upgraded if
        newer version available.
        @param processRuntimeDependencies: if True install dependencies
        @param downloadAllFiles: download files for all platforms.
        """
        self._install(processRuntimeDependencies, downloadAllFiles, reInstall=True)
        q.logger.log('Successfully reInstalled qPackage %r'%self, 6)

    def _install(self, processRuntimeDependencies, downloadAllFiles, reInstall):
        """
        Install QPackage and its dependencies.
        Already installed dependencies which are already installed will be upgraded if
        newer version available.
        @param processRuntimeDependencies: if True install dependencies
        @param downloadAllFiles: download files for all platforms.
        @param reInstall: if true will reinstall even if latest buildnr is installed
        """
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to install qpackage %s. QPackage is deleted..')
        if self._getState() == 'MOD' or self._getState() == 'NEW':
            q.action.startOutput()
            confirm = q.gui.dialog.askYesNo('Installing from upload Directory <%s>. Are you sure you want to continue?'%self.uploadDir)
            q.action.stopOutput()
            if not confirm:
                removed = False
                trials =0
                while self._getState() == 'MOD' or self._getState() == 'NEW' and trials < 5:
                    trials +=1
                    removed = self._removeUploadDir()
                    if removed == None:
                        return
        devmode = i.qpackageLocalConfig.isQPackageInDevMode(self.domain, self.name, self.version)
        if devmode:
            reInstall = True

        qpackageTasklets = QPackageTasklets()
        qpackageTasklets.install(self, processRuntimeDependencies, downloadAllFiles, reInstall, devmode)

    def prepare(self):
        '''
        Download all files of the latest build and prepares the qpackage for a new build
        if upload dir does not already exist
        '''
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to prepare qpackage %s. QPackage is deleted..')
        if self._getState() == 'NEW':
            return
        elif self._getState() == 'MOD':
            use = q.gui.dialog.askYesNo('Upload directory <%s> already exists.. Use existing directory?'%self.uploadDir)
            if use:
                return
            while self._getState() == 'MOD' or self._getState() == 'NEW':
                if self._removeUploadDir() is None:
                    return

        self.download(False, True)
        if self._getState() == 'LOCAL':
            q.system.fs.copyDirTree(self.packageDir, self.uploadDir)
        if not self._getState() == 'MOD':
            raise RuntimeError('Failed to prepare qpackage %s' %self)
        q.logger.log('Successfully preparing qPackage %r'%self, 6)

    def start(self):
        """
        Check if QPackage is installed and calls the start tasklet
        """
        self.__isInstalled()
        self.__callTasklet('start')

    def stop(self):
        """
        Check if QPackage is installed and calls the stop tasklet
        """
        self.__isInstalled()
        self.__callTasklet('stop')

    def restart(self):
        """
        Check if QPackage is installed and calls the restart tasklet
        """
        self.__isInstalled()
        self.__callTasklet('restart')

    def getStatus(self):
        """
        Check if QPackage is installed and calls the restart tasklet
        """
        self.__isInstalled()
        self.__callTasklet('getStatus')

    def uninstall(self):
        """
        Uninstall
        """
        self.__isInstalled()
        self.__callTasklet('uninstall')

    def package(self):
        """
        Calls the package tasklet of the QPackage
        """
        if self._getState() == 'DELETED':
            raise RuntimeError('Failed to package qpackage %s. QPackage is deleted..')
        if not self._getState() == 'MOD' and not self._getState() == 'NEW':
            self.prepare()
            export = q.gui.dialog.askYesNo('Do you wish to export the source of your qpackage')
            if export:
                self.source.export()
        if not self._getState() == 'SERVER':
            qpackageTasklets  = QPackageTasklets()
            qpackageTasklets.package(self)
        q.logger.log('Successfully packaged QPackage %r'%self, 6)

    def enableDevelopmentMode(self):
        """
        Enable development mode for this QPackage.
        In development mode, installing a QPackage equals building a QPackage
        """
        i.qpackageLocalConfig.enableQPackageDevMode(self.domain, self.name, self.version)

    def disableDevelopmentMode(self):
        """
        Disable development mode for this QPackage.
        """
        i.qpackageLocalConfig.disableQPackageDevMode(self.domain, self.name, self.version)

    def _checkBuildDependencies(self):
        """
        Checks if all build dependencies are installed
        """
        try:
            ##try to retrieve the qpackage object, if this fails then we throw an exception. As this means
            ##that the qpackage doesnt exist in the packageDir
            q.logger.log('Retrieving QPackage <%s> Object'%self.name, 6)
            qpackageObject = q.qpackages.qpackagePackagesDir.qpackageGetObject(self.name, self.version, self.domain, str(self.qualityLevel))

        except Exception, ex:
            q.logger.log('Failed to retrieve QPackageObject for %r' %self, 7)
            raise RuntimeError(ex)

        q.logger.log('Checking for build dependencies', 7)
        for dep in qpackageObject.getBuildDependencies():
            depQPackageObject = QPackageDependencyHelper().getMostApplicableQPackage(dep, q.platform)
            if not q.qpackages.qpackageIsInstalled(depQPackageObject.qpackageName, depQPackageObject.version, depQPackageObject.domain):
                raise RuntimeError('Please install build dependency <%s>'%depQPackageObject.qpackageName)

    def __callTasklet(self, tag):
        """
        Call a method on QPackageTasklets to execute a matching tasklet
        """
        q.logger.log('Calling %s tasklet for qPackage %r'%(tag,self), 6)
        qpackageTasklets  = QPackageTasklets()
        method = getattr(qpackageTasklets, str(tag))
        method(self)
        q.logger.log('Successfully called %s qPackage %r'%(tag,self), 6)

    def __isInstalled(self):
        if not q.qpackages.qpackageIsInstalled(self.name, self.version, self.domain):
            raise RuntimeError('Please install QPackage (%s, %s) first'%(self.name, self.version))

    def __str__(self):
        return '%s %s (%s) - %s'%(self.name, self.version, self.domain, self.state)

    def __repr__(self):
        return '%s %s (%s) - %s'%(self.name, self.version, self.domain, self._getState())

class SourceManagement:
    def __init__(self, qpackageObject):
        self._qpackage = qpackageObject

    def build(self):
        """
        Calls the getSource + compile tasklet of the qpackage
        """
        q.logger.log('Building qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.build(self._qpackage)

    def get(self):
        """
        Calls the getSource-tasklet of the qpackage
        """
        q.logger.log('Get Source for qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.getSource(self._qpackage)

    def diff(self):
        """
        Calls the diff-tasklet of the qpackage
        """
        q.logger.log('Source Diff for qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.diff(self._qpackage)

    def remove(self):
        """
        Calls the clean-tasklet of the qpackage
        """
        q.logger.log('Remove Source for qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.remove(self._qpackage)

    def stat(self):
        """
        Calls the stat-tasklet of the qpackage
        """
        q.logger.log('Stat source for qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.stat(self._qpackage)

    def compile(self):
        """
        Calls the compile-tasklet of the qpackage
        """
        q.logger.log('Calling compile tasklet for qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.compile(self._qpackage)

    def checkin(self):
        """
        Calls the svnrecipe-tasklet of the qpackage with action=checkin
        """
        q.logger.log('Checking in source of qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.checkin(self._qpackage)

    def checkout(self):
        """
        Calls the svnrecipe-tasklet of the qpackage with action=checkout
        """
        q.logger.log('Checking out source of qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.checkout(self._qpackage)

    def export(self):
        """
        Calls the svnrecipe-tasklet of the qpackage with action=export
        """
        q.logger.log('Exporting source of qPackage %s'%str(self._qpackage), 6)
        qpackageTasklets  = QPackageTasklets()
        qpackageTasklets.export(self._qpackage)