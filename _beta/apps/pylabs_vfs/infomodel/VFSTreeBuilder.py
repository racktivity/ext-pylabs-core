#replaces PysyncWalker

from pylabs import q

class VFSTreeBuilder(object):
    def __init__(self, startPath, objectStore, processHiddenFiles=False, usemd5 = False):
        if not q.system.fs.exists(startPath):
            raise RuntimeError('Cannot build VFS Tree from dir: %s'%startPath)
        self.root = startPath
        self.objectStore = objectStore
        self.processHiddenFiles = processHiddenFiles
        
    def checkIfHiddenDir(self, path):
        if self.processHiddenFiles:
            return False
        for item in q.system.fs.pathNormalize(path).split("/"):
            if item.startswith("."):
                return True
        return False

    def scan(self):
        """
        """
        dirs=q.system.fs.listDirsInDir(self.root, recursive=True, dirNameOnly=False, findDirectorySymlinks=True)
        dirs.append(self.root) #make sure own directory is added as well
        for dirFullPath in dirs:                        
            if self.checkIfHiddenDir(dirFullPath): 
                continue
            q.console.echo("scan: %s" % dirFullPath)
            dirShortPath = q.system.fs.pathRemoveDirPart(dirFullPath, self.root, removeTrailingSlash=True).strip()
            dirObject = self.objectStore.new(dirShortPath)
            files = q.system.fs.listFilesInDir(dirFullPath)
            for fileFullPath in files:
                dirObject.addFile(fileFullPath)
            subdirs = q.system.fs.listDirsInDir(dirFullPath, recursive=False, dirNameOnly=True)
            for subdirname in subdirs:
                if subdirname[0]<>".":
                    dirObject.addSubDir(subdirname)
            self.objectStore.save(dirObject)
#                
#
#    def _reportFileChange(self,change,fullFilePath,size=0,modDate=0,md5hash=""): 
#        """
#        @param change N,D,M  (New, Deleted, Modified)
#        """
#        content = "%sF:%s|%s|%s|%s\n"%(change,fullFilePath,size,modDate,md5hash,key)
#        q.system.fs.writeFile(self._MetadataChangesPath, content, append=True)
#        ch = ""
#        if change=="N":
#            ch="NEW"
#        if change=="M":
#            ch="MOD"
#        if change=="D":
#            ch="DEL"
#        if ch=="":
#            raise RuntimeError("wrong change type, use N,D,M")
#        #q.console.echo("%s: %s" % (ch,fullFilePath))
#        

        