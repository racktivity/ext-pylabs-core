#!/usr/bin/python
from pylabs import q
import json

KEYWORDS = ('HEADER', 'NL', 'P', 'T', 'CODEBLOCK', 'BOLD', '*', '#', 'IMAGE',
            'STRIKE', 'ITALIC', 'UNDER', 'LINK', 'ERROR', 'TABLE', "PB")

class MarkDown(object):

    def __init__(self, tokenfile):
        self.tokenfile = tokenfile

    def convert(self, outputpath):
        result = ""
        basedir = q.system.fs.getDirName(self.tokenfile)
        data = q.system.fs.fileGetContents(self.tokenfile)
        for line in data.splitlines():
            words = line.split('|',2)
            keyword = words[0]
            meta = words[1]
            text = words[2]
            if keyword not in KEYWORDS:
                raise RuntimeError('Unsupported keyword %s' % keyword)
            if keyword == 'HEADER':
                result += "%s%s%s" % ("#" * int(meta), text, "\n")
            elif keyword == 'NL':
                result += "\n"
            elif keyword == 'BOLD':
                result += "**%s**" % text
            elif keyword == 'STRIKE':
                result += "<strike>%s</strike>" % text
            elif keyword == 'ITALIC':
                result += "*%s*" % text
            elif keyword == 'UNDER':
                result += "<u>%s</u>" % text
            elif keyword in ["T", "P"]:
                result += text
            elif keyword in 'CODEBLOCK':
                result += "`%s`" % text
            elif keyword == '*':
                result += "%s %s" % ("*" * int(meta), text)
            elif keyword == '#':
                result += "1. %s" % (text)
            elif keyword == 'IMAGE':
                result += "![Image](%s)" % (text)
            elif keyword == 'LINK':
                result += "[%s](%s)" % (meta,text)
            elif keyword == 'TABLE':
                pass
        q.system.fs.writeFile(outputpath, result)
