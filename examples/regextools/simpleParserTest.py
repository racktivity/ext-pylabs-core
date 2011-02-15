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

from pylabs.InitBase import *
from pylabs.Shell import *


q.application.appname="simpleparser"

q.application.start()

content=pylabs.q.system.fs.fileGetContents("examplecontent1.txt")

class Parser:
    
    def __init__(self,content):
        self.classes={}
        classes=q.codetools.regex.extractBlocks(content,["^class "],[],[],["^ "],[".*"],["^ *\#"]) 
        for classContent in classes:
            classname = self.getClassName(classContent)
            self.classes[classname] = classContent
            
    def getClassName(self,text):
        pattern=r"(?<=^class )[ A-Za-z0-9_\-]*\b"
        return q.codetools.regex.findOne(pattern,text)
   
    def processClass(self,classname):
        classContent = self.classes[classname]
        firstline=classContent.split("\n")[0]
        inheritance=q.codetools.regex.findOne("\(.*\)",firstline)  #finds (...)
        inheritance=inheritance[1:-1]  #finds inside ()
        q.console.echo("%s inherits from %s" % (classname, inheritance))
        classbody=q.codetools.regex.removeLines("^class ",classContent)
        q.console.echo("The body of %s is \n%s" % (classname, classbody))
        

    def processClassMethod(self,className):
        classContent = self.classes[className]
        defs = self.getDefs(classContent)
        for defblock in defs:
            firstline=defblock.split("\n")[0] 
            defname = self.getDefName(firstline)
            defparams = self.getDefParams(firstline)
            defbody = q.codetools.regex.removeLines("^    def ",defblock) 
            q.console.echo("%s has the following parameters:" % defname)
            for defparam in defparams:
                q.console.echo("\t%s" % defparam)
            q.console.echo("The body is \n%s" % defbody)

    def getDefs(self,classContent):
        return q.codetools.regex.extractBlocks(classContent,["^    def "],[],[],["^ "],[".*"],["^ *\#"])
    
    def getDefName(self,text):
        pattern=r"(?<=^    def )[ A-Za-z0-9_\-]*\b"
        return q.codetools.regex.findOne(pattern,text)
    
    def getDefParams(self,text):
        tmp=q.codetools.regex.findOne("\(.*\)",text)  #finds (...)
        tmp=tmp[1:-1]  #finds inside ()
        params=tmp.split(",")
        return params

parser=Parser(content)        
qshell()       
    
q.application.stop()