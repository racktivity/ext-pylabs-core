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
from pylabs.qpackages.common.QPackageObject import QPackageObject
from pylabs.qpackages.common.VLists import VLists
from pylabs.qpackages.common.VListEntry import VListEntry
from pylabs.qpackages.common.enumerators import VListType


class QPackagePackagesDir(BaseType):
    """
    Manages all qpackages in the local packagedir.

    This is the main entrypoint for managing all qpackages on the local system.
    """
    vlists = q.basetype.object(VLists, doc='The Vlists for the server')

    def __init__(self):
        self.vlists = VLists(VListType.SERVER)

    def qpackageFind(self, name=None, version=None, domain=None, qualityLevels=None, supportedPlatforms=None, tags=None, buildNr=None, exactMatch=True):
        """
        Check in the local packages dir if a qpackage can be found.

        if qualitylevels not specified: look for all quality levels
        if domain not specified: look for all domains
        return array of QPackage objects

        @param name:               Name of the qpackage to find.

        optional
        @param version:            Version of the qpackage to find.
        @param domain:             Domain to find qpackage in. All domains if not specified.
        @param qualityLevels:      List of quality levels to look in, all if none supplied.
        @param supportedPlatforms: List of supportedPlatforms for which the qpackage should be supported.
        @param tags:               is comma separated list of tags
        @param buildnr:            Build number of the qpackage to find.
        @return:                   List of QPackageObjects matching the criteria.
        """

        result = list()
        resList = self.vlists.find(name, domain, version, qualityLevels,supportedPlatforms, tags, buildNr, exactMatch=exactMatch)
        for vEntry in resList:
            qpackage = QPackageObject(vEntry.domain, vEntry.qpackageName, vEntry.version)
            qpackage.buildNr = {}
            qpackage.buildNr[vEntry.qualityLevel] = str(vEntry.buildNr)
            result.append(qpackage)
        return result

    def qpackageExists(self, name, version=None, domain=None, qualityLevels=None, supportedPlatforms=None, buildNr=None):
        """
        if qualitylevels not specified: look for all local quality level
        if domain not specified, look for appropriate domain (use vlists on packagedir)
        if 1 found return True otherwise False

        @param name:               Name of the qpackage to find.
        @param version:            Version of the qpackage to find.

        optional
        @param domain:             Domain to find qpackage in. All local available domains if not specified.
        @param qualityLevels:      List of quality levels to look in, all local qualitylevels if none supplied.
        @param supportedPlatforms: List of supportedPlatforms for which the qpackage should be supported.
        @param buildnr:            Build number of the qpackage to find.

        @return:                   Boolean indicating if the QPackage exists and the criteria only match 1 QPackage.
        """
        result = self.qpackageFind(name, version=version, domain=domain, qualityLevels=qualityLevels, supportedPlatforms=supportedPlatforms, buildNr=buildNr)
        if len(result) >= 1:
            return True
        return False

    def qpackageCreate(self, name, version, domain, supportedPlatforms=None, acl=None):
        """
        create qpackage directory in qpackage package dir, make sure directory get's populated starting
        from appropriate qpackage template out of qpackageserver.
        set qpackage.cfg
        if dir exists -> fail
        always use local as quality level

        @param name:               Name of the qpackage to create.
        @param version:            Version of the qpackage to create.
        @param domain:             Domain to create qpackage in.

        optional
        @param supportedPlatforms: List of supportedPlatforms for which the qpackage should be supported.
        @param acl:

        @return:                   QPackageObject of the newly created QPackage.

        @todo: Check ACL parameter! => QPackageACL works directly on file. Is this required?

        """
        qpackageDir = q.system.fs.joinPaths(q.dirs.packageDir, domain, name)
        if q.system.fs.exists(qpackageDir):
            if q.system.fs.walk(qpackageDir, return_folders=True):
                raise IOError('Directory <%s> already exists'%qpackageDir)
            else:
                q.system.fs.removeDir(qpackageDir)

        templateQPackageDir = q.system.fs.joinPaths(q.dirs.packageDir, domain, 'template_qpackage')
        if q.system.fs.exists(templateQPackageDir):
            q.logger.log('Creating new qpackage <%s> based on template_qpackage'%name, 6)
            q.system.fs.copyDirTree(templateQPackageDir, qpackageDir)
            q.system.fs.moveDir(q.system.fs.joinPaths(qpackageDir, '0.0'), q.system.fs.joinPaths(qpackageDir, version))
            q.system.fs.removeDirTree(q.system.fs.joinPaths(qpackageDir, version, 'upload_trunk'))

        else:
            q.logger.log('Creating a new QPackage', 6)
            q.system.fs.createDir(q.system.fs.joinPaths(qpackageDir, version))
            q.system.fs.createDir(q.system.fs.joinPaths(qpackageDir, version, 'cfg' ))
        q.logger.log('Instantiating a new qpackage object', 6)

        qpackageObject = QPackageObject(domain, name, version, new=True)
        qpackageObject.supportedPlatforms = supportedPlatforms if supportedPlatforms else list()

        q.logger.log('Re-creating the configuration with the correct values', 6)
        qpackageObject.createConfig()

        return qpackageObject

    def qpackageGetObject(self, name, version, domain=None, qualityLevel=None):
        """
        Retrieve a QPackage object
        @param name:               Name of the qpackage.
        @param version:            Version of the qpackage.
        @param domain:             Domain to find qpackage in.
        @param qualityLevels:      Quality level of the QPackage
        @return:                   The requested QPackage's QPackageObject
        """
        if domain:
            return QPackageObject(domain, name, version)

        results = self.qpackageFind(name, version, domain, qualityLevels=[qualityLevel] if qualityLevel else None)
        if not results:
            raise ValueError('QPackage <%s> was not found.'%name)

        elif len(results) > 1:
            raise ValueError('Found more than one QPackage matching <%s>'%(name))
        qpackageObject = QPackageObject(results[0].domain, results[0].name, results[0].version)
        return qpackageObject

    def qpackageDelete(self, name, version, domain):
        """
        if qualitylevels not specified: delete all
        if domain not specified, look for appropriate domain (use vlists on packagedir)

        @param name:               Name of the qpackage to delete.
        @param version:            Version of the qpackage to delete.
        @param domain:             Domain to delete qpackage from.
        """
        q.logger.log('deleting files of QPackage %s with version %s'%(name, version), 8)
        qpackage = QPackageObject( domain, name, version)
        qpackageDir = q.system.fs.joinPaths(q.dirs.packageDir, qpackage.getRelativeQPackagePath())

        if not q.system.fs.exists(qpackageDir):
            raise IOError('QPackage Directory does not exist <%s>'%qpackageDir)
        q.system.fs.removeDirTree(qpackageDir)

        self.createVlists(domain)
        self.vlists.loadVLists(domain)

        if not q.system.fs.walk(q.system.fs.joinPaths(q.dirs.packageDir, str(domain), name), return_folders=True):
            q.system.fs.removeDir(q.system.fs.joinPaths(q.dirs.packageDir, str(qpackage.domain), qpackage.name))

        q.logger.log('deleted files of QPackage %s with version %s'%(name, version), 8)

    def qpackageCopy(self, name, version, domain, toName, toVersion, toDomain=None, copyFiles=False):
        """
        Copies a QPackage in the local packagedir.
        Copies all files and updates the QPackage metatdata.

        @param name:               Name of the qpackage to copy.
        @param version:            Version of the qpackage to copy.
        @param domain:             Domain to copy qpackage from.
        @param toName:             Name for the new QPackage.
        @param toVersion:          Version for the new QPackage.

        optional
        @param toDomain:           Domain to copy the QPackage to. Default same domain as QPackage copied.

        @return:                   QPackageObject of the newly created QPackage.
        """
        #try:
            #qpackageObject = self.qpackageGetObject(name, version, domain)
        #except Exception, e:
            #raise RuntimeException('Failed to find QPackage (%s, %s, %s)'%(name, version, domain))
        #toDomain = toDomain if toDomain else str(qpackageObject.domain)
        #if self.qpackageFind(toName, toVersion, toDomain):
            #raise RuntimeError('QPackage (%s, %s, %s) already exists'%(toName, toVersion, toDomain))

        #qpackageDir = qpackageObject.getRelativeQPackagePath()
        #installerDir = q.system.fs.joinPaths(qpackageDir, 'installer')
        #licenseDir = q.system.fs.joinPaths(qpackageDir, 'LICENSES')
        #cfgDir = q.system.fs.joinPaths(qpackageDir, 'cfg')

        #toQPackageObject = QPackageObject(toDomain, toName, toVersion, new=True)
        pass

    def createVlists(self, domain=None, qualityLevels=None):
        """
        walk over all qpackages in packagedir and create multiple vlists

        optional
        @param domain:           Domain to create the VLists for. Default all.
        """
        if not domain:
            for domain in self.getDomains():
                self.vlists.createVLists(domain, qualityLevels)
        else:
            self.vlists.createVLists(domain, qualityLevels)

    def getDomains(self):
        """
        List all domains in packages Dir
        """
        listOfDomains = list()
        for domain in [q.system.fs.getBaseName(domainDir) for domainDir in q.system.fs.listDirsInDir(q.dirs.packageDir)]:
            listOfDomains.append(domain)
        return listOfDomains

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __fake_data__(self):
        pass