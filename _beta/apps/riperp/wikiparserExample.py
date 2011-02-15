from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="setup wizardrunner"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True

class Parser():
    def __init__(self, wikifilePath):
        self.wikifilePath=wikifilePath
        self.wikifilePathWorking="%s.working" % self.wikifilePath
        self.content=pylabs.q.system.fs.fileGetContents(wikifilePath)
    
    def reload(self):
        self.content=pylabs.q.system.fs.fileGetContents(self.wikifilePathWorking)
        
    def do(self):
        self.step1RemoveComments()
        self.step3ProcessMacro()
        #all other steps
        
    def _setContent(self, content):
        self.content=content
        q.system.fs.writeFile(self.wikifilePathWorking, self.content) 
        
    def step1RemoveComments(self):
        #removes comments from content
        self._setContent(q.codetools.regex.replace(regexFind=r"""\#(\w).*""", regexFindsubsetToReplace=".*", replaceWith="",text= self.content))

    def step2DownloadRemoteImages(self):
        #process like in Step3ProcessMacro
        #see if remote image, if yes downoad image to same dir (check imagename not there yet, if there raise error)
        #replace text to work with local image
        pass

    def step3ProcessMacro(self):
        #!http://asite.com/picture.jpg! 
        te=q.codetools.getTextFileEditor(self.wikifilePathWorking)
        tce=te.getTextCharEditor()
        blockname="macro"
        tce.matchBlocksDelimiter(startpattern="{macro",blockname=blockname,delimiteropen="{",delimiterclose="}")
        highest=tce.getHighestBlockNr(blockname)
        for t in range(0, highest):
            blockcontent= tce.getBlock(blockname, t+1)
            newcontent="MACRO: TESTREPLACEDMACRONeedsToBecomeTaskletExecution"
            tce.replaceBlock(blockname, t+1, newcontent)
        tce.printtext()
        tce.save()
        self.reload()
        
    def step4processMacroInclude(self):
        #process includes
        pass

    def step4processMacroChildren(self):
        pass
        
    def step5tokenize(self):
        #rewrite file that everything comes on line per line
        #introduce special TOKEN CHARS like NL (New Line)
        state="start"
        result=[]
        for line in self.content.split("/n"):
            line2=line.strip().lower()
            if state=="codeblock":
                codeblContent="%s%s//n"%(codeblContent, line)
                
            if state=="start" and q.codetools.regex.match("h\d\.",line2):
                #found header
                headernr=line2[1]
                line3=line2[2:]
                result.append("HEADER|%s|%s"%(headernr, line3))
                result.append("NL")
                state="found"

            regex="^\*+"
            if state=="start" and q.codetools.regex.match(regex,line2):
                #found bullet
                bullets=q.codetools.regex.findOne(regex,line2)
                level=len(bullets)
                line3=q.codetools.regex.replace(regexFind=regex, regexFindsubsetToReplace=".*", replaceWith="", text=line2)                
                result.append("*|%s|%s"%(level, line3))
                result.append("NL")
                state="found"

            regex="^\#+"
            if state=="start" and q.codetools.regex.match(regex,line2):
                #found list
                bullets=q.codetools.regex.findOne(regex,line2)
                level=len(bullets)
                line3=q.codetools.regex.replace(regexFind=regex, regexFindsubsetToReplace=".*", replaceWith="", text=line2)                
                result.append("#|%s|%s"%(level, line3))
                result.append("NL")
                state="found"

            regex="\*(\w).*.(\w)\*"
            if state=="start" and q.codetools.regex.match(regex,line2):  #find bold text, we only support on 1 line
                #find line before bold
                comment=q.codetools.regex.findOne(regex,line2)
                linebefore=line2.split(comment)[0]
                lineafter=line2.split(comment)[1]
                comment=comment[1:-1] #remove comment signs
                result.append("T`|%s|%s"%("", linebefore))  #T from text
                result.append("COMMENT|%s|%s"%("", comment))
                result.append("T|%s|%s"%("", lineafter))
                result.append("NL")
                state="found"
                
            #do same for italic, ...
                
            if state=="start" and q.codetools.regex.match("{.?code.?}",line2):            
                state="codeblock"
                codeblContent=""
                
            if state=="start":
                #normal paragraph
                result.append("P|%s|%s"%("", line2))
                result.append("NL")                
                
            if state=="codeblock" and q.codetools.regex.match("{.?code.?}",line2):
                state="start"
                codeblContent=""
                result.append("CODEBLOCK||%s"%codeblContent)
                result.append("NL")
        #@todo join result and write to content and reload

    def step6ProcessTokens(self):
        #process tokens and automate creation of doc
        pass
    
p=Parser("example.wiki")
p.do()
