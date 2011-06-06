from GServer import *
from pylabs import q
import cgi
import os
import errno

class NoEntryError(RuntimeError):
    def __init__(self, *args):
        self.msg = args[0]
        self.errno = -errno.ENOENT
   
class VFSServerExtension(object):
    
    def __init__(self):
        pass
    
    def start(self, metadataPath, rootPath, serverHost='127.0.0.1', serverPort=8080, keyfile=None, certfile=None, SSLCredentials=None, async=False):
        ''' Starts a VFS server on the given host:port 
        
        @param metadataPath: The path of the metadata directory on the server.
        @param rootPath: The path of the root directory to mount the VFS on.
        @param serverHost: The IP address of the server host.
        @param serverPort: The port number the server will listen on.
        @param keyfile: An optional key file for encrypted connections.
        @param certfile: An optional certificate for encrypted connections. 
        @param SSLCredentials: An option field; 's'aves/'l'oads supplied SSL credentials to/from a configuration file 
        @param async: If True, the VFS server will start in an asynchronous mode
        '''
         
        self.metadataPath = metadataPath
        self.rootPath = rootPath
        self.handler = VFSHandler(metadataPath, rootPath)
        self.gserver = GServer(self.handler)
        if SSLCredentials and str.lower(SSLCredentials) == 's':
            self._saveSSLCredentials(keyfile, certfile)
        elif SSLCredentials and str.lower(SSLCredentials) == 'l':
            keyfile, certfile = self._loadSSLCredentials()
        self.gserver.start(serverHost, serverPort, keyfile, certfile, async)
    
    def stop(self, timeout=None):
        ''' Stops the VFS server serving on host:port 
    
        @param timeout: Time in milliseconds beyond which a forced halt will be issued '''
        self.gserver.stop(timeout)
        
    def restart(self, timeout=None, keyfile=None, certfile=None, async=False):
        ''' Restarts the VFS Server on the same host:port specified upon starting the server for the first time
        
        @param timeout: Time in milliseconds beyond which a forced halt will be issued
        @param keyfile: An optional key file for encrypted connections
        @param certfile: An optional certificate for encrypted connections
        @param async: If True, the VFS server will start in an asynchronous mode 
        '''
        self.stop(timeout)
        self.start(self.metadataPath, self.rootPath, async=async)
        
    def _loadSSLCredentials(self):
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'pylabs_vfsserver', 'vfsserverextension.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        if cfgfile.checkSection('SSL_Credentials'):
            return cfgfile.getValue('SSL_Credentials','keyfile'),cfgfile.getValue('SSL_Credentials','certfile')
    
    def _saveSSLCredentials(self, keyfile, certfile):
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'pylabs_vfsserver', 'vfsserverextension.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        cfgfile.addSection('SSL_Credentials')
        params = {'keyfile':keyfile, 'certfile':certfile}
        for k, v in params.items():
            cfgfile.addParam('SSL_Credentials', k, v)
        
     
class VFSHandler(object):
    
    def __init__(self, metadataPath, rootPath):
        self.vfs = q.system.vfs.getVFS(metadataPath, rootPath, True)
        self.currentVersion, self.currentVersionHR = sorted(self.vfs.listVersions()).pop(), sorted(self.vfs.listVersionsHR()).pop()
    
    def _findDir(self, path):
        return self.vfs.dirObjectGet(path)
    
    def _findFile(self, path):
        '''
        raise NoEntryError if path doesn't correspond to a file
        @return dirNode, fileNode
        '''
        dirNode = None
        #how to handle files, while the VFS holds only size?
            #assume the path is file path and get its parent folder
        parentPath = os.path.dirname(path)
        fileName = q.system.fs.getBaseName(path)
        fileNode = None
        try:
            dirNode = self.vfs.dirObjectGet(parentPath)
            if fileName in dirNode.files:
                fileNode = dirNode.files[fileName]
            else:
                raise NoEntryError('No such file: %s'%path)
        except NoEntryError, ex:
            q.logger.log('No such directory: %s'%parentPath)
            raise
        return dirNode, fileNode
    
    def _getRelativePath(self, path, objType):
        relativePath = path.replace(self.vfs.root,'').split('/') #Getting the relative path of the file by omitting the VFS rootPath
        if objType == 'file':
            relativePath.pop() #Removing the last item from the relative path, assuming it's the file name
        relativePath = [item for item in relativePath if item <> ''] #Cleaning up empty strings resulting from extra slashes '/'
        relativePath = '/'.join(relativePath) #Joining the left directory(ies) into a string
        return relativePath        

    def handle(self, env, start_response):
        methods = {
        'dirstat' : self.dirstat,
        'fileGetInfo' : self.fileGetInfo,
        'listVersions' : self.listVersions,
        'getFromVersionEpoch': self.getFromVersionEpoch,
        'getLatest': self.getLatest
        }
        segments = filter(lambda seg: seg, env['PATH_INFO'].split('/'))
        try:
            handler_method = methods[segments[0]]
            start_response('200 OK', [('Content-Type', 'text/html')])
            queryString = env['QUERY_STRING']
            queryParams = dict(cgi.parse_qsl(queryString))
            if queryParams:
                result = handler_method(**queryParams)
            else:
                result = handler_method() #In case of parameter-less methods
            return [str(result)]
        except (KeyError, IndexError, ValueError):
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return ['<h1>Not Found</h1>']  
    
        
    def dirstat(self, path):
        ''' Gets directory info from the VFS object Store 
        
        @param path: The absolute path of the directory
        
        @return: A dictionary of the directory information
        '''
        relativePath = self._getRelativePath(path, 'dir')      
        dirNode = self._findDir(relativePath)
        result = list()
        result.append(sorted(dirNode.dirs.keys())) #Adding a sorted list of sub-directories to the result list
        result.append(sorted([self.fileGetInfo(file) for file in dirNode.files.keys()])) #Adding a sorted list of files to the result list
        return {'version': '%s: %s'%(self.currentVersionHR,self.currentVersion), 'content':result}
#        def fileNodeToDic(fileNode):
#            attrs = ('crtdate', 'docId', 'md5hash', 'name', 'moddate', 'size')
#            result = {}
#            return [result.update([(attr, getattr(fileNode, attr, ''))]) for attr in attrs]
#        
#        result.append(sorted([(f.name, fileNodeToDic(f)) for f in dirNode.files.values()]), key=lambda t: t[0])
#        return result
    
    def fileGetInfo(self, path):
        ''' Gets file info from the VFS object store
        
        @param path: The absolute path of the file
        
        @return: A dictionary of the file information 
        '''
        relativePath = self._getRelativePath(path, 'file')
        tmpDir = self.vfs.dirObjectStore.get(relativePath)
        if tmpDir.containsFile(path):
            fileInfo = tmpDir.getFileInfo(path)
            return {'version': '%s: %s'%(self.currentVersionHR,self.currentVersion), 'content': {'name':fileInfo.name,'size':fileInfo.size,'moddate':fileInfo.moddate,'crtdate':fileInfo.crtdate,'md5hash':fileInfo.md5hash,'docId':fileInfo.docId,'dataKey':fileInfo.dataKey}}
        else:
            raise NoEntryError('Cannot find file: %s'%path)

    def listVersions(self):
        ''' Lists the metadata versions of the mounted VFS
        
        @return: A dictionary of metadata versions in the form of 'Human-readable Epoch version':Epoch version '''
        return {'version': '%s: %s'%(self.currentVersionHR,self.currentVersion), 'content': dict(zip(self.vfs.listVersionsHR(),self.vfs.listVersions()))}
    
    def getFromVersionEpoch(self, versionEpoch):
        '''Gets the metadata version specified
        
        @param versionEpoch: The epoch version to retrieve'''
        self.vfs.getFromVersionEpoch(versionEpoch)
        self.currentVersion, self.currentVersionHR = versionEpoch, self.vfs.dirObjectStore.scantimeId 
        return {'version': '%s: %s'%(self.currentVersionHR,self.currentVersion)} 
    
    def getLatest(self):
        ''' Gets the latest metadata version'''
        self.vfs.getLatest()
        self.currentVersion, self.currentVersionHR = sorted(self.vfs.listVersions()).pop(), sorted(self.vfs.listVersionsHR()).pop()
        return {'version': '%s: %s'%(self.currentVersionHR,self.currentVersion)} 


