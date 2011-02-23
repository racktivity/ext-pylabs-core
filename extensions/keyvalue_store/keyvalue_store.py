'''
Created on Aug 7, 2010

@author: abdelrahman, despiegk
'''
from pylabs.Shell import *

from pylabs import q
import cPickle

class DBConnection(object):
    """
    Represents a key/value db connection
    """
    
    def __init__(self, dbDir = "",name=""):
        """
        """
        if dbDir=="" and name<>"":
            dbDir = q.system.fs.joinPaths(q.dirs.varDir, 'db',name)
        if dbDir=="":
            raise RuntimeError("need to specify dbdir or name")
        self.dbDir = dbDir
        self._initialize()
        
    def _initialize(self):
        """
        Intializes the connection, create the directories
        """
        if not q.system.fs.isDir(self.dbDir):
            q.system.fs.createDir(self.dbDir)        
        self.id=q.application.getUniqueMachineId()
    
    def _getDbRecordPath(self, category, key):
        """
        create the path for the record in db
        @param category: the category of the store, something like table in the relational db
        @param key: a key to identify the object that will be stored
        """
        path = q.system.fs.joinPaths(self.dbDir, category)
        key=str(key)
        while len(key) < 5:
            key=key+"_"
        dirpath=q.system.fs.joinPaths(path, key[0:2],key[2:4])
        q.system.fs.createDir(dirpath)
        path = q.system.fs.joinPaths(dirpath,key+".db")
        return path

    def _lockParse(self, value):
        """
        @return machineid, time, value,locktimeout
        """
        if value.find("*_*LOCK*_*")==-1:
            raise RuntimeError("Cannot parse lock value %s, not well constructed."%(value))
        splitted=value.split("*_*LOCK*_*")
        if len(splitted)==4:
            return splitted #machineid, time, value,locktimeout
        else:
            RuntimeError("Cannot parse lock value %s, not well constructed."%(value))

    def lockcheck(self, category, key):
        """
        @return lockedTrueFalse,machineid, time, value,locktimeout
        """
        value=self.get(category, key)
        if value.find("*_*LOCK*_*")<>-1:
            return true, _lockParse(value)
        else:
            return False, 0, 0, value, 0

    def lockWaitFreeOrOurLock(self,category, key, timeout=5, force=False):
        """
        if locked will wait for time specified
        @param force, if force will erase lock when timeout is reached
        @return status,value    status=True when locked, False when free
        """
        value=self.get(category, key)
        start=q.base.time.getTimeEpoch()
        timedout=False
        while value.find("*_*LOCK*_*")<>-1 and timedout==False:     
            machineid, time, value2, locktimeout=self._lockParse(value)
            if machineid==self.id:
                #is our lock
                return True, value2
            if time+locktimeout<start:
                #the lock was already timed out we will remove
                self.settest(category, key, value2)
                return False, value2
            now=q.base.time.getTimeEpoch()
            if now-start>timeout:
                timedout=True
        if timedout:
            if force==False:
                raise RuntimeError("Cannot lock %s %s"%(category, key))
            else:
                machineid, time, value2, locktimeout=self. _lockParse(value)
                self.set(category, key, value2)
                return False, value2
        return False, value

    def lock(self, category, key, timeout=5, force=False):
        """
        will lock for max time specified (in sec)
        @param newvalue if specified will lock and set this value
        """
        locked, value=self.lockWaitFreeOrOurLock(category, key, timeout, force)
        valnew= "%s*_*LOCK*_*%s*_*LOCK*_*%s*_*LOCK*_*%s" % (self.id, q.base.time.getTimeEpoch(), value, timeout)
        self.set(category, key,valnew)
        if self.get(category, key)<>valnew:
            print "LOCK COLLISSION"
            return self.lock(category, key, timeout, force)
        return value
        
    def unlock(self, category, key,timeout=5,  force=False, newvalue=None):
        """
        will unlock if lock is from us, if force will take lock after timeout
        """
        locked, value=self.lockWaitFreeOrOurLock(category, key, timeout, force)
        if locked:
            if newvalue<>None:
                self.settest(category, key, newvalue)
            else:
                self.settest(category, key, value)
        else:
            if newvalue<>None:
                self.settest(category, key, newvalue)
        
    def incrementReset(self, category, newint=0):
        self.set("increment", category, newint)
            
    def increment(self, category):
        if not self.exists("increment", category):
            self.set("increment", category, 0)
            value=0
        else:
            value=self.lock("increment", category)
        try:
            integer=q.basetype.integer.fromString(value)
        except:
            raise RuntimeError("Could not increment category: %s, there was no integer in keyvalue store increment:category"%category)
        integer=integer+1
        self.unlock("increment", category,timeout=5,  force=False, newvalue=integer)
        return integer

    def settest(self, category, key, value):
        """
        if well stored return True
        """
        self.set(category, key, value)
        if self.get(category, key)==value:
            return True
        return False

    def set(self, category, key, value):
        """
        @param category: the category of the store, something like table in the relational db
        @param key: a key to identify the object that will be stored
        @param type to force a type
        """
        path=self._getDbRecordPath(category,key)
        q.system.fs.writeFile(path, "%s"%value)
        return True

    def exists(self, category, key):
        """
        Retrieve a value from the category with the specified key
        
        @param category: the category to fetch the value from
        @param key: they of the object to restore
        
        return True if exists, False if not
        """
        path=self._getDbRecordPath(category,key)
        if not q.system.fs.exists(path):
            return False
        else:
            return True
            
    def get(self, category, key,returnFalseWhenNotFound=False):
        """
        Retrieve a value from the category with the specified key
        
        @param category: the category to fetch the value from
        @param key: they of the object to restore
        
        @return: the object stored in a category with the specified key
        @raise RuntimeError: if the category/key doesnt exist unless if returnFalseWhenNotFound==True
        """
        path=self._getDbRecordPath(category,key)
        if not q.system.fs.exists(path):
            if returnFalseWhenNotFound:
                return False
            else:
                raise RuntimeError("Could not find object cat:%s key:%s in db: %s." % (category,key,path))
        content=q.system.fs.fileGetContents(path)
        #fd=open(path, 'rb')
        ##type=int(fd.readline())
        #content="\n".join(fd.readlines())
        #fd.close()
        return content
    
    def listCategories(self):
        """
        List all the category that is created in this db
        """
        return map(lambda path: q.system.fs.getBaseName(path), q.system.fs.listDirsInDir(self.dbDir))
    
    def list(self,category,minmtime=None,maxmtime=None):
        """
        @param minmtime min mod time of db entry in epoch
        @param maxmtime max mod time of db entry in epoch
        """        
        path = q.system.fs.joinPaths(self.dbDir, category)
        files=q.system.fs.listFilesInDir(path, recursive=True, filter="*.db", minmtime=minmtime, maxmtime=maxmtime)
        files=[q.system.fs.getBaseName(item) for item in files]
        files=[item[:-3] for item in files]
        return files
    
    def delete(self,category,key):
        path=self._getDbRecordPath(category,key)
        if q.system.fs.exists(path):
            q.system.fs.removeFile(path)

class DB(object):
    """
    Key/Value store database
    """
    
    def getConnection(self, dbDir):
        """
        If the connection to the same dbname and dbDir already exits, returns it. Otherwise create new connection and return it.
        
        @param dbDir: the directory where the database will be located, if None, then it will be /opt/qbase3/var/db/dbname
        """
        
        return DBConnection(dbDir)
