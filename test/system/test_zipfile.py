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
import inspect
import hashlib
import shutil

from pylabs import pylabsTestCase
from pylabs import q

FILE_MD5 = '658012c52cf07c4f9a706b3c52ef8cfc'

class TestExtract(pylabsTestCase):
    def setUp(self):
        pylabsTestCase.setUp(self)
        thispath = inspect.getfile(TestExtract)
        zipdir = os.path.dirname(thispath)
        self.zippath = os.path.join(zipdir, 'testzip.zip')
        self.out = os.path.join(q.dirs.tmpDir, 'ziptest')
        #Check md5sum of zipfile. We don't want this test to fail because
        #someone changed the file...
        assert os.path.exists(self.zippath)
        fd = open(self.zippath, 'rb')
        content = fd.read()
        fd.close()

        hash_calc = hashlib.md5(content)
        hash = hash_calc.hexdigest()
        assert hash == FILE_MD5, 'Invalid test zip file'

        del hash_calc
        del content

    def tearDown(self):
        if os.path.exists(self.out):
            shutil.rmtree(self.out)

    def test_instanciation(self):
        from pylabs.system.pm_zipfile import ZipFile
        zip = ZipFile(self.zippath)
        zip.close()

    def test_extract_single_file(self):
        from pylabs.system.pm_zipfile import ZipFile
        zip = ZipFile(self.zippath)
        os.mkdir(self.out)
        zip.extract(self.out, ('./testfolder/bar.txt', ))
        zip.close()

        f = os.path.join(self.out, 'testfolder', 'bar.txt')
        self.assert_(os.path.exists(f))
        fd = open(f, 'r')
        content = fd.read().strip()
        fd.close()
        self.assertEqual(content, '0xdeadbeef')

    def test_extract_all(self):
        from pylabs.system.pm_zipfile import ZipFile
        zip = ZipFile(self.zippath)
        os.mkdir(self.out)
        zip.extract(self.out)
        zip.close()

        f = os.path.join(self.out, 'testfolder', 'bar.txt')
        self.assert_(os.path.exists(f))
        fd = open(f, 'r')
        content = fd.read().strip()
        fd.close()
        self.assertEqual(content, '0xdeadbeef')

        f = os.path.join(self.out, 'foo.txt')
        self.assert_(os.path.exists(f))
        fd = open(f, 'r')
        content = fd.read().strip()
        fd.close()
        self.assertEqual(content, 'TarFile test')
