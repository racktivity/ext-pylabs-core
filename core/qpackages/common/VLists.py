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

from pymonkey import q
from pymonkey.baseclasses import BaseType
from pymonkey.enumerators import QPackageQualityLevelType

from pymonkey.qpackages.common.enumerators import VListType
from pymonkey.qpackages.common.QPackageObject import QPackageObject
from pymonkey.qpackages.common.VList import VList
from pymonkey.qpackages.common.VListEntry import VListEntry
from pymonkey.qpackages.common.DomainObject import DomainObject

class VLists(BaseType):
    ''' This class will generate VLists and provide the logic to reload them.
    '''
    vlists = q.basetype.dictionary(doc='dict of all VLists known on this system for the current qualityLevel', default=dict(), allow_none=True)
    _type = q.basetype.enumeration(VListType, doc='Type of this VListContainer')

    def __init__(self, vListType):
        if not isinstance(vListType, (basestring, VListType)):
            raise ValueError('vListType should be a valid type please check q.enumerators.VListType')
        else:
            self._type = VListType.getByName(str(vListType))
        self.loadVLists()

    def getDomains(self):
        ''' This will list all the domains that are known
        @return: list of Domains
        '''
        domains = list()
        domainPath = None
        if self._type == VListType.SERVER:
            serverVlistDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver', 'vlists')
            if q.system.fs.exists(serverVlistDir):
                domainPath = q.system.fs.listDirsInDir(serverVlistDir)
                
        else:
            clientVlistDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageclient', 'vlists')
            if q.system.fs.exists(clientVlistDir):
                domainPath = q.system.fs.listDirsInDir(clientVlistDir)
        if domainPath:
            for path in domainPath:
                domain = DomainObject(q.system.fs.getBaseName(path))
                domains.append(domain)
        return domains

    def loadVLists(self, domain=None, qualityLevels=None):
        ''' Loads all the vlists in memory (only meta)

        @param domain: the domain you wish to load, if None, load all known domains
        '''
        if domain:
            q.logger.log('loading the Vlist metadata for domain %s'%str(domain), 8)
            if not qualityLevels:
                domVlists = self.getVLists(domain)
            else:
                domVlists  = dict()
                if not isinstance(qualityLevels, (list, tuple)):
                    qualityLevels = (qualityLevels,)
                for qualityLevel in qualityLevels:
                    domVlists['%s_%s'%(domain, qualityLevel)] = self.getVList(domain, qualityLevel)
            for key in domVlists.iterkeys():
                self.vlists[key] = domVlists[key]
            q.logger.log('loaded the Vlist metadata for domain %s'%str(domain), 8)
        else:
            for domain in self.getDomains():
                self.loadVLists(domain, qualityLevels)

    def reloadVLists(self, domain=None):
        ''' reloads VLists (e.g.: when QPackages have been added, updated or removed).
        
        @param domain: if domain is given reload the VLists for that domain, else reload them all
        '''
        if domain:
            q.logger.log('Reloading the Vlist metadata for domain %s'%domain, 8)
            vlists = self.getVLists(domain)
            for key in vlists.iterkeys():
                self.vlists['%s_%s'%(domain.name,key)] = vlists[key]
        else:
            q.logger.log('reloading the Vlist metadata', 8)
            for domain in self.getDomains():
                vlists = self.getVLists(domain)
                for key in vlists.iterkeys():
                    self.vlists[key] = vlists[key]
        q.logger.log('Reloading VList metadata finished', 8)

    def createVLists(self, domain=None, qualityLevels=None):
        ''' create VLists for the selected domain
        @param domain: domain for the VLists to be generated
        @param qualityLevels: quality levels to create vlists for
        '''
        if self._type == VListType.CLIENT:
            raise RuntimeError('Cannot create VLists for clients')
        if domain:
            self._writeEntries(domain, qualityLevels)
        else:
            for domain in self.getDomains():
                self._writeEntries(domain, qualityLevels)

    def _writeEntries(self, domain, qualityLevels=None):
        ''' Loop over the QPackages in a domain and add them to the appropriate QualityLevel
        @param domain: the domain to loop over
        '''
        if not isinstance(domain, (basestring, DomainObject)):
            raise ValueError('Domain should be a string or a DomainObject')
        else:
            domain = DomainObject(str(domain))

        domainPath = domain.getDomainPath()
        if not q.system.fs.exists(domainPath):
            q.system.fs.createDir(domainPath)
        listQPackages = q.system.fs.listDirsInDir(domainPath)
        vlists = dict()
        # creating all Vlists, so they can prepare to be written.
        if not qualityLevels:
            qualityLevels = ('trunk', 'test', 'unstable', 'beta', 'stable')
        if not isinstance(qualityLevels, (list, tuple)):
            qualityLevels = (str(qualityLevels),)
        for ql in qualityLevels:
            vlists[str(ql)] = VList(domain, str(ql), self._type, create=True)

        # loop over all qpackage folders
        for qpackagePath in listQPackages:
            qpackageName = q.system.fs.getBaseName(qpackagePath)
            # list all versions of the qpackage
            qpackageVersionPath = q.system.fs.listDirsInDir(qpackagePath)
            # loop over versions and process them
            for versionPath in qpackageVersionPath:
                version = q.system.fs.getBaseName(versionPath)
                if not q.system.fs.isDir(q.system.fs.joinPaths(versionPath, 'cfg')) or not q.system.fs.isFile(q.system.fs.joinPaths(versionPath, 'cfg', 'qpackage.cfg')):
                    q.console.echo('WARNING: Directory %s does not have a valid QPackage structure.\n'%versionPath)
                    continue
                try:
                    qpackage = QPackageObject(domain, qpackageName, version)
                except Exception, e:
                    q.console.echo('WARNING: Failed to parse configuration of <%s>\n\"%s\".\nPlease make sure your package directory only contains valid QPackages.\n'%(q.system.fs.joinPaths(versionPath, 'cfg', 'qpackage.cfg'),e))
                    continue
                if not qpackage.buildNr:                    
                    buildNr = 'NEW'
                else:
                    buildNr = 'MOD'
                added = False
                qualitylevel = q.qpackages.getDefaultQualityLevel() or 'trunk'
                if q.system.fs.exists(q.system.fs.joinPaths(versionPath, 'upload_%s'%qualitylevel)):
                    qpackageString = '%s|%s|%s|%s|%s|%s\n'%(qpackage.name, qpackage.version, buildNr,
                                             (', '.join(str(plat) for plat in qpackage.supportedPlatforms)),
                                              (', '.join(str(tag) for tag in qpackage.tags)),
                                               qpackage.description)
                    if str(qualitylevel) in vlists:
                        vlists[str(qualitylevel)].writeEntry(qpackageString)
                        added = True

                for key in qpackage.buildNr.iterkeys():
                    if not key in qualityLevels:
                        continue
                    if str(key) == str(qualitylevel) and added:
                        continue
                    qpackageString = '%s|%s|%s|%s|%s|%s\n'%(qpackage.name, qpackage.version, qpackage.buildNr[key],
                                                 (', '.join(str(plat) for plat in qpackage.supportedPlatforms)),
                                                  (', '.join(str(tag) for tag in qpackage.tags)),
                                                   qpackage.description)
                    vlists[key].writeEntry(qpackageString)
        for vlist in vlists.itervalues():
            vlist.finishWriting()

        return vlists.values()

    def getVLists(self, domainName):
        ''' returns a list of VLists for the selected domain
        @param domainName: Name of the domain for the VLists to be returned
        @return: dict containing the vlists keyed on their qualityLevel
        '''
        # make sure this is a DomainObject
        domain = DomainObject(domainName)

        vlists = dict()
        for path in domain.getVListFiles(self._type):
            qualityLevel = q.system.fs.getBaseName(path).replace('.vlist','')
            vlist = VList(domain, str(qualityLevel), self._type, create=False)
            vlist.parse()
            vlists['%s_%s'%(vlist.domain.name, qualityLevel)] = vlist
        return vlists

    def getVList(self, domain, qualityLevel):
        ''' returns a VList for the selected domain and qualityLevel
        @param domain: domain that should be used for the vlist generation
        @param qualityLevel: QPackageQualityLevel '''
        #make sure this is a domain obect
        domain = DomainObject(str(domain))
        path =  domain.getVListFile(qualityLevel, self._type)
        vlist = VList(domain, str(qualityLevel), self._type, create=False)
        vlist.parse()
        return vlist

    def find(self, qpackageName=None, domain=None, version=None, qualityLevels=None, supportedPlatforms="", tags="", buildNr="", description='', exactMatch=True):
        ''' Will search the QPackage in the VLists and return it when found

        @param qpackageName: Name of the QPackage you wish to find

        optional
        @param domain:         search only a specific domain
        @param version:        Version of the QPackage you wish to find
        @param qualityLevels:  list of qualityLevels you are searching for. If none given search on current.
        @param supportedPlatforms: list of supported platforms you are searching in
        @param tags: is comma separated list of tags
        @param buildNr: build number you are searching for
        @param description: description you are searching for

        @return: list(VlistEntry)'''
        results = list()
        vlists = list()

        if domain:
            domList = (domain,)
        else:
            domList = self.getDomains()

        for domain in domList:
            for vlist in self.vlists.itervalues():
                if vlist.domain.name == str(domain):
                    if qualityLevels:
                        if not str(vlist.qualityLevel) in qualityLevels:
                            continue
                    vlists.append(vlist)
        for vlist in vlists:
            resList = vlist.find(qpackageName=qpackageName, version=version, buildNr=buildNr, supportedPlatforms=supportedPlatforms, tags=tags, description=description, exactMatch=exactMatch)
            for qpackageString in resList:
                vEntry = VListEntry.getFromString(vlist.domain, vlist.qualityLevel, qpackageString)
                results.append(vEntry)
        return results

    def findDeep(self, all='', tags='', description=''):
        ''' Will search the tags, description for certain information

        This will take longer!
        @param all: string to search for in all fields of the VLists
        @param tags: comma separated string for searching multiple tags
        @param description: string to search for in the description field
        @return: list(VlistEntry)
        '''
        results = list()
        for vlist in self.vlists.itervalues():
            results.extend(vlist.findDeep(all, tags, description))
        return results