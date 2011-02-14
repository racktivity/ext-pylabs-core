from pymonkey.InitBase import q
import uno
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
import time
import os
import string

FILTER_TYPES = {'pdf': 'writer_pdf_Export', 'doc': 'MS Word 97', 'odt': 'writer8'}

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
        self.desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.context)
        self.initialized = True

    def loadNewDocument(self):
        """
        Create a new document
        """
        self.document = self.desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())

    def loadExsitingDocument(self, doclocation):
        """
        Load an existing document from the filesystem
        """
        if not q.system.fs.exists(doclocation):
            raise RuntimeError('Document with location %s does not exist on the filesystem' % doclocation)
        url = unohelper.systemPathToFileUrl(doclocation)
        self.document = self.desktop.loadComponentFromURL(url, "_blank", 0, ())

    def getTextCursor(self):
        """
        Get a cursor to populate the document
        """
        self._checkDocument()
        self.cursor = self.document.Text.createTextCursor()
        return self.cursor

    def addText(self, text, newline=False, indent=False):
        self.checkCursor()
        if newline:
            self.document.Text.insertString(self.cursor, '\n\n' + text, 0)
        elif indent:
            self.document.Text.insertString(self.cursor, '\n\n\t' + text, 0)
        else:
            self.document.Text.insertString(self.cursor, text, 0)

    def addHeader(self, text, headerlevel=1):
        self._checkDocument()
        self.cursor.ParaStyleName = 'Heading %d' % headerlevel
        self.document.Text.insertString(self.cursor, text, False)

    def addBullets(self, text, bulletlevel=1):
        if self.cursor.NumberingStyleName != 'List %d' % bulletlevel:
            self.cursor.NumberingStyleName='List %d Start' % bulletlevel
            self.cursor.NumberingStyleName='List %d' % bulletlevel
        self.document.Text.insertString(self.cursor, text + chr(13), False)
        self.cursor.NumberingStyleName='List %d End' % bulletlevel

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
        self.cursor.setPropertyValue('CharStrike', SINGLE)
    
    def resetStrikeThrough(self):
        self.cursor.setPropertyValue('CharStrike', strikeNONE)

    def insertHyperlink(self, url, name=''):
        name = name or url
        self.cursor.setPropertyValue('HyperLinkURL', url)
        self.cursor.setPropertyValue('HyperLinkName', name)
        self.cursor.setPropertyValue('HyperLinkTarget', '_blank')

    def addNewLine(self):
        self._checkDocument()
        self.document.Text.insertControlCharacter(self.cursor, PARAGRAPH_BREAK, False)
    
    def insertImageObject(self, imagelocation):
        """
        Insert an image object into the document
        
        @param imagelocation: path to image on filesystem
        @type imagelocation: string
        """
        if not q.system.fs.exists(imagelocation):
            raise RuntimeError('Image with location %s does not exist on filesystem' % imagelocation)
        l = [PropertyValue() for i in range(4)]
        l[0].Name = 'FileName'
        l[0].Value = unohelper.systemPathToFileUrl(imagelocation)
        l[1].Name = 'FilterName'
        l[1].Value = '<All formats>'
        l[2].Name = 'AsLink'
        l[2].Value = False
        l[3].Name = 'Style'
        l[3].Value = 'Graphics'
        dispatcher = context.ServiceManager.createInstanceWithContext('com.sun.star.frame.DispatchHelper', self.context)
        dispatcher.executeDispatch(self.document.getCurrentController(), ".uno:InsertGraphic", "", 0, tuple(l))

    def insertTable(self, rows, columns):
        self._checkDocument()
        table = self.document.createInstance("com.sun.star.text.TextTable")
        table.initialize(rows, columns)
        self.document.Text.inserTextContent(self.cursor, table, 0)

    def _checkCursor(self):
        if not self.cursor:
            raise RuntimeError('No cursor set')
    
    def _checkDocument(self):
        if not self.document:
            raise RuntimeError('Document is not loaded')

    def getFontName(self):
        self._checkCursor()
        return self.cursor.getPropertyValue('CharFontName')
    
    def getFontHeight(self):
        self._checkCursor()
        return self.cursor.getPropertyValue('CharHeight')
    
    def getFontWeight(self):
        self._checkCursor()
        return self.cursor.getPropertyValue('CharWeight')

    def changeFont(self, fontname, height=12.0, weight=100.0):
        self._checkCursor()
        self.cursor.setPropertyValue('CharFontName', fontname)
        if height:
            self.cursor.setPropertyValue('CharHeight', height)
        if weight:
            self.cursor.setPropertyValue('CharWeight', weight)

    def saveFileAs(self, filename):
        self._checkDocument()
        url = unohelper.systemPathToFileUrl(filename)
        self.document.storeAsURL(url, ())

    def saveChanges(self):
        self._checkDocument()
        self.document.store()

    def exportToPDF(self, filename):
        return self._export('pdf', filename)

    def exportToDoc(self, filename):
        return self._export('doc', filename)

    def exportToODT(self, filename):
        return self._export('odt', filename)

    def _export(self, extension, filename=None):
        #@todo: still need a filter for docx
        if extension not in FILTER_TYPES.keys():
            raise RuntimeError('Unsupported extension %s' % extension)
        if not filename:
            filename = q.system.fs.joinPaths(q.dirs.tmpDir, str(time.time()) + 'document.%s' % extension)

        outputprops = (PropertyValue( "FilterName" , 0, FILTER_TYPES[extension] , 0 ), PropertyValue( "Overwrite" , 0, True , 0 ),)
        url = unohelper.systemPathToFileUrl(pdf_filename )
        self.document.storeToURL(url, outputprops)
        if q.system.fs.isFile(pdf_filename) and os.path.getsize(pdf_filename) != 0:
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
            