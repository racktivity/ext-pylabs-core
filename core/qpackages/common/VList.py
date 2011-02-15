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
from pylabs.enumerators import QPackageQualityLevelType
from pylabs.qpackages.common.DomainObject import DomainObject
from pylabs.qpackages.common.VListEntry import VListEntry
from pylabs.qpackages.common.enumerators import VListType

VERSION      = 1

class VList(BaseType):
    """
    A VList is a list of QPackages with base properties provided by a domain for a given qualityLevel.
    """
    domain       = q.basetype.object(DomainObject, doc='The domain this VList belongs to', allow_none=True, default=None)
    qualityLevel = q.basetype.object(QPackageQualityLevelType, doc='The qualityLevel this Vlist represents', allow_none=False)
    version      = q.basetype.integer(doc='Version of the VList format', allow_none=False, default=VERSION)
    numEntries   = q.basetype.integer(doc='Number of QPackages in the VList', allow_none=False, default=0)
    vlistType    = q.basetype.enumeration(VListType, doc='Specifies whether this VList is a server VList or a client VList', allow_none=False, default=VListType.CLIENT)
    _vlistfile   =  None # this will be filled in when the fileDescriptor is opened, and only then!

    def __init__(self, domain, qualityLevel, vlistType=VListType.CLIENT, create=False):
        ''' Construct the object
        @param domain:       : Domain of the VList
        @param qualityLevel  : qualityLevel of the VList

        optional
        @param create:       : Create a new list if True
        @param vlistType:    : Type of the VList (server, client)
        '''
        # check whether the domain value contains the correct type.
        if isinstance(domain, basestring):
            self.domain = DomainObject(domain)
        elif isinstance(domain, DomainObject):
            self.domain = domain
        else:
            raise ValueError('domain should be a string or a DomainObject')

        # check whether qualityLevel is the correct type.
        if isinstance(qualityLevel, (basestring, QPackageQualityLevelType)):
            self.qualityLevel = QPackageQualityLevelType.getByName(str(qualityLevel))
        else:
            raise ValueError('qualityLevel should be a string or a QPackageQualityLevelType')

        if isinstance(vlistType, (basestring, VListType)):
            self.vlistType = VListType.getByName(str(vlistType))
        else:
            raise ValueError('VListType should be a string or a VListType Object')
        # if create == True we should not validate nor parse, but write initial header (if file does not exist).
        if create:
            self._prepareVList()
        else:
            # validating the vlist for correctness
            if not self.isListValid():
                raise RuntimeError('The VList for domain %s with qualityLevel %s is incorrectly formatted'%(self.domain.name, str(self.qualityLevel)))

    def parse(self):
        ''' Will take a VList file header and parse it
        '''
        # construct vlist path
        q.logger.log('Start parsing the VList header: %s'%(self), 8)
        path = self._getVListPath()
        fileDescriptor = open(path, 'r')
        foundVersion=False
        foundEntries=False
        for line in fileDescriptor:
            if foundEntries and foundVersion:
                break
            if line.startswith('#@schemaversion:'):
                self.version = int(line[line.index(':')+1:].strip())
                foundVersion=True
            elif line.startswith('#@entries:'):
                self.numEntries = int(line[line.index(':')+1:].strip())
                foundEntries=True
        fileDescriptor.close()
        q.logger.log('Finished parsing the VList header: %s'%(self), 8)

    def parseEntry(self, line):
        ''' Parse a VList line
        This is mainly used to facilitate the search on certain fields

        @param line:    VList line you whish to parse.
        @return:        VListEntry
        '''
        q.logger.log('Start parsing entry %s'%line, 8)
        entry = VListEntry()
        lineparts = line.split('|') # pipe is the separator
        entry.qpackageName = lineparts[0]
        entry.version = lineparts[1]
        entry.buildNr = str(lineparts[2]) if lineparts[2] else '0'
        entry.supportedPlatforms = lineparts[3].split(',') # platforms are comma separated
        entry.tags = lineparts[4].split(',') # tags are comma separated
        entry.description = lineparts[5]
        q.logger.log('Parsed entry %s from VList %s'%(entry, self), 8)
        return entry

    def find(self, qpackageName=None, version=None, buildNr=None, supportedPlatforms=None, tags=None, description=None, exactMatch=True):
        ''' Search for QPackages in this list matchin all defined criteria

        optional
        @param qpackageName:    Name of the QPackage you are looking for
        @param version:     Version of the QPackage you are looking for
        @param buildNr:     Build number of the QPackage you are looking for
        @param supportedPlatforms: list of supported platforms you are searching in
        @param tags:        Tags assigned to the QPackage you are looking for
        @param description: Description of the QPackage you are looking for

        @return:            List of VListEntries that match ALL specified criteria

        @TODO: implement extra criteria
        '''
        q.logger.log('Started searching on VList from domain %s with qualityLevel %s'%(self.domain.name, str(self.qualityLevel)), 8)

        #open filedescriptor and go to the first line for entries
        path = self._getVListPath()
        fileDescriptor = open(path, 'r')
        results = list()
        i = 0
        for line in fileDescriptor:
            if line.startswith('#@schemaversion:') or line.startswith('#@entries:'):
                continue
            ''' Ok we will not parse each line into an object as it is probably to heavy when we have a huge VList.
            But we will just take the line, split it into pieces and then search the pieces. By reassigning the line variable
            and the linebits we allow the GC to reclaim the memory when it runs. However we do not enforce a GC (NOT DONE)
            @TODO: IMPORTANT: for supportedPlatforms we do not check the parents, so you need an exact string match.
            This can be added later (so if you search on linux32 and in the list is generic you will match) but for the first version
            we don't find it a priority to spend time on it.
            I've documented below what piece stands for what, we can do this as the format should never change.
            [0] = qpackageName
            [1] = version
            [2] = buildNr
            [3] = supportedPlatforms
            [4] = tags
            [5] = description
            '''
            linebits = line.split('|')
            if qpackageName:
                if (exactMatch and not qpackageName.lower() == linebits[0]) or not qpackageName.lower() in linebits[0]:
                    continue
            if version and not version == linebits[1]:
                continue
            if buildNr and not str(buildNr) == str(linebits[2]):
                continue
            if supportedPlatforms:
                foundSupportedPlatform = False
                for sup in supportedPlatforms.split(','):
                    if sup.strip().lower() in linebits[3].lower():
                        foundSupportedPlatform = True
                if not foundSupportedPlatform: 
                    continue
            if tags:
                foundTag = False
                for tag in tags.split(','):
                    if tag.strip().lower() in linebits[4].lower():
                        foundTag = True
                if not foundTag:
                    continue
            if description and not description.lower() in linebits[5]:
                continue
            results.append(line.strip())
        q.logger.log('Finished search on VList %s'%self, 8)
        return results

    def isListValid(self):
        ''' Checks whether the VList is a valid VList

        This means the number of entries is the same as the number in the list,
        the list should not contain twice the same QPackage
        for each QPackage the name, version and buildNr should be filled in

        @return:      Boolean True is valid, false if not valid'''

        q.logger.log('Checking if VList for domain %s with qualityLevel %s is valid'%(self.domain.name, str(self.qualityLevel) ), 8)
        path = self._getVListPath()
        fileDescriptor = open(path, 'r')
        entries = 0
        lines = 0
        version = 0
        for line in fileDescriptor:
            if line.strip():
                if not line.startswith('#'):
                    lines += 1
                else:
                    if line.startswith('#@schemaversion:'):
                        version = int(line[line.index(':')+1:].strip())
                    elif line.startswith('#@entries:'):
                        entries = int(line[line.index(':')+1:].strip())
        fileDescriptor.close()

        if version != 1: # we only know version 1
            q.logger.log('Unknown version (%s) in the VList for domain %s with qualityLevel %s'%(version, self.domain.name, str(self.qualityLevel)), 5)
            return False
        if not entries == lines:
            q.logger.log('The metadata in the VListfile is incorrect!', 8)
            return False
        return True

    def writeEntry(self, entry):
        ''' Will write an entry to the file and augment the numentries with 1

        @param entry: String to be added to the VList file'''

        if not self._vlistfile:
            raise RuntimeError('Vlist File is not open for writing.')

        q.logger.log('Write VList entry for domain %s, qualityLevel %s to disk'%(self.domain, str(self.qualityLevel)), 8)
        self.numEntries +=1
        self._vlistfile.write(entry)
        if self.numEntries%100 == 0:
            self._vlistfile.flush()
        q.logger.log('VList entry for domain %s, qualityLevel %s written to disk'%(self.domain, str(self.qualityLevel)), 8)

    def finishWriting(self):
        ''' Closes the Vlist file and removes it from the class, so we cannot write to it anymore '''
        if not self._vlistfile:
            raise RuntimeError('Vlist File is not open, cannot close.')

        q.logger.log('Closing VlistFile for domain %s, qualityLevel %s'%(str(self.domain), str(self.qualityLevel)), 8)
        self._writeMeta()
        self._vlistfile.flush()
        self._vlistfile.close()
        q.system.fs.copyFile(self._vlistfile.name, self._getVListPath(create=True))
        q.system.fs.remove(self._vlistfile.name)
        self._vlistfile = None
        q.logger.log('Closed VlistFile for domain %s, qualityLevel %s'%(str(self.domain), str(self.qualityLevel)), 8)

    def _prepareVList(self):
        ''' Create a FileDescriptor towards the correct VList file and open it for write '''
        self._vlistfile = open(q.system.fs.getTempFileName(), 'w')

    def _writeMeta(self):
        ''' Will write the metadata to the VList file'''
        q.logger.log('Creating VList meta for domain %s, qualityLevel %s'%(self.domain, str(self.qualityLevel)),8)
        self._vlistfile.write('#@schemaversion:%d\n'%VERSION) # version
        self._vlistfile.write('#@entries:%d\n'%self.numEntries or 0)# numEntries
        q.logger.log('Creating VList meta for domain %s, qualityLevel %s'%(self.domain, str(self.qualityLevel)),8)

    def _getVListPath(self, create=False):
        ''' Returns the path of the VList '''
        if self.vlistType == VListType.CLIENT:
            path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageclient', 'vlists', self.domain.name, '%s.vlist'%str(self.qualityLevel))
        else:
            path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver', 'vlists', self.domain.name, '%s.vlist'%str(self.qualityLevel))

        if create:
            q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver', 'vlists', self.domain.name))
            return path
        else:
            if q.system.fs.exists(path):
                return path
            raise RuntimeError('%s VList file with domain %s and qualityLevel %s does not exist'%(str(self.vlistType), self.domain.name, str(self.qualityLevel)))

    def __str__(self):
        return '%s_%s'%(self.domain, self.qualityLevel)

    def __repr__(self):
        return str(self)