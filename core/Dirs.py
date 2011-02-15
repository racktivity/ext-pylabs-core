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

import sys, os
from user import home

import pylabs

def pathToUnicode(path):
    """
    Convert path to unicode. Use the local filesystem encoding. Will return
    path unmodified if path already is unicode.

    @param path: path to convert to unicode
    @type path: basestring
    @return: unicode path
    @rtype: unicode
    """
    if isinstance(path, unicode):
        return path

    return path.decode(sys.getfilesystemencoding())

class Dirs(object):
    """Utility class to configure and store all relevant directory paths"""

    appDir = None ##string
    '''Application installation base folder (basedir/apps)

    @type: string
    '''

    baseDir = None ##string
    '''pylabs sandbox base folder

    @type: string
    '''

    cfgDir = None ##string
    '''Configuration file folder (appdir/etc)

    @type: string
    '''

    tmpDir = None ##string
    '''Temporary file folder (appdir/tmp)

    @type: string
    '''

    libDir = [] ##array(string)
    '''Library folders added to C{sys.path}

    @type: list<string>
    '''

    varDir = None ##string
    '''Var folder (basedir/var)

    @type: string'''

    logDir = None ##string
    '''Log file folder (appdir/log)

    @type: string
    '''

    homeDir = None ##string
    '''Home folder

    @type: string
    '''

    pidDir = None ##string
    '''Location of the PID files, is set in the initialization of the
    application

    @type: string
    '''

    cmdbDir = None ##string
    '''CMDB storage folder (vardir/cmdb)

    @type: string
    '''

    extensionsDir = None ##string
    '''pylabs extensions base folder (basedir/lib/pylabs/extensions)

    @type: string
    '''

    packageDir = None

    packageDir_2 = None
    
    etcDir = None ##string
    ''' etc folder where system configuration is kept (basedir/etc)

    @type: string
    '''

    binDir = None ##string
    '''Binaries folder (basedir/bin)

    @type: string
    '''

    __initialized = False ##bool

    def init(self):
        """Initializes all the configured directories if needed

        If a folder attribute is None, set its value to the corresponding
        default path.

        @returns: Initialization success
        @rtype: bool
        """
        if self.__initialized == True:
            return True
        if not self.appDir:
            self.appDir = os.path.join(self.baseDir,"apps")
        if not self.tmpDir:
            self.tmpDir = os.path.join(self.appDir,"tmp")
        if not self.varDir:
            self.varDir = os.path.join(self.appDir,"var")
        if not self.cfgDir:
            self.cfgDir = os.path.join(self.appDir,"etc")
        if not self.logDir:
            self.logDir = os.path.join(self.appDir,"log")
        if not self.cmdbDir:
            self.cmdbDir = os.path.join(self.varDir,"cmdb")
        if not self.packageDir:
            self.packageDir = os.path.join(self.varDir,"qpackages")
        if not self.packageDir_2:
            self.packageDir_2 = os.path.join(self.varDir,"qpackages2")
        if not self.etcDir:
            self.etcDir = os.path.join(self.baseDir, 'etc')
        if not self.homeDir:
            self.homeDir = pathToUnicode(os.path.join(home, ".qbase"))

        if not self.extensionsDir:
            self.extensionsDir = os.path.join(self.baseDir, 'lib', 'pylabs','extensions')
        if not self.binDir:
            self.binDir = os.path.join(self.baseDir, 'bin')

        pylabs.q.system.fs.createDir(self.tmpDir)
        pylabs.q.system.fs.createDir(self.varDir)
        pylabs.q.system.fs.createDir(self.logDir)
        pylabs.q.system.fs.createDir(self.cmdbDir)
        pylabs.q.system.fs.createDir(self.packageDir)
        pylabs.q.system.fs.createDir(self.homeDir)

        # TODO: Should check for basedir also and barf if it is not set properly!

        self.__initialized = True
        return True