from pylabs import q
from pylabs.Shell import *
from infomodel.infomodel import *
from infomodel.ObjectStore import ObjectStoreManager 


class VFSMetadata():
    """
    a userfriendly layer on top of DirObjectsStore
    allows manipulation of virtual filesystem e.g. walk over it, compare 2 versions of a filesystem, ...
    """
    
    def __init__(self, metadataPath, rootpath=""):
        self.metadataPath = metadataPath
        self.root = rootpath #path of root in which we will scan, when empty get from vfs metadata
        self.dirObjectsStore = ObjectStoreManager(metadataPath, self.root)
        if not self.root:
            self.root = self.dirObjectsStore.root
        q.system.fs.changeDir(self.root)
        self.state = "INIT"

    def _checkActive(self):
        if self.state != "OK":
            raise RuntimeError("Cannot continue, please populate vfs from filesystem of get latest version or another version, use functions get... or populate...")
        if not self.dirObjects.stateIsActive():
            raise RuntimeError("VFS is in wrong state, state=%s" % self.dirObjects.stateGet())

    def populateFromFilesystem(self, processHiddenFiles=False, usemd5=False):
        """
        scan filesystem and populate the VFS will create a new version of the metadata (each scan results in a new version)
        """
        self.state="SCAN"
        self.dirObjects = self.dirObjectsStore.new(processHiddenFiles, usemd5)  #the walk happens here
        self.walk=self.dirObjects.walk        
        self.state="OK"
        
    def getLatest(self):
        self.dirObjects = self.dirObjectsStore.get()
        self.walk=self.dirObjects.walk
        self.state="OK"
        
    def getFromVersionEpoch(self,versionEpoch):
        self.dirObjects = self.dirObjectsStore.get(versionEpoch=versionEpoch)
        self.walk = self.dirObjects.walk
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
        return self.dirObjectsStore.list()

    def listVersionsHR(self):
        """
        human readable list
        """
        return self.dirObjectsStore.listHR()
    
    def compareWithOlderVersion(self,versionEpoch,changefilePath,ignoreDate=False):
        """
        @param changefilePath is file in which changes will be recorded
        format
            $CHANGETYPE|F:size|moddate|md5|path
            $CHANGETYPE|D:|||path
        $CHANGETYPE is D,N,M (Deleted, New, Modified)
        
        """
        vfsOlder = VFSMetadata(self.metadataPath)
        vfsOlder.getFromVersionEpoch(versionEpoch=versionEpoch)
        self._checkActive()
        vfsOlder._checkActive()
        args={}
        q.system.fs.remove(changefilePath)
        def raiseError(path,error):
            q.system.fs.writeFile(changefilePath+".error","%s|%s\n"%(error,path), True)
        def compare(args, path, type, moddate, size, md5):
            if type=="D":
                if vfsOlder.dirObjectExists(path):
                    dirObject=self.dirObjectGet(path)
                    dirObjectOlder=vfsOlder.dirObjectGet(path)
                    setfilesOlder=set(dirObjectOlder.getFileNames())
                    setfiles=set(dirObject.getFileNames())
                    deletedfiles=setfilesOlder-setfiles
                    newfiles=setfiles-setfilesOlder
                    commonfiles=setfiles & setfilesOlder
                    for file in commonfiles:
                        size2,modDate2,md5hash2=dirObjectOlder.getFileInfo(file)
                        size,modDate,md5hash=dirObject.getFileInfo(file)
                        name = file
                        if ignoreDate:
                            if  (md5hash2=="" or md5hash==""):
                                raiseError(dirObjectOlder.getFilePath(name),"Cannot compare because hashing code is not known for file")
                            if md5hash<>md5hash2:
                                q.system.fs.writeFile(changefilePath,"M|F|%s|%s|%s|%s\n"%(size,modDate,md5hash,dirObject.getFilePath(name)),True)
                        else:
                            if modDate<>modDate2:
                                #file potentially changed
                                if md5hash<>"" and md5hash2<>"":
                                    #can use md5 to check
                                    if md5hash<>md5hash2:
                                        #we now know for sure files are different
                                        q.system.fs.writeFile(changefilePath,"M|F|%s|%s|%s|%s\n"%(size,modDate,md5hash,path),True)
                                else:
                                    #cannot use md5
                                        q.system.fs.writeFile(changefilePath,"M|F|%s|%s|%s|%s\n"%(size,modDate,md5hash,path),True)
                    for file in deletedfiles:
                        size,modDate,md5hash=dirObject.getFileInfo(file)
                        q.system.fs.writeFile(changefilePath,"D|F|%s|%s|%s|%s\n"%(size,modDate,md5hash,path),True)
                    for file in newfiles:
                        size,modDate,md5hash=dirObject.getFileInfo(file)
                        q.system.fs.writeFile(changefilePath,"N|F|%s|%s|%s|%s\n"%(size,modDate,md5hash,path),True)
                else:
                    #new dir, does not exist in old metadata
                    q.system.fs.writeFile(changefilePath,"N|D||||%s\n"%path,True)
                    
        self.walk(compare,args,"",recursive=True)
    
    
    def compareWithOlderVersionOld(self,versionEpoch):
        vfsOlder=VFSMetadata(self.metadataPath)
        vfsOlder.getFromVersionEpoch(versionEpoch=versionEpoch)
        self._checkActive()
        vfsOlder._checkActive()
        dirs=self.listDirsInDir("",recursive=True,dirNameOnly=False) #get dirs from current
        dirsOlder=vfsOlder.listDirsInDir("",recursive=True,dirNameOnly=False) #get dirs from older
        changes={}
        
        for dirPath in dirs:                        
            dirObjectOlder=vfsOlder.getDirObject(dirPath)
            dirObject=self.getDirObject(dirPath)
            #get the filenames from both dirobjects
            filenamesOlder=dirObjectOlder.getFileNames()            
            filenames=dirObject.getFileNames()
            for filename in filenames:
                pass
            ipshell()
                
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
        [size,modDate,md5hash] =dirObject.getFileInfo(filename)
        if not self.ignoreModDate:
            if float(modDate)<>float(modDateOnDisk):
                q.console.echo("File %s changed because of moddate" % fullFilePath)
                self.reportModFile(fullFilePath)                
                return dirObject  
        if long(sizeOnDisk)<>long(size):
            self.reportModFile(fullFilePath)
            q.console.echo("File %s changed because of size" % fullFilePath)
            return dirObject  
        if not self.usemd5:
            if md5OnDisk<>md5hash:
                q.console.echo("File %s changed because of md5" % fullFilePath)
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
        return self.dirObjects.get(path)
    
    def dirObjectExists(self,path):
        return self.dirObjects.exists(path)
    
    