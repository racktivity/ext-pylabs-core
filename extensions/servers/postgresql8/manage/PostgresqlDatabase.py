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
from PostgresqlACE import PostgresqlACE
from PostgresqlEnums import PostgresqlAccessRightType

class PostgresqlDatabase(CMDBSubObject):
    name      = q.basetype.string(doc="Unique name for this Postgres database")
    owner     = q.basetype.string(doc="Owner of this Postgres database", allow_none=True)
    initDone  = q.basetype.boolean(doc="Indicates if this Postgres database was already initialized", default=False)
    deleted   = q.basetype.boolean(doc="Indicates if this Postgres database should be deleted")
    acl       = q.basetype.dictionary(doc="Dictionary of PostgresqlACE objects")

    def __init__(self, name, owner=None):
        CMDBSubObject.__init__(self)
        self.name = name
        self.owner = owner

    def addACE(self, username, passwd, right=PostgresqlAccessRightType.READ, fromIp=None, toIp=None, netIp=None, netMask=None) :
        """
        Add user to Access Control List
        @param username: name of the user
        @param right: access right granted to this user (R, W, C)
        @param fromIp: start range for network access (ipaddress)
        @param toIp: end range for network access(ipaddress)
        @param netIp: network ipaddress
        @netMask: network mask
        @param passwd: password for the user
        """

        if not username in self.acl:
            q.logger.log("Adding ACL entry for [%s]"%username, 5)
            ace = PostgresqlACE(username, passwd, right, fromIp, toIp, netIp, netMask)
            self.acl[username] = ace

        else:
            raise Exception,"User (%s) Already Exists"%username

    def removeACE(self, username):
        """
        Delete a user from Access Control List
        @param username: name of the user to delete
        """
        if not username in self.acl:
            raise Exception,'USER (%s) doesnt exist'%username
        else:
            self.acl[username].deleted = True
            q.logger.log("USER (%s) was successfully DELETED "%username, 5)

    def __repr__(self):
        stringRep = "\tName = %s \n"%self.name + "\tOwner = %s "%self.owner
        if self.acl:
            stringRep += "\n\t\tAccess Control List:\n"
            for ace in self.acl.itervalues():
                stringRep += '\t\t' + str(ace)

        return stringRep

    def __fake_data__(self):
        self.name = 'DB-%s' % q.base.idgenerator.generateRandomInt(10, 100)
        self.owner = 'OWNER-%s' % q.base.idgenerator.generateRandomInt(10, 100)
        self.acl = {}
        self.initDone = False
        self.deleted = False
        for i in range(0, 5):
            ace = PostgresqlACE('USER-%s' % q.base.idgenerator.generateRandomInt(10, 100), 'PASSWD-%s' % q.base.idgenerator.generateRandomInt(10, 100))
            self.acl[ace.userName] = ace