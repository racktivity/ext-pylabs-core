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
from pylabs.sync.Sync import SyncLocal

class QPackageInstallerHelper(BaseType):
    """
    Installer class which contains helper methods to install the content of a qpackage.
    This helper method is passed on as a parameter to the qpackage's install script.
    """
    qpackageName = q.basetype.string(doc='Name of the qpackage')
    domain = q.basetype.string(doc = 'Domain of the qpackage')
    newVersion = q.basetype.string(doc = 'Version of the new qpackage to install')
    newBuildNr = q.basetype.string(doc = 'Build number of the new qpackage to install')
    
    def __init__(self, qpackageName, domain, newVersion, newBuildNr):
        self.qpackageName = qpackageName
        self.domain = domain
        self.newVersion = newVersion
        self.newBuildNr = newBuildNr
        self._qpackageDir= q.system.fs.joinPaths(q.dirs.packageDir, self.domain, self.qpackageName, 
                                             self.newVersion, self.newBuildNr)
        if not q.system.fs.exists(self._qpackageDir):
            raise RuntimeError("QPackageDir does not exist: [%s]" % self._qpackageDir)
        self._localSync = SyncLocal(self._qpackageDir)

    def copyFilesToSandbox(self, dirName='files'):
        """
        Copy Files from package dir to sandbox
        @param dirName: name of the directory to copy
        """
        q.logger.log('Syncing %s dir to sandbox'%dirName, 5)
        platformDirsToCopy = self.getPlatformDirsToCopy(dirName)
        for platformDir in platformDirsToCopy:
            q.logger.log('Syncing files in <%s>'%platformDir, 5)
            self.copyFilesTo(platformDir, q.dirs.baseDir)

    def copyTaskletsToSandbox(self):
        """
        Copy Tasklets dir from package dir to sandbox
        """
        q.logger.log('Syncing tasklets dir to sandbox', 5)
        platformDirsToCopy = self.getPlatformDirsToCopy('tasklets')
        destinationDir = q.system.fs.joinPaths(q.dirs.baseDir, 'tasklets', 'qpackages', self.domain, self.qpackageName, self.newVersion)
        if not q.system.fs.exists(destinationDir):
            q.system.fs.createDir(destinationDir)
        for platformDir in platformDirsToCopy:
            q.logger.log('Syncing files in <%s>'%platformDir, 5)
            self.copyFilesTo(platformDir, destinationDir)
        
    def getPlatformDirsToCopy(self, dirName='files'):
        """
        Return a list of platform related directories to be copied in sandbox
        @param dirName: name of the directory to look in
        """
        platformDirs = list()
        platform = q.platform

        platformSpecificDir = q.system.fs.joinPaths(self._qpackageDir, dirName, str(platform), '')

        if q.system.fs.isDir(platformSpecificDir):
            platformDirs.append(platformSpecificDir)

        genericDir = q.system.fs.joinPaths(self._qpackageDir, dirName, 'generic', '')

        if q.system.fs.isDir(genericDir):
            platformDirs.append(genericDir)

        if platform.isUnix():
            unixDir = q.system.fs.joinPaths(self._qpackageDir, dirName, 'unix', '')
            if q.system.fs.isDir(unixDir):
                platformDirs.append(unixDir)

            if platform.isSolaris():
                sourceDir = q.system.fs.joinPaths(self._qpackageDir, dirName, 'solaris', '')
            elif platform.isLinux():
                sourceDir = q.system.fs.joinPaths(self._qpackageDir, dirName, 'linux', '')
            elif platform.isDarwin():
                sourceDir = q.system.fs.joinPaths(self._qpackageDir, dirName, 'darwin', '')

        elif platform.isWindows():
            sourceDir = q.system.fs.joinPaths(self._qpackageDir, dirName, 'win', '')

        if q.system.fs.isDir(sourceDir):
            if not str(sourceDir) in platformDirs:
                platformDirs.append(sourceDir)

        return platformDirs

    def copyFilesTo(self, sourceDir, destination):
        """
        Copy Files
        @param sourceDir: directory to copy files from
        @param destination: directory to copy files to
        """
        if q.system.fs.isDir(sourceDir):
            q.logger.log('Syncing files from <%s> to <%s>'%(sourceDir, destination), 5)
            self._localSync.enableKeepPermissionsOwnerGroup() # Preserve rights, owner, ...
            self._localSync.setDestinationDir(destination)
            self._localSync.setSourceDir(sourceDir)
            self._localSync.do()
            q.logger.log('Syncing done', 5)
        else:
            q.logger.log('Directory <%s> does not exist'%sourceDir, 5)