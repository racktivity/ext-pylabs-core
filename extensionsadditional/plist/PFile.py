# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

import pylabs

from enums import PFileType, PFileErrorCode

class PFile(pylabs.baseclasses.BaseType):
    """
    Data container for all properties of a file/folder/symlink registered in a plist
    
    @TODO: Checkout of we should map everything to a tuple with a fixed position for each field
    @TODO: Should paths be saved as lists split on os.sep to support cross-platform paths?     
    """
    directoryPath  = pylabs.q.basetype.dirpath(doc = 'directory path, relative to root path', allow_none = True)
    fileName       = pylabs.q.basetype.string(doc = 'name of the file', allow_none = True)
    fileType       = pylabs.q.basetype.enumeration(PFileType, doc = 'Type of file')
    errorCode      = pylabs.q.basetype.enumeration(PFileErrorCode, doc = 'Code indication error state of file')
    protectionMode = pylabs.q.basetype.integer(doc = 'Inode protection mode', allow_none = True)
    inodeNumber    = pylabs.q.basetype.integer(doc = 'Inode number', allow_none = True) # Will be different on different filesystems
    device         = pylabs.q.basetype.integer(doc = 'Device inode resides on', allow_none = True) # Will be different on different filesystems
    numberOfLinks  = pylabs.q.basetype.integer(doc = 'Number of links to the inode', allow_none = True)
    uid            = pylabs.q.basetype.integer(doc = 'User id of the owner', allow_none = True)
    gid            = pylabs.q.basetype.integer(doc = 'Group id of the owner', allow_none = True)
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
        self.protectionMode = protectionMode
        self.inodeNumber    = inodeNumber
        self.device         = device
        self.numberOfLinks  = numberOfLinks
        self.uid            = uid
        self.gid            = gid
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
        self.protectionMode = None
        self.inodeNumber    = None
        self.device         = None
        self.numberOfLinks  = None
        self.uid            = None
        self.gid            = None
        self.size           = None
        self.atime          = None
        self.mtime          = None
        self.ctime          = None
        self.md5            = None