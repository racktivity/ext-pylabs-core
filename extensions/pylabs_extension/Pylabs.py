

import pylabs
from pylabs import q
from pylabs.Shell import *

class Pylabs():
    def __init__(self):        
        self.objectInspector=PylabsObjectInspector()
    
    def editorInstallEric4(self):
        """
        Resets all values to empty values
        """
        q.qp.findNewest("eric*") .install()
        
    def enabledPlatformPythonForPylabs(self):
        sitepackageDir=q.qpackagetools.getSitePackageDir()
    
    
    #api codes
##4 function with params
##7 ???
##8 property

import inspect
class PylabsObjectInspector():
    """
    functionality to inspect objectr structure and generate apifile
    """
    
    def __init__(self):
        self.apiFileLocation=q.system.fs.joinPaths(q.dirs.cfgDir, "codecompletionapi","pylabs.api")
        q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.cfgDir, "codecompletionapi"))

    def _processMethod(self, method):
        source=inspect.getsource(method)
        inspected=inspect.getargspec(method)
        params=""
        for param in inspected.args:
            if param.lower().strip()<>"self":
                params=params+param+","
        params=params[:-1]
        return source, params

    def inspect(self, objectLocationPath="q"):
        """
        walk over objects in memory and create code completion api in pylabs cfgdir under codecompletionapi
        @param object is start object
        @param objectLocationPath is full location name in object tree e.g. q.system.fs , no need to fill in
        """
        if not q.basetype.string.check(objectLocationPath):
            raise RuntimeError("objectLocationPath needs to be string")
        print objectLocationPath
        object=eval(objectLocationPath)    
        for dictitem in dir(object):
            objectLocationPath2="%s.%s" % (objectLocationPath, dictitem)            
            if dictitem[0]<>"_" and dictitem[0:3]<>"pm_": 
                print objectLocationPath2
                objectNew=None
                try:
                    objectNew=eval("%s"%objectLocationPath2)                
                except:
                    print "COULD NOT EVAL %s" % objectLocationPath2                
                if objectNew==None:
                    pass
                elif dictitem.upper()==dictitem:
                    #is special type or constant
                    objectLocationPath2="%s.%s" % (objectLocationPath, dictitem)
                    ##print "special type: %s" % objectLocationPath2 
                    q.system.fs.writeFile(self.apiFileLocation, "%s?7\n"%objectLocationPath2, True)                          
                elif str(type(objectNew)).find("'instance'")<>-1 or str(type(objectNew)).find("<class")<>-1 or str(type(objectNew)).find("'classobj'")<>-1 :
                    q.system.fs.writeFile(self.apiFileLocation, "%s?8\n"%objectLocationPath2, True)
                    ##print "class or instance: %s" % objectLocationPath2          
                    self.inspect( objectLocationPath2)
                elif str(type(objectNew)).find("'instancemethod'")<>-1 or str(type(objectNew)).find("'function'")<>-1\
                or str(type(objectNew)).find("'staticmethod'")<>-1 or str(type(objectNew)).find("'classmethod'")<>-1:
                    #is instancemethod
                    source, params=self._processMethod(objectNew)
                    objectLocationPath2="%s.%s" % (objectLocationPath, dictitem)
                    ##print "instancemethod: %s" % objectLocationPath2          
                    q.system.fs.writeFile(self.apiFileLocation, "%s?4(%s)\n"%(objectLocationPath2, params), True)       
                elif str(type(objectNew)).find("'str'")<>-1 or str(type(objectNew)).find("'type'")<>-1 or str(type(objectNew)).find("'list'")<>-1\
                or str(type(objectNew)).find("'bool'")<>-1 or str(type(objectNew)).find("'int'")<>-1 or str(type(objectNew)).find("'NoneType'")<>-1\
                or str(type(objectNew)).find("'dict'")<>-1 or  str(type(objectNew)).find("'property'")<>-1 or str(type(objectNew)).find("'tuple'")<>-1:
                    #is instancemethod
                    objectLocationPath2="%s.%s" % (objectLocationPath, dictitem)
                    ##print "property: %s" % objectLocationPath2 
                    q.system.fs.writeFile(self.apiFileLocation, "%s?8\n"%objectLocationPath2, True)      
                else:
                    print str(type(objectNew))+ " "+objectLocationPath2

