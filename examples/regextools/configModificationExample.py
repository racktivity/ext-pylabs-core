
from pymonkey.InitBase import *
from pymonkey.Shell import *


q.application.appname="testconfigmodif"

q.application.start()
q.qshellconfig.interactive=True

def findBlocks():
    tool=q.codetools.getTextFileEditor("examplecontent1.txt")
    textfile= tool.extractBlocks(blockStartPatterns=["^class "],blockStopPatternsNegative=["^ "])
    print textfile
    print

#A good tool to try out the regular expressions is regexbuddy, ideal to use with this tool

def replaceLinesTest():
    #REMARK FOR THE EJABBERDCONFIG IS A DANGEROUS THING TO DO BECAUSE FORMAT IS NOT LINE BASED
    print "lets now modify the ejabberd config file for the hosts section"
    tool=q.codetools.getTextFileEditor("exampleEjabberdConfig.cfg")
    
    def modifyHostLine(argument,line):
        #find [...] and replace with new hosts in total
        if line.find("example")<>-1:
            line=q.codetools.regex.replace(regexFind="\[.*\]",regexFindsubsetToReplace="\[.*\]",replaceWith="[\"example.org\"]",text=line)
        return line

    #will look for only 1 line which matches the host syntax, that one line will then be processed  \
    print "\n\nWILL REPLACE HOSTS LINE TO: example.org only"
    tool.replace1LineFromFunction(modifyHostLine,"",["^ *{.*hosts.*,"])  
    print tool.content
    print "\n\n"
    print "WILL NOW REPLACE HOSTS LINE TO: {hosts, [\"example.net\", \"example.com\", \"example.org\""
    #if you know in advance what you want to replace this with is much easier
    tool.replace1Line("{hosts, [\"example.net\", \"example.com\", \"example.org\"]}.",includes=["^ *{.*hosts.*,"]) #put the original content back)
    print tool.content
##replaceLinesTest()


def aNonLineBasedExample():
    tool=q.codetools.getTextFileEditor("exampleEjabberdConfig.cfg")
    editor=tool.getTextCharEditor()
    editor.matchBlocksDelimiter("^[ \t]*{[ \r\n\t]*listen[ \r\n\t]*","listen")
    editor.matchBlocksPattern(startpattern="^[ \t]*%%",stoppattern="\n",blockname="comment")#will mark the comment lines    
    ##print editor.get1Block("listen")
    ##print editor.get1Block("comment")#needs to fail
    ##print editor.getBlock("comment",5)#needs to work
    ##editor.delete1Block("listen")
    ##editor.deleteBlocks("comment")
    #editor.replace1Block("listen","AAAAAAAAAA\n")
    print editor.get1Block("listen")
    editor.replaceBlock("listen",1,"AAAAAAAAAA\n")
    #editor.printtext()
    print "will now be replaced"
    print editor.get1Block("listen")
    #ipshell()
    
aNonLineBasedExample()




#textfile=tool.extractBlocks(blockStartPatterns=["^ *{.*hosts.*,"],blockStopPatterns=["^ *%","^ *{","^ *[","^ *"])
#print textfile

    
q.application.stop()
