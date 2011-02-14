from pymonkey import q
from ftplib import FTP
from pymonkey.baseclasses.CommandWrapper import CommandWrapper
import os

# maybe this could be switched to http://curlftpfs.sourceforge.net/ 
class FtpFS(object):
    server = None
    path = None
    filename = None
    end_type = None
    username = 'anonymous'
    password = 'user@aserver.com'
    local_file = None
    ftp = None
    is_dir = False
    recursive = False

    def __init__(self,end_type,server,path,username,password,is_dir=False,recursive=False,tempdir=q.dirs.tmpDir, Atype='copy'):
        """
        Initialize connection
        """
        q.logger.log("FtpFS: connection information: server [%s] path [%s] username [%s] password [%s]" % (server,path,username,password))

        self.end_type = end_type
        self.Atype = Atype
        self.server = server
        # what if no path is specified
        self.filename = q.system.fs.getBaseName(path)
        #self.path = path.rstrip(self.filename).lstrip('/')
        self.path = os.path.dirname(path).lstrip('/')
        #q.logger.log("FtpFS: path is %s" % self.path)
        self.local_dir =  q.system.fs.joinPaths(tempdir , q.base.idgenerator.generateGUID())
        self.local_file = q.system.fs.joinPaths(self.local_dir , self.filename)
        self.tempdir=tempdir
        q.system.fs.createDir(self.local_dir)

        self.is_dir = is_dir
        self.recursive = recursive

        if is_dir == False:
            q.logger.log("FtpFS: copying filename [%s] path [%s]" % (self.filename,self.path))
        else:
            q.logger.log("FtpFS: copying to local directory [%s] from path [%s]" % (self.local_dir,self.path))

        self.username = username
        self.password = password

    def _connect(self, dontCD=False):
        try:
            self.ftp = FTP(self.server)
            #self.ftp.set_debuglevel(2)
            self.ftp.connect()
            if self.username != None and self.password != None:
                self.ftp.login(self.username,self.password)
            else:
                self.ftp.login()
        except:
            raise RuntimeError('Failed to login on ftp server [%s] credentials login: [%s] pass [%s]' % (self.server,self.username,self.password))
        # change to correct directory
        if not dontCD:
            path = self.path.lstrip(os.sep).split(os.sep)
            for directory in path:
                try:
                    self.ftp.cwd(directory)
                except:
                    self.ftp.mkd(directory)
                    self.ftp.cwd(directory)

    def exists(self):
        self._connect(dontCD=True)
        try:
            self.ftp.cwd(self.path)
        except:
            return False
        if (not self.is_dir):
            self.found=False
            def walker(x):
                if x.find(self.filename) != -1:
                    self.found=True
            self.ftp.dir(walker)
            return self.found

    def upload(self,uploadPath):
        """
        Store file
        """
        self._connect()
        q.logger.log("FtpFS: uploading [%s] to FTP server" % uploadPath)
        if self.is_dir:
            f = q.system.fs.listFilesInDir(uploadPath)
            f += q.system.fs.listDirsInDir(uploadPath)
    #                d = q.system.fs.listDirsInDir(uploadPath,self.recursive)
            for file in f:
                q.logger.log("Checking file [%s]" % file)
                if q.system.fs.isDir(file):
                    self.handleUploadDir(file,uploadPath)
                else:
                    remotefile = q.system.fs.getBaseName(file)
                    self.storeFile(remotefile,file)
        else:
            if q.system.fs.getBaseName(self.local_file) == '':
                    remotefile = q.system.fs.getBaseName(uploadPath)
            else:
                    remotefile = self.filename
            self.storeFile(remotefile,uploadPath)

    def download(self):
        """
        Download file
        """
        self._connect()
        # FIXME: make sure the original file name is kept
        # should return path to which file was downloaded
        if self.is_dir:
            q.logger.log("FtpFS: downloading dir [%s]" % self.path)
            listing = []
            remote_file_list = self.ftp.retrlines('LIST', listing.append)
            for l in listing:
                t = l.split()
                name = t[-1:]
                q.logger.log("Checking t [%s] with name [%s]" % (t,name))
                if len(name) > 0:
                    if t[0].startswith('d'): #WARNING: dirty-hack alarm!
                        ldir = q.system.fs.joinPaths(self.ftp.pwd(), name[0])
                        self.handleDownloadDir(ldir)
                    elif t[0].startswith('l'): 
                        q.logger.log("FtpFS: symlink on FTP (skipping)")
                    else: # it's a normal file
                        q.logger.log("FtpFS: normal file")
                        #rdir = '/'.join([self.local_dir , self.path])
                        rdir = q.system.fs.joinPaths(self.local_dir , self.path)
                        q.system.fs.createDir(rdir)
                        self.retrieveFile(name[0],self.path,rdir)
                else:
                    q.logger.log("FtpFS: skipping [%s]" % name)
            return self.local_dir
        else:
            self.retrieveFile(self.filename,self.path,self.local_file)
            return self.local_file

    def cleanup(self):
        """
        Cleanup of ftp connection
        """
        self.ftp.quit()
        q.system.fs.removeDirTree(self.local_dir)

    def retrieveFile(self,file,dir,dest):
        """
        Ftp copying file
        """
        if self.is_dir:
            lfile = q.system.fs.joinPaths(dest, file)
        else:
            lfile = self.local_file
        q.logger.log("FtpFS: retrieving [%s] from dir [%s] to [%s]" % (file, dir,lfile))
        self.ftp.retrbinary('RETR %s' % file, open(lfile, 'wb').write)

    def storeFile(self,file,uploadPath):
        """
        Ftp upload file
        """
        q.logger.log("FtpFS: storing [%s] from [%s]" % (file,uploadPath))
        self.ftp.storbinary('STOR %s' % file, open(uploadPath, 'rb'), 1024)

    def handleUploadDir(self,dir,upload_path):
        """
        Ftp handle a upload directory
        """
        self._connect()
        q.logger.log("FtpFS: handleUploadDir [%s]" % dir)
        dname = q.system.fs.getBaseName(dir)
        q.logger.log("FtpFS: dirname is %s and upload path %s" % (dname, upload_path))
        fname =  dir.replace(upload_path, '')
        previous_dir = '/'.join(['/' , self.path])
        #creating directory on FTP
        q.logger.log("FtpFS: mkd and cwd to [%s] (previous dir %s)" % (fname,previous_dir))
        self.ftp.mkd(fname)
        #self.ftp.cwd(fname)

        f = q.system.fs.listFilesInDir(dir)
        f += q.system.fs.listDirsInDir(dir)
#       d = q.system.fs.listDirsInDir(uploadPath,self.recursive)
        for file in f:
            q.logger.log("Checking file [%s]" % file)
            if q.system.fs.isDir(file):
                self.handleUploadDir(file,upload_path)
            else:
               remotefile = q.system.fs.getBaseName(file)
               self.ftp.cwd(fname)
               self.storeFile(remotefile,file)
               self.ftp.cwd(previous_dir)

    def handleDownloadDir(self,dirname):
        """
        Ftp handle a download directory
        """
        self._connect()
        q.logger.log("FtpFS: handleDownloadDir [%s]" % dirname)
        rdir = '/'.join([self.local_dir , dirname])
        q.logger.log("FtpFs: handleDownloadDir - creating local [%s]" % rdir)
        q.system.fs.createDir(rdir)
        self.ftp.cwd(dirname)

        listing = []
        remote_file_list = self.ftp.retrlines('LIST', listing.append)
        for l in listing:
           t = l.split()
           name = t[-1:]
           q.logger.log("Checking t [%s] with name [%s]" % (t,name))
           if len(name) > 0:
                    if t[0].startswith('d'): #WARNING: dirty-hack alarm!
                        ldir = q.system.fs.joinPaths(self.ftp.pwd(), name[0])
                        self.handleDownloadDir(ldir)
                    elif t[0].startswith('l'): 
                        q.logger.log("FtpFS: symlink on FTP (skipping)")
                    else: # it's a normal file
                        q.logger.log("FtpFS: normal file, attempting to retrieve file [%s] to location [%s]" % (name[0], rdir))
                        self.retrieveFile(name[0],self.path,rdir)
           else:
                q.logger.log("FtpFS: skipping [%s]" % name)

        previous_dir = dirname.rstrip(q.system.fs.getBaseName(dirname))
        self.ftp.cwd(previous_dir) 

    def list(self):
        """
        List files in dir
        """
        self._connect()
        dir_content = []
        q.logger.log("list: Returning list of FTP directory [%s]" % self.path)
        listing = []
        self.ftp.retrlines('LIST', listing.append)
        for l in listing:
            t = l.split()
            name = t[-1:][0]
            dir_content.append(name)

        return dir_content
