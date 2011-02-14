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

from PList import PList
from PFile import PFile

from enums import PFileType, PFileFields, PFileErrorCode

class PFind(object):
    """
    Creates plists based on pfilters
    """

    def createPlist(self, rootPath, pfilters = None):
        """
        Creates a plist based on the criteria defined in the given pfilter
        
        #not used: @param pfields:     list of PFileFields to add for each pfile. Fields will also be stored in this order
        @param pfilters:    list of pfilters object defining criteria for this plist's pfiles
        
        @return: the newly created plist
        """
        
        plist = PList()
        plist.rootPath = rootPath
        #plist.fieldListOrder = None
        # Workaround
        plist._defineColumns()
        
        worker = PFindWorker(plist, pfilters)
        worker.doWalk(plist.rootPath, plist.addPFile)     #2nd param is action which will be given to walker
        
        return plist
        
class PFindWorker(object):
    
    def __init__(self, plist, pfilters = None):
        
        self.plist    = plist
        self.pfilters = pfilters
        
    def doWalk(self, path, action):
        """
        Walk the tree defined in plist and execute func for all pfiles
        matching pfilter's crriteria
        """
        q.system.fswalker.walk(path,  self.handlePath, action, recursive = True, includeFolders = True)
        
    def handlePath(self, action, path):
        """
        Check if the path matches all criteria and execute the requested
        action if it does
        """
        pfile = PFile()
        pfile = self.getPFileFromPath(path)
        
        if self.pfilters<>None:
            if not False in (pfilter.validate(pfile) for pfilter in self.pfilters):
                action(pfile)
        else:
            action(pfile)
            
    def getPFileFromPath(self, path, statInfo = True, md5 = False):
        
        pfile = PFile()
        
        # Required Fields
        folder = os.path.sep.join(dir for dir in path.split(os.sep)[0:-1]) 
        
        pfile.directoryPath  = self._relpath(folder, self.plist.rootPath) if self.plist.rootPath else folder
        pfile.fileName       = q.system.fs.getBaseName(path)   
        pfile.fileType       = PFileType.UNKNOWN
        pfile.errorCode      = PFileErrorCode.NO_ERROR
        
        # Optional Fields
        
        # Stat info
        if statInfo:
            stat = q.system.fs.statPath(path)
            pfile.protectionMode = stat[0]
            pfile.inodeNumber    = stat[1]
            pfile.device         = stat[2]
            pfile.numberOfLinks  = stat[3]
            pfile.uid            = stat[4]
            pfile.gid            = stat[5]
            pfile.size           = stat[6]
            pfile.atime          = stat[7]
            pfile.mtime          = stat[8]
            pfile.ctime          = stat[9]
            
        # Hash
        if md5:
            pfile.md5            = None
        
        return pfile
    
    def _relpath(self, target, base=os.curdir):
        """
        Return a relative path to the target from either the current dir or an optional base dir.
        Base can be a directory specified either as absolute or relative to current dir.
        
        @TODO: MOVE
        """
    
        if not os.path.exists(target):
            raise OSError, 'Target does not exist: '+target
    
        if not os.path.isdir(base):
            raise OSError, 'Base is not a directory or does not exist: '+base
    
        base_list = (os.path.abspath(base)).split(os.sep)
        target_list = (os.path.abspath(target)).split(os.sep)
    
        # On the windows platform the target may be on a completely different drive from the base.
        if os.name in ['nt','dos','os2'] and base_list[0] <> target_list[0]:
            raise OSError, 'Target is on a different drive to base. Target: '+target_list[0].upper()+', base: '+base_list[0].upper()
    
        # Starting from the filepath root, work out how much of the filepath is
        # shared by base and target.
        for i in range(min(len(base_list), len(target_list))):
            if base_list[i] <> target_list[i]: break
        else:
            # If we broke out of the loop, i is pointing to the first differing path elements.
            # If we didn't break out of the loop, i is pointing to identical path elements.
            # Increment i so that in all cases it points to the first differing path elements.
            i+=1
    
        rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
        
        if not rel_list:
            #rel_list = base_list
            rel_list = ['.']
            
        return os.path.join(*rel_list)