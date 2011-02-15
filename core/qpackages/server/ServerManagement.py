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
from pylabs.enumerators.PlatformType import PlatformType
from pylabs.qpackages.server.SessionManager import SessionManager
from pylabs.qpackages.common.QPackageACL import QPackageACL
from pylabs.qpackages.server.DomainACL import DomainACL
from pylabs.qpackages.common.QPackagePackagesDir import QPackagePackagesDir
from pylabs.qpackages.common.VLists import VLists
from pylabs.qpackages.common.enumerators import VListType
from pylabs.qpackages.server.AccessControl import AccessControl

class ServerManagement(BaseType):
    """
    User interface to a QPackage server management mounted on q (q.qpackageserver) which
    connects all different components (q.qpackages.*, SessionManager, ...) from a server 
    perspective.
    
    This will be the main interface for the QPackageServer XMLRPC interface
    """
    accessControl = q.basetype.object(AccessControl, doc='AccessControl object')
    sessions = q.basetype.object(SessionManager, doc='The servers user database', default=SessionManager())
    packagesDir = q.basetype.object(QPackagePackagesDir,doc='QPackagePackagesDir', default=QPackagePackagesDir())
    vlists = q.basetype.object(VLists, doc='The client Vlists from master server')

    def __init__(self):
        """
        Initializes all properties.
        """
        q.logger.log('Initializing ServerManagement', 5)
        self.vlists = VLists(VListType.CLIENT)
        self.accessControl = AccessControl()
    
    
    ####################
    ## Authentication ##
    ####################
    
    def authenticate(self, login, password):
        """
        Checks if the given credential pair is correct.
        
        @param login:    Login to authenticate
        @param password: Password of the login to authenticate.
        
        @return:         Boolean indicating if the authentication was successfull.
        """

        return self.accessControl.users.validate(login, password)
    
    ###################
    ## Authorization ##
    ###################
    def authorize(self, domainName, qualityLevel, login, qpackageName=None, permissionType=q.enumerators.ACLPermission.R):
        """
        Check if user has certain permissions on domain/QPackage
        @param domainName: name of the domain
        @param qualityLevel: quality level to check permissions for
        @param login:    Login to check permissions for
        @param qpackageName: name of the qpackage to check user's permission on
        @param permissionType: type of permission to check for user
        """
        if self.checkDomainPermissions(domainName, login, permissionType):
            return True
        if qpackageName and self.checkQPackagePermissions(domainName, qpackageName, login, qualityLevel, permissionType):
            return True
        return False

    def checkDomainPermissions(self, domainName, login, permissionType):
        """
        Check if user has certain permissions on domain
        @param domainName: name of the domain
        @param login:    Login to check permissions for
        @param permissionType: type of permission to check for user
        """
        q.logger.log('Checking if user %s has permission %s on domain %s'%(login, permissionType, domainName), 6)
        if str(permissionType) in str(self.accessControl.domainsACL.domainACLGetPermissions(domainName, login)):
            return True
        q.logger.log('Checking if user %s belongs to a group which has permission %s on domain %s'%(login, permissionType, domainName), 6)
        for group in self.accessControl.groups.listGroupsOfUser(login):
            if str(permissionType) in str(self.accessControl.domainsACL.domainACLGetPermissions(domainName, group)):
                return True
        return False
    
    def checkQPackagePermissions(self, domainName, qpackageName, login, qualityLevel, permissionType):
        """
        Check if user has certain permissions on QPackage
        @param domainName: name of the domain
        @param qpackageName: name of the qpackage to check user's permission on
        @param login:    Login to check permissions for
        @param qualityLevel: quality level to check permissions for
        @param permissionType: type of permission to check for user
        """
        domainACL = self.accessControl.domainsACL.domainACLGet(domainName)
        if str(permissionType) in str(domainACL.qpackageACLGetPermissions(qpackageName, login, qualityLevel)):
            return True
        q.logger.log('Checking if user %s belongs to a group which has permission %s on qpackage %s'%(login, permissionType, qpackageName), 6)
        for group in self.accessControl.groups.listGroupsOfUser(login):
            if str(permissionType) in str(domainACL.qpackageACLGetPermissions(qpackageName, group, qualityLevel)):
                return True
        return False
    
    def createDomain(self, domainName, authoritative):
        """
        Create a domain
        @param domainName: name of the domain to create
        @param authoritative: boolean which defines if this domain is authoritative 
        """
        domainDir = q.system.fs.joinPaths(q.dirs.packageDir, domainName)
        if not q.system.fs.exists(domainDir):
            q.system.fs.createDir(domainDir)

        domainCfgDir=q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', domainName)
        if not q.system.fs.exists(domainCfgDir):
            q.system.fs.createDir(domainCfgDir)
        domainCfg = q.system.fs.joinPaths(domainCfgDir, 'domainconfig.cfg')
        if q.system.fs.exists(domainCfg):
            q.system.fs.removeFile(domainCfg)

        iniFile = q.tools.inifile.new(domainCfg)
        iniFile.addSection('main')
        iniFile.addParam('main', 'authoritative', int(authoritative))
        iniFile.write()
