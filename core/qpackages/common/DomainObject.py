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
from pylabs.qpackages.common.enumerators import VListType

class DomainObject(BaseType):

    name = q.basetype.string(doc="The domain's unique name", allow_none=False)
    domainLogin = q.basetype.string(doc='The login for this domain', allow_none=True)
    domainPassword = q.basetype.string(doc='The password for this domain', allow_none=True)
    acl = None

    def __init__(self, name):
        if name:
            self.name = str(name)
        else:
            raise ValueError('Domain needs to have an unique name')

    def getVListFiles(self, vListType):
        ''' returns the file path of all the VLists for the domain.
        @return: list of file paths towards the different VLists
        '''
        q.logger.log('getVlistFiles for domain %s'%self.name, 8)
        files = list()
        vlistPath = self._getVListsPath(vListType)
        if not q.system.fs.isDir(vlistPath):
            q.logger.log('getVlistFiles for domain %s failed, domain VList files not found!'%self.name, 8)
            return None

        files = q.system.fs.listFilesInDir(vlistPath, filter='*.vlist')
        if files:
            q.logger.log('getVlistFiles for domain %s succeeded'%self.name, 8)
        else:
            q.logger.log('getVlistFiles for domain %s failed: not found'%self.name, 8)
        return files

    def getVListFile(self, qualityLevel, vListType):
        q.logger.log('getVlistFile for domain %s with qualityLevel %s'%(self.name, qualityLevel), 8)
        qualityLevel = QPackageQualityLevelType.getByName(str(qualityLevel)) # We do this to make sure the user requests an existing qualityLevel
        vlistPath = self._getVListsPath(vListType)
        # check whether the domain vlist folder exists
        if not q.system.fs.isDir(vlistPath):
            q.logger.log('getVlistFile for domain %s with qualityLevel %s failed , domain VList files not found!'%(self.name,str(qualityLevel)), 8)
            return None

        path = q.system.fs.joinPaths(vlistPath, '%s.vlist'%str(qualityLevel))
        # check if the path is a file
        if q.system.fs.isFile(path):
            q.logger.log('getVlistFile for domain %s with qualityLevel %s succeeded: %s'%(self.name, str(qualityLevel), path), 8)
            return path
        q.logger.log('getVlistFile for domain %s with qualityLevel %s failed: not found'%(self.name, qualityLevel), 8)
        return None

    def getDomainPath(self):
        ''' Construct the path for the domain folder '''
        path = q.system.fs.joinPaths(q.dirs.packageDir, self.name)
        return path

    def _getVListsPath(self, vListType):
        '''Construct the path for the VLists'''
        if VListType.CLIENT == vListType:
            path  = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageclient', 'vlists', self.name)
        else:
            path  = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver', 'vlists', self.name)
        if not (q.system.fs.exists(path) or q.system.fs.isDir(path)):
            raise RuntimeError('The location of the domain vlists does not exist or is not a directory (%s)'%path)
        return path

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()