from pymonkey import q
from QPackageIObject4 import QPackageIObject4

# Return QPackageIObject instead of the real package object
# So interative methods can be added/overwritten
class QPackageIClient4():
    
    """
    methods to deal with qpackages, seen from client level, interactive
    @qlocation i.qp
    """

    def getPackagesWithBrokenDependencies(self):
        return [p for p in q.qp.find('*') if len(p.getBrokenDependencies()) > 0]
                    
    def getPackage(self,domain,name,version):
        """
        Get an interactive QPackage Object,
        the underlying QPackage object can be obtained from myInteractivePackageObject.qpackage
        """
        return QPackageIObject4(q.qp.get(domain,name,version))
    
    # builds the required directory structure
    # When repo is not None a default codemanagement tasklet is generated
    # When isExtension is true the files are put under lib/pymonkey/extensions
    # When create link is true a link is made in lib/pymonkey/extensions to the files.. for easy testing  
    def createNewPackage(self):
        """ 
        Builds the required directory structure and generates the default files; 
        install.py, configure.py, package.py, codemanagement.py, backup.py, startstop.py
        After editing these files to their correct content the new package can be published using aPackage.quickPublish()
        """
        domain  = q.console.askChoice(q.qp.getDomainNames(), "Please select a domain")
        q.qp.getDomainObject(domain)._ensureDomainCanBeUpdated()

        name    = q.console.askString("Please provide a name")
        version = q.console.askString("Please provide a version","1.0")
        descr   = q.console.askString("Please provide a description","")
        supportedPlatforms = None
        while not supportedPlatforms:
            supportedPlatforms = q.console.askChoiceMultiple(q.enumerators.PlatformType.ALL, 'Please enumerate the supported platforms')
        qp      = q.qp.createNewQPackage(domain, name, version, descr, supportedPlatforms)
        res = QPackageIObject4(qp)
        self._attachLastPackages([res])
        return res
    
    def _find(self, domain="", name="", version="", platform=None):
        """ 
        Tries to find a package based on the provided criteria
        You may also use a wildcard to provide the name or domain (*partofname*)
        """
        if not name:
            name = q.console.askString("Please provide the name or part of the name of the package to search for (e.g *extension* -> lots of extensions)")
        res = [QPackageIObject4(p) for p in q.qp.find(domain=domain, name=name, version=version, platform=platform)]
        if not res:
            q.console.echo('No packages found, did you forget i.qp.updateMetadataAll()?')
        return res

    def findByName(self,name):
        ''' just a different name of find, delegates to find'''
        return self.find(domain="",name=name)

    
    def find(self, name="", domain="" , version="", platform=q.enumerators.PlatformType.GENERIC):
        """ 
        Tries to find a package based on the provided criteria
        You may also use a wildcard to provide the name or domain (*partofname*)
        """
        result = self._find(domain, name, version, platform)
        if not result:
            q.console.echo("package not found")
        if len(result) > 1:
            result = [q.console.askChoice(result, "Multiple packages found, please choose one")]
        if result:
            self._attachLastPackages(result)
            return result[-1]
        return None
    '''
    i.qp.getBundleSources(
    i.qp.getDomainRepositories(
    i.qp.getDomainRepository(
    i.qp.lastQPackages

    i.qp.showConfig()
    '''

    def _attachLastPackages(self, lastPackages):
        print "lastPackages: " + str(lastPackages)
        if not lastPackages:
            return
        self.lastPackage = lastPackages[-1]
        if not hasattr(self, 'lastPackages') or self.lastPackages == None:
            class Object:
                pass
            self.lastPackages = Object()
        for package in lastPackages:
            setattr(self.lastPackages, package.qpackage.name, package)

    def printConfig(self):
        '''
        prints out the current configuration.
        more concrete this prints out all bundles sources and the repository for each domain.
        '''
        for d in q.qp.getDomainNames():
            q.console.echo('Domain: ' + str(q.qp.getDomainObject(d)))
        q.console.echo('These configurations can be altered by manually editing the file:')
        q.console.echo('sources.cfg under /opt/qbase3/cfg/qpackages4/ ')
        
        '''
        # TODO finish this
        # How can we edit the config files
        # we make them normal config files of which we can
        def _editConfig(self):
                Shows for each domain:
                the repository
                the bundles sources

                ask to configure a domain
                when configuring a domain we may
                we may edit the repo or the bundle sources
                when we select bundle sources we may add new one or delete old one
                after we are done we go up one level again
                we may also configure passwords

            selectedDomain=None # The selected domain
            selectedAspect=None # BundleSources/MetaRepository
            while True:
                self.printConfig()
                if selectedDomain:
                    if not selectedAspect:
                        selectedAspect = q.gui.dialog.askChoice("Please select the operation:", ['Edit bundle sources', 'Edit meta repository source', 'Abort'])
                        if selectedAspect == 'Abort':
                            selectedDomain = None
                    elif selectedAspect=='Edit bundle sources':
                        operation = q.gui.dialog.askChoice("Please select the operation:", ['Add source', 'Remove source', 'Fill in credentials', 'Abort'])
                        if operation == 'Add source':
                            q.gui.dialog.askString('Please type in the url')
                            # add this source
                        elif operation == 'Remove source':
                            source = q.gui.dialog.askChoice("Please select the source to remove:", sources)
                            #remove the source
                            pass
                        elif operation == 'Fill in credentials':
                            pass
                        elif operation == 'Abort':
                            selectedAspect=None
                    elif selectedAspect=='Edit meta repository source':
                        pass
                else:
                    # ask domain
                    pass
                pass
            pass
        '''

    def updateAll(self):
        '''
        Updates all installed qpackages to the latest builds.
        The latest meta information is retrieved from the repository and based on this information,
        The install packages that have a buildnr that has been outdated our reinstall, thust updating them to the latest build.
        '''
        # update all meta information:
        q.qp.updateMetaData()
        # iterate over all install packages and install them
        # only when they are outdated will they truly install
        for p in q.qp.getInstalledPackages():
            p.install()
    
    def updateMetaDataAll(self,force=False):
        """
        Updates the metadata information of all qpackages
        This used to be called updateQPackage list
        @param is force True then local changes will be lost if any
        """
        q.qp.updateMetaData("",force)

    def mergeMetaDataAll(self,):
        """
        Tries to merge the metadata information of all qpackages with info on remote repo.
        This used to be called updateQPackage list
        """        
        q.qp.mergeMetaData("")        
        
    def updateMetaDataForDomain(self,domainName=""):
        """
        Updates the meta information of specific domain
        This used to be called updateQPackage list
        """
        if domainName=="":
            domainName = q.console.askChoice(q.qp.getDomainNames(), "Please choose a domain")
        q.qp.getDomainObject(domainName).updateMetadata("")

    def publishAll(self, commitMessage=None):
        """
        Publishes  all domains, for more informartion see publishDomain
        """
        if not commitMessage:
            commitMessage = q.console.askString('please enter a commit message')
        for domain in q.qp.getDomainNames():
            self.publishDomain(domain, commitMessage=commitMessage)

    def publishDomain(self, domain="", commitMessage=None):
        """
        Publishes a domain. To publish a domain means to make your local changes to the corresponding domain available to other users.
        A domain can be changed in the following ways: a new package is created in it, a package in it is modified, a package in it is deleted.
        To make the changes available to others the new metadata is uploaded to the mercurial servers and for the packages whos files have been modified,
        new bundles are created and uploaded to an ftp server.
        """
        if domain=="":
            domain=q.console.askChoice(q.qp.getDomainNames(), "Please select a domain")
        q.qp.getDomainObject(domain)._ensureDomainCanBeUpdated()
        q.qp.getDomainObject(domain).publish(commitMessage=commitMessage)

    def publishMetaDataAsTarGz(self, domain=""):
        """
        Compresses the meta data of a domain into a tar and upload that tar to the bundleUpload server.
        After this the that uptain there metadata as a tar can download the latest metadata.
        """
        if domain=="":
            domain=q.console.askChoice(q.qp.getDomainNames(), "Please select a domain")
        q.qp.publishMetaDataAsTarGz(domain=domain)
