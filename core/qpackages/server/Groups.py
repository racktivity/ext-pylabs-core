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
from pylabs.baseclasses import BaseType
from pylabs.qpackages.server.Users import Users

class Groups(BaseType):

    def __init__(self):
        ''' Constructor for the QPackage Server Groups config file.
        The object will allow for checks, addition of groups, users, removal of users, groups etc.
        '''
        pass

    def addGroup(self, group):
        ''' Add a new group

        @param group: group name to add
        '''
        q.logger.log('Adding group %s'%group, 8)
        if self.exists(group.strip()):
            raise RuntimeError('Group %s already exists'%group)

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        cfgContent += '%s:\n'%group.strip()
        q.system.fs.writeFile(self._getConfigFilePath(), cfgContent)
        q.logger.log('Added group %s'%group, 8)

    def removeGroup(self, group):
        ''' Removes the group from the config

        @param group: group to remove
        '''
        q.logger.log('Removing group %s'%group, 8)
        if not self.exists(group.strip()):
            raise RuntimeError('Group %s does not exists'%group)

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        newContent = ''
        for line in cfgContent.splitlines():
            if not line.startswith('%s:'%group):
                newContent += '%s\n'%line
        q.system.fs.writeFile(self._getConfigFilePath(), newContent)
        q.logger.log('Removed group %s'%group, 8)

    def addUserToGroup(self, group, username):
        ''' Add a user to a group
        @param group:    group where the user will belong to
        @param username: username of the user you wish to add
        '''
        u = Users()
        if not u.exists(username):
            raise ValueError('User does not exist, please create the user first')
        q.logger.log('Adding user %s to group %s'%(username, group), 8)
        if self.exists(group):
            cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
            newContent = ''
            for line in cfgContent.splitlines():
                groupString, userString = line.split(':', 1)
                if group == groupString:
                    if userString.strip():
                        users = userString.strip().split(',')
                    else:
                        users = list()
                    if username in users:
                        raise RuntimeError('User %s already belongs to group %s'%(username, group))
                    if users:
                        users.append(username)
                        line = groupString + ':' + ','.join(users)
                    else:
                        line = groupString + ':' + username
                newContent += '%s\n'%line
            q.system.fs.writeFile(self._getConfigFilePath(), newContent)
        else:
            raise RuntimeError('Group %s does not exists'%group)
        q.logger.log('Added user %s to group %s'%(username, group), 8)

    def removeUserFromGroup(self, group, username):
        ''' Removes a user from the group

        @para group:     group where you wish to remove the user from
        @param username: username of the user you wish to remove from the config'''
        q.logger.log('Removing user %s from group %s'%(username, group), 8)
        if self.exists(group):
            cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
            newContent = ''
            for line in cfgContent.splitlines():
                groupString, userString = line.split(':', 1)
                if group == groupString:
                    users = userString.split(',')
                    if not username.strip() in users:
                        raise RuntimeError('User %s does not belongs to group %s'%(username, group))
                    users.remove(username.strip())
                    line =line.split(':')[0] + ':' + ','.join(users)
                newContent += '%s\n'%line
            q.system.fs.writeFile(self._getConfigFilePath(), newContent)
        else:
            raise RuntimeError('Group %s does not exists'%group)
        q.logger.log('Removed user %s from group %s'%(username, group), 8)

    def exists(self, group):
        ''' Will check if a group exists in the configfile. Returns true if group exists.

        @param group: group to check
        @return bool
        '''
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%group):
                return True
        return False

    def checkUserInGroup(self, group, username):
        ''' Checks if a user belongs to a group or not.

        @param group: group to check
        @param username: user you wish to validate
        @return bool
        '''
        if self.exists(group):
            cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
            for line in cfgContent.splitlines():
                groupString, userString = line.split(':', 1)
                if group == groupString:
                    if username.strip() in userString.split(','):
                        return True
            return False
        else:
            raise RuntimeError('Group %s does not exists'%group)

    def list(self):
        ''' Returns a list of all known groups
        @return list'''

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        groupList = list()
        for line in cfgContent.splitlines():
            if line.strip():
                groupList.append(line.split(':',1)[0])
        return groupList

    def listUsersInGroup(self, group):
        '''lists all the users in a group

        @param group: group to list the users
        @return: returns list of users
        '''
        if not self.exists(group):
            raise ValueError('Group does not exist.')

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            groupString, userString = line.split(':', 1)
            if group == groupString:
                return userString.split(',')
        return None

    def listGroupsOfUser(self, username):
        ''' Lists all the groups a user belongs to.

        @param username: username you wish to search
        @return: list of groups
        '''
        groupList = list()
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            group, usersString = line.split(':',1)
            if username.strip() in usersString.split(','):
                groupList.append(group)
        return groupList

    def _getConfigFilePath(self):
        ''' returns the file path of the config file
        @return string: path of the file'''
        path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver', 'groups.cfg')
        if not q.system.fs.exists(path):
            q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver'))
            q.system.fs.createEmptyFile(path)
        return path

    def __str__(self):
        return '%s'%('QPackageServer groups')

    def __repr__(self):
        return str(self)