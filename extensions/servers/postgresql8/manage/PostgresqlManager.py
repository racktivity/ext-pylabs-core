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
from pylabs.baseclasses.ManagementApplication import ManagementApplication, CMDBLockMixin
from pylabs.db.DBConnection import DBConnection
from pylabs.enumerators import AppStatusType

from PostgresqlServer import PostgresqlServer
from PostgresqlEnums import PostgresqlAccessRightType

class PostgresqlManager(ManagementApplication, CMDBLockMixin):

    cmdb = PostgresqlServer()
    name = "postgresql"
    configFileDir = cmdb.configFileDir

    def __str__(self):
        return self.cmdb.printDatabases(None, False)

    def __repr__(self):
        return self.__str__()


    def start(self):
        """
        Start Postgresql Server
        """
        q.logger.log('************Start************', 1)
        if self.getStatus() == AppStatusType.HALTED:
            try:
                q.cmdtools.postgresql8.pg_ctl.start(self.cmdb.rootLogin, self.configFileDir)
                return self.getStatus()
            except Exception, ex:
                q.logger.log(ex.message, 4)
                raise RuntimeError, ex.message

    def stop(self):
        """
        Stop Postgresql Server
        """
        if self.getStatus() == AppStatusType.RUNNING:
            try:
                q.cmdtools.postgresql8.pg_ctl.stop(self.cmdb.rootLogin, self.configFileDir)
                return self.getStatus()
            except Exception, ex:
                q.logger.log(ex.message ,4)
                raise RuntimeError, ex.message

    def reload(self):
        """
        Reload Postgresql Server
        """
        if self.getStatus() == AppStatusType.RUNNING:
            try:
                q.cmdtools.postgresql8.pg_ctl.reload(self.cmdb.rootLogin, self.configFileDir)
                return self.getStatus()
            except Exception, ex:
                q.logger.log(ex.message ,4)
                raise RuntimeError, ex.message

    def restart(self):
        """
        Restart Postgresql Server
        """
        self.stop()
        self.start()

    def getStatus(self):
        """
        Get Status of Postgresql Server (Running/ Stopped) by using the Postgresql command wrapper
        """
        q.logger.log(self.cmdb.initialized, 1)
        if self.cmdb.initialized:
            try:
                if q.cmdtools.postgresql8.pg_ctl.getStatus(self.cmdb.rootLogin, self.configFileDir) == AppStatusType.RUNNING:
                    sqlquery = "select count(d.datname) as name from pg_catalog.pg_database d;"
                    ret = q.cmdtools.postgresql8.query._executeSQL('qbase', sqlquery, database='postgres', options='-t')
                    ret = ret.split()
                    if len(ret) == 1:
                        try:
                            num = int(ret[0])
                            if num > 0: return AppStatusType.RUNNING
                        except:
                            q.console.echo('"%s" did not return the expected value \n %s , should be a number' %(sqlquery, ret))
                            return AppStatusType.UNKNOWN
                    q.console.echo('"%s" did not return the expected value \n %s' %(sqlquery, ret))
                    return AppStatusType.UNKNOWN
                return AppStatusType.HALTED
            except Exception, ex:
                q.logger.log(ex.message, 4)
                raise RuntimeError, ex.message
        else:
            return AppStatusType.UNKNOWN

    def printStatus(self):
        # TODO: implement nicely using self.name and self.status
        print "Application [%s] is %s" % (self.cmdb.name, self.getStatus())

    def applyConfig(self):
        """
        Save configurations of users (ACL) to pg_hba config file and Database
        Initialize Server
        Start Server if server isnt already running
        Create/Delete databases
        Write config file with the new Access Control List
        Create/Delete database users
        Save server.postgresql8 object to cmdb
        Restart Server
        """

        # This is the main method which makes the translation between the configuration database and the reality.
        # Command tools are used here to configure the Postgres server.

        q.logger.log("Applying configuration", 5)
        q.logger.log("Initializing server", 5)
        self.init()

        fileLocation = q.system.fs.joinPaths(self.configFileDir, 'pg_hba.conf')
        newDictOfDBs = dict()

        contents = "# TYPE        DATABASE        USER        CIDR-ADDRESS         METHOD\n"
        unix     = "local           all        %(rootLogin)s                        trust\n"%{'rootLogin':self.cmdb.rootLogin}
        ip4Entry = "host            all        %(rootLogin)s       127.0.0.1/32        trust\n"%{'rootLogin':self.cmdb.rootLogin}
        ip6Entry = "host            all        %(rootLogin)s       ::1/128        trust\n"%{'rootLogin':self.cmdb.rootLogin}
        contents += unix
        contents += ip4Entry
        contents += ip6Entry
        for login in self.cmdb.logins:
            contents += "%(type)s           %(database)s        %(login)s       %(cidr_address)s        %(method)s\n" % login

        q.logger.log("running %s server"%self.name, 5)
        if self.getStatus() == AppStatusType.RUNNING:
            self.reload()
        else:
            self.start()

        pgDatabases = self.cmdb.databases.values()
        for pgDatabase in pgDatabases:
            newACLEntryDict = dict()
            if pgDatabase.deleted :
                q.cmdtools.postgresql8.dropdb(pgDatabase.name, pgDatabase.owner)

            else:
                self.startChanges()
                newDictOfDBs[pgDatabase.name] = pgDatabase
                if not pgDatabase.initDone:
                    q.cmdtools.postgresql8.createdb(pgDatabase.name,self.cmdb.rootLogin, pgDatabase.owner)

                acl = pgDatabase.acl

                for aclEntry in acl.values():

                    if not aclEntry.deleted:
                        newACLEntryDict[aclEntry.userName] = aclEntry
                        hbaEntries = self._generateACLEntry(aclEntry, pgDatabase.name)
                        for hbaEntry in hbaEntries:
                            contents += str(hbaEntry)
                            contents +="\n"


                self._applyACL(pgDatabase.name, self.cmdb.rootLogin, acl)
                acl = newACLEntryDict
                pgDatabase.initDone = True
                self.save() #saving with each iteration is the most basic & correct way of keeping cmdb and reality in sync
        self.startChanges()
        self.cmdb.databases = newDictOfDBs
        self.save()
        q.system.fs.writeFile(fileLocation, contents)

        self.reload()


    def applyUserCredentials(self):
        """
        create or update root login credentials
        """
        q.cmdtools.postgresql8.applyusercredentials(self.cmdb.rootLogin, self.cmdb.rootPasswd, self.configFileDir)

    def init(self):
        """
        create user for service
        create service
        """
        if self.cmdb.initialized:
            #service already initialized
            self.start()
            self.applyUserCredentials()
            return
        else:
            self.applyUserCredentials()
            try:
                q.cmdtools.postgresql8.initdb(self.cmdb.rootLogin, self.configFileDir)
            except Exception, ex:
                q.logger.log(ex.message, 4)
                raise RuntimeError, ex.message
            else:
                self.startChanges()
                self.cmdb.initialized = True
                q.logger.log("Saving the [%s] information to the cmdb"%self.name, 5)
                self.save()

    def save(self):
        """
        If configuration not dirty (i.e. configuration is in sync with cmdb), then
        return. Otherwise save the configuration in the cmdb and clear the dirty flag
        """
        self.cmdb.save()

    def _generateACLEntry(self, aclEntry, dbName):
        q.logger.log("Generating ACL entry for database [%s]"%dbName, 5)
        q.logger.log("Username [%s]"%aclEntry.userName, 5)
        q.logger.log("Password [%s]"%aclEntry.passwd, 5)
        hbaEntryList = list()

        if not aclEntry.fromIp and not aclEntry.toIp:

            if not aclEntry.netIp  and not aclEntry.netMask:
                hbaEntryList.append("host        %(dbName)s        %(userName)s     127.0.0.1/32     md5"%{'dbName':dbName, 'userName':aclEntry.userName})
            else:
                hbaEntryList.append("host        %(dbName)s        %(userName)s       %(netIp)s        %(netMask)s         md5"%{'dbName':dbName, 'userName':aclEntry.userName, 'netIp':aclEntry.netIp, 'netMask':aclEntry.netMask})

        elif (aclEntry.fromIp  and not aclEntry.toIp) or aclEntry.fromIp == aclEntry.toIp:

            CIDR_ADDRESS = "%s/32"%aclEntry.fromIp
            hbaEntryList.append("host        %(dbName)s        %(userName)s       %(CidrAdd)s        md5"%{'dbName':dbName, 'userName':aclEntry.userName, 'CidrAdd':CIDR_ADDRESS})

        elif aclEntry.fromIp and aclEntry.toIp :

            fromIpSplit = str(aclEntry.fromIp).split(".")
            toIpSplit = str(aclEntry.toIp).split(".")


            if fromIpSplit[1] != toIpSplit[1]:
                return []

            if fromIpSplit[2] != toIpSplit[2]:
                return []

            for i in range(int(fromIpSplit[3]), int(toIpSplit[3])+1):

                netRange = "%s.%s.%s.%s"%(fromIpSplit[0], fromIpSplit[1], fromIpSplit[2], str(i))
                CIDR_ADDRESS = "%s/32" %netRange
                hbaEntry = "host        %(dbName)s       %(userName)s       %(CIDR_ADDRESS)s        md5"%{'dbName':dbName, 'userName':aclEntry.userName, 'CIDR_ADDRESS':CIDR_ADDRESS}
                hbaEntryList.append(hbaEntry)

        return hbaEntryList

    def _applyACL(self, name, owner, aclList):
        """
        Add users roles to the database
        """
        dbConnection = DBConnection("localhost", name, owner, "")
        createCommand = "CREATE USER \"%s\""
        dropCommand = "DROP USER \"%s\""
        command = ""

        listOfUsers = self._listDBUsers(name, owner)

        for aclEntry in aclList.values():
            userName = aclEntry.userName
            userNameTupleRepresentation  = (userName,)
            command = createCommand%userName
            passwd  = aclEntry.passwd
            right = aclEntry.right
            if not aclEntry.deleted:
                q.logger.log("Creating user [%s]"%userName, 5)
                if passwd and passwd != "":
                    command += " WITH PASSWORD \'%s\'"%passwd

                if right == PostgresqlAccessRightType.CREATEDB:
                    command += " CREATEDB CREATEUSER "

                if not userNameTupleRepresentation in listOfUsers:
                    q.logger.log("Executed command: %s" %command, 5)
                    output = dbConnection.sqlexecute(command)

            else:
                q.logger.log("Dropping user [%s]"%userName, 5)
                command = dropCommand%userName
                output = dbConnection.sqlexecute(command)

    def _listDBUsers(self, name, owner):
        sqlCommand = 'SELECT usename FROM pg_shadow'
        dbConnection = DBConnection("localhost", name, owner, "")
        output = dbConnection.sqlexecute(sqlCommand)

        return output.getresult()
