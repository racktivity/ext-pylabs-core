from pymonkey.InitBase import *
from pymonkey.Shell import *
from pymonkey.qpackages.common.QPackageObject import QPackageObject

q.application.appname = "processor"
q.application.start()

class Dummy():
    pass



class QPackagesClient():
    """
    @qlocation q.qp.client
    """
    def _getPackageDir(self):
        packagedir=q.dirs.packageDir
        return packagedir
    
    def __init__(self):
        self.loadMetadata()
        
    def loadMetadata(self):
        self.domains=[]
        self.packages=[] #array of array [[domain,name,version]]
        self.domains=q.system.fs.listDirsInDir(self._getPackageDir(),dirNameOnly=True)
        for domainName in self.domains:
            domainpath=q.system.fs.joinPaths(self._getPackageDir(),domainName)
            packages=q.system.fs.listDirsInDir(domainpath,dirNameOnly=True)
            for packagename in packages:
                packagepath=q.system.fs.joinPaths(domainpath,packagename)
                versions=q.system.fs.listDirsInDir(packagepath,dirNameOnly=True)
                for version in versions:
                    self.packages.append([domainName,packagename,version])
                    
    def qpackageGetpath(self,domain,name,version):
        return q.system.fs.joinPaths(self._getPackageDir(),domain,name,version)
             
    def qpackageExist(self,domain,name,version):
        return q.system.fs.exists(self.qpackageGetpath(domain,name,version))
            
    def qpackagegGet(self,domain,name,version):        
        if self.qpackageExist(domain,name,version)==False:
            q.eventhandler.raiseCriticalError("Could not find package %s " % self.qpackageGetpath(domain,name,version))
        packagedir=self.qpackageGetpath(domain,name,version)
        descriptionFilePath=q.system.fs.joinPaths(self.qpackageGetpath(domain,name,version),"cfg","description.wiki")
        configFilePath=q.system.fs.joinPaths(self.qpackageGetpath(domain,name,version),"cfg","qpackage.cfg")
        qp=QPackageObject(domain,name,version)
        if not q.system.fs.exists(descriptionFilePath):
            q.system.fs.writeFile(descriptionFilePath,"h2. %s %s %s\n\n...\n" % (domain,name,version))
        else:
            qp.description=q.system.fs.fileGetContents(descriptionFilePath)
        if not q.system.fs.exists(configFilePath):
            q.eventhandler.raiseCriticalError("No Config File For QPackage %s " % self.qpackageGetpath(domain,name,version))
        else:
            ipshell()
            
                
q.qp=Dummy()            
q.qp.local= QPackagesLocal()   
q.qp.local.loadMetadata()
q.qp.local.get("qpackages.org","juggernautdb","1.0")
#ipshell()

        
    
        
        
        

q.application.stop()
