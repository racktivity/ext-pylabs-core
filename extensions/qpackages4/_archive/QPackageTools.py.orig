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
from pymonkey.qpackages.client.QPackageInstallerHelper import QPackageInstallerHelper
from pymonkey.qpackages.client.QPackageConfigure import QPackageConfigure
from zipfile import ZipFile
import py_compile, os, re, sys

class QPackageTools(object):
    """
    Set of methods which can be executed on a qpackage for package management
    is located on q.qpackagetools and used in tasklets for installation, building, codemgmt, ...
    """
    
    def getSitePackageDir(self) :
        return q.system.fs.joinPaths(q.dirs.baseDir, "lib","python","site-packages")

    def createEggZipFromSandboxDir(self, sourceSandboxDir, targetEggFileName,append=False):

        """
        Creates a half hatched egg file from sourceSandboxDir directory. Half hatched eggs are zip files containing your python code without the egg manifest files.
        @param sourceSandboxDir: the path of the directory containing your python code that'll be put inside the egg
        @param targetEggFileName: that name of the resulted egg file, should end with .egg.zip and it shouldn't contain any version number or build number
        """

        eggFile = ZipFile(targetEggFileName,"w" if not append else "a")
        sourceSandboxDir = sourceSandboxDir.rstrip('/')
        parentSandboxDir = q.system.fs.getDirName(sourceSandboxDir)
        baseSandboxDir = q.system.fs.getBaseName(sourceSandboxDir)
        q.logger.log("Creating egg %s from  %s " % (targetEggFileName, sourceSandboxDir), 3)
        q.system.fs.changeDir(parentSandboxDir)
        for filepath in q.system.fs.walk(baseSandboxDir, True, "*.py"):
            pyfilepath = filepath
            pycfilepath = filepath + "c"
            py_compile.compile(pyfilepath, pycfilepath)
            eggFile.write(pyfilepath)
            eggFile.write(pycfilepath)
        eggFile.close()

    def copyEggToSandbox(self, sourceEggZipFile, targetEggFile):
        """
        Copy *.egg.zip file from packagedir to sandbox.
        Add EGG-INFO/PKG-INFO file in the egg; use proper egg filename
        """
        # Step 1: copy *.egg.zip file
        q.system.fs.copyFile(sourceEggZipFile, targetEggFile)

        # Step 2: Parse name and version of egg
        filename = q.system.fs.getBaseName(targetEggFile)
        import re
        mo = re.match("^(?P<name>[_A-Z]+)-(?P<version>([0-9]+\.)+)(?P<buildNr>[0-9]+)", filename, re.I)
        groupdict = mo.groupdict()
        name = groupdict['name']
        version = groupdict['version'][:-1]
        buildNr = groupdict['buildNr']
        
        # Step 3: Bake egg
        import zipfile
        z = zipfile.ZipFile(targetEggFile, 'a')
        eggString = "Metadata-Version: 1.0\nName: %s\nVersion: %s\n" % (name, "%s.%s"%(version, buildNr))
        z.writestr('EGG-INFO/PKG-INFO', eggString)
        z.close()

        # Step 4: Check to add egg to path
        import pkg_resources
        # WorkingSet checks the eggs in current sys.path
        working_set = pkg_resources.WorkingSet()
        requirement = pkg_resources.Requirement.parse(name)
        # Search for eggs with this eggs name in the working set
        egg = working_set.find(requirement)
        if not egg:
            # No egg with this eggs name on sys.path
            sys.path.append(targetEggFile)

    def signalConfigurationNeeded(self, qpackageObject):
        """
        Sets flag to indicate that the configuration tasklet for this qpackage should run next time the Q-Shell starts.
        At the end of the install procedure of a qpackage dependency tree, the user will be asked to restart Q-Shell. (If there's at least one qpackage with a reconfigure request outstanding.) 
        Compare this to installing a few new programs on Windows, and then requiring a reboot of the system.
        After restarting, configure tasklets are executed in the order at which the framework.reconfigure() requests were received.
        The Configure-tasklets should set some default configuration (e.g. configure an apache default site) and start the application if it's a service.
        @param qpackageObject: qpackageObject to signal
        """
        configure = QPackageConfigure()
        configure.signalForConfiguration(qpackageObject.name, qpackageObject.version, qpackageObject.domain)

    def convertSourceToPyc(self, src, dstDir):
        """
        Clones src to dstDir but with all python files being compiled to .pyc files
        @param src: path of the directory containing python source files
        @param dstDir: destination directory, if it doesn't exist then it's the resulted clone name
        """
        q.logger.log('Cloning directory tree from %s to %s and compiling py files there'% (src, dstDir),3)
        if ((src is None) or (dstDir is None)):
            raise TypeError('Not enough parameters passed in system.fs.copyDirTree to copy directory from %s to %s '% (src, dstDir))
        if q.system.fs.isDir(src):
            names = os.listdir(src)
            if not q.system.fs.exists(dstDir):
                q.system.fs.createDir(dstDir)
            errors = []
            for name in list(names):
                srcname = q.system.fs.joinPaths(src, name)
                dst = q.system.fs.joinPaths(dstDir, name)
                try:
                    if q.system.fs.isDir(srcname):
                        self.convertSourceToPyc(srcname, dst)
                    else:
                        if re.search('\.py$',srcname):
                            compiledFile = srcname + "c"
                            compiledDstFile = dst + "c"
                            py_compile.compile(srcname,compiledFile)
                            q.system.fs.copyFile(compiledFile, compiledDstFile)
                            q.system.fs.removeFile(compiledFile)
                        else:
                            if q.system.fs.exists(srcname):
                                q.system.fs.copyFile(srcname, dst)
                except (IOError, os.error), why:
                    errors.append((srcname, dst, why))
            if errors:
                raise Exception (errors)
        else:
            raise RuntimeError('Source path %s in system.fs.copyDirTree is not a directory'% src)

    def getPythonVersion(self):
        """
        Returns python version in the form of x.x "i.e 2.5"
        """
        return '.'.join([str(x) for x in sys.version_info[:2]])

    def requireQPackage(self, domain, name, version, installLatestBuild=False):
        ''' This method will install the QPackage you requested

        If the QPackage is already installed with the correct version it will do nothing.
        If the QPackage is installed, but wrong version it will update it.
        If the QPackage is installed with correct version, but not the latest build it will
        update it if installLatestBuild is set to True

        @param domain: Domain of the QPackage you wish to install
        @type domain: string
        @param name: Name of the QPackage you wish to install
        @type name: string
        @param version: Version of the QPackage you wish to install
        @type version: string
        @param installLatestBuild: (optional) If True the QPackage will be updated to latest build 
        @type installLatestBuild: bool
        '''
        q.logger.log('require called for QPackage %s version %s on domain %s'%(name, version, domain), 5)
        qpackages = q.qpackages.qpackageFind(name=name, version=version, domain=domain, qualityLevels=q.qpackages.getDefaultQualityLevel(), state='SERVER')
        if q.qpackages.qpackageIsInstalled(name, version, domain):
            if installLatestBuild and qpackages and \
              qpackages[0].buildNr > q.qpackages.qpackageGetInstalledBuildNr(name, version, domain):
                q.logger.log('Found a QPackage with higher buildnr, updating to build %s now' % qpackages[0].buildNr, 5)
                qpackages[0].install(processRuntimeDependencies=True, downloadAllFiles=False)
            return
        if qpackages:
            q.logger.log('Found a QPackage, installing now', 5)
            qpackages[0].install(processRuntimeDependencies=True, downloadAllFiles=False)
        else:
            # We should not check multiple returns as we are using the exactMatch.
            raise RuntimeError('No QPackages found with name:%s, version:%s, domain:%s'%(name, version, domain))

    def enableExtension(self, extensionCfg):
        ''' This method will set the extension to enabled

        @param extensionCfg: Full path to the inifile of the extension
        @type extensionCfg: string
        '''

        if not q.system.fs.exists(extensionCfg):
            q.eventhandler.raiseCriticalError("File %s does not exist!" % extensionCfg)
        inif = q.tools.inifile.open(extensionCfg)
        for section in inif.getSections():
            inif.setParam(section, 'enabled', '1')
        inif.write()

    def __str__(self):
        return 'qpackages.client.QPackageTools' 

    def __repr__(self):
        return self.__str__()

    sitepackageDir = property(fget=getSitePackageDir, doc="Python site-packages directory\n@type: string\n")
