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

from pylabs.db import DBConnection
from pylabs.templateEngine import QTemplateEngine
from pylabs.QShell import QShell
import pylabs
import os

class SqlFile(object):
    path ##string
    name ##string
    sqltxt ##string


class DBSQLPopulator(object):
    """
    read directories of sql files & execute them in order
    directory has sql files in format [nr]__[nameofsqlfile].sql e.g. 1__machinemodel.sql
    it has also logic how to work with templates
    """
    __dbconnection ##string
    sqlfiles ##array(SqlFile)  #list of files found in dir

    def __init__(self,dbconnection):
        self.__dbconnection = dbconnection

    def __getSqlFiles(self,path):
        list = pylabs.q.system.fs.listFilesInDir(path)
        list.sort()
        self.sqlfiles=[]
        for sqlfilepath in list:
            sqlfile=SqlFile()
            sqlfile.sqltxt=q.system.fs.fileGetContents(sqlfilepath)
            sqlfile.path=sqlfilepath
            filename=os.path.basename(sqlfilepath)
            if filename.find("__")<>1:
                raise ValueError("wrong fileformat of sql file, shoud be [priority nr]__[name].sql")
            filename=filename.split("__")[1]
            sqlfile.name=filename.rsplit(".")[0]
            pylabs.q.logger.log("*** Found sql script with name %s." % sqlfile.name, 7)
            self.sqlfiles.append(sqlfile)

    def executeSqlFromDir(self, dirpath):
        """
        execute all sql scripts in specified dirs
        """
        self.populateSqlFilesFromDir(dirpath)
        self.executeSqlFiles()

    def populateSqlFilesFromDir(self, dirpath):
        """
        populate object with all sql files from dir
        """
        if pylabs.q.system.fs.exists(dirpath):
            self.__getSqlFiles(dirpath)
        self.__applyDefaultVarReplace()

    def executeSqlFiles(self):
        for sqlfile in self.sqlfiles:
            self.dbconnection.sqlexecute(sqlfile.sqltxt)

    def __replaceVarDefault(self,text,sqlfile):
        te=QTemplateEngine()
        te.add("filename",sqlfile.name)
        text=te.replace(text)
        return text

    def __applyDefaultVarReplace(self):
        """
        replace {name} in sql files with name of sql file
        """
        for sqlfile in self.sqlfiles:
            sqlfile.sqltxt=self.__replaceVarDefault(sqlfile.sqltxt,sqlfile)


    def replaceVarInAllSqlFiles(self,varname,value):
        for sqlfile in self.sqlfiles:
            value=self.__replaceVarDefault(value,sqlfile)
            te=QTemplateEngine()
            te.add(varname,value)
            sqlfile.sqltxt=te.replace(sqlfile.sqltxt)