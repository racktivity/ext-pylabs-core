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

import pymonkey
from pg import connect
from pymonkey.db import DBTable
from pymonkey.pmtypes import QTypeSystem

class DBTableSpace(object):
    name ##string
    dbtables ##array(DBTable)
    __rootobjectname ##string
    __dbconnection ##DBConnection

    def __init__(self,dbconnection,rootobjectname,name=""):
        if name=="":
            self.name=rootobjectname
        self.__rootobjectname=rootobjectname
        self.__dbconnection = dbconnection

    def exists(self):
        """
        check if rootobject exists
        """
    def init(self,owner="", path=""):
        if path=="":
            path=self.__dbconnection.dbpath
        if path.strip()=="":
            raise ValueError("Cannot create tablespace when database path has not been given")
        if owner=="":
            owner=self.__dbconnection.defaultowner
        name=self.name
        path=path+"/"+name+"/"
        pymonkey.q.system.fs.createDir(path)
        sql="DROP TABLESPACE IF EXISTS %s;" % name
        self.__dbconnection.sqlexecute(sql)
        sql="CREATE TABLESPACE  %s OWNER %s LOCATION '%s';" % (name,owner,path)
        self.__dbconnection.sqlexecute(sql)

    def createTablesInDB(self,rootObjectCodeStructure):
        """
        rootObjectCodeStructure represents rootobject definitions
        walk over this structure, init right DBTable objects
        First populate all DBTable objects and then create them
        """
        #populate self.dbtables from rootObjectCodeStructure
        for dbtable in self.dbtables:
            dbtable.createTableInDB()
        #...