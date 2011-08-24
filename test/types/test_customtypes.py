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

import pylabs
from pylabs.baseclasses.BaseType import BaseType
from pylabs.pmtypes.CustomTypes import IPAddress, Duration

class TestCustomType(unittest.TestCase):
    def test_IPAddress(self):
        '''Test whether all known platforms are generic'''
        ip  = IPAddress()
        self.assertTrue(ip.check('10.100.255.0'))
        self.assertFalse(ip.check('10.100.256.0'))
        self.assertFalse(ip.check('10.100'))
        self.assertFalse(ip.check('10.100.256.12.123'))

    def test_Duration(self):
        duration = Duration()
        self.assertTrue(duration.check('1h'))
        self.assertTrue(duration.check('1m'))
        self.assertTrue(duration.check('1s'))
        self.assertTrue(duration.check('42h'))
        self.assertTrue(duration.check('42m'))
        self.assertTrue(duration.check('42s'))
        self.assertTrue(duration.check('10'))
        self.assertFalse(duration.check('h'))
        self.assertFalse(duration.check('m'))
        self.assertFalse(duration.check('s'))
        self.assertFalse(duration.check(''))

        class DurationTest(BaseType):
            d = Duration(doc="Test", default=-1)

        duration = DurationTest()
        duration.d = '1h'
        self.assertEquals(duration.d, 3600)
        duration.d = 42
        self.assertEquals(duration.d, 42)