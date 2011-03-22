#!/usr/bin/env python

#    Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

from pylabs.InitBase import *
from pylabs.Shell import *
from PysyncWalker import *
from VirtualFileSystemMetadata import *
import fnmatch

#
q.application.appname = "VFSTestMetadata"
q.application.start()

q.logger.maxlevel=6 
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True



import os, sys
from errno import *
from stat import *
import fcntl

import fuse
from fuse import Fuse


if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

# We use a custom file class
fuse.feature_assert('stateful_files', 'has_init')

class VFSStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

def flag2mode(flags):
    md = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
    m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]
    if flags | os.O_APPEND:
        m = m.replace('w', 'a', 1)
    return m


class Xmp(Fuse):

    def __init__(self, *args, **kw):

        Fuse.__init__(self, *args, **kw)

        # do stuff to set up your filesystem here, if you want
        #import thread
        #thread.start_new_thread(self.mythread, ())
        q.logger.log(args)
        q.logger.log(kw)
        self.root = '/tmp/fuse/'

#    def mythread(self):
#
#        """
#        The beauty of the FUSE python implementation is that with the python interp
#        running in foreground, you can have threads
#        """
#        print "mythread: started"
#        while 1:
#            time.sleep(120)
#            print "mythread: ticking"
    def _findPath(self, path):
        '''
        raise NoEntryError if path doesn't correspond for a dir or a file
        return isDir, DirObject(path is isDie, otherwise parent dir of file), dict {'filename':name, 'filestat':stat, 'dirstat':stat}
        '''
        isDir, dirObject, info = False, None, {'filename' : None, 'filestat' : -ENOENT, 'dirstat' : None}
        st = VFSStat()
        q.logger.log('_findPath(%s)'%path)
        #how to handle files, while the VFS holds only size?
        try:
            dirObject = self.vfs.dirObjectGet(path[1:])
            st.st_mode = S_IFDIR | 0777
            st.st_nlink = 2
            st.st_mtime = dirObject.moddate
            st.st_atime = dirObject.accessdate
            isDir = True
            info['dirstat'] = st
        except NoEntryError, ex:      
            #assume the path is file path and get its parent folder
            parentPath = os.path.dirname(path)
            fileName = q.system.fs.getBaseName(path)
            q.logger.log('No dir found with name: %s, looking for files with name: %s under dir: %s'%(path[1:], fileName, parentPath[1:]))
            try:
                dirObject = self.vfs.dirObjectGet(parentPath[1:])
                q.logger.log('DEBUG: files under %s: %s'%(parentPath, dirObject.files))
                if fileName in dirObject.files:
                    q.logger.log('Found file with name: %s under dir: %s'%(path[1:], parentPath[1:]))
                    st.st_mode = S_IFREG | 0666
                    st.st_nlink = 1
                    st.st_size = dirObject.files[fileName][0]
                    st.st_mtime = dirObject.files[fileName][1]
                    info['filename'] = fileName
                    info['filestat'] = st
            except NoEntryError, ex:
                q.logger.log('No file found with name: %s under dir: %s'%(fileName, parentPath[1:]))
                raise
        return isDir, dirObject, info
    
    def getattr(self, path):
        q.logger.log('getattr(%s)'%path)
        ret = -ENOENT
        try:
            isDir, dirObject, info = self._findPath(path)
            ret = info['dirstat'] if isDir else info['filestat'] 
        except NoEntryError, ex:
            pass
        q.logger.log('getattr return: %s'%(ret if isinstance(ret, int) else ret.__dict__))
        return ret

    def readlink(self, path):
        q.logger.log('readling(%s)%'%(path))

    def readdir(self, path, offset):
        q.logger.log("readdir(%s, %s)" % (path, offset))
        try:
            dirObject = self.vfs.dirObjectGet(path[1:])
            entries = dirObject.dirs + dirObject.files.keys()
            for entry in sorted(entries):
                q.logger.log("direntry %s" % entry)
                yield fuse.Direntry(entry)
        except NoEntryError, ex:  
            q.logger.log(ex)

    def unlink(self, path):
        q.logger.log('unlink(%s)'%(path))
    
    def rmdir(self, path):
        q.logger.log('rmdir(%s)%'%(path))
    
    
    def symlink(self, path, path1):
        q.logger.log('symlink(%s, %s)%'%(path, path1))
    
    def rename(self, path, path1):
        q.logger.log('rename(%s, %s)%'%(path, path1))
    
    def link(self, path, path1):
        q.logger.log('link(%s, %s)%'%(path, path1))

    def chmod(self, path, mode):
        q.logger.log('chmod(%s, %s)%'%(path, mode))

    def chown(self, path, user, group):
        q.logger.log('chown(%s, %s, %s)%'%(path, user, group))

    def truncate(self, path, len):
        q.logger.log('truncate(%s, %s)%'%(path, len))

    def mknod(self, path, mode, dev):
        q.logger.log('mknod(%s, %s, %s)'%(path, mode, dev))
        self.create(path, mode, dev)
        
    def create(self, path, flags, *mode):
        q.logger.log('create(%s, %s, %s)'%(path, flags, mode))
        q.logger.log('creating new file entry: %s'%path)
        parentPath = os.path.dirname(path) #q.system.fs.getDirName returns double /
        parentDirObject = None
        try:
            q.logger.log('DEBUG vfs.dirObjectGet(%s)'%parentPath[1:])
            parentDirObject = self.vfs.dirObjectGet(parentPath[1:])
            q.logger.log('DEBUG parent dir found %s'%parentPath[1:])
            parentDirObject.addFileObject(path[1:], 0, q.base.time.getTimeEpoch(), '')
            self.vfs.dirObjects.save(parentDirObject)
        except NoEntryError, ex:
            q.logger.log('DEBUG parent dir not found %s'%parentPath[1:])    

    def read(self, path, length, offset, *args):
        fileObj = args[0] if args else None
        q.logger.log('XMP: read(%s, %s, %s, %s)'%(path, length, offset, fileObj))
        data = '01234567890012345678900123456789001234567890012345678900123456789001234567890012345678900123456789001234567890'
        return 'A'*length

    def mkdir(self, path, mode):
        q.logger.log('mkdir(%s, %s)'%(path, mode))
    
    def utime(self, path, times):
        atime, mtime = times
        try:
            isDir, dirObject, info = self._findPath(path)
        except NoEntryError, ex:
            return -ENOENT
        if isDir:
            dirObject.moddate = mtime
            dirObject.accessdate = atime
            self.vfs.dirObjects.save(dirObject)
        else:
            size, moddate, md5hash = dirObject.files[info['filename']] 
            dirObject.files[info['filename']] = size, mtime, md5hash
            self.vfs.dirObjects.save(dirObject)
        

#    The following utimens method would do the same as the above utime method.
#    We can't make it better though as the Python stdlib doesn't know of
#    subsecond preciseness in acces/modify times.
#  
#    def utimens(self, path, ts_acc, ts_mod):
#      os.utime("." + path, (ts_acc.tv_sec, ts_mod.tv_sec))

    def access(self, path, mode):
        q.logger.log('access(%s, %s)%'%(path, mode))

#    This is how we could add stub extended attribute handlers...
#    (We can't have ones which aptly delegate requests to the underlying fs
#    because Python lacks a standard xattr interface.)
#
#    def getxattr(self, path, name, size):
#        val = name.swapcase() + '@' + path
#        if size == 0:
#            # We are asked for size of the value.
#            return len(val)
#        return val
#
#    def listxattr(self, path, size):
#        # We use the "user" namespace to please XFS utils
#        aa = ["user." + a for a in ("foo", "bar")]
#        if size == 0:
#            # We are asked for size of the attr list, ie. joint size of attrs
#            # plus null separators.
#            return len("".join(aa)) + len(aa)
#        return aa

    def statfs(self):
        """
        Should return an object with statvfs attributes (f_bsize, f_frsize...).
        Eg., the return value of os.statvfs() is such a thing (since py 2.2).
        If you are not reusing an existing statvfs object, start with
        fuse.StatVFS(), and define the attributes.

        To provide usable information (ie., you want sensible df(1)
        output, you are suggested to specify the following attributes:

            - f_bsize - preferred size of file blocks, in bytes
            - f_frsize - fundamental size of file blcoks, in bytes
                [if you have no idea, use the same as blocksize]
            - f_blocks - total number of blocks in the filesystem
            - f_bfree - number of free blocks
            - f_files - total number of file inodes
            - f_ffree - nunber of free file inodes
        """
        q.logger.log('statfs')

    def fsinit(self):
        self.vfs=VirtualFileSystemMetadata(self.root,"/opt/qbase5/var/log")  #scan log dir and create metadata store for it
        self.vfs.reset()
        self.vfs.populateFromFilesystem()        
        self.vfs.getLatest()
        
        
    def XmpFileFactory(self, path, flags, *mode):
        q.logger.log('File Factory (%s, %s, %s)'%(path, flags, mode))
        Xmp.XmpFile.vfs = self.vfs #set the vfs ref on class level since it's required too early during __init__
        return Xmp.XmpFile(path, flags, *mode)
        
    class XmpFile(object):

        def __init__(self, path, flags, *mode):
            #look for file and get path from elsewhere
            q.logger.log('file_class init')
            self._accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR | os.O_APPEND
            st = VFSStat()
            st.st_mode = S_IFREG | 0666
            st.st_nlink = 1
            st.st_size = 0
            self._stat = st
            self.path = path
            self.mode = mode
            
        def open(self, path, flags):
            q.logger.log('open(%s, %s, %s)'%(path, flags))
            #self._stat.st_mtime = q.base.time.getTimeEpoch()
            parentPath = os.path.dirname(path) #q.system.fs.getDirName returns double /
            self.parentDirObject = None
            self.fileName = q.system.fs.getBaseName(path)
            try:
                q.logger.log('DEBUG vfs.dirObjectGet(%s)'%parentPath[1:])
                self.parentDirObject = self.vfs.dirObjectGet(parentPath[1:])
                q.logger.log('DEBUG parent dir found %s'%parentPath[1:])
                if self.fileName in self.parentDirObject.files:
                    self._stat.st_size = self.parentDirObject.files[self.fileName][0]
                    self._stat.st_mtime = self.parentDirObject.files[self.fileName][1]
                else:
                    return -ENOENT
            except NoEntryError, ex:
                q.logger.log(ex)
                return -ENOENT
            
            q.logger.log('files: %s'%self.vfs.dirObjectGet(parentPath[1:]).files)
            self.fd = hash(path) #might come handy later, otherwise will be removed

        def read(self, length, offset):
            q.logger.log('XmpFile:read(%s, %s)'%(length, offset))
            data = '01234567890012345678900123456789001234567890012345678900123456789001234567890012345678900123456789001234567890'
            slen = len(data)
            if offset < slen:
                if offset + length > slen:
                    size = slen - offset
                buf = data[offset:offset+size]
            else:
                buf = ''
            return buf

        def write(self, buf, offset):
            q.logger.log('write(%s, %s)%'%(buf, offset))
            return len(buf)
        
        def release(self, flags):
            q.logger.log('release(%s)%'%(flags))

        def _fflush(self):
#            if 'w' in self.file.mode or 'a' in self.file.mode:
#                self.file.flush()
            pass

        def fsync(self, isfsyncfile):
#            self._fflush()
#            if isfsyncfile and hasattr(os, 'fdatasync'):
#                os.fdatasync(self.fd)
#            else:
#                os.fsync(self.fd)
            q.logger.log('fsync(%s)%'%(isfsyncfile))

        def flush(self):
#            self._fflush()
#            # cf. xmp_flush() in fusexmp_fh.c
#            os.close(os.dup(self.fd))
            q.logger.log('flush()')

        def fgetattr(self):
            q.logger.log('fgetattr()')
            return self._stat

        def ftruncate(self, len):
            q.logger.log('ftruncate(%s)%'%(len))
        
        def lock(self, cmd, owner, **kw):
            # The code here is much rather just a demonstration of the locking
            # API than something which actually was seen to be useful.

            # Advisory file locking is pretty messy in Unix, and the Python
            # interface to this doesn't make it better.
            # We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
            # way. The following implementation *might* work under Linux. 
            #
            # if cmd == fcntl.F_GETLK:
            #     import struct
            # 
            #     lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
            #                            kw['l_start'], kw['l_len'], kw['l_pid'])
            #     ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
            #     flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
            #     uld2 = struct.unpack('hhQQi', ld2)
            #     res = {}
            #     for i in xrange(len(uld2)):
            #          res[flockfields[i]] = uld2[i]
            #  
            #     return fuse.Flock(**res)

            # Convert fcntl-ish lock parameters to Python's weird
            # lockf(3)/flock(2) medley locking API...
            op = { fcntl.F_UNLCK : fcntl.LOCK_UN,
                   fcntl.F_RDLCK : fcntl.LOCK_SH,
                   fcntl.F_WRLCK : fcntl.LOCK_EX }[kw['l_type']]
            if cmd == fcntl.F_GETLK:
                return -EOPNOTSUPP
            elif cmd == fcntl.F_SETLK:
                if op != fcntl.LOCK_UN:
                    op |= fcntl.LOCK_NB
            elif cmd == fcntl.F_SETLKW:
                pass
            else:
                return -EINVAL

            fcntl.lockf(self.fd, op, kw['l_start'], kw['l_len'])



def main():

    usage = """
Userspace nullfs-alike: mirror the filesystem tree from some point on.

""" + Fuse.fusage

    server = Xmp(dash_s_do='setsingle', version="%prog " + fuse.__version__, usage=usage)

#    server.parser.add_option(mountopt="root", metavar="PATH", default='/opt/qbase5/dir1', help="mirror filesystem from under PATH [default: %default]")
    server.parse(errex=1)
    server.multithreaded = 0
    server.fuse_args.fuse_modifiers["foreground"]=True
    try:
        if server.fuse_args.mount_expected():
            os.chdir(server.root)
    except OSError:
        print >> sys.stderr, "can't enter root of underlying filesystem"
        sys.exit(1)

    #ipshell()
#    server.file_class = server.XmpFileFactory
    server.main()
    q.logger.log('Fuse system mounted successfuly, loading vfs metadata ...')
    metadatapath= "/opt/qbase5/var/vfs/var_log/"
    vfs=VirtualFileSystemMetadata(metadatapath,"/opt/qbase5/var/log")  #scan log dir and create metadata store for it
    vfs.reset()
    vfs.populateFromFilesystem()        
    vfs.getLatest()

    #ipshell()

    

if __name__ == '__main__':
    main()

q.application.stop()
