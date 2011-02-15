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
from pylabs.enumerators import QPackageQualityLevelType
from pylabs.qpackages.common.enumerators import ACLPermission
from pylabs.qpackages.common.DomainObject import DomainObject
class QPackageACL(BaseType):

    domain = q.basetype.string(doc='Domain to where this QPackage belongs', allow_none=False)
    qpackageName = q.basetype.string(doc='Name of the qpackage', allow_none=False)

    def __init__(self, domain, qpackageName):
        ''' Constructor for the QPackageACL. This always belongs to a domain and QPackage, thus those are set in the object.
        The object will allow for checks, useradds, removal of users etc. It will however not list the users.
        @param domain: Domain where the QPackage belongs, this is kept as a string.
        @param qpackageName: name of the QPackage
        '''
        self.domain = str(domain)
        self.qpackageName = qpackageName.strip()

    def addPermission(self, username, permission, qualityLevel):
        ''' Add a permission to the configfile
        @param username: username of the user you wish to add
        @param permission: ACLPermission or string representing the permission the user receives
        @param qualityLevel: QPackageQualityLevelType or string represeting the qualityLevel that the permissions are for.
        '''
        if not permission or not isinstance(permission, (basestring, ACLPermission)):
            raise ValueError('permission must be a valid permission ("R", "W", or "RW")')
        if not qualityLevel or not isinstance(qualityLevel, (basestring, QPackageQualityLevelType)):
            raise ValueError('qualityLevel must be a valid qualityLevel.')

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        if self.exists('username', qualityLevel):
            raise RuntimeError('User %s already has a permission for qualityLevel %s'%(username, str(qualityLevel)))
        cfgContent += '%s:%s:%s\n'%(username, str(permission), str(qualityLevel))
        q.system.fs.writeFile(self._getConfigFilePath(), cfgContent)

    def removePermission(self, username, qualityLevel=None):
        ''' Removes a user from the configfile. If qualityLevel not specified, all entries of the user will be removed.

        @param username: username of the user you wish to remove from the config
        @param qualityLevel: qualityLevel that you wish to remove the permission for'''

        if qualityLevel and not isinstance(qualityLevel, (basestring, QPackageQualityLevelType)):
            raise ValueError('qualityLevel must be a valid qualityLevel.')

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        newContent = ''
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%username):
                lineparts = line.split(':')
                # if qualityLevel specified, only remove for that qualityLevel
                if qualityLevel:
                    if str(qualityLevel) == lineparts[2]:
                        continue
                else:
                    continue
            newContent += '%s\n'%line
        q.system.fs.writeFile(self._getConfigFilePath(), newContent)

    def getPermissions(self, username, qualityLevel):
        ''' Returns the permission for the given user and qualityLevel, return None when not found

        @param username: username of the user you wish to remove from the config
        @param qualityLevel: qualityLevel that you wish to remove the permission for'''

        if qualityLevel and not isinstance(qualityLevel, (basestring, QPackageQualityLevelType)):
            raise ValueError('qualityLevel must be a valid qualityLevel.')

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%username):
                lineparts = line.split(':')
                if qualityLevel and lineparts[2] == str(qualityLevel):
                    return ACLPermission.getByName(lineparts[1].strip())
        return None

    def exists(self, username, qualityLevel=None):
        ''' Will check if a user has a permission.
        If qualityLevel given check whether the user has a permission for that qualityLevel
        Returns true when permission has been found.

        @param username: user to check
        @param qualityLevel: if given the check will consider the qualityLevel
        @return bool
        '''
        if qualityLevel and not isinstance(qualityLevel, (basestring, QPackageQualityLevelType)):
            raise ValueError('qualityLevel must be a valid qualityLevel.')

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%username):
                lineparts = line.split(':')
                if qualityLevel and lineparts[2] == str(qualityLevel):
                    return True
        return False

    def listPermissions(self):
        ''' Returns a list of all known permissions
        @return list'''

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        userList = list()
        for line in cfgContent.splitlines():
            if line.strip():
                userList.append(line)
        return userList

    def _getConfigFilePath(self):
        ''' returns the file path of the config file 
        @return string: path of the file'''
        path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', self.domain, self.qpackageName, 'qpackageacl.cfg')
        if not q.system.fs.exists(path):
            q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', self.domain, self.qpackageName))
            q.system.fs.createEmptyFile(path)
        return path

    def __str__(self):
        return '%s %s'%('ACL for ', self.qpackageName)

    def __repr__(self):
        return str(self)