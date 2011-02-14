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

from pymonkey.System import System
import re
from pymonkey.Shell import *
from pymonkey import q

class RegexTemplates_FindLines:
    """
    regexexamples which find lines
    """
    #@todo for all methods do input checking

    def findCommentlines(self):
        return "^( *#).*"
    
    def findClasslines(self):
        return "^class .*"

    def findDeflines(self):
        return "^def .*"
    
class Empty:
    pass
    
class RegexMatches:
    def __init__(self):
        self.matches=[]
        
    def addMatch(self,match):
        if match<>None or match<>"":
            rm=RegexMatch()
            rm.start=match.start()
            rm.end=match.end()
            rm.founditem=match.group()
            rm.foundSubitems = match.groups()
        self.matches.append(rm)

    def __str__(self):
        out=""
        for match in self.matches:
            out=out+match.__str__()
        return out

    def __repr__(self):
        return self.__str__()

class RegexMatch:
    def __init__(self):
        self.start=0
        self.end=0
        self.founditem=""
        self.foundSubitems = None

    def __str__(self):
        out="%s start:%s end:%s\n" % (self.founditem, self.start, self.end)
        return out

    def __repr__(self):
        return self.__str__()
        
        
class RegexTools:
    #@todo doe some propper error handling with re, now obscure errors
    def __init__(self):
        self.templates=Empty()
        self.templates.lines=RegexTemplates_FindLines()

    def match(self,pattern,text):
        """
        search if there is at least 1 match
        """
        if pattern=="" or text=="":
            raise RuntimeError("Cannot do .codetools.regex.match when pattern or text parameter is empty")     
        #pymonkey.q.logger.log("Regextools: pattern:%s in text:%s" % (pattern,text),5)        
        #print "Regextools: pattern:%s in text:%s" % (pattern,text)
        pattern=self._patternFix(pattern)
        result=re.findall(pattern,text)
        if len(result)>0:
            return True
        else:
            return False
        
    def matchMultiple(self,patterns,text):
        """
        see if any patterns matched
        if patterns=[] then will return False
        """
        if patterns=="":
            raise RuntimeError("Cannot do .codetools.regex.matchMultiple when pattern is empty")        
        if text=="":
            return False
        if type(patterns).__name__<>'list' :
            raise RuntimeError("patterns has to be of type list []")
        if patterns==[]:
            return False
            
        for pattern in patterns:
            pattern=self._patternFix(pattern)
            if self.match(pattern,text):
                return True
        return False

    def _patternFix(self,pattern):
        if pattern.find("(?m)")==-1:
            pattern="%s%s" % ("(?m)",pattern)
        return pattern
    
    def replace(self,regexFind,regexFindsubsetToReplace,replaceWith,text):
        """
        Search for regexFind in text and if found, replace the subset regexFindsubsetToReplace of regexFind with replacewith and returns the new text
        Example:
            replace("Q-Layer Server", "Server", "Computer", "This is a Q-Layer Server")
            will return "This is a Q-Layer Computer"
        @param regexFind: String to search for, can be a regular expression
        @param regexFindsubsetToReplace: The subset within regexFind that you want to replace
        @param replacewith: The replacement
        @param text: Text where you want to search and replace
        """
        if not regexFind or not regexFindsubsetToReplace or not text:
            raise RuntimeError("Cannot do .codetools.regex.replace when any of the four variables is empty.")
        if regexFind.find(regexFindsubsetToReplace) == -1:
            raise RuntimeError('regexFindsubsetToReplace must be part or all of regexFind "ex: regexFind="Some example text", regexFindsubsetToReplace="example"')
        matches = self.findAll(regexFind,text)
        if matches:
            finalReplaceWith = re.sub(regexFindsubsetToReplace, replaceWith, matches[0])
            text=re.sub(self._patternFix(regexFind), finalReplaceWith, text)

        return text

    def findOne(self,pattern,text, flags=0):
        """
        Searches for a one match only on pattern inside text, will throw a RuntimeError if more than one match found
        @param pattern: Regex pattern to search for
        @param text: Text to search in
        """
        if not pattern or not text:
            raise RuntimeError("Cannot do .codetools.regex.findOne when pattern or text parameter is empty")               
        pattern=self._patternFix(pattern)
        result= re.finditer(pattern,text, flags)
        finalResult = list()
        for item in result:
            finalResult.append(item.group())

        if len(finalResult)>1:
            raise "found more than 1 result of regex %s in text %s" % (pattern,text)
        if len(finalResult)==1:
            return finalResult[0]
        return ""
    

    def findAll(self,pattern,text, flags=0):
        """
        Search all matches of pattern in text and returns an array
        @param pattern: Regex pattern to search for
        @param text: Text to search in
        """
        if pattern=="" or text=="":
            raise RuntimeError("Cannot do .codetools.regex.findAll when pattern or text parameter is empty")        
        pattern=self._patternFix(pattern)
        results = re.finditer(pattern,text, flags)
        matches = list()
        if results:
            matches = [x.group() for x in results]
        return matches

    def getRegexMatches(self, pattern, text, flags=0):
        """
        match all occurences and find start and stop in text
        return RegexMatches  (is array of RegexMatch)
        """
        if pattern=="" or text=="":
            raise RuntimeError("Cannot do q.codetools.regex.getRegexMatches when pattern or text parameter is empty")
        pattern=self._patternFix(pattern)
        rm=RegexMatches()
        for match in re.finditer(pattern, text, flags):
            rm.addMatch(match)
        return rm

    def yieldRegexMatches(self, pattern, text, flags=0):
        """The same as getRegexMatches but instead of returning a list that contains all matches it uses yield to return a generator object
            witch would improve the performance of the search function.
        """
        if pattern=="" or text=="":
            raise RuntimeError("Cannot do q.codetools.regex.getRegexMatches when pattern or text parameter is empty")
        pattern=self._patternFix(pattern)
        
        for match in re.finditer(pattern, text, flags):
            rm = RegexMatch()
            rm.start = match.start()
            rm.end = match.end()
            rm.founditem = match.group()
            rm.foundSubitems = match.groups()
            yield rm
        
    def getRegexMatch(self, pattern, text, flags=0):
        """
        find the first match in the string that matches the pattern.
        @return RegexMatch object, or None if didn't match any.
        """
        if pattern == "" or text == "":
            raise RuntimeError("Cannot do q.codetools.regex.getRegexMatches when pattern or text parameter is empty")
        pattern = self._patternFix(pattern)
        match = re.match(pattern, text, flags)
        if match:
            rm = RegexMatch()
            rm.start = match.start()
            rm.end = match.end()
            rm.founditem = match.group()
            rm.foundSubitems = match.groups()
            return rm
        else:
            return None #no match
            
    def removeLines(self,pattern,text):
        """
        remove lines based on pattern  
        """
        if pattern=="" or text=="":
            raise RuntimeError("Cannot do q.codetools.regex.removeLines when pattern or text parameter is empty")
        pattern=self._patternFix(pattern)
        return self.processLines(text,excludes=[pattern])

    def processLines(self,text,includes="",excludes=""):
        """
        includes happens first
        excludes last
        both are arrays
        """
        if includes=="":
            includes=[".*"]  #match all
        if excludes=="":
            excludes=[]  #match none
                       
        lines = text.split("\n")
        out=""
        for line in lines:
            if self.matchMultiple(includes,line) and not self.matchMultiple(excludes,line):
                out="%s%s\n" % (out,line)
        return out

    def replaceLines(self,replaceFunction,arg,text,includes="",excludes=""):
        """
        includes happens first
        excludes last
        both are arrays
        replace the matched line with line being processed by the functionreplaceFunction(arg,lineWhichMatches)
        the replace function has 2 params, argument & the matching line
        """
        if includes=="":
            includes=[".*"]  #match all
        if excludes=="":
            excludes=[]  #match none
                       
        lines = text.split("\n")
        out=""
        for line in lines:
            if self.matchMultiple(includes,line) and not self.matchMultiple(excludes,line):
                line=replaceFunction(arg,line)
            out="%s%s\n" % (out,line)
        if out[-2:]=="\n\n":
            out=out[:-1]
        return out    
    
    def findLine(self,regex,text):
        """
        returns line when found
        @param regex is what we are looking for
        @param text, we are looking into
        """

        return self.processLines(text,includes=[self._patternFix(regex)],excludes="")
    
    def getINIAlikeVariableFromText(self,variableName,text,isArray=False):
        """
        e.g. in text
        '
        test= something
        testarray = 1,2,4,5
        '
        getINIAlikeVariable("test",text) will return 'something'
        @isArray when True and , in result will make array out of 
        getINIAlikeVariable("testarray",text,True) will return [1,2,4,5]
        """
        line=self.findLine("^%s *=" % variableName,text)
        if line<>"":
            val=line.split("=")[1].strip()
            if isArray==True:
                splitted=val.split(",")
                if len(splitted)>0:
                    splitted=[ item.strip() for item in splitted]
                    return splitted
                else:
                    return [val]
            else:
                return val            
        return ""
        
    def extractFirstFoundBlock(self,text,blockStartPatterns,blockStartPatternsNegative=[],blockStopPatterns=[],blockStopPatternsNegative=[],linesIncludePatterns=[".*"],linesExcludePatterns=[],includeMatchingLine=True):
            result=self.extractBlocks(text,blockStartPatterns,blockStartPatternsNegative,blockStopPatterns,blockStopPatternsNegative,linesIncludePatterns,linesExcludePatterns,includeMatchingLine)
            if len(result)>0:
                return result[0]
            else:
                return ""


    def extractBlocks(self,text,blockStartPatterns=['.*'],blockStartPatternsNegative=[],blockStopPatterns=[],blockStopPatternsNegative=[],linesIncludePatterns=[".*"],linesExcludePatterns=[],includeMatchingLine=True):
        """
        look for blocks starting with line which matches one of patterns in blockStartPatterns and not matching one of patterns in blockStartPatternsNegative
        block will stop when line found which matches one of patterns in blockStopPatterns and not in blockStopPatternsNegative or when next match for start is found
        in block lines matching linesIncludePatterns will be kept and reverse for linesExcludePatterns
        example pattern: '^class ' looks for class at beginning of line with space behind 
        @param resultObject is of type: extensions/codetools/TextFileEditor/TextFileBlocksBase
        """
        #check types of input
        if type(blockStartPatterns).__name__<>'list' or type(blockStartPatternsNegative).__name__<>'list' or type(blockStopPatterns).__name__<>'list' \
            or type(blockStopPatternsNegative).__name__<>'list' or type(linesIncludePatterns).__name__<>'list' or type(linesExcludePatterns).__name__<>'list' :
            raise RuntimeError("Blockstartpatterns,blockStartPatternsNegative,blockStopPatterns,blockStopPatternsNegative,linesIncludePatterns,linesExcludePatterns has to be of type list")                                
        
        state="scan"
        lines=text.split("\n")
        line=""
        result=[]
        for t in range(len(lines)):
            line=lines[t]            
            #print "\nPROCESS: %s,%s state:%s line:%s" % (t,len(lines)-1,state,line)
            emptyLine = not line
            addLine = (self.matchMultiple(linesIncludePatterns,line) and not self.matchMultiple(linesExcludePatterns,line)) or emptyLine
            if state=="foundblock" and (\
                                          t==len(lines)-1 or \
                                          (self.matchMultiple(blockStopPatterns,line)  or \
                                          (self.matchMultiple(blockStartPatterns,line) and not self.matchMultiple(blockStartPatternsNegative,line)) or \
                                          (len(blockStopPatternsNegative)>0 and not self.matchMultiple(blockStopPatternsNegative,line)))\
                                        ):
                
                #new potential block found or end of file
                result.append(block) #add to results line
                if t==len(lines)-1:
                    state="endoffile"
                    if addLine:
                        block="%s%s\n" % (block,line)  
                else:
                    #have to go back to scanning
                    state="scan"
                    if blockStartPatterns==blockStopPatterns:
                        #otherwise we would start match again                    
                        if t<len(lines):
                            t=t+1
                            line=lines[t]
                        else:
                            line=""                          
                            
            if state=="foundblock":
                #print "foundblock %s" % self.matchMultiple(linesIncludePatterns,line)
                if addLine:
                    block="%s%s\n" % (block,line)                            

            if state=="scan" and self.matchMultiple(blockStartPatterns,line) and not self.matchMultiple(blockStartPatternsNegative,line):
                #found beginning of block
                state="foundblock"
                blockstartline=t
                block=""
                if includeMatchingLine:
                    if addLine:
                        block=line+"\n"
                                            
            
        return result


    
if __name__ == '__main__':
    content=pymonkey.q.system.fs.fileGetContents("examplecontent1.txt")
    rt=RegexTools()
    print rt.getClassName("class iets(test):")
    #content="class iets(test):"
    regexmatches=rt.getRegexMatches(r"(?m)(?<=^class )[ A-Za-z0-9_\-]*\b",content)  #find all occurences of class and find positions
    
    ipshell()