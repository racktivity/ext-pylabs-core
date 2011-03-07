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
from pylabs.baseclasses.CMDBServerObject import CMDBServerObject
from PostgresqlDatabase import PostgresqlDatabase

import os

class PostgresqlServer(CMDBServerObject):

    cmdbtypename    = 'postgresql8server'
    name = q.basetype.string('postgresql8server')
    configFileDir   = q.basetype.dirpath(doc="Directory containing the configuration files", default=q.system.fs.joinPaths(os.sep, 'etc', 'postgresql', '8.4', 'main'))
    databases       = q.basetype.dictionary()
    logins          = q.basetype.list()

    # security?
    rootLogin       = q.basetype.string(doc="Root login for the Postgres server", allow_none=True)
    rootPasswd      = q.basetype.string(doc="Password for the root login", allow_none=True)
    initialized     = q.basetype.boolean(doc="Indicates if this Postgres database server was already initialized", default=False)


    def __init__(self):
        CMDBServerObject.__init__(self)

    def addDatabase(self, name, owner=None):
        """
        Adds a database
        @param name: Name of the database to create
        @param owner: Owner of the database to create
        @return: PostgresqlDB object created
        """

        # Confusing -> db already exists
        if name in self.databases:
            return self.databases[name]

        owner = owner or self.rootLogin
        newDB = PostgresqlDatabase(name, owner)
        self.databases[newDB.name] = newDB
        return newDB

    def removeDatabase(self, name):
        """
        Deletes a database by name
        @param name: Name of the database to delete
        """
        q.logger.log("Marking database [%s] for deletion"%name, 5)
        self.databases[name].deleted = True

    def printDatabases(self, name=None,verbose=True):
        """
        Human friendly output of site configuration
        """
        if name:
            q.console.echo(self.databases[name])
        else:
            stringRep = ''
            for db in self.databases.itervalues():
                stringRep += (str(db) if verbose else (db.name + '\n'))

            q.console.echo(stringRep)

    def addLogin(self, login, type='local', cidr_address='', database='all', method='trust'):
        new_login = dict()
        new_login['login'] = login
        new_login['type'] = type
        new_login['cidr_address'] = cidr_address
        new_login['database'] = database
        new_login['method'] = method
        self.logins.append(new_login)

    def removeLogin(self, login, type='local', cidr_address='', database='all', method='trust'):
        login_to_remove = dict()
        login_to_remove['login'] = login
        login_to_remove['type'] = type
        login_to_remove['cidr_address'] = cidr_address
        login_to_remove['database'] = database
        login_to_remove['method'] = method
        if login_to_remove in self.logins:
            self.logins.remove(login_to_remove)


    def __fake_data__(self):
        # CMDB Object
        self.name = 'postgresql8server'
        self.cmdbid = q.base.idgenerator.generateRandomInt(10, 100)
        self.cmdbguid = str(q.base.idgenerator.generateGUID())

        # CMDB Application Object
        self.pid = q.base.idgenerator.generateRandomInt(1024, 2048)
        self.initDone = True

        # CMDB Server Object
        self.autoRestart = False
        self.startAtReboot = True

        # PostgresqlDatabase
        for i in range(0, 5):
            name = 'Database-%s' % q.base.idgenerator.generateRandomInt(10, 100)
            db = PostgresqlDatabase(name)
            self.databases[db.name] = db
