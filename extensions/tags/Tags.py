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
from urllib import unquote, quote

class Tags():
    """
    represent set of tags & _labels
    label is e.g. important (no value attached)
    tag is with value attached e.g. customer:kristof
    """    
    def __init__(self, tagstring='',setFunction4Tagstring=None):
        """
        @param tagstring:  example "labelexample customer:newco"
        @type tagstring: string
        @param setFunction4Tagstring is a function which will set the paramstring somewhere when changed by this class
        """
        self.tags = dict()
        self.labels = set()
        self.tagstring=tagstring
        if tagstring<>"":
            self.fromString(tagstring)
        self._setFunction4Tagstring=setFunction4Tagstring
        
    def fromString(self, tagstring):
        """
        go from string to Tag class filled in
        
        @param tagstring: example "important customer:kristof"
        @type tagstring: string        
        """
        
        if not tagstring:
            return

        tags = tagstring.split()
        for tag in tags:
            if tag.find(':') > 0:
                key = tag.split(':')[0]
                value = tag.split(':')[1]
                self.tags[unquote(key)] = unquote(value)
            else:
                self.labels.add(unquote(tag))
        self.tagstring=tagstring
        
    def _toString(self):
        """
        build string representation from tags
        
        @return: string representation from tags
        @rtype: string                
        """
        labelsString = " ".join([quote(label) for label in self.labels])
        tagsString = " ".join(["%s:%s" % (quote(k), quote(v)) for k, v in self.tags.iteritems()])
        
        self.tagstring = " ".join((labelsString, tagsString)).strip()
        self.tagstring=self.tagstring.replace("%2C", ",")
        
        if self._setFunction4Tagstring<>None:
            self._setFunction4Tagstring(self.tagstring)
        
        return self.tagstring
        
    __repr__ = __str__ = _toString
        
    def tagGet(self, tagname):
        """
        @param tagname: e.g customer
        @type tagname: string 
        
        @return: value behind tag 
        @rtype: string
        """
        if self.tags.has_key(tagname):
            return self.tags[tagname]
        else:
            #raise error when tag does not exist
            raise Exception('tagname %s does not exist'% tagname)
        
    def tagExists(self, tagname):
        """
        check whether tagname exists in the tags dictionary
        
        @return: true if tag exists
        @rtype: boolean        
        """
        return self.tags.has_key(tagname)
        
    def labelExists(self, labelname):
        """
        check whether labelname exists in the labels 
        
        @return: true if label exists
        @rtype: boolean        
        """
        return self.labels.issuperset(set([labelname]))
            
    
    def tagDelete(self, tagname):
        """
        delete tag, raise error if not existing
        
        @param tagname: e.g customer
        @type tagname: string        
        
        """
        if self.tags.has_key(tagname):
            val=self.tags.pop(tagname)
            self._toString()
            return val
        else:
            #raise error when tag does not exist
            raise Exception('tagname %s does not exist'% tagname)
        
    def labelDelete(self, labelname):
        """
        delete label, raise error if not existing
        
        @param labelname: e.g important
        @type labelname: string 
        """
        if not self.labelExists(labelname):
            raise Exception('label %s does not exist'% labelname)
        self.labels.remove(labelname)
        self._toString()
        
    def tagSet(self, tagName, tagValue):
        """
        add new key value tag
        
        @param tagName: e.g customer        
        @type tagName: string 
        
        @param tagValue: e.g kristof
        @type tagValue: string        
        """
        self.tags[tagName] = str(tagValue)
        self._toString()
        
    def labelSet(self, labelName):
        """
        add new label
        
        @param labelName: e.g important
        @type labelName: string
        """
        self.labels.add(labelName)
        self._toString()
        
    
    
