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
 
from pymonkey.InitBase import *
from pymonkey import q

userName = 'postgresqluser03'
password = 'pass'
dataDir = q.system.fs.joinPaths(q.dirs.baseDir, 'apps', 'postgresql', 'testconf03')

if q.platform.isWindows():
    if q.system.windows.isServiceInstalled('pgsql-8.3'):
        q.system.windows.removeService('pgsql-8.3')

if q.system.fs.isDir(dataDir):
    q.system.fs.removeDirTree(dataDir)

#apply user credentials for user testUser
q.cmdtools.postgresql8.applyusercredentials(userName, password, dataDir)

#initialize a new database cluster using the dataDir
q.cmdtools.postgresql8.initdb(userName, dataDir)

#get the server status
q.cmdtools.postgresql8.pg_ctl.getStatus(userName, dataDir)

#start the database server
q.cmdtools.postgresql8.pg_ctl.start(userName, dataDir)

#get the server status
q.cmdtools.postgresql8.pg_ctl.getStatus(userName, dataDir)

#stop the server
q.cmdtools.postgresql8.pg_ctl.stop(userName, dataDir)

#get the server status
q.cmdtools.postgresql8.pg_ctl.getStatus(userName, dataDir)

#start the database server
q.cmdtools.postgresql8.pg_ctl.start(userName, dataDir)

#create new database
q.cmdtools.postgresql8.createdb('testDatabse', userName)

#stop the server
q.cmdtools.postgresql8.pg_ctl.stop(userName, dataDir)

#start the database server
q.cmdtools.postgresql8.pg_ctl.start(userName, dataDir)

#drop the created database
q.cmdtools.postgresql8.dropdb('testDatabse', userName)