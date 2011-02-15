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

import md5

from pylabs import q
from pylabs.baseclasses import BaseType
from pylabs.qpackages.common.DomainObject import DomainObject
class Users(BaseType):

    def __init__(self):
        ''' Constructor for the QPackage Server Users config file.
        The object will allow for checks, useradds, removal of users etc. It will however not list the users.
        '''
        pass

    def addUser(self, username, password):
        ''' Add a user to the configfile
        @param username: username of the user you wish to add
        @param password: plain text password for the user, will be hashed
        '''
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        if not self.exists(username):
            md5hash = md5.md5(password)
            cfgContent += '\n%s:%s'%(username, md5hash.hexdigest())
            q.system.fs.writeFile(self._getConfigFilePath(), cfgContent)
        else:
            raise RuntimeError('User already exists')

    def removeUser(self, username):
        ''' Removes a user from the configfile
        @param username: username of the user you wish to remove from the config'''
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        newContent = ''
        if not self.exists(username):
            raise RuntimeError('User does not exist and cannot be removed')
        for line in cfgContent.splitlines():
            if '%s:'%username in line:
                continue
            newContent += '%s\n'%line
        q.system.fs.writeFile(self._getConfigFilePath(), newContent)

    def exists(self, username):
        ''' Will check if a user exists in the configfile. Returns true is user exists.

        @param username: user to check
        @return bool
        '''
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%username):
                return True
        return False

    def validate(self, username, password):
        ''' Validates if the password is correct for the username
        Returns True is the user and password match.

        @param username: user you wish to validate
        @param password: password that needs to be validated
        @return bool
        '''
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            lineparts = line.split(':')
            if line.startswith('%s:'%username):
                digest = md5.md5(password).hexdigest()
                if lineparts[1] == digest:
                    return True
        return False

    def list(self):
        ''' Returns a list of all known users
        @return list'''

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        userList = list()
        for line in cfgContent.splitlines():
            if line.strip():
                lineparts = line.split(':')
                userList.append(lineparts[0])
        return userList

    def _getConfigFilePath(self):
        ''' returns the file path of the config file
        @return string: path of the file'''
        path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver', 'users.cfg')
        if not q.system.fs.exists(path):
            q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver'))
            q.system.fs.createEmptyFile(path)
        return path

    def __str__(self):
        return '%s'%('QPackageServer users')

    def __repr__(self):
        return self.__str__()