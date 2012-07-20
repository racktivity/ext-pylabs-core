from pylabs import q

class Ubuntu:
    def __init__(self):
        self._aptupdated = False
        self._checked = False
        try:
            import apt
        except ImportError:
            #we dont wont qshell to break, self.check will take of this
            return
        apt.apt_pkg.init()
        apt.apt_pkg.Config.set("APT::Install-Recommends", "0")
        apt.apt_pkg.Config.set("APT::Install-Suggests", "0")
        self._cache = None

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
        if not self._cache:
            try:
                import apt
                self._cache = apt.Cache()
            except ImportError:
                pass

    def checkInstall(self, packagename, cmdname):
        """
        @param packagename is name of ubuntu package to install e.g. curl
        @param cmdname is cmd to check e.g. curl
        """
        self.check()
        result, _ = q.system.process.execute("which %s" % cmdname, False)
        if result != 0:
            self.install(packagename)
        else:
            return
        result, _ = q.system.process.execute("which %s" % cmdname, False)
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
        self._cache.clear()

    def installDebFile(self, path):
        self.check()
        import apt.debfile
        deb = apt.debfile.DebPackage(path)
        deb.install()

    def remove(self, packagename):
        self.check()
        pkg = self._cache[packagename]
        if pkg.is_installed:
            pkg.mark_delete()
        self._cache.commit()
        self._cache.clear()

    def startService(self, servicename):
        self._service(servicename, 'start')

    def stopService(self, servicename):
        self._service(servicename, 'stop')

    def disableStartAtBoot(self, servicename):
        q.system.process.execute("update-rc.d -f %s remove" % servicename)

    def _service(self, servicename, action):
        return q.system.process.execute("service %s %s" % (servicename, action))


    def updatePackageMetadata(self, force=True):
        self.check()
        self._cache.update()

    def upgradePackages(self, force=True):
        self.check()
        self.updatePackageMetadata()
        self._cache.upgrade()


