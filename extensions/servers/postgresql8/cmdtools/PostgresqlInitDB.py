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
 
import re, os

from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper

from PostgresqlApplyUserCredentials import PostgresqlApplyUserCredentials


class PostgresqlInitDB(CommandWrapper):
    """
        Initializes a PostgreSQL instance system databases

        @param username:  username to use when initializing the server
        @param  dataDir: data directory to be used to initialize system databases
    """

    def __call__(self, username, dataDir = None):
        """
        Initializes a PostgreSQL instance system databases

        @param username:  username to use when initializing the server
        @param  dataDir: data directory to be used to initialize system databases
        """
        try:
            name = "pgsql-8.3"
            cmdbtypename    = 'postgresql8server'
            configFileDir = dataDir and dataDir or q.system.fs.joinPaths(os.sep, 'etc', 'postgresql', '8.4', 'main')
            binDir = q.system.fs.joinPaths(os.sep, 'usr', 'lib', 'postgresql', '8.4', 'bin')
            exitCode = 1
            output = ''

            q.logger.log("Applying %s credentials for [%s]"%(username, name))

            if not q.system.fs.isDir(configFileDir):

                    q.logger.log("Creating configuration directory [%s]"%configFileDir, 1)
                    q.system.fs.createDir(configFileDir)

                    if q.platform.isUnix():
                        q.logger.log("Setting owner for [%s] to [%s]"%(configFileDir, username), 5)
                        q.system.unix.chown(configFileDir, username, None)
                        q.logger.log("Setting owner for [%s] to [%s]"%(q.dirs.baseDir, username), 5)
                        q.system.unix.chown(binDir, username, None)

            binPath  = q.system.fs.joinPaths(binDir,"initdb")
            initDBCommand = "%s -E=%s --no-locale -D %s"%(binPath, "UTF-8", configFileDir)

            if q.platform.isUnix():
                    exitCode, output = q.system.unix.executeAsUser("%(initDBCommand)s"%{"initDBCommand":initDBCommand},username, dieOnNonZeroExitCode = False)
                    if exitCode:
                        raise RuntimeError,('initdb failed with error %s'%output, exitCode)

            elif q.platform.isWindows():
                    if not q.system.windows.isServiceInstalled(name):
                        q.logger.log("Registering [%s] that located at [%s]as a windows service"%(name, q.system.fs.joinPaths(binDir,"pg_ctl.exe")), 1)
                        result = q.system.windows.createService(name, name, binDir+"\pg_ctl.exe", 'runservice -W -N %(serviceName)s -D \"%(configFileDir)s\"'%{'serviceName':name, 'configFileDir':configFileDir})
                        if result :
                            q.system.windows.startService(name)
                        else:
                            q.logger.log("cannot regsiter service %s"%name, 6)

                    if q.system.fs.isEmptyDir(configFileDir):
                        command = "%(initDBCommand)s -U %(login)s"%{"login":username, "initDBCommand":initDBCommand}
                        exitCode, output = q.system.process.execute(command, dieOnNonZeroExitCode = False)
                        if exitCode:
                            raise RuntimeError,('initdb failed with error %s'%output, exitCode)
            return exitCode, output
        except:
            print q.errorconditionhandler.getCurrentExceptionString()
            raise
