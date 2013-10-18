from pylabs import q, i
from pylabs.baseclasses import BaseType
from pylabs.enumerators.PlatformType import PlatformType
from pylabs.baseclasses.dirtyflaggingmixin import DirtyFlaggingMixin
from DependencyDef4 import DependencyDef4
from QPackageStateObject import QPackageStateObject
from pylabs.sync.Sync import SyncLocal
from QPackageIObject4 import QPackageIObject4
from QPackageDefaultFilesGenerator import QPackageDefaultFilesGenerator
import json
import os

class QPackageObject4(BaseType, DirtyFlaggingMixin):
    ''' Data representation of a QPackage, should contain all information contained in the qpackage.cfg '''

    # All this information represents the package as in the repo..
    # the already install package may have differnent dependencies,
    # may have a higher build number
    # if so we cannot say anything about the
    domain  = q.basetype.string(doc='The domain this QPackage belongs to', allow_none=True, default=None)
    name    = q.basetype.string(doc='Name of the QPackage should be lowercase', allow_none=False)
    version = q.basetype.string(doc='Version of a string', allow_none=False)

    buildNr  = q.basetype.integer(doc='Build number of the QPackage', allow_none=False, default=0)
    bundleNr = q.basetype.integer(doc='Build number of the Bundle', allow_none=False, default=0)
    metaNr   = q.basetype.integer(doc='Build number of the MetaData', allow_none=False, default=0)

    #should be readonly
    supportedPlatforms = q.basetype.list(doc='List of PlatformTypes',allow_none=False, default=list())
    tags               = q.basetype.list(doc='list of tags describing the QPackage', allow_none=True, default=list())
    description        = q.basetype.string(doc='Description of the QPackage, can be larger than the description in the VList4', allow_none=True, flag_dirty=True, default='')
    dependencies       = q.basetype.list(doc='List of DependencyDefinitions for this QPackage', allow_none=True, default=list())
    guid               = q.basetype.string(doc='Unique global id', allow_none=False, flag_dirty=True, default='')
    #lastModified=q.basetype.float(doc='When was this package last modified (time.time)', allow_none=False, flag_dirty=True, default='')

    def __init__(self, domain, name, version,branch="", description="",new=False):

        ''' initialization of the QPackage

        @param domain:  The domain that the QPackage belongs to, can be a string or the DomainObject4
        @param name:    The name of the QPackage
        @param version: The version of the QPackage
        '''

        ##q.logger.log('Initializing the QPackage Object %s - %s - %s'%(domain, name, version), 6)
        #checks on correctness of the parameters
        if not domain:
            raise ValueError('The domain parameter cannot be empty or None')
        if not name:
            raise ValueError('The name parameter cannot be empty or None')
        if not version:
            raise ValueError('The version parameter cannot be empty or None')
        self.domain = domain
        self.name = name
        self.version = version
        self.tags = []
        if branch=="":
            domainobject=q.qp.getDomainObject(domain)
            branch=domainobject.metadataBranch
        self.branch=branch

        if new==False:
            domainobject=q.qp.getDomainObject(domain)
            if domainobject.metadataBranch.lower()<>self.branch.lower():
                #the qpackage we are trying to instanstiate is another branch than the main
                domainobject.updateMetadataTmpLocation(branch) #update the tmp metadata dir to the right branch
                self.fromTmp=True
            self._parseConfig()
        else:
            #new qpackage
            if q.system.fs.exists(self.getPathMetadata()):
                raise RuntimeError ("Cannot create new qpackage, does already exist on %s" % self.getPathMetadata())
            #qpackage did not exist yet
            # create it
            self.buildNr = -1
            q.system.fs.createDir(self.getPathMetadata())
            ##self.save() # dont save unless we need to!

        if self.guid=="":
            self.guid= q.base.idgenerator.generateGUID()

        descriptionpath = q.system.fs.joinPaths(self.getPathMetadata(), 'description.wiki')
        if q.system.fs.exists(descriptionpath):
            self.description= q.system.fs.fileGetContents(descriptionpath)
        if self.description=="":
            self.description="h2. %s %s %s\n\n...\n" % (self.domain,self.name,self.version)
        if new:
            self.save()
        q.logger.log('Initialization of the QPackage %s has finished'%str(self), 8)

###############################################################
############  MAIN OBJECT METHODS (DELETE, ...)  ##############
###############################################################

    def delete(self):
        """
        Deletes all bundles, metadata, files of the qpackage
        """
        if q.qshellconfig.interactive:
            do=q.gui.dialog.askYesNo("Are you sure you want to remove %s_%s_%s, all bundles, metadata & files will be removed" % (self.domain,self.name,self.version))
        else:
            do=True
        if do:
            # When deleting this package from the main branch
            # We should make sure there are no more packages on other branches
            # If there are we abort this operation.

            path=q.qp.getDataPath(self.domain,self.name,self.version)
            q.system.fs.removeDirTree(path)
            path=q.qp.getMetadataPath(self.domain,self.name,self.version)
            q.system.fs.removeDirTree(path)
            #@todo walk over all files in bundles, remove relevant files
            for f in q.system.fs.listFilesInDir(q.qp.getBundlesPath()):
                baseName = q.system.fs.getBaseName(f)
                if baseName.split('__')[0] == self.name and baseName.split('__')[1] == self.version:
                    q.system.fs.deleteFile(f)
            # @todo Upload repository

            #@todo over ftp try to delete the targz file (less urgent)

    def save(self):
        """
        Creates a new config file and saves the most important qpackage params in it
        """
        ##self.assertAccessable()
        # Todo put this back on!!
        # Disabled this to be able to use convertor
        self._log('saving.. to ' + self.getPathMetadata())
        self._ensureOnCorrectBranch()

        if self.buildNr=="":
            self._raiseError("buildNr cannot be empty")
        if self.description=="":
            self._raiseError("description cannot be empty")

        #create directory
        q.system.fs.createDir(self.getPathMetadata())
        q.system.fs.createDir(self.getPathFiles())

        #write config file
        inifile = self._getIniFile(reset=True)
        inifile.addSection('main')
        inifile.addSection('checksum')
        sups = ''
        for sup in self.supportedPlatforms:
            sups += '%s, '%( str(sup).strip())
        inifile.setParam('main', 'supportedPlatforms', sups)
        inifile.setParam('main', 'tags', ','.join(self.tags))
        #check if guid already created, if not create
        inifile.setParam('main', 'guid', self.guid)
        inifile.setParam('main', 'buildNr', self.buildNr)
        inifile.setParam('main', 'MetaNr', self.metaNr)
        inifile.setParam('main', 'bundleNr', self.bundleNr)
        for platform, bundleName, bundleFile in self._getBundleFiles():
            inifile.setParam('checksum', platform.name, q.tools.hash.sha256(bundleFile))

        inifile.write()
        for dependency in self.dependencies:
            self._addDependencyToCfgFile(dependency.domain, dependency.name, dependency.supportedPlatforms, minversion=dependency.minversion, \
                                         maxversion=dependency.maxversion, dependencytype=dependency.dependencytype)

        descriptionpath = q.system.fs.joinPaths(self.getPathMetadata(), 'description.wiki')
        q.system.fs.writeFile(descriptionpath, self.description)


    def reload(self):
        """
        Reloads the qpackage's config file
        """
        self._parseConfig()
        #@todo check on qpackage client reload fuction walks over all objects


################################################################################
#########################  OBJECT MODIFICATION  ################################
################################################################################

    def addDependency(self, domain, name, supportedPlatforms, minversion=None, maxversion=None, dependencytype=None):
        '''
        Add a dependency definition to the cfg file.
        @param domain:             domain of the QPackage you wish to depend on
        @param name:               name of the QPackage dependency
        @param supportedPLatforms: list of the supported platforms for that QPackage dependency (array of q.enumerators.PlatformType...)
        @param minversion:         minimal version of the QPackage dependency
        @param maxversion:         maximal version of the QPackage dependency
        @param dependencytype:     Dependency Type from q.enumerators.DependencyType
        '''
        ##self.assertAccessable()
        if dependencytype==None:
            dependencytype=q.enumerators.DependencyType4.BUILD

        self._checkDependencyInput(domain, name, supportedPlatforms, minversion, maxversion, dependencytype)

        if (domain, name, dependencytype) in [(d.domain, d.name, d.dependencytype) for d in self.dependencies]:
            raise RuntimeError('You are trying to add a duplicate dependency')

        dep=DependencyDef4()
        dep.dependencytype=dependencytype
        dep.domain = domain
        dep.name = name
        dep.minversion = minversion
        dep.maxversion = maxversion
        dep.supportedPlatforms = supportedPlatforms
        self.dependencies.append(dep)
        self.save()

    def removeDependency(self, dependency):
        '''
        Remove a dependency.
        You can remove only a dependency completely. If you wish to change a dependency, just do an addDependency and we will overwrite it.

        @param dependency: a dependency object obtained from a Qpackage.
        '''
        ##self.assertAccessable()
        if not dependency in self.dependencies:
            raise RuntimeError('Dependency ' + str(dependency) + ' not found!')

        self.dependencies.remove(dependency)
        self.save()


    def addTag(self, tag):
        '''
        Adding a tag to the QPackage
        @param tag: string of type customer or customer:kristof   first is like a label, 2nd is tag with value
        '''
        ##self.assertAccessable()
        q.logger.log('Adding tag "%s" to the QPackage %s'%(tag, self.name), 8)
        if not tag in self.tags:
            self.tags.append(tag)
        else:
            q.logger.log('QPackage %s already contains the "%s" tag'%(self.name, tag), 8)
        self.save()

    def removeTag(self, tag):
        '''
        Removing a tag from the QPackage
        @param tag: string
        '''
        ##self.assertAccessable()
        q.logger.log('Removing tag "%s" to the QPackage %s'%(tag, self.name), 8)
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise ValueError('QPackage does not have the tag you are trying to remove')
        self.save()


##################################################################################################
###################################  CONFIG FILE HANDLING  #######################################
##################################################################################################

    def _fixConfigFile(self,cfg):
        """
        open the config file, check for all possible broken items in config file, fix & safe
        """
        if not cfg.checkParam('main', 'buildNr'):
            cfg.setParam('main', 'buildNr', cfg.getValue('main', 'build'))
        if not cfg.checkParam('main', 'bundleNr'):
            cfg.setParam('main', 'bundleNr', cfg.getValue('main', 'buildNr'))
        if not cfg.checkParam('main', 'metaNr'):
            cfg.setParam('main', 'metaNr', cfg.getValue('main', 'buildNr'))

    def getChecksum(self, platform):
        cfg = self._getIniFile()
        if not cfg.checkSection('checksum'):
            return None
        if not cfg.checkParam('checksum', platform.name):
            return None
        return cfg.getValue('checksum', platform.name)

    def _parseConfig(self):
        '''
        Get the needed information from the config file
        If the configfile does not exist, then it will be created.
        '''
        q.logger.log('Start parsing the configuration file of the QPackage %s' % str(self), 8)

        cfgPath = q.system.fs.joinPaths(self.getPathMetadata(), 'qpackage.cfg')
        if q.system.fs.exists(cfgPath)==False:
            self._raiseError("Cannot find qpackage, there should be a config file in %s" % cfgPath)
        cfg = self._getIniFile()
        self._fixConfigFile(cfg)
        self._clear()

        self.buildNr  = int(cfg.getValue('main', 'buildNr'))
        self.bundleNr = int(cfg.getValue('main', 'bundleNr'))
        self.metaNr   = int(cfg.getValue('main', 'metaNr'))

        #self.lastModified=float(cfg.getValue('main', 'lastModified'))
        self.guid=cfg.getValue('main', 'guid')
        # get the comma separated list of tags, loop over them and add to the tagslist in the QPackage
        tagsList = str(cfg.getValue('main', 'tags')).split(',')
        q.logger.log('Parsing QPackage %s, tags = %s'%(str(self), cfg.getValue('main','tags')), 8)
        for tag in tagsList:
            if tag and tag.strip() not in self.tags:
                self.tags.append(tag.strip())
        # get the comma separated list of platform types, then loop over then and add them to the QPackage list.
        supPlatforms = str(cfg.getValue('main', 'supportedPlatforms')).split(',')
        q.logger.log('Parsing QPackage %s, supportedPlatforms = %s'%(str(self), cfg.getValue('main', 'supportedPlatforms')), 8)
        for platform in supPlatforms:
            if platform and PlatformType.getByName(platform.strip()) not in self.supportedPlatforms:
                self.supportedPlatforms.append(PlatformType.getByName(platform.strip()))
        dependencies = list()
        #get Dependency definitions (runtime)
        for section in cfg.getSections():
            # only check sections that contain dep_ or depbuild_
            if str(section).startswith('dep_') or str(section).startswith('depbuild_'):
                dep = DependencyDef4()
                if str(section).startswith('depbuild'):
                    dep.dependencytype = q.enumerators.DependencyType4.BUILD
                    dep.name = section[9:]
                    q.logger.log('Parsing QPackage build dependency for %s, %s'%( str(self), dep.name ), 8)
                else:
                    dep.dependencytype = q.enumerators.DependencyType4.RUNTIME
                    dep.name = section[4:]
                    q.logger.log('Parsing QPackage dependency for %s, %s'%( str(self), dep.name ), 8)

                dep.domain = cfg.getValue(section, 'domain')
                q.logger.log('Parsing %s dependency %s, domain: %s'%( str(dep.dependencytype), dep.name, dep.domain ), 8)
                dep.minversion = cfg.getValue(section, 'minversion')
                q.logger.log('Parsing %s dependency %s, minversion: %s'%( str(dep.dependencytype), dep.name, dep.minversion ), 8)
                dep.maxversion = cfg.getValue(section, 'maxversion')
                q.logger.log('Parsing %s dependency %s, maxversion: %s'%( str(dep.dependencytype), dep.name, dep.maxversion ), 8)
                supPlatforms = str(cfg.getValue(section, 'supportedPlatforms')).split(',')
                q.logger.log('Parsing %s dependency %s, supportedPlatforms = %s'%(str(dep.dependencytype), dep.name, cfg.getValue('main', 'supportedPlatforms')), 8)
                for platform in supPlatforms:
                    if platform:
                        dep.supportedPlatforms.append(PlatformType.getByName(platform.strip()))
                dependencies.append(dep)
        self.dependencies  = dependencies

    def _checkDependencyInput(self,domain, name, supportedPlatforms, minversion, maxversion, dependencytype):
        """

        """
        if not domain or not q.basetype.string.check(domain):
            raise ValueError('The domain parameter must be a string and cannot be None')
        if not name or not q.basetype.string.check(domain):
            raise ValueError('The name parameter cannot be empty or None')
        if not supportedPlatforms:
            raise ValueError('The supportedPlatforms parameter must not contain an empty list or None, is array of q.enumerators.PlatformType')
        if not q.basetype.list.check(supportedPlatforms):
            self._raiseError("supported platform must be array of q.enumerators.PlatformType")
        for platf in supportedPlatforms:
            if not q.enumerators.PlatformType.check(platf):
                self._raiseError("supported platform must be array of q.enumerators.PlatformType")
        if not q.enumerators.DependencyType4.check(dependencytype):
            self._raiseError("Cannot find dependencytype %s, get the type from q.enumerators.DependencyType..." % dependencytype)


    def _addDependencyToCfgFile(self, domain, name, supportedPlatforms, minversion=None, maxversion=None, dependencytype=None):
        '''
        Add a dependency definition to the cfg file.
        @param domain:             domain of the QPackage you wish to depend on
        @param name:               name of the QPackage
        @param supportedPLatforms: list of the supported platforms for that QPackage dependency (array of q.enumerators.PlatformType...)
        @param minversion:         minimal version of the QPackage dependency
        @param maxversion:         maximal version of the QPackage dependency
        @param DependencyType4:     Dependency Type (build, runtime)
        '''

        if dependencytype==None:
            dependencytype=q.enumerators.DependencyType4.BUILD

        self._checkDependencyInput(domain, name, supportedPlatforms, minversion, maxversion, dependencytype)

        cfg = self._getIniFile()
        if dependencytype == q.enumerators.DependencyType4.RUNTIME:
            sectionName = 'dep_%s'%name.strip()
        else:
            sectionName = 'depbuild_%s'%name.strip()
        if not cfg.checkSection(sectionName):
            cfg.addSection(sectionName)
            cfg.addParam(sectionName, 'domain', str(domain).strip())
            cfg.addParam(sectionName, 'minversion', (minversion if minversion else ''))
            cfg.addParam(sectionName, 'maxversion', (maxversion if maxversion else ''))
            sups = ''

            for sup in supportedPlatforms:
                sups += '%s, '%( str(sup).strip())
            cfg.addParam(sectionName, 'supportedPlatforms', sups)
        else:
            cfg.setParam(sectionName, 'domain', str(domain).strip())
            cfg.setParam(sectionName, 'minversion', (minversion if minversion else ''))
            cfg.setParam(sectionName, 'maxversion', (maxversion if maxversion else ''))
            sups = ''

            for sup in supportedPlatforms:
                sups += '%s, '%( str(sup).strip())
            cfg.setParam(sectionName, 'supportedPlatforms', sups)
            cfg.write()

    def _getIniFile(self, reset=False):
        ##self.assertAccessable()
        ''' returns the IniFile object of the QPackage
        @param reset means clean first
        '''
        # return qpackage config file
        cfgPath = q.system.fs.joinPaths(self.getPathMetadata(), 'qpackage.cfg')
        ##if new and q.system.fs.exists(cfgPath):
        ##    q.system.fs.removeFile(cfgPath)
        ##if not new and not q.system.fs.exists(cfgPath):
        ##    raise RuntimeError("Cannot find qpackage config file on %s" % cfgPath)
        if reset and q.system.fs.exists(cfgPath):
            q.system.fs.removeFile(cfgPath)
        if q.system.fs.exists(cfgPath):
            inifile=q.tools.inifile.open(cfgPath)
        else:
            inifile=q.tools.inifile.new(cfgPath)
        return inifile

################################################################################
####################################  PLATFORM  ################################
################################################################################


    def addSupportedPlatform(self, platform):
        '''
        Add a supported platform to the QPackage
        @param platform: string or q.enumerators.PlatformType
        '''
        ##self.assertAccessable()
        q.logger.log('Adding platform %s to supportedplatforms of %s'%(str(platform), self.name), 8)
        if not q.enumerators.PlatformType.check(platform):
            self._raiseError("platform needs to be of type q.enumerators.PlatformType")
        if not platform in self.supportedPlatforms:
            self.supportedPlatforms.append(platform)
        self.save()

    def removeSupportedPlatform(self, platform):
        '''
        Remove a supported platform from the QPackage
        @param platform: string of PlatformType to remove
        '''
        ##self.assertAccessable()
        if self.supportedPlatforms == []:
            raise RuntimeError("This package doesn't have any supported platforms")
        q.logger.log('Removing platform %s to supportedplatforms of %s'%(str(platform), self.name), 8)
        if isinstance(platform, (basestring, PlatformType)):
            if PlatformType.getByName(str(platform)) in self.supportedPlatforms:
                self.supportedPlatforms.remove(PlatformType.getByName(str(platform)))
            else:
                self._raiseError("Cannot find platform %s in qpackage metadata. Cannot be removed." %platform)
        else:
            self._raiseError("Cannot find platform %s, is it an existing type?" %platform)
        self.save()


#############################################################################
###############################  TASKLETS  ##################################
#############################################################################

    def _getTaskletEngine(self):
        metadatapath=self.getPathMetadata()
        if q.system.fs.exists(q.system.fs.joinPaths(metadatapath,"generic")):
            taskletspath=q.system.fs.joinPaths(metadatapath,"generic")
        else:
            taskletspath=q.system.fs.joinPaths(metadatapath,"tasklets")
        return q.taskletengine.get(taskletspath)

    def _hasTasklet(self, tag):
        engine = self._getTaskletEngine()
        return engine.find(tags=(tag)) != []

    def _executeTasklet(self, tag,action,dependencies=False, ensureTaskletExists=False, params={}):
        """
        execute tasklets of specific qpackage
        @param action is "install", "codeManagement","configure","package","backup","startstop"
        """
        #process all dependencies
        if dependencies:
            deps=self.getDependencies(recursive=True)
            for dep in deps:
                dep._executeTasklet(tag,action,dependencies)

        if not q.qp._activeQpackageIsActionsAlreadyExecuted(
            domain=self.domain,
            name=self.name,
            version=self.version,
            buildnr=self.buildNr,
            tag=tag,action=action): # is this really nessassary, what is the purpose?
                                                            # It will cause hard to find bugs
            self._log('executing tasklet ' + tag + ' ' + action)
            self.getState().setCurrentAction(tag,action)
            engine = self._getTaskletEngine()
            # Does not crash if we dont have the tasklet
            if ensureTaskletExists and not self._hasTasklet(tag):
                raise Exception('Tasklet ' + tag + ' not found.')
            _params = {'qpackage':self,'tag':tag,'action':action}
            _params.update(params)
            engine.execute(params=_params, tags=(tag,))
            self.getState().setCurrentActionIsDone()
            q.qp._activeQpackageSetActionsExecuted(domain=self.domain,
                                                   name=self.name,
                                                   version=self.version,
                                                   buildnr=self.buildNr,
                                                   tag=tag,action=action)
            return _params.get('result', None)


#############################################################################
##################################  CHECKS  #################################
#############################################################################

    def isUninstallable(self):
        ##self.assertAccessable()
        return self._hasTasklet('uninstall')


#############################################################################
####################################  GETS  #################################
#############################################################################

    def getIsPreparedForUpdatingFiles(self):
        """
        Returns true if package has been prepared
        """
        prepared = self.getState().prepared
        if prepared == 1:
            return True
        return False

    def getDependingInstalledPackages(self, recursive=False):
        '''
        Returns the packages that are dependent on this packages and installed on this machine
        This is a heavy operation and might take some time
        '''
        ##self.assertAccessable()
        if self.getDependingPackages(recursive=recursive) == None:
            raise RuntimeError("No depending packages present")
        [p for p in self.getDependingPackages(recursive=recursive) if p.isInstalled()]

    def getDependingPackages(self, recursive=False, platform=q.enumerators.PlatformType.GENERIC):
        '''
        Returns the packages that are dependent on this package
        This is a heavy operation and might take some time
        '''
        ##self.assertAccessable()
        return [p for p in q.qp.getQPackageObjects() if self in p.getDependencies(recursive=recursive, platform=platform)]


    def getState(self):
        ##self.assertAccessable()
        """
        from dir get [qbase]/cfg/qpackages4/state/$qpackagedomain_$qpackagename_$qpackageversion.state
        is a inifile with following variables
        * lastinstalledbuildNr
        * lastaction
        * lasttag
        * lastactiontime  epoch of last time an action was done
        * currentaction  ("" if no action current)
        * currenttag ("" if no action current)
        * lastexpandedbuildNr  (means expanded from tgz into qpackage dir)
        @return a QpackageStateObject
        """
        return QPackageStateObject(self)

    def getVersionAsInt(self):
        """
        translates string version representation to a number
        """
        ##self.assertAccessable()
        #@todo
        version=self.version
        return float(version)

    def getPathMetadata(self):
        """
        Returns absolute pathname of the package's metadatapath
        """
        domainobject=q.qp.getDomainObject(self.domain)
        if domainobject.metadataBranch.lower()<>self.branch.lower():
            return q.qp.getMetadataPath(self.domain,self.name,self.version,fromtmp=True)
        else:
            return q.qp.getMetadataPath(self.domain,self.name,self.version,fromtmp=False)

    def _ensureOnCorrectBranch(self):
        domainobject=q.qp.getDomainObject(self.domain)
        domainobject._ensureInitialized()
        if domainobject.metadataBranch.lower()<>self.branch.lower():
            if domainobject.hgclientTmp.getbranchname().lower() != self.branch.lower():
                raise RuntimeError('wrong branch!')
        else:
            if domainobject.hgclient.getbranchname().lower() != self.branch.lower():
                raise RuntimeError('wrong branch!')

    def getPathFiles(self):
        """
        Returns absolute pathname of the qpackage's filespath
        """
        ##self.assertAccessable()
        return q.qp.getDataPath(self.domain,self.name,self.version)


    def getPathSourceCode(self):
        """
        Returns absolute path to where this package's source can be extracted to
        """
        return q.system.fs.joinPaths(q.dirs.varDir, 'src', self.name, self.version)


    # Needed seperatly because we may also get the bundle from an ftp source
    def getBundleName(self, platform):
        """
        Returns the bundle name of the qpackage (dependant on the platform given)
        """
        return "%s__%s__%s__%s__%s.tgz" % (self.name, self.version, self.guid, self.bundleNr, str(platform))

    def getBundlePlatforms(self):
        """
        Returns all the platforms a bundle can be installed on
        """
        platform = q.platform.findPlatformType()
        platforms = []
        while platform != None:
            platforms.append(platform)
            platform = platform.parent
        return platforms

    # This is the local downloaded bundle
    def getPathBundle(self, bundleName):
        """
        Returns the path of the given bundle
        """
        return q.system.fs.joinPaths(q.qp.getBundlesPath(), self.domain, bundleName)
        #@todo return full path

    # This should be based on the Tmp repo
    # TODO
#    def getHighestBuildNr(self):
#        """
#        fetch the latest buildnr from the repo
#        a connection to bitbucket is required
#        """
#        domain=q.qp.getDomainObject(self.domain)
#        domain.hgclientTmp.pull()
#        domain.hgclientTmp.update("default")
#        qpackage=q.qp.get(self, domain, name, version,)
#        inifile       = q.tools.inifile.open(tmpPath)
#        buildNr       = int(inifile.getValue('main', 'build'))
#        return buildNr

    def getHighestInstalledBuildNr(self):
        """
        Returns the latetst installed buildnumber
        """
        ##self.assertAccessable()
        return self.getState().lastinstalledbuildnr

    def getBrokenDependencies(self, platform=None):
        """
        Returns a list of dependencies that cannot be resolved
        """
        ##self.assertAccessable()
        broken = []
        for dep in self.dependencies: # go over my dependencies
                                        # Do this without try catch
                                        # pass boolean to findnewest that it should return None instead of fail
            try:
                q.qp.findNewest(domain=dep.domain,name=dep.name, minversion=dep.minversion,maxversion=dep.maxversion,platform=platform)
            except Exception, e:
                print str(e)
                broken.append(dep)
        return broken


    def pm_getDependencies(self, dependencytype=None, platform=q.enumerators.PlatformType.GENERIC,recursive=False, depsfound=None, parent=None, depth=0, printTree=False, padding='', isLast=False, encountered=False):
        '''
        This will return the dependencies for the QPackage
        @param depsfound [[$domain,$name,$version]]
        @return [[parent,qpackageObject]]
        '''
        if q.enumerators.DependencyType4.check(dependencytype)==False and dependencytype<>None:
            raise RuntimeError("parameter dependencytype in get dependencies needs to be of type: q.enumerators.DependencyType4, now %s" % dependencytype)
        if q.enumerators.PlatformType.check(platform)==False and platform<>None:
            raise RuntimeError("parameter platform in get dependencies needs to be of type: q.enumerators.PlatformType, now %s" % platform)
        depsfoundToReturn=[]

        if depsfound == None:
            depsfound=set()

        childPadding=''
        if printTree: # print myself
            end = ''
            # The dependencies my children visit do not affect the dependency i visit
            # but my children cannot decent into dependency I already decented into
            end = '*'      if encountered            else ''
            prefix = '\''  if isLast else '|'
            childPadding  = padding + (' ' if isLast else '|') + '   '
            q.console.echo(padding + prefix + '--' + str(self) + end)

        if not encountered:
            for i in range(len(self.dependencies)): # go over my dependencies
                dep = self.dependencies[i]
                found=False
                if dep.dependencytype == dependencytype or dependencytype==None:
                    for plat in dep.supportedPlatforms:
                        #print str(plat) + '.hasParent(' + str(platform) + ')'
                        if plat.has_parent(platform):
                            found = True
                if found:
                    #dependenciesAlreadyFound=[d for parent,d in depsfound]
                    # If We encounter an exception keep printing the tree
                    # so we can see all missing packages in one go

                    # If platform is generic, than we look for a package supporting generic?
                    # Thus we look for a package supporting all platforms? Or do we look for packages supporting any of the enumerated platforms?
                    # We need the do the latter, so the definition of findNewest should reflect this!
                    depqpackage      = q.qp.findNewest(domain=dep.domain,name=dep.name, minversion=dep.minversion,maxversion=dep.maxversion,platform=platform, returnNoneIfNotFound=True)
                    if not depqpackage:
                        self._log('dependency ' + str(dep) + ' could not be resolved for package ' + str(self))
                        continue
                    childEncountered = str(depqpackage) in depsfound
                    childDeptsFound  = depsfound
                    if not childEncountered:
                        depsfound.add(str(depqpackage))
                        depsfoundToReturn.append(depqpackage)
                    if printTree:
                        #childDeptsFound = set(depsfound)
                        pass
                    if recursive:
                        depsfoundToReturn.extend(depqpackage.pm_getDependencies(dependencytype, platform,recursive, childDeptsFound,depqpackage, depth + 1, printTree, childPadding, i == len(self.dependencies) - 1, childEncountered))
        return depsfoundToReturn #only returns the new ones



    def getDependencyTree(self, platform=q.enumerators.PlatformType.GENERIC):
        '''
        This will return the Build dependencies for the QPackage
        '''
        ##self.assertAccessable()
        self.pm_getDependencies(None, platform,recursive=True, printTree=True)

    def getBuildDependencyTree(self, platform=None):
        '''
        This will return the Build dependencies for the QPackage
        '''
        ##self.assertAccessable()
        self.pm_getDependencies(q.enumerators.DependencyType4.BUILD, platform,recursive=True, printTree=True)

    def getRuntimeDependencyTree(self, platform=None):
        '''
        This will return the runtime dependencies for the QPackage, will not recurse into the dependencies
        '''
        ##self.assertAccessable()
        self.pm_getDependencies(q.enumerators.DependencyType4.RUNTIME, platform,recursive=True, printTree=True)

    def getDependencies(self, platform=q.enumerators.PlatformType.GENERIC,recursive=False):
        '''
        This will return the Build dependencies for the QPackage
        '''
        ##self.assertAccessable()
        res = self.pm_getDependencies(None, platform,recursive)
        res.sort()
        return res

    def getBuildDependencies(self, platform=None,recursive=False):
        '''
        This will return the Build dependencies for the QPackage
        '''
        ##self.assertAccessable()
        res = self.pm_getDependencies(q.enumerators.DependencyType4.BUILD, platform,recursive)
        res.sort()
        return res

    def getRuntimeDependencies(self, platform=None,recursive=False):
        '''
        This will return the runtime dependencies for the QPackage, will not recurse into the dependencies
        '''
        ##self.assertAccessable()
        res = self.pm_getDependencies(q.enumerators.DependencyType4.RUNTIME, platform,recursive)
        res.sort()
        return res


#############################################################################
################################  CHECKS  ###################################
#############################################################################

    def hasModifiedFiles(self):
        """
        Returns true if the files have been modified
        Returns false if the files haven't been modified
        """
        ##self.assertAccessable()
        if self.getState().prepared == 1:
            return True
        return False

    def hasModifiedMetaData(self):
        """
        Returns True if the files have been modified
        Returns False if the files haven't been modified
        """
        ##self.assertAccessable()
        return self in q.qp.getDomainObject(self.domain).getQPackageTuplesWithModifiedMetadata()

    def isInstalled(self):
        """
        Returns True if the package is installed
        Returns False if the package isn't installed
        """
        ##self.assertAccessable()
        return self.getState().lastinstalledbuildnr != -1

    def supportsPlatform(self, platform):
        """
        Returns True if the specified platform is supported by the package
        Returns False if the specified platform isn't supported by the package
        """
        if not platform:
            return True
        for supportedPlatform in self.supportedPlatforms:
            if platform.has_parent(supportedPlatform):
                return True
        # To be complete we should check if we support all children of the platform
        # Then to we support the platform.. these situation may occur in the packages


#############################################################################
#################################  ACTIONS  ################################
#############################################################################

    def update(self):
        """
        Will reinstall the package
        """
        ##self.assertAccessable()
        # Should this download the new meta information?? NO
        self.install()

    def backup(self, url):
        """
        Runs the backup tasklet
        @param url where to back up to, e.g. : ftp://login:passwd@10.10.1.1/myroot/
        """
        ##self.assertAccessable()
        tag="backup"
        action="backup"
        ##url = q.console.askString('Url to backup to')
        self._executeTasklet(tag,action,params={'backupurl':url})
        self._log('backuped to ' + url)
        ## qpackage.backup(backupurl="ftp://login:passwd@10.10.1.1/myroot/")
        ## qpackage.restore(backupurl="ftp://login:passwd@10.10.1.1/myroot/")

    def restore(self, url):
        """
        Runs the backup tasklet
        @param url where to restore from, e.g. : ftp://login:passwd@10.10.1.1/myroot/
        """
        ##self.assertAccessable()
        tag="backup"
        action="restore"
        ##url = q.console.askString('Url to restore from')
        self._executeTasklet(tag,action,params={'backupurl':url})
        self._log('restored from ' + url)

    #Checks out the code to un unkwown place
    def start(self):
        """
        uns the startstop tasklet
        """
        ##self.assertAccessable()
        tag="startstop"
        action="start"
        self._executeTasklet(tag,action)
        self._log('start')

    # populates the files directory based on the source that is in an unknown location
    def stop(self):
        """
        Runs the startstop tasklet
        """
        ##self.assertAccessable()
        tag="startstop"
        action="stop"
        self._executeTasklet(tag,action)
        self._log('stop')

    def restart(self):
        """
        Runs the startstop tasklet
        """
        ##self.assertAccessable()
        tag="startstop"
        action="restart"
        self._executeTasklet(tag,action)
        self._log('restart')

    def getStatus(self):
        """
        Runs the startstop tasklet
        """
        ##self.assertAccessable()
        tag="startstop"
        action="getStatus"
        status = self._executeTasklet(tag,action)
        self._log('getStatus')
        return status

    def install(self,dependencies=True,download=True,reinstall=False, path=''):
        """
        Runs the install tasklet
        @param dependencies: if True, all dependencies will be installed too
        @param download:     if True, bundles of package will be downloaded too
        @param reinstall:    if True, package will be reinstalled
        """
        ##self.assertAccessable()
        #print 'possibly installing ' + str(self) + ' path : ' + path
        #pdb.set_trace()



        self._log('install')

        #state=self.getState()

        # If I am already installed assume my dependencies are also installed
        if self.buildNr <= self.getState().lastinstalledbuildnr and not reinstall:
            self._log('already installed')
            return # Nothing to do

        q.action.start('Installing %s' % str(self), 'Failed to install %s' % str(self))

        # Check apt dependecies
        recipe_file = q.system.fs.joinPaths(self.getPathMetadata(), 'recipe.json')
        if q.system.fs.exists(recipe_file):
            recipe = json.loads(q.system.fs.fileGetContents(recipe_file))
            q.platform.ubuntu.check() # To make sure our cache is initialized
            for repo in recipe:
                if "apt-dependencies" in repo:
                    for apt in repo["apt-dependencies"]:
                        if apt in q.platform.ubuntu._cache and not q.platform.ubuntu._cache[apt].is_installed:
                            q.platform.ubuntu.install(apt)

        if dependencies:
            deps=self.getDependencies()
            for dep in deps:
                dep.install(path= path + ',' + str(self))

        tag="install"
        action="install"
        if download:
            self.download(dependencies=False)
        self._expand() #expand all tgz in qpackage dir
        if reinstall or self.buildNr > self.getState().lastinstalledbuildnr:
            #print 'really installing ' + str(self)
            self._log('installing')
            if self.getState().checkNoCurrentAction==False:
                raise RuntimeError ("qpackage is in inconsistent state, ...")
            self._executeTasklet(tag,action,dependencies=False)
            self.getState().setLastInstalledBuildNr(self.buildNr)

        q.extensions.pm_sync()

        q.action.stop(False)

    # Make sure there are no longer installed packages that depend on me
    def uninstall(self, unInstallDependingFirst=False):
        '''
        Invokes the uninstall tasklet, but only if there are no longer dependent installed packages on this package
        So you should first uninstall all packages that are dependent on this package and then uninstall this package,
        or you can just set the unInstallDependingFirst param and then this method will do it for you.
        '''
        ##self.assertAccessable()
        if unInstallDependingFirst:
            for p in self.getDependingInstalledPackages():
                p.uninstall(True)
        if self.getDependingInstalledPackages(True):
            raise RuntimeError('Other package on the system dependend on this one, uninstall them first!')
        tag="install"
        action="uninstall"
        state=self.getState()
        if state.checkNoCurrentAction==False:
            raise RuntimeError ("qpackage is in inconsistent state, ...")
        self._log('uninstalling' + str(self))
        # If we don't have an uninstall tasklet we crash here.. I suppose
        self._executeTasklet(tag,action)
        state.setLastInstalledBuildNr(-1)

    def isUninstallable(self):
        # Does no work since we cannot look inside a package..
        return True
        #return self._hasTasklet('uninstall')

    def prepareForUpdatingFiles(self, forceDownload=False, suppressErrors=False):
        """
        After this command the operator can change the files of the qpackage.
        This command will generate the default tasklets: backup, codemanagement, configure, install, package, startstop.
        """
        ##self.assertAccessable()
        q.system.fs.createDir(self.getPathFiles())
        QPackageDefaultFilesGenerator(self).createDefaultFiles() # self._createDefaultFiles() ?? can I do this?
        if not self.hasModifiedFiles():
            self.getState().setPrepared(1)
            if not self.isNew():
                self.download(forceDownload=forceDownload, suppressErrors=suppressErrors)
                self._expand(suppressErrors=suppressErrors)

    def isNew(self):
        # We are new when our files have not yet been committed
        # check if our qpackage.cfg file in the repo is in the ignored or added categories
        domainObject = q.qp.getDomainObject(self.domain)
        cfgPath = q.system.fs.joinPaths(self.getPathMetadata(), 'qpackage.cfg')
        return not domainObject._isTrackingFile(cfgPath)

    def copyFiles(self):
        """
        Copy the files from package dir to sandbox
        """
        _qpackageDir = self.getPathFiles()

        self._log('Syncing %s to sandbox' % _qpackageDir)
        platformDirsToCopy = self._getPlatformDirsToCopy()
        for platformDir in platformDirsToCopy:
            self._log('Syncing files in <%s>'%platformDir)
            self._copyFilesTo(platformDir, q.dirs.baseDir)

    def configure(self,dependencies=False):
        """Runs the configure tasklet"""

        q.action.start('Configuring %s' % str(self), 'Failed to configure %s' % str(self))

        tag="configure"
        action=""
        ##self.assertAccessable()
        self._executeTasklet(tag,action,dependencies)
        self.getState().setIsPendingReconfiguration(False)
        self._log('configure')

        q.action.stop(False)

    def checkout(self):
        """Runs the codemanagement tasklet if present """
        ##self.assertAccessable()
        tag="codemanagement"
        action="checkout"
        if self._hasTasklet(tag):
            self._executeTasklet(tag,action)
        self._log('checkout')

    def _getRelativeRecipe(self):
        recipefile = q.system.fs.joinPaths(self.getPathMetadata(), 'recipe.json')
        if not q.system.fs.exists(recipefile):
            return
        recipe = json.loads(q.system.fs.fileGetContents(recipefile))
        for repo in recipe:
            connection = i.config.clients.mercurial.findByUrl(repo['location'])
            connection.pullupdate()
            branch = repo.get('branch', 'default')
            connection.switchbranch(branch)
            for repolocation, qbaselocation in repo['mapping'].iteritems():
                repofulllocation = q.system.fs.joinPaths(connection.basedir, repolocation)
                yield repofulllocation, qbaselocation

    def checkoutRecipe(self):
        iterator = self._getRelativeRecipe()
        sourcecode = self.getPathSourceCode()
        if not iterator:
            return
        q.system.fs.removeDirTree(sourcecode)
        for repofulllocation, qbaselocation in iterator:
            qbasefull = q.system.fs.joinPaths(sourcecode, qbaselocation)
            q.system.fs.copyDirTree(repofulllocation, qbasefull)

    def installDebug(self):
        iterator = self._getRelativeRecipe()
        if not iterator:
            raise RuntimeError("No recipe defined for this qpackage")
        for repofulllocation, qbaselocation in iterator:
            parts = qbaselocation.split("/")
            platform = parts[0]
            platformtype = q.enumerators.PlatformType.getByName(platform)
            if platformtype not in self.getBundlePlatforms():
                continue
            qbaselocation = qbaselocation.replace(platform, "", 1)
            if qbaselocation.startswith("/"):
                qbaselocation = qbaselocation[1:]
            qbasefull = q.system.fs.joinPaths(q.dirs.baseDir, qbaselocation)
            answer = True
            if q.system.fs.exists(qbasefull):
                answer = q.console.askYesNo("Folder %s exists, remove and link to repo?" % qbasefull)
            if answer:
                q.system.fs.removeDirTree(qbasefull)
                q.system.fs.symlink(repofulllocation, qbasefull)



    # populates the files directory based on the source that is in an unknown location
    def compile(self):
        """Runs the compile tasklet if present """
        ##self.assertAccessable()
        tag="compile"
        action=""
        if self._hasTasklet(tag):
            self._executeTasklet(tag,action)
        self._log('compile')

    def package(self):
        """ Runs the package tasklet if present """
        ##self.assertAccessable()
        if not self.getIsPreparedForUpdatingFiles():
            raise RuntimeError('Cannot package if not prepared')
        tag="package"
        action=""
        if self._hasTasklet(tag):
            self._executeTasklet(tag,action)
        self._log('package')

    def download(self,dependencies=False, destinationDirectory=None, suppressErrors=False, forceDownload=False,allplatforms=False):
        """
        downloads the qpackage, the destination directory parameter allows you to overwrite
        the default destination (opt/qbase/var/qpackages4/bundles)
        """

        q.action.start('Downloading %s' % str(self), 'Failed to download %s' % str(self))

        if dependencies:
            deps=self.getDependencies(recursive=True)
            for dep in deps:
                dep.download(dependencies=False, destinationDirectory=destinationDirectory)

        domain     = q.qp.getDomainObject(self.domain)

        self._log('Downloading bundles for package ' + str(self))
        state      = self.getState()
        foundOne   = False
        for platform in self.getBundlePlatforms():
            bundleName = self.getBundleName(platform)
            if destinationDirectory != None:
                bundleFile = q.system.fs.joinPaths(destinationDirectory, domain.domainname, bundleName)
            else:
                bundleFile = self.getPathBundle(bundleName)
            sourceFile = q.system.fs.joinPaths(domain.bundleDownload, bundleName) #location to download bundle from
            self._log("Check bundle file exists %s" % bundleFile)
            if q.system.fs.exists(bundleFile) and forceDownload==False:
                #we are not forced to download so if we find the file there is good enough
                foundOne=True
            checksum = self.getChecksum(platform)
            download = True
            if q.system.fs.exists(bundleFile):
                if checksum:
                    download = q.tools.hash.sha256(bundleFile) != checksum
                else:
                    download = False
            if download or forceDownload:
                if q.cloud.system.fs.sourcePathExists(sourceFile):
                    #download from source to local dir
                    self._log('Trying to download from  ' + sourceFile)
                    self._downloadFile(sourceFile, bundleFile, checksum)
                    #@todo function above not throw an exception if this fails! (info nick)
                    if not q.system.fs.exists(bundleFile):
                        raise RuntimeError("%s was not downloaded well to %s" % (sourceFile,bundleFile))
                    state.setLastDownloadedBuildNr(self.buildNr)
                    foundOne=True
                    self._log('Successfully downloaded bundle for package ' + str(self) + ' from domain ' + sourceFile)
                elif checksum:
                    raise RuntimeError("Failed to download %s while checksum was given" % sourceFile)
            else:
                self._log('bundle %s was already downloaded' % bundleFile)
                state.setLastDownloadedBuildNr(self.buildNr)


        if foundOne==False:
            if not suppressErrors:
                raise RuntimeError('Could not find a bundle for %s on central or local repo.' % bundleName)
            else:
                q.action.stop(True)
                return False

        q.action.stop(False)
        return True

    def _downloadFile(self, url, destinationpath, checksum, retry=1):
        valid = False
        actual_checksum = None
        while not valid and retry >= 0:
            q.cloud.system.fs.copyFile(url, 'file://' +  destinationpath)
            if checksum:
                actual_checksum = q.tools.hash.sha256(destinationpath)
                if actual_checksum != checksum:
                    retry -= 1
                    continue
            valid = True
        if not valid:
            q.system.fs.remove(destinationpath)
            raise RuntimeError("Checksum mismatch for file %s retrieved from %s\nGot checksum %s expected %s" % (destinationpath, url, actual_checksum, checksum))


###################################################################
########################  ACTIONS PRIVATE  ########################
###################################################################

    def _getBundleFiles(self):
        for platform in q.platform.ALL:
            bundleName = self.getBundleName(platform)
            bundleFile = self.getPathBundle(bundleName)
            if q.system.fs.exists(bundleFile):
                yield platform, bundleName, bundleFile


    # upload the bundle
    def _upload(self):
        """
        upload qpackage
        """
        self._log('Begin Uploading bundles for package ' + str(self) + ' ... (Please wait)')
        source     = q.qp.getDomainObject(self.domain)
        if source.bundleUpload == None:
            raise RuntimeError('Uploading not supported, no bundleupload property specified for domain ' + source)
        for platform, bundleName, bundleFile in self._getBundleFiles():
            sourceFile = q.system.fs.joinPaths(source.bundleUpload, bundleName)
            q.cloud.system.fs.copyFile('file://' +  bundleFile, sourceFile) # Add protocol, Of cource upload will not work for all protocols (http)
            self._log('Successfully uploaded bundle for package ' + str(self) + ' to source ' + sourceFile)

    # Needed in some codemanagement tasklets
    def extract(self, suppressErrors=False):
        self._expand(suppressErrors)

    def expand(self, suppressErrors=False):
        self._expand(suppressErrors)

    # Expands the bundle to files so we have the artifacts ready to be installed
    def _expand(self, suppressErrors=False):
        ##self.assertAccessable()
        state=self.getState()
        if state.lastexpandedbuildnr == self.buildNr:
            self._log('already expanded')
            return # nothing to do
        state.setCurrentAction('expand', 'default')
        for platform in self.getBundlePlatforms():
            bundleName = self.getBundleName(platform)
            bundleFile = self.getPathBundle(bundleName)
            dataPath   = q.qp.getDataPath(self.domain,self.name,self.version)
            if not q.system.fs.exists(bundleFile):
                continue
            self._log("expand action")
            checksum = self.getChecksum(platform)
            if checksum:
                actual_checksum = q.tools.hash.sha256(bundleFile)
                if actual_checksum != checksum:
                    raise RuntimeError("Checksum mismatch for file %s\nGot checksum %s expected %s" % (bundleFile, actual_checksum, checksum))
            q.system.fs.targzUncompress(bundleFile, q.system.fs.joinPaths(dataPath, str(platform)))
            state.setLastExpandedBuildNr(self.buildNr)
        state.setCurrentActionIsDone()

#    def _copyFilesToSandbox(self):          #Todo: function still being used???
#        ##
#        ##Copy Files from package dir to sandbox
#        ##@param dirName: name of the directory to copy
#        ##
#        _qpackageDir = self.getPathFiles()
#
#        q.logger.log('Syncing %s to sandbox' % _qpackageDir, 5)
#        platformDirsToCopy = self._getPlatformDirsToCopy()
#        print 'platformDirsToCopy: ' + str(platformDirsToCopy)
#        if False:
#            try:
#                t = 1/0
#            except:
#                import traceback
#                print '\n'.join(traceback.format_stack())
#        for platformDir in platformDirsToCopy:
#            q.logger.log('Syncing files in <%s>'%platformDir, 5)
#            self._copyFilesTo(platformDir, q.dirs.baseDir)

    def _getPlatformDirsToCopy(self):
        ##
        ##Return a list of platform related directories to be copied in sandbox
        ##@param dirName: name of the directory to look in
        ##
        platformDirs = list()
        platform = q.platform

        _qpackageDir = self.getPathFiles()

        platformSpecificDir = q.system.fs.joinPaths(_qpackageDir, str(platform), '')

        if q.system.fs.isDir(platformSpecificDir):
            platformDirs.append(platformSpecificDir)

        genericDir = q.system.fs.joinPaths(_qpackageDir, 'generic', '')

        if q.system.fs.isDir(genericDir):
            platformDirs.append(genericDir)

        if platform.isUnix():
            unixDir = q.system.fs.joinPaths(_qpackageDir, 'unix', '')
            if q.system.fs.isDir(unixDir):
                platformDirs.append(unixDir)

            if platform.isSolaris():
                sourceDir = q.system.fs.joinPaths(_qpackageDir, 'solaris', '')
            elif platform.isLinux():
                sourceDir = q.system.fs.joinPaths(_qpackageDir, 'linux', '')
            elif platform.isDarwin():
                sourceDir = q.system.fs.joinPaths(_qpackageDir, 'darwin', '')

        elif platform.isWindows():
            sourceDir = q.system.fs.joinPaths(_qpackageDir, 'win', '')

        if q.system.fs.isDir(sourceDir):
            if not str(sourceDir) in platformDirs:
                platformDirs.append(sourceDir)

        return platformDirs

    def _copyFilesTo(self, sourceDir, destination):


        ##
        ##Copy Files
        ##@param sourceDir: directory to copy files from
        ##@param destination: directory to copy files to
        ##


        def createAncestors(file):
            # Create the ancestors
            q.system.fs.createDir(q.system.fs.getDirName(file))

        if sourceDir [-1] != '/':
            sourceDir = sourceDir + '/'
        prefixHiddenFile = sourceDir + '_'

        if q.system.fs.isDir(sourceDir):

            files     = q.system.fs.walk(sourceDir, recurse=True, return_folders=True,followSoftlinks=False)
            for file in files:

                # Remove hidden files and directories:
                if file.find ( prefixHiddenFile ) == 0 :
                    continue

                destinationFile = q.system.fs.joinPaths(destination, file[len(sourceDir):])
                createAncestors(destinationFile)
                if q.system.fs.isLink( file ) :
                    q.system.fs.symlink( os.readlink( file ), destinationFile, overwriteTarget=True )
                elif q.system.fs.isDir (file) :
                    q.system.fs.createDir( destinationFile )
                else:
                    q.system.fs.copyFile(file, destinationFile)

            self._log('Syncing done')

        else :
            self._log('Directory <%s> does not exist'%sourceDir)


    # if there is not files directory we create one and generate an empty tar
    # we also put out a warning
    # we compress the files (artfacts) to a bundle
    def _compress(self, overwriteIfExists=False):
        state=self.getState()
        if self.guid=="":
            self._raiseError( "Cannot find qpackage.")
        state.setCurrentAction('compressing', 'default')
        datapath  = q.qp.getDataPath(self.domain,self.name,self.version)
        if not q.system.fs.exists(datapath):
            return # Nothing to do
        platforms = set([q.system.fs.getBaseName(platform) for platform in q.system.fs.listDirsInDir(datapath)])
        platforms.add('generic')
        for platform in platforms:
            platformdir = q.system.fs.joinPaths(datapath, platform)
            bundleName = self.getBundleName(platform)
            bundleFile = self.getPathBundle(bundleName)
            if not q.system.fs.exists(platformdir):
                if str(platform) != 'generic' :
                    continue
                else:
                    q.system.fs.createDir(platformdir)
                    self._log('created directory ' + datapath)
            if not q.system.fs.exists(q.system.fs.getDirName(bundleFile)):
                q.system.fs.createDir(q.system.fs.getDirName(bundleFile))
            q.system.fs.targzCompress(platformdir, bundleFile)
        state.setCurrentActionIsDone()
        self.save()

    #
    # Generate default files
    #

########################################################################
#########################  RECONFIGURE  ################################
########################################################################

    def signalConfigurationNeeded(self):
        """
        Sets in the corresponding qpackage's state file if reconfiguration is needed
        """
        self.getState().setIsPendingReconfiguration(True)
        q.qp._setHasPackagesPendingConfiguration(True)

    def isPendingReconfiguration(self):
        """
        Returns True if the package needs reconfiguration
        Returns False if the package doesn't need reconfiguration
        """
        if self.getState().getIsPendingReconfiguration() == 1:
            return True
        return False


#########################################################################
#######################  SUPPORTING FUNCTIONS  ##########################

    def _raiseError(self,message):
        ##self.assertAccessable()
        message="%s : %s_%s_%s" % (message,self.domain,self.name,self.version)
        raise RuntimeError(message)

    def _clear(self):
        ##self.assertAccessable()
        """
        empty all properties appart from domain,name,version
        """
        self.tags=[]
        self.supportedPlatforms=[]
        self.buildNr=0
        self.dependencies=[]

    def __cmp__(self,other):
        if other == None or other=="":
            return False
        return self.name == other.name and str(self.domain) == str(other.domain) and q.qp._getVersionAsInt(self.version)==q.qp._getVersionAsInt(other.version)

    def __repr__(self):
        return self.__str__()

    def getInteractiveObject(self):
        """
        Returns the interactive version of the qpackage object
        """
        ##self.assertAccessable()
        return QPackageIObject4(self)

    def _resetPreparedForUpdatingFiles(self):
        self.getState().setPrepared(0)

    def __str__(self):
        return "QPackage %s %s %s" % (self.domain,self.name,self.version)

    def __eq__(self, other):
        return str(self) == str(other)

    def _log(self, mess):
        q.logger.log(str(self) + ':' + mess, 3)

    def reportNumbers(self):
        return ' metaNr:' + str(self.metaNr) + ' bundleNr:' + str(self.bundleNr) + ' buildNr:' + str(self.buildNr)
