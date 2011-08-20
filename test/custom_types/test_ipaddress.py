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

from pylabs.pmtypes import IPv4Address, IPv4Range

class TestIPv4Address(unittest.TestCase):
    def test_str(self):
        '''Test whether integer to string conversion works fine'''
        ip = IPv4Address('192.168.10.45')
        self.assertEquals(str(ip),'192.168.10.45')
        
    def test_int(self):
        '''Test whether string to integer conversion works fine'''	
        ip = IPv4Address('172.16.5.3')
        self.assertEquals(int(ip), 2886731011)
        ip = IPv4Address('0.0.0.0')
        self.assertEquals(int(ip), 0)
        ip = IPv4Address('255.255.255.255')
        self.assertEquals(int(ip), 0xFFFFFFFF)

class TestIPv4Range(unittest.TestCase):
    def test_instanciation_fromto(self):
        '''Test IPv4Range instanciation using from and to addresses'''
        from_, to = '192.168.1.0', '192.168.1.10'

        r = IPv4Range(from_, to)
        self.assertEquals(str(r.fromIp), from_)
        self.assertEquals(str(r.toIp), to)
        
        r = IPv4Range(fromIp=from_, toIp=to)
        self.assertEquals(str(r.fromIp), from_)
        self.assertEquals(str(r.toIp), to)

        fromo = IPv4Address(from_)
        too = IPv4Address(to)

        r = IPv4Range(fromo, too)
        self.assertEquals(str(r.fromIp), from_)
        self.assertEquals(str(r.toIp), to)

        r = IPv4Range(fromIp=fromo, toIp=too)
        self.assertEquals(str(r.fromIp), from_)
        self.assertEquals(str(r.toIp), to)

    def test_invalid_instanciation(self):
        '''Test instanciation providing invalid input (wrong pairs)'''
        self.assertRaises(ValueError, IPv4Range, 1, None, 2, None)
        self.assertRaises(ValueError, IPv4Range, 1, None, None, 2)
        self.assertRaises(ValueError, IPv4Range, 1, None, 2, None)
        self.assertRaises(ValueError, IPv4Range, None,1 , 2, None)
        self.assertRaises(ValueError, IPv4Range, None, 1, None, 2)

        self.assertRaises(ValueError, IPv4Range, 1)
        self.assertRaises(ValueError, IPv4Range, None, 1)
        self.assertRaises(ValueError, IPv4Range, None, None, 1)
        self.assertRaises(ValueError, IPv4Range, None, None, None, 1)
        
    def test_netip_netmask_calculations(self):
        '''Test whether fromIp and toIp are calculated correctly when netIp and 
        netMask are provided'''
        ipr = IPv4Range(netIp='10.100.0.0', netMask='255.255.0.0')
        self.assertEqual(str(ipr.fromIp), '10.100.0.0')
        self.assertEqual(str(ipr.toIp), '10.100.255.255')

    def test_contains(self):
        '''Test whether the contains method works fine'''
        r = IPv4Range('10.100.0.10', '10.100.200.45')

        self.assert_('10.100.0.10' in r)
        self.assert_('10.100.200.45' in r)
        self.assert_('10.100.0.11' in r)
        self.assert_('10.100.200.44' in r)
        self.assert_('10.100.100.100' in r)

        self.assert_('10.100.0.9' not in r)
        self.assert_('10.100.200.46' not in r)
        self.assert_('192.168.10.100' not in r)

        self.assert_('0.0.0.0' not in r)

    def test_len(self):
        '''Test IPv4Range length calculation'''
        r = IPv4Range('10.100.0.0', '10.100.0.100')
        self.assertEquals(len(r), 101)

        r = IPv4Range('10.100.1.100', '10.100.2.99')
        self.assertEquals(len(r), 256)

        r = IPv4Range('127.0.0.1', '127.0.0.1')
        self.assertEquals(len(r), 1)

        r = IPv4Range('1.2.3.4', '1.2.3.5')
        self.assertEqual(len(r), 2)

    def test_add_exc(self):
        r1 = IPv4Range('1.2.3.4', '1.2.3.5')
        r2 = IPv4Range('1.2.3.7', '1.2.3.9')

        def addRanges():
            return r1 + "not a range"
        self.assertRaises(TypeError, addRanges)

        def addRanges():
            return r1 + r2
        self.assertRaises(ValueError, addRanges)

        def addRanges():
            return r2 + r1
        self.assertRaises(ValueError, addRanges)

        def addRanges():
            return r1 + r1
        self.assertRaises(ValueError, addRanges)

    def test_add(self):
        r1 = IPv4Range('1.2.3.4', '1.2.3.5')
        r2 = IPv4Range('1.2.3.6', '1.2.3.9')

        for r in (r1+r2, r2+r1):
            self.assertEqual(str(r.fromIp), '1.2.3.4')
            self.assertEqual(str(r.toIp), '1.2.3.9')
