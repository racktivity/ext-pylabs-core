from pylabs import q
from pylabs.Shell import *
import fnmatch
from infomodel.infomodel import *
from infomodel.ObjectStore import ObjectStoreManager 
from infomodel.iterators import  DirNodeStoreCompositeIterator
from functools import partial
from collections import defaultdict

def __mod__(self, other):
  if isinstance(self, DirNode):
      return False
  if isinstance(self, FileNode) and isinstance(other, self.__class__):
      return self.md5hash != other.md5hash
  return False

class VFSMetadata():
    """
    a userfriendly layer on top of DirObjectsStore
    allows manipulation of virtual filesystem e.g. walk over it, compare 2 versions of a filesystem, ...
    """
    
    def __init__(self, metadataPath, rootpath=""):
        self.metadataPath = metadataPath
        self.root = rootpath #path of root in which we will scan, when empty get from vfs metadata
        self.dirObjectStoreManager = ObjectStoreManager(metadataPath, self.root)
        if not self.root:
            self.root = self.dirObjectStoreManager.root
        q.system.fs.changeDir(self.root)
        self.state = "INIT"

    def _checkActive(self):
        if self.state != "OK":
            raise RuntimeError("Cannot continue, please populate vfs from filesystem of get latest version or another version, use functions get... or populate...")
        if not self.dirObjectStore.stateIsActive():
            raise RuntimeError("VFS is in wrong state, state=%s" % self.dirObjectStore.stateGet())

    def populateFromFilesystem(self, processHiddenFiles=False, usemd5=False):
        """
        scan filesystem and populate the VFS will create a new version of the metadata (each scan results in a new version)
        """
        self.state="SCAN"
        self.dirObjectStore = self.dirObjectStoreManager.new(processHiddenFiles, usemd5)  #the walk happens here
        self.walk=self.dirObjectStore.walk
        self.state="OK"
        
    def getLatest(self):
        self.dirObjectStore = self.dirObjectStoreManager.get()
        self.walk=self.dirObjectStore.walk
        self.state="OK"
        
    def getFromVersionEpoch(self,versionEpoch):
        self.dirObjectStore = self.dirObjectStoreManager.get(versionEpoch=versionEpoch)
        self.walk = self.dirObjectStore.walk
        self.state = "OK"

    def listFilesInDir(self, path, recursive=False, fileNameOnly=True, filter=None):
        """Retrieves list of files found in the specified directory
        @param path:       directory path to search in
        @type  path:       string
        @param recursive:  recursively look in all subdirs
        @type  recursive:  boolean
        @param filter:     unix-style wildcard (e.g. *.py) - this is not a regular expression
        @type  filter:     string
        @rtype: list
        """
        self._checkActive()
        def _process(args, path, ttype, moddate=0, size=0, md5hash=""):
            fileNameOnly, filter, pathsreturn = args            
            if ttype == "F":
                if (filter is None) or fnmatch.fnmatch(path, filter):
                    #fullpath=q.system.fs.joinPaths(path, fileNameOnly)
                    if fileNameOnly:
                        pathsreturn.append(q.system.fs.getBaseName(path))
                    else:
                        pathsreturn.append(path)
        pathsreturn=[]
        self.walk(_process, (fileNameOnly, filter, pathsreturn) , path, recursive=recursive)                
        return pathsreturn

    def listDirsInDir(self, path, recursive=False, dirNameOnly=True, filter=None):
        """Retrieves list of files found in the specified directory
        @param path:       directory path to search in
        @type  path:       string
        @param recursive:  recursively look in all subdirs
        @type  recursive:  boolean
        @param filter:     unix-style wildcard (e.g. *.py) - this is not a regular expression
        @type  filter:     string
        @rtype: list
        """
        self._checkActive()
        def _process(args,path,ttype,moddate=0,size=0,md5hash=""):
            dirNameOnly,filter,pathsreturn=args
            if ttype=="D":
                if (filter is None) or fnmatch.fnmatch(path, filter):
                    if dirNameOnly:
                        pathsreturn.append(q.system.fs.getDirName(path+"/",True))
                    else:
                        pathsreturn.append(path)
        pathsreturn=[]
        self.walk(_process, [dirNameOnly,filter,pathsreturn], path, recursive=recursive)                
        return pathsreturn

    def listVersions(self):
        return self.dirObjectStoreManager.list()

    def listVersionsHR(self):
        """
        human readable list
        """
        return self.dirObjectStoreManager.listHR()
    
    def __iter__(self):
        return DirNodeStoreCompositeIterator(self.dirObjectStore, '')
    
    def compareWithOlderVersion(self, versionEpoch):
        vfsOlder = VFSMetadata(self.metadataPath)
        vfsOlder.getFromVersionEpoch(versionEpoch=versionEpoch)
        self._checkActive()
        vfsOlder._checkActive()
        itr = iter(self)
        older_itr = iter(vfsOlder)
        #unfortunately we have to expand the iterators into lists to use difflib
        content = [entry for entry in itr]
        older_content = [entry for entry in older_itr]
        seq_matcher = q.tools.diff.getSequenceMatcher(seq1=content, seq2=older_content, comparator=__mod__)
        return seq_matcher
    
    def diffWithOlderVersion(self, versionEpoch, groupSimilarOperations=False, ignoreEquals=True):
        '''
        if groupSimilarOperations is False, returns a list of strings representing Transaction Log of changes between the two VFS versions
        else a dictionary of <action> : <list of files/dirs> based on the value of 
        '''
        seq_matcher = self.compareWithOlderVersion(versionEpoch)
        return q.tools.diff.diffSequences(seq_matcher, groupSimilarOperations, ignoreEquals)
     
                
    def compareCurrentWithFS(self):
            dirObject=self._checkFileStatus(dirObject,fullFilePath)
            subdirs=q.system.fs.listDirsInDir(dirFullPath, recursive=False, dirNameOnly=True)
            for subdirname in subdirs:
                if subdirname[0]<>".":
                    dirObject.addSubDir(subdirname)
            self.dirObjectFactory.save(dirObject)


    def _checkFileStatus(self,dirObject,fullFilePath):
        stat=q.system.fs.statPath(fullFilePath)
        filename=q.system.fs.getBaseName(fullFilePath)
        sizeOnDisk=stat.st_size
        modDateOnDisk=stat.st_mtime
        if self.usemd5:
            md5OnDisk=q.tools.hash.md5("/opt/qbase3/qshell")            
        else:
            md5OnDisk=""
        if not dirObject.containsFile(filename):
            #file is new
            dirObject.addFileObject(filename,sizeOnDisk,modDateOnDisk,md5OnDisk)
            self.reportNewFile(fullFilePath)    
            return dirObject
        [size, modDate, md5hash, dataKey] = dirObject.getFileInfo(filename)
        if not self.ignoreModDate:
            if float(modDate)<>float(modDateOnDisk):
#                q.console.echo("File %s changed because of moddate" % fullFilePath)
                self.reportModFile(fullFilePath)                
                return dirObject  
        if long(sizeOnDisk)<>long(size):
            self.reportModFile(fullFilePath)
#            q.console.echo("File %s changed because of size" % fullFilePath)
            return dirObject  
        if not self.usemd5:
            if md5OnDisk<>md5hash:
#                q.console.echo("File %s changed because of md5" % fullFilePath)
                self.reportModFile(fullFilePath)
                return dirObject
        return dirObject


    def reset(self):
        """
        remove all data from metadata store
        """
        q.system.fs.removeDirTree(self.metadataPath)
        self.__init__(self.metadataPath,self.root)


    def dirObjectGet(self,path):
        self._checkActive()
        return self.dirObjectStore.get(path)
    
    
    def dirObjectExists(self,path):
        self._checkActive()
        return self.dirObjectStore.exists(path)
    
    
