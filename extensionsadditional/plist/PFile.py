#@todo do not use this object when creating a plist it should go without using these intermediate objects
#@todo is ok to use to retrieve a File info out of Plist

import pylabs

from enums import PFileType, PFileErrorCode

class PFile(pylabs.baseclasses.BaseType):
    """
    Data container for all properties of a file/folder/symlink registered in a plist
    
    @TODO: Checkout of we should map everything to a tuple with a fixed position for each field
    @TODO: Should paths be saved as lists split on os.sep to support cross-platform paths?     
    """
    id
    directoryPath  = pylabs.q.basetype.dirpath(doc = 'directory path, relative to root path', allow_none = True)
    fileName       = pylabs.q.basetype.string(doc = 'name of the file', allow_none = True)
    fileType       = pylabs.q.basetype.enumeration(PFileType, doc = 'Type of file')
    errorCode      = pylabs.q.basetype.enumeration(PFileErrorCode, doc = 'Code indication error state of file')
    fileparts ...
    size           = pylabs.q.basetype.integer(doc = 'Size in bytes of a plain file; amount of data waiting on some special files', allow_none = True)
    atime          = pylabs.q.basetype.integer(doc = 'Time of last access', allow_none = True) # Will be different on different filesystems
    mtime          = pylabs.q.basetype.integer(doc = 'Time of last modification', allow_none = True) # Will be different on different filesystems
    ctime          = pylabs.q.basetype.integer(doc = 'The ctime as reported by the operating system. On some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time (see platform documentation for details)', allow_none = True) # Will be different on different filesystems
    md5            = pylabs.q.basetype.string(doc = 'md5 checksum of the file', allow_none = True)

    def __init__(self, directoryPath = None, fileName = None, fileType = PFileType.UNKNOWN, errorCode = PFileErrorCode.NO_ERROR, protectionMode = None, 
                 inodeNumber = None, device = None, numberOfLinks = None, uid = None, gid = None, size = None, atime = None, 
                 mtime = None, ctime = None, md5 = None):
        """
        Initialize a new pfile object
        """
    
        self.directoryPath  = directoryPath
        self.fileName       = fileName
        self.fileType       = fileType
        self.errorCode      = errorCode
        self.size           = size
        self.atime          = atime
        self.mtime          = mtime
        self.ctime          = ctime
        self.md5            = md5
        
    def clear(self):
        """
        Resets all values to empty values
        """
        
        self.directoryPath  = None
        self.fileName       = None
        self.fileType       = PFileType.UNKNOWN
        self.errorCode      = PFileErrorCode.NO_ERROR
        self.size           = None
        self.atime          = None
        self.mtime          = None
        self.ctime          = None
        self.md5            = None
        
    def diffWithFile(self,filepath):
      """
      return filePatchObject
      """