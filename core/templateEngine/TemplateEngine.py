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

from pylabs.System import System
import urllib

class TemplateEngine(object):
    replaceDict = {}##dict(string,string)
    System ##System

    def add(self, search, replace):
        self.replaceDict[search] = replace

    def __replace(self,body):
        for search in self.replaceDict.keys():
            replace = self.replaceDict[search]
            body = body.replace("{" + search + "}", replace)
            body = body.replace("{:urlencode:" + search + "}", urllib.quote(replace, ''))
        return body

    def replace(self, body, replaceCount = 3):
        for i in range(replaceCount):
            body = self.__replace(body)
        return body

    def replaceInsideFile(self, filePath, replaceCount = 3):
        self.__createFileFromTemplate(filePath, filePath, replaceCount)

    def __createFileFromTemplate(self, templatePath, targetPath, replaceCount = 3):
        originalFile = System.fileGetContents(templatePath)
        modifiedString = self.replace(originalFile, replaceCount)
        System.writeFile(targetPath, modifiedString)

    def reset(self):
        self.replaceDict={}

if __name__ == '__main__':
    te=TemplateEngine()
    te.add("login", "kristof")
    te.add("passwd","root")
    text="This is a test file for {login} with a passwd:{passwd}"
    print te.replace(text)