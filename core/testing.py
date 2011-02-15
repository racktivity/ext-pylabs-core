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

import os
import os.path
import unittest
import tempfile
import shutil

class pylabsTestCase(unittest.TestCase):
    def setUp(self):
        import pylabs
        from pylabs.pylabs import pylabs

        if hasattr(pylabs, 'q'):
            delattr(pylabs, 'q')
        pylabs.q = pylabs()

        from pylabs import q

        baseDir = tempfile.mkdtemp()
        print 'Using base directory', baseDir

        #touch qshell 'executable' file
        #do not actually copy over the file (for now)
        if pylabs.q.platform.isWindows():
            qshell = os.path.join(baseDir, 'qshell.bat')

        if pylabs.q.platform.isUnix():
            qshell = os.path.join(baseDir, 'qshell')

        fd = os.open(qshell, os.O_WRONLY | os.O_CREAT, 0755)
        os.close(fd)

        q.init()

        q.dirs.baseDir = baseDir + os.sep
        
        varDir = os.path.join(baseDir, 'var', '')
        os.mkdir(varDir, 0700)
        q.dirs.varDir = varDir

        cfgDir = os.path.join(baseDir, 'cfg', '')
        os.mkdir(cfgDir, 0700)
        q.dirs.cfgDir = cfgDir

        tmpDir = os.path.join(q.dirs.varDir, 'tmp', '')
        os.mkdir(tmpDir, 0700)
        q.dirs.tmpDir = tmpDir

        pidDir = os.path.join(q.dirs.varDir, 'pid', '')
        os.mkdir(pidDir, 0700)
        q.dirs.pidDir = pidDir

        logDir = os.path.join(q.dirs.varDir, 'log', '')
        os.mkdir(logDir, 0700)
        q.dirs.logDir = logDir

        cmdbDir = os.path.join(q.dirs.varDir, 'cmdb', '')
        os.mkdir(cmdbDir, 0700)
        q.dirs.cmdbDir = cmdbDir

        q.dirs.init()

        d = dict()
        d['qualitylevel'] = 'unstable'
        q.cmdb.saveObject('siteconfig', d)

        from sitecustomize import find_qbase_path
        q.dirs.extensionsDir = os.path.join(find_qbase_path(), \
                'lib', 'pylabs', 'extensions')

        q.dirs.binDir = os.path.join(find_qbase_path(), 'bin')

        q.init_final()

    def tearDown(self):
        from pylabs import q
        from sitecustomize import find_qbase_path

        if q.dirs.baseDir == find_qbase_path():
            raise RuntimeError('q.dirs.baseDir is your QBase folder. I do not want to remove this, something is wrong in your test setup. Are you importing pylabs.InitBase* somewhere?')

        print 'Removing baseDir', q.dirs.baseDir
        shutil.rmtree(q.dirs.baseDir)


from pylabs.enumerators import PlatformType

class DisabledTestCase(unittest.TestCase):
    def run(self, *args, **kwargs):
        print 'Testcase is disabled'
        return

def PlatformSpecificTestCase(platform, *args, **kwargs):
    '''Return class_ if platform is current platform, otherwise return object

    This can be used to create TestCase classes which should only be executed
    on one or more specific platforms, eg:

    >>> class MyTest(PlatformSpecificTestCase(PlatformType.LINUX)):
    ...     def test_foo(self):
    ...         self.assert_(True)

    This test will only work on Linux systems.

    @param platform: Platform or list of platforms
    @type platform: PlatformType
    @param args: List of extra supported platforms
    @type args: list<PlatformType>
    @param kwargs.class_: Type to return if platform matches
    @type kwargs.class_: type

    @returns: Requested class on platform match, or C{DisabledTestCase}
    @rtype: type
    '''
    class_ = kwargs.get('class_', unittest.TestCase)
    local_platform = PlatformType.findPlatformType()
    if isinstance(platform, PlatformType):
        platforms = (platform, )
    else:
        platforms = tuple(platform)

    for platform in platforms:
        if local_platform.has_parent(platform):
            return class_

    return DisabledTestCase