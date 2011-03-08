from pylabs.Shell import *
from pylabs import q

class PysyncWalker:
    """
    walker for filesystem will populate dirobjects
    """
    def __init__(self,startPath,dirobjects,processHiddenFiles=False,usemd5=False):
        if not q.system.fs.exists(startPath):
            raise RuntimeError("Cannot start walker for dir '%s', make sure it exist and is not empty." % startPath)
        self.usemd5=usemd5
        self.root=startPath     
        self.dirObjects=dirobjects
        self.processHiddenFiles=processHiddenFiles
        
    def checkIfHiddenDir(self,path):
        if self.processHiddenFiles:
            return False
        for item in q.system.fs.pathNormalize(path).split("/"):
            if item.strip()<>"" and item[0]==".":
                return True
        return False

    def scan(self):
        """
        """
        dirs=q.system.fs.listDirsInDir(self.root, recursive=True, dirNameOnly=False, findDirectorySymlinks=True)
        dirs.append(self.root) #make sure own directory is added as well
        for dirFullPath in dirs:                        
            if not self.checkIfHiddenDir(dirFullPath):
                q.console.echo("scan: %s" % dirFullPath)
                dirShortPath=q.system.fs.pathRemoveDirPart(dirFullPath, self.root, removeTrailingSlash=True).strip()
                dirObject=self.dirObjects.new(dirShortPath)
                files=q.system.fs.listFilesInDir(dirFullPath)
                for fullFilePath in files:
                    dirObject=self._getFileStatus(dirObject,fullFilePath)
                subdirs=q.system.fs.listDirsInDir(dirFullPath, recursive=False, dirNameOnly=True)
                for subdirname in subdirs:
                    if subdirname[0]<>".":
                        dirObject.addSubDir(subdirname)
                self.dirObjects.save(dirObject)
                
    def _getFileStatus(self,dirObject,fullFilePath):
        stat=q.system.fs.statPath(fullFilePath)
        filename=q.system.fs.getBaseName(fullFilePath)
        sizeOnDisk=stat.st_size
        modDateOnDisk=stat.st_mtime
        #creationDateOnDisk=stat.st_ctime
        #accessDateOnDisk=stat.st_atime
        if self.usemd5:
            md5OnDisk=q.tools.hash.md5(fullFilePath)            
        else:
            md5OnDisk=""            
        #return [filename,sizeOnDisk,modDateOnDisk,md5OnDisk]
        dirObject.addFileObject(filename,sizeOnDisk,modDateOnDisk,md5OnDisk)
        return dirObject
                

    def _reportFileChange(self,change,fullFilePath,size=0,modDate=0,md5hash=""): 
        """
        @param change N,D,M  (New, Deleted, Modified)
        """
        content="%sF:%s|%s|%s|%s\n"%(change,fullFilePath,size,modDate,md5hash,key)
        q.system.fs.writeFile(self._MetadataChangesPath, content, append=True)
        ch=""
        if change=="N":
            ch="NEW"
        if change=="M":
            ch="MOD"
        if change=="D":
            ch="DEL"
        if ch=="":
            raise RuntimeError("wrong change type, use N,D,M")
        #q.console.echo("%s: %s" % (ch,fullFilePath))
        

