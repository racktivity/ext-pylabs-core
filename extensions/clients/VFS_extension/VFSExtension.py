from pylabs import q
import sys
sys.path.append('/opt/qbase5/lib/pylabs/extensions/pylabs_vfs')
from VFSMetadata import *


class VFSExtension(object):
    
    def __init__(self):
        self._mounted = False
        self.vfs = None
    
    def _preMount(self,mountpoint, root, localfilestore=None, metadatapath=None):
        ''' A prerequisite method for mounting the Virtual FileSystem '''
        
        cfgpath = q.system.fs.joinPaths(q.dirs.cfgDir, 'vfs.cfg')
        cfgfile = q.tools.inifile.open(cfgpath) 
        
        if cfgfile.getValue('status','mounted') == 'True':
            self.unmount()
        
        if localfilestore:
            cfgfile.setParam('vfs_paths', 'localfilestore', localfilestore)
        if metadatapath:
            cfgfile.setParam('vfs_paths', 'metadatapath', metadatapath)
            

        cfg = cfgfile.getSectionAsDict('vfs_paths')                
        self.mountpoint = mountpoint
        
        if q.system.fs.isDir(self.mountpoint):
            if not q.system.fs.isEmptyDir(self.mountpoint):
                raise RuntimeError('the mount directory must be empty')
        else:
            q.system.fs.createDir(self.mountpoint)
            
        
        self.vfs = VFSMetadata(q.system.fs.joinPaths(cfg['metadatapath'],'vfsMD'), mountpoint)
        cfgfile.setParam('status','mounted','True')
    
    def mount(self, mountpoint, root, localfilestore=None, metadatapath=None):#, savepaths=False):
        
        #Check for the mount status of the virtual filesystem
        self._preMount(mountpoint, root, localfilestore, metadatapath)
        command = 'python /opt/qbase5/lib/pylabs/extensions/clients/vfs/memvfs.py '+self.mountpoint
        try:
            q.system.unix.executeAsUser(command, username='root')
            self._mounted = True
        except Exception as ex:
            q.logger.log(ex)
        
        #Initializing the virtual filesystem's metadata
        self._initializeVFS()

    def listVersions(self):
        if self._mounted:
            return self.vfs.listVersions()
        
    def listVersionsHR(self):
        if self._mounted:
            return self.vfs.listVersionsHR()
    
    def update(self):
        if self._mounted:
            self.vfs.populateFromFilesystem()
        
    def getLatestVersion(self):
        if self._mounted:
            self.vfs.getLatest()
            
    def _initializeVFS(self):
        self.vfs.reset()
        self.vfs.populateFromFilesystem() 
        self.vfs.getLatest()
        
    def diffWithOlderVersion(self, versionEpoch, groupSimilarOperations=False, ignoreEquals=True):
        if self._mounted:
            return self.vfs.diffWithOlderVersion(versionEpoch, groupSimilarOperations, ignoreEquals)
        
    def compareCurrentWithOlder(self, versionEpoch):
        if self._mounted:
            return self.vfs.compareWithOlderVersion(versionEpoch)
    
    
    def unmount(self):
        cfgpath = q.system.fs.joinPaths(q.dirs.cfgDir, 'vfs.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        cfg = cfgfile.getSectionAsDict('vfs_paths')
        
        command = 'fusermount -uz '+cfg['mountpoint']
        self.vfs = None
        try:
            q.system.unix.executeAsUser(command, username='root')
            self._mounted = False
        except Exception as ex:
            q.logger.log(ex)
