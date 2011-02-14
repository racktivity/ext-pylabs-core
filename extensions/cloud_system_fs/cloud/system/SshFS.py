from pymonkey import q
from pymonkey.baseclasses.CommandWrapper import CommandWrapper
import os
import re

# requires sshfs package
class SshFS(object):
        server = None
        directory = None
        share = None
        filename = None
        end_type = None
        username = None
        password = None
        mntpoint = None
        _command = 'sshfs'

        def __init__(self,end_type,server,directory,username,password,is_dir,recursive,tempdir=q.dirs.tmpDir, Atype='copy'):
            """
            Initialize connection
            """

            self.is_dir = is_dir
            self.recursive = recursive
            self.end_type = end_type
            self.server = server
            self.share = directory
            self.tempdir=tempdir
            self.Atype = Atype
            self.curdir = os.path.realpath(os.curdir)

            ldirectory = directory
            while ldirectory.startswith('/'):
                ldirectory = ldirectory.lstrip('/')
            while ldirectory.endswith('/'):
                ldirectory = ldirectory.rstrip('/')
            self.path_components = ldirectory.split('/')
            

            if not self.is_dir:
                self.filename = q.system.fs.getBaseName(directory)
                self.directory = os.path.dirname(self.share)
            else:
                self.directory = self.share

            self.username = re.escape(username)
            self.password = re.escape(password)
            self.mntpoint = '/'.join(['/mnt',q.base.idgenerator.generateGUID()])
            self.is_mounted = False
            

        def _connect(self):
            q.system.fs.createDir(self.mntpoint)

            q.logger.log("SshFS: mounting share [%s] from server [%s] with credentials login [%s] and password [%s]" % (self.directory,self.server,self.username,self.password))

            command = "echo \"%s\" | %s %s@%s:%s %s  -o password_stdin -o StrictHostKeyChecking=no" % (self.password,self._command,self.username,self.server,self.directory,self.mntpoint)
            
            q.logger.log("SshFS: executing command [%s]" % command)

            exitCode, output = q.system.process.execute(command,dieOnNonZeroExitCode=False, outputToStdout=False)
            if not exitCode == 0:
                raise RuntimeError('Failed to execute command %s'%command)
            else:
                self.is_mounted = True

        def exists(self):
            raise RuntimeError('Not supported')

        def upload(self,uploadPath):
            """
            Store file
            """
            self. _connect()
            if self.Atype == "move":
                if self.is_dir:
                    if self.recursive:
                        q.system.fs.moveDir(uploadPath,self.mntpoint)
                    else:
                        # walk tree and move
                        for file in q.system.fs.walk(uploadPath, recurse=0):
                            q.logger.log("SshFS: uploading directory -  Copying file [%s] to path [%s]" % (file,self.mntpoint))
                            q.system.fs.moveFile(file,self.mntpoint)
                else:
                    q.logger.log("SshFS: uploading file - [%s] to [%s]" % (uploadPath,self.mntpoint))
                    q.system.fs.moveFile(uploadPath,q.system.fs.joinPaths(self.mntpoint,self.filename))
            else:
                if self.Atype == "copy":
                    if self.is_dir:
                        if self.recursive:
                            q.system.fs.copyDir(uploadPath,self.mntpoint)
                        else:
                        # walk tree and copy
                            for file in q.system.fs.walk(uploadPath, recurse=0):
                                q.logger.log("SshFS: uploading directory -  Copying file [%s] to path [%s]" % (file,self.mntpoint))
                                q.system.fs.copyFile(file,self.mntpoint)
                    else:
                        q.logger.log("SshFS: uploading file - [%s] to [%s]" % (uploadPath,self.mntpoint))
                        q.system.fs.copyFile(uploadPath,q.system.fs.joinPaths(self.mntpoint,self.filename))
 
        def download(self):
            """
            Download file
            """
            self. _connect()
            if self.is_dir:
                q.logger.log("SshFS: downloading from [%s]" % self.mntpoint)
                return self.mntpoint
            else:
                pathname =  q.system.fs.joinPaths(self.mntpoint,self.filename)
                q.logger.log("SshFS: downloading from [%s]" % pathname)
                return pathname

        def cleanup(self):
            """
            Umount sshfs share
            """
            q.logger.log("SshFS: cleaning up and umounting share")
            command = "umount %s" % self.mntpoint

            exitCode, output = q.system.process.execute(command,dieOnNonZeroExitCode=False, outputToStdout=False)
            if not exitCode == 0:
                raise RuntimeError('Failed to execute command %s'%command)

            q.system.fs.removeDir(self.mntpoint)
            self.is_mounted = False

        def list(self):
            """
            List content of directory
            """
            self._connect()
            os.chdir(self.mntpoint)
            if self.path_components:
                if len(self.path_components) > 1:
                    os.chdir('/' + '/'.join(self.path_components[:-1]))
                    if os.path.isdir(self.path_components[-1]):
                        os.chdir(self.path_components[-1])
                    else:
                        raise RuntimeError('%s is not a valid directory under %s' %('/'.join(self.path_components),self.sharename))
                if os.path.isdir(self.path_components[0]):
                    os.chdir(self.path_components[0])

            flist = q.system.fs.walk(os.curdir,return_folders=1,return_files=1)
            os.chdir(self.curdir)
            q.logger.log("list: Returning content of SSH Mount [%s] which is tmp mounted under [%s]" % (self.share , self.mntpoint))
            
            return flist
        def __del__(self):
            if self.is_mounted:
                q.logger.log('SshFS GC') 
                self.cleanup()
            os.chdir(self.curdir)
