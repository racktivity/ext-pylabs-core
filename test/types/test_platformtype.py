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

import unittest

from pylabs.enumerators import PlatformType

class TestPlatformType(unittest.TestCase):
    def test_all_generic(self):
        '''Test whether all known platforms are generic'''
        for platform in PlatformType.ALL:
            self.assert_(platform.isGeneric())

    def test_unix(self):
        '''Test whether all known UNIX platforms expose themselves as UNIX'''
        UNIX_PLATFORMS = (PlatformType.UNIX, PlatformType.LINUX, PlatformType.LINUX32,
                PlatformType.LINUX64, PlatformType.SOLARIS,
                PlatformType.SOLARIS32, PlatformType.SOLARIS64,
                PlatformType.ESX, PlatformType.DARWIN, )
        for platform in UNIX_PLATFORMS:
            self.assert_(platform.isUnix())
        for platform in (platform for platform in PlatformType.ALL if platform not 
                in UNIX_PLATFORMS):
            self.assert_(not platform.isUnix())

    def test_linux(self):
        '''Test whether all known Linux platforms expose themselves as Linux'''
        LINUX_PLATFORMS = (PlatformType.LINUX, PlatformType.LINUX32, PlatformType.LINUX64, )
        for platform in LINUX_PLATFORMS:
            self.assert_(platform.isLinux())
        for platform in (platform for platform in PlatformType.ALL if platform not
                in LINUX_PLATFORMS):
            self.assert_(not platform.isLinux())

    def test_windows(self):
        '''Test whether all known Windows platforms expose themselves as
        Windows'''
        WINDOWS_PLATFORMS = (PlatformType.WIN, PlatformType.WIN32, PlatformType.WIN64, )
        for platform in WINDOWS_PLATFORMS:
            self.assert_(platform.isWindows())
        for platform in (platform for platform in PlatformType.ALL if platform not
                in WINDOWS_PLATFORMS):
            self.assert_(not platform.isWindows())

    def test_solaris(self):
        '''Test whether all known Solaris platforms expose themselves as
        Solaris'''
        SOLARIS_PLATFORMS = (PlatformType.SOLARIS, PlatformType.SOLARIS32, 
                PlatformType.SOLARIS64, )
        for platform in SOLARIS_PLATFORMS:
            self.assert_(platform.isSolaris())
        for platform in (platform for platform in PlatformType.ALL if platform not
                in SOLARIS_PLATFORMS):
            self.assert_(not platform.isSolaris())

    def test_reverse_lookup(self):
        '''Test name-based reverse lookup'''
        for platform in PlatformType.ALL:
            self.assert_(platform is PlatformType.getByName(str(platform)))

        self.assertRaises(KeyError, PlatformType.getByName, 'FoObAr')

    def test_shared_vapp_folders(self):
        '''Test folder name of files folder in vapps for shared platforms'''
        SHARED_PLATFORMS = PlatformType.GENERIC, PlatformType.UNIX, \
            PlatformType.LINUX, PlatformType.SOLARIS, PlatformType.WIN

        for platform in SHARED_PLATFORMS:
            self.assert_(platform.vappFolderName.endswith('shared'))

        for platform in (platform for platform in PlatformType.ALL if
                platform not in SHARED_PLATFORMS):
            self.assert_(not str(platform.vappFolderName).endswith('shared'))