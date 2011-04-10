from pylabs import q
from iterators import *
import errno

class NoEntryError(RuntimeError):
    def __init__(self, *args):
        self.msg = args[0]
        self.errno = errno.ENOENT
            
class FileNode(object):
    isLeaf = True
    def __init__(self, name, size, moddate, md5hash=""):
        self.name = name
        self.size = size
        self.moddate = moddate
        self.md5hash = md5hash
    
    def __getitem__(self, idx):
        '''allows the file object to be unpacked into its primitive attributes
        might come handy with compatibility with the existing code'''
        return (self.size, self.moddate, self.md5hash)[idx]

    def __cmp__(self, other):
        return cmp(self.name, other.name)
    
# disabled since unpack would prefer __iter__ for __getitem__
#    def __iter__(self):
#        return NullIterator()
    
    def __eq__(self, other):
        return self.name == other.name & self.md5hash == other.md5hash
    
    def __str__(self):
        return 'f:%s'%self.name
    
    __repr__ = __str__
    
class DirNode(object):
    isLeaf = False
    def __init__(self, key, path, moddate=None, accessdate=None):
        self.key = key
        self.path = path
        _now = q.base.time.getTimeEpoch()
        self.moddate = moddate or _now
        self.accessdate = accessdate or _now
        self.stpoolid = 0
        self.files = dict()
        self.dirs = dict() #consider using flyweight pattern and not keeping dir objects in memory
        self._dirs = list() #a simple list of names that is serialized

    def __cmp__(self, other):
        return cmp(self.path, other.path)
    
    def __iter__(self):
        return DirIterator(self)
    
    def __str__(self):
        content="Dirpath: %s\n"% (self.path)
        for key in self.files:
            fileinfo=tuple(self.files[key])
            content="%sFile: %s %s\n" %(content, key, fileinfo)
        for dir in sorted(self.dirs.values()):
            content="%sSubdir: %s\n" %(content, dir.path)
        return content
   
    def __repr__(self):
        '''Serliaizes a dirNode'''
        content="1\n" #identifies format used, is for further reference
        content="%s%s\n"%(content, self.path)
        for key in self.files:
            size, moddate, md5hash = self.files[key]
            content="%sF:%s|%s|%s|%s\n"%(content, size, moddate, md5hash,key)
        for key in sorted(self.dirs.keys()):
            content = "%sD:%s\n"%(content, key)
        return content
    
    def deserialize(self, key, content):
        lines = content.split("\n")
        typ = lines[0]
        self.__init__(key,lines[1])
        lines2 = lines[2:]
        for line in lines2:
            if line.strip():
                if line[0:2]=="F:":
                    [size,modDate,md5hash,name]=line[2:].split("|")
                    self.addFile(name,long(size),float(modDate),md5hash)
                if line[0:2]=="D:":
                    self.addSubDir(line[2:])
        return self

    def _getChildren(self):
        children = sorted(self.dirs.values())
        children.extend(sorted(self.files.values()))
        return children
    
    children = property(fget=_getChildren)
    
    def addFileNode(self, fileNode):
        self.files[fileNode.name] = fileNode
        
    def addFile(self, name, size=0, moddate=0, md5hash=''):
        self.files[name.strip()] = FileNode(name, size, moddate, md5hash)
        
    def addFilePath(self, fileFullPath):
        stat = q.system.fs.statPath(fileFullPath)
        filename = q.system.fs.getBaseName(fileFullPath)
        size = stat.st_size
        moddate = stat.st_mtime
        #creationDateOnDisk = stat.st_ctime
        #accessDateOnDisk = stat.st_atime
        if self.usemd5:
            md5hash = q.tools.hash.md5(fileFullPath)            
        else:
            md5hash = ""            
        self.addFile(filename, size, moddate, md5hash)
    
    def addDirNode(self, dirNode):
        self.dirs[dirNode.path] = dirNode
        
    def addSubDir(self, path):
        self.dirs[path] = DirNode(DirNode.getKey(path), path)
    
    @classmethod
    def getKey(cls, path):
        separator="_!_"
        if path.find(separator) <> -1:
            raise RuntimeError("Cannot work with dir %s because has our separator %s in pathname" % (separator,dirPath))
        key = path.replace("/",separator)
        return key
    
    #copied over from DirObjects
    def updateAccessdate(self):
        self.accessdate=q.base.time.getTimeEpoch()

    def updateModdate(self):
        self.moddate=q.base.time.getTimeEpoch()        
    
    def containsFile(self, name):
        return name.strip() in self.files
        
    def getFileInfo(self, name):
        return self.files.get(name.strip(), None)
    
    def getFilePath(self, name):
        return q.system.fs.joinPaths(self.path, name)

        
def test():
    #build a sample composite
    pass
    
def testCompositeIterator():
    key_prefix = 'k'
    dir_prefix = 'dir'
    file_prefix = 'file'
    path = '/'
    root = DirNode('k_000', path)
    for i in range(1, 3):
        d = DirNode('%s%03d'%(key_prefix, i), path+'%s%03d/'%(dir_prefix, i))
        root.addDirNode(d)
        for j, k in zip(range(1, 3), range(1, 3)):
            f = FileNode('%s%03d'%(file_prefix, j), j, q.base.time.getTimeEpoch(), '')
            sd = DirNode('%s%03d'%(key_prefix, k), d.path+'%s%03d'%(dir_prefix, k))
            d.addFileNode(f)
            d.addDirNode(sd)
    itr = CompositeIterator(root)
    return itr        
    
if __name__ == '__main__':
    test()        