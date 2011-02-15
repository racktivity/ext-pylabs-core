from pylabs.InitBase import q, i
from pylabs.Shell import *
import os
q.qshellconfig.interactive=True

NEWLINE = "NL||"

class Parser(object):

    def __init__(self, wikifilePath, macrotaskletspath=None, taskletengine=None, workdir=None):
        self.wikifilePath=wikifilePath
        self.wikidir = q.system.fs.getDirName(os.path.abspath(self.wikifilePath))
        if not workdir:
            self.workdir = q.system.fs.getTmpFilePath()
            q.system.fs.remove(self.workdir)
        else:
            self.workdir = workdir
        q.system.fs.createDir(self.workdir)
        self.wikifilePathWorking = "%s.working" % self.wikifilePath
        self.wikifilePathTokenized = q.system.fs.joinPaths(self.workdir, "%s.token" % q.system.fs.getBaseName(self.wikifilePath))
        if macrotaskletspath:
            self.te = q.taskletengine.get(macrotaskletspath)
        elif taskletengine:
            self.te = taskletengine
        else:
            raise RuntimeError("Either macrotaskletspath or taskletengine should be passed to %s" % self.__class__)
        self.content=pylabs.q.system.fs.fileGetContents(wikifilePath)
    
    def reload(self):
        self.content=pylabs.q.system.fs.fileGetContents(self.wikifilePathWorking)
        
    def do(self, outputfile):
        self.stepRemoveComments()
        self.stepProcessMacro()
        tokens = self.stepTokenize()
        self.stepProcessTokens(tokens, outputfile)
        
    def _setContent(self, content):
        self.content=content
        q.system.fs.writeFile(self.wikifilePathWorking, self.content) 
        
    def stepRemoveComments(self):
        #removes comments from content
        self._setContent(q.codetools.regex.replace(regexFind=r"\#(\w).*", regexFindsubsetToReplace=".*", replaceWith="",text= self.content))

    def stepProcessImage(self, image):
        imagepath = q.system.fs.joinPaths(self.wikidir, image)
        basename = q.system.fs.getBaseName(imagepath)
        name, extension = os.path.splitext(basename)
        destname = q.system.fs.joinPaths(self.workdir, basename)
        counter = 1
        while q.system.fs.exists(destname):
            basename = "%s_%s%s" % (name, counter, extension)
            destname = q.system.fs.joinPaths(self.workdir, basename)
            counter +=1
        if q.system.fs.exists(imagepath):
            q.system.fs.copyFile(imagepath, destname)
        else:
            try:
                q.system.net.download(image, destname)
            except:
                raise RuntimeError("Image %s does not exists or failed to download" % image)
        return "IMAGE||%s" % basename

    def stepProcessLink(self, linkcontent):
        splitted = linkcontent.split("|")
        name = linkcontent
        link = linkcontent
        if len(splitted) > 1:
            name = splitted[0]
            link = splitted[1]
        return "LINK|%s|%s" % (name, link)

    def stepProcessMacro(self):
        #!http://asite.com/picture.jpg! 
        te=q.codetools.getTextFileEditor(self.wikifilePathWorking)
        tce=te.getTextCharEditor()
        blockname="macro"
        tce.matchBlocksDelimiter(startpattern="{macro",blockname=blockname,delimiteropen="{",delimiterclose="}")
        if not tce.getBlockNames():
            #no blocks found just return
            return
        highest=tce.getHighestBlockNr(blockname)
        for t in range(0, highest):
            blockcontent= tce.getBlock(blockname, t+1)
            config = blockcontent.split(":",1)[1]
            items = config.split()
            tags = list()
            params = dict()
            for item in items:
                keypair = item.split(":")
                if len(keypair) == 1:
                    tags.append(keypair[0])
                else:
                    params[keypair[0]] = keypair[1]
            self.te.execute(params, tags=tags)
            
            newcontent=params.get("result", "No Matching Macro")
            tce.replaceBlock(blockname, t+1, newcontent)
        tce.save()
        self.reload()
        
    def stepProcessInclude(self, page):
        import glob
        
        pagepath = q.system.fs.joinPaths(self.wikidir, page)
        print pagepath
        fs = glob.glob("%s*" % pagepath)
        f = None
        for f in fs:
            if f.endswith("txt") or f.endswith("wiki"):
                break
        else:
            raise RuntimeError("Failed to include %s" % page)
            q.eventhandler.raiseWarning("Failed to include %s" % page)
            return []
        p = Parser(f, taskletengine=self.te)
        p.stepRemoveComments()
        p.stepProcessMacro()
        return p.stepTokenize()

    def stepProcessMacroChildren(self):
        pass

    def _parseMarkup(self, line):
        tokens = {"BOLD":"\*", "ITALIC":"_", "STRIKE":"\-", "UNDER": "\+"}
        result = list()
        for tokenname, token in tokens.iteritems():
            regex=r"(.*[^\\])%(token)s(\w.*\w)%(token)s(.*)" % {'token': token}
            match = q.codetools.regex.getRegexMatch(regex, line)
            if match:  #find bold text, we only support on 1 line
                #find line before bold
                linebefore, comment, lineafter=match.foundSubitems
                if linebefore:
                    before = self._parseMarkup(linebefore)
                    if before:
                        result.extend(before)
                    else:
                        result.append("T||%s" % (linebefore))  #T from text
                result.append("%s||%s" % (tokenname, comment))
                if lineafter:
                    after = self._parseMarkup(lineafter)
                    if after:
                        result.extend(after)
                    else:
                        result.append("T||%s" % (lineafter))
                result.append(NEWLINE)
        return result

    def stepTokenize(self):
        #rewrite file that everything comes on line per line
        #introduce special TOKEN CHARS like NL (New Line)
        state="start"
        result=[]
        for line in self.content.splitlines():
            line2 = line.strip().lower()
            
            if not line2:
                result.append(NEWLINE)
                continue
            
            if state == "start":
                if q.codetools.regex.match("h\d\.",line2):
                    #found header
                    headernr = line2[1]
                    line3 = line2[3:]
                    result.append("HEADER|%s|%s"%(headernr, line3))
                    result.append(NEWLINE)
                    continue

                #bullets and lists
                matches = False
                for marker in "*#":
                    regex = r"^(\%s+)\s(.+)" % marker
                    match = q.codetools.regex.getRegexMatch(regex, line2)
                    if match:
                        #found bullet
                        bullets, text = match.foundSubitems
                        level=len(bullets)
                        result.append("%s|%s|%s"%(marker, level, text))
                        result.append(NEWLINE)
                        matches = True
                        break
                if matches:
                    matches = False
                    continue
                
                matches = False
                regexs = {r"\{.?include\s+(.*)}": self.stepProcessInclude, 
                            r"^\!(.*)\!": self.stepProcessImage,
                            r"^\[(.*)\]": self.stepProcessLink,}
                for regex, func in regexs.iteritems():
                    match = q.codetools.regex.getRegexMatch(regex, line)
                    if match:
                        res = func(match.foundSubitems[0])
                        if isinstance(res, list):
                            result.extend(res)
                        else:
                            result.append(res)
                        matches = True
                        break
                if matches:
                    matches = False
                    continue
                
                if q.codetools.regex.match("{.?code.?}",line2):
                    state="codeblock"
                    continue
                
                #normal paragraph
                lines = self._parseMarkup(line)
                if lines:
                    result.append("P|%s|%s"%("", ""))
                    result.extend(lines)
                else:
                    result.append("P|%s|%s"%("", line))
                result.append(NEWLINE)
                continue
                
            elif state=="codeblock":
                if q.codetools.regex.match("{.?code.?}",line2):
                    state="start"
                    result.append(NEWLINE)
                    continue
                else:
                    result.append("T||%s" % line)
                    result.append(NEWLINE)
                    continue
        return result
        

    def stepProcessTokens(self, tokens, outputfile):
        content = "\n".join(tokens)
        q.system.fs.writeFile(self.wikifilePathTokenized, content)
        converter = q.system.fs.joinPaths(q.dirs.binDir, 'wiki_tokenconverter')
        converter += " -f '%s' -o '%s'" % (self.wikifilePathTokenized, outputfile)
        q.system.process.execute(converter)
        q.system.fs.deleteDirTree(self.workdir)


if __name__ == '__main__':
    q.application.appname="wikitest"
    q.application.start()
    p=Parser("example.wiki", "tasklets")
    p.do()
    q.application.stop()
