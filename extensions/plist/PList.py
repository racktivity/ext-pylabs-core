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

#import pymonkey
from pymonkey import q
from pymonkey.Shell import *
import os

class PList(pymonkey.baseclasses.BaseType):
    """
    Meta-Data container for a collection of pfiles
    Data is  stored in a file on disk    
    
    Provides methods for managing and consulting data
    
    """
    
    COL_SEP = '\0'
    ROW_SEP = '\n'
    
    version         = q.basetype.integer(doc = 'Version of this plist', default = 1)
    type            = None
    fieldListOrder  = q.basetype.list(doc = 'List of PFileFields to capture for each file. The fields will also be save in this order', default = [])
    fieldSortOrder  = q.basetype.list(doc = 'List of PFileFields to determine sort order. None for no sorting (default)', allow_none = True, default = None)
    numberOfEntries = q.basetype.integer(doc = 'Number of pfiles in this plist', default = 0)
    rootPath        = q.basetype.dirpath(doc = 'Base path for the pfiles in this plist. The pfile\'s paths in the plist are relative to this path', allow_none = True, default = None)
    _filePath       = q.basetype.filepath(doc = 'Path to the plist file')
    
    def __init__(self, plistPath=None):
        """
        Initialize a PList
        """
        if plistPath==None:
            plistPath=q.system.fs.getTempFileName(q.dirs.tmpDir, 'plist_')
        self._filePath =  plistPath              
        self._defineColumns()
        self._fp = None
        
    def addFile(self, directoryPath, fileName, fileType = None, errorCode = None, stmode = None, stino = None, stdev = None, stnlink = None, stuid = None, stgid = None, stsize = None, statime = None, stmtime = None, stctime = None, fp = None):
        """
        Adds a file with the given properties to the plist
        
        @param fp:    Optional pointer to the open plist db
        """
        print "%s %s " % (directoryPath,fileName)
        
        
        pass
    
    def removeFile(self, directoryPath, fileName):
        """
        Removes a file from the plist
        """
        pass
    
    def addPFile(self, pfile, fp = None):
        """
        Adds a pfile to the plist
        
        @param pfile: PFile object to add to the list
        @param fp:    Optional pointer to the open plist db
        """
        #print "Adding  file %s to list" % pfile.fileName
        
        self._open(mode = 'ab+')
        self._writeLine(self._getPFileLine(pfile))
        self._close()
        
    
    def removePFile(self, pfile):
        """
        Removes a pfile from the plist
        """
        pass
    
    def delete(self): 
        """
        Deletes this plist
        
        @TODO: delete the plist 
        """
        pass 
     
    
    ################################################
    ##                                            ##
    ################################################
    def copyTo(self, destinationdir): 
        pass 
    def hardlinkTo(self, destinationdir): 
        pass 
    def symlinkTo(self, destinationdir): 
        pass 
    
    def compressTarGZip(self, compressedDestFile): 
        pass 
    #just tar no compression 
    def compressTar(self, compressedDestFile): 
        pass 
    def resyncTO(self, rsyncDestination): 
        pass 
    
    def _fromFile(self, plistPath):
        
        
        # Read header and get PList properties
        if not q.system.fs.exists(plistPath):
            raise ValueError('PList path %s does not exists!' % plistPath)
        
        
    def _createNew(self, plistPath):
        pass
    
    def _getPFileLine(self, pfile):
        """
        Returns the string representation of a pfile record for this plist
        
        @param pfile: PFile to give string representation of record for
        @return:      String representation of the record for the given pfile
        """  
        # Return all required + optionale fields in the requested order of the given pfile 
        return self.COL_SEP.join([str(getattr(pfile, str(column), '')) for column in self._columns]) + self.ROW_SEP
        
        
    def _defineColumns(self):
        """
        Define the set of colums for this plist in the correct order
        """
        
        # Gather all required and optional colums for the current plist
        columns = ['directoryPath', 'fileName', 'fileType', 'errorCode']
        columns.extend(self.fieldListOrder)
        
        self._columns = columns
    
    ###########################################
    ##             File Operations           ##
    ###########################################
    def _open(self, mode = 'rb+'):
        
        if not self._fp:
            try:
                self._fp = open(self._filePath, mode = mode, buffering = 1) 
            except:
                raise
    
    def _close(self):
        
        if self._fp:
            self._fp.close()
            self._fp = None
            
    def _writeLine(self, line):
        
        try:
            self._fp.write(line)
        except:
            raise
        
    def _writeLines(self, lines):
        
        try:
            self._fp.writelines(lines)
        except:
            raise