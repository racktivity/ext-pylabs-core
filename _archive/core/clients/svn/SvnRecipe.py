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

'''Vapp build recipe implementation for vapps stored in Subversion'''
import os.path

try:
    import cPickle as pickle
except ImportError:
    import pickle

import pymonkey
from pymonkey import q
class SvnRecipeItem:
    '''Build info for an SvnBuildRecipe (used to create buildinfo.ini)'''
    
    def __init__(self, svnConnection, svnSourcePath, destinationPath, revision=None):
        svnConnection.check()
        self.svnConnection=svnConnection #check of real svnconnection
        self.svnSourcePath=svnSourcePath
        self.destinationPath=self.getLocalDestDir(destinationPath)
        self.revision=revision        

    def export(self):
        '''
        exports files to destination location without having the .svn folders
        '''
        if self.svnConnection.svnPathExists(self.svnSourcePath) :                
            self.svnConnection.export(self.svnSourcePath,self.destinationPath,self.revision)
        else:
            raise RuntimeError("Source %s doesn't exist on the server." % self.svnSourcePath)
        
    def checkout(self):
        """
        checkout files to destination location
        if there were already files checked out at that location ask if destination should be removed (interactive), if not interactive session will fail
        """    
        #check if svn path exists
        if self.svnConnection.svnPathExists(self.svnSourcePath) :                
            self.svnConnection.checkout(self.svnSourcePath,self.destinationPath,self.revision)
        else:
            raise RuntimeError("Source %s doesn't exist on the server."%self.svnSourcePath)

    def update(self):
        """
        try to update files on destination (in sandbox), if not there yet checkout
        """
        if q.system.fs.exists(self.destinationPath):
            self.svnConnection.update(self.svnSourcePath,self.destinationPath,self.revision)
            if not self.svnConnection.isReadyForCommit(self.destinationPath):
                raise RuntimeError("Conflict discoverd in file %s ."%self.destinationPath)
        else:
            self.svnConnection.checkout(self.svnSourcePath,self.destinationPath,self.revision)
            
    def remove(self):
        """
        remove files from destination
        """
        if q.system.fs.exists(self.destinationPath):
            #TODO Check Force with Carl
            self.svnConnection.remove(self.destinationPath,True)
        else:
            #files already not found 
            q.logger.log("Warning! The directory %s you want to remove doesn't exist !" % self.destinationPath)
            
    def checkin(self, logMsg):
        """
        checkin svn dir
        do update of dir first, if conflicts raise error
        commit changes back to svn
        """
        if q.system.fs.exists(self.destinationPath):
            self.update()            
            #Ask for log message
            self.svnConnection.checkin(self.destinationPath,logMsg)
        else:
            #raise some error
            raise RuntimeError("Can't find directory %s to checkin" % self.destinationPath)
        
    def status(self):
        '''
        Returns svn status of directory in a nice string representation
        '''
        return self.svnConnection.status(self.destinationPath)

    def diff(self):
        '''
        Returns the diff as string
        '''
        return self.svnConnection.diff(self.destinationPath)
    
    def getLocalDestDir(self, path):
        '''
        returns local absolute path in sandbox
        '''
        return q.system.fs.joinPaths(q.dirs.baseDir,path)

class SvnRecipe:
    """
    Build recipe for Subversion'''
    """

    def __init__(self):
        self._items = list()        

    def addSource(self, svnConnection, svnSourcePath, destinationPath, revision=None):
        #@todo remove platformtypes
        '''Add a source to the build recipe.

        When cooking this recipe, files from svnSourcePath in the Subversion
        server at svnServerURI will be checked out under destinationPath in the Sandbox.

        An optional SVN revision can be provided.        

        Example:
        There is an existing svnconnection called pymonkey which connects to http://svn.pymonkey.org
        files on serverhttp://svn.pymonkey.org in /trunk/myvapp/bin will
        go into q.dirs.baseDir/apps/myapp/ if this method is called with arguments
        'http://svn.mine.tld', '/trunk/myvapp/bin', '/apps/myapp/'.        

        @param svnConnection: connection to svnserver
        @param svnSourcePath: File source folder in the Subversion server (string)
        @param destinationPath: Destination path for files in svnSourcePath (string)
        @param revision: SVN revision to checkout, HEAD if not provided (int)        
        '''
        #@todo check if real svnconnection object (of right type)                 
        self._items.append(SvnRecipeItem(svnConnection, svnSourcePath, destinationPath, revision))

    def checkoutToSandbox(self):
        """
        checkout all svn recipe items
        if there were already files checked out at that location ask if destination should be removed (interactive), if not interactive session will fail        
        """
        for svnItem in self._items:
            if q.system.fs.exists(svnItem.destinationPath) and not q.system.fs.isEmptyDir(svnItem.destinationPath):
                if q.qshellconfig.interactive:
                    #interactive mode, ask if existing files should be removed
                    answer = q.gui.dialog.askYesNo("Warning! There appears to be files in the checkout location %s. Do you want to remove them before checkout ?"%svnItem.destinationPath)
                    if answer:
                        q.system.fs.removeDirTree(svnItem.destinationPath)
                    else:
                        raise RuntimeError('Checkout location is not empty')
                else:
                    #non interactive mode, throw an error for non empty dir
                    raise RuntimeError("Checkout location %s is not empty"%svnItem.destinationPath)
            svnItem.checkout()

    def exportToSandbox(self):
        """
        checkout all svn recipe items
        """
        for svnItem in self._items:
            if q.system.fs.exists(svnItem.destinationPath) and not q.system.fs.isEmptyDir(svnItem.destinationPath):
                if q.qshellconfig.interactive:
                    #interactive mode, ask if existing files should be removed
                    answer = q.gui.dialog.askYesNo("Warning! There appears to be files in the export location %s. Do you want to remove them before exporting ?"%svnItem.destinationPath)
                    if answer:
                        q.system.fs.removeDirTree(svnItem.destinationPath)
                    else:
                        raise RuntimeError('Export location is not empty')
                else:
                    #non interactive mode, throw an error for non empty dir
                    raise RuntimeError("Export location %s is not empty"%svnItem.destinationPath)
            svnItem.export()
    def updateInSandbox(self):
        """
        walks over all checked out dirs and does update (when conflict raise error)
        """
        for svnItem in self._items:
            svnItem.update()
        
    def checkinFromSandbox(self):
        """
        will walk over all relevant checked out dirs and try to commit (first an update and check on conflicts)
        add files automatically (only relevant types of files)
        """
        logMsg = q.gui.dialog.askMultiline('Enter svn commit message')
        for svnItem in self._items:
            svnItem.checkin(logMsg)
        
    def removeFromSandbox(self):
        """
        will remove all destinations in sandbox where svn recipe checkouts to
        """
        for svnItem in self._items:
            q.system.fs.removeDirTree(svnItem.destinationPath)
    # prio 2    
    def getChangeLogFromSandBox(self, fromDate):
        """
        walk over checked out dirs and create log of changes (deletes, new, updates, ...)
        """
    
    # prio 2    
    def filesFindDeletedInSandBox(self):
        """
        walk over checked out dirs and check which files are deleted in relation to repo
        returns array with filepaths
        """
    
    # prio 2    
    def filesFindNewInSandBox(self):
        """
        walk over checked out dirs and check which files are new in relation to repo
        returns array with filepaths
        """

    # prio 2
    def filesFindChangedInSandBox(self):
        """
        walk over checked out dirs and check which files are new in relation to repo
        returns array with filepaths
        """

    # prio 2
    def filesChangedInSandBox(self):
        """
        walk over checked out dirs and check if changes, if anywhere a change -> True otherwise False
        """        
    
    # prio 2            
    def filesRemoveSvnTagsInSandBox(self):
        """
        """
        
    def filesStatInSandBox(self):
        """
        """
        for svnItem in self._items:
            print svnItem.status()
            
    def filesDiffInSandBox(self):
        """
        """
        for svnItem in self._items:
            print svnItem.diff()
            
    def isDestinationClean(self):
        '''
        Returns True if destination directories are empty, otherwise it returns False
        '''
        for svnItem in self._items:
            if q.system.fs.exists(svnItem.destinationPath) and not q.system.fs.isEmptyDir(svnItem.destinationPath):
                return False
        return True


    def executeTaskletAction(self, actionname):
        '''
        Execute the required actions for all recipe items
        '''
        # A mapping dictionary
        mapping={
            'checkin' : self.checkinFromSandbox,
            'checkout': self.checkoutToSandbox,
            'update': self.updateInSandbox,
            'remove': self.removeFromSandbox,
            'stat': self.filesStatInSandBox,
            'diff': self.filesDiffInSandBox,
            'export': self.exportToSandbox        
        }
        #Execute the desird function
        mapping[actionname]()