from pymonkey import q
from pymonkey.Shell import *
import os
import json
import re, htmlentitydefs
#q.qshellconfig.interactive=True


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                if text[1:-1] == "nbsp":
                    return " "
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    text = re.sub("&#?\w+;", fixup, text)
    d = re.escape(r"[]{}+\*")
    return re.sub(r"\\([%s])" % d, "\g<1>", text)

class Parser(object):

    def __init__(self, startWikiFilePath, wikidir, macrotaskletspath=None, resultsdir=None, taskletengine=None, workdir=None):
        """
        @param startWikiFilePath is start file for which a doc will be generated, is in confluence format
        @param wikidir is dir in which all wiki documents reside
        @param macrotaskletspath is dir in which all tasklets reside which implement the macro's
        @param resultsdir is directory in which resulting documents will be stored                
        """
        self.wikifilePath=startWikiFilePath
        self.wikidir = wikidir
        self.resultsdir=resultsdir
        self._errors = list()
        if not workdir:
            self.workdir = q.system.fs.getTmpFilePath()
            q.system.fs.remove(self.workdir)
        else:
            self.workdir = workdir
        q.system.fs.createDir(self.workdir)
        self.wikifilePathWorking = "%s.working" % self.wikifilePath
        self.wikifilePathTokenized = q.system.fs.joinPaths(self.workdir, "%s.token" % q.system.fs.getBaseName(self.wikifilePath))
        self._errorlog = q.system.fs.joinPaths(self.resultsdir, "errors.log")
        if macrotaskletspath:
            self._te = q.taskletengine.get(macrotaskletspath)
        elif taskletengine:
            self._te = taskletengine
        else:
            raise RuntimeError("Either macrotaskletspath or taskletengine should be passed to %s" % self.__class__)
        self.content=pymonkey.q.system.fs.fileGetContents(self.wikifilePath)
        self.NEWLINE = "NL||"

    def logError(self, log):
        self._errors.append(log)
    
    def reload(self):
        self.content=pymonkey.q.system.fs.fileGetContents(self.wikifilePathWorking)
        
    def do(self):
        tokens = list()
        if self.content:
            self.stepRemoveComments()
            self.stepProcessMacro()
            tokens = self.stepTokenize()
        content = "\n".join(tokens)
        q.system.fs.writeFile(self.wikifilePathTokenized, content)
        q.system.fs.writeFile(self._errorlog, "\n".join(self._errors))
        
    def _setContent(self, content):
        self.content=content
        q.system.fs.writeFile(self.wikifilePathWorking, self.content) 
        
    def stepRemoveComments(self):
        #removes comments from content
        if self.content:
            self.content = q.codetools.regex.replace(regexFind=r"\#(\w).*", regexFindsubsetToReplace=".*", replaceWith="",text= self.content)
        self._setContent(self.content)

    def stepProcessImage(self, token, image):
        options = ""
        imageparts = image.split("|")
        image = imageparts[0]
        if len(imageparts) > 1:
            options = imageparts[1]
        imagepath = q.system.fs.joinPaths(self.wikidir, image)
        imagepath2 = q.system.fs.joinPaths(q.system.fs.getDirName(self.wikifilePath), image)
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
        elif q.system.fs.exists(imagepath2):
            q.system.fs.copyFile(imagepath2, destname)
        else:
            try:
                q.system.net.download(image, destname)
            except:
                raise RuntimeError("Image %s does not exists or failed to download" % image)
        return "IMAGE|%s|%s" % (options, basename)

    def stepProcessLink(self, token, linkcontent):
        splitted = linkcontent.split("|")
        name = linkcontent
        link = linkcontent
        if len(splitted) > 1:
            name = splitted[0]
            link = splitted[1]
        return "LINK|%s|%s" % (name, link)

    def stepProcessMacro(self):
        SPECIAL_MACRO = ("include", "tokenized")
        te=q.codetools.getTextFileEditor(self.wikifilePathWorking)
        tce=te.getTextCharEditor()
        blockname="macro"
        tce.matchBlocksDelimiter(startpattern="{",blockname=blockname,delimiteropen="{",delimiterclose="}")
        if not tce.getBlockNames():
            #no blocks found just return
            return
        highest=tce.getHighestBlockNr(blockname)
        for t in range(0, highest):
            blockcontent= tce.getBlock(blockname, t+1).strip("{}")
            macroconfig = blockcontent.split(":",1)
            items = list()
            if len(macroconfig) < 1:
                self.logError("Unsupported macro %s" % blockcontent)
                tce.deleteBlock(blockname,t+1)
                continue
            elif macroconfig[0] in SPECIAL_MACRO:
                continue
            elif macroconfig[0] == "MACRO":
                items = macroconfig[1].split()
            else:
                items = macroconfig[0].split()
            tags = ['macro']
            params = dict()
            for item in items:
                keypair = item.split(":")
                if len(keypair) == 1:
                    tags.append(keypair[0])
                else:
                    params[keypair[0]] = keypair[1]
            self._te.execute(params, tags=tags)
            
            newcontent=params.get("result")
            if newcontent is None:
                tce.deleteBlock(blockname,t+1)
                self.logError("Macro %s did not return data" % macroconfig)
            else:
                tce.replaceBlock(blockname, t+1, newcontent)
        tce.save()
        self.reload()
        
    def stepProcessInclude(self, page):
        
        pageparts = page.split(":")
        space = ""
        pagename = ""
        if len(pageparts) == 2:
            space, pagename = pageparts
        else:
            pagename = pageparts[0]
        pagepath = q.system.fs.joinPaths(self.wikidir, space)
        for f in q.system.fs.listFilesInDir(pagepath, filter="%s*" % pagename, recursive=True):
            if f.endswith("txt") or f.endswith("wiki"):
                break
        else:
            error = "Failed to include %s" % page
            self.logError(error)
            return []
            
        p = Parser(f, self.wikidir, resultsdir=self.resultsdir, taskletengine=self._te, workdir=self.workdir)
        tokens = list()
        if p.content:
            p.stepRemoveComments()
            p.stepProcessMacro()
            tokens = p.stepTokenize()
        return tokens

    def stepProcessMacroChildren(self):
        pass

    def _parseMarkers(self, line):
        tokenize = lambda t,l: "%s||%s" % (t, unescape(l))
        tokens =   {"BOLD":("\*", "\*", tokenize), 
                    "ITALIC":("_", "_", tokenize), 
                    "STRIKE":("\-", "\-", tokenize), 
                    "UNDER": ( "\+", "\+", tokenize),
                    "IMAGE": ( "\!", "\!", self.stepProcessImage),
                    "LINK": ( "\[", "\]", self.stepProcessLink)}
        result = list()
        for tokenname, (token1, token2, func) in tokens.iteritems():
            regex=r"(^|.*\s)%(token1)s(\w.*\w)%(token2)s($|\s.*)" % {'token1': token1, 'token2': token2}
            match = q.codetools.regex.getRegexMatch(regex, line)
            if match:  #find bold text, we only support on 1 line
                #find line before bold
                linebefore, comment, lineafter=match.foundSubitems
                if linebefore:
                    before = self._parseMarkers(linebefore)
                    if before:
                        result.extend(before)
                    else:
                        result.append("T||%s" % (unescape(linebefore)))  #T from text
                result.append(func(tokenname, comment))
                if lineafter:
                    after = self._parseMarkers(lineafter)
                    if after:
                        result.extend(after)
                    else:
                        result.append("T||%s" % (unescape(lineafter)))
                result.append(self.NEWLINE)
        return result
    
    def stepProcessTableLine(self, line, table):
        delimeter = "|"
        if line.startswith("||"):
            delimeter = "||"
        line = line.strip(delimeter)
        table[len(table)+1] = line.split(delimeter)

    def stepTokenize(self):
        #rewrite file that everything comes on line per line
        #introduce special TOKEN CHARS like NL (New Line)
        state = "start"
        result = list()
        table = dict()
        for line in self.content.splitlines():
            line2 = line.strip().lower()
            if not line2:
                result.append(self.NEWLINE)
                continue
                
            istable = q.codetools.regex.match("^\|.*\|$", line2)
            
            if state == "table":
                if istable:
                    self.stepProcessTableLine(line, table)
                    continue
                else:
                    state = "start"
                    result.append("TABLE||%s" % json.dumps(table))
                    table = dict()
            
            elif state == "start":
                if istable:
                    state = "table"
                    self.stepProcessTableLine(line, table)
                    continue
                if q.codetools.regex.match("h\d\.",line2):
                    #found header
                    line = line.strip()
                    headernr = line[1]
                    line3 = unescape(line[3:])
                    result.append("HEADER|%s|%s"%(headernr, line3))
                    continue

                #bullets and lists
                matches = False
                for marker in "*#":
                    regex = r"^(\%s+)\s(.+)" % marker
                    match = q.codetools.regex.getRegexMatch(regex, line)
                    if match:
                        #found bullet
                        bullets, text = match.foundSubitems
                        level=len(bullets)
                        result.append("%s|%s|%s"%(marker, level, unescape(text)))
                        matches = True
                        break
                if matches:
                    matches = False
                    continue
                
                matches = False
                regexs = {r"\{.?include[:|\s+](.*)\}": self.stepProcessInclude, }
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
                
                if q.codetools.regex.match("{.?tokenized.?}",line2):
                    state="tokenized"
                    continue
                
                #normal paragraph
                lines = self._parseMarkers(line)
                if lines:
                    result.append("P||")
                    result.extend(lines)
                else:
                    result.append("P||%s" % (unescape(line)))
                result.append(self.NEWLINE)
                continue
                
            elif state=="codeblock":
                if q.codetools.regex.match("{.?code.?}",line2):
                    state="start"
                    result.append(self.NEWLINE)
                    continue
                else:
                    result.append("T||%s" % line)
                    result.append(self.NEWLINE)
                    continue
            elif state=="tokenized":
                if q.codetools.regex.match("{.?tokenized.?}",line2):
                    state="start"
                    continue
                else:
                    result.append(line)
                    continue
        if table:
            result.append("TABLE||%s" % json.dumps(table))
        return result


