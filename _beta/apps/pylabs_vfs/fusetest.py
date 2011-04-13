#!/usr/bin/env python

import fuse


fuse.fuse_python_api = (0, 2)

from fuse import Fuse
import os
from errno import *
from stat import *
import os
import sys
import re
import glob

count_id = 0;

#import CompatMysqldb
import types 

index_dir="/opt/qbase5/dir1"
logfile='/opt/qbase5/dir1/log.log'
indexer = 0
db_glob = 0
db = 0
#FUSE_PYTHON_API=0.1
def stripnulls(data):
    "strip whitespace and nulls"
    return data.replace("\00", "").strip()


class Psfs(Fuse):
    
    flags = 1
    index_var = 0;

    def __init__(self, *args, **kw):
        #self.logfile = open(logfile,'a')
        self.log('Starting')
        Fuse.__init__(self, *args, **kw)
        self.root = index_dir

    def p(self,path):
        return index_dir+path

    def log(self,message):
        l = open(logfile,'a')
        l.write(message+'\n')
        l.close()
        pass

    def getattr(self, path):
        #self.log("getattr " +path)
        return os.lstat(self.p(path))

    def readlink(self, path):
        #self.log("readlink "+path)
        return os.readlink(self.p(path))

    def getdir(self, path):
        #self.log("getdir " + path)
        return map(lambda x: (x,0), os.listdir(path))

    def unlink(self, path):
        self.log("unlink " + path)
        return os.unlink(self.p(path))

    def readdir(self, path, offset):
        #self.log('listing ' + path)
        for e in os.listdir("." + self.p(path)):
            yield fuse.Direntry(e)

    def rmdir(self, path):
        self.log("rmdir " + path)
        return os.rmdir(self.p(path))

    def symlink(self, path, path1):
        if not path.startswith('/'):
            path = '/'+path
        self.log("symlink %s %s" % (path,path1))
        return os.symlink(self.p(path), self.p(path1))

    def rename(self, path, path1):
        self.log("rename %s %s" % (path,path1))
        return os.symlink(self.p(path), self.p(path1))

    def link(self, path, path1):
        self.log("link %s %s" % (path,path1))
        return os.link(self.p(path), self.p(path1))

    def chmod(self, path, mode):
        self.log("chmod %s %s" % (path,mode))
        return os.chmod(self.p(path), mode)

    def chown(self, path, user, group):
        self.log("chown %s %s %s" % (path,user,group))
        return os.chown(self.p(path), user, group)

    def truncate(self, path, size):
        self.log("truncate %s %s" % (path,size))
        f = open(self.p(path), "w+")
        aux = f.truncate(size)
        return aux

    def mknod(self, path, mode, dev):
        """ Python has no os.mknod, so we can only do some things """
        self.log("mknod %s %s %s" %(path,mode,dev))
        if S_ISREG(mode):
            open(self.p(path), "w")
        else:
            return -EINVAL

    def mkdir(self, path, mode):
        self.log("mkdir %s %s" %(path,mode))
        return os.mkdir(self.p(path), mode)

    def utime(self, path, times):
        self.log("utime %s %s" % (path,times))
        return os.utime(self.p(path), times)

    def open(self, path, flags):
        self.log("open %s %s" % (path,flags))
        #os.open(self.p(path), flags)
        return 0

    def read(self, path, len, offset):
        #self.log(str(os.environ))
        self.log("read %s %s %s" %(path, len, offset))
        f = open(self.p(path), "r")
        #print f.read()
        f.seek(offset)
        return f.read(len)

    def write(self, path, buf, off):
        self.log("write %s <buf> %s" % (path,off))
        f = open(self.p(path), "a")
        f.seek(off)
        f.write(buf)
        length = len (buf)
        return length

if __name__ == '__main__':
    server = Psfs(dash_s_do='setsingle')
    server.flags = 0
    server.parse(errex=1)
    server.multithreaded = 0
    idg = 0    
    #for i in glob.glob(index_dir+"/*"):
    #    self.log("Indexing ",i," ..."
    #    indexer.index_file(i)
    server.main()