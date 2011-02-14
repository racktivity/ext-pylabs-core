from pymonkey import q
from pymonkey.Shell import *
from QPackageObject4 import QPackageObject4
from QPackageObject3 import QPackageObject3
from DependencyDef4 import DependencyDef4

class QPackagesMigratorV3V4():
    """
    methods to deal with qpackages, seen from client level
    
    @qlocation q.qp.client
    """
    def _getPackageDir(self):
        """
        get qpackage for v3 version
        """
        packagedir=q.dirs.packageDir
        return packagedir
    
    def __init__(self): 
        self.loadMetadata()
        

    def migrateToV4(self,copyFiles=True,overwrite=False):
        q.system.fs.createDir(q.dirs.packageDir+"4")      
        for packagItem in self.packageslist:            
            self.qpackageMigrateToV4(packagItem[0],packagItem[1],packagItem[2],copyFiles,overwrite)
            
    def qpackageMigrateToV4(self,domain,name,version,copyFiles=True,overwrite=False):

        package=self.get(domain,name,version)
        packagepathV3=self.qpackageGetpath(domain,name,version)
        
        def getDirDest(omain,name,version,typedir):
            path=q.system.fs.joinPaths(self._getPackageDir()+"4",typedir,domain,name,version)
            q.system.fs.createDir(path)
            return path
        q.console.echo("process package %s" % package)
        
        builds=q.system.fs.listDirsInDir(q.system.fs.joinPaths(packagepathV3),dirNameOnly=True)
        builds.sort()
        builds.pop()
        buildnr=builds[-1]
        # remove files if needed    
        if overwrite:
            typedir="metadata"
            path=q.system.fs.joinPaths(self._getPackageDir()+"4",typedir,domain,name,version)
            q.system.fs.removeDirTree(path)
            typedir="files"
            path=q.system.fs.joinPaths(self._getPackageDir()+"4",typedir,domain,name,version)
            q.system.fs.removeDirTree(path)            
        #rewrite metadata        
        newPackage=QPackageObject4(domain,name,version,new=True)
        newPackage.name=package.name
        if package.description<>"":
            newPackage.description=package.description
        if int(buildnr)>0:
            newPackage.buildnr=int(buildnr)
        else:
            raise RuntimeError("Cannot find buildnr for %s" % package)        
        newPackage.version=package.version
        newPackage.domain=package.domain
        newPackage.tags=package.tags
        newPackage.dependencies=package.dependencies
        #newPackage.dependencies=[]
        #for dependency3 in package.dependencies:
            #dep4=DependencyDef4()
            #ipshell()
            #dep4.dependencytype=q.enumerators.DependencyType4.getByName(str(dependency3.dependencytype))
            #dep4.domain=dependency3.domain
            #dep4.maxversion=dependency3.maxversion
            #dep4.minversion=dependency3.minversion
            #dep4.name=dependency3.name
            #dep4.supportedPlatforms=dependency3.supportedPlatforms
            #newPackage.dependencies.append(dep4)
        newPackage.supportedPlatforms=package.supportedPlatforms   
        newPackage.save()
        #copy tasklets        
        q.system.fs.copyDirTree(q.system.fs.joinPaths(packagepathV3,buildnr,"tasklets"),getDirDest(domain,name,version,"metadata"))
        #copy files
        if copyFiles:
            if q.system.fs.exists(q.system.fs.joinPaths(packagepathV3,buildnr,"files")):
                q.system.fs.copyDirTree(q.system.fs.joinPaths(packagepathV3,buildnr,"files"),getDirDest(domain,name,version,"files"))
        #populate platform dirs
        q.system.fs.createDir(q.system.fs.joinPaths(getDirDest(domain,name,version,"files"),"generic"))
        q.system.fs.createDir(q.system.fs.joinPaths(getDirDest(domain,name,version,"files"),"linux"))
        #compress package in bundle dir
        if copyFiles:
            newPackage.compress()
        
                
    def loadMetadata(self):
        if not q.system.fs.exists(self._getPackageDirV3()):
            raise RuntimeError("Cannot find V3 style qpackages dir %s" % self._getPackageDirV3())
        self.domains=[]
        self.packageslist=[] #array of array [[domain,name,version]]
        self.domains=q.system.fs.listDirsInDir(self._getPackageDirV3(),dirNameOnly=True)
        for domainName in self.domains:
            domainpath=q.system.fs.joinPaths(self._getPackageDirV3(),domainName)
            packages=q.system.fs.listDirsInDir(domainpath,dirNameOnly=True)
            for packagename in packages:
                packagepath=q.system.fs.joinPaths(domainpath,packagename)
                versions=q.system.fs.listDirsInDir(packagepath,dirNameOnly=True)
                for version in versions:
                    self.packageslist.append([domainName,packagename,version])

    def loadMetadata(self):
        self.domains=[]
        self.packageslist=[] #array of array [[domain,name,version]]
        self.domains=q.system.fs.listDirsInDir(self._getPackageDir(),dirNameOnly=True)
        for domainName in self.domains:
            domainpath=q.system.fs.joinPaths(self._getPackageDir(),domainName)
            packages=q.system.fs.listDirsInDir(domainpath,dirNameOnly=True)
            for packagename in packages:
                packagepath=q.system.fs.joinPaths(domainpath,packagename)
                versions=q.system.fs.listDirsInDir(packagepath,dirNameOnly=True)
                for version in versions:
                    self.packageslist.append([domainName,packagename,version])
                    
                    
    def qpackageGetpath(self,domain,name,version):
        return q.system.fs.joinPaths(self._getPackageDir(),domain,name,version)
             
    def exists(self,domain,name,version):
        return q.system.fs.exists(self.qpackageGetpath(domain,name,version))
            
    def get(self,domain,name,version):        
        if self.exists(domain,name,version)==False:
            q.eventhandler.raiseCriticalError("Could not find package %s " % self.qpackageGetpath(domain,name,version))
        qp=QPackageObject3(domain,name,version)
        configFilePath=q.system.fs.joinPaths(self.qpackageGetpath(domain,name,version),"cfg")
        if not q.system.fs.exists(configFilePath):
            q.eventhandler.raiseCriticalError("No Config File For QPackage %s " % self.qpackageGetpath(domain,name,version))
        #qpackage found and config file found
        return qp
            
