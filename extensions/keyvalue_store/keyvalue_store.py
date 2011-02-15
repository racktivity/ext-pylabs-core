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

    def put(self, category, key, value):
        """
        @param category: the category of the store, something like table in the relational db
        @param key: a key to identify the object that will be stored
        @param type to force a type
        """
        path=self._getDbRecordPath(category,key)
        q.system.fs.writeFile(path, "%s"%value)

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