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
from pylabs import pylabsTestCase
from pylabs import q

class TestDomain(pylabsTestCase):
    def test_init(self):
        ''' Test if we can initialize the object
        '''
        from pylabs.qpackages.common.DomainObject import DomainObject
        domain = DomainObject('test.pylabs.org')
        self.assert_(domain)

        # trying to create a domain with an empty string will fail.
        self.assertRaises(ValueError, DomainObject, '')

    def test_getVLists(self):
        #setup needed:
        from pylabs.qpackages.common.DomainObject import DomainObject
        q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.packageDir, 'test.pylabs.org', 'vlists'))
        content = '''1
2
pylabs|2.0|152|generic|pylabs,base|This is the core framework
pexpect |2.3|1|unix|pexpect,pylabs|External framework that allows to work with interactive commandline tools
'''
        q.system.fs.writeFile(q.system.fs.joinPaths(q.dirs.packageDir, 'test.pylabs.org', 'vlists', 'unstable.vlist'), content)

        domain = DomainObject('test.pylabs.org')
        self.assert_(domain.getVListFiles)