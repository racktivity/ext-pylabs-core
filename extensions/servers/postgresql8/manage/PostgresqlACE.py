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
 
from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject
from PostgresqlEnums import PostgresqlAccessRightType
class PostgresqlACE(CMDBSubObject):
    """
    A PostgresqlACE represents the configuration of one Access Control Entry
    """
    userName      = q.basetype.string(doc="Unique username for the ACE")
    passwd        = q.basetype.string(doc="Password for the ACE", allow_none=True)
    fromIp        = q.basetype.ipaddress(doc="Start IP address for a range from which this user can connect", allow_none=True)
    toIp          = q.basetype.ipaddress(doc="End IP address for a range from which this user can connect", allow_none=True)
    netIp         = q.basetype.ipaddress(doc="IP address in case you want to add a complete subnet instead of a range", allow_none=True)
    netMask       = q.basetype.ipaddress(doc="Network mask of IP range to allow access", allow_none=True)
    deleted       = q.basetype.boolean(doc="Indicates of this ACE is deleted", default = False)
    right         = PostgresqlAccessRightType.READ

    def __init__(self, username, passwd, right=PostgresqlAccessRightType.READ, fromIp=None, toIp=None, netIp=None, netMask=None):
        CMDBSubObject.__init__(self)
        self.userName = username
        self.right = right
        self.passwd = passwd
        self.fromIp = fromIp
        self.toIp = toIp
        self.netIp = netIp
        self.netMask = netMask

    def __repr__(self):
        stringRep = "Username: %s%s"%(self.userName, ' [marked for deletion]' if self.deleted else '')
        stringRep += "\tRight: %s\n"%self.right
        return stringRep

    def __fake_data__(self):
        self.userName = 'ACE-%s' % q.base.idgenerator.generateRandomInt(10, 100)
        self.passwd   = 'PASSWD-%s' % q.base.idgenerator.generateRandomInt(10, 100)
        self.fromIp = '.'.join(str(q.base.idgenerator.generateRandomInt(0, 255)) for i in xrange(4))
        self.toIp = '.'.join(str(q.base.idgenerator.generateRandomInt(0, 255)) for i in xrange(4))
        self.netIp = '.'.join(str(q.base.idgenerator.generateRandomInt(0, 255)) for i in xrange(4))
        self.netMask = '.'.join(str(q.base.idgenerator.generateRandomInt(0, 255)) for i in xrange(4))
        self.right = PostgresqlAccessRightType.WRITE
        self.deleted = False