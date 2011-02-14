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
from pymonkey.enumerators import QPackageQualityLevelType

from pymonkey.qpackages.common.DomainObject import DomainObject

class VListEntry(BaseType):

    qpackageName = q.basetype.string(doc='Name for the QPackage', allow_none=False)
    version = q.basetype.string(doc='Version of the QPackage', allow_none=False)
    buildNr = q.basetype.string(doc='number of the build', allow_none=False, default='0')
    supportedPlatforms = q.basetype.list(doc='supported platforms of this QPackage', allow_none=False, default=list())
    tags = q.basetype.list(doc='Tags for the QPackage', allow_none=True)
    description = q.basetype.string(doc='Optional description for the QPackage', allow_none=True)
    domain = q.basetype.object(DomainObject, doc='Domain object', allow_none=False)
    qualityLevel = q.basetype.enumeration(QPackageQualityLevelType, doc='qualityLevel where the QPackage belongs', allow_none=True)

    @staticmethod
    def getFromString(domain, qualityLevel, entryString):
        ''' Returns a VListEntry from a string representation 
        @param entry: entry from a vlist'''
        q.logger.log('Start parsing entry %s'%entryString, 8)
        entry = VListEntry()
        lineparts = entryString.split('|') # pipe is the separator
        entry.qpackageName = lineparts[0]
        entry.version = lineparts[1]
        entry.buildNr = str(lineparts[2]) if lineparts[2] else '0'
        entry.supportedPlatforms = [str(supportedPlatform).replace(' ', '') for supportedPlatform in lineparts[3].split(',')] # platforms are comma separated
        entry.tags = lineparts[4].split(',') # tags are comma separated
        entry.description = lineparts[5]
        entry.domain = domain
        entry.qualityLevel = qualityLevel
        q.logger.log('Parsed entry %s '%(entry), 8)
        return entry

    def __str__(self):
        return '%s %s (%s)'%(self.qpackageName, self.version, str(self.qualityLevel))

    def __repr__(self):
        return self.__str__()