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

from pymonkey.config import * 
from pymonkey import q 
import re 

def cleanList(packagesString):
    if packagesString.strip() == "*NONE*":
        return []
    entries = map(lambda x:x.strip(), packagesString.split(','))
    result = []
    for entry in entries:
        match = re.match('^\\(\\s*([a-zA-Z0-9._\\-]+)\\s*\\|\\s*([a-zA-Z0-9_]+)\\s*\\|\\s*(([0-9]+\\.)*[0-9]+)\\s*\\)$', entry)
        if (not match):
            raise RuntimeError('Invalid format for packages in development mode.')
        result.append((match.groups()[0], match.groups()[1], match.groups()[2]))
    return result

def makePackageString(cleanlist):
    if len(cleanlist) == 0:
        return "*NONE*"
    result = ""
    for (domain, name, version) in cleanlist:
        result = result + "(%s | %s | %s), " % (domain, name, version)
    result = result[:-2]
    try:
        # see if it is parsable
        testcleanlist = cleanList(result)
    except:
        raise RuntimeError("Invalid format for package list")
    return result


class QPackageLocalConfigItem(ConfigManagementItem):
    CONFIGTYPE = 'qpackage_settings'
    DESCRIPTION = 'QPackage Local Configuration'

    def ask(self):
        packages = self.dialogAskString('qpackages_in_development_mode', 'Enter comma separated list of QPackages to be put in delopment mode.\nEnter *NONE* for no packages.\nFor example: (openvapps.org | pymonkey | 2.0),  (test.com | mypackage | 2.1)\nEnter List')
        result = cleanList(packages)
        if result == []:
            self.params['qpackages_in_development_mode'] = '*NONE*'

    def show(self):
        """
        Optional customization of show() method
        """
        allPackages = cleanList(self.params['qpackages_in_development_mode'])
        if len(allPackages) == 0:
            result = "\nThere are no packages in development mode.\n"
        else:
            result = '\nThe following packages are in development mode:'
            for package in allPackages:
                result = (result + ('\n\n Package:\n   Domain:  %s\n   Name:    %s\n   Version: %s' % (package[0], package[1], package[2])))

        q.gui.dialog.message(result)

QPackageLocalConfig = ItemSingleClass(QPackageLocalConfigItem)

def listQPackagesInDevMode(self):
    myItem = self._ITEMCLASS(self._CONFIGTYPE, 'main', load=True)
    return cleanList(myItem.params['qpackages_in_development_mode'])

QPackageLocalConfig.listQPackagesInDevMode = listQPackagesInDevMode

def isQPackageInDevMode(self, domain, name, version):
    return (domain, name, version) in self.listQPackagesInDevMode()

QPackageLocalConfig.isQPackageInDevMode = isQPackageInDevMode

def _setQPackageDevMode(self, packageInfo, enable):
    domain = packageInfo[0]
    name = packageInfo[1]
    version = packageInfo[2]
    myList = self.listQPackagesInDevMode()
    dirty = False
    if enable:
        if (domain, name, version) not in myList:
            myList.append(packageInfo)
            dirty = True
    if not enable:
        if (domain, name, version) in myList:
            myList.remove(packageInfo)
            dirty = True
    if dirty:
        packageString = makePackageString(myList)
        self.configure({'qpackages_in_development_mode':packageString})

QPackageLocalConfig._setQPackageDevMode = _setQPackageDevMode

def enableQPackageDevMode(self, domain, packagename, version):
    self._setQPackageDevMode((domain, packagename, version), True)

QPackageLocalConfig.enableQPackageDevMode = enableQPackageDevMode

def disableQPackageDevMode(self, domain, packagename, version):
    self._setQPackageDevMode((domain, packagename, version), False)

QPackageLocalConfig.disableQPackageDevMode = disableQPackageDevMode

def disableAllQpackagesDevMode(self):
    self.configure({'qpackages_in_development_mode':'*NONE*'})

QPackageLocalConfig.disableAllQpackagesDevMode = disableAllQpackagesDevMode

if QPackageLocalConfigItem.CONFIGTYPE not in q.config.list():
    ini = q.config.getInifile(QPackageLocalConfigItem.CONFIGTYPE)
    ini.addSection('main')
    ini.addParam('main', 'qpackages_in_development_mode', '*NONE*')