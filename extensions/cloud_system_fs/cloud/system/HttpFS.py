from pymonkey import q
from pymonkey.baseclasses.CommandWrapper import CommandWrapper
import urllib

CHUNKSIZE=8192

# FIXME: HTTP basic authentication support
class HttpFS(object):
    server = None
    path = None
    filename = None
    local_file = None
    end_type = None
    local_file = None
    http_socket = None

    def __init__(self,end_type,server,path,tempdir=q.dirs.tmpDir,Atype=None):
        """
        Initialize connection
        """
        q.logger.log("HttpFS: connection information: server [%s] path [%s]" % (server,path))
        self.filename = q.system.fs.getBaseName(path)
        self.tempdir=tempdir

        # Simple assumption
        if len(self.filename) == 0:
            self.filename = 'index.html'
            self.path = 'index.html'
        else:
            self.path = path

        """
        Initialize connection
        """
        q.logger.log("HttpFS: connection information: server [%s] path [%s]" % (server,path))
        self.filename = q.system.fs.getBaseName(path)
        self.tempdir=tempdir

        # Simple assumption
        if len(self.filename) == 0:
            self.filename = 'index.html'
            self.path = 'index.html'
        else:
            self.path = path

        self.server = server

    def _connect(self, suppressErrors=False):
        if not hasattr(self, 'local_dir') or not self.local_dir: self.local_dir =  '/'.join([self.tempdir , q.base.idgenerator.generateGUID()])
        self.local_file = '/'.join([self.local_dir , self.filename])
        self.local_dir = self.local_dir.replace('//', '/')
        self.local_file = self.local_file.replace('//', '/')

        # construct url again
        connect_url = 'http://%s%s' % (self.server,self.path)
        self.http_socket = urllib.urlopen(connect_url)

        if self.http_socket.getcode() == 403: # Forbidden
            if not suppressErrors:
                raise RuntimeError("You are not authorized to access resource: " + connect_url)
            return False
        if self.http_socket.getcode() == 404: # Not found
            if not suppressErrors:
                raise RuntimeError("Resouce %s not found" % connect_url)
            return False
        if self.http_socket.getcode() != 200: # OK
            if not suppressErrors:
                raise RuntimeError("unknown error occurd while geeting resource "+ connect_url)
            return False
        return True

    def exists(self):
        return self._connect(suppressErrors=True)

    def upload(self):
        """
        Upload of file
        This is currently not supported for HTTP
        """
        self._connect()
        return None

    def download(self):
        """
        Download file
        """
        self._connect()
        q.system.fs.createDir(self.local_dir)
        q.logger.log("HttpFS: downloading file to local file [%s]" % self.local_file)
        file = open(self.local_file,'wb')
        rb = self.http_socket.read(CHUNKSIZE)
        while rb:
            file.write(rb)
            rb = self.http_socket.read(CHUNKSIZE)
        #file.write(self.http_socket.read(CHUNKSIZE))
        file.close()
        return self.local_file

    def cleanup(self):
        """
        Cleanup http connection and temp file
        """
        q.system.fs.removeDirTree(self.local_dir)
