from WikiParser import Parser
from pylabs.Shell import *
from pylabs import q, i

class DocTools:

    def wiki2IntermediateFormat(self, startWikiFilePath='/opt/qbase3/apps/doctools/wiki/example.wiki',\
        wikidir='/opt/qbase3/apps/doctools/wiki',\
        macrotaskletspath='/opt/qbase3/apps/doctools/tasklets',\
        resultsdir='/opt/qbase3/apps/doctools/out'):
        """
        generates document which has tokenized output of wiki doc
        @param startWikiFilePath is start file for which a doc will be generated, is in confluence format
        @param wikidir is dir in which all wiki documents reside
        @param macrotaskletspath is dir in which all tasklets reside which implement the macro's
        @param resultsdir is directory in which resulting documents will be stored
        """
        q.system.fs.createDir(resultsdir)
        q.system.fs.createDir(macrotaskletspath)
        wikiparser = Parser(startWikiFilePath, wikidir, macrotaskletspath, resultsdir)
        wikiparser.do()
        return wikiparser.wikifilePathTokenized

    def intermediateFormatToPDF(self, intermediateFilePath, resultsdir='/opt/qbase3/apps/doctools/out', templatePath=None):
        """
        Generates PDF document from a tokenized parsed file from wiki syntax
        
        @param intermediateFilePath: Path to tokenized output of a wiki doc
        @param resultsdir: directory in which resulting documents will be stored
        """
        #pass this file to lib/wiki_tokenconverttool , this tool uses platform python
        outputfilepath = self._getOutputFilePath(intermediateFilePath, resultsdir)
        self._convert(intermediateFilePath, '%s.pdf' % outputfilepath, templatePath)

    def intermediateFormatToDOC(self, intermediateFilePath, resultsdir='/opt/qbase3/apps/doctools/out', templatePath=None):
        """
        Generates DOC document from a tokenized parsed file from wiki syntax
        
        @param intermediateFilePath: Path to tokenized output of a wiki doc
        @param resultsdir: directory in which resulting documents will be stored
        """
        outputfilepath = self._getOutputFilePath(intermediateFilePath, resultsdir)
        self._convert(intermediateFilePath, '%s.doc' % outputfilepath, templatePath)

    def intermediateFormatToODT(self, intermediateFilePath, resultsdir='/opt/qbase3/apps/doctools/out', templatePath=None):
        """
        Generates ODT document from a tokenized parsed file from wiki syntax
        
        @param intermediateFilePath: Path to tokenized output of a wiki doc
        @param resultsdir: directory in which resulting documents will be stored
        """
        outputfilepath = self._getOutputFilePath(intermediateFilePath, resultsdir)
        self._convert(intermediateFilePath, '%s.odt' % outputfilepath, templatePath)

    def generateDoc(self, outpuPath, startWikiFilePath, templatePath=None):
        """
        Generate DOC document from wiki syntax
        
        @param outputPath: Path of desired generated file e.g. /opt/qbase3/apps/doctools/out
        @param startWikiFilePath: start file for which a doc will be generated, is in confluence format
        """
        self._checkOutDir(outputPath)
        intermediatefilepath = self.wiki2IntermediateFormat(startWikiFilePath, wikidir=q.system.fs.getDirName(startWikiFilePath), resultsdir=outputPath)
        self.intermediateFormatToDOC(intermediatefilepath, outpuPath, templatePath)

    def generatePDF(self, outputPath, startWikiFilePath, templatePath=None):
        """
        Generate PDF document from wiki syntax
        
        @param outputPath: Path of desired generated file e.g. /opt/qbase3/apps/doctools/out/
        @param startWikiFilePath: start file for which a doc will be generated, is in confluence format
        """
        self._checkOutDir(outputPath)
        intermediatefilepath = self.wiki2IntermediateFormat(startWikiFilePath, wikidir=q.system.fs.getDirName(startWikiFilePath), resultsdir=outputPath)
        self.intermediateFormatToPDF(intermediatefilepath, outputPath, templatePath)
    
    def generateODT(self, outputPath, startWikiFilePath, templatePath=None):
        """
        Generate ODT document from wiki syntax
        
        @param outputPath: Path of desired generated file e.g. /opt/qbase3/apps/doctools/out/
        @param startWikiFilePath: start file for which a doc will be generated, is in confluence format
        """
        self._checkOutDir(outputPath)
        intermediatefilepath = self.wiki2IntermediateFormat(startWikiFilePath, wikidir=q.system.fs.getDirName(startWikiFilePath), resultsdir=outputPath)
        self.intermediateFormatToODT(intermediatefilepath, outputPath, templatePath)

    def _checkOutDir(self, resultsdir):
        if not q.system.fs.exists(resultsdir):
            q.system.fs.createDir(resultsdir)

    def _convert(self, intermediateFilePath, outputfile, templatePath):
        converter = q.system.fs.joinPaths(q.dirs.appDir, 'doctools', 'lib', 'WikiTokenConverter.py')
        if templatePath:
            converter += " -f '%s' -o '%s' -t '%s'" % (intermediateFilePath, outputfile, templatePath)
        else:
            converter += " -f '%s' -o '%s'" % (intermediateFilePath, outputfile)
        q.system.process.execute(converter)

    def _getOutputFilePath(self, intermediateFilePath, resultsdir):
        return q.system.fs.joinPaths(resultsdir, q.system.fs.getBaseName(intermediateFilePath).split('.')[0])
