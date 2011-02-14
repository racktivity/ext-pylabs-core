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
from pymonkey.baseclasses import BaseType
from pymonkey.enumerators.PlatformType import PlatformType

class QPackageDomains(BaseType):
    """
    Wrapper class for a list of QPackageDomain objects.
    This class contains logic to populate itself based on the
    qpackagedomainlist.cfg file 
    """
    pm_QPackageDomains = q.basetype.dictionary(doc="Internal list of known domains", allow_none=True, default=dict())
    
    def __init__(self):
        """
        Initialize the list, read from config file
        """
        self.pm_LoadDomainConfigs()

    def qpackageDomainAdd(self, domainName, host, login=None, password=None):
        """
        Configures a new domain and stores configuration

        @param domainName: Name of the domain to add
        @param host:           IP/dns of the domain to add
        @param login:          Login used to authenticate to the master qpackage server which is serving this domain
        @param password:       Password used to authenticate to the master qpackage server which is serving this domain
        """
        q.logger.log('Adding domain %s'%domainName, 5)

        q.qshellconfig.loadConfigFile('qpackagedomainlist')

        for qpackageDomain in self.pm_QPackageDomains.itervalues():
            if qpackageDomain.name == domainName or qpackageDomain.host == host:
                raise ValueError('Domain already exists')

        q.qshellconfig.qpackagedomainlist.setParam(domainName, 'ipaddr', host)
        if login:
            q.qshellconfig.qpackagedomainlist.setParam(domainName, 'login', login)
        if password:
            q.qshellconfig.qpackagedomainlist.setParam(domainName, 'password', password)

        self.refresh()
        q.qshellconfig.refresh()

    def qpackageDomainRemove(self, domainName):
        """
        Remove domain from the configured domains

        @domainName: name of the domain to remove
        """

        q.logger.log('Removing domain <%s>'%domainName, 5)

        q.qshellconfig.loadConfigFile('qpackagedomainlist')

        if not domainName in self.pm_QPackageDomains:
            raise ValueError('Domain %s does not exist'%domainName)

        q.qshellconfig.qpackagedomainlist.removeSection(connectionName)

        self.refresh()
        q.qshellconfig.refresh()

    def refresh(self):
        """
        Update/Refresh configured domains
        """
        q.logger.log('Updating configured domains', 5)
        self.pm_LoadDomainConfigs()

    def pm_LoadDomainConfigs(self):
        """
        Load all domains configurations defined in qpackagedomainlist.cfg
        """
        q.logger.log('Loading configured domains', 5)

        domains = dict()

        q.qshellconfig.loadConfigFile('qpackagedomainlist')

        for domainName in q.qshellconfig.qpackagedomainlist.getSections():
            try:
                host = q.qshellconfig.qpackagedomainlist.getParam(domainName, 'ipaddr',  defaultValue=None, forceDefaultValue=True)
                login = q.qshellconfig.qpackagedomainlist.getParam(connectionName, 'login',  defaultValue=None, forceDefaultValue=True)
                password = q.qshellconfig.qpackagedomainlist.getParam(connectionName, 'password',  defaultValue=None, forceDefaultValue=True)

                domain = QPackageDomain(domainName, host)
                domain.login = login if login else '*NONE*'
                domain.password = password if password else '*NONE*'

                domains[domainName] = domain

            except Exception, e:
                pass
        self.pm_QPackageDomains = domains

    #required iterable elements
    def __iter__(self):
        return self.pm_QPackageDomains.values().__iter__()
    
    def __len__(self):
        return self.pm_QPackageDomains.__len__()
    
    def __contains__(self, v):
        if isinstance(v, str):
            return v in self.pm_QPackageDomains.keys()
        elif isinstance(v, QPackageServerConnection):
            return v in self.pm_QPackageDomains.values()
    
    def __getitem__(self, v):
        if isinstance(v, int):
            return self.pm_QPackageDomains.__getitem__(self.pm_QPackageDomains.keys()[v])
        elif isinstance(v, str):
            return self.pm_QPackageDomains.__getitem__(v) 


class QPackageDomain(BaseType):
    """
    represents a qpackage domain
    has logic to work with a domain
    """
    name              = q.basetype.string(doc='Name of your domain', allow_none=False)
    host              = q.basetype.string(doc='IP/dns of your domain', allow_none=False)
    login             = q.basetype.string(doc='Login used to authenticate to the master qpackage server which is serving this domain', allow_none=True)
    password          = q.basetype.string(doc='Password used to authenticate to the master qpackage server which is serving this domain.', allow_none=True)

    def __init__(self, domainName, host, login=None, password=None):
        """
        @param domainName: Name of your domain
        @param host:           IP/dns of your domain
        @param login:          Login used to authenticate to the master qpackage server which is serving this domain
        @param password:       Password used to authenticate to the master qpackage server which is serving this domain
        """
        self.name = domainName
        self.host = host
        self.login = login
        self.password = password

    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)