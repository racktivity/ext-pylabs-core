from pylabs import q

class QPackageIObject4:
    
    def __init__(self, qpackage):
        self.qpackage = qpackage

    def prepareForUpdatingFiles(self):
        """
        This Package will be prepared to allow you to update files in the qpackage files directory
        you can do this manually (edit files in $qbasedir/var/qpackages4/files/...
        or you can use the $qpackageobject.quickPackage() action which will do it for you
        """
        self.qpackage.prepareForUpdatingFiles()

    def quickPackage(self):
        ##self.assertAccessable()

        """
        The following process will be followed
        - checkout code -> sandbox
        - build code (if needed)
        - package code -> qpackage files directory
        when ready to quickPackage your qpackages you will still have to do a i.qp.publishAll()
        """
        self.qpackage.prepareForUpdatingFiles(False)
        self.qpackage.checkout()
        self.qpackage.compile()
        self.qpackage.package()
        #i.qp.publishDomain(self.package.domain)

    def getBrokenDependencies(self):
        """
        Show which qpackages are broken for a specific platform.
        """
        ##self.assertAccessable()
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        return self.qpackage.getBrokenDependencies(platform)
        
    def getDependencyTree(self):
        """
        Show the dependency tree (per platform).
        """
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        self.qpackage.getDependencyTree(platform)
        
    def _printList(self,arr):
        for item in arr:
            q.console.echo(item)
        
    def showBuildDependencyTree(self):
        """
        Shows the dependency tree for building a qpackage.
        """
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        self.qpackage.getBuildDependencyTree(platform)
        
    def getRuntimeDependencyTree(self):
        """
        Shows the dependency tree for the runtime environment.
        """
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        self.qpackage.getRuntimeDependencyTree(platform)
                
    
    def showDependencies(self):
        """
        Returns all depensencies for this package.
        See also: addDependency and removeDependency
        """
        ##self.assertAccessable()
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        recursive = q.console.askYesNo("Recursive?")
        self._printList(self.qpackage.getDependencies(platform, recursive))
        
    def showBuildDependencies(self):
        """
        Returns the build dependencies for this package.
        See also: addDependency and removeDependency
        """
        ##self.assertAccessable()
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        recursive = q.console.askYesNo("Recursive?")
        self._printList(self.qpackage.getBuildDependencies(platform, recursive))
        
    def showRuntimeDependencies(self):
        """
        Returns the runtime dependencies for this package.
        See also: addDependency and removeDependency
        """
        ##self.assertAccessable()
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        recursive = q.console.askYesNo("Recursive?")
        self._printList(self.qpackage.getRuntimeDependencies(platform, recursive))
    
    def addDependency(self):
        """
        Add a dependency to a package.
        """
        domain             = q.console.askChoice(q.qp.getDomainNames(), "Please select a domain")
        name               = q.console.askString("Please provide a name for the dependency")
        supportedPlatforms = q.console.askChoiceMultiple(q.enumerators.PlatformType.ALL, "Please provide a comma separated list of supported platforms")
        minversion         = q.console.askString("Please provide a minimum version, eg: 1.2")
        maxversion         = q.console.askString("Please provide a maximum version, eg: 2.5")
        dependencytype     = q.console.askChoice([q.enumerators.DependencyType4.BUILD,q.enumerators.DependencyType4.RUNTIME], "Please select a dependencytype")
        
        self.qpackage.addDependency(domain, name, supportedPlatforms, minversion, maxversion, dependencytype)
        self.qpackage.save()

    def removeDependency(self):
        """
        Remove a dependency from a qpackage.
        """
        ##self.assertAccessable()
        dependency = q.console.askChoice(self.qpackage.dependencies, "Please select the dependency to remove")
        self.qpackage.removeDependency(dependency)
        self.qpackage.save()
        
    def addSupportedPlatform(self):
        """
        Adds a supported platform
        """
        ##self.assertAccessable()
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        self.qpackage.addSupportedPlatform(platform)
        self.qpackage.save()

    def removeSupportedPlatform(self):
        """
        Removes a supported platform
        """
        ##self.assertAccessable()
        platform = q.console.askChoice(self.qpackage.supportedPlatforms, "Please select the platform to remove")
        self.qpackage.removeSupportedPlatform(platform) 
        self.qpackage.save()
        
    def addTag(self):
        """
        Adds a tag to this package
        """
        ##self.assertAccessable()
        tag = q.console.askString("Please enter a tag string:")
        self.qpackage.addTag(tag)
        self.qpackage.save()

    def removeTag(self):
        """
        Removes a tag from this package
        """
        ##self.assertAccessable()
        tag = q.console.askChoice(self.qpackage.tags, "Please select the tag to remove")
        self.qpackage.removeTag(tag)
        self.qpackage.save()

    def showDependingInstalledPackages(self):
        """
        Show which qpackages have this qpackage as dependency.
        Do this only for the installed qpackages.
        """
        ##self.assertAccessable()
        recursive = q.console.askYesNo("Recursive?")
        self._printList(self.qpackage.getDependingInstalledPackages(recursive))

    def showDependingPackages(self):
        """
        Show which qpackages have this qpackage as dependency.
        """
        ##self.assertAccessable()
        platform = q.console.askChoice(q.enumerators.PlatformType.ALL, "Please select a platform")
        recursive = q.console.askYesNo("Recursive?")
        self._printList(self.qpackage.getDependingPackages(recursive, platform))

    def backup(self):
        """
        Makes a backup for this package by running its backup tasklet.
        This is the invers operation from restore.
        """
        ##self.assertAccessable()
        url = q.console.askString("Url to backup to?")
        self.qpackage.backup(url)
        
    def restore(self):
        """
        Restores a qpackage from specified url by running its backup tasklet.
        This is the invers operation form backup.
        """
        url = q.console.askString("Url to restore from?")
        self.qpackage.restore(url)

    def configure(self):
        """
        Configure this qpackage by running its checkout tasklet.
        """
        ##self.assertAccessable()
        #dependencies = q.console.askYesNo("Do you want the dependencies to be configured too?")
        self.qpackage.configure()

    def checkout(self):
        """
        Checks out this package by running its checkout tasklet.
        """
        ##self.assertAccessable()
        self.qpackage.checkout()

    def compile(self):
        """
        Compiles this package by running its compile tasklet.
        """
        ##self.assertAccessable()
        self.qpackage.compile()

    def package(self):
        """
        Packages this package by running its package tasklet.
        """
        ##self.assertAccessable()
        self.qpackage.package()

    def install(self):
        """
        Install this package by running its install tasklet.
        """
        self.qpackage.install()
        ##self.assertAccessable()
  

    def reinstall(self):
        """
        Install this package by running its install tasklet.
        """
        self.qpackage.install(reinstall=True)
        ##self.assertAccessable()
          
        
    def download(self):
        """
        Downloads the bundle of this package from the bundle server through ftp as specified in the bundledownload property of the domain of this package.
        This is the invers operation from upload.
        """
        ##self.assertAccessable()
        dependencies   = q.console.askYesNo("Do you want the bundles of all depending packages to be downloaded too?")
        self.qpackage.download(dependencies)

    def upload(self):
        """
        Uploads the bundle of this package to the bundle server though ftp as specified in the bundleupload property of the domain of this package.
        This is the inverted operation from download.
        """
        ##self.assertAccessable()
        #dependencies = q.console.askYesNo("Do you want the bundles of all depending packages to be uploaded too?")
        self.qpackage._upload()

    def expand(self):
        """
        Expands this package bundle from the bundles directory to the correct location under the files directory.
        This is the invers operation form compress.
        """
        ##self.assertAccessable()
        dependencies = q.console.askYesNo("Do you want the bundles of all depending packages to be expanded too?")
        self.qpackage._expand(dependencies)

    def compress(self):   #Todo is compress interactively necessary
        """
        Compresses the files of this package to a bundle and puts that bundle in the bundles directory
        This is the invers operation form expand.
        """
        self.qpackage._compress()
    
    def reload(self):
        """
        Reloads this packages meta information from disk.
        In other words: rereads the package.cfg file from disk.
        """
        ##self.assertAccessable()
        self.qpackage.reload()

    def delete(self):
        self.qpackage.delete()

    def getDescription(self):
        """
        Returns the description of this package.
        """
        ##self.assertAccessable()
        return self.qpackage.description

    def setDescription(self):
        """
        Sets the desciptions of this package and updates it on disk
        """
        ##self.assertAccessable()
        description = q.console.askString("Please enter a description:")
        self.qpackage.description=description
        self.qpackage.save()

    def __str__(self):
        #if not self.qpackage.assertAccessable():
        return "IPackage %s %s %s" % (self.qpackage.domain,self.qpackage.name,self.qpackage.version)
        #else:
        #    return "Deleted IPackage %s %s %s" % (self.qpackage.domain,self.qpackage.name,self.qpackage.version)

    def __repr__(self):
        return self.__str__()