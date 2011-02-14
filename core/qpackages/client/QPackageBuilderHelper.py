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

class QPackageBuilderHelper(BaseType):
    """
    Builder class which contains helper methods to build the content of a qpackage.
    This helper method is passed on as a parameter to the qpackage's build script.
    """
    qpackageName = q.basetype.string(doc='Name of the qpackage')
    qpackageDomain = q.basetype.string(doc = 'Domain of the qpackage')
    qpackageVersion = q.basetype.string(doc='Version of the qpackage')
    qpackageQualityLevel = q.basetype.string(doc='Quality level of the qpackage', allow_none=True)
    _packages = q.basetype.list(doc='List of packages to checkout or export', default=list())
    
    def __init__(self, qpackageName, qpackageDomain, qpackageVersion, qpackageQualityLevel=None):
        self.qpackageName = qpackageName
        self.qpackageDomain = qpackageDomain
        self.qpackageVersion = qpackageVersion
        self.qpackageQualityLevel = qpackageQualityLevel

    def buildFromSvn(self, svnUri, svnPackage, destinationDir='files', exportTo='', userName = None, password=None, platform='generic'):
        """
        Build qpackage from svn. Files will be exported to the upload folder of the qpackage in packageDir 
        e.g. buildFromSvn('http://svn.pymonkey.org/svn/code/trunk/', '/utils', exportTo='utils')
        will export http://svn.pymonkey.org/svn/code/trunk/utils/ to upload_<qualityLevel>/files/generic/utils/

        buildFromSvn('http://svn.pymonkey.org/svn/code/trunk/','/test', 'unitTests', q.system.fs.joinPaths('share', 'tests'))
        will export http://svn.pymonkey.org/svn/code/trunk/test/ to upload_<qualityLevel>/unitTests/generic/share/tests/

        @param svnUri: uri of svn e.g. http://svn.pymonkey.org/svn/code
        @param svnPackage: name of the package to export. e.g. /trunk/pymonkey
        @param destinationDir: name of the folder to export files to. if none specified, will be set to files
        @param exportTo: dir path to export to. e.g q.system.fs.joinPaths('lib', 'pymonkey', 'core')
        @param userName: login for svn. if repository requires authentication
        @param password: password of the user..if repository requires authentication
        @param platform: platform to build QPackage for. 
        """
        destination = q.system.fs.joinPaths(q.dirs.packageDir, self.qpackageDomain, self.qpackageName, self.qpackageVersion, 'upload_%s'%self.qpackageQualityLevel, destinationDir, str(platform), exportTo)
        self.exportFromSvn(svnUri, svnPackage, destination, userName, password)

    def exportFromSvn(self, svnUri, svnPackage, destinationDir, userName=None, password=None):
        """
        Export files from svn
        @param svnUri: uri of svn e.g. http://svn.pymonkey.org/svn/code
        @param svnPackage: name of the package to export. e.g. /trunk/pymonkey
        @param destinationDir: name of the folder to export files to
        @param userName: login for svn. if repository requires authentication
        @param password: password of the user..if repository requires authentication
        """
        self._packages.append(svnPackage)
        connection = q.clients.svn.createConnection(svnUri,username=userName, password=password, storeCredentials=False)
        cleanup = True
        if len(self._packages) > 1:
            cleanup = False
        connection.export(svnPackage, destinationDir, force = cleanup)

    def checkOutFromSvn(self, svnUri, svnPackage, destinationDir, userName=None, password=None):
        """
        Checkout files from svn
        @param svnUri: uri of svn e.g. http://svn.pymonkey.org/svn/code
        @param svnPackage: name of the package to export. e.g. /trunk/pymonkey
        @param destinationDir: name of the folder to checkout files to
        @param userName: login for svn. if repository requires authentication
        @param password: password of the user..if repository requires authentication
        """
        self._packages.append(svnPackage)
        connection = q.clients.svn.createConnection(svnUri, username=userName, password=password, storeCredentials=False)
        connection.checkout(svnPackage, destinationDir)