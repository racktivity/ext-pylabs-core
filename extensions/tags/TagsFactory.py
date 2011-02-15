# <License type="BSD" version="2.2">
#
# Copyright (c) 2009, A-server NV.
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
# 3. Neither the name A-server, nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY A-server, "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, LUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL A-server, OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, IDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (LUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (LUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

import pylabs
from Tags import Tags


class TagsFactory(pylabs.baseclasses.BaseType):
    """
    Factory Class of dealing with TAGS     
    """
    
    def getObject(self,tagstring="",setFunction4Tagstring=None):
        """
        check whether labelname exists in the labels 
        
        @param tagstring:  example "important customer:kristof"
        @type tagstring: string           
        """
        return Tags(tagstring,setFunction4Tagstring)
    
    def getTagString(self, labels=None, tags=None):
        """
        Return a valid tags string, it's recommended to use this function
        and not to build the script manually to skip reserved letters.
        
        @param labels: A set of labels
        @param tags: A dict with key values 
        """
        labels = labels or set()
        tags = tags or dict()
        if not isinstance(labels, set):
            raise TypeError("labels must be of type set")
        
        if not isinstance(tags, dict):
            raise TypeError("tags must be of type dict")
        
        t = Tags()
        t.labels = labels
        t.tags = tags
        return str(t)
    