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

'''Accessors (factories) to several PyMonkey tools'''

# Implementation details
# ======================
# There's one container class, 'Tools', to which a reference is created on
# q.tools (the tools attribute of the PYMonkey class is class Tools (not an
# instance).
# In Tools some attributes are set, references to tool classes, which expose
# one or more static methods.
# Overall: this works using static methods, no instances are created (since
# this is not necessary for our purpose).

import pymonkey
from pymonkey.inifile.IniFile import IniFile
import pymonkey.hash

class InifileTool:
    @staticmethod
    def open(filename):
        '''Open an existing INI file

        @param filename: Filename of INI file
        @type filename: string

        @raises RuntimeError: When the provided filename doesn't exist

        @returns: Opened INI file object
        @rtype: pymonkey.inifile.IniFile.IniFile
        '''
        if not pymonkey.q.system.fs.exists(filename):
            raise RuntimeError('Attempt to open non-existing INI file %s' % filename)
        return IniFile(filename, create=False)

    @staticmethod
    def new(filename):
        '''Create a new INI file

        @param filename: Filename of INI file
        @type filename: string

        @raises RuntimeError: When the provided filename exists

        @returns: New INI file object
        @rtype: pymonkey.inifile.IniFile.IniFile
        '''
        if pymonkey.q.system.fs.exists(filename):
            raise RuntimeError('Attempt to create existing INI file %s as a new file' % filename)
        return IniFile(filename, create=True)


class ExpectTool:
    @staticmethod
    def new(cmd=None):
        '''Create a new Expect session

        @param cmd: Command to execute
        @type cmd: string

        @returns: Expect session
        @rtype: pymonkey.cmdline.QExpect.QExpect
        '''
        from pymonkey.cmdline.QExpect import QExpect
        return QExpect(cmd=cmd or '')


class HashTool:
    pass

for alg in pymonkey.hash.SUPPORTED_ALGORITHMS:
    setattr(HashTool, '%s_string' % alg,
            staticmethod(getattr(pymonkey.hash, alg)))
    setattr(HashTool, alg,
            staticmethod(getattr(pymonkey.hash, '%s_file' % alg)))


class Tools:
    inifile = InifileTool
    expect = ExpectTool
    hash = HashTool