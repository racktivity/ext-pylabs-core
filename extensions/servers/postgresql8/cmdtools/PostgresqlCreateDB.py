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

class PostgresqlCreateDB(CommandWrapper):
    """
        Creates a database with the specified name for the specified username and owner

        @param name:      name for the new database
        @param username:  username to use when creating the database
        @param owner:     owner for the new database
    """


    def __call__(self, name, username, owner=None):
        """
        Creates a database with the specified name for the specified username and owner

        @param name:      name for the new database
        @param username:  username to use when creating the database
        @param owner:     owner for the new database
        """
        binDir = q.system.fs.joinPaths(os.sep, 'usr', 'lib', 'postgresql', '8.4', 'bin')
        createDBCmd = q.system.fs.joinPaths(binDir, "createdb")
        command = "%s "%(createDBCmd)
        if owner and owner != "":
            command += "-O %s" %(owner)

        command += " --username=%s"%username
        command += " --encoding=UTF8"
        command += " %s" % (name)
        q.logger.log("Creating database [%s]"%name)
        if q.platform.isWindows():
            exitCode, output = q.system.process.execute(command, dieOnNonZeroExitCode=False)
        else:
            exitCode, output = q.system.unix.executeAsUser(command, username, dieOnNonZeroExitCode=False)
        #what if the exitCode is None?????
        if exitCode :
            raise Exception, 'create database failed with error: %s'%output

        return output