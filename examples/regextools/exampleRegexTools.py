import sys
from pylabs.InitBase import *
from pylabs.Shell import *


q.application.appname="testregex"

q.application.start()

content=pylabs.q.system.fs.fileGetContents("examplecontent1.txt")

def matchRegexes():
    text="ThisIs A Test"
    print q.codetools.regex.match(pattern=" A ",text=text)
    print q.codetools.regex.matchMultiple(patterns=[" a","Test"],text=text)
    print q.codetools.regex.matchMultiple(patterns=[" a"],text=text)
    
#matchRegexes()

def findclassnames():
    """
    use of regex find in text, fill all occurences of classnames and return as array
    """
    regexmatches=q.codetools.regex.findAll(pattern=r"(?m)(?<=^class )[ A-Za-z0-9_\-]*\b",text=content) 
    for item in regexmatches:
        q.console.echo(item)

#findclassnames()

def processLinesTest():
    #process lines out of testfile, find first all class, def and comment lines, then remove ##comment lines
    print q.codetools.regex.processLines(text=content,includes=["^class ","^def ","^#"],excludes=["^##"])

#processLinesTest()
    
def extractBlocksExample():
    print "next statement finds all classblocks out of content"
    items=q.codetools.regex.extractBlocks(text=content,blockStartPatterns=["^class "],blockStopPatternsNegative=["^ "]) 
    #ipshell()
    for t in range(len(items)):
        print "class %s\n%s\n\n" % (t+1,items[t])
    print "**************************************************************\n\n"
    print "now ignore comment rows in blocks (only when at start of line)"
    classes=q.codetools.regex.extractBlocks(text=content,blockStartPatterns=["^class "],blockStopPatternsNegative=["^ "],linesExcludePatterns=["^ +\#"]) 
    for t in range(len(classes)):
        print "Class %s\n%s\n\n" % (t+1,classes[t])
    print "**************************************************************\n\n"
    print "find \"\"\" blocks at start of line in file (e.g. file comment)"
    items=q.codetools.regex.extractBlocks(text=content,blockStartPatterns=["^\"\"\""],blockStopPatterns=["^\"\"\""],includeMatchingLine=False) 
    for t in range(len(items)):
        print "%s\n%s\n\n" % (t+1,items[t])
        

extractBlocksExample()        
        
qshell()       
    
q.application.stop()