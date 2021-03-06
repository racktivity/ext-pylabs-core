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
#            q.console.echo("scan: %s" % dirFullPath)
            dirShortPath = q.system.fs.pathRemoveDirPart(dirFullPath, self.root, removeTrailingSlash=True).strip()
            dirObject = self.objectStore.new(dirShortPath)
            dirObject.fullpath = dirFullPath
            files = q.system.fs.listFilesInDir(dirFullPath)
            for fileFullPath in files:
                #Make a file object to be added to the DirNode
                fileObject = q.system.fs.statPath(fileFullPath) #Get file stats
                fileHash = q.tools.hash.md5(fileFullPath) #Get file content hash
                fileDataKey = ''
                fileDocId = ''
                dirObject.addFile(fileFullPath,fileObject.st_size,fileObject.st_mtime, fileObject.st_ctime, fileHash, fileDataKey, fileDocId) #add the file object details, hash, datakey, and docId
            subdirs = q.system.fs.listDirsInDir(dirFullPath, recursive=False, dirNameOnly=True)
            for subdirname in subdirs:
                if subdirname[0]<>".":
                    dirObject.addSubDir(subdirname)
            self.objectStore.save(dirObject)
#        

        