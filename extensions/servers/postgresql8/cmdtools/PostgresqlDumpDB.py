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
from pylabs.baseclasses.CommandWrapper import CommandWrapper
import os
import pwd


class PostgresqlDumpDB(CommandWrapper):
    """
        PostgreSQL database archiving utility 


    """

    def __call__(self, dbname, outputfile, runAs=None, blobs=None, dataOnly=False, columnInsert=False,format='c',ignoreVersion=False, schemas=[],tables=[],excludeSchemas=[],excludeTables=[],noOwner=False,withACL=True):
        """
        Creates a dump of the database with the specified name

        @param dbname:  name of the database to delete
        @param outputfile: owner of the database to delete
        @param runAs:
        @param blobs: Store blobs. Only usefull when making selective dumps (e.g. when specifying the schema's and or tables to dump
        @param dataonly: Only dump the data
        @param columnInserts: usefull when the column order in inserts has to be explicitly specified. Slower but more security
        @param withACL: dump ACL's
        @param ignoreVersion: ignore version mismatch between pg-dump utility and database. Only if you know what you're doing
        @param schemas: explicitly specify schema's to dump (and only those)
        @param tables: explicitly specify schema's to dump (and only those)
        @param tables: explicitly specify tables to dump (and only those)
        @param excludeSchemas: explicitly specify tables to dump (and only those)
        @param excludeTables: explicitly specify tables to dump (and only those)


        """

        def setIfTrue(fl,val,default):
            if val == default: return ''
            if val:
                return fl
            return ''
        def setIfFalse(fl,val,default):
            if val == default: return ''
            if not val:
                return fl
            return ''
        def expandList(fl,val,default):
            if val == default: return ''
            if isinstance(val,list):
                rc=''
                for i in val:
                    rc = rc + fl + ' ' + i + ' '
                return rc
            return '%s %s' %(fl,val)

        def setIfNotDefault(fl,val,default):
            if val==default: return ''
            return '%s %s' %(fl,val)
                

        def noop(fl,val,default):
            return ''

        options_to_check = [[setIfTrue,blobs,False,'-b'],[setIfTrue,dataOnly,None,'-a'],[setIfTrue,columnInsert,None,'-D'],[setIfNotDefault,format,'p','-F'],[setIfTrue,ignoreVersion,None,'-i'],[expandList,schemas,[],'-n'],[expandList,tables,[],'-t'],[expandList,excludeSchemas,[],'-N'],[expandList,excludeTables,[],'-T'],[noop,noOwner,None,'-O'],[setIfFalse,withACL,True,'-x']]

        options = [ i[0](i[3],i[1],i[2]) for i in options_to_check]
        optionstring = ' '.join([o.strip() for o in options if o])
            
        binDir = q.system.fs.joinPaths(os.sep, 'usr', 'lib', 'postgresql', '8.4', 'bin')
        dumpCommand = "pg_dump %s -f %s %s" %(optionstring,outputfile,dbname)
        dumpCommandPath = q.system.fs.joinPaths(binDir,dumpCommand)
        if q.platform.isWindows():
            exitCode, output = q.system.process.execute(dumpCommandPath, dieOnNonZeroExitCode=False)
        else:
            if runAs:
               exitCode, output = q.system.unix.executeAsUser(dumpCommandPath, runAs,dieOnNonZeroExitCode = False)
            else:
               exitCode, output = q.system.process.execute(dumpCommandPath,dieOnNonZeroExitCode = False)

        if exitCode:
            raise Exception,'dump database failed with error: %s'%output

        return output
