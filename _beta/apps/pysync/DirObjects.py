from pymonkey.Shell import *
from pymonkey import q

from PysyncWalker import *

class DirObjectsStore():
    """
    serialized format on disk read code )-:  #@todo despiegk: spec format
    {key:MetadataForDirObject} #key=last name of dir, will make sure we have no hash collissions, 
    """
    def __init__(self,metadataPath,rootpath=""):
        self.metadatapath=metadataPath
        q.system.fs.createDir(self.metadatapath)        
        self.db=q.db.getConnection(self.metadatapath)
        if rootpath=="":
            if self.db.exists("main","rootpath"): 
                self.root=self.db.get("main","rootpath")
            else:
                raise RuntimeError("Cannot create a dirobjectStore if the rootobject is not specified or know from previous state")
        else:
            self.root=rootpath
            self.db.put("main","rootpath",rootpath)
        
    def get(self,versionEpoch=0):
        """
        @param versionEpoch if not specified will be latest version
        """
        return DirObjects(self.db,self.metadatapath,versionEpoch=versionEpoch)        
    
    def new(self,processHiddenFiles=False,usemd5=False):
        """
        scan filesystem and populate DirObjects
        """
        dirObjects=DirObjects(self.db,self.metadatapath,newversion=True)
        dirObjects.stateSetError()
        #SCAN FS
        walker=PysyncWalker(self.root,dirObjects,processHiddenFiles,usemd5)
        walker.scan()
        dirObjects.stateSetActive()
        return dirObjects
    
    def delete(self,versionEpoch):
        if not self.db.exists("stateEpochToId",versionEpoch):
            raise RuntimeError("Cannot find metadata db for %s" % versionEpoch)
        scantimeId=self.db.get("stateEpochToId",id)
        metadataFSScan=q.system.fs.joinPaths(self.metadatapath,"states",scantimeId)
        q.system.fs.removeDirTree(metadataFSScan)
        self.db.delete("stateEpochToId",versionEpoch)     
                    
    def deleteOlderThan(self,olderThanInSec=0):
        """
        remove metadata older than in seconds, if 0 remove all
        """
        entries=self.db.list(category="stateEpochToId",minmtime=None,maxmtime=q.base.time.getTimeEpoch()-olderThanInSec)
        for entry in entries:
            self.delete(entry)

    def list(self):
        l=self.db.list(category="stateEpochToId")
        return l
    
    def listHR(self):
        l=self.db.list(category="stateEpochToId")
        l=[self.db.get("stateEpochToId",item) for item in l]
        return l
   

class DirObjects():
    
    def __init__(self,db,metadatapath,newversion=False,versionEpoch=0):
        self.db=db
        self.metadatapath=metadatapath
        
        if newversion==True and versionEpoch<>0:
            raise RuntimeError("cannot create new version and have a versionEpoch param defined, conflicts")
        self._metadatapathCurrent=""
        if versionEpoch<>0:
            #get defined version
            self.scantimeId=self.db.get("stateEpochToId",versionEpoch)
            self._metadatapathCurrent=q.system.fs.joinPaths(self.metadatapath,"fsmetadata_%s"%self.scantimeId)
            self.stateSetActive()
            return 
        if newversion==False:
            if self.db.exists("main","latestScanId"):      
                self.scantimeId=self.db.get("main","latestScanId")
                self._metadatapathCurrent=q.system.fs.joinPaths(self.metadatapath,"fsmetadata_%s"%self.scantimeId)        
                self.stateSetActive()
                q.system.fs.symlink(self._metadatapathCurrent,q.system.fs.joinPaths(self.metadatapath,"fsmetadata_current") , overwriteTarget=True)
            else:
                raise RuntimeError("Cannot find latest metadata of VFS, please reset VFS and start again")
        else:
                self.metadataDBNew()

    def _getDBCat(self):
        return "fsmetadatadb_%s"%self.scantimeId
        
    def metadataDBNew(self):
        """
        the result of walking over the filesystem is stored in a DB, this method makes sure we create a new version of the DB.
        """
        #check metadata path and create new one if it already exists, can only happen if this programm gets started 2 times < 1 sec
        protectionnr=0
        ttime=q.base.time.getTimeEpoch()
        self.scantimeId=q.base.time.getLocalTimeHRForFilesystem()
        self._metadatapathCurrent=q.system.fs.joinPaths(self.metadatapath,"fsmetadata_%s"%self.scantimeId)
        while q.system.fs.exists(self._metadatapathCurrent):
            if protectionnr>100:
                raise RuntimeError("error in finding of unique id to record changes, overflow")
            protectionnr+=1
            if self.scantimeId.find("__")>-1:
                prefix=self.scantimeId.split("__")[0]
                order=int(self.scantimeId.split("__")[1])                    
                order=order+1
            else:
                order=1
                prefix=self.scantimeId
            self.scantimeId=prefix+"__"+str(order)
            self._metadatapathCurrent=q.system.fs.joinPaths(self.metadatapath,"fsmetadata_%s"%self.scantimeId)
        #q.system.fs.createDir(self._metadatapathCurrent)        
        self.stateSetError()#metadata without population is error
        self.db.put("stateEpochToId",ttime,self.scantimeId) #remember the id's starting from epoch  (epoch to id mapping)
        self.db.put("main","latestScanId",self.scantimeId) #remember the latest id
        q.system.fs.symlink(self._metadatapathCurrent,q.system.fs.joinPaths(self.metadatapath,"fsmetadata_current") , overwriteTarget=True)
        
    def stateSetError(self):
        self.db.put(self._getDBCat(),"STATE","ERROR")
    
    def stateSetActive(self):
        self.db.put(self._getDBCat(),"STATE","ACTIVE")

    def stateSetDeleted(self):
        self.db.put(self._getDBCat(),"STATE","DELETED")
        
    def stateGet(self):
        self.db.get(self._getDBCat(),"STATE")

    def stateIsActive(self):
        return self.db.get(self._getDBCat(),"STATE")=="ACTIVE"

    def stateIsError(self):
        return self.db.get(self._getDBCat(),"STATE")=="ERROR"

    def stateIsNew(self):
        return self.db.get(self._getDBCat(),"STATE")=="NEW"

    def getKey(self,dirPath):
        separator="_!_"
        #dirPath=q.system.fs.pathNormalize(q.system.fs.pathDirClean(q.system.fs.pathShorten(q.system.fs.pathToUnicode(dirPath))))
        #dirPathShort=q.system.fs.pathRemoveDirPart(dirPath, self.root, removeTrailingSlash=True).strip()
        #key=q.tools.hash.md5_string(dirPathShort)
        #q.console.echo( "getkey:%s, %s"% (dirPathShort,key))
        if dirPath.find(separator)<>-1:
            raise RuntimeError("Cannot work with dir %s because has our separator %s in pathname" % (separator,dirPath))
        key=dirPath.replace("/",separator)
        return key
    
    def _get(self,key):
        """
        get object from disk, fail if  not there
        """        
        return self.deserialize(key,self.db.get("fsmetadata_%s"%self.scantimeId,key))

    def _put(self,dirObject):
        """
        get object from disk, fail if  not there
        """        
        self.db.put("fsmetadata_%s"%self.scantimeId,dirObject.key,self.serialize(dirObject))
    
    def _exists(self,key):
        """
        see if object exists, if yes return True, otherwise False
        """        
        exists= self.db.exists("fsmetadata_%s"%self.scantimeId,key)
        return exists

    def exists(self,dirPath):     
        key=self.getKey(dirPath)        
        return self._exists(key)

    def new(self,dirPath):
        key=self.getKey(dirPath)        
        if self._exists(key)==False:
            return DirObject(key,dirPath)
        else:
            raise RuntimeError("Dirobject %s does already exist" % dirPath)
            #self._put(dirObject)

    def getCreateIfNotExist(self,dirPath):
        if self.exists(dirPath):
            return self.get(dirPath)
        else:
            return self.new(dirPath)
    
    def get(self,dirPath):
        key=self.getKey(dirPath)        
        if self._exists(key)==False:
            raise RuntimeError("Dirobject %s does not exist" % dirPath)
        else:
            dirObject=self._get(key)
            #if dirObject.dirPath<>dirPath:                
            #    raise RuntimeError("Hash collission, 1 directory produced same md5 as a different dir")
        return dirObject
    
    def save(self,dirObject):
        self._put(dirObject)
        
    def serialize(self,dirObject):
        dirObject.updateModdate()
        content="1\n" #identifies format used, is for further reference
        content="%s%s\n"%(content,dirObject.dirPath)
        for key in dirObject.files.keys():
            [size,modDate,md5hash]=dirObject.files[key]
            content="%sF:%s|%s|%s|%s\n"%(content,size,modDate,md5hash,key)
        for key in dirObject.dirs:
            content="%sD:%s\n"%(content,key)
        return content
            
    def deserialize(self,key,content):
        lines=content.split("\n")
        typ=lines[0]
        obj=DirObject(key,lines[1])
        lines2=lines[2:]
        for line in lines2:
            if line.strip()<>"":
                if line[0:2]=="F:":
                    [size,modDate,md5hash,name]=line[2:].split("|")
                    obj.addFileObject(name,long(size),float(modDate),md5hash)
                if line[0:2]=="D:":
                    obj.addSubDir(line[2:])
        return obj

    def walk(self,function,args,path,recursive=True):
        """
        pass function, argements given to function are 
            for file $args, $fullpath, "F", moddate, size, md5
            for dir $args, $fullpath, "D", 0,0,""
        """
        dirobject=self.get(path)
        files=dirobject.files.keys()
        files.sort()
        for key in files:
            size,modDate,md5hash=dirobject.files[key]
            fullpath=q.system.fs.joinPaths(path,key)
            function(args,fullpath,"F",modDate,size,md5hash)
        dirs=dirobject.dirs
        dirs.sort()
        for dir in dirobject.dirs:
            fullpath=q.system.fs.joinPaths(path,dir)
            function(args,fullpath,"D",0,0,"")
            if recursive:
                self.walk(function,args,fullpath,recursive)
            
class DirObject():
    """
    self.stpoolid is id of storage pool in storage network e.g. mounted NFS filesystem
    self.moddate is epoch for last change of dir
    self.accessdate is epoch for last access of this dir
    """
    def __init__(self,key,path):
        """
        @param path is normalized path to directory (case sensitive) and short (is inside rootdir)
        @param files={} #key is name of file
        """
        self.dirPath=path
        self.files={} #key is name of file
        self.dirs=[]
        self.stpoolid=0
        self.key=key
        ttime=q.base.time.getTimeEpoch()
        #self.creationdate=ttime
        self.moddate=ttime
        #self.accessdate=ttime
        
    def updateAccessdate(self):
        self.accessdate=q.base.time.getTimeEpoch()

    def updateModdate(self):
        self.moddate=q.base.time.getTimeEpoch()        
        
    def getFileInfo(self,name):
        name=name.strip()
        if self.files.has_key(name):
            return self.files[name]
        else:
            return False

    def getFilePath(self,filename):
        

    def addFileObject(self,name,size,modDate,md5hash=""):
        name=name.strip()
        self.files[name]=[size,modDate,md5hash]        
    
    def addSubDir(self,name):
        if name not in self.dirs:
            self.dirs.append(name)
        
    def getFileNames(self):
        filenames=[]
        for key in self.files.keys():
            filenames.append(key)
        return filenames    
            
    def __str__(self):
        content="Dirpath: %s\n"% (self.dirPath)
        for key in self.files.keys():
            fileinfo=self.files[key]
            content="%sFile: %s %s\n" %(content,key,fileinfo)
        for dir in self.dirs:
            content="%sSubdir: %s\n" %(content,dir)
        return content
        
    def __repr__(self):
        return self.__str__()
