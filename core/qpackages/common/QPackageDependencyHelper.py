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
from pylabs.enumerators import PlatformType
from pylabs.qpackages.common.enumerators import DependencyType
from pylabs.qpackages.common.VLists import VLists
from pylabs.qpackages.common.enumerators import VListType
from pylabs.qpackages.common.QPackageVersioning import QPackageVersioning
from pylabs.qpackages.common.QPackageObject import QPackageObject

class QPackageDependencyHelper(BaseType):
    vlists = q.basetype.object(VLists, default=VLists(VListType.CLIENT))

    def __init__(self):
        self.vlists.loadVLists()
        self._depList = list()

    def getMostApplicableQPackage(self, dependencyDef, supportedPlatform):
        """
        Find the most applicable QPackage in the vlists matching dependency def
        @param dependencyDef: DependencyDef object
        @param supportedPlatform: platforms
        """
        results = self.vlists.find(dependencyDef.name, dependencyDef.domain, qualityLevels=[q.qpackages.getDefaultQualityLevel()])
        results.sort(cmp=QPackageVersioning.versionCompare, key=lambda qpackageObject:qpackageObject.version)

        if not dependencyDef.maxversion and not dependencyDef.minversion:
            results.reverse()
            for qpackage in results:
                if self._checkSupportedPlatforms(qpackage, supportedPlatform):
                    return qpackage
            raise ValueError('Failed to find an applicable QPackage for <%s>'%dependencyDef.name)

        applicableQPackages=list()

        for index, qpackage in enumerate(results):
            if not self._checkSupportedPlatforms(qpackage, supportedPlatform):
                if index == len(results) -1 and not applicableQPackages:
                    raise ValueError('Failed to find an applicable QPackage for <%s>'%dependencyDef.name)
                continue
            if dependencyDef.maxversion:
                ## check if qpackage matching the maxversion is available
                if qpackage.version == dependencyDef.maxversion:
                    return qpackage
                ##check if qpackage version is less than max version and greater than or equal min version
                elif dependencyDef.minversion and QPackageVersioning.versionCompare(qpackage.version, dependencyDef.maxversion) < 0 \
                 and QPackageVersioning.versionCompare(qpackage.version, dependencyDef.minversion) >= 0:
                    applicableQPackages.append(qpackage)

            elif dependencyDef.minversion:
                if QPackageVersioning.versionCompare(qpackage.version, dependencyDef.minversion) >= 0:
                    applicableQPackages.append(qpackage)

        if applicableQPackages:
            ## since qpackages are sorted ascendingly based on version, take the last qpackage matching (highest available version)
            return applicableQPackages[-1]
        raise ValueError('Failed to find an applicable QPackage for <%s>'%dependencyDef.name)

    def listDependency(self, qpackageDomain, qpackageName, qpackageVersion, platform=q.platform):
        """
        Retrieve a one level dependency list
        @param qpackageDomain: domain of the qpackage
        @param qpackageName: name of the QPackage
        @param qpackageVersion: version of the QPackage
        @param platform: platform type to show dependencies for
        """
        try:
            qpackageObject = QPackageObject(qpackageDomain, qpackageName, qpackageVersion)
        except:
            raise RuntimeError('Please download QPackage <%s, %s, %s>'%(qpackageName,qpackageVersion,qpackageDomain))
        dep = list()
        for dependency in qpackageObject.getRuntimeDependencies(str(platform)):
            depQPackageObject = self.getMostApplicableQPackage(dependency, str(platform))
            try:
                qpackage = QPackageObject(depQPackageObject.domain, depQPackageObject.qpackageName, depQPackageObject.version)
                dep.append(qpackage)
            except:
                raise RuntimeError('Please download QPackage <%s, %s, %s>'%(depQPackageObject.qpackageName,depQPackageObject.version,depQPackageObject.domain))

        return dep

    def getFlatDependency(self, qpackageDomain, qpackageName, qpackageVersion, platform = q.platform):
        """
        Get a flat list of dependencies of QPackage
        @param qpackageDomain: domain of the qpackage
        @param qpackageName: name of the QPackage
        @param qpackageVersion: version of the QPackage
        @param platform: platform type to show dependencies for
        """
        flatDep = set()
        deplist = self.listDependency(qpackageDomain, qpackageName, qpackageVersion, platform)
        for dep in deplist:
            if not self._checkIfQPackageInList(dep, flatDep):
                flatDep.add(dep)

        for dep in deplist:
            deps = self.getFlatDependency(dep.domain, dep.name, dep.version, platform)
            for dep in deps:
                if not self._checkIfQPackageInList(dep, flatDep):
                    flatDep.add(dep)
        return list(flatDep)

    def exportDependencyTree(self, qpackageDomain, qpackageName, qpackageVersion, platform = q.platform):
        """
        Print Dependencies for a QPackage in a tree format
        @param qpackageDomain: domain of the qpackage
        @param qpackageName: name of the QPackage
        @param qpackageVersion: version of the QPackage
        @param platform: platform type to show dependencies for
        @param padding: padding string
        @param sign: sign to distinguish the last element
        @param append: if True will append a *, for QPackage already in the tree
        """
        self._depList = list()
        self._exportDependencyTree(qpackageDomain, qpackageName, qpackageVersion, platform)

    def _exportDependencyTree(self, qpackageDomain, qpackageName, qpackageVersion, platform = q.platform, padding = ' ', sign='|', append=False):
        """
        Print Dependencies for a QPackage in a tree format
        @param qpackageDomain: domain of the qpackage
        @param qpackageName: name of the QPackage
        @param qpackageVersion: version of the QPackage
        @param platform: platform type to show dependencies for
        @param padding: padding string
        @param sign: sign to distinguish the last element
        @param append: if True will append a *, for QPackage already in the tree
        """
        #qpackageObject = QPackageObject(qpackageDomain, qpackageName, qpackageVersion)
        q.console.echo( padding[:-1]  + '%s--'%sign+ '(%s %s)'%(qpackageName,qpackageVersion)+ ('*' if append else ' '))
        padding = padding + '  '
        deps = []
        deps = self.listDependency(qpackageDomain, qpackageName, qpackageVersion, platform)
        if append:
            return
        count = 0
        for dep in deps:
            count += 1
            if  str(dep) in self._depList:
                append=True

            self._depList.append(str(dep))
            if count == len(deps):
                self._exportDependencyTree(dep.domain, dep.name, dep.version, platform=platform, padding=padding + ' ', sign='`', append=append)
            else:
                self._exportDependencyTree(dep.domain, dep.name, dep.version, platform=platform, padding=padding + '|', append=append)


    def getFullDependency(self, domain, name, version):
        self._fullList = list()
        self._getFullDependency(domain, name, version)
        return self._fullList

    def _getFullDependency(self, domain, name, version):
        self._fullList.append((domain, name, version))
        deps = self.listDependency(domain, name, version) or list()
        depList = list()
        depList =[(domain, name, version)]
        depList.extend([(str(qp.domain), qp.name, qp.version) for qp in deps])
        if set(depList).issubset(set(self._fullList)):
            return
        for index, dep in enumerate(deps):
            self._getFullDependency(dep.domain, dep.name, dep.version)

    def _checkSupportedPlatform(self, qpackageObject, supportedPlatform):
        """
        Check if a QPackage is supported on platform(s) specified
        """
        if supportedPlatform in qpackageObject.supportedPlatforms:
            return True
        for platform in qpackageObject.supportedPlatforms:
            if q.platform.getByName(str(platform).strip()).has_parent(str(supportedPlatform)) or q.platform.getByName(str(supportedPlatform)).has_parent(str(platform).strip()):
                return True

        return False

    def _checkSupportedPlatforms(self, qpackageObject, supportedPlatforms):
        if not isinstance( supportedPlatforms, list):
            supportedPlatforms = str(supportedPlatforms).split(',')
        supported = True
        for supportedPlatform in supportedPlatforms:
            if not self._checkSupportedPlatform(qpackageObject, supportedPlatform):
                q.logger.log('Platform %s is not supported for QPackage %s'%(supportedPlatform, qpackageObject.qpackageName),6)
                supported = False

        return supported

    def _checkIfQPackageInList(self, dep, flatDep):
        """
        Check if QPackage is already in the list of Dependencies
        """
        qpackageExists = False
        for qpackage in flatDep:
            if qpackage.name == dep.name:
                qpackageExists = True
                break
        return qpackageExists