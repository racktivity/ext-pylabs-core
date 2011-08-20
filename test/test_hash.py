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
import unittest
import tempfile

from pylabs import hash

test_string_content = '''This is a test string
containing a \0
But nothing more'''

test_file_content = '''This is the content
of the test file.
It contains some special characters like \0, \1, \2 and \3.'''

class _HashTestBase(unittest.TestCase):
    def setUp(self):
        fd, self.filepath = tempfile.mkstemp()
        fd = os.fdopen(fd, 'wb')
        fd.write(test_file_content)
        fd.close()

    def tearDown(self):
        os.unlink(self.filepath)

    def test_string(self):
        hash_string_func = getattr(hash, self.ALGORITHM)
        value = hash_string_func(test_string_content)
        self.assertEqual(value, self.STRING_HASH)

    def test_file(self):
        hash_file_func = getattr(hash, '%s_file' % self.ALGORITHM)
        value = hash_file_func(self.filepath)
        self.assertEqual(value, self.FILE_HASH)

class TestMD5(_HashTestBase):
    ALGORITHM = 'md5'
    STRING_HASH = '97850f1e2a5eb4b02138a5dd35f89d4e'
    FILE_HASH = '5d6465d6cdf6ca3e8e92a146db945701'

class TestSHA1(_HashTestBase):
    ALGORITHM = 'sha1'
    STRING_HASH = '718cdddc77cdcf1fe39789d9c431cf21d92e65be'
    FILE_HASH = '7d4ddf9300abbc4c92f5939a2f06fb01cee10058'

class TestSHA256(_HashTestBase):
    ALGORITHM = 'sha256'
    STRING_HASH = \
        'f5c200146de03b5bc31b5cd138a156885a5fd715278fd1adfd3bed924998b4e3'
    FILE_HASH = \
        'cad0571db4a42ee62e3c1cf6148621bdaec7f5e54045546a6de701bb5fc8cf66'

class TestSHA512(_HashTestBase):
    ALGORITHM = 'sha512'
    STRING_HASH = 'd93c861d14a17fadf9880912e905885a93106672b3b0096966997d2f' \
                  '6ac950a1fce05572775812492979f4816727ea92f2c178e318e5c15a' \
                  'a83e1be01bd8404c'
    FILE_HASH = '470fe2aad49160c4d6314a725aa76a84deb9d67eef85af240d99f9329e' \
                '65574947326ea9474ff3b1b065fc8f49588b513365f412bbf698c32e56' \
                'f0d274aea522'

class TestCRC32(_HashTestBase):
    ALGORITHM = 'crc32'
    STRING_HASH = 1461827377
    FILE_HASH = -765554084