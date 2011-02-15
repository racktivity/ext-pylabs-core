#!/usr/bin/python
from pylabs.InitBase import q
from PyUnoWrapper import PyUnoWrapper
import os
from optparse import OptionParser

KEYWORDS = ('HEADER', 'NL', 'P', 'T', 'CODEBLOCK', 'BOLD', '*', '#', 'IMAGE',
            'STRIKE', 'ITALIC', 'UNDER', 'LINK', 'ERROR', 'TABLE')

class WikiTokenConverter(object):

    def __init(self):
        q.application.appname = 'WikiTokenConverter'
        q.application.start()

    def writeDocument(self, parsedfilepath, filepath):
        data = q.system.fs.fileGetContents(parsedfilepath)
        baseDir = os.path.dirname(parsedfilepath)
        for line in data.splitlines():
            words = line.split('|', 2)
            keyword = words[0]
            level = words[1]
            text = words[2]
            if keyword not in KEYWORDS:
                raise RuntimeError('Unsupported keyword %s' % keyword)
            if keyword == 'HEADER':
                pyuno.addHeader(text, int(level))
            elif keyword == 'NL':
                pyuno.addNewLine()
            elif keyword == 'BOLD':
                pyuno.setBold()
                pyuno.addText(text)
                pyuno.resetBold()
            elif keyword == 'STRIKE':
                pyuno.setStrikeThrough()
                pyuno.addText(text)
                pyuno.resetStrikeThrough()
            elif keyword == 'ITALIC':
                pyuno.setItalic()
                pyuno.addText(text)
                pyuno.resetItalic()
            elif keyword == 'UNDER':
                pyuno.setUnderline()
                pyuno.addText(text)
                pyuno.resetUnderline()
            elif keyword in ['P', 'T', 'CODEBLOCK']:
                pyuno.addText(text)
            elif keyword == '*':
                pyuno.addBullets(text, int(level))
            elif keyword == '#':
                pyuno.addNumberings(text, int(level))
            elif keyword == 'IMAGE':
                location = os.path.join(baseDir, text)
                border = 0
                width = 0
                height = 0
                if level:
                    attributes = level.split(',')
                    for attribute in attributes:
                        if 'border' in attribute.strip():
                            border = int(attribute.strip().split('=')[1])
                        elif 'width' in attribute.strip():
                            width = int(attribute.strip().split('=')[1])
                        elif 'height' in attribute.strip():
                            height = int(attribute.strip().split('=')[1])
                if width or height:
                    pyuno.insertImage(location, border, width, height)
                else:
                    pyuno.insertImage(location, border)
            elif keyword == 'LINK':
                pyuno.insertHyperlink(text, int(level))
            elif keyword == 'TABLE':
                pyuno.insertTable(text)

    def _getLocations(self, wikifileLocation):
        dirname = os.path.dirname(wikifileLocation)
        filename = os.path.basename(wikifileLocation)
        absfilename = filename.split('.')[0]
        filelocation = '%s/%s' % (dirname, absfilename)
        return dirname, absfilename, filelocation

    def generateDOC(self, wikifileLocation):
        dirname, absfilename, filelocation = self._getLocations(wikifileLocation)
        pyuno.exportToDOC('%s.doc' % filelocation)

    def generatePDF(self, wikifileLocation):
        dirname, absfilename, filelocation = self._getLocations(wikifileLocation)
        pyuno.exportToPDF('%s.pdf' % filelocation)

    def generateODT(self, wikifileLocation):
        dirname, absfilename, filelocation = self._getLocations(wikifileLocation)
        pyuno.saveFileAs('%s/%s.odt' % (dirname, absfilename))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--filepath', dest='parsedfilepath', help='Parsed tokenized file path')
    parser.add_option('-o', '--outputfilepath', dest='outputfilepath', help='Output file path to be generated e.g. /opt/qbase3/myfile.pdf')
    parser.add_option('-t', '--templatepath', dest='templatepath', help='Template file Path')
    (options, args) = parser.parse_args()

    pyuno = PyUnoWrapper()
    if options.templatepath:
        document = pyuno.loadExsitingDocument(options.templatepath)
    else:
        document = pyuno.loadNewDocument()
    cursor = pyuno.getTextCursor()

    tokenconverter = WikiTokenConverter()
    tokenconverter.writeDocument(options.parsedfilepath, options.outputfilepath)
    extensionsdict = {'odt': tokenconverter.generateODT, 'doc': tokenconverter.generateDOC, 'pdf': tokenconverter.generatePDF}
    extension = os.path.basename(options.outputfilepath).split('.')[1]
    extensionsdict[extension](options.outputfilepath)
    q.application.stop()

