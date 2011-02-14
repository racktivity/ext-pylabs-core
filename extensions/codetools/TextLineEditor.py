from pymonkey.Shell import *
from pymonkey import q


class TextLineEditor():
    """
    represents a piece of text but broken appart in blocks/tokens
    this one works on a line basis
    """
    
    def __init__(self,text):
        self.lines=[]
        self._higestblocknr={} #key is name of block, the value is the last used blocknr
        
    def getNrLines(self):
        return len(self.linenr)
        
    def existsBlock(self,blockname):
        return self._higestblocknr.has_key(blockname)
    
    def getBlockNames(self):
        return self._higestblocknr.keys()
    
    def matchBlocks(self,blockname,blockStartPatterns=['.*'],blockStartPatternsNegative=[],blockStopPatterns=[],blockStopPatternsNegative=[]):
        """
        walk over blocks which are marked as matched and split blocks in more blocks depending criteria
        can be usefull to do this multiple times (sort of iterative) e.g. find class and then in class remove comments
        """
        blocks=self.getBlockNames()
        if blocks==[]:
            #starting situation
            self.matchBlock(None,blockStartPatterns,blockStartPatternsNegative,blockStopPatterns,blockStopPatternsNegative)
        for block in self.blocks:
            self.matchBlock(block.startline,blockStartPatterns,blockStartPatternsNegative,blockStopPatterns,blockStopPatternsNegative)
        
    def _matchBlock(blockname,blocknr,blockStartPatterns=['.*'],blockStartPatternsNegative=[],blockStopPatterns=[],blockStopPatternsNegative=[]):
        """
        split block with startline
        look for blocks starting with line which matches one of patterns in blockStartPatterns and not matching one of patterns in blockStartPatternsNegative
        block will stop when line found which matches one of patterns in blockStopPatterns and not in blockStopPatternsNegative or when next match for start is found
        example pattern: '^class ' looks for class at beginning of line with space behind 
        """
        #check types of input
        if type(blockStartPatterns).__name__<>'list' or type(blockStartPatternsNegative).__name__<>'list' or type(blockStopPatterns).__name__<>'list' \
            or type(blockStopPatternsNegative).__name__<>'list':
            raise RuntimeError("Blockstartpatterns,blockStartPatternsNegative,blockStopPatterns,blockStopPatternsNegative has to be of type list")
                                          
        
        if startline==None:
            text=self.text
        else:
            if len(q.codetools.regex.extractBlocks(text,blockStartPatterns,blockStartPatternsNegative,blockStopPatterns,blockStopPatternsNegative))<2:
                q.logger.log("block with startline %s cannot be extracted because no candidates found." % startline,8)
                return False
            text=self.getBlock(blockname,blocknr)
            self.deleteBlock(blockname,blocknr)

        state="scan"
        lines=text.split("\n")
        line=""
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
                self.addBlock(block,True,startline=blockstartline,endline=t-1)                            
                            
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
                else:
                    self.addBlock(line,False,startline=t,endline=t) #add a no match
                    pass
                    
            elif state=="scan":
                #scanning but no match
                self.addBlock(line,False,startline=t,endline=t)
                
            self._sort()
            
    def getNextBlockNr(self,name):
        if not self._higestblocknr.has_key(name):
            self._higestblocknr[name]=1
        else:
            self._higestblocknr[name]+=1
        return self._higestblocknr[name]

    def getHighestBlockNr(self,name):
        if not self._higestblocknr.has_key(name):
            raise RuntimeError("Cound not find block with name %s" % name)
        else:
            return self._higestblocknr[name]
    
    def appendBlock(self,text,blockname=""):
        """
        @param match means block was found and matching
        """
        blocknr=self.getNextBlockNr(blockname)
        for line in text.split("\n"):
            self.lines.append(LTLine(line,blockname,blocknr))
        
    def insertBlock(self,linenr,text,blockname="",blocknr=None):
        """
        block will be inserted at linenr, means line with linenr will be moved backwards
        """
        if blocknr==None:
            blocknr=self.getNextBlockNr(blockname)
        for line in text.split("\n").revert():
            self.lines.insert(linenr,LTLine(line,blockname,blocknr))            
            
    def deleteBlock(self,blockname,blocknr=None):
        """
        mark block as not matching based on startline
        """
        self.getBlock(blockname,blocknr) #just to check if block exists
        self.lines=[line for line in self.lines if (line.name<>blockname and (blocknr==None or line.blocknr==blocknr))]
        
        
    def getBlock(self,blockname,blocknr):
        """
        get block based on startline
        """
        block=[line for line in self.lines (line.name==blockname and line.blocknr==blocknr)]
        if len(block)==0:
            raise RuntimeError("Cannot find block from text with blockname %s and blocknr %s" % (blockname,blocknr))
        return str.join(block)
        
    def replaceBlock(self,blockname,blocknr,text):
        """
        set block based on startline with new content
        """
        self.deleteBlock(blockname,blocknr)
        self.insertBlock(getFirstLineNrForBlock(self,blockname,blocknr),text,blockname,blocknr)
        
        
    def getFirstLineNrForBlock(self,blockname,blocknr):
        for linenr in range(len(self.lines)):
            line=self.lines[linenr]
            if line.name==blockname and line.blocknr==blocknr:
                return linenr
        raise RuntimeError("Could not find block with name %s and blocknr %s" % (blockname,blocknr))
    
       

    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        if len(self.blocks)>0:
            return string.join([str(block) for block in self.blocks])
        else:
            return ""

class LTLine():
    def __init__(self,line,blockname="",blocknr=0):
        """        
        @param no blockname means ignore
        """
        self.name=blockname
        self.line=text
        self.blocknr=blocknr
     
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        if self.name<>"":
            text="+ %s %s: %s\n" % (self.name,self.blocknr,self.line)
            return text
        else:
            text="- %s\n" % (self.line)
            return text
        
        
