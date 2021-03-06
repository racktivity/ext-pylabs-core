#!/usr/bin/python

#    pyHesiodFS:
#    Copyright (C) 2007  Quentin Smith <quentin@mit.edu>
#    "Hello World" pyFUSE example:
#    Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import sys, os, stat, errno
from syslog import *
import fuse
from fuse import Fuse

import hesiod

new_fuse = hasattr(fuse, '__version__')

fuse.fuse_python_api = (0, 2)

if not hasattr(fuse, 'Stat'):
    fuse.Stat = object

class MyStat(fuse.Stat):
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

    def toTuple(self):
        return (self.st_mode, self.st_ino, self.st_dev, self.st_nlink,
                self.st_uid, self.st_gid, self.st_size, self.st_atime,
                self.st_mtime, self.st_ctime)

class PyHesiodFS(Fuse):

    def __init__(self, *args, **kwargs):
        Fuse.__init__(self, *args, **kwargs)
        
        openlog('pyhesiodfs', 0, LOG_DAEMON)
        
        try:
            self.fuse_args.add("allow_other", True)
        except AttributeError:
            self.allow_other = 1

        if sys.platform == 'darwin':
            self.fuse_args.add("noappledouble", True)
            self.fuse_args.add("noapplexattr", True)
            self.fuse_args.add("volname", "MIT")
            self.fuse_args.add("fsname", "pyHesiodFS")
        self.mounts = {}
    
    def getattr(self, path):
        st = MyStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif '/' not in path[1:]:
            if self.findLocker(path[1:]):
                st.st_mode = stat.S_IFLNK | 0777
                st.st_nlink = 1
                st.st_size = len(self.findLocker(path[1:]))
            else:
                return -errno.ENOENT
        else:
            return -errno.ENOENT
        if new_fuse:
            return st
        else:
            return st.toTuple()

    def getCachedLockers(self):
        return self.mounts.keys()

    def findLocker(self, name):
        """Lookup a locker in hesiod and return its path"""
        if name in self.mounts:
            return self.mounts[name]
        else:
            try:
                filsys = hesiod.FilsysLookup(name)
            except IOError, e:
                if e.errno in (errno.ENOENT, errno.EMSGSIZE):
                    raise IOError(errno.ENOENT, os.strerror(errno.ENOENT))
                else:
                    raise IOError(errno.EIO, os.strerror(errno.EIO))
            # FIXME check if the first locker is valid
            if len(filsys.filsys) >= 1:
                pointers = filsys.filsys
                pointer = pointers[0]
                if pointer['type'] != 'AFS' and pointer['type'] != 'LOC':
                    syslog(LOG_NOTICE, "Unknown locker type "+pointer['type']+" for locker "+name+" ("+repr(pointer)+" )")
                    return None
                else:
                    self.mounts[name] = pointer['location']
                    syslog(LOG_INFO, "Mounting "+name+" on "+pointer['location'])
                    return pointer['location']
            else:
                syslog(LOG_WARNING, "Couldn't find filsys for "+name)
                return None

    def getdir(self, path):
        return [(i, 0) for i in (['.', '..'] + self.getCachedLockers())]

    def readdir(self, path, offset):
        for (r, zero) in self.getdir(path):
            yield fuse.Direntry(r)
            
    def readlink(self, path):
        return self.findLocker(path[1:])

def main():
    try:
        usage = Fuse.fusage
        server = PyHesiodFS(version="%prog " + fuse.__version__,
                            usage=usage,
                            dash_s_do='setsingle')
        server.parse(errex=1)
    except AttributeError:
        usage="""
pyHesiodFS [mountpath] [options]

"""
        if sys.argv[1] == '-f':
            sys.argv.pop(1)
        server = PyHesiodFS()

    server.main()

if __name__ == '__main__':
    main()
