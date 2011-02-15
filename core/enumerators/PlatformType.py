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

# Preparation for returning the platformtype of the system
import sys, os, re
import pylabs
from pylabs.baseclasses import BaseEnumeration

def _useELFtrick(file):
    fd=os.open(file, os.O_RDONLY)
    out = os.read(fd,5)
    if out[0:4]!="\x7fELF":
        result = 0 # ELF trick fails...
    elif out[4] == '\x01':
        result = 32
    elif out[4] == '\x02':
        result = 64
    else:
        result = 0
    os.close(fd)
    return result

class PlatformType(BaseEnumeration):
    '''Platform representation'''

    @staticmethod
    def findPlatformType():
        '''Discovers the platform and sets the C{PlatformType} to the retrieved platform'''
        _platform = None
        if sys.platform.startswith("linux"):
            bits = _useELFtrick("/sbin/init")
            if bits == 32:
                _platform = PlatformType.LINUX32
            elif bits == 64:
                _platform = PlatformType.LINUX64
            else:
                _platform = PlatformType.UNKNOWN
            if os.path.exists("/proc/vmware"):
                _platform = PlatformType.ESX

        elif sys.platform.startswith("sunos"):
            import commands
            _, bits = commands.getstatusoutput('isainfo -b')
            bits = int(bits)
            if bits == 32:
                _platform = PlatformType.SOLARIS32
            elif bits == 64:
                _platform = PlatformType.SOLARIS64
            else:
                _platform = PlatformType.UNKNOWN

        elif sys.platform.startswith("win"):
            # todo: find a way to distinguish win32 from win64
            _platform = PlatformType.WIN32

        elif sys.platform.startswith("cygwin"):
            _platform = PlatformType.CYGWIN

        elif sys.platform.startswith("darwin"):
            _platform = PlatformType.DARWIN

        else:
            _platform = PlatformType.OTHER

        return _platform

    @staticmethod
    def findSandboxType():
        '''Discovers the platform and sets the C{PlatformType} to the retrieved platform'''
        _platform = None
        from pylabs import q
        _pythonPath = q.system.fs.joinPaths(q.dirs.baseDir, "bin", "python")
        if sys.platform.startswith("linux"):
            bits = _useELFtrick(_pythonPath)
            if bits == 32:
                _platform = PlatformType.LINUX32
            elif bits == 64:
                _platform = PlatformType.LINUX64
            else:
                _platform = PlatformType.UNKNOWN
            if os.path.exists("/proc/vmware"):
                _platform = PlatformType.ESX

        elif sys.platform.startswith("sunos"):
            bits = _useELFtrick(_pythonPath)
            if bits == 32:
                _platform = PlatformType.SOLARIS32
            elif bits == 64:
                _platform = PlatformType.SOLARIS64
            else:
                _platform = PlatformType.UNKNOWN

        elif sys.platform.startswith("win"):
            # todo: find a way to distinguish win32 from win64
            _platform = PlatformType.WIN32

        elif sys.platform.startswith("cygwin"):
            _platform = PlatformType.CYGWIN

        elif sys.platform.startswith("darwin"):
            _platform = PlatformType.DARWIN

        else:
            _platform = PlatformType.OTHER

        return _platform

    def getVersion(self):
        """
        Get Version of Operating System
        Only Solaris is currently supported. Executing <uname -v>
        """
        if self.isSolaris():
            exitcode, output = pylabs.q.system.process.execute("uname -v", outputToStdout=False)

            matchresult = re.search("[snv_|osce-](\d+)", output)
            if matchresult:
                return int(matchresult.groups()[0])
            else:
                raise ValueError("Executed [uname -v] Expected output ." % output)
        else:
            raise OSError('Unsupported Platform (%s)'%pylabs.q.platform)

    def __init__(self, vappFolderName, parent=None):
        '''Initialization
        
        @param vappFolderName: The name of the folder to be used inside the files folder of vapps for this specific platform
        @param parent: The parent L{PlatformType}
        '''
        self._vappFolderName = vappFolderName
        self._parent = parent

    def has_parent(self, parent):
        '''Check whether the provided parent L{PlatformType} is a parent of this type'''
        if isinstance(parent,str):
            parent = PlatformType.getByName(parent)
        current = self
        while current:
            if current == parent:
                return True
            current = current.parent
        return False

    def getChildren(self, recursive=False):
        if not recursive:
            return [p for p in PlatformType.ALL if p.parent == self]
        else:
            children = self.getChildren()
            res      = []
            for c in children:
                res.append(c)
                res.extend(c.getChildren(recursive=True))
            return res

    def isUnix(self):
        '''Checks whether the platform is Unix-based'''
        return self.has_parent(PlatformType.UNIX)

    def isWindows(self):
        '''Checks whether the platform is Windows-based'''
        return self.has_parent(PlatformType.WIN)

    def isLinux(self):
        '''Checks whether the platform is Linux-based'''
        return self.has_parent(PlatformType.LINUX)

    def isGeneric(self):
        '''Checks whether the platform is generic (they all should)'''
        return self.has_parent(PlatformType.GENERIC)

    def isSolaris(self):
        '''Checks whether the platform is Solaris-based'''
        return self.has_parent(PlatformType.SOLARIS)

    def isESX(self):
        '''Checks whether the platform is VMware ESX based'''
        return self.has_parent(PlatformType.ESX)

    def isDarwin(self):
        '''Checks whether the platform is darwin'''
        return self.has_parent(PlatformType.DARWIN)

    #TODO Remove this in-time when PlatformType storage in vapps is fixed
    def _get_name(self):
        '''Compatibility function for non-Enumeration-based PlatformTypes'''
        try:
            return self._pm_enumeration_name
        except AttributeError:
            return self._name

    name = property(fget=_get_name, doc='Platform name')
    vappFolderName = property(fget=lambda s: s._vappFolderName, doc='Folder name of files folder in vapps')
    parent = property(fget=lambda s: s._parent, doc='Parent platform')

    def __repr__(self):
        return str(self)

#PlatformType.registerItem(type,vappfoldername,parent)
PlatformType.registerItem('generic', 'shared')
PlatformType.registerItem('unix', 'unixshared', PlatformType.GENERIC)
PlatformType.registerItem('linux', 'linuxshared', PlatformType.UNIX)
PlatformType.registerItem('linux32', 'linux32', PlatformType.LINUX)
PlatformType.registerItem('linux64', 'linux64', PlatformType.LINUX)
PlatformType.registerItem('win', 'winshared', PlatformType.GENERIC)
PlatformType.registerItem('win32', 'win32', PlatformType.WIN)
PlatformType.registerItem('win64', 'win64', PlatformType.WIN)
PlatformType.registerItem('solaris', 'solarisshared', PlatformType.UNIX)
PlatformType.registerItem('solaris32', 'solaris32', PlatformType.SOLARIS)
PlatformType.registerItem('solaris64', 'solaris64', PlatformType.SOLARIS)
PlatformType.registerItem('esx', None, PlatformType.UNIX)
PlatformType.registerItem('cygwin', None, PlatformType.GENERIC)
PlatformType.registerItem('darwin', None, PlatformType.UNIX)
PlatformType.registerItem('other', None, PlatformType.GENERIC)

PlatformType.finishItemRegistration()

PlatformType.ALL = (PlatformType.GENERIC, PlatformType.UNIX,
        PlatformType.LINUX, PlatformType.LINUX32, PlatformType.LINUX64,
        PlatformType.WIN, PlatformType.WIN32, PlatformType.WIN64,
        PlatformType.SOLARIS, PlatformType.SOLARIS32, PlatformType.SOLARIS64,
        PlatformType.ESX, PlatformType.CYGWIN, PlatformType.DARWIN,
        PlatformType.OTHER, )
