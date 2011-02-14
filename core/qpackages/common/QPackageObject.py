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
from pymonkey.inifile import IniFile
from pymonkey.baseclasses import BaseType
from pymonkey.enumerators import PlatformType, QPackageQualityLevelType
from pymonkey.baseclasses.dirtyflaggingmixin import DirtyFlaggingMixin
from pymonkey.enumerators import QPackageQualityLevelType
from pymonkey.qpackages.common.DomainObject import DomainObject
from pymonkey.qpackages.common.DependencyDef import DependencyDef
from pymonkey.qpackages.common.enumerators import DependencyType

class QPackageObject(BaseType, DirtyFlaggingMixin):
    ''' Data representation of a QPackage, should contain all information contained in the qpackage.cfg '''
    
    domain = q.basetype.object(DomainObject, doc='The domain this QPackage belongs to', allow_none=True, default=None)
    name = q.basetype.string(doc='Name of the QPackage should be lowercase', allow_none=False)
    version = q.basetype.string(doc='Version of a string', allow_none=False)
    buildNr = q.basetype.dictionary(doc='Build number of the QPackage, keyed on the qualityLevel', allow_none=False, default=dict())
    supportedPlatforms = q.basetype.list(doc='List of PlatformTypes',allow_none=False, default=list())
    tags = q.basetype.list(doc='list of tags describing the QPackage', allow_none=True, default=list())
    description = q.basetype.string(doc='Description of the QPackage, can be larger than the description in the VList', allow_none=True, flag_dirty=True, default='')
    dependencies = q.basetype.list(doc='List of DependencyDefinitions for this QPackage', allow_none=True, default=list())
    qpackageType = q.basetype.string(doc='Type of the QPackage', allow_none=True, default='')
    _rootPath = q.basetype.path(doc='Root path location of the qpackage', allow_none=True) 

    def __init__(self, domain, name, version, rootPath=q.dirs.packageDir, new=False):
        ''' initialization of the QPackage 
        
        @param domain:  The domain that the QPackage belongs to, can be a string or the DomainObject
        @param name:    The name of the QPackage
        @param version: The version of the QPackage
        @param rootPath: The base path where to find the package, this is by default the packageDir, but can be set to another dir.
        @param new:     if True we will create a new config and set it's defaults.
        '''
        
        ##q.logger.log('Initializing the QPackage Object %s - %s - %s'%(domain, name, version), 6)
        #checks on correctness of the parameters
        if domain and not isinstance(domain, (basestring, DomainObject)):
            raise ValueError('The domain parameter must be a string or a DomainObject.')
        if not name:
            raise ValueError('The name parameter cannot be empty or None')
        if not version:
            raise ValueError('The version parameter cannot be empty or None')
        
        self.domain = DomainObject(str(domain))
        self.name = name
        self.version = version
        self._rootPath = rootPath
        if new:
            self.createConfig()
        else:
            self.parseConfig()
        q.logger.log('Initialization of the QPackage %s has finished'%str(self), 6)

    def parseConfig(self):
        ''' Get the needed information from the config file 
        If the configfile does not exist, then it will be created.
        '''
        q.logger.log('Start parsing the configuration file of the QPackage %s'%str(self), 6)
        cfg = self._getIniFile()
        # get the comma separated list of tags, loop over them and add to the tagslist in the QPackage 
        tagsList = str(cfg.getValue('main', 'tags')).split(',')
        q.logger.log('Parsing QPackage %s, tags = %s'%(str(self), cfg.getValue('main','tags')), 8)
        for tag in tagsList:
            if tag and tag.strip() not in self.tags:
                self.tags.append(tag.strip())
        self.description = cfg.getValue('main', 'description')
        q.logger.log('Parsing QPackage %s, description = %s'%(str(self), self.description), 8)
        # get the comma separated list of platform types, then loop over then and add them to the QPackage list.
        supPlatforms = str(cfg.getValue('main', 'supportedPlatforms')).split(',')
        q.logger.log('Parsing QPackage %s, supportedPlatforms = %s'%(str(self), cfg.getValue('main', 'supportedPlatforms')), 8)
        for platform in supPlatforms:
            if platform and PlatformType.getByName(platform.strip()) not in self.supportedPlatforms:
                self.supportedPlatforms.append(PlatformType.getByName(platform.strip()))
        # get the qualityLevel we are using and set the buildNr
        for section in cfg.getSections():
            if str(section).startswith('ql_'):
                key = section[3:].strip()
                self.buildNr[key]=cfg.getValue(section, 'buildNr')
                q.logger.log('Parsing QPackage buildNr for %s, %s = %s'%( str(self), key, self.buildNr[key] ), 8)
        dependencies = list()
        #get Dependency definitions (runtime)
        for section in cfg.getSections():
            # only check sections that contain dep_ or depbuild_
            if str(section).startswith('dep_') or str(section).startswith('depbuild_'):
                dep = DependencyDef()
                if str(section).startswith('depbuild'):
                    dep.dependencyType = DependencyType.BUILD
                    dep.name = section[9:]
                    q.logger.log('Parsing QPackage build dependency for %s, %s'%( str(self), dep.name ), 8)
                else:
                    dep.dependencyType = DependencyType.RUNTIME
                    dep.name = section[4:]
                    q.logger.log('Parsing QPackage dependency for %s, %s'%( str(self), dep.name ), 8)
                
                dep.domain = cfg.getValue(section, 'domain')
                q.logger.log('Parsing %s dependency %s, domain: %s'%( str(dep.dependencyType), dep.name, dep.domain ), 8)
                dep.minversion = cfg.getValue(section, 'minversion')
                q.logger.log('Parsing %s dependency %s, minversion: %s'%( str(dep.dependencyType), dep.name, dep.minversion ), 8)
                dep.maxversion = cfg.getValue(section, 'maxversion')
                q.logger.log('Parsing %s dependency %s, maxversion: %s'%( str(dep.dependencyType), dep.name, dep.maxversion ), 8)
                supPlatforms = str(cfg.getValue(section, 'supportedPlatforms')).split(',')
                q.logger.log('Parsing %s dependency %s, supportedPlatforms = %s'%(str(dep.dependencyType), dep.name, cfg.getValue('main', 'supportedPlatforms')), 8)
                for platform in supPlatforms:
                    if platform:
                        dep.supportedPlatforms.append(PlatformType.getByName(platform.strip()))
                dependencies.append(dep)
        self.dependencies  = dependencies

    def createConfig(self):
        ''' Will create a qpackage.cfg file in it correct location, if one exists, we will overwrite it. '''
        cfgDir = q.system.fs.joinPaths(self._rootPath, self.getRelativeQPackagePath(), 'cfg')

        if not q.system.fs.isDir(cfgDir):
            q.logger.log('The folder %s does not exist, creating'%cfgDir, 6)
            q.system.fs.createDir(cfgDir)
        cfgPath = q.system.fs.joinPaths(cfgDir, 'qpackage.cfg')

        q.logger.log('The qpackage.cfg file for %s does not exist, creating default one'%str(self), 6)
        cfgIni = IniFile(cfgPath, create=True)
        # create the main section.
        self._generateMain(cfgIni)
        self.updateQualityLevels()

    def pm_getDependencies(self, dependencyType, platform):
        '''
        This will return the dependencies for the QPackage, will not recurse into the dependencies
        '''
        deps = list()
        for dep in self.dependencies:
            if dep.dependencyType == dependencyType:
                if not platform:
                    deps.append(dep)
                    continue
                for plat in dep.supportedPlatforms:
                    if PlatformType.getByName(platform).has_parent(plat):
                        deps.append(dep)
                        
        return deps

    def getBuildDependencies(self, platform=None):
        '''This will return the Build dependencies for the QPackage, will not recurse into the dependencies
        '''
        return self.pm_getDependencies(DependencyType.BUILD, platform)

    def getRuntimeDependencies(self, platform=None):
        ''' This will return the runtime dependencies for the QPackage, will nor recurse into the dependencies
        '''
        return self.pm_getDependencies(DependencyType.RUNTIME, platform)

    def addDependency(self, domain, name, supportedPlatforms, minversion=None, maxversion=None, dependencyType='runtime'):
        ''' Add a dependency definition to the cfg file. 
        @param domain:             domain of the QPackage you wish to depend on
        @param name:               name of the QPackage
        @param supportedPLatforms: list of the supported platforms for that QPackage dependency
        @param minversion:         minimal version of the QPackage dependency
        @param maxversion:         maximal version of the QPackage dependency
        @param dependencyType:     Dependency Type (build, runtime)'''

        if not domain or not isinstance(domain, (basestring, DomainObject)):
            raise ValueError('The domain parameter must be a string or a DomainObject.')
        if not name:
            raise ValueError('The name parameter cannot be empty or None')
        if not supportedPlatforms:
            raise ValueError('The supportedPlatforms parameter must not contain an empty list')

        if isinstance(supportedPlatforms, str):
            supportedPlatforms = supportedPlatforms.split(',')

        cfg = self._getIniFile()
        if DependencyType.getByName(str(dependencyType).strip()) == DependencyType.RUNTIME:
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
        self.parseConfig()

    def addSupportedPlatform(self, platform):
        ''' Add a supported platform to the QPackage
        @param platform: string or PlatformType
        '''
        q.logger.log('Adding platform %s to supportedplatforms of %s'%(str(platform), self.name), 8)
        if isinstance(platform, (basestring, PlatformType)):
            cfg = self._getIniFile()
            sups = ''
            if PlatformType.getByName(str(platform)) not in self.supportedPlatforms:
                for sup in self.supportedPlatforms:
                    sups += '%s, '%(str(sup).strip())
                sups += '%s, '%(str(platform).strip())
                cfg.setParam('main', 'supportedplatforms', sups)
        self.parseConfig()

    def addTag(self, tag):
        ''' Adding a tag to the QPackage
        @param tag: string
        '''
        q.logger.log('Adding tag "%s" to the QPackage %s'%(tag, self.name), 8)
        if not tag in self.tags:
            self.tags.append(tag)
            inifile = self._getIniFile()
            inifile.setParam('main', 'tags', ', '.join(self.tags))
            self.parseConfig()
        else:
            q.logger.log('QPackage %s already contains the "%s" tag'%(self.name, tag), 8)

    def setDescription(self, description):
        ''' Sets the description of the QPackage
        @param description: Description for the QPackage
        '''
        q.logger.log('Setting description "%s" to the QPackage %s'%(description, self.name), 8)
        inifile = self._getIniFile()
        inifile.setParam('main', 'description', description)
        self.parseConfig()

    def removeTag(self, tag):
        ''' Removing a tag from the QPackage
        @param tag: string
        '''
        q.logger.log('Removing tag "%s" to the QPackage %s'%(tag, self.name), 8)
        if tag in self.tags:
            self.tags.remove(tag)
            inifile = self._getIniFile()
            inifile.setParam('main', 'tags', ', '.join(self.tags))
        else:
            raise ValueError('QPackage does not have the tag you are trying to remove')

    def updateConfig(self):
        self.createConfig()
        for dependency in self.dependencies:
            self.addDependency(dependency.domain, dependency.name, dependency.supportedPlatforms,\
                                     minversion=dependency.minversion, maxversion=dependency.maxversion,\
                                     dependencyType=dependency.dependencyType)

    def removeSupportedPlatform(self, platform):
        ''' Remove a supported platform from the QPackage
        @param platform: string of PlatformType to remove
        '''
        q.logger.log('Removing platform %s to supportedplatforms of %s'%(str(platform), self.name), 8)
        if isinstance(platform, (basestring, PlatformType)):
            cfg = self._getIniFile()
            if PlatformType.getByName(str(platform)) in self.supportedPlatforms:
                self.supportedPlatforms.remove(PlatformType.getByName(str(platform)))
            sups = ''
            for sup in self.supportedPlatforms:
                sups+= '%s, '%(str(sup).strip())
            cfg.setParam('main', 'supportedplatforms', sups)
        self.parseConfig()

    def removeDependency(self, name, dependencyType='runtime'):
        ''' Remove a dependency.
        You can remove only a dependency completely. If you wish to change a dependency, just do an addDependency and we will overwrite it.

        @param name:           name of the QPackage
        @param dependencyType: Dependency Type (build, runtime)
        '''
        q.logger.log('Removing %s dependency %s from %s'%(str(dependencyType), name, self.name), 8)
        if not dependencyType or not isinstance(dependencyType, (basestring, DependencyType)):
            raise ValueError('The domain parameter must be a string or a DomainObject.')
        if not name:
            raise ValueError('The name parameter cannot be empty or None')

        cfg = self._getIniFile()
        if DependencyType.getByName(str(dependencyType).strip()) == DependencyType.RUNTIME:
            sectionName = 'dep_%s'%name
        else:
            sectionName = 'depbuild_%s'%name
        if not cfg.checkSection(sectionName):
            raise RuntimeError('Section %s not found in the qpackage.cfg for QPackage %s'%(sectionName, self))
        q.logger.log('Found section %s for dependency %s in QPackage %s'%(sectionName, name, self.name), 8)
        cfg.removeSection(sectionName)
        cfg.write()
        self.parseConfig()

    def save(self):
        ''' Checks what fields are dirty and saves them to the cfg file.'''
        inifile = self._getIniFile()
        if 'description' in self.dirtyProperties:
            inifile.setParam('main', 'description', self.description)
        #always set the lists and dicts as there is no dirty status when appending or removing items.
        for dependency in self.dependencies:
            self.addDependency(dependency.domain, dependency.name, dependency.supportedPlatforms, minversion=dependency.minversion, \
                               maxversion=dependency.maxversion, dependencyType=dependency.dependencyType)
        inifile.setParam('main', 'tags', ', '.join(self.tags))
        sups = ''
        for sup in self.supportedPlatforms:
            sups += '%s, '%( str(sup).strip())
        inifile.setParam('main', 'supportedplatforms', sups)

    def _getIniFile(self):
        ''' returns the IniFile object of the QPackage
        '''
        # check whether the QPackage has a config file.
        cfgPath = self.pm_getCfgFilePath()
        # if the file does not exist we have a problem and should raise.
        q.logger.log('Checking path %s'%cfgPath,8)
        if not q.system.fs.exists(cfgPath):
            raise RuntimeError('QPackage configuration has not been found for QPackage %s' % self)

        return IniFile(cfgPath)

    def getRelativeQPackagePath(self):
        ''' Returns the relative path for the QPackage starting from the domain '''
        return q.system.fs.joinPaths(self.domain.name, self.name, self.version)

    def getRelativeBuildPath(self, qualityLevel):
        ''' Returns the relative path for the QPackage with it's buildnr for the given qualityLevel

        @param qualityLevel: qualityLevel for the buildNr, if empty take the q.qshellconfig...'''
        if not isinstance(qualityLevel, (basestring, QPackageQualityLevelType)):
            raise ValueError('qualityLevel must be a correct qualityLevel in stringformat or object')
        if str(qualityLevel) in self.buildNr.iterkeys():
            return q.system.fs.joinPaths(self.getRelativeQPackagePath(), self.buildNr[str(qualityLevel)])
        else:
            return q.system.fs.joinPaths(self.getRelativeQPackagePath(), 'upload_%s'%str(qualityLevel))

    def pm_getCfgFilePath(self):
        ''' Constructs the path of the qpackage.cfg '''
        cfgPath = q.system.fs.joinPaths(self._rootPath, self.getRelativeQPackagePath(), 'cfg', 'qpackage.cfg')
        return cfgPath

    def _generateMain(self, inifile):
        ''' Generate the main section from the current object.
        @param inifile: The Ini file for the object. Should be a PyMonkey IniFile
        '''
        inifile.addSection('main')
        inifile.setParam('main', 'domain', self.domain.name)
        inifile.setParam('main', 'name', self.name)
        inifile.setParam('main', 'version', self.version)
        sups = ''
        for sup in self.supportedPlatforms:
            sups += '%s, '%( str(sup).strip())
        inifile.setParam('main', 'supportedPlatforms', sups)
        inifile.setParam('main', 'tags', ','.join(self.tags))
        inifile.setParam('main', 'description', self.description)
        inifile.setParam('main', 'type', self.qpackageType)

    def updateQualityLevels(self):
        ''' This will generate the qualityLevels part of the config file for the QPackage '''
        inifile = self._getIniFile()
        for key in self.buildNr.iterkeys():
            if inifile.checkSection('ql_%s'%key):
                inifile.setParam('ql_%s'%key, 'buildnr', self.buildNr[key])
            else: 
                inifile.addSection('ql_%s'%key)
                inifile.setParam('ql_%s'%key, 'buildnr', self.buildNr[key])

    def pm_getACL(self):
        ''' Constructs an QPackage ACL object and returns it '''
        pass

    def __cmp__(self,other):
        from pymonkey.qpackages.common.QPackageVersioning import QPackageVersioning
        return self.name == other.name and str(self.domain) == str(other.domain) and QPackageVersioning.versionCompare(self.version, other.version)

    def __str__(self):
        return '%s %s'%(self.name, self.version)
    def __repr__(self):
        return self.__str__()