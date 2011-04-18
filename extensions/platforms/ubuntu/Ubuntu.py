from pylabs import q
import apt

class Ubuntu:
    def __init__(self):
        self._aptupdated = False
        self._checked = False
        self._cache = apt.cache.Cache()
        
    def check(self):
        """
        check if ubuntu
        """
        if not self._checked:
            try:
                import lsb_release
                info = lsb_release.get_distro_information()['ID']
                if info != 'Ubuntu':
                    raise RuntimeError("Only ubuntu is supported, platform is not even linux.")
                self._checked = True
            except ImportError:
                self._checked = False
                raise RuntimeError("Only ubuntu is supported.")
        
    def checkInstall(self, packagename, cmdname):
        """
        @param packagename is name of ubuntu package to install e.g. curl
        @param cmdname is cmd to check e.g. curl
        """
        self.check()
        result,out=q.system.process.execute("which %s" % cmdname,False)
        if result != 0:
            self.install(packagename)
        else:
            return 
        result,out=q.system.process.execute("which %s" % cmdname,False)   
        if result != 0:
            raise RuntimeError("Could not install package %s and check for command %s." % (packagename, cmdname))

        
    def install(self, packagename):
        self.check()
        if isinstance(packagename, basestring):
            packagename = [ packagename ]
        for package in packagename:
            pkg = self._cache[package]
            if not pkg.is_installed:
                pkg.mark_install()
        self._cache.commit()

    def remove(self, packagename):
        self.check()
        pkg = self._cache[packagename]
        if pkg.is_installed:
            pkg.mark_delete()
        self._cache.commit()
        
    def updatePackageMetadata(self, force=True):
        self.check()
        self._cache.update()
            
    def upgradePackages(self, force=True):
        self.check()        
        self.updatePackageMetadata()
        self._cache.upgrade()
    
       
