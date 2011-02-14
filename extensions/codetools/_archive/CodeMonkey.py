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
#from QCodeGenerator import QCodeGenerator
#from CodeFormatterSQL import CodeFormatterSQL
#from CodeFormatterSQLDiff import CodeFormatterSQLDiff_fromDB, CodeFormatterSQLDiff_fromOldSpecFiles
#@todo refactor to use new  q.codetools.... for codeformatters
from codetools.parser.CodeParser import CodeParser
from codetools.parser.TypeDef import TypeDef, TypeDefs
from pymonkey.inifile import IniFile
from codetools.parser.CodeStructure import CodeStructure

from pymonkey.db.DBConnection import DBConnection
#from DBFetcher import DBFetcher
import os

class CodeMonkey:
    """
    The CodeMonkey class contains convenience functions for code generation.
    """
   
    def __init__(self):
       # self.codegen = QCodeGenerator()
        self._dirs= []
        self.codestructures = []
        
    #~ def generateQDB(self, sourceDir, destDir, domainTypeFilePath):
        #~ self.codegen.convertFiles(sourceDir, destDir, generatorClass = CodeFormatterSQL, generatorArguments = {"domainTypes": self.readDomainTypes(domainTypeFilePath)})
        
    #~ def generateQDB_DiffFromDB(self, sourceDir, destDir, domainTypeFilePath, dbIP, dbName, dbLogin, dbPwd):
        #~ self.codegen.convertFiles(sourceDir, destDir, generatorClass = CodeFormatterSQLDiff_fromDB, generatorArguments = {"domainTypes": self.readDomainTypes(domainTypeFilePath), "dbIP": dbIP, "dbName": dbName, "dbLogin": dbLogin, "dbPwd": dbPwd})
        
    #~ def generateQDB_DiffFromFile(self, oldSourceDir, newSourceDir, destDir, oldDomainTypeFilePath, newDomainTypeFilePath = None):
        #~ oldDomainTypes = self.readDomainTypes(oldDomainTypeFilePath)
        #~ if newDomainTypeFilePath is None:
            #~ newDomainTypes = oldDomainTypes
        #~ else:
            #~ self.readDomainTypes(oldDomainTypeFilePath)
            
        #~ spf = SpecFileParser()
        
        #~ oldCodeStructure = CodeStructure()
        #~ for filePath in q.system.listFilesInDir(oldSourceDir):
            #~ oldCodeStructure.addCodeFile(spf.parse(filePath))
        
        #~ self.codegen.convertFiles(newSourceDir, destDir, generatorClass = CodeFormatterSQLDiff_fromOldSpecFiles, generatorArguments = {"newDomainTypes": newDomainTypes, "oldCodeStructure": oldCodeStructure, "oldDomainTypes": oldDomainTypes})
      
    def readDomainTypes(self, domainTypeFilePath):
        """
        Reads an INI-file containing domain type definitions and fills them into a TypeDefs-object.
        """
        result = TypeDefs()
        inifile = IniFile(domainTypeFilePath)
        for section in inifile.getSections():
            if section.endswith("(n)"):
                td = TypeDef(section[:-3], withLength = True)
            else:
                td = TypeDef(section, withLength = False)
            for (iniName, typeDefName) in [("dbtype", "databaseDefinition"), ("pythontype", "pythonType"), ("regex", "regex"), ("comment", "comment")]:
                if inifile.checkParam(section, iniName):
                    setattr(td, typeDefName, inifile.getValue(section, iniName))
            result.addTypeDef(td)
        return result
            
    def generatePython(self, sourceDir, destDir=None):
        raise Exception("This function uses CodeFormatterStd, which should be refactored.")
        if destDir is None:
            destDir = sourceDir
        self.codegen.convertFiles(sourceFile, destFile)
        
    # TODO: Code below is only used by CodeFormatterStd, which should be refactored.
    
    #def __init__(self):
    #    codeModelDirPath=q.dirs.getBaseDir()+os.sep+"lib"+os.sep+"pymonkey"+os.sep+"parser"+os.sep+"CodeFormatters"+os.sep+"CodeTemplateStd"+os.sep
    #    self.codeformatter=CodeFormatterStd.CodeFormatterStd(codeModelDirPath)   

    def addCurrentDir(self):
        self.addDir(os.path.realpath("."))

    def addDir(self,dir):
        if q.system.fs.exists(dir)==False:
            raise "Cannot find dir for pymonkey processing"
        self._dirs.append(dir)

        
    def processSpecFile(self,dir,filename):
        q.logger.log("CodeMonkey process spec file %s" % filename)
        #found file which needs processinqg
        cp = CodeParser()
        codefile = cp.parse(q.system.fs.joinPaths(dir,filename))
        return codefile

    def processSourceCodeFile(self,dir,filename):
        q.logger.log("CodeMonkey process source code file %s" % filename)
        #found file which needs processing
        cp = CodeParser()
        codefile = cp.parse(q.system.fs.joinPaths(dir,filename))
        return codefile
        
    def writeCode(self,dir=""):
        """write code back to directory, not the spec code"""
        for codefile in self.codestructures:
            codefile.writeCode(self.codeformatter,dir)

    def writeSpec(self,dir=""):
        """write spec back to directory, (if dir not specified is default spec dir) """
        for codestruct in self.codestructures:
            codestruct.writeSpec(dir)            
            
    def processSpecs(self):
        """
        read spec code and populate codestructures
        """
        specSubDirName="_spec"
        codestructure = CodeStructure()
        for dir in self._dirs:
            if q.system.fs.exists(q.system.fs.joinPaths(dir,specSubDirName)):
                files=q.system.fs.listPyScriptsInDir(q.system.fs.joinPaths(dir,specSubDirName))
                for fileName in files:
                    codestructure.addCodeFile(self.processSpecFile(q.system.fs.joinPaths(dir,specSubDirName),"%s.py" % fileName))
        return codestructure
                                
    def processSourceCode(self):
        """
        read source code and populate codestructures
        """
        specSubDirName=""
        codestructure = CodeStructure() 
        for dir in self._dirs:
            if q.system.fs.exists(q.system.fs.joinPaths(dir,specSubDirName)):                
                files=q.system.fs.listPyScriptsInDir(q.system.fs.joinPaths(dir,specSubDirName))
                for fileName in files:
                    codestructure.addCodeFile(self.processSourceCodeFile(q.system.fs.joinPaths(dir,specSubDirName),"%s.py" % fileName))
        return codestructure

    def getClass(self, className):
        for cf in self.codefiles:
            for classDef in cf.classDefs:
                if classDef.name == className:
                    return classDef
        q.logger.log("Could not find the class [%s]" % className, 3)
        return None