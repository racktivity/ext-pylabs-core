#!/usr/bin/env python

# -------------------------------------------------------------------
# Copyright (c) 2009 Matt Giuca
# This software and its accompanying documentation is licensed under the
# MIT License.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -------------------------------------------------------------------

# MemFS - A Simple Python Fuse Example
# An example of a real file system, implemented from TemplateFS.
# A simple memory-mapped file system. (The contents are stored in Python data
# structures, and lost when the system is unmounted).
#
# Usage:
#     memfs.py MOUNTPOINT
# To unmount:
#     fusermount -u MOUNTPOINT
#
# Use `tail -f LOG` to read the log in real-time (as it is written).
# Also, mount with `./memfs.py MOUNTPOINT -d` to have FUSE print out its own
# debugging messages (which are in some cases more, and some cases less useful
# than mine).

import fuse

import os
import stat
import errno
import datetime
import time
import calendar

from pylabs.InitBase import *
from pylabs.Shell import *
from VFSMetadata import *
from infomodel.infomodel import DirNode, FileNode
import functools

# FUSE version at the time of writing. Be compatible with this version.
fuse.fuse_python_api = (0, 2)

# First, we define a class deriving from fuse.Stat. This object is used to
# describe a file in our virtual file system.
# This class is rather large, but the concept is really simple (there's just a
# lot of code here to make construction really easy).
# All you have to do is present an object with the following fields, all ints:
#   st_mode:
#       Should be stat.S_IFREG or S_IFDIR OR'd with a normal Unix permission
#       flag, such as 644.
#   st_ino, st_dev:
#       0. Ignored, but required.
#   st_nlink:
#       Number of hard links to this file. For files, usually 1. For
#       directories, usually 2 + number of immediate subdirs (one for parent,
#       one for self, one for each child).
#   st_uid, st_gid:
#       uid/gid of file owner.
#   st_size:
#       File size in bytes.
#   st_atime, st_mtime, st_ctime:
#       File access times, in seconds since the epoch, UTC time. Last access
#       time, modification time, stat change time, respectively.


class debug_log(object):
    def __init__(self, f):
        self.f = f
        self.__doc__ = f.__doc__
    def __call__(self, *args, **kwargs):
        try:
            q.logger.log('#DEBUG: %s(%s, %s)'%(self.f.__name__, args, kwargs))
            ret = self.f(*args, **kwargs)
            q.logger.log('#DEBUG: %s returned successfully with value: %s'%(self.f.__name__, ret))
            return ret
        except Exception, ex:
            q.logger.log('#DEBUG: %s failed with Exception %s'%(self.f.__name__, ex))
            raise
    def __get__(self, obj, objtype):
        #support decoration of instance methods
        return functools.partial(self.__call__, obj)  
          
class Stat(fuse.Stat):
    """
    A Stat object. Describes the attributes of a file or directory.
    Has all the st_* attributes, as well as dt_atime, dt_mtime and dt_ctime,
    which are datetime.datetime versions of st_*time. The st_*time versions
    are in epoch time.
    """
    # Filesize of directories, in bytes.
    DIRSIZE = 4096

    # We can define __init__ however we like, because it's only called by us.
    # But it has to have certain fields.
    def __init__(self, st_mode, st_size, st_nlink=1, st_uid=None, st_gid=None,
            dt_atime=None, dt_mtime=None, dt_ctime=None):
        """
        Creates a Stat object.
        st_mode: Required. Should be stat.S_IFREG or stat.S_IFDIR ORed with a
            regular Unix permission value like 0644.
        st_size: Required. Size of file in bytes. For a directory, should be
            Stat.DIRSIZE.
        st_nlink: Number of hard-links to the file. Regular files should
            usually be 1 (default). Directories should usually be 2 + number
            of immediate subdirs (one from the parent, one from self, one from
            each child).
        st_uid, st_gid: uid/gid of file owner. Defaults to the user who
            mounted the file system.
        st_atime, st_mtime, st_ctime: atime/mtime/ctime of file.
            (Access time, modification time, stat change time).
            These must be datetime.datetime objects, in UTC time.
            All three values default to the current time.
        """
        self.st_mode = st_mode
        self.st_ino = 0         # Ignored, but required
        self.st_dev = 0         # Ignored, but required
        # Note: Wiki says st_blksize is required (like st_dev, ignored but
        # required). However, this breaks things and another tutorial I found
        # did not have this field.
        self.st_nlink = st_nlink
        if st_uid is None:
            st_uid = os.getuid()
        self.st_uid = st_uid
        if st_gid is None:
            st_gid = os.getgid()
        self.st_gid = st_gid
        self.st_size = st_size
        now = datetime.datetime.utcnow()
        self.dt_atime = dt_atime or now
        self.dt_mtime = dt_mtime or now
        self.dt_ctime = dt_ctime or now

    def __repr__(self):
        return ("<Stat st_mode %s, st_nlink %s, st_uid %s, st_gid %s, "
            "st_size %s>" % (self.st_mode, self.st_nlink, self.st_uid,
            self.st_gid, self.st_size))

    def _get_dt_atime(self):
        return self.epoch_datetime(self.st_atime)
    def _set_dt_atime(self, value):
        self.st_atime = self.datetime_epoch(value)
    dt_atime = property(_get_dt_atime, _set_dt_atime)

    def _get_dt_mtime(self):
        return self.epoch_datetime(self.st_mtime)
    def _set_dt_mtime(self, value):
        self.st_mtime = self.datetime_epoch(value)
    dt_mtime = property(_get_dt_mtime, _set_dt_mtime)

    def _get_dt_ctime(self):
        return self.epoch_datetime(self.st_ctime)
    def _set_dt_ctime(self, value):
        self.st_ctime = self.datetime_epoch(value)
    dt_ctime = property(_get_dt_ctime, _set_dt_ctime)

    @staticmethod
    def datetime_epoch(dt):
        """
        Converts a datetime.datetime object which is in UTC time
        (as returned by datetime.datetime.utcnow()) into an int, which represents
        the number of seconds since the system epoch (also in UTC time).
        """
        # datetime.datetime.timetuple converts a datetime into a time.struct_time.
        # calendar.timegm converts a time.struct_time into epoch time, without
        # modifying for time zone (so UTC time stays in UTC time, unlike
        # time.mktime).
        return calendar.timegm(dt.timetuple())
    @staticmethod
    def epoch_datetime(seconds):
        """
        Converts an int, the number of seconds since the system epoch in UTC
        time, into a datetime.datetime object, also in UTC time.
        """
        return datetime.datetime.utcfromtimestamp(seconds)

    def set_times_to_now(self, atime=False, mtime=False, ctime=False):
        """
        Sets one or more of atime, mtime and ctime to the current time.
        atime, mtime, ctime: All booleans. If True, this value is updated.
        """
        now = datetime.datetime.utcnow()
        if atime:
            self.dt_atime = now
        if mtime:
            self.dt_mtime = now
        if ctime:
            self.dt_ctime = now

    def check_permission(self, uid, gid, flags):
        """
        Checks the permission of a uid:gid with given flags.
        Returns True for allowed, False for denied.
        flags: As described in man 2 access (Linux Programmer's Manual).
            Either os.F_OK (test for existence of file), or ORing of
            os.R_OK, os.W_OK, os.X_OK (test if file is readable, writable and
            executable, respectively. Must pass all tests).
        """
        if flags == os.F_OK:
            return True
        user = (self.st_mode & 0700) >> 6
        group = (self.st_mode & 070) >> 3
        other = self.st_mode & 07
        if uid == self.st_uid:
            # Use "user" permissions
            mode = user | group | other
        elif gid == self.st_gid:
            # Use "group" permissions
            # XXX This will only check the user's primary group. Don't we need
            # to check all the groups this user is in?
            mode = group | other
        else:
            # Use "other" permissions
            mode = other
        if flags & os.R_OK:
            if mode & os.R_OK == 0:
                return False
        if flags & os.W_OK:
            if mode & os.W_OK == 0:
                return False
        if flags & os.X_OK:
            if uid == 0:
                # Root has special privileges. May execute if anyone can.
                if mode & 0111 == 0:
                    return False
            else:
                if mode & os.X_OK == 0:
                    return False
        return True

class FSObject(object):
    """
    A file system object (subclasses are File and Dir).
    Attributes:
        name: str
        stat: Stat
        parent: Dir or None
    """
    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self.name)

class Dir(FSObject):
    """
    A directory. May contain child directories and files.
    Attributes:
        name: str
        stat: Stat
        files: dict mapping str names to File and Dir objects.
    """
    def __init__(self, name, mode, uid, gid, parent=None, path=None):
        """
        Create a new directory object.
        """
        self.name = name
        self.path = path
        self.stat = Stat(mode, Stat.DIRSIZE, st_nlink=2, st_uid=uid,
            st_gid=gid)
#        self.files = {}
        self.parent = parent
        self.path = q.system.fs.joinPaths(self.parent.path, self.name) if parent else self.path
        self.files = DirChildrenProxy(self)        
        
    def __str__(self):
        return "<%s %s>" % (type(self).__name__, self.path)
    
    __repr__ = __str__
        
class FileDataProxy(object):
    """A data descriptor that acts as well as a sequence
    """
    @debug_log
    def __init__(self):
        pass

    @debug_log
    def __get__(self, obj, objtype):
        #@todo call findPath in vfs and get the the key of file data in object store
        self.file = obj
        self.vfs = self.file.vfs
        self.store = self.vfs.dirObjectStore
        self.dirObject, self.fileNode = self.findFile(self.file.path)
#        self.datakey = vfs.findPath(obj.name).datakey
        return self
    
#    @debug_log
    def __set__(self, obj, val):
        self.file = obj
        self.fileData = val
    
    @debug_log            
    def __len__(self):
        return len(self.fileData)
    @debug_log
    def __getitem__(self, idx):
        #@todo use the key to the file data to retrieve data from object store, handle numerical and slice indexes
        return self.fileData[idx]
    @debug_log
    def __setitem__(self, idx, val):
        #@todo update the data corresponding to the key
        raise NotImplementedError('cannot assign')
    
    def __add__(self, val):
        return self.fileData + val
    
    def _setFileData(self, fileData):
        dataKey = self.store.getKey(q.system.fs.joinPaths('DATA', self.file.path))
        self.dirObject.files[self.file.name].dataKey = dataKey
        if len(fileData) < 1048576:
            self.store.putFileData(dataKey, fileData)
        else:
            self.store.delete(dataKey)
            versionPrefix = self.store._getDBCat()
            path = q.system.fs.joinPaths(self.vfs.localFileStore, versionPrefix, self.file.path)
            q.system.fs.writeFile(path, fileData)
        self.dirObject.files[self.file.name].size = len(fileData)
        self.store.save(self.dirObject)
        
    def _getFileData(self):
        fileData = ''
        if self.dirObject.files[self.file.name].size < 1048576:
            try:
                dataKey = self.store.getKey(q.system.fs.joinPaths('DATA', self.file.path))
                fileData = self.store.getFileData(dataKey)
            except RuntimeError, ex: #q.db.get throws a RuntimeError if the key is not found 
                q.logger.log(ex)
        else:
            try:
                dataKey = self.store.getKey(q.system.fs.joinPaths('DATA', self.file.path))
                filePath = self._keyToPath(dataKey)
                versionPrefix = self.store._getDBCat()
                path = q.system.fs.joinPaths(self.vfs.localFileStore, versionPrefix, filePath)
                fileData = q.system.fs.fileGetContents(path)
            except RuntimeError, ex:
                q.logger.log(ex)
        return fileData
    
    fileData = property(fset=_setFileData, fget=_getFileData)
    
    @debug_log
    def _keyToPath(self, dataKey):
        separator="_!_"
        path = dataKey.replace(separator, '/')
        return path[5:]
    
    @debug_log
    def findFile(self, path):
        '''
        raise NoEntryError if path doesn't correspond for a dir or a file
        return isDir, DirObject(path is isDie, otherwise parent dir of file), dict {'filename':name, 'filestat':stat, 'dirstat':stat}
        '''
        dirObject = None
        #how to handle files, while the VFS holds only size?
            #assume the path is file path and get its parent folder
        parentPath = os.path.dirname(path)
        fileName = q.system.fs.getBaseName(path)
        fileNode = None
        q.logger.log('No dir found with name: %s, looking for files with name: %s under dir: %s'%(path, fileName, parentPath))
        try:
            dirObject = self.store.get(parentPath)
            q.logger.log('DEBUG: files under %s: %s'%(parentPath, dirObject.files))
            if fileName in dirObject.files:
                q.logger.log('Found file with name: %s under dir: %s'%(path, parentPath))
                fileNode = dirObject.files[fileName]
        except NoEntryError, ex:
            q.logger.log('No file found with name: %s under dir: %s'%(fileName, parentPath))
            raise
        return dirObject, fileNode

class File(FSObject):
    """
    A non-directory file. May be a regular file, symlink, fifo, etc.
    Attributes:
        name: str
        stat: Stat
        data: byte string. Contents of the file.
            For a symlink, this is the link text.
            Do not edit manually; use provided methods.
    """
    def __init__(self, name, data, mode, uid, gid, parent=None):
        """
        Create a new file object, with the supplied contents.
        """
        self.name = name
        self.stat = Stat(mode, len(data), st_nlink=1, st_uid=uid,
            st_gid=gid)
        self.parent = parent
        self.path = q.system.fs.joinPaths(self.parent.path, self.name)
#        self.data = data

    data = FileDataProxy()
    
    def __str__(self):
        return "<%s %s>" % (type(self).__name__, self.path)
    
    __repr__ = __str__
    
#    @debug_log
    def read(self, size, offset):
        """
        Reads from a file. Returns a bytes object.
        """
        q.logger.log("data: %r" % self.data)
        q.logger.log("returned: %r" % self.data[offset:offset+size])
        # Update timestamps: read updates atime
        self.stat.set_times_to_now(atime=True)
        return self.data[offset:offset+size]
    
#    @debug_log
    def write(self, buf, offset):
        """
        Writes to the file.
        Returns the number of bytes written.
        """
        if offset < len(self.data):
            # Write over part of the file. Save the bits we want to keep.
            before = self.data[:offset]
            after = self.data[offset+len(buf):]
        else:
            if offset > len(self.data):
                # First pad the file with 0s, using truncate
                self.truncate(offset)
            before = self.data
            after = ''
        # Insert buf in between before and after
        self.data = before + buf + after
        self.stat.st_size = len(self.data)
        # Update timestamps: write updates mtime
        self.stat.set_times_to_now(mtime=True)
        return len(buf)

    @debug_log
    def truncate(self, size):
        """
        Truncates a file. Returns None.
        """
        if size < len(self.data):
            # Shrink
            self.data = self.data[:size]
            self.stat.st_size = size
        elif size > len(self.data):
            # Grow
            self.data = self.data + '\0'*(size-len(self.data))
            self.stat.st_size = size
        # Update timestamps: truncate updates mtime
        self.stat.set_times_to_now(mtime=True)


#Proxy classes to connect VFS to MemFS

class DirChildrenProxy(object):
    
    @debug_log
    def __init__(self, parent):
        self.parent = parent
        self.vfs = parent.vfs
        self.store = self.vfs.dirObjectStore
        try:
            self.dirObject = self.store.get(self.parent.path)
        except NoEntryError, ex:
            q.logger.log(ex)
            q.logger.log('#DEBUG: Directory %s not found'%self.parent.path)
            self.dirObject = self.store.new(self.parent.path, False)
            self.store.save(self.dirObject)
#    @debug_log
    def __getitem__(self, key):
        if key in self.dirObject.dirs:
            return Dir(key, mode=self.parent.stat.st_mode, uid=self.parent.stat.st_uid, gid=self.parent.stat.st_gid,
            parent=self.parent, path=self.dirObject.fullpath)
        elif key in self.dirObject.files:
            data = 'hello data' 
            #@todo consider saving mode in VFS
            return File(key, data, mode=stat.S_IFREG|0755, uid=self.parent.stat.st_uid, gid=self.parent.stat.st_gid,
            parent=self.parent)
        else:
            raise KeyError(key)
            
    @debug_log
    def __setitem__(self, key, value):
        if isinstance(value, Dir):
            self.dirObject.dirs[key] = self._dirNodeFromDir(value)
        elif isinstance(value, File):
            self.dirObject.files[key] = self._fileNodeFromFile(value)
        self.store.save(self.dirObject)
    
    @debug_log    
    def __delitem__(self, key):
        try:
            del self.dirObject.dirs[key]
        except KeyError:
            try:
                del self.dirObject.files[key]
            except KeyError:
                raise
        
        self.store.save(self.dirObject)
    
    @debug_log
    def keys(self):
        q.logger.log(self.dirObject)
        keys = sorted(self.dirObject.dirs.keys())
        keys.extend(sorted(self.dirObject.files.keys()))
        return keys
    @debug_log    
    def __len__(self):
        return len(self.dirObject.dirs) + len(self.dirObject.files)
    
    def _dirNodeFromDir(self, dir_):
        #name, mode, uid, gid, parent=None
        path = dir_.path
        return DirNode(DirNode.getKey(path), path)
    
    def _fileNodeFromFile(self, file):
        return FileNode(file.name, file.stat.st_size, file.stat.st_mtime)

# Almost all that is required is the definition of a class deriving from
# fuse.Fuse, and implementation of a bunch of methods.
class MemFS(fuse.Fuse):
    """
    A Fuse filesystem object. Implements methods which are called by the Fuse
    system as a result of the operating system requesting filesystem
    operations on places where this file system is mounted.

    Unless otherwise documented, all of these methods return an int.
    This should be 0 on success, or the NEGATIVE of an errno value on failure.
    For example, to report "no such file or directory", methods return
    -errno.ENOENT. See the errno manpage for a list of errno values. (Though
    note that Python's errno is slightly different; see help(errno)).
    Methods should return errno.EOPNOTSUPP (operation not supported) if they
    are deliberately not supported, or errno.ENOSYS (function not implemented)
    if they have not yet been implemented.

    Unless otherwise documented, all paths should begin with a '/' and be
    "absolute paths", where "absolute" means relative to the root of the
    mounted filesystem. There are no references to files outside the
    filesystem.

    Attributes:
        root_dir: Dir object
    """
    def __init__(self, *args, **kwargs):
        """
        Creates a new MemFS object. Needs to call fuse.Fuse.__init__ with the
        args (just forward them along).
        """
        q.logger.log("Mounting file system")
        q.logger.log('DEBUG: args: %s, kwargs: %s'%(args, kwargs))
        super(MemFS, self).__init__(*args, **kwargs)

    @debug_log
    def _search_path(self, path):
        """
        Given a path string, returns the Dir or File object corresponding to
        the path, or None.
        """
        if not path.startswith(os.sep):
            return None
        path = path.split(os.sep)[1:]
        # Walk the directory hierarchy
        cur_dir = self.root_dir
        for node in path:
            if node == "":
                continue
            if not isinstance(cur_dir, Dir):
                # A file - doesn't have children
                return None
            try:
                cur_dir = cur_dir.files[node]
            except KeyError:
                return None
        return cur_dir
    
    @debug_log
    def _search_new_path(self, path):
        """
        Given a path string, searches for the path but doesn't require the
        last segment to exist (as in the creation of a new file).
        Returns a pair (parent-node, name), or None.
        parent-node is the Dir or File object corresponding to the parent of
        the path node. name is the name of the final segment.
        eg. _search_new_path("/a/b/c") searches for "/a/b". If it finds it,
            returns the Dir or File object for "/a/b", and the string "c".
            If it doesn't find "/a/b", returns None.
        """
        if not path.startswith(os.sep):
            return None
        path = path.split(os.sep)[1:]
        # First get name and remove it from path
        name = None
        for i in range(len(path)-1, -1, -1):
            if path[i] != "":
                name = path[i]
                path = path[:i]
                break
        if name is None:
            return None

        # Walk the directory hierarchy
        cur_dir = self.root_dir
        for node in path:
            if node == "":
                continue
            if not isinstance(cur_dir, Dir):
                # A file - doesn't have children
                return None
            try:
                cur_dir = cur_dir.files[node]
            except KeyError:
                return None
        return cur_dir, name
    
    @debug_log
    def fsinit(self):
        """
        Will be called when the file system has finished mounting, and is
        ready to be used.
        It doesn't have to exist, or do anything.
        """
        q.logger.log("File system mounted")
        try:
            metadatapath = "/opt/qbase5/var/vfs/var_log/"
            root = "/opt/qbase5/var/log" 
            self.vfs=VFSMetadata(metadatapath, root)  #scan log dir and create metadata store for it
            self.vfs.reset()
            self.vfs.populateFromFilesystem()
            self.vfs.getLatest()
            q.logger.log('VFS initialized successfully')
        except Exception, ex:
            q.logger.log(ex)
            raise
        self.vfs.localFileStore = '/tmp/vfsFiles'
        Dir.vfs = self.vfs #injecting vfs instance to Dir class
        File.vfs = self.vfs
#        self.root_dir = Dir('/', stat.S_IFDIR|0755, os.getuid(), os.getgid())
        
        self.root_dir = Dir('', stat.S_IFDIR|0755, os.getuid(), os.getgid(), path='')
        
    @debug_log
    def fsdestroy(self):
        """
        Will be called when the file system is about to be unmounted.
        It doesn't have to exist, or do anything.
        """
        q.logger.log("Unmounting file system")

    @debug_log
    def statfs(self):
        """
        Retrieves information about the mounted filesystem.
        Returns a fuse.StatVfs object containing the details.
        This is optional. If omitted, Fuse will simply report a bunch of 0s.

        The StatVfs should have the same fields as described in man 2 statfs
        (Linux Programmer's Manual), except for f_type.
        This includes the following:
            f_bsize     (optimal transfer block size)
            f_blocks    (number of blocks total)
            f_bfree     (number of free blocks)
            f_bavail    (number of free blocks available to non-root)
            f_files     (number of file nodes in system)
            f_ffree     (number of free file nodes)
            f_namemax   (max length of filenames)

        Note f_type, f_frsize, f_favail, f_fsid and f_flag are ignored.
        """
        q.logger.log("statfs")
        stats = fuse.StatVfs()
        # Fill it in here. All fields take on a default value of 0.
        return stats

    @debug_log
    def getattr(self, path):
        """
        Retrieves information about a file (the "stat" of a file).
        Returns a fuse.Stat object containing details about the file or
        directory.
        Returns -errno.ENOENT if the file is not found, or another negative
        errno code if another error occurs.
        """
        q.logger.log("getattr: %s" % path)
        file = self._search_path(path)
        if file is None:
            return -errno.ENOENT
        return file.stat

    # Note: utime is deprecated in favour of utimens.
    @debug_log
    def utime(self, path, times):
        """
        Sets the access and modification times on a file.
        times: (atime, mtime) pair. Both ints, in seconds since epoch.
        Deprecated in favour of utimens.
        """
        atime, mtime = times
        q.logger.log("utime: %s (atime %s, mtime %s)" % (path, atime, mtime))
        file = self._search_path(path)
        if file is None:
            return -errno.ENOENT
        file.stat.st_atime = atime
        file.stat.st_mtime = mtime
        # Update timestamps: utime updates ctime
        file.stat.set_times_to_now(ctime=True)
        return 0
    @debug_log
    def access(self, path, flags):
        """
        Checks permissions for accessing a file or directory.
        flags: As described in man 2 access (Linux Programmer's Manual).
            Either os.F_OK (test for existence of file), or ORing of
            os.R_OK, os.W_OK, os.X_OK (test if file is readable, writable and
            executable, respectively. Must pass all tests).
        Should return 0 for "allowed", or -errno.EACCES if disallowed.
        May not always be called. For example, when opening a file, open may
        be called and access avoided.
        """
        q.logger.log("access: %s (flags %s)" % (path, oct(flags)))
        file = self._search_path(path)
        if file is None:
            return -errno.ENOENT
        if file.stat.check_permission(self.GetContext()['uid'],
            self.GetContext()['gid'], flags):
            return 0
        else:
            return -errno.EACCES

    @debug_log
    def readlink(self, path):
        """
        Get the target of a symlink.
        Returns a bytestring with the contents of a symlink (its target).
        May also return an int error code.
        """
        q.logger.log("readlink: %s" % path)
        return -errno.EOPNOTSUPP
    
    @debug_log
    def mknod(self, path, mode, rdev):
        """
        Creates a non-directory file (or a device node).
        mode: Unix file mode flags for the file being created.
        rdev: Special properties for creation of character or block special
            devices (I've never gotten this to work).
            Always 0 for regular files or FIFO buffers.
        """
        # Note: mode & 0770000 gives you the non-permission bits.
        # Common ones:
        # S_IFREG:  0100000 (A regular file)
        # S_IFIFO:  010000  (A fifo buffer, created with mkfifo)

        # Potential ones (I have never seen them):
        # Note that these could be made by copying special devices or sockets
        # or using mknod, but I've never gotten FUSE to pass such a request
        # along.
        # S_IFCHR:  020000  (A character special device, created with mknod)
        # S_IFBLK:  060000  (A block special device, created with mknod)
        # S_IFSOCK: 0140000 (A socket, created with mkfifo)

        # Also note: You can use self.GetContext() to get a dictionary
        #   {'uid': ?, 'gid': ?}, which tells you the uid/gid of the user
        #   executing the current syscall. This should be handy when creating
        #   new files and directories, because they should be owned by this
        #   user/group.
        q.logger.log("mknod: %s (mode %s, rdev %s)" % (path, oct(mode), rdev))
        parent, filename = self._search_new_path(path)
        if parent is None:
            return -errno.ENOENT
        if not isinstance(parent, Dir):
            return -errno.ENOTDIR
        context = self.GetContext()
        uid = context['uid']
        gid = context['gid']
        parent.files[filename] = File(filename, '', mode, uid=uid, gid=gid,
            parent=parent)
        # Update timestamps: mknod updates mtime
        parent.stat.set_times_to_now(mtime=True)
        return 0
    
    @debug_log
    def mkdir(self, path, mode):
        """
        Creates a directory.
        mode: Unix file mode flags for the directory being created.
        """
        # Note: mode & 0770000 gives you the non-permission bits.
        # Should be S_IDIR (040000); I guess you can assume this.
        # Also see note about self.GetContext() in mknod.
        q.logger.log("mkdir: %s (mode %s)" % (path, oct(mode)))
        parent, filename = self._search_new_path(path)
        if parent is None:
            return -errno.ENOENT
        if not isinstance(parent, Dir):
            return -errno.ENOTDIR
        mode |= stat.S_IFDIR
        context = self.GetContext()
        uid = context['uid']
        gid = context['gid']
        parent.files[filename] = Dir(filename, mode, uid=uid, gid=gid,
            parent=parent, path=path)
        parent.stat.st_nlink += 1
        # Update timestamps: mkdir updates mtime
        parent.stat.set_times_to_now(mtime=True)
        return 0

    def _unlink(self, fileobj):
        parent = fileobj.parent
        if parent is None:
            # Was root
            return -errno.EBUSY
        del parent.files[fileobj.name]
        # Update timestamps: mkdir updates parent's mtime
        parent.stat.set_times_to_now(mtime=True)
        return 0

    @debug_log
    def unlink(self, path):
        """Deletes a file."""
        q.logger.log("unlink: %s" % path)
        file = self._search_path(path)
        if file is None:
            return -errno.ENOENT
        return self._unlink(file)

    @debug_log
    def rmdir(self, path):
        """Deletes a directory."""
        q.logger.log("rmdir: %s" % path)
        dir_ = self._search_path(path)
        if dir_ is None:
            return -errno.ENOENT
        if not isinstance(dir_, Dir):
            return -errno.ENOTDIR
        if len(dir_.files) > 0:
            return -errno.ENOTEMPTY
        r = self._unlink(dir_)
        if r == 0:
            dir_.parent.stat.st_nlink -= 1
        return r

    @debug_log
    def symlink(self, target, name):
        """
        Creates a symbolic link from path to target.

        The 'name' is a regular path like any other method (absolute, but
        relative to the filesystem root).
        The 'target' is special - it works just like any symlink target. It
        may be absolute, in which case it is absolute on the user's system,
        NOT the mounted filesystem, or it may be relative. It should be
        treated as an opaque string - the filesystem implementation should not
        ever need to follow it (that is handled by the OS).

        Hence, if the operating system creates a link FROM this system TO
        another system, it will call this method with a target pointing
        outside the filesystem.
        If the operating system creates a link FROM some other system TO this
        system, it will not touch this system at all (symlinks do not depend
        on the target system unless followed).
        """
        q.logger.log("symlink: target %s, name: %s" % (target, name))
        return -errno.EOPNOTSUPP

    @debug_log
    def link(self, target, name):
        """
        Creates a hard link from name to target. Note that both paths are
        relative to the mounted file system. Hard-links across systems are not
        supported.
        """
        q.logger.log("link: target %s, name: %s" % (target, name))
        return -errno.EOPNOTSUPP

    @debug_log
    def rename(self, old, new):
        """
        Moves a file from old to new. (old and new are both full paths, and
        may not be in the same directory).
        
        Note that both paths are relative to the mounted file system.
        If the operating system needs to move files across systems, it will
        manually copy and delete the file, and this method will not be called.
        """
        q.logger.log("rename: target %s, name: %s" % (old, new))
        return -errno.EOPNOTSUPP
    @debug_log
    def chmod(self, path, mode):
        """Changes the mode of a file or directory."""
        q.logger.log("chmod: %s (mode %s)" % (path, oct(mode)))
        return -errno.EOPNOTSUPP
    @debug_log
    def chown(self, path, uid, gid):
        """Changes the owner of a file or directory."""
        q.logger.log("chown: %s (uid %s, gid %s)" % (path, uid, gid))
        return -errno.EOPNOTSUPP

    @debug_log
    def truncate(self, path, size):
        """
        Shrink or expand a file to a given size.
        If 'size' is smaller than the existing file size, truncate it from the
        end.
        If 'size' if larger than the existing file size, extend it with null
        bytes.
        """
        q.logger.log("truncate: %s (size %s)" % (path, size))
        file = self._search_path(path)
        if file is None:
            return -errno.ENOENT
        if not isinstance(file, File):
            return -errno.EISDIR
        file.truncate(size)
        return 0

    ### DIRECTORY OPERATION METHODS ###
    # Methods in this section are operations for opening directories and
    # working on open directories.
    # "opendir" is the method for opening directories. It *may* return an
    # arbitrary Python object (not None or int), which is used as a dir
    # handle by the methods for working on directories.
    # All the other methods (readdir, fsyncdir, releasedir) are methods for
    # working on directories. They should all be prepared to accept an
    # optional dir-handle argument, which is whatever object "opendir"
    # returned.

    @debug_log
    def opendir(self, path):
        """
        Checks permissions for listing a directory.
        This should check the 'r' (read) permission on the directory.

        On success, *may* return an arbitrary Python object, which will be
        used as the "fh" argument to all the directory operation methods on
        the directory. Or, may just return None on success.
        On failure, should return a negative errno code.
        Should return -errno.EACCES if disallowed.
        """
        q.logger.log("opendir: %s" % path)
        dir_ = self._search_path(path)
        if dir_ is None:
            return -errno.ENOENT
        if not isinstance(dir_, Dir):
            return -errno.ENOTDIR
        if dir_.stat.check_permission(self.GetContext()['uid'],
            self.GetContext()['gid'], os.R_OK):
            return dir_
        else:
            return -errno.EACCES

    @debug_log
    def releasedir(self, path, dh):
        """
        Closes an open directory. Allows filesystem to clean up.
        """
        q.logger.log("releasedir: %s (dh %s)" % (path, dh))

    @debug_log
    def fsyncdir(self, path, datasync, dh):
        """
        Synchronises an open directory.
        datasync: If True, only flush user data, not metadata.
        """
        q.logger.log("fsyncdir: %s (datasync %s, dh %s)"
            % (path, datasync, dh))

    @debug_log
    def readdir(self, path, offset, dh):
        """
        Generator function. Produces a directory listing.
        Yields individual fuse.Direntry objects, one per file in the
        directory. Should always yield at least "." and "..".
        Should yield nothing if the file is not a directory or does not exist.
        (Does not need to raise an error).

        offset: I don't know what this does, but I think it allows the OS to
        request starting the listing partway through (which I clearly don't
        yet support). Seems to always be 0 anyway.
        """
        q.logger.log("readdir: %s (offset %s, dh %s)" % (path, offset, dh))
        # Update timestamps: readdir updates atime
        dh.stat.set_times_to_now(atime=True)
        yield fuse.Direntry(".")
        yield fuse.Direntry("..")
        for f in dh.files.keys():
            yield fuse.Direntry(f)

    ### FILE OPERATION METHODS ###
    # Methods in this section are operations for opening files and working on
    # open files.
    # "open" and "create" are methods for opening files. They *may* return an
    # arbitrary Python object (not None or int), which is used as a file
    # handle by the methods for working on files.
    # All the other methods (fgetattr, release, read, write, fsync, flush,
    # ftruncate and lock) are methods for working on files. They should all be
    # prepared to accept an optional file-handle argument, which is whatever
    # object "open" or "create" returned.

    @debug_log
    def open(self, path, flags):
        """
        Open a file for reading/writing, and check permissions.
        flags: As described in man 2 open (Linux Programmer's Manual).
            ORing of several access flags, including one of os.O_RDONLY,
            os.O_WRONLY or os.O_RDWR. All other flags are in os as well.

        On success, *may* return an arbitrary Python object, which will be
        used as the "fh" argument to all the file operation methods on the
        file. Or, may just return None on success.
        On failure, should return a negative errno code.
        Should return -errno.EACCES if disallowed.
        """
        q.logger.log("open: %s (flags %s)" % (path, oct(flags)))
        file = self._search_path(path)
        if file is None:
            return -errno.ENOENT
        if not isinstance(file, File):
            return -errno.EISDIR
        accessflags = 0
        if flags & os.O_RDONLY:
            accessflags |= os.R_OK
        if flags & os.O_WRONLY:
            accessflags |= os.W_OK
        if flags & os.O_RDWR:
            accessflags |= os.R_OK | os.W_OK
        if file.stat.check_permission(self.GetContext()['uid'],
            self.GetContext()['gid'], accessflags):
            return file
        else:
            return -errno.EACCES
    @debug_log
    def fgetattr(self, path, fh):
        """
        Retrieves information about a file (the "stat" of a file).
        Same as Fuse.getattr, but may be given a file handle to an open file,
        so it can use that instead of having to look up the path.
        """
        q.logger.log("fgetattr: %s (fh %s)" % (path, fh))
        return fh.stat

    @debug_log
    def release(self, path, flags, fh):
        """
        Closes an open file. Allows filesystem to clean up.
        flags: The same flags the file was opened with (see open).
        """
        q.logger.log("release: %s (flags %s, fh %s)" % (path, oct(flags), fh))

    @debug_log
    def fsync(self, path, datasync, fh):
        """
        Synchronises an open file.
        datasync: If True, only flush user data, not metadata.
        """
        q.logger.log("fsync: %s (datasync %s, fh %s)" % (path, datasync, fh))
        
    @debug_log
    def flush(self, path, fh):
        """
        Flush cached data to the file system.
        This is NOT an fsync (I think the difference is fsync goes both ways,
        while flush is just one-way).
        """
        q.logger.log("flush: %s (fh %s)" % (path, fh))

    @debug_log
    def read(self, path, size, offset, fh):
        """
        Get all or part of the contents of a file.
        size: Size in bytes to read.
        offset: Offset in bytes from the start of the file to read from.
        Does not need to check access rights (operating system will always
        call access or open first).
        Returns a byte string with the contents of the file, with a length no
        greater than 'size'. May also return an int error code.

        If the length of the returned string is 0, it indicates the end of the
        file, and the OS will not request any more. If the length is nonzero,
        the OS may request more bytes later.
        To signal that it is NOT the end of file, but no bytes are presently
        available (and it is a non-blocking read), return -errno.EAGAIN.
        If it is a blocking read, just block until ready.
        """
        q.logger.log("read: %s (size %s, offset %s, fh %s)"
            % (path, size, offset, fh))
        return fh.read(size, offset)

    @debug_log
    def write(self, path, buf, offset, fh):
        """
        Write over part of a file.
        buf: Byte string containing the text to write.
        offset: Offset in bytes from the start of the file to write to.
        Does not need to check access rights (operating system will always
        call access or open first).
        Should only overwrite the part of the file from offset to
        offset+len(buf).

        Must return an int: the number of bytes successfully written (should
        be equal to len(buf) unless an error occured). May also be a negative
        int, which is an errno code.
        """
#        q.logger.log("write: %s (offset %s, fh %s)" % (path, offset, fh))
#        q.logger.log("  buf: %r" % buf)
        return fh.write(buf, offset)

    @debug_log
    def ftruncate(self, path, size, fh):
        """
        Shrink or expand a file to a given size.
        Same as Fuse.truncate, but may be given a file handle to an open file,
        so it can use that instead of having to look up the path.
        """
        q.logger.log("ftruncate: %s (size %s, fh %s)" % (path, size, fh))
        fh.truncate(size)
        return 0

# Now all we need is a main function.
# Fuse modules are actual Python scripts, which are user-executable. The main
# function needs to tell Fuse to mount themselves.
def main():
    # Our custom usage message
    usage = """
    MemFS: A demo FUSE file system.
    """ + fuse.Fuse.fusage
    server = MemFS(version="%prog " + fuse.__version__,
        usage=usage, dash_s_do='setsingle')
    server.parse(errex=1)
    server.multithreaded = 0
    try:
        server.main()
    except fuse.FuseError, e:
        print str(e)

if __name__ == '__main__':
    main()

