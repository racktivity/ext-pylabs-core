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
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

class ApacheDirectory(CMDBSubObject):
    """
    Class which is responsible for the configuration of 1 Apache directory
    """
    
    directives = q.basetype.dictionary(doc="key value pairs to set configuration", allow_none=True)
    directoryPath = q.basetype.dirpath(doc="directory-path is either the full path to a directory, or a wild-card string using Unix shell-style matching", allow_none=True)
    
    
    def addDirective (self, directiveName, directiveValue):
        """ 
        add directive to directives dict.
        """
        if directiveName != None and directiveValue != None:
            directiveValueStored = self.getDirective(directiveName)
            if directiveValueStored == None:
                self.directives[directiveName] = directiveValue
            else:
                q.logger.log("Directive (%s):(%s) already exits"%(directiveName, directiveValueStored))
                
    def getDirective(self, directiveName):
        """
        return value from directives dict 
        """
        if directiveName in self.directives:
            return self.directives[directiveName]
        
        q.logger.log("%s Doesnt Exist"%directiveName)
        
        return None
            
    def list(self):
        """
        return dict with key value pairs of directory configuration
        """
        return self.directives
    
    def _generateConfigData(self):
        """
        Returns configuration data for 1 directory 
        Example:
            <Directory /opt/qbase/www/>
                Order Deny,Allow
                Deny from All
            </Directory>         
        """
        
        if q.platform.isUnix() and self.directoryPath.startswith("/") == False:
            self.directoryPath = "/%s"%self.directoryPath
            
        configData = "\t<Directory \"%s\">\n"%self.directoryPath
        
        for directiveName in self.directives.keys():
            directiveValue = self.getDirective(directiveName)
            configData += "\t\t%s %s\n"%(directiveName, directiveValue)
            
        configData += "\t</Directory>\n"
        
        return configData
        
    def __str__(self):
        rep = "Directory %s\n"%self.directoryPath
        
        for directiveName in self.directives.keys():
            rep += "\t\t%s     %s\n"%(directiveName, self.directives[directiveName])
        
        return rep
    
    def __repr__(self):
        return self.__str__()