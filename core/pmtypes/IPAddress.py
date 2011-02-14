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

'''IP address and related classes'''

class IPv4Address:
    '''Representation of a standard IPv4 address'''
    #Implementation note: we always store addresses in their integer
    #representation, since this makes it much easier to do manipulations on
    #them. See http://www.aboutmyip.com/AboutMyXApp/IP2Integer.jsp

    def __init__(self, ip, netmask=None, gateway=None):
        '''Create a new IPv4 address representation

        The provided argument can be an integer representation of the address,
        or a standard string representation ('123.123.123.123').

        An optional netmask and gateway can be provided.

        @param ip: IP address
        @type ip: integer or string
        @param netmask: Netmask for this address
        @type netmask: IPv4Address
        @param gateway: Gateway
        @type gateway: IPv4Address
        '''
        if isinstance(ip, int):
            self._ip = ip
        else:
            #Split the input string on dots, convert the resulting integer in
            #it's hexadecimal representation, append all hex values as strings
            #together (this equals the sum(x * 256^N, N=3..0) part of the
            #equasion), convert the resulting string to an integer using 16 as
            #base
            self._ip = int(''.join('%02x' % int (x) for x in str(ip).split('.')), 16)

        self.netmask = netmask
        self.gateway = gateway
    
    def __str__(self):
        result = ''
        #We take a copy since we got to alter this value
        ip = self._ip
        for i in xrange(4):
            result = ".%d%s" % ((ip & 0x000000FF), result)
            ip = ip >> 8
        #Strip of starting .
        return result[1:]
    
    def __int__(self):
        return self._ip

    def __cmp__(self,other):
        if other is None:
            return 1
        other = IPv4Address(str(other))
        return cmp(self._ip, int(other))

    def __add__(self, amount):
        a = int(amount)
        n = self._ip + a
        if n > int(IPv4Address('255.255.255.255')):
            raise OverflowError
        return IPv4Address(self._ip + a)


class IPv4Range(object):
    def __init__(self, fromIp=None, toIp=None, netIp=None, netMask=None):
        """Generates a new IPv4Range object
        
        Provide either fromIp and toIp or netIp and netMask.

        @param fromIp: Starting IP address
        @type fromIp: IPv4Address or string
        @param toIp: End IP address
        @type toIp: IPv4Address or string
        @param netIp: Base IP address when using netmask-based range definition
        @type netIp: IPv4Address or string
        @param netMask: Netmask to use in combination with C{netIp}
        @type netMask: IPv4Address or string
        """
        if (fromIp or toIp) and (netIp or netMask):
            raise ValueError("Provide either fromIp and toIp or netIp and netMask")
        if (fromIp or toIp) and not (fromIp and toIp):
            raise ValueError("Provide either fromIp and toIp or netIp and netMask")
        if (netIp or netMask) and not (netIp and netMask):
            raise ValueError("Provide either fromIp and toIp or netIp and netMask")
        
        if fromIp:
            self.fromIp = IPv4Address(str(fromIp))
            self.toIp = IPv4Address(str(toIp))
        if netIp:
            self.netMask = IPv4Address(str(netMask))
            self.netIp = IPv4Address(int(IPv4Address(str(netIp))) & (int(self.netMask)))
            self.fromIp = self.netIp
            self.toIp = IPv4Address(int(self.fromIp) ^ ((~int(self.netMask))&0xFFFFFFFF))

    @staticmethod
    def convertNetmask(netmask):
        '''Convert a netmask to it's integer representation

        This can convert (eg) 255.255.255.0 to 24.

        @param netmask: Netmask to convert
        @type netmask: IPv4Address or string or int

        @returns: Integer representation of the netmask
        @rtype: number
        '''
        result = 0
        value = int(IPv4Address(netmask))
        while value!=0:
            result += 1
            value = (value<<1) & 0xFFFFFFFF
        return result

    def __contains__(self, iptocheck):
        '''Check whether a given IP address is in the range

        @param iptocheck: IP address to check
        @type iptocheck: IPv4Address or string

        @returns: Whether the provided address is in the range
        @rtype: bool
        '''
        iptocheck = IPv4Address(str(iptocheck))
        return int(iptocheck) >= int(self.fromIp) \
            and int(iptocheck) <= int(self.toIp)

    def __str__(self):
        return ' - '.join([str(self.fromIp), str(self.toIp)])
        
    def __iter__(self):
        curr = self.fromIp
        while curr <= self.toIp:
            yield curr
            curr += 1

    def __add__(self, other):
        """
        Add this IP range to an other (adjacent) IP range

        @param other: IPv4Range adjacent to this one
        @type other: IPv4Range
        @return: An IP range containing exactly all IP addresses from both ranges
        @rtype: IPv4Range
        @raise ValueError: if trying to add a non-IPv4Range or if the other IPv4Range is not adjacent to this one
        """
        notAdjacent = ValueError("IP ranges are not adjacent")

        if not isinstance(other, IPv4Range):
            raise TypeError("Can only add IPv4Ranges to other IPv4Ranges")

        # Check if adjacent (self|other or other|self, call other + self if the latter)
        if self.fromIp == other.fromIp:
            raise notAdjacent
        elif other.fromIp < self.fromIp:
            return other + self
        # self.fromIp < other.fromIp

        if (self.toIp+1) != other.fromIp:
            raise notAdjacent

        # return new range (self.fromIp, other.toIp)
        return IPv4Range(self.fromIp, other.toIp)

    def __len__(self):
        return int(self.toIp) - int(self.fromIp) + 1
