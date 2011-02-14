from pymonkey import *
from pymonkey.Shell import *

class Ubuntu():
    def __init__(self):
        self._aptupdated=False
        self._checked=False
        
    def check(self):
        """
        check if ubuntu
        """
        if self._checked==False:
            if not (q.platform.name=="linux32" or q.platform.name=="linux64"):
                raise RuntimeError("Only ubuntu is supported, platform is not even linux.")
            if q.system.process.execute("uname -a")[1].lower().find("ubuntu")<>-1:
                self._checked=True
            else:
                raise RuntimeError("Only ubuntu is supported")
        
    def checkInstall(self, packagename, cmdname):
        """
        @param packagename is name of ubuntu package to install e.g. curl
        @param cmdname is cmd to check e.g. curl
        """
        if not q.platform.isLinux():
            raise RuntimeError("only linux supported for this method (checkinstall)")
        result,out=q.system.process.execute("which %s" % cmdname,False)   
        if result<>0:
            self.install(packagename)
        else:
            return 
        result,out=q.system.process.execute("which %s" % cmdname,False)   
        if result<>0:
            raise RuntimeError("Could not install package %s and check for command %s." % (packagename, cmdname))

        
    def install(self,packagename):
        self.check()
        self.updatePackageMetadata(force=False)
        q.logger.log("apt-get install %s" % packagename)
        q.system.process.executeWithoutPipe("apt-get install %s -y" % packagename) #@todo wrap better to raise proper error

    def remove(self,packagename):
        self.check()
        q.system.process.executeWithoutPipe("apt-get remove %s -y" % packagename,dieOnNonZeroExitCode=False) #@todo wrap better to raise proper error
        
        
    def updatePackageMetadata(self,force=True):
        self.check()
        if self._aptupdated==False:
            q.system.process.execute("apt-get update",dieOnNonZeroExitCode=False)
            self._aptupdated=True
            
    def upgradePackages(self,force=True,die=False):
        self.check()        
        self.updatePackageMetadata()
        q.system.process.execute("apt-get upgrade",dieOnNonZeroExitCode=die)
    
    def installFileMonitor(self):
        self.check()
        self.install("gamin")
        self.install("python-gamin")
        q.system.fs.symlink("/usr/lib/libgamin-1.so.0","/opt/qbase3/lib/libgamin-1.so.0",True)
        
    def linkPylabsToSystem(self):
        self.install("python2.6")
        self.remove("mercurial")
        self.remove("mercurial-common")
        q.system.fs.copyFile(q.system.fs.joinPaths(q.dirs.baseDir,"utils","defaults","system","sitecustomize.py"),"/usr/lib/python2.6/sitecustomize.py")
        q.system.fs.symlink("/opt/qbase3/bin/hg","/usr/bin/hg",True)
        q.system.fs.symlink("/opt/qbase3/qshell","/usr/bin/qshell",True)
        
        
