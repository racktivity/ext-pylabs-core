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
from pymonkey import q
class SvnConnection:
     
    #@todo refactor to have login, passwd, uri, name as visible properties  
    #@todo add name as first argument
    
    #@todo if store credendials make sure connectioninfo in ini file is set properly
    def __init__(self, serverURI, branch, svnlogin=None, svnpasswd=None):
        '''
        
        @param serverURI: Full Subversion server URI
        @type serverURI: string
        '''
        self._svnURI = serverURI + "/" + branch + "/"
        self._svnlogin=svnlogin
        self._svnpasswd=svnpasswd
#        self._svnStoreCredentials = storeCredentials
        self.check()

        #@todo put in different connect method
        self._svnclient=pysvn.Client()
        self._svnclient.exception_style = 0
        self._svnclient.set_auth_cache(True)
        #self._svnclient.set_store_passwords(self._svnStoreCredentials)
        self._svnclient.set_default_username(self._svnlogin)
        self._svnclient.set_default_password(self._svnpasswd)
        self._svnclient.callback_get_login = self.getCredentials
        self._svnclient.callback_get_log_message = self.getEmptyLogMessageCallBack

        self.checkConnection()

    def check(self):
        """
        """
        #@todo add logic to check if connection already exists in the svnconnections ini file, if not ask the data through i.svn.connect...
        #e.g. if not login passwd, will be asked for, should be able to press enter if not login passwd (destinction between None & "")

    def getCredentials(self, realm, username, may_save ):
        retCode = not ( self._svnlogin == None or self._svnpasswd == None )
        return retCode, self._svnlogin, self._svnpasswd, True

    def getEmptyLogMessageCallBack(self):
        return True, ""


    def checkConnection(self):
        #do a list on svn server to see if svn connection works
        pymonkey.q.logger.log("Check SVN connection")         
        try:
            self._svnclient.list(self._svnURI)
        except:
            raise RuntimeError("Could not connect to svn server with url %s" % self._svnURI)

    def checkout(self,path,destination,revisionNumber=None):
        """
        @param path: is part of svn after basepath
        @param destinatio: is location where checkout will happen
        """
        return self.doAction(path,destination,"checkout",revisionNumber=revisionNumber)


    def import_(self,source,svnpath,message=""):
        """
        @param source: is location where content comes from
        @param svnpath: is part of svn after basepath
        """
        if not self.svnPathExists(svnpath):
            svnpath=self._svnURI+"/"+svnpath
            pymonkey.q.logger.log("Svn import path %s to dest %s with message \n %s " % (svnpath,source,message)) 
            self._svnclient.import_(source,svnpath,message)
            return True
        else:
            pymonkey.q.logger.log("Svn location does exist. Skipping import.") 
            return False
            
        ##return self.doAction(svnpath,source,"import")

    def getFileContent(self,path):
        #tmpdir=pymonkey.q.dirs.getTmpDir()
        #file=path.replace("/","_")
        #file=file.replace("\\","_")
        #file=tmpdir+os.sep+file+".tmp"
        #self.checkout(path)
        url=self._svnURI+path
        pymonkey.q.logger.log("SVN CAT: %s "% (url))
        result= self._svnclient.cat(url)
        return result

    def update(self,path,destination,revisionNumber=None):
        """
        @param path: is part of svn after basepath
        @param destination: is location where update will happen
        """
        return self.doAction(path,destination,"update",revisionNumber=revisionNumber)

    def cleanup(self,path):
        """
        cleanup svn dir
        @param path: path
        """
        return self._svnclient.cleanup(path)

    def export(self,path,destination,revisionNumber=None, force=False):
        """
        @param path: is part of svn after basepath
        @param destination: is location where export will happen
        @param revisionNumber: number of revision to export, if None use HEAD
        @param force: If True overwrite destination, else remove destination first
        """
        return self.doAction(path,destination.replace('/',os.sep),"export",revisionNumber=revisionNumber,force=force)

    def checkin(self,path,log_message,recurse=True):
        """
        Checkin
        """
        return self._svnclient.checkin(path,log_message,recurse=recurse)

    def remove(self,path,force=False):
        """
        remove path
        @param path: path to remove
        @param force: also delete unversioned items
        """
        svnpath=self._svnURI+"/"+path
        return self._svnclient.remove(svnpath,force)

    def copy (self,source,destination,revision=None ):
        """
        copy path
        @param source: source path/url
        @param destination: destination path/url
        @param revision
        """

        def get_log_message():
            return True, "Copy from %s to %s" % (source,destination)
        self._svnclient.callback_get_log_message = get_log_message

        if revision == None:
            revision = pysvn.Revision(pysvn.opt_revision_kind.head)
        source  ='%s/%s' %(self._svnURI,source)
        destination = '%s/%s' %(self._svnURI,destination)
        return self._svnclient.copy(source,destination,revision)

    def isAdmDir(self,basename):
        """
        returns true is basename is svn admin dir
        """
        return self._svnclient.is_adm_dir(basename)

    def svnPathExists(self,path):
        """
        returns true if path exists on server
        @param path: is part of svn after basepath
        """
        p='%s/%s' % (self._svnURI,path)
        pymonkey.q.logger.log("check path %s on svn exists" %  p)
        try:
            self._svnclient.list(p)
            return True
        except:
            return False

    def add(self,svnDir,recurse=True):
        """
        Add path to svn if not yet under version control
        @param path: path to add to svn
        @param recurse: add subdirs recursively
        """

        def addItemToSvn(path):
            if path == None:
                return
            if path in alreadyInSvn:
                if pymonkey.q.system.fs.isDir(path):
                    #check sub items
                    items = os.listdir(path)
                    for item in items:
                        if not self.isAdmDir(item):
                            addItemToSvn(os.sep.join([path,item]))
            else:
                ## IF is_adm_dir
                if not self.isAdmDir(os.path.basename(path)):
                    try:
                        return self._svnclient.add(path,recurse=recurse)
                    except:
                        raise RuntimeError("Could not add path %s to svn" % path)
        alreadyInSvn = []
        try:
            svnInfo2 = self._svnclient.info2(svnDir)
        except:
            svnInfo2 = []
        ignoreStart=str(time.time())
        for svnInfo in svnInfo2:
            path = svnInfo[0]
            info = svnInfo[1]

            if info['kind'] == 'dir' and path.endswith('.svn'):
                ignoreStart = path

            if not path.startswith(ignoreStart):
                alreadyInSvn.append( path )
        alreadyInSvn.sort()
        addItemToSvn(svnDir)

    def doAction(self,path,destination,action,autoCheckoutOnFailure=True,revisionNumber=None,force=False):
        """
        @todo we should redo this code, too ugly
        """
        destination = destination.rstrip(os.path.sep)
        url=self._svnURI+path
        pymonkey.q.logger.log("SVNACTION:%s :%s to %s"% (action,url,destination))

        if pymonkey.q.system.fs.isDir(destination)==False:
            pymonkey.q.system.fs.createDir(destination)

        if revisionNumber == None:
            revisionObject = pysvn.Revision(pysvn.opt_revision_kind.head)
        else:
            revisionObject = pysvn.Revision(pysvn.opt_revision_kind.number, revisionNumber)

        try:
            if action =="checkout" or (action=='export' and not force):
                pymonkey.q.system.fs.removeDirTree(destination)
            if action=="import":
                #destination here is source 
                print self._svnclient.import_(destination,url ,"")
                return 0
            if action=="checkout":
                self._svnclient.checkout(url, destination, revision = revisionObject)
                # checkout doesn't return a revision number, so update the checked out vapp to get the release number.
            if action=="update" or action=="checkout":
                r = self._svnclient.update(destination, revision = revisionObject)
                resultingRevisionNumber = r[0].number
                if resultingRevisionNumber < 0:
                    raise RuntimeError("Could not update '%s'. Result number was '%s'. Maybe the '.svn' directory is not present at the target?" % (destination, resultingRevisionNumber))
            if action=="export":
                r = self._svnclient.export(url, destination, revision = revisionObject, force=force)
                resultingRevisionNumber = r.number
                if r < 0:
                    raise RuntimeError("Could not export '%s'. Result number was '%s'." % (destination, r))
            return resultingRevisionNumber
        except:
            if autoCheckoutOnFailure and action=="update":
                return self.doAction(path,destination, "checkout", revisionNumber = revisionNumber)                
            else:
                raise RuntimeError("") #@todo

    def getLastChangedRevision(self,path="."): 
        """
        Returns the number of the youngest revision in the repository
        """ 
        retVal = -1
        try:             
            info = self.info(path,recurse=False)
            if len(info) == 1:
                retVal = info[0][1]['last_changed_rev'].number
        except:             
            retVal = -1 
        return retVal 
    
    def status(self,path='.',recurse=True):
        '''
        Returns current svn status of directory in a string representation 
        '''
        changes = self._svnclient.status(path,recurse=recurse)
        return '\n'.join(self._formatStatusOutput(changes))

    def diff(self,path='.'):
        '''
        Returns the diff in a string representation
        '''
        tmpDir=q.dirs.tmpDir
        return self._svnclient.diff(tmpDir,path)
    
    def info(self,path=".",revision=None,recurse=True):
        """
        @param path: path relative to url
        @param revision: revision: None => HEAD
        @param recurse: get recursive info
        """
        retVal = []
        fullURL = self._svnURI + path
        try:
            if revision == None:
                revision = pysvn.Revision(pysvn.opt_revision_kind.head )
            retVal = self._svnclient.info2(fullURL,revision,recurse=recurse)
        except:
            retVal = []
        return retVal

    def __cleanLogs(self,logs):
        """
        """
        
        def compare_svn(a, b):
            return cmp(b['revision'], a['revision'])

        def compare_paths(a,b):
            return cmp(a['path'],b['path'])
            
        retVal = []
        for log in logs:            
            thisLog = {}
            thisPaths = []
            thisLog['revision'] = log['revision'].number
            thisLog['date'] = log['date']
            thisLog['author'] = log['author']            
            thisLog['message'] = log['message']
            for path in log['changed_paths']:
                thisPath = {}
                thisPath['path'] = path['path']
                thisPath['action'] = path['action']
                
                thisPaths.append(thisPath)
            thisPaths.sort(compare_paths)
            thisLog['paths'] = thisPaths
            retVal.append(thisLog)
        retVal.sort(compare_svn)
        return retVal


    def log(self, path=".", fromRev = None, toRev = None, limit=0):
        """
        get svn messages
        @param path: relative url in this svn repo
        @param fromRev: source revision number (None: HEAD)
        @param toRev: target revision number (None: 0)
        @param limit: limit number of log entries (0 to get all)
        
        examples: 
            get last log for complete svn tree:
                log(limit=1)
            get 5 last logs: 
                log(limit=5)
            get first log starting from rev X for path Y:
                log(Y,X,limit=1)
            get all logs between rev X and Y (both inclusive) for path Z:
                log(Z,X,Y)
                
        Return boolean to indicate wheter any modifications have happened in this
        log returns a list of log entries; each log entry is a dictionary. The dictionary contains:
        * author - string - the name of the author who committed the revision
        * date - float time - the date of the commit
        * message - string - the text of the log message for the commit
        * revision - pysvn.Revision - the revision of the commit  
        * changed_paths - list of dictionaries. Each dictionary contains:        
            * path - string - the path in the repository
            * action - string
            * copyfrom_path - string - if copied, the original path, else None
            * copyfrom_revision - pysvn.Revision - if copied, the revision of the original, else None

        """
        retVal = []
        fullUrl = self._svnURI + path
        
        if fromRev == None:
            fromRevision = pysvn.Revision(pysvn.opt_revision_kind.head)
        else:
            fromRevision = pysvn.Revision(pysvn.opt_revision_kind.number, fromRev)
        
        if toRev == None:
            toRevision = pysvn.Revision(pysvn.opt_revision_kind.number,0 )
        else:
            toRevision = pysvn.Revision(pysvn.opt_revision_kind.number, toRev)
        
        logs = self._svnclient.log(fullUrl, fromRevision, toRevision, discover_changed_paths=False, strict_node_history=False, limit=limit)
        
        logs = self.__cleanLogs(logs)
        retVal.extend(logs)            
        
        return retVal
        

    def hasModifications(self, url, revisionNumber1, revisionNumber2=None):
        """
        @param url: relative url in this svn repo
        @revisionNumber1: source revision number
        @revisionNumber2: target revision number (omit to compare to HEAD)
        Return boolean to indicate wheter any modifications have happened in this
        svn subtree between the two revisions.

        Warning: This method can potentially be slow if large diffs are inspected
        """
        fullUrl = self._svnURI + url
        revision1 = pysvn.Revision(pysvn.opt_revision_kind.number, revisionNumber1)
        if revisionNumber2 == None:
            revision2 = pysvn.Revision(pysvn.opt_revision_kind.head)
        else:
            revision2 = pysvn.Revision(pysvn.opt_revision_kind.number, revisionNumber2)
        diff = self._svnclient.diff(pymonkey.q.dirs.getTmpDir(), fullUrl, revision1, fullUrl, revision2)

        return (diff != '')

    def isCommitted(self, repoPath):
        """
        Check for local checkout path if it has been committed. This
        does not check if the repository is up to date with the server,
        only if it contains modified files.


        @param repoPath: local path to checkout of repository
        @type repoPath: string
        @return: bool
        """
        unchanged_statuses = [
            pysvn.wc_status_kind.normal,
            pysvn.wc_status_kind.ignored,
            pysvn.wc_status_kind.unversioned,
            pysvn.wc_status_kind.none,
        ]
        files = self._svnclient.status(repoPath)
        for f in files:
            if not f.text_status in unchanged_statuses:
                return False
        return True

    def isUpToDate(self, repoPath, serverUri):
        """
        Check if the local checkout at repoPath is up to date with the
        code at the server. Returns True if no files are modified locally
        and the local revision is equal to the server revision.

        @param repoPath: local path to checkout of repository
        @type repoPath: string
        @param serverUri: URI of repository on server, including subpath to where the code from repoPath can be found
        @type serverUri: string
        @return: bool
        """
        if not self.isCommitted(repoPath):
            return False
        server_revision = self.getRevision(serverUri)
        local_revision = self.getRevision(repoPath)
        return local_revision.number == server_revision.number

    def getRevision(self, uri):
        """
        Returns the revision object for uri.

        @param uri: url or path to get the revision for
        @type uri: string
        @return: pysvn.Revision object for uri
        """
        return self._svnclient.info2(uri, recurse=False)[0][1]['last_changed_rev']

    def isReadyForCommit(self, repoPath):
        """
        Returns whether the checkout at repoPath is clean and can be committed.

        Can be used after an svn update to check if any files have conflicts etc.

        @param repoPath: path of the checkout
        @type repoPath: string
        @return: bool
        """
        good_statuses = [
            pysvn.wc_status_kind.added,
            pysvn.wc_status_kind.deleted,
            pysvn.wc_status_kind.modified,
            pysvn.wc_status_kind.ignored,
            pysvn.wc_status_kind.unversioned,
            pysvn.wc_status_kind.normal,
        ]

        files = self._svnclient.status(repoPath)
        for f in files:
            if not f.text_status in good_statuses:
                return False
        return True
    
    def _formatStatusOutput(self,changes):
        output=[]
        addedFiles=[f.path for f in changes if f.text_status == pysvn.wc_status_kind.added]
        removedFiles=[f.path for f in changes if f.text_status == pysvn.wc_status_kind.deleted]
        modifiedFiles=[f.path for f in changes if f.text_status == pysvn.wc_status_kind.modified]
        conflictedFiles=[f.path for f in changes if f.text_status == pysvn.wc_status_kind.conflicted]
        unversionedFiles=[f.path for f in changes if f.text_status == pysvn.wc_status_kind.unversioned]
        if addedFiles:            
            output.append('files to be added:')
            output.append('\n'.join(addedFiles))    
        if removedFiles:
            output.append('files to be removed:')
            output.append('\n'.join(removedFiles))        
        if modifiedFiles:
            output.append('files that have changed:')
            output.append('\n'.join(modifiedFiles))        
        if conflictedFiles:
            output.append('files with merge conflicts:')
            output.append('\n'.join(conflictedFiles))        
        if unversionedFiles:
            output.append('unversioned files:')
            output.append('\n'.join(unversionedFiles))
        return output