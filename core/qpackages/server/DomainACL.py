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
from pylabs.qpackages.common.enumerators import ACLPermission
from pylabs.qpackages.common.DomainObject import DomainObject
from pylabs.qpackages.server.Groups import Groups
from pylabs.qpackages.server.Users import Users
from pylabs.qpackages.common.QPackageACL import QPackageACL

class DomainsACL(BaseType):
    domains = q.basetype.list(doc="list of known domain with acls", allow_none=True, default=dict())

    def __init__(self):
        self.pm_LoadKnownDomains()

    def domainACLAdd(self, domain, userName, permission):
        """
        Add a user permission on a domain
        @param domain: name of the domain
        @param userName: name of the user to add
        @param permission: permission to give to the user e.g. q.enumerators.ACLPermission.R
        """
        domainACL = DomainACL(str(domain))

        if domainACL.exists(userName):
            raise ValueError('DomainACL already exists for user %s'%userName)
        
        domainACL.addPermission(userName, permission)

        if not str(domain) in self.domains:
            self.domains.append(str(domain))

    def domainACLRemove(self, domain, userName):
        """
        Remove a user from list of permitted users
        @param domain: name of the domain
        @param userName: name of the user to remove
        """
        domainACL = DomainACL(str(domain))

        if not domainACL.exists(userName):
            raise ValueError('DomainACL does not exist for user %s'%userName)

        domainACL.removePermission(userName)

        if not str(domain) in self.domains and domainACL.listPermissions():
            self.domains.append(str(domain))
        elif str(domain) in self.domains and not domainACL.listPermissions():
            self.domains.remove(str(domain))
    
    def domainACLModify(self, domain, userName, permission):
        """
        Modify a user's permission on a domain
        @param domain: name of the domain
        @param userName: name of the user to modify
        @param permission: new permission to give to the user e.g. q.enumerators.ACLPermission.R
        """
        self.domainACLRemove(domain, userName)
        self.domainACLAdd(domain, userName, permission)
    
    def domainACLExists(self, domain, userName):
        """
        Check if user exists in domain acl
        @param domain: name of the domain
        @param userName: name of the user to check
        """
        domainACL = DomainACL(domain)
        return domainACL.exists(userName)
    
    def domainACLGetPermissions(self, domain, userName):
        """
        Retrieve user's permissions on a domain
        @param domain: name of the domain
        @param userName: name of the user
        """
        domainACL = DomainACL(domain)
        return domainACL.getPermissions(userName)
    
    def domainACLList(self, domain=None):
        """
        List domain acls for a certain domain or known domains
        @param domain: name of the domain
        """
        if not domain:
            domainsACLs = dict()
            for domain in self.domains:
                domainACL = DomainACL(str(domain))
                domainsACLs[domain]=domainACL.listPermissions()
            return domainsACLs

        domainACL = DomainACL(str(domain))

        permissions = domainACL.listPermissions()
        if permissions:
            if not str(domain) in self.domains:
                self.domains.append(str(domain))
        return permissions

    def domainACLGet(self, domain):
        """
        Retrieve a domain acl object
        @param domain: name of the domain
        """
        return DomainACL(domain)

    def refresh(self):
        self.pm_LoadKnownDomains()

    def pm_LoadKnownDomains(self):
        """
        Load list of domains with acls
        """
        qpackageDomainsDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains')
        domains = list()
        if not q.system.fs.exists(qpackageDomainsDir):
            self.domains = domains
            return

        for domainDir in q.system.fs.listDirsInDir(qpackageDomainsDir):
            configFile = q.system.fs.joinPaths(domainDir, 'domainacl.cfg')
            if not q.system.fs.exists(configFile):
                continue
            if self.domainACLList(q.system.fs.getBaseName(domainDir)):
                domains.append(q.system.fs.getBaseName(domainDir))

        self.domains = domains
    
    #required iterable elements
    def __iter__(self):
        return self.pm_DomainACL.values().__iter__()
    
    def __len__(self):
        return self.pm_DomainACL.__len__()
    
    def __contains__(self, v):
        if isinstance(v, str):
            return v in self.pm_DomainACL.keys()
        elif isinstance(v, QPackageServerConnection):
            return v in self.pm_DomainACL.values()
    
    def __getitem__(self, v):
        if isinstance(v, int):
            return self.pm_DomainACL.__getitem__(self.pm_DomainACL.keys()[v])
        elif isinstance(v, str):
            return self.pm_DomainACL.__getitem__(v)

class DomainACL(BaseType):

    domain = q.basetype.object(DomainObject, doc='Domain to where this QPackage belongs', allow_none=False)
    qpackageNames = q.basetype.list(doc='list of known qpackages with acls', default = list())

    def __init__(self, domain):
        """
        Constructor for the DomainACL. This always belongs to a domain.
        The object will allow for checks, user/groupadds, removal of users/groups etc.
        @param domain: Domain of which this ACL reflects the permissions.
        """
        self.domain = DomainObject(str(domain))
        self.pm_LoadKnownQPackages()

    def addPermission(self, name, permission):
        """
        Add a permission to the configfile
        @param name: name of the user or group you wish to add
        @param permission: ACLPermission or string representing the permission the user receives
        """
        if not permission or not isinstance(permission, (basestring, ACLPermission)):
            raise ValueError('permission must be a valid permission ("R", "W", or "RW")')
        # check first if the user exists!
        if name is not '*':
            users = Users()
            groups = Groups()
            if not users.exists(name) and not groups.exists(name):
                raise ValueError('user or group %s does not exist, please create the user first'%name)

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        if self.exists(name):
            raise RuntimeError('user or group %s already has a permission for domain %s'%(name, self.domain.name))
        cfgContent += '%s:%s\n'%(name, str(permission))
        q.system.fs.writeFile(self._getConfigFilePath(), cfgContent)

    def removePermission(self, name):
        """
        Removes a user from the configfile.
        @param name: name of the user or group you wish to remove from the config
        """

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        newContent = ''
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%name):
                continue
            newContent += '%s\n'%line
        q.system.fs.writeFile(self._getConfigFilePath(), newContent)

    def getPermissions(self, name):
        """
        Returns the permission for the given user/group, return None when not found

        @param name: name of the user or group you wish to see the permission
        """

        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%name):
                lineparts = line.split(':')
                return ACLPermission.getByName(lineparts[1].strip())
        return None

    def exists(self, name):
        """
        Will check if a user or group exists.
        Returns true when permission has been found.

        @param name: user or group to check
        @return bool
        """
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        for line in cfgContent.splitlines():
            if line.startswith('%s:'%name):
                    return True
        return False

    def listPermissions(self):
        """
        Returns a list of all known permissions
        @return list
        """
        cfgContent = q.system.fs.fileGetContents(self._getConfigFilePath())
        permissionList = list()
        for line in cfgContent.splitlines():
            if line.strip():
                permissionList.append(line)
        return permissionList

    def _getConfigFilePath(self):
        """
        returns the file path of the config file 
        @return string: path of the file
        """
        path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', self.domain.name, 'domainacl.cfg')
        if not q.system.fs.exists(path):
            q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', self.domain.name))
            q.system.fs.createEmptyFile(path)
        return path

    def qpackageACLAdd(self, qpackageName, userName, permission, qualityLevel):
        """
        Add a user to qpackage acl
        @param qpackageName: name of the qpackage to add user to
        @param username: username of the user you wish to add
        @param permission: ACLPermission or string representing the permission the user receives
        @param qualityLevel: qualityLevel that you wish to add the permission for
        """
        qpackageACL = QPackageACL(str(self.domain), qpackageName)
        qpackageACL.addPermission(userName, permission, qualityLevel)

        if not qpackageName in self.qpackageNames:
            self.qpackageNames.append(qpackageName)

    def qpackageACLRemove(self, qpackageName, userName, qualityLevel=None):
        """
        Remove a user from pylabs.qpackage acl
        @param qpackageName: name of the qpackage to remove user from
        @param username: username of the user you wish to remove
        @param qualityLevel: qualityLevel that you wish to remove the permission for
        """
        qpackageACL = QPackageACL(str(self.domain), qpackageName)
        qpackageACL.removePermission(userName, qualityLevel)
        
        if not qpackageName in self.qpackageNames and qpackageACL.listPermissions():
            self.qpackageNames.append(qpackageName)
        elif qpackageName in self.qpackageNames and not qpackageACLACL.listPermissions():
            self.qpackageNames.remove(qpackageName)

    def qpackageACLList(self, qpackageName=None):
        """
        Returns a list of all known permissions
        @param qpackageName: name of the qpackage to list users for
        """
        if not qpackageName:
            qpackagesACLs = dict()
            for qpackage in self.qpackageNames:
                qpackageACL = QPackageACL(str(self.domain), qpackage)
                qpackagesACLs[qpackage]= qpackageACL.listPermissions()
            return qpackagesACLs

        qpackageACL = QPackageACL(str(self.domain), qpackageName)
        permissions =  qpackageACL.listPermissions()

        if permissions:
            if not qpackageName in self.qpackageNames:
                self.qpackageNames.append(qpackageName)
        return permissions

    def qpackageACLGetPermissions(self, qpackageName, userName, qualityLevel):
        """
        Retrieves the permission for the given user and qualityLevel
        @param qpackageName: name of the qpackage to retrieve user's permission for
        @param username: username of the user you wish to retrieve permission for
        @param qualityLevel: qualityLevel that you wish to retrieve permission for
        """
        qpackageACL = QPackageACL(str(self.domain), qpackageName)
        return qpackageACL.getPermissions(userName, qualityLevel)

    def qpackageACLExists(self, qpackageName, userName, qualityLevel=None):
        """
        Checks if a user has a permission.
        @param qpackageName: name of the qpackage to check user's permission for
        @param username: username of the user you wish to check permission for
        @param qualityLevel: qualityLevel that you wish to check permission for
        """
        qpackageACL = QPackageACL(str(self.domain), qpackageName)
        return qpackageACL.exists(userName, qualityLevel)

    def pm_LoadKnownQPackages(self):
        """
        Load list of domains with acls
        """
        qpackagesDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', str(self.domain))
        qpackages = list()
        q.logger.log('Checking if domain directory exists <%s>'%qpackagesDir, 6)
        if not q.system.fs.exists(qpackagesDir):
            q.logger.log('Directory <%s> does not exists. Return an empty list', 6)
            self.qpackageNames = qpackages
            return

        q.logger.log('Checking for QPackages acls', 6)
        for qpackageDir in q.system.fs.listDirsInDir(qpackagesDir):
            configFile = q.system.fs.joinPaths(qpackageDir, 'qpackageacl.cfg')
            if not q.system.fs.exists(configFile):
                continue
            if self.qpackageACLList(q.system.fs.getBaseName(qpackageDir)):
                qpackages.append(q.system.fs.getBaseName(qpackageDir))

        self.qpackageNames = qpackages

    def __str__(self):
        return '%s %s'%('ACL for ', self.domain.name)

    def __repr__(self):
        return str(self)