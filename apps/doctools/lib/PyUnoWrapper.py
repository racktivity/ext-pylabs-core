import uno
import unohelper
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.beans import PropertyValue
from com.sun.star.awt.FontWeight import BOLD
from com.sun.star.awt.FontSlant import ITALIC
from com.sun.star.awt.FontSlant import NONE
from com.sun.star.awt.FontUnderline import WAVE
from com.sun.star.awt.FontUnderline import NONE as underlineNONE
from com.sun.star.style.ParagraphAdjust import CENTER, LEFT, RIGHT
from com.sun.star.awt.FontStrikeout import SINGLE
from com.sun.star.awt.FontStrikeout import NONE as strikeNONE
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.style.NumberingType import ARABIC
import time
import os
import string
import Image
import json

FILTER_TYPES = {'pdf': 'writer_pdf_Export', 'doc': 'MS Word 97', 'odt': 'writer8'}
WHITE = 16777215
BLACK = 0
GREY = 7833753

class PyUnoWrapper(object):

    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialize()
        self.document = None
        self.cursor = None

    def initialize(self):
        #import the OpenOffice component context.
        local = uno.getComponentContext()
        #Access the UnoUrlResolver service. This will allow you to connect to OpenOffice.org program. 
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        #load the context and you are now connected. You can access OpenOffice via its API mechanism. 
        self.context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        #load/create the service responsible for the current document called desktop
        self.desktop = self.context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.context)
        self.initialized = True

    def loadNewDocument(self):
        """
        Create a new document
        """
        self.document = self.desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
        return self.document

    def loadExsitingDocument(self, doclocation):
        """
        Load an existing document from the filesystem
        """
        if not os.path.exists(doclocation):
            raise RuntimeError('Document with location %s does not exist on the filesystem' % doclocation)
        url = unohelper.systemPathToFileUrl(doclocation)
        self.document = self.desktop.loadComponentFromURL(url, "_blank", 0, ())
        return self.document

    def getTextCursor(self):
        """
        Get a cursor to populate the document
        """
        self.cursor = self.document.Text.createTextCursor()
        return self.cursor

    def addText(self, text, newline=False, indent=False):
        if newline:
            self.document.Text.insertString(self.cursor, '\n\n' + text, 0)
        elif indent:
            self.document.Text.insertString(self.cursor, '\n\n\t' + text, 0)
        else:
            self.document.Text.insertString(self.cursor, text, 0)

    def addHeader(self, text, headerlevel=1):
        self.cursor.ParaStyleName = 'Heading %d' % headerlevel
        self.document.Text.insertString(self.cursor, text, False)

    def addBullets(self, text, bulletlevel=1):
        self.cursor.NumberingStyleName='List %d Start' % bulletlevel
        self.cursor.setPropertyValue('NumberingLevel', ARABIC)
        self.cursor.NumberingStyleName='List 1'
        self.cursor.NumberingLevel = int(bulletlevel)
        self.document.Text.insertString(self.cursor, text + chr(13), False)
        self.cursor.NumberingStyleName='List %d End' % bulletlevel

    def addNumberings(self, text, numberinglevel=1):
        if self.cursor.NumberingStyleName != 'Numbering %d' % numberinglevel:
            self.cursor.NumberingStyleName='Numbering %d Start' % numberinglevel
            self.cursor.NumberingStyleName='Numbering %d' % numberinglevel
            self.cursor.NumberingLevel = numberinglevel
        self.document.Text.insertString(self.cursor, text + chr(13), False)
        self.cursor.NumberingStyleName='Numbering %d End' % numberinglevel

    def setBold(self):
        self.cursor.setPropertyValue('CharWeight', float(BOLD))

    def resetBold(self):
        self.cursor.setPropertyValue('CharWeight', 100.0)

    def setItalic(self):
        self.cursor.setPropertyValue('CharPosture', ITALIC)

    def resetItalic(self):
        self.cursor.setPropertyValue('CharPosture', NONE)

    def setUnderline(self):
        self.cursor.setPropertyValue('CharUnderline', WAVE)

    def resetUnderline(self):
        self.cursor.setPropertyValue('CharUnderline', underlineNONE)

    def setTextPosition(self, position):
        if position not in ('center', 'left', 'right'):
            raise AttributeError('Undefined position, should be either center, left or right')
        positiondict = {'center': CENTER, 'left': LEFT, 'right': RIGHT}
        self.cursor.setPropertyValue('ParaAdjust', positiondict[position])

    def setStrikeThrough(self):
        self.cursor.setPropertyValue('CharStrikeout', SINGLE)
    
    def resetStrikeThrough(self):
        self.cursor.setPropertyValue('CharStrikeout', strikeNONE)

    def insertHyperlink(self, url, name=''):
        name = name or url
        self.cursor.setPropertyValue('HyperLinkURL', url)
        self.cursor.setPropertyValue('HyperLinkName', name)
        self.cursor.setPropertyValue('HyperLinkTarget', '_blank')

    def addNewLine(self):
        self.document.Text.insertControlCharacter(self.cursor, PARAGRAPH_BREAK, False)
    
    def insertImage(self, imagelocation, border=0, width=0, height=0):
        """
        Insert an image object into the document
        
        @param imagelocation: path to image on filesystem
        @type imagelocation: string
        """
        if not os.path.exists(imagelocation):
            raise RuntimeError('Image with location %s does not exist on filesystem' % imagelocation)
        image = Image.open(imagelocation)
        origWidth = image.size[0]
        origHeight = image.size[1]
        if width and not height:
            height = float(origHeight*width)/origWidth
        elif height and not width:
            width = float(height*origWidth)/origHeight
        graph = self.document.createInstance('com.sun.star.text.GraphicObject')
        if border:
            bordersize = int(border) * 26.45833
            graph.LeftBorderDistance = bordersize
            graph.RightBorderDistance = bordersize
            graph.BottomBorderDistance = bordersize
            graph.TopBorderDistance = bordersize
            graph.BorderDistance = bordersize
        if width and height:
            graph.Width = int(width) * 26.45833
            graph.Height = int(height) * 26.45833
        graph.GraphicURL = unohelper.systemPathToFileUrl(imagelocation)
        graph.AnchorType = AS_CHARACTER
        self.document.Text.insertTextContent(self.cursor, graph, False)

    def insertTable(self, stringdata):
        def insertTextIntoCell(table, cellName, text, color):
            tableText = table.getCellByName(cellName)
            cursor = tableText.createTextCursor()
            cursor.setPropertyValue("CharColor", color)
            tableText.setString(text)

        table = self.document.createInstance("com.sun.star.text.TextTable")
        data = json.loads(stringdata)
        rows = len(data.keys())
        columns = len(data.values()[0])
        table.initialize(rows, columns)
        self.document.Text.insertTextContent(self.cursor, table, 0)
        rows = table.Rows
        table.setPropertyValue( "BackTransparent", uno.Bool(0) )
        table.setPropertyValue("BackColor", WHITE)
        row = rows.getByIndex(0)
        row.setPropertyValue("BackTransparent", uno.Bool(0))
        row.setPropertyValue("BackColor", GREY)
        for roworder, rowdata in data.iteritems():
            for index, rowtext in enumerate(rowdata):
                tableposition = "%s%d" % (chr(65+index), int(roworder))
                if tableposition.endswith('1'):
                    insertTextIntoCell(table, tableposition, rowtext, WHITE)
                else:
                    insertTextIntoCell(table, tableposition, rowtext, BLACK)

    def getFontName(self):
        return self.cursor.getPropertyValue('CharFontName')
    
    def getFontHeight(self):
        return self.cursor.getPropertyValue('CharHeight')
    
    def getFontWeight(self):
        return self.cursor.getPropertyValue('CharWeight')

    def changeFont(self, fontname, height=12.0, weight=100.0):
        self.cursor.setPropertyValue('CharFontName', fontname)
        if height:
            self.cursor.setPropertyValue('CharHeight', height)
        if weight:
            self.cursor.setPropertyValue('CharWeight', weight)

    def saveFileAs(self, filename):
        url = unohelper.systemPathToFileUrl(filename)
        self.document.storeAsURL(url, ())

    def saveChanges(self):
        self.document.store()

    def exportToPDF(self, filename):
        return self._export('pdf', filename)

    def exportToDOC(self, filename):
        return self._export('doc', filename)

    def exportToODT(self, filename):
        return self._export('odt', filename)

    def _export(self, extension, filename=None):
        if extension not in FILTER_TYPES.keys():
            raise RuntimeError('Unsupported extension %s' % extension)
        if not filename:
            filename = os.path.join('/tmp', str(time.time()) + 'document.%s' % extension)

        outputprops = (PropertyValue( "FilterName" , 0, FILTER_TYPES[extension] , 0 ), PropertyValue( "Overwrite" , 0, True , 0 ),)
        url = unohelper.systemPathToFileUrl(filename )
        self.document.storeToURL(url, outputprops)
        if os.path.isfile(filename) and os.path.getsize(filename) != 0:
            return True
        return False

    def findAndReplace(self, find=None, replace=None):
        search = self.document.createSearchDescriptor()
        search.SearchString = unicode(find)
        found = self.document.findFirst(search)
        while found:
            found.String = string.replace(found.String, unicode(find), unicode(replace))
            found = self.document.findNext(found.End, search)
    
    def close(self):
        self.document.dispose()
            