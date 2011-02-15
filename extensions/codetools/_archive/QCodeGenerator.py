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
from codetools.parser.CodeParser import CodeParser
from codetools.codeformatters.templates.CodeFormatterStd import CodeFormatterStd
from codetools.parser.CodeStructure import CodeStructure
import os

class QCodeGenerator:
    
    def __init__(self):
        pass
        
    def convertFiles(self, sourceDir, destDir, parserClass = SpecFileParser, parserArguments = {}, generatorClass = CodeFormatterStd, generatorArguments = {}):
        """
        Loops over all files in [sourceDir] and passes them to [parserClass]. Optional arguments can be specified in [parserArguments].
        The parsed codeStructure is passed to [generatorClass]. Optional arguments for the code generator can be specified in [generatorArguments].
        The resulted files will be written in [destDir].
        """
        
        codeStructure = CodeStructure()
        parserInstance = parserClass()
        generatorInstance = generatorClass()
        
        for filePath in q.system.listFilesInDir(sourceDir):
            newCodeFile = parserInstance.parse(filePath, **parserArguments)
            codeStructure.addCodeFile(newCodeFile)
            
        generatedFiles = generatorInstance.generate(codeStructure, **generatorArguments)
        
        for (filename, contents) in generatedFiles.iteritems():
            q.system.writeFile(destDir + os.sep + filename, contents)