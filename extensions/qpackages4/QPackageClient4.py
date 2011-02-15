import math
from pylabs import q
from QPackageObject4 import QPackageObject4
from ConvertQPackages import Convertor # temp
from Domain import *

# Testing QPackages?

# Needed abstractions: 1) asking userinput
#                      2) Files
#                      For files we copy the correct files to the correct locations

class QPackageClient4():
    sourcesFile = None

    """
    branch="default"
    methods to deal with qpackages, seen from client level

    @qlocation q.qp
    """
    def __init__(self):
        """
        """
        q.system.fs.createDir(q.system.fs.joinPaths(self._getPackageDir(),"metadata"))
        q.system.fs.createDir(q.system.fs.joinPaths(self._getPackageDir(),"files"))
        q.system.fs.createDir(q.system.fs.joinPaths(self._getPackageDir(),"bundles"))
        q.system.fs.createDir(q.system.fs.joinPaths(self._getPackageDir(),"metatars"))
        self._activeQpackageActionsReset()
        self.convertor = Convertor() # temp
        self.domains=[]
        self._metadatadirTmp=q.system.fs.joinPaths(q.dirs.varDir,"tmp","qpackages","md")
        q.system.fs.createDir(self._metadatadirTmp)

        # can't ask username here
        # because pylabs is not interactive yet
        # So we ask the username/passwd lazy in the domain object
        self.reloadconfig()

    def _renew(self):
        q.qp = QPackageClient4()


    def reloadconfig(self):
        """
        Reload all qpackage config data from disk
        """
        cfgpath=q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages4', 'sources.cfg')
        if not q.system.fs.exists(cfgpath):
            q.system.fs.createDir(q.system.fs.getDirName(cfgpath))
        else:
            cfg = q.tools.inifile.open(cfgpath)
            domainDict = dict()
            for domains in self.domains: domainDict[domains.domainname] = domains
            for domain in cfg.getSections():
                if domain in domainDict.keys():
                    self.domains.remove(domainDict[domain])
                self.domains.append(Domain(domainname=domain))

    def createNewQPackage(self, domain, name, version, description, supportedPlatforms):
        """
        Creates a new qpackage4, this includes all standard tasklets, a config file and a description.wiki file
        @param domain:      string - The domain the new qpackage should reside in
        @param name:        string - The name of the new qpackage
        @param version:     string - The version of the new qpackage
        @param description: string - The description of the new qpackage (is stored in the description.wiki file)
        """
        # Create one in the repo
        if not domain in q.qp.getDomainNames():
            raise RuntimeError('Provided domain is nonexistent on this system')
        if self.getDomainObject(domain).metadataFromTgz:
            raise RuntimeError('The meta data for domain ' + domain + ' is coming from a tgz, you cannot create new packages in it.')
        branch=self.getDomainObject(domain).metadataBranch
        qp      = QPackageObject4(domain, name, version, branch, description, new=True)
        qp.prepareForUpdatingFiles(suppressErrors=True)
        qp.supportedPlatforms = supportedPlatforms
        qp.save()
        return qp


############################################################
##################  GET FUNCTIONS  #########################
############################################################

    def get(self, domain, name, version,branch=""):
        """
        Returns a qpackage from the default repo or from a certain branch in the repo if it is specified
        @param domain:  string - The domain the qpackage is part from
        @param name:    string - The name of the qpackage
        @param version: string - The version of the qpackage
        @param branch:  string - The branch in which the qpackage is stored in the repo
        """
        # return a package from the default repo
        key = '%s%s%s%s' % (domain,name,version, branch)
        if self._getcache.has_key(key):
            return self._getcache[key]
        if self.exists(domain,name,version)==False:
            raise RuntimeError("Could not find package %s." % self.getMetadataPath(domain,name,version))
        self._getcache[key]=QPackageObject4(domain, name, version,branch)
        return self._getcache[key]

    def downloadAllBundles(self):
        """
        Downloads all bundles from all packages in all domains from the repos
        """
        for package in self.getQPackageObjects():
            package._download()

    def exists(self,domain,name,version):
        """
        Checks whether the qpackage's metadata path is currently present on your system
        """
        return q.system.fs.exists(self.getMetadataPath(domain,name,version))

    def getInstalledPackages(self):
        """
        Returns a list of all currently installed packages on your system
        """
        return [p for p in self.getQPackageObjects() if p.isInstalled()]

    def getPackagesWithBrokenDependencies(self):
        """
        Returns a list of all qpackages which have dependencies that cannot be resolved
        """
        return [package for package in self.getQPackageObjects() if len(package.getBrokenDependencies()) > 0]
    
    def getPendingReconfigurationPackages(self):
        """
        Returns a List of all qpackages that are pending for configuration
        """
        return filter(lambda qpackage: qpackage.isPendingReconfiguration(), self.getQPackageObjects())

#############################################################
######################  DOMAINS  ############################
#############################################################

    def getDomainObject(self,domain):
        """
        Get provided domain as an object
        """
        for item in self.domains:
            if item.domainname.lower()==domain.lower().strip():
                return item

    def getDomainNames(self):
        """
        Returns a list of all domains present in the sources.cfg file
        """
        result=[]
        for item in self.domains:
            result.append(item.domainname)
        return result


############################################################
###################  GET PATH FUNCTIONS  ###################
############################################################

    def _getPackageDir(self):
        """
        Get qpackage for v4 version
        """
        packagedir=q.dirs.packageDir+"4"
        return packagedir

    def getMetadataPath(self,domain,name,version,fromtmp=False):
        """
        Returns the metadatapath for the provided qpackage
        if fromtmp is True, then tmp directorypath will be returned

        @param domain:  string - The domain of the qpackage
        @param name:    string - The name of the qpackage
        @param version: string - The version of the qpackage
        @param fromtmp: boolean
        """
        if fromtmp:
            self._metadatadirTmp
            return q.system.fs.joinPaths(self._metadatadirTmp,domain,name,version)
        else:
            return q.system.fs.joinPaths(self._getPackageDir(),"metadata",domain,name,version)

    def getDataPath(self,domain,name,version):
        """
        Returns the filesdatapath for the provided qpackage
        @param domain:  string - The domain of the qpackage
        @param name:    string - The name of the qpackage
        @param version: string - The version of the qpackage
        """
        return q.system.fs.joinPaths(self._getPackageDir(),"files",domain,name,version)

    def getMetaTarPath(self, domainName):
        """
        Returns the metatarsdatapath for the provided domain
        This is the place where the .tgz bundles are stored for each domain
        """
        return q.system.fs.joinPaths(self._getPackageDir(), "metatars", domainName)

    # This is a name inconsitency with qpackage.getPathFiles
    #                                          .getPathBundles
    # Put Path in front or in back, but not both?
    def getBundlesPath(self):
        """
        Returns the bundlesdatapath where all bundles are stored for all different domains
        """
        return q.system.fs.joinPaths(self._getPackageDir(),"bundles")


############################################################
######################  CACHING  ###########################
############################################################

    _getcache = {}

    def _deleteFromCache(self, domain, name, version):
        #called by a package when we call delete on it so it can be gatbage collected
        key = '%s%s%s%s' % (domain, name, version, self.getBranchname(domain))
        self._getcache.remove(key)
        key = '%s%s%s%s' % (domain, name, version, "default")
        self._getcache.remove(key)



############################################################
##########################  FIND  ##########################
############################################################

    def findNewest(self, name="", domain="", minversion="",maxversion="",platform=q.enumerators.PlatformType.GENERIC, returnNoneIfNotFound=False):
        """
        Find the newest qpackage which matches the criteria
        If more than 1 qpackage matches -> error
        If no qpackage match and not returnNoneIfNotFound -> error
        @param name:       string - The name of qpackage you are looking for
        @param domain:     string - The domain of the qpackage you are looking for
        @param minversion: string - The minimum version the qpackage must have
        @param maxversion: string - The maximum version the qpackage can have
        @param platform:   string - Which platform the qpackage must run on
        @param returnNoneIfNotFound: boolean - if true, will return None object if no qpackages have been found
        """
        results=self.find(domain=domain,name=name,platform=platform)
        namefound=""
        domainfound=""
        if minversion=="":
            minversion="0"
        if maxversion=="":
            maxversion="100.100.100"
        #look for duplicates
        for qp in results:
            if namefound=="":
                namefound=qp.name
            if domainfound=="":
                domainfound=qp.domain
            if qp.domain<>domainfound or qp.name<>namefound:
                packagesStr="\n"
                for qp2 in results:
                    packagesStr="    %s\n" % str(qp2)
                raise RuntimeError("Found more than 1 qpackage matching the criteria.\n %s" % packagesStr)
        #check for version match
        if len(results)==0:
            if returnNoneIfNotFound:
                return None
            raise RuntimeError("Did not find qpackage with criteria domain:%s, name:%s, platform:%s (independant from version)" % (domain,name,platform))
        # filter packages so they ly between min and max version bounds
        result=[qp for qp in results if self._getVersionAsInt(minversion)<=self._getVersionAsInt(qp.version)<=self._getVersionAsInt(maxversion)]
        result.sort(lambda qp1, qp2: - int(self._getVersionAsInt(qp1.version) - self._getVersionAsInt(qp2.version)))
        if not result:
            if returnNoneIfNotFound:
                return None
            raise RuntimeError("Did not find qpackage with criteria domain:%s, name:%s, minversion:%s, maxversion:%s, platform:%s" % (domain,name,minversion,maxversion,platform))
        return result[0]

    def find(self, name="", domain="", version="", platform=q.enumerators.PlatformType.GENERIC):
        """
        returns list of found qpackages
        @param domain:  string - The name of qpackage domain, when using * means partial name
        @param name:    string - The name of the qpackage you are looking for
        @param version: string - The version of the qpackage you are looking for
        """
        q.logger.log("Find qpackage domain:%s name:%s version:%s platform:%s" %(domain,name,version,platform))
        #work with some functional methods works faster than doing the check everytime

        def findPartial(pattern,text):
            pattern=pattern.replace("*","")
            if text.lower().find(pattern.lower().strip())<>-1:
                return True
            return False

        def findFull(pattern,text):
            return pattern.strip().lower()==text.strip().lower()

        def alwaysReturnTrue(pattern,text):
            return True

        domainFindMethod=alwaysReturnTrue
        nameFindMethod=alwaysReturnTrue
        versionFindMethod=alwaysReturnTrue

        if domain<>"":
            if domain.find("*")<>-1:
                domainFindMethod=findPartial
            else:
                domainFindMethod=findFull
        if name<>"":
            if name.find("*")<>-1:
                nameFindMethod=findPartial
            else:
                nameFindMethod=findFull
        if version <>"":
            if version.find("*")<>-1:
                versionFindMethod=findPartial
            else:
                versionFindMethod=findFull
        result=[]
        for p_domain, p_name, p_version in self._getQPackageTuples():
            if domainFindMethod(domain,p_domain) and nameFindMethod(name,p_name) and versionFindMethod(version,p_version):
                result.append([p_domain, p_name, p_version])
        result2=[]
        for item in result:
                result2.append(self.get(item[0],item[1], item[2]))
        return result2

    # Used in getQPackageObjects and that is use in find
    def _getQPackageTuples(self):
        res = list()
        domains=self.getDomainNames()
        for domainName in domains:
            domainpath=q.system.fs.joinPaths(self._getPackageDir(),"metadata",domainName)
            if q.system.fs.exists(domainpath):
                packages= [p for p in q.system.fs.listDirsInDir(domainpath,dirNameOnly=True) if p != '.hg'] # skip hg file
                for packagename in packages:
                    packagepath=q.system.fs.joinPaths(domainpath,packagename)
                    versions=q.system.fs.listDirsInDir(packagepath,dirNameOnly=True)
                    for version in versions:
                        res.append([domainName,packagename,version])
        return res

    def getQPackageObjects(self, platform=q.enumerators.PlatformType.GENERIC, domain=None):
        """
        Returns a list of qpackage objects for specified platform & domain
        """
        def hasPlatform(package):
            return any([supported.has_parent(platform) for supported in package.supportedPlatforms])
        packageObjects = [self.get(*p) for p in self._getQPackageTuples()]
        return [p for p in packageObjects if hasPlatform(p) and (domain == None or p.domain == domain)]


############################################################
########  CHECK ON ALREADY EXECUTED ACTIONS  ###############
############################################################

    def _activeQpackageActionsReset(self):
        """
        make sure that previous actions on qpackages are not remembered, re-execute all actions
        """
        self._activeActions={}

    def _activeQpackageIsActionsAlreadyExecuted(self,domain,name,version,buildnr,tag,action):
        """
        check if that action has already been executed if yes return true
        """
        return self._activeActions.has_key("%s_%s_%s_%s_%s_%s" % (domain,name,version,buildnr,tag,action))

    def _activeQpackageSetActionsExecuted(self,domain,name,version,buildnr,tag,action):
        """
        set that the action has already been executed
        """
        self._activeActions["%s_%s_%s_%s_%s_%s" % (domain,name,version,buildnr,tag,action)]=True


############################################################
#################  UPDATE / PUBLISH  #######################
############################################################

    def updateMetaData(self,domain="",force=False):
        """
        Does an update of the meta information repo for each domain
        """

        if domain<>"":
            q.logger.log("Update metadata information for qpackages domain %s" % domain, 1)
            d=self.getDomainObject(domain)
            d.updateMetadata(force=force)
        else:
            for domainName in self.getDomainNames():
                self.updateMetaData(domainName, force=force)

    def mergeMetaData(self,domain="", commitMessage=''):
        """
        Does an update of the meta information repo for each domain
        """

        if not q.qshellconfig.interactive:
            if commitMessage == '':
                raise RuntimeError('Need commit message')

        if domain<>"":
            q.logger.log("Merge metadata information for qpackages domain %s" % domain, 1)
            d=self.getDomainObject(domain)
            d.mergeMetadata(commitMessage=commitMessage)
        else:
            for domainName in self.getDomainNames():
                self.mergeMetaData(domainName, commitMessage=commitMessage)

    def publishMetaDataAsTarGz(self, domain=""):
        """
        Updates the metadata for all domains (if no domain specified), makes a tar from it and uploads the tar to the qpackage server so tar based clients can now use the latest packages
        """
        if domain<>"":
            q.logger.log("Push metadata information for qpackages domain %s to reposerver." % domain, 1)
            d = self.getDomainObject(domain)
            d.buildTar()
            d.publishTar()
        else:
            for domainName in self.getDomainNames():
                self.publishMetaDataAsTarGz(domainName)

    def publish(self, commitMessage,domain=""):
        """
        Publishes all domains' bundles & metadata (if no domain specified)
        @param commitMessage: string - The commit message you want to assign to the publish
        """
        if domain=="":
            for domain in q.qp.getDomainNames():
                self.publish( commitMessage=commitMessage,domain=domain)
        else:
            domainobject=q.qp.getDomainObject(domain)
            domainobject.publish(commitMessage=commitMessage)


##########################################################
####################  RECONFIGURE  #######################
##########################################################

    def _setHasPackagesPendingConfiguration(self, value=True):
        file = q.system.fs.joinPaths(q.dirs.baseDir, 'cfg', 'qpackages4', 'reconfigure.cfg')
        if not q.system.fs.exists(file):
            ini_file = q.tools.inifile.new(file)
        else:
            ini_file = q.tools.inifile.open(file)

        if not ini_file.checkSection('main'):
            ini_file.addSection('main')


        ini_file.setParam("main","hasPackagesPendingConfiguration", "1" if value else "0")
        ini_file.write()

    def _hasPackagesPendingConfiguration(self):
        file = q.system.fs.joinPaths(q.dirs.baseDir, 'cfg', 'qpackages4', 'reconfigure.cfg')
        if not q.system.fs.exists(file):
            return False
        ini_file = q.tools.inifile.open(file)

        if ini_file.checkSection('main'):
            return ini_file.getValue("main","hasPackagesPendingConfiguration") == '1'

        return False

    def _runPendingReconfigeFiles(self):
        if not self._hasPackagesPendingConfiguration():
            return

        # Get all packages that need reconfiguring and reconfigure them
        # We store the state to reconfigure them in their state files
        configuredPackages = set()

        def configure(package):
            # If already processed return
            if package in configuredPackages:
                return True
            configuredPackages.add(package)

            # first make sure depending packages are configured
            for dp in package.getDependencies(recursive=False):
                if not configure(dp):
                    return False

            # now configure the package
            if package.isPendingReconfiguration():
                q.logger.log("qpackage %s %s %s needs reconfiguration" % (package.domain,package.name,package.version),3)
                try:
                    package.configure()
                except:
                    q.debugging.printTraceBack('Got error while reconfiguring ' + str(package))
                    if q.console.askChoice(['Skip this one', 'Go to shell'], 'What do you want to do?') == 'Skip this one':
                        return True
                    else:
                        return False
            return True


        pendingPackages = self.getPendingReconfigurationPackages()
        hasPendingConfiguration = False
        for p in pendingPackages:
            if not configure(p):
                hasPendingConfiguration = True
                break

        self._setHasPackagesPendingConfiguration(hasPendingConfiguration)


############################################################
################  SUPPORTING FUNCTIONS  ####################
############################################################

    def _getVersionAsInt(self,version):
        """
        @param version is string
        """
        if version.find(",")<>-1:
            raise RuntimeError("version string can only contain numbers and . e.g. 1.1.1")
        if version=="":
            version="0"
        if version.find(".")<>-1:
            versions=version.split(".")
        else:
            versions=[version]
        if len(versions)>4:
            raise RuntimeError("max level of versionlevels = 4 e.g. max 1.1.1.1")
        #make sure always 4 levels of versions for comparison
        while(len(versions)<4):
            versions.append("0")
        result=0
        for counter in range(0,len(versions)):
            level=len(versions)-counter-1
            if versions[counter]=="":
                versions[counter]="0"
            result=int(result+(math.pow(1000,level)*int(versions[counter].strip())))
        return result
