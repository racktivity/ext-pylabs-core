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

import sys
import time
import os
import os.path

import pysvn

import pymonkey

#@todo do not use for now

raise RuntimeError("SvnConnectionLocal NOT SUPPORTED, needs to be refactored")

class SvnConnectionLocal :

    _svnConnection = None
    _localDir = None
    _url = None

    def __init__ (self, serverURI, localDir=None, initialUpdate=False, svnlogin=None, svnpasswd=None ):
        self._svnConnection = SvnConnection(serverURI, svnlogin, svnpasswd)
        self._localDir = localDir
        self._url = serverURI
        if initialUpdate:
            self.update()

    def __path2PathDest__ (self,srcPath=None,dstPath=None):
        """
        translate path into svn path and local directory
        """
        if srcPath!=None and srcPath!='':
            if dstPath == None:
                destination = os.sep.join([self._localDir,srcPath])
            else:
                destination = os.sep.join([self._localDir,dstPath])
        else:
            srcPath = ''
            if dstPath == None:
                destination = self._localDir
            else:
                destination = os.sep.join([self._localDir,dstPath])
        return {'path':srcPath , 'local':destination}

    def __path2URLDest__ (self,srcPath=None,dstPath=None):
        """
        translate path into destination url  and local directory
        """
        if srcPath!=None and srcPath!='':
            if dstPath == None:
                destination = srcPath
            else:
                destination = dstPath
        else:
            srcPath = ''
            if dstPath == None:
                destination = ''
            else:
                destination = dstPath
        source = os.sep.join([self._localDir,srcPath])
        return {'local':source , 'dest':destination}

    def getSvnConnection(self):
        """Get Svn connection"""
        return self._svnConnection

    def getLocalDir(self):
        """
        get local directory
        """
        return self._localDir

    def setLocalDir(self,localDir=None):
        seld._localDir = localDir

    def update(self,path=None,revision=None):
        """
        update
        @param path: path
        @param revision: rev
        """
        pathDest = self.__path2PathDest__(path)
        self._svnConnection.update(pathDest['path'],pathDest['local'],revision)

    def cleanup(self,path=None):
        """
        cleanup
        @param path: path
        """
        pathDest = self.__path2PathDest__(path)
        self._svnConnection.cleanup(pathDest['local'])

    def checkout(self,srcPath=None,dstPath=None,revision=None):
        """
        checkout
        @param path: path
        @param revision: rev
        """
        pathDest = self.__path2PathDest__(srcPath,dstPath)
        self._svnConnection.checkout(pathDest['path'],pathDest['local'],revision)

    def log(self,path=None,srcRev=None,destRev=None):
        """
        log
        @param path: path
        @param srcRev: source revision
        @param destRev: destination revision
        @return logs
        """
        pathDest = self.__path2URLDest__(path)
        self._svnConnection.log(pathDest['dest'],srcRev,destRev)

    def import_(self,srcPath,dstPath=None, message=None):
        """
        """
        pathDest = self.__path2URLDest__(srcPath,dstPath)
        self._svnConnection.import_(pathDest['local'],pathDest['dest'],message)

    def checkin(self,path=None,message="",recurse=True):
        """
        checkin
        @param path: path
        @param message: message
        @param recuse: recursive
        """
        pathDest = self.__path2PathDest__(path)
        self._svnConnection.checkin(pathDest['local'],message,recurse)

    def add(self,path=None, recurse=True):
        """
        add
        @param path: path
        @param recurse: recursive
        """
        pathDest = self.__path2PathDest__(path)
        self._svnConnection.add(pathDest['local'],recurse)

    def copy (self, source=None, dest=None, revision=None):
        """
        copy
        @param source: source path
        @param des: destination path
        @revision: source revision
        """
        pathSource = self.__path2PathDest__(source)
        pathDest = self.__path2PathDest__(dest)

        if revision==None:
            revision = pysvn.Revision(pysvn.opt_revision_kind.working)
        else:
            revision = pysvn.Revision(pysvn.opt_revision_kind.number, revision)

        self._svnConnection.copy(pathSource['local'],pathDest['local'],revision)

    def remove ( self, path=None, force=False ):
        """
        remove
        @param path: path
        @param force: also delete unversioned items
        """
        pathDest = self.__path2PathDest__(path)
        self._svnConnection.remove(pathDest['local'],force)

    def __getattr__ (self, attr):
        """
        redirect all other calls to svnConnection
        """
        return getattr(self._svnConnection, attr)

    def svnPathExists(self,path):
        return self._svnConnection.svnPathExists(path)