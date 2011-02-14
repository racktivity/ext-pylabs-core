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

import sys
import os

import pymonkey

# Set this variable before initialising PyMonkey when your application
# does not include a qshellbin. (i.e. a py2exed Q-Helper without shell.exe)
# The value of this variable must be a qshellbin, or must behave like one
# when called.
qshellbin = None

class _Vars:
    def __init__(self):
        self._vars = dict()

    def setVar(self, name, value):
        """Set variable to a certain value

        @param name: The name of the variable
        @param value: The value to set the variable to
        """
        if name is not None:
            self._vars[name] = value

    def getVar(self, name):
        """Get variable value

        @param name: Variable name
        @rtype: string representing the value of variable
        """
        return name and self._vars.get(name, None) or None

    def pm_setSystemVars(self):
        '''Set system variables

        Sets some well-known system variables in q.vars. This includes:

         * qshellbin

        '''
        _qshellbin = qshellbin
        if not _qshellbin:
            pymonkey.q.logger.log('Looking up qshell executable path', 7)
            executables = None

            if pymonkey.q.platform.isWindows():
                executables = ('qshell.exe', 'qshell.bat', )
                '''Possible executable names'''

            if pymonkey.q.platform.isUnix() and not pymonkey.q.platform.isDarwin():
                executables = ('qshell', )
                '''Possible executable names'''

            if pymonkey.q.platform.isDarwin():
                executables = ('qshell.py', 'qshell')

            if not executables:
                raise RuntimeError('Unable to find qshell executable: platform not supported')

            if sys.executable.endswith(executables):
                _qshellbin = sys.executable
            else:
                for executable in executables:
                    executable = os.path.join(pymonkey.q.dirs.baseDir, executable)
                    if pymonkey.q.system.fs.exists(executable):
                        _qshellbin = executable
                        break

            if not _qshellbin:
                raise RuntimeError('Unable to find qshell executable')

            pymonkey.q.logger.log('Found qshell binary at %s' % _qshellbin, 7)
        # If we're on Windows, make sure qshellbin is a short path name
        if pymonkey.q.platform.isWindows():
            import win32api
            _qshellbin = win32api.GetShortPathName(_qshellbin)

        self.setVar('qshellbin', _qshellbin)

#@todo more logging & errorchecking

Vars = _Vars()
del _Vars