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
 
from pymonkey import q
from pymonkey.baseclasses.CMDBSubObject import CMDBSubObject
from ApacheDirectory import ApacheDirectory
from ApacheLocation import ApacheLocation 
import re

class ApacheVirtualHost(CMDBSubObject):
    """
    Class which is responsible for the configuration of 1 Apache virtual host
    """
    documentRoot = q.basetype.string(doc="Location on filesystem where files are being served from (if applicable)", allow_none=True)
    servername = q.basetype.string(doc="Hostname and port that the server uses to identify itself ", allow_none=True)
    apacheDirectories = q.basetype.dictionary(doc="Contains the configured directories",allow_none=True)
    apacheLocations = q.basetype.dictionary(doc="Contains the configured locations", allow_none=True)
    alias = q.basetype.dictionary(doc="Contains the aliases", allow_none=True)
    extraConfig= q.basetype.dictionary(doc="Contains some extra configuration", allow_none=True)

    def addDirectory(self, directoryPath):
        """
        Add directory to apacheDirectories array and returns new ApacheDirectoy object
        """
        directoryPath = directoryPath.replace("\\","/")
        directoryPath = directoryPath.replace("//","/")
                
        apacheDir = self.getDirectory(directoryPath)
            
        if apacheDir == None:
            
            apacheDir = ApacheDirectory()
            apacheDir.directoryPath = directoryPath
            self.apacheDirectories[directoryPath] = apacheDir
            
        else:
            q.logger.log("Directory Path (%s) Already Exists"%directoryPath)
        
        return apacheDir
    

    def getDirectory(self, directoryPath):
        """
        return ApacheDirectoy object 
        """
        if directoryPath in self.apacheDirectories:
            return self.apacheDirectories[directoryPath]

        q.logger.log("Directory (%s) was not found "%directoryPath )        
        
        return None
    
       
    def addLocation(self, urlPath):
        """
        Add directory to apacheLocations array and returns new ApacheLocation object
        """
        location = self.getLocation(urlPath)
        
        if location == None:
            location = ApacheLocation()
            location.urlPath = urlPath
            self.apacheLocations[urlPath]  = location
            
        else:
            q.logger.log("Location (%s) already Exists"%urlPath)
            
        return location
        
    def getLocation(self, urlPath):
        """
        return ApacheLocation object 
        """
        if urlPath in self.apacheLocations:
            return self.apacheLocations[urlPath]
        
        q.logger.log("Location (%s) was not found"%urlPath)
        
        return None
             
    def _generateConfigData(self, port):
        """
        Loop over all directories and locations in apacheDirectories and apacheLocations array and collect all configuration data.
        
        E.g. 
            for directory in apacheDirectories:
                output += directory._generateConfigData()
            for location in apacheLocations:
                output += location._generateConfigData()
        """        
        config = ""
        config += "\nListen %s"%port
            
        config += "\n<VirtualHost 0.0.0.0:%s>\n"% ( port)
        default = re.compile("default")
        
        if self.documentRoot != None and self.documentRoot != "":
            config += "\tDocumentRoot \"%s\"\n"%self.documentRoot
            
        for alias in self.alias.keys():
            config += "\tAlias /%s \"%s\"\n"%(alias, self.alias[alias])
        
        for conf in self.extraConfig.keys():
            config += "\n\t%s\t%s" % ( conf, self.extraConfig[conf] )
            config +="\n"
        
        if self.servername != None and self.servername != "" and not default.search(self.servername):
            config += "\n\tServerName \"%s\"\n"%self.servername
        
        for directory in self.apacheDirectories.values():
            config += directory._generateConfigData()
            config += "\n"
            
        for location in self.apacheLocations.values():
            config += location._generateConfigData()
            config += "\n"
        
        virtualHostEndTag = "</VirtualHost>\n"
        
        config += virtualHostEndTag
        
        return config
       
    def __str__(self):
        rep = "Virtual Host Configuration:\n"
        
        rep += "\n\t Apache Directories:\n"
        for directory in self.apacheDirectories.values():
            rep += "\t\t%s"%str(directory)
            
        rep += "\n\t Apache Locations:\n"    
        for location in self.apacheLocations.values():
            rep += "\t\t%s"%str(location)

        rep += "\n\t Extra Configurations:\n"   
        for extra in self.extraConfig.keys():
            rep += "\t\t%s \t %s"%(extra, self.extraConfig[extra])
            
        return rep
    
    def __repr__(self):
        return self.__str__()