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
from pylabs.qpackages.client.QPackage import QPackage
from pylabs.qpackages.interactive.QPackageServerConnectionsGUI import QPackageServerConnectionsGUI
from pylabs.qpackages.common.QPackageVersioning import QPackageVersioning
import string

class QPackageManagementGUI(object):

    def find(self, qpackageName='', version='', domain='', state='', retQPackages=False):
        """
        Find one or more QPackage
        Searches for an exact match of qpackageName (if specified) unless wildcard * is added at the end of the qpackageName.
        e.g i.qpackages.find('pymon*') and i.qpackages.find('pylabs')
        @param qpackageName: name of the QPackage to search for
        @param version: version of the QPackage you are searching for
        @param domain: domain you wish to search
        @param state: state of the qpackage to search for (SERVER,LOCAL,NEW,MOD)
        @param retQPackages: if set to True qpackages found will be returned
        """
        if not qpackageName:
            qpackageName = q.console.askString("Please provide the name (or part of the name followed by an asterisk (*)) of the QPackage to search for")

        if str(qpackageName).endswith('*'):
            exactMatch = False
        else:
            exactMatch = True
        qpackageName = str(qpackageName).replace('*', '')

        qpackageListFound = q.qpackages.qpackageFind(qpackageName, version=version, domain=domain, qualityLevels=q.qpackages.getDefaultQualityLevel(), state=state, exactMatch=exactMatch)
        if not qpackageListFound:
            return None

        qpackagesChosen = q.console.askChoiceMultiple(qpackageListFound)
        if not qpackagesChosen:
            return

        if retQPackages:
            return qpackagesChosen

        setattr(self, 'lastQPackage', qpackagesChosen[-1])
        for qpackage in qpackagesChosen:
            if not hasattr(self, 'lastQPackages'):
                setattr(self, 'lastQPackages', LastQPackages())

            self.lastQPackages.pm_add(qpackage)

    def findFirst(self, qpackageName="", version='', domain='', state=""):
        """
        Search for a QPackage and return the first one found
        @param qpackageName: name of the QPackage to search for
        @param version: version of the QPackage you are searching for
        @param domain: domain you wish to search
        @param state: state of the qpackage to search for (SERVER,LOCAL,NEW,MOD)
        """
        if not qpackageName:
            qpackageName = q.console.askString("Please provide part of the QPackage name to search for")
        if str(qpackageName).endswith('*'):
            exactMatch = False
        else:
            exactMatch = True
        qpackageName = str(qpackageName).replace('*', '')
        qpackageFound = q.qpackages.qpackageFindFirst(qpackageName, version=version, domain=domain, qualityLevels=q.qpackages.getDefaultQualityLevel(), state=state, exactMatch=exactMatch)

        if not qpackageFound:
            return
        if not hasattr(self, 'lastQPackages'):
            setattr(self, 'lastQPackages', LastQPackages())
        self.lastQPackages.pm_add(qpackageFound)
        setattr(self, 'lastQPackage', qpackageFound)
        return qpackageFound

    def findInDevelopmentMode(self, qpackageName='', qpackageVersion = '', qpackageDomain = ''):
        """
        Search for a QPackage in development mode
        @param qpackageName: name of the QPackage to search for
        @param qpackageVersion: version of the QPackage you are searching for
        @param qpackageDomain: domain you wish to search
        """
        if not qpackageName:
            qpackageName = q.console.askString("Please provide part of the QPackage name to search for")

        if not qpackageVersion:
            qpackageVersion = q.console.askString("Please provide version of the QPackage")

        if not qpackageDomain:
            qpackageDomain = q.console.askString("Please provide domain of the QPackage")

        qpackageListFound = q.qpackages.qpackageFindInDevelopmentMode(qpackageName, qpackageVersion, qpackageDomain)

        if not qpackageListFound:
            return None

        qpackagesChosen = q.console.askChoiceMultiple(qpackageListFound)
        if not qpackagesChosen:
            return

        setattr(self, 'lastQPackage', qpackagesChosen[-1])
        for qpackage in qpackagesChosen:
            if not hasattr(self, 'lastQPackages'):
                setattr(self, 'lastQPackages', LastQPackages())

            self.lastQPackages.pm_add(qpackage)

    def create(self, qpackageName=None, qpackageVersion=None, qpackageDomain=None, qpackageQualityLevel=None, supportedPlatforms=None):
        """
        Create a QPackage
        @param qpackageDomain: domain where you wish to create the QPackage
        @param qpackageName: name of the QPackage
        @param qpackageVersion: version of the QPackage
        @param qpackageQualityLevel: quality level of the QPackage
        """
        if not qpackageDomain:
            q.console.echo('Please select a domain to create QPackage on')
            qpackageDomain = q.console.askChoice(self.listAllDomains())

        while not qpackageName or not self._checkQPackageName(qpackageName):
            qpackageName = q.console.askString('Name of the new QPackage (only lowercase, digits and _)')

        if not qpackageVersion:
            qpackageVersion = q.console.askString('Version of the new QPackage', defaultparam='1.0')

        while not qpackageQualityLevel:
            qpackageQualityLevel = q.gui.dialog.askChoice('Please choose a quality level',['trunk', 'test', 'unstable', 'beta', 'stable'], defaultValue=q.qpackages.getDefaultQualityLevel() or 'trunk')

        qpackage = q.qpackages.qpackageCreate(qpackageName, qpackageVersion, qpackageDomain, qpackageQualityLevel)

        qpackage.setSupportedPlatforms(supportedPlatforms)
        if not hasattr(self, 'lastQPackages'):
            setattr(self, 'lastQPackages', LastQPackages())

        self.lastQPackages.pm_add(qpackage)
        setattr(self, 'lastQPackage',qpackage)

        return qpackage

    def setQualityLevel(self, defaultQualityLevel=""):
        """
        Set the default qualityLevel
        @param defaultQualityLevel: default quality level to set
        """
        if not defaultQualityLevel:
            defaultQualityLevel = q.gui.dialog.askChoice('Please choose a quality level',['trunk', 'test', 'unstable', 'beta', 'stable'], defaultValue=q.qpackages.getDefaultQualityLevel() if q.qpackages.getDefaultQualityLevel() else 'trunk')
        q.qpackages.setQualityLevel(defaultQualityLevel)

    def updateAllQPackages(self):
        """
        Updates all installed QPackages
        """
        self.updateQPackageList()
        q.qpackages.updateAllQPackages()

    def updateQPackageList(self):
        """
        Get and Load latest vlists
        """
        q.qpackages.updateQPackageList()

    def _checkQPackageName(self, qpackageName):
        """
        Check if QPackage name doesnt contain invalid characters
        @param qpackageName: name of the QPackage to check
        """
        VALID_NAME_CHARACTERS = set('%s%s_' % (string.ascii_lowercase, string.digits))
        if qpackageName[0].isdigit():
            q.console.echo('QPackage name cannot start with a digit')
            return False
        for character in qpackageName:
            if not character in VALID_NAME_CHARACTERS:
                q.console.echo('Character <%s> is not allowed'%character)
                return False
        return True

    def listAllDomains(self):
        """
        Returns a list of all domains configured for all connections
        """
        return q.qpackages.listAllDomains()

class LastQPackages(object):
    pm_lastqpackages = list()

    def pm_add(self, qpackage):
        self.pm_lastqpackages.append(qpackage)
        setattr(self, qpackage.name, qpackage)
        
    def __iter__(self):
        return self.pm_lastqpackages.__iter__()

    def __len__(self):
        return self.pm_lastqpackages.__len__()

    def __contains__(self, v):
        if isinstance(v, QPackage):
            return (v.name, v.version, v.domain) in [(p.name, p.version, p.domain) for p in self.pm_lastqpackages]
        else:
            return v in self.pm_lastqpackages

    def __getitem__(self, v):
        return self.pm_lastqpackages.__getitem__(v)

    def __str__(self):
        return self.pm_lastqpackages.__str__()
    def __repr__(self):
        return self.pm_lastqpackages.__repr__()