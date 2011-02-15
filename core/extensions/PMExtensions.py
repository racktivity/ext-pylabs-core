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

import cStringIO
import imp
import os
import pkg_resources
import sys
import zipfile

import pylabs
import pylabs.inifile
import pylabs.extensions.PMExtensionsGroup as PMExtensionsGroup
from pylabs.extensions.PMExtension import PMExtension, EggPMExtension

SYSTEM_EXTENSIONS = list()
HOOK_POINTS = dict()

def find_eggs(path):
    """
    Helper for egg loader functions

    @param path: path to find the eggs on
    @type path: string
    @return: a list of eggs
    @rtype: list
    """
    eggs, errors = pkg_resources.working_set.find_plugins(
        pkg_resources.Environment([path])
    )
    return eggs

class pylabsZipFile(zipfile.ZipFile):
    """Extends the Python 2.5 zipfile ZipFile class to add a Python 2.6 like
    open method that returns a file pointer"""
    def open(self, name, mode='r'):
        if mode != 'r':
            raise RuntimeError("Only read-only file access supported")

        content = self.read(name)
        return cStringIO.StringIO(content)

class ExtensionFactory(object):
    """Simple factory baseclass for BasePMExtension objects"""
    def build(self, extensionPath, moduleName, className, pmExtensionName):
        """
        Create a new BasePMExtensions object

        @param extensionPath: the extension root (dirname of the extension.cfg file)
        @type extensionPath: string
        @param moduleName: name of the module containing the root class of this extension
        @type moduleName: string
        @param className: name of the root class of this extension
        @type className: string
        @param pmExtensionName: name used to expose class under q.[one or more extensionsgroup's].[pmExtensionName]
        @type pmExtensionName: string
        @return: a freshly instantiated extension
        @rtype: L{pylabs.extensions.PMextension.BasePMExtension}
        """
        raise NotImplementedError

class PMExtensionFactory(ExtensionFactory):
    """Simple factory class for PMExtension objects"""
    def build(self, extensionPath, moduleName, className, pmExtensionName):
        return PMExtension(extensionPath, moduleName, className, pmExtensionName)

class EggPMExtensionFactory(ExtensionFactory):
    """Simple factory class for EggPMExtension objects"""
    def build(self, extensionPath, moduleName, className, pmExtensionName):
        return EggPMExtension(extensionPath, moduleName, className, pmExtensionName)

class ExtensionInfoFinder(object):
    """Base class for extension info finders"""

    def __init__(self, rootDir, extensionConfigName="extension.cfg", warn_old_extensions=True):
        self.rootDir = rootDir
        self.extensionConfigName = extensionConfigName
        self.warn_old_extensions = warn_old_extensions

    def find(self):
        """
        This method starts a scan for extensions and returns information about
        each found extension. Must be implemented by children.
        """
        raise NotImplementedError

    def _hasOldStyleSection(self, inifile):
        """
        To warn the user about old extensions, this method can be used
        to detect them.

        @param inifile: inifile of an extension
        @type inifile: L{pylabs.inifile.IniFile.IniFile}
        @return: wether the inifile contains old style sections
        @rtype: boolean
        """
        sections = inifile.getSections()
        return 'main' in sections

    def _getHookInformation(self, inifile, path, factory):
        """
        Extract the hook information from an inifile. path and factory are
        are extra parameters to be added to each information dict.

        @param inifile: inifile that should be scanned for extension information
        @type inifile: L{pylabs.inifile.IniFile.IniFile}
        @param path: internal extension path
        @type path: string
        @param factory: factory to create the extension described in the INI file
        @type factory: L{PMExtensionFactory}
        @return: a list of dicts containing extension information
        @rtype: list of dicts
        """
        sections = inifile.getSections()
        hookInformationList = list()
        for hookid in sorted(section for section in sections if section.startswith('hook')):
            pylabs.q.logger.log('Found hook %s in %s' % (hookid, inifile, ), 7)
            # Extract the information from the section
            hookInformation = self._extractHookInformation(inifile, hookid)
            if not hookInformation:
                continue
            # Add global information
            hookInformation['extension_path'] = path
            hookInformation['extension_factory'] = factory
            hookInformationList.append(hookInformation)
        return hookInformationList

    def _extractHookInformation(self, inifile, section):
        """
        Extract hook information from an INI file section

        @param inifile: INI file containing the section with the hook information
        @type inifile: L{pylabs.inifile.IniFile.IniFile}
        @param section: section of the INI file that contains the hook information
        @type section: string
        @return: hook information
        @rtype: dict
        """
        if self.warn_old_extensions and self._hasOldStyleSection(inifile):
            #This is most likely an old-style extension
            import warnings
            warnings.warn('Extension %s contains a main section in the extension.cfg file, please update it' % \
                    dir[len(pylabs.q.dirs.extensionsDir) + 1:] if dir.startswith(pylabs.q.dirs.extensionsDir) else dir)
            # Explicit None for clarity
            return None

        qlocation = inifile.getValue(section, "qlocation")
        modulename = inifile.getValue(section, "modulename")
        classname = inifile.getValue(section, "classname")
        enabled = inifile.getBooleanValue(section,"enabled")

        hook = {
            'qlocation': qlocation,
            'modulename': modulename,
            'classname': classname,
            'enabled': enabled,
            'hookid': section,
        }
        return hook

class PyExtensionInfoFinder(ExtensionInfoFinder):
    """Extension info finder class for normal extensions"""

    def find(self):
        """
        Find all extensions and hooks defined in them
        """
        extension_hooks = list()
        #Find all extension names
        dirs = pylabs.q.system.fs.listDirsInDir(self.rootDir, True,findDirectorySymlinks=True)
        # Use a simple PMExtensionFactory
        factory = PMExtensionFactory()
        for dir in (d for d in dirs if pylabs.q.system.fs.exists(os.path.join(d, self.extensionConfigName))):
            #we found possible extension because extension.cfg file found
            pylabs.q.logger.log('Found extension in %s' % dir, 6)
            # Load extension ini file
            configfilePath = os.path.join(dir, self.extensionConfigName)
            inifile = pylabs.inifile.IniFile(configfilePath)
            path = pylabs.q.system.fs.getDirName(configfilePath)
            hooks = self._getHookInformation(inifile, path, factory)
            extension_hooks.extend(hooks)

        return extension_hooks

class EggExtensionInfoFinder(ExtensionInfoFinder):
    """Extension info finder class for egg extensions"""
    def find(self):
        """
        Find the extensions info for extensions in egg format
        """
        extension_hooks = list()
        eggs = find_eggs(self.rootDir)
        factory = EggPMExtensionFactory()
        for egg in eggs:
            # Add egg to path so other parts of pylabs can import its contents
            eggfile = egg.location
            sys.path.append(eggfile)
            for filePointer, path in self._generateExtensionConfigFilePointers(eggfile):
                inifile = pylabs.inifile.IniFile(filePointer)
                hooks = self._getHookInformation(inifile, path, factory)
                extension_hooks.extend(hooks)
        return extension_hooks

    def _generateExtensionConfigFilePointers(self, eggFileName):
        """
        Generate file pointers and paths for each extension config file in a egg file.

        The generated paths are the internal paths of the extensions in the
        egg file.

        Note: this is a generator! It does not return a list.

        @param eggFileName: name of the egg file
        @type eggFileName: string
        @return: generates (file pointers, path) pairs
        @rtype: generator
        """
        # Always use forward slashes in eggs
        sep = "/"
        eggFile = pylabsZipFile(eggFileName)
        for internalFileName in eggFile.namelist():
            parts = internalFileName.split(sep)
            if parts and parts[-1] == self.extensionConfigName:
                # construct egg path i.e.
                # /opt/qbase2/lib/pylabs/extensions/my_extension.egg/my_first_extension/
                # This format is supported by the eggfile module
                path = sep.join([eggFileName] + parts[:-1])
                yield eggFile.open(internalFileName), path

# Change this list to add extra kinds of extensions
# Normal extensions are loaded first
EXTENSION_INFO_FINDER_CLASSES = [PyExtensionInfoFinder, EggExtensionInfoFinder]

class PMExtensions:
    """
    all functionality required to load all extensions
    """
    def __init_properties__(self):    
        self.pmExtensionsGroup={}
        self.extensionsRootPath="" #rootdir of extensions

    def __init__(self, hook_base_object, hook_base_name):
        self.hook_base_object = hook_base_object
        self.hook_base_name = hook_base_name
        self.extensionLocationCache = dict()

        HOOK_POINTS[hook_base_name] = self
        
    def init(self):
        self.__init_properties__()
        if not pylabs.q.system.fs.exists(pylabs.q.dirs.extensionsDir):
            raise RuntimeError("Cannot find extensions dir")
        self.extensionsRootPath = pylabs.q.dirs.extensionsDir

        self._extensionInfoFinders = [klass(self.extensionsRootPath) for klass in EXTENSION_INFO_FINDER_CLASSES]

    def findExtensionInfo(self, warn_old_extensions=True):
        hooks = list()
        for infoFinder in self._extensionInfoFinders:
            infoFinder.warn_old_extensions = warn_old_extensions
            hooks.extend(infoFinder.find())
        return hooks

    def findExtensions(self):
        """
        Initialize all extensions in extensionsRootPath, attach to baseObject
        """
        if SYSTEM_EXTENSIONS:
            self._populateExtensions()
            return

        pylabs.q.logger.log('Loading pylabs extensions from %s' % self.extensionsRootPath,7)

        #Add extensions base dir to sys.path
        sys.path.append(self.extensionsRootPath)

        SYSTEM_EXTENSIONS.extend(self.findExtensionInfo())

        self._populateExtensions()

    def _populateExtensions(self):
        for hook in SYSTEM_EXTENSIONS:
            if hook['qlocation'].startswith(self.hook_base_name):
                self._populateExtension(hook['extension_path'], hook)

    def _populateExtension(self,extensionPath, hookInfo):
        qlocation = hookInfo['qlocation']
        modulename = hookInfo['modulename']
        classname = hookInfo['classname']
        enabled = hookInfo['enabled']
        extensionFactory = hookInfo['extension_factory']

        pylabs.q.logger.log('Found %s hook %s.%s to be hooked on %s' % (
                                'enabled' if enabled else 'disabled',
                                modulename, classname,
                                qlocation), 7)

        if enabled == True:
            self._hook_extension(extensionFactory, extensionPath, modulename, classname, qlocation)

        pylabs.q.logger.log('Finished loading hook', 7)

    #We need this to be public
    populateExtension = _populateExtension


    def _hook_extension(self, extensionFactory, extensionPath, modulename, classname, qlocation):
        pylabs.q.logger.log('Hooking %s.%s of extension in %s on %s' % (
                                modulename, classname,
                                extensionPath,
                                qlocation,
                              ), 6)
        pmExtensionName = qlocation.rpartition('.')[-1]

        extension = extensionFactory.build(extensionPath, modulename, classname, pmExtensionName)

        #Attach extension instance to q object at given mountpoint (qlocation)
        qlocationparts = qlocation.split('.')[1:-1]
        current = self.hook_base_object
        #@todo cleanup c&n don't mean anything
        for part in qlocationparts:
            c = getattr(current, part, None)
            if c:
                current = c
                continue
            if current is self.hook_base_object:
                #parent is q object
                n = PMExtensionsGroup.PMExtensionsGroup(self)
            else:
                n = PMExtensionsGroup.PMExtensionsGroup(current)
            setattr(current, part, n)
            current = n

        # Check extension location cache if location is free
        mountedExtension = self.extensionLocationCache.get(qlocation, None)
        if mountedExtension:
            # If type of the mounted extension is an instance of the class of
            # the new extension, raise an error.
            if isinstance(extension, mountedExtension.__class__):
                raise RuntimeError("Cannot mount %s on mountpoint "
                "%s, because %s of similar type is already mounted"
                " there" % (extension, qlocation, mountedExtension))
            else:
                pylabs.q.errorconditionhandler.raiseWarning("Cannot mount %s on "
                    "requested mountpoint %s, because %s of other type is "
                    "already mounted there." % (
                        extension, qlocation, mountedExtension
                    ), 6)
                return

        #Don't allow overwriting unknown attribute on same location
        if hasattr(current, pmExtensionName):
            raise RuntimeError("Cannot mount %s on mountpoint %s because "
                "unknown object %s is already mounted there" % (
                    extension, qlocation, getattr(current, pmExtensionName)
                ))

        #We only support lazy loading on extensionsGroup's otherwise we will load here (no lazy loading)
        if isinstance(current, PMExtensionsGroup.PMExtensionsGroup):
            current.pm_addExtension(extension)
        else:
            extension.activate()
            setattr(current, pmExtensionName, extension.instance)

        # Add the mounted extension to the cache
        self.extensionLocationCache[qlocation] = extension