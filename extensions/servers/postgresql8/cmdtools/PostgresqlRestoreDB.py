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


class PostgresqlRestoreDB(CommandWrapper):
    """
        PostgreSQL Database restore utility

    """

    def __call__(self, dbname, inputfile, runAs=None,cleanDB=False,createDB=False,userName=None, dataOnly=False, format='c', schemas=[],tables=[],withACL=True,singleTransaction=True):
        """
        Restores a database

        @param dbname:  name of the database to delete
        @param inputfile:  name of the database to delete
        @param runAs: run this command as
        @param cleanDB: delete objects in database before restoring
        @param createDB: create the database. Please note that the name of the database that is created is the name specified in the dumpfile. You need to specify another database name (ex: template1) in order to connect to the database and create restore the database
        @param dataOnly: only restore the data
        @param schemas: restrict restore to schemas specified here
        @param tables: restrict restore to tables specified here
        @param  honour ACLs specified in dumpfile
        @param singleTransaction: handle this restore in a single transaction (either everything works either everything fails) This parameter is discarded if createDB == True

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

        # Solve some incompatibilities
        if createDB and singleTransaction:
            q.eventhandler.raiseError('createDB = True and singleTransaction = True are mutually exclusive options')
        else:
            l_singleTransaction = singleTransaction

        if dbname == 'template1' and not createDB:
            q.eventhandler.raiseError('You cannot restore to template1. Did you forget to specify createDB=True ?')

        if not runAs:
            q.eventhandler.raiseError('Please specify a user to run this command as !')

        if format not in ['c','t']:
            q.eventhandler.raiseError('Format %s not supported by this command' %format)

        # Transform input to pg_restore: list of [evaluatorfunction,parametertouse, pg_restore default, flag_to_use]
        options_to_check = [[setIfTrue,cleanDB,False,'-c'],[setIfTrue,createDB,False,'--create'],[setIfNotDefault,format,'p','-F'],[expandList,schemas,[],'-n'],[expandList,tables,[],'-t'],[setIfFalse,withACL,True,'-x'],[setIfNotDefault,userName,None,'-U'],[setIfTrue,l_singleTransaction,False,'-1']]

        options = [ i[0](i[3],i[1],i[2]) for i in options_to_check]
        optionstring = ' '.join([o.strip() for o in options if o])

            
        binDir = q.system.fs.joinPaths(os.sep, 'usr', 'lib', 'postgresql', '8.4', 'bin')
        restoreCommand = "pg_restore %s -d %s %s" %(optionstring,dbname,inputfile)
        restoreCommandPath = q.system.fs.joinPaths(binDir,restoreCommand)
        #q.console.echo(restoreCommandPath)
        if q.platform.isWindows():
            exitCode, output = q.system.process.execute(restoreCommandPath, dieOnNonZeroExitCode=False)
        else:
            if runAs:
                exitCode, output = q.system.unix.executeAsUser(restoreCommandPath, runAs, dieOnNonZeroExitCode = False)
            else:
                exitCode, output = q.system.process.execute(restoreCommandPath, dieOnNonZeroExitCode = False)
        #what if exitCode is None
        if exitCode:
            raise Exception,'restore database failed with error: %s'%output

        return output
