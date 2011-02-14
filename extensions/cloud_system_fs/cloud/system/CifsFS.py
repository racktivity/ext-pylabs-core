from pymonkey import q
from pymonkey.baseclasses.CommandWrapper import CommandWrapper
import os
import re

# requires smbfs package
class CifsFS(object):
    server = None
    share = None
    end_type = None
    filename = None
    username = None
    password = None
    mntpoint = None
    is_dir = False
    subdir = None
    recursive = False
    options = None

    _command = "mount.cifs"

    def __init__(self,end_type,server,share,username,password,is_dir,recursive,tempdir=q.dirs.tmpDir,Atype='copy'):
        """
        Initialize connection
        """
        q.logger.log('starting CIFS with %s' %share)
        self.is_dir     = is_dir
        self.is_mounted = False
        self.recursive  = recursive
        self.end_type   = end_type
        self.server     = server
        self.curdir     = os.path.realpath(os.curdir)
        self.Atype      = Atype
        self.share      = share

        lshare = share
        while lshare.startswith('/'):
            lshare = lshare.lstrip('/')
        while lshare.endswith('/'):
            lshare = lshare.rstrip('/')
        share_path = lshare.split('/')

        self.sharename = share_path[0]
        if len(share_path) > 1:
            subdirs = share_path[1:]
        else:
            subdirs=[]

        if not is_dir:
            self.filename = subdirs[-1]
            self.path_components = subdirs[:-1]
        else:
            self.filename = None
            self.path_components = subdirs

        self.username = re.escape(username)
        self.password = re.escape(password)
        self.mntpoint = '/'.join(['/mnt',q.base.idgenerator.generateGUID()])
        self.path     = '/'.join(self.path_components)

        print 'self.sharename:'       + str(self.sharename)
        print 'self.path_components:' + str(self.path_components)
        print 'self.path:'            + str(self.path)

    def _connect(self, suppressErrors=False):
        q.system.fs.createDir(self.mntpoint)

        # Mount sharename
        if self.username == None and self.password == None:
            command = '%s //%s/%s %s -o' % (self._command,self.server,self.sharename,self.mntpoint)
        else:
            command = '%s //%s/%s %s -o username=%s,password=%s' % (self._command,self.server,self.sharename,self.mntpoint,self.username,self.password)
        q.logger.log("CifsFS: executing command [%s]" % command)
        exitCode, output = q.system.process.execute(command,dieOnNonZeroExitCode=True, outputToStdout=False)

        # create remote dir
        q.system.fs.createDir(q.system.fs.joinPaths(self.mntpoint, self.path))

        self.orgmntpoint = self.mntpoint
        self.mntpoint    = q.system.fs.joinPaths(self.mntpoint, self.path)

    def exists(self):
        raise RuntimeError('Unsupported operation')

    def upload(self,uploadPath):
        """
        Store file
        """
        self._connect()
        if self.Atype == "move":
            if self.is_dir:
                if self.recursive:
                    q.system.fs.moveDir(uploadPath,self.mntpoint)
                else:
                # walk tree and move
                    for file in q.system.fs.walk(uploadPath, recurse=0):
                        q.logger.log("FileFS: uploading directory -  Copying file [%s] to path [%s]" % (file,self.mntpoint))
                        q.system.fs.moveFile(file,self.mntpoint)
            else:
                q.logger.log("CifsFS: uploading file - [%s] to [%s] filename [%s] (sub directory [%s])" % (uploadPath,self.mntpoint,self.filename,self.subdir))
                if self.subdir:
                    rfile = q.system.fs.joinPaths(self.subdir, self.filename)
                    q.logger.log("CifsFS: moving to [%s]" % rfile)
                    q.system.fs.moveFile(uploadPath,q.system.fs.joinPaths(self.mntpoint,rfile))
                else:
                    q.system.fs.moveFile(uploadPath,q.system.fs.joinPaths(self.mntpoint,self.filename))
        else:
            if self.Atype == "copy":
                if self.is_dir:
                    if self.recursive:
                        q.system.fs.copyDirTree(uploadPath,self.mntpoint)
                    else:
                    # walk tree and copy
                        for file in q.system.fs.walk(uploadPath, recurse=0):
                            q.logger.log("FileFS: uploading directory -  Copying file [%s] to path [%s]" % (file,self.mntpoint))
                            q.system.fs.copyFile(file,self.mntpoint)
                else:
                    q.logger.log("CifsFS: uploading file - [%s] to [%s] filename [%s] (sub directory [%s])" % (uploadPath,self.mntpoint,self.filename,self.subdir))
                    if self.subdir:
                        rfile = q.system.fs.joinPaths(self.subdir, self.filename)
                        q.logger.log("CifsFS: moving to [%s]" % rfile)
                        q.system.fs.copyFile(uploadPath,q.system.fs.joinPaths(self.mntpoint,rfile))
                    else:
                        q.system.fs.copyFile(uploadPath,q.system.fs.joinPaths(self.mntpoint,self.filename))

    def download(self):
        """
        Download file
        """
        self._connect()
        if self.is_dir:
            if self.subdir:
                pathname = q.system.fs.joinPaths(self.mntpoint,self.subdir,self.filename)
            else:
                pathname = self.mntpoint
            q.logger.log("CifsFS: downloading from [%s]" % pathname)
            return pathname
        else:
            if self.subdir:
                rfile = q.system.fs.joinPaths(self.subdir, self.filename)
                pathname =  q.system.fs.joinPaths(self.mntpoint,self.subdir,self.filename)
            else:
                pathname =  q.system.fs.joinPaths(self.mntpoint,self.filename)
            q.logger.log("CifsFS: downloading from [%s] the file [%s]" % (pathname,self.filename))
            return pathname

    def cleanup(self):
        """
        Umount cifs share
        """
        # umount the samba share
        q.logger.log("CifsFS: Cleaning up and umounting the share")
        command = "umount %s" % self.orgmntpoint

        exitCode, output = q.system.process.execute(command, dieOnNonZeroExitCode=False, outputToStdout=False)
        if not exitCode == 0:
            raise RuntimeError('Failed to execute command %s'%command)

        if q.system.fs.exists(self.orgmntpoint):
            q.system.fs.removeDir(self.orgmntpoint)

        self.is_mounted = False

    def list(self):
        """
        List content of directory
        """
        os.chdir(self.mntpoint)
        if self.path_components:
            if len(self.path_components) > 1:
                os.chdir('/'.join(self.path_components[:-1]))
                if os.path.isdir(self.path_components[-1]):
                    os.chdir(self.path_components[-1])
                else:
                    raise RuntimeError('%s is not a valid directory under %s' %('/'.join(self.path_components),self.sharename))
            if os.path.isdir(self.path_components[0]):
                os.chdir(self.path_components[0])

        flist = q.system.fs.walk(os.curdir,return_folders=1,return_files=1)
        os.chdir(self.curdir)
        q.logger.log("list: Returning content of share [%s] which is tmp mounted under [%s]" % (self.share , self.mntpoint))

        return flist

    def __del__(self):
        if self.is_mounted:
            q.logger.log('CifsFS GC') 
            self.cleanup()
        os.chdir(self.curdir)
