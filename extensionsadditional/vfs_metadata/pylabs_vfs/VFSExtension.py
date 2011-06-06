from VFSMetadata import *
from infomodel.infomodel import DirNode, FileNode

class VFSExtension():
    
    def _getNewFileNode(self, name, size, mtime):
        return FileNode(name, size, mtime)
    
    def _getNewDirNode(self, key, path):
        return DirNode(key, path)
    
    def getVFS(self, metadataPath, rootPath, populate=False):
        '''Gets an instance of the VFSMetadata class
        
        @param metadataPath: The path of the metadata
        @param rootPath: The path to populate and act as root
        @param populate: If true, the specified root directory will be scanned and a new
                         Epoch version will be created
        @return: An instance of the VFS Metadata '''
        
        vfs = VFSMetadata(metadataPath, rootPath)
        if populate:
            vfs.populateFromFilesystem()
        return vfs
    
    def exportMetadata(self, vfs, exportPath):
        ''' Exports the metadata folder to the specified export Path
        
        @param vfs: The current metadata instance
        @param exportPath: The directory to export to '''
        
        q.system.fs.copyDirTree(vfs.metadataPath, exportPath)
    
    def importMetadata(self, vfs, importPath, versionEpoch=None, overwriteMetadata=False):
        ''' Imports metadata from the specified import path 
        
        @param vfs: The current metadata instance
        @param importPath: The path to import the metadata from
        @param versionEpoch: If specified, the specified Epoch version of the metadata
                             will be returned
        @param overwriteMetadata: If True, the current metadata instance will be reset
        @return: Returns the latest version of the metadata or a specific one based on
                 the parameters above.'''
        
        if overwriteMetadata:
            vfs.reset()
        q.system.fs.copyDirTree(importPath,vfs.metadataPath,overwriteMetadata)
        if versionEpoch:
            vfs.getFromVersionEpoch(versionEpoch)
        else:
            vfs.getLatest()
        return vfs

    
    
        