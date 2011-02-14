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
from pymonkey.Shell import *
import urllib

class TemplateEngine(object):
    replaceDict = {}##dict(string,string)

    def add(self, search, replace):
        if not q.basetype.string.check(search):
            raise RuntimeError("only strings can be searched for when using template engine, param search is not a string")
        if not q.basetype.string.check(replace):
            raise RuntimeError("can only replace with strings when using template engine, param replace is not a string")
        self.replaceDict[search] = replace

    def __replace(self, body):
        for search in self.replaceDict.keys():
            replace = self.replaceDict[search]
            searchWithColons="{%s}" % search 
            searchWithUrlEncode="{:urlencode:%s}" % search 
            body = body.replace(searchWithColons, replace)
            body = body.replace(searchWithUrlEncode, urllib.quote(replace, ''))
        return body

    def replace(self, body, replaceCount = 3):
        """
        replace happens std 3 times to allow recursive template behaviour e.g. var gets replaces, combo introduces var which gets replaced again
        """
        if body=="":
            raise RuntimeError("cannot replace text if empty, body param cannot be empty")        
        for i in range(replaceCount):
            body = self.__replace(body)
        return body

    def replaceInsideFile(self, filePath, replaceCount = 3):
        self.__createFileFromTemplate(filePath, filePath, replaceCount)

    def __createFileFromTemplate(self, templatePath, targetPath, replaceCount = 3):
        originalFile = q.system.fs.fileGetContents(templatePath)
        modifiedString = self.replace(originalFile, replaceCount)
        q.system.fs.writeFile(targetPath, modifiedString)

    def reset(self):
        self.replaceDict={}

if __name__ == '__main__':
    te=TemplateEngine()
    te.add("login", "kristof")
    te.add("passwd","root")
    text="This is a test file for {login} with a passwd:{passwd}"
    print te.replace(text)
    
    
    
###OLD CODE
##class TemplateEngine(object):
    ##replaceDict = {}##dict(string,string)
    ##System ##System

    ##def add(self, search, replace):
        ##self.replaceDict[search] = replace

    ##def __replace(self,body):
        ##for search in self.replaceDict.keys():
            ##replace = self.replaceDict[search]
            ##body = body.replace("{" + search + "}", replace)
            ##body = body.replace("{:urlencode:" + search + "}", urllib.quote(replace, ''))
        ##return body

    ##def replace(self, body, replaceCount = 3):
        ##for i in range(replaceCount):
            ##body = self.__replace(body)
        ##return body

    ##def replaceInsideFile(self, filePath, replaceCount = 3):
        ##self.__createFileFromTemplate(filePath, filePath, replaceCount)

    ##def __createFileFromTemplate(self, templatePath, targetPath, replaceCount = 3):
        ##originalFile = System.fileGetContents(templatePath)
        ##modifiedString = self.replace(originalFile, replaceCount)
        ##System.writeFile(targetPath, modifiedString)

    ##def reset(self):
        ##self.replaceDict={}    