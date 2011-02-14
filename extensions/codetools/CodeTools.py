
from RegexTools import RegexTools
from TemplateEngineWrapper import TemplateEngineWrapper
from WordReplacer import WordReplacer
from TextFileEditor import TextFileEditor

class CodeTools:
    def __init__(self):
        self.regex=RegexTools()
        self.templateengine=TemplateEngineWrapper()
        
        #self.wordreplacer=WordReplacer()
    
    def getWordReplacerTool(self):
        return WordReplacer()
    
    def getTextFileEditor(self,filepath):
        """
        returns a class which helps you to edit a text file
        e.g. find blocks, replace lines, ...
        """
        return TextFileEditor(filepath)