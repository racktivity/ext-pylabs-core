from pylabs.Shell import *
from pylabs import q
from TextLineEditor import TextLineEditor
from TextCharEditor import TextCharEditor

        
class TextFileEditor:
    """
    Allow manipulate of a text file
    ideal to manipulate e.g. config files
    BE CAREFULL, CHANGES ON textfileeditor and chareditor can overwrite each other
    """
    def __init__(self,filepath):
        self.filepath=filepath
        self.content=q.system.fs.fileGetContents(filepath)
        
    def getTextLineEditor(self,blockStartPatterns=['.*'],blockStartPatternsNegative=[],blockStopPatterns=[],blockStopPatternsNegative=[]):
        """
        look for blocks starting with line which matches one of patterns in blockStartPatterns and not matching one of patterns in blockStartPatternsNegative
        block will stop when line found which matches one of patterns in blockStopPatterns and not in blockStopPatternsNegative or when next match for start is found
        @return an editor class which allows manipulation of the text based on lines ("\n")
        """
        textLineEditor=TextLineEditor(self.content,self.filepath)
        #@todo does not work anymore
        raise RuntimeError("Not implemented")
        q.codetools.regex.extractBlocks(textfile.text,blockStartPatterns,blockStartPatternsNegative,blockStopPatterns,blockStopPatternsNegative,\
                                        includeMatchingLine=True,resultObject=textfile)
        return textLineEditor
    
    def getTextCharEditor(self):        
        te=TextCharEditor(self.content,self)
        self._textCharEditorActive=True
        return te
    
    def find1Line(self,includes="",excludes=""):
        """
        if moren than 1 line or 0 line error will be raised
        @param includes are include patters (regular expressions)
        @param excludes
        @return [linenr,line]
        """
        q.logger.log("try to find 1 line which matches the specified includes %s & excludes %s" % (includes,excludes),8)
        result=[]
        linenr=0
        if includes=="":
            includes=[".*"]  #match all
        if excludes=="":
            excludes=[]  #match none
        for line in self.content.split("\n"):
            if q.codetools.regex.matchMultiple(includes,line) and not q.codetools.regex.matchMultiple(excludes,line):
                result.append(line)
                linenrfound=linenr
                linefound=line
            linenr+=1
            
        if len(result)==0:
            raise RuntimeError("Could not find a line matching %s and not matching %s in file %s" % (includes,excludes,self.filepath))
        if len(result)>1:
            raise RuntimeError("Found more than 1 line matching %s" % (patterns,self.filepath))
        return [linenrfound,linefound]
    
    def replaceLinesFromFunction(self,replaceFunction,argument,includes="",excludes=""):
        """
        includes happens first
        excludes last
        both are arrays
        @param argument which is going to be give to replacefunction
        @replaceFunction is the replace function has 2 params, argument & the matching line, returns the processed line
        replace the matched line with line being processed by the functionreplaceFunction(argument,lineWhichMatches)
        
        """   
        #@todo add good logging statements everywhere
        self.content=q.codetools.regex.replaceLines(replaceFunction,argument, self.content,includes,excludes)
        self.save()

    def replace1LineFromFunction(self,replaceFunction,argument,includes="",excludes=""):
        """
        same as with replaceLinesFromFunction, but only 1 line will be matched
        
        """   
        self.find1Line(includes,excludes) #make sure only 1 line can match otherwise error will be raised
        self.replaceLinesFromFunction(replaceFunction,argument,includes,excludes)      
        self.save()

    def replace1Line(self,newcontent,includes="",excludes=""):
        """
        includes happens first
        excludes last
        both are arrays
        replace matching lines with new content
        """
        self.find1Line(includes,excludes) #make sure only 1 line can match otherwise error will be raised
        self.replaceLines(newcontent,includes,excludes)               
        self.save()
        
        
    def replaceLines(self,newcontent,includes="",excludes=""):
        """
        includes happens first
        excludes last
        both are arrays
        replace matching lines with new content
        """
        def replfunc(newline,line):
            return newline
        self.replaceLinesFromFunction(replfunc,newcontent,includes,excludes)                    
        self.save()

    def deleteLines(self,pattern):
        """
        remove lines which match the pattern (only 1 pattern)
        """
        self.content=q.codetools.regex.removeLines(patterns,self.content)
        self.save()
        

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
        self.content=q.codetools.regex.replace(regexFind,regexFindsubsetToReplace,replaceWith,self.content)
        self.save()
                
    
    def getRegexMatches(self, pattern):
        result= q.codetools.regex.getRegexMatches(pattern, self.content)
        return result
            
    def save(self,filepath=None):
        """
        write the manipulated file to a new path or to the original
        """
        if filepath==None:
            filepath=self.filepath
        if filepath==None:
            raise RuntimeError("Cannot write the textfile because path is None")
        q.system.fs.writeFile(filepath,self.content)            
        