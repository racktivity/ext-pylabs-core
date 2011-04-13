from pylabs import q
from VFSTreeBuilder import VFSTreeBuilder
from infomodel import *
from iterators import DirNodeStoreCompositeIterator
from functools import partial
from pylabs import q

class ObjectStoreManager():
    """
    Is store for metadata for a filesystem
    We store dirNodes in a key/value store
    
    serialized format on disk read code
    {key:MetadataForDirObject} #key=last name of dir, will make sure we have no hash collisions, 
    """
    def __init__(self, metadataPath, rootpath=""):
        self.metadatapath = metadataPath
        q.system.fs.createDir(self.metadatapath)        
        self.db = q.db.getConnection(self.metadatapath)
        self.db.set = self.db.put#temp compatiblity workaround
        if not rootpath:
            if self.db.exists("main", "rootpath"): 
                self.root = self.db.get("main", "rootpath")
            else:
                raise RuntimeError("Cannot create an objectStore if the rootobject is not specified or known from previous state")
        else:
            self.root = rootpath
            self.db.set("main", "rootpath", rootpath)
        
    def get(self, versionEpoch=0):
        """
        @param versionEpoch if not specified will be latest version
        """
        return ObjectStore(self.db, self.metadatapath, versionEpoch=versionEpoch)        
    
    def new(self, processHiddenFiles=False, usemd5=False):
        """
        scan filesystem and populate objectStore
        """
        objectStore = ObjectStore(self.db, self.metadatapath, newversion=True)
        objectStore.stateSetError()
        #SCAN FS
        walker = VFSTreeBuilder(self.root, objectStore, processHiddenFiles, usemd5)
        walker.scan()
        objectStore.stateSetActive()
        return objectStore
    
    def delete(self, versionEpoch):
        if not self.db.exists("stateEpochToId", versionEpoch):
            raise RuntimeError("Cannot find metadata db for %s" % versionEpoch)
        scantimeId = self.db.get("stateEpochToId", id)
        metadataFSScan = q.system.fs.joinPaths(self.metadatapath, "states", scantimeId)
        q.system.fs.removeDirTree(metadataFSScan)
        self.db.delete("stateEpochToId", versionEpoch)     
                    
    def deleteOlderThan(self,olderThanInSec=0):
        """
        remove metadata older than in seconds, if 0 remove all
        """
        entries = self.db.list(category="stateEpochToId", minmtime=None, maxmtime=q.base.time.getTimeEpoch()-olderThanInSec)
        for entry in entries:
            self.delete(entry)

    def list(self):
        return self.db.list(category="stateEpochToId")
    
    def listHR(self):
        l=self.db.list(category="stateEpochToId")
        l=[self.db.get("stateEpochToId", item) for item in l]
        return l
   
class ObjectStore():
    
    def __init__(self, db, metadatapath, newversion=False, versionEpoch=0):
        self.db = db
        self.metadatapath = metadatapath
        
        if newversion and versionEpoch != 0:
            raise RuntimeError("cannot create new version and have a versionEpoch param defined, conflicts")
        
        self._metadatapathCurrent = ""
        if versionEpoch != 0:
            #get defined version
            self.scantimeId = self.db.get("stateEpochToId",versionEpoch)
            self._metadatapathCurrent = q.system.fs.joinPaths(self.metadatapath,"fsmetadata_%s"%self.scantimeId)
            self.stateSetActive()
            return 
        
        if newversion==False:
            if self.db.exists("main", "latestScanId"):      
                self.scantimeId = self.db.get("main","latestScanId")
                self._metadatapathCurrent = q.system.fs.joinPaths(self.metadatapath, "fsmetadata_%s"%self.scantimeId)        
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
        protectionnr = 0
        ttime = q.base.time.getTimeEpoch()
        self.scantimeId = q.base.time.getLocalTimeHRForFilesystem()
        self._metadatapathCurrent = q.system.fs.joinPaths(self.metadatapath,"fsmetadata_%s"%self.scantimeId)
        while q.system.fs.exists(self._metadatapathCurrent):
            if protectionnr > 100:
                raise RuntimeError("error in finding of unique id to record changes, overflow")
            protectionnr += 1
            if self.scantimeId.find("__") > -1:
                prefix = self.scantimeId.split("__")[0]
                order = int(self.scantimeId.split("__")[1])                    
                order += 1
            else:
                order = 1
                prefix = self.scantimeId
            self.scantimeId = prefix+"__"+str(order)
            self._metadatapathCurrent = q.system.fs.joinPaths(self.metadatapath,"fsmetadata_%s"%self.scantimeId)
        self.stateSetError()#metadata without population is error
        self.db.set("stateEpochToId", ttime, self.scantimeId) #remember the id's starting from epoch  (epoch to id mapping)
        self.db.set("main", "latestScanId", self.scantimeId) #remember the latest id
        q.system.fs.symlink(self._metadatapathCurrent, q.system.fs.joinPaths(self.metadatapath,"fsmetadata_current"), overwriteTarget=True)
        
    def stateSetError(self):
        self.db.set(self._getDBCat(), "STATE", "ERROR")
    
    def stateSetActive(self):
        self.db.set(self._getDBCat(), "STATE", "ACTIVE")

    def stateSetDeleted(self):
        self.db.set(self._getDBCat(), "STATE", "DELETED")
        
    def stateGet(self):
        self.db.get(self._getDBCat(), "STATE")

    def stateIsActive(self):
        return self.db.get(self._getDBCat(), "STATE") == "ACTIVE"

    def stateIsError(self):
        return self.db.get(self._getDBCat(), "STATE") == "ERROR"

    def stateIsNew(self):
        return self.db.get(self._getDBCat(), "STATE") == "NEW"

    def getKey(self,dirPath):
        separator="_!_"
        if dirPath.find(separator) != -1:
            raise RuntimeError("Cannot work with dir %s because it contains separator %s in pathname" % (separator, dirPath))
        
        key = dirPath.replace("/", separator)
        return key
    
    def _get(self,key):
        """
        get object from disk, fail if  not there
        """        
        return self.deserialize(key, self.db.get("fsmetadata_%s"%self.scantimeId, key))

    def _set(self, dirNode):
        """
        get object from disk, fail if  not there
        """        
        self.db.set("fsmetadata_%s"%self.scantimeId, dirNode.key, self.serialize(dirNode))
    
    def _exists(self, key):
        """
        see if object exists, if yes return True, otherwise False
        """        
        return self.db.exists("fsmetadata_%s"%self.scantimeId, key)

    def exists(self, dirPath):     
        key = self.getKey(dirPath)        
        return self._exists(key)

    def new(self, dirPath, getIfExists=False):
        key = self.getKey(dirPath)
        dirObj = None        
        if not self._exists(key):
            dirObj = DirNode(key, dirPath)
        else:
            if getIfExists:
                dirObj = self.get(dirPath)
            else:
                raise RuntimeError("Dir %s already exists" % dirPath)
        return dirObj

    def getCreateIfNotExist(self, path):
        if self.exists(path):
            return self.get(path)
        else:
            return self.new(path)
    
    def get(self, dirPath):
        key = self.getKey(dirPath)        
        if not self._exists(key):
            msg = "Dir %s does not exist" % dirPath
            q.logger.log(msg)
            raise NoEntryError(msg)
        else:
            dirNode = self._get(key)
        return dirNode
    
    def save(self, dirNode):
        self._set(dirNode)
        
    def serialize(self, dirNode):
        dirNode.updateModdate()
        return dirNode.serialize()
            
    def deserialize(self, key, content):
        obj = DirNode(None, None)
        return obj.deserialize(key, content)

    def walk(self, function, args, path, recursive=True):
        itr = DirNodeStoreCompositeIterator(self, path, recursive)
        for entry in itr:
            function(args, 
                  entry.name, 
                  'F' if entry.isLeaf else 'D',
                  entry.moddate,
                  getattr(entry, 'size', 0),
                  getattr(entry, 'md5hash', 0) )
        
    def _walk(self, function, args, path, recursive=True):
        """
        walks over dirobjects collection (virtual metadata, not on a real filesystem)
        pass function, argements given to function are 
            for file $args, $fullpath, "F", moddate, size, md5
            for dir $args, $fullpath, "D", 0,0,""
        """
        dirobject = self.get(path)
        files=dirobject.files.keys()
        files.sort()
        for key in files:
            size,modDate,md5hash = dirobject.files[key]
            fullpath = q.system.fs.joinPaths(path,key)
            function(args, fullpath, "F", modDate, size, md5hash)
        dirs = dirobject.dirs.values()
        dirs.sort()
        for dir in dirs:
            fullpath = q.system.fs.joinPaths(path, dir.path)
            function(args, fullpath, "D", 0, 0, "")
            if recursive:
                self.walk(function, args, fullpath, recursive)
            
    def __str__(self):
        raise RuntimeError("NOT IMPLEMENTED @todo please implement")
        
    def __repr__(self):
        return self.__str__()

