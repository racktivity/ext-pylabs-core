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

from pymonkey import q
from pymonkey.baseclasses.CMDBSubObject import CMDBSubObject
from ApacheACE import ApacheACE

from ApacheCommon import parseComplexConfig
from Cheetah.Template import Template as CheetahTemplate

"""
This module contains the base classes for Apache Sites. Tomcat sites, Python
sites, HTML sites, they all inherit from these classes.

There are two important classes in this module:
- SiteTemplate: a Cheetah template class that can be inherited from
- ApacheSite: a CMDB subobject that contains the relevant config data

The ApacheSite class has a pm_template attribute that must point to a
SiteTemplate class.

The SiteTemplate class defines the structure of the config file that is written
to disk. It is divided into block to enable subclasses of the template to
insert custom information of overload information from the parent class. If you
are not familiar with Cheetah templates, try checking some of the existing
subclasses in this extension. Subclassing SiteTemplate can be done by calling

SiteTemplateChild = SiteTemplate.subclass(source="My custom source")

For more information, check the Cheetah documentation.
"""


SiteTemplate = CheetahTemplate.compile(source="""
    #block alias
    Alias /$name "$location"
    #end block

    #block pre_directory
    #end block

    <Directory "$location">
    #block directory
        #block directory_start
        #end block

        #block acl
            #if $hasACL or $hasAuth
                AuthType Basic
            #else
                AuthType None
            #end if
            #if $hasACL
                AuthName "$name"
                AuthUserFile $aclFile
                Require valid-user
            #end if
        #end block

        #block directory_end
        #end block
    #end block
    </Directory>

    <Location "/$name">
        #block location
            #if $options
                Options $options
            #end if

            #if $hasACL or $hasAuth
                Order Deny,Allow
            #else
                Order allow,Deny
                Allow from all
            #end if
            #if $hasAuth
                AuthType Basic
                AuthName '$name authentication'
                #for $item in $auth
                $item
                #end for
                #if $authRequired
                Require valid-user
                #end if
            #end if
            #block complexconfig
            #for $item in $complexConfig
                $item
            #end for
        #end block
        #end block
    </Location>

    #block post_location
    #end block
""")

class ApacheSite(CMDBSubObject):
    """
    Class which is responsible for the configuration of 1 Apache site
    """
    name = q.basetype.string(doc="The name of the site", allow_none=True)
    acl = q.basetype.dictionary(doc="list of ACEs for this site", allow_none=True)
    location = q.basetype.string(doc="location of the site files")
    complexConfig = q.basetype.dictionary(doc="is full apache config file but for one virtualhost (allows sysadmin to make 100% custom configuration but on a per site basis)", allow_none=True)
    options = q.basetype.list(doc="site specific options")
    auth = q.basetype.dictionary(doc="Authentication backend")
    authRequired = True

    # Overload this attribute if you wish to use your own template
    pm_template = SiteTemplate

    # Special modules needed for this site (must be a dictionary with module
    # names as keys and module .so locations as values)
    modules = None

    def __init__(self, name, location):
        CMDBSubObject.__init__(self)
        self.name = name
        self.location = location
        self.authRequired = True

    def addACL(self, username, passwd, right="R"):
        """
        Add user to the Access Control List
        @param username: name of the user
        @type username: string
        @param passwd: password of the user
        @type passwd: string
        @param right: access right (R, W)
        @type right: string
        @return: the new Access Control Entry object
        @rtype: ApacheACE.ApacheACE
        @raise ValueError: if a user with username already exists
        """
        if username in self.acl:
            raise ValueError("User already exists")

        aclEntry = ApacheACE(username, passwd, right)
        self.acl[username] = aclEntry
        return aclEntry

    def addAuth(self,name,authtype):
        """
        @param name: name of authentication realm
        @type name: string
        @param authtype: type of backend authentication (q.enumerators.ApacheAuthType)
        @type authtype: q.enumerators.ApacheAuthType
        """

        if name in self.auth:
            raise ValueError("Auth already exists")

        AuthClass = authtype.value
        authc = AuthClass(name)
        self.auth[name] = authc
        q.logger.log("Authentication (%s) of Type (%s) was Added" % (name, AuthClass), 5)

        return authc

    def deleteACL(self, username):
        """
        Delete user from the Access Control List
        @param username: name of the user to delete
        @type username: string
        @raise KeyError: if username not found
        """
        del self.acl[username]

    def deleteAuth(self,name):
        """
        Delete authentication
        @param name: name of authentication realm
        @type name: string

        """
        del self.auth[name]

    def pm_getTemplateContext(self, aclFileDir):
        """
        Get the template context for this class.

        Overload this method if you wish to use custom veriables in your
        template.

        @param aclFileDir: directory that should contain the ACL file for this site
        @type aclFileDir: string
        @return: the template context for this site
        @rtype: dict
        """
        return {
            "name": self.name,
            "location": self.location,
            "complexConfig": parseComplexConfig(self.complexConfig),
            "aclFile": self.pm_getACLFileName(aclFileDir),
            "auth": self.pm_getAuth(),
            "hasACL": bool(self.acl),
            "hasAuth": bool(self.auth),
            "authRequired":self.authRequired,
            "options": " ".join(set(self.options)),
        }


    def pm_getAuth(self):
        """
        Return Auth
        """
        for k,v in self.auth.iteritems():
            return v.prepareConfig()

    def pm_getACLFileName(self, aclFileDir):
        return q.system.fs.joinPaths(aclFileDir, "%s.access.conf" % (self.name, ))

    def pm_writeACL(self, aclFileDir):
        """
        Write the ACL file for this site

        @param aclFileDir: ACL file dir; MUST be unique for each vhost (to avoid name conflicts)
        @type aclFileDir: string
        """
        if not self.acl:
            return

        if not q.system.fs.isDir(aclFileDir):
            q.system.fs.createDir(aclFileDir)

        fileName = self.pm_getACLFileName(aclFileDir)
        filePath = q.system.fs.joinPaths(aclFileDir, fileName)
        # Removing the (old) file so we can create a new one with createACE
        if q.system.fs.isFile(filePath):
            q.system.fs.removeFile(filePath)

        create = True
        for ace in self.acl.values():
            q.cmdtools.apache.htpasswd.createACE(filePath, ace.userName, ace.passwd, create)
            create = False

    def pm_getConfig(self, aclFileDir):
        """
        Get the configuration for this site

        @param aclFileDir: directory where the ACL httpasswd files for this site should be stored
        @type aclFileDir: string
        @return: configuration for this site
        @rtype: string
        """
        context = self.pm_getTemplateContext(aclFileDir)
        return str(self.pm_template(searchList=[context]))
