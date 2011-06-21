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

from pylabs import q
from pylabs.Shell import *

from PFilter import PFilter
from PFind import PFind,PFindWorker

class PListFactory(object):
    """
    Factory class for creating plists related objects
    
    """
    def __init__(self):
        self._find=PFind()

    def getFilterObject(self):
        return PFilter()
                
    def filesystemScan(self,root,pfilter=None):
        """
        do a find starting from root in filesystem with an optional filter
        use the getFilterObject to define a filter first
        returns a new plistObject with the result of this find
        """
        return self._find.createPlist(root,pfilter)
    
    def filter(self,plistObject,pfilter=None):
        """
        use the getFilterObject to define a filter first
        returns a new plistObject with the result of this filteroperation
        """
        return self._find.createPlist(root,pfilter)
        
      
    def diff(self,plistObjectSource,plistObjectDest,plistObjectNew,plistObjectDeleted,plistObjectModified,ignoreDates=False):
        """
        compare 2 plists
        returns a new changeListObject with the result of this method
        """
       
    def add(plistObject1,plistObject1,failIfDuplicateObjects=True):
        """
        add 2 plists
        returns a new changeListObject with the result of this method
        result needs to be unique per filepath in plist
        @param failIfDuplicateObjects if False the file with most recent moddate wins
        """
        
    def substract(self,plistObjectSource,plistObjectToSustract):
      
      
     

        