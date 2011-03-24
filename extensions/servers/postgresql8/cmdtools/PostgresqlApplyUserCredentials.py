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
 
import os
import re

from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.db.DBConnection import DBConnection

class PostgresqlApplyUserCredentials(CommandWrapper):
     """
        Create or update user login credentials
     """

     def __call__(self, username, password, dataDir = None):
        """
        Create or update user login credentials
        """

        serviceName = "pgsql-8.4"
        configFileDir = dataDir and dataDir or q.system.fs.joinPaths(os.sep, 'etc', 'postgresql', '8.4', 'main')
        binDir = q.system.fs.joinPaths(os.sep, 'usr', 'lib', 'postgresql', '8.4', 'bin')

        q.logger.log("Loading [%s] authentication configuration file"%serviceName, 1)
        fileLocation = q.system.fs.joinPaths(configFileDir, "pg_auth")
        userName = re.compile(username)

        if q.system.fs.isFile(fileLocation):
            fileContents = q.system.fs.fileGetContents(fileLocation)

            if userName.search(fileContents):
                dBConnection = DBConnection(None, "template1", username, password)
                result = dBConnection.sqlexecute("ALTER ROLE \"%s\" WITH PASSWORD '%s'"%(username, password))
                return

        if q.platform.isUnix():
            if not self._linuxUserExists(username):
                q.logger.log("Login [%s] does not exist. Creating an entry"%username, 5)
                exitCode, output = q.system.process.execute("useradd %s"%username, dieOnNonZeroExitCode = False)
                if exitCode:
                    raise RuntimeError, 'failed to add user %s for service %s with error %s'%(username, serviceName, output)
            else:
                q.logger.log("User %s already exits"%username, 1)

        if q.platform.isWindows():
            if not q.system.windows.isSystemUser(username):
                q.logger.log("Creating windows user [%s]"%username, 5)
                result = q.system.windows.addSystemUser(username, password)
                if result:
                    raise RuntimeError, 'failed to add user %s for service %s with error %s'%(username, serviceName, result)


     def _linuxUserExists(self, username, dieOnNonZeroExitCodeFlag = False):
        """Checks if a given user is already exists in the system

        @param username: name of the user to check if exists
        """
        exitCode, output = q.system.process.execute("awk -F: '{ print $1 }' /etc/passwd|grep -x %s"%username, dieOnNonZeroExitCode = dieOnNonZeroExitCodeFlag)
        return not exitCode
