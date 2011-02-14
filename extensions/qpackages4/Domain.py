from pymonkey import q
from pymonkey.Shell import *

class Domain(): 

###############################################################
################# BEGIN OF GETTERS AND SETTERS ################
###############################################################

    # Lazy BundleDownload
    def _getBundleDownload(self):
        self._ensureInitialized()
        return self._bundleDownload

    def _setBundleDownload(self, value):
        self._bundleDownload = value
        self.saveConfig()

    #Lazy BundleUpload
    def _getBundleUpload(self):
        self._ensureInitialized()
        return self._bundleUpload

    def _setBundleUpload(self, value):
        self._bundleUpload = value
        self.saveConfig()

    #Lazy MetadataBranch
    def _getMetadataBranch(self):
        self._ensureInitialized()
        return self._metadataBranch

    def _setMetadataBranch(self, value):
        self._metadataBranch = value
        self.saveConfig()

    #Lazy MetaDataFromMercurial
    def _getMetadataFromMercurial(self):
        self._ensureInitialized()
        return self._metadataFromMercurial

    def _setMetadataFromMercurial(self, value):
        self._metadataFromMercurial = value
        self.saveConfig()

    #Lazy metadataFromTgz
    def _getMetadataFromTgz(self):
        self._ensureInitialized()
        return self._metadataFromTgz

    def _setMetadataFromTgz(self, value):
        self._metadataFromTgz = value
        self.saveConfig()

    bundleDownload        = property(_getBundleDownload, _setBundleDownload)
    bundleUpload          = property(_getBundleUpload, _setBundleUpload)
    metadataBranch        = property(_getMetadataBranch, _setMetadataBranch)
    metadataFromMercurial = property(_getMetadataFromMercurial, _setMetadataFromMercurial)
    metadataFromTgz       = property(_getMetadataFromTgz, _setMetadataFromTgz)


    bundleDownload        = property(_getBundleDownload, _setBundleDownload)
    bundleUpload          = property(_getBundleUpload, _setBundleUpload)


    # Lazy hg connections

    def _getHGClient(self):
        self._ensureHgConnectionsAreInitialized()
        return self._hgclient

    def _setHGClient(self, hgclient):
        raise RuntimeError('readonly')

    def _getTmpCHGlient(self):
        self._ensureHgConnectionsAreInitialized()
        return self._hgclientTmpC

    def _setTmpCHGClient(self, hgclient):
        raise RuntimeError('readonly')

    hgclient    = property(_getHGClient, _setHGClient)
    hgclientTmp = property(_getTmpCHGlient, _setTmpCHGClient)


    ################################################################
    ################# END OF GETTERS AND SETTERS ###################
    ################################################################

    """
    is representation of domain
    source can come from tgz or from mercurial
    """

    def __init__(self, domainname): ## Init must come after definition of lazy getters and setters!
        self.domainname  = domainname
        self.initialized = False

    def _ensureInitialized(self):


        if self.initialized:
            return
        self.initialized = True

        cfgFilePath = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages4', 'sources.cfg')
        cfg = q.tools.inifile.open(cfgFilePath)

        def replace(string1, string2):
            content = q.system.fs.fileGetContents(cfgFilePath)
            content = content.replace(string1, string2)
            q.system.fs.writeFile(cfgFilePath, content)

        def getCfgParam(cfg, domain, keyname):
            """
            get param from inifile and if predefined keywords found ask user to fill in
            """
            val=cfg.getValue(domain, keyname)            
            for i in range(10):
                usernamePattern = '$username_%i$' % i
                passwordPattern = '$password_%i$' % i
                if val.find(usernamePattern) != -1:
                    username = q.console.askString("login for connectiontype " + keyname + " of domain " + domain + " please", 'guest')
                    replace(usernamePattern, username)
                    val = val.replace(usernamePattern, username)
                if val.find(passwordPattern) != -1:
                    password = q.console.askString("Your password please", '1234')
                    replace(passwordPattern, password)
                    val = val.replace(passwordPattern, password)
            return val

        # We can ask passwords now because pymonkey is not yet ready for
        self._metadataFromTgz=int(getCfgParam(cfg, self.domainname, 'metadataFromTgz').strip())
        self._bundleDownload=getCfgParam(cfg, self.domainname, 'bundleDownload')
        self._metadataBranch= cfg.getValue(self.domainname, 'metadataBranch') if cfg.checkParam(self.domainname, 'metadataBranch') else 'default'

        self._hgclient=None
        self._hgclientTmp=None

        self.metadatadir=q.system.fs.joinPaths(q.dirs.packageDir+"4","metadata", self.domainname)
        self._metadatadirTmp=""

        self._bundleUpload = None
        self._metadataFromMercurial = None

        if not self._metadataFromTgz:
            self._metadataFromMercurial=getCfgParam(cfg, self.domainname, 'metadataFromMercurial')
            if cfg.checkParam(self.domainname, 'bundleUpload'):
                self._bundleUpload=getCfgParam(cfg, self.domainname, 'bundleUpload')

        q.system.fs.createDir(self.metadatadir)
        self._metadataFromTgz = self._metadataFromTgz==1 or self._metadataFromTgz==True
        if not self.metadataFromTgz:
            #means we work with mercurial for this domain
            self._metadatadirTmp = q.system.fs.joinPaths(q.dirs.varDir,"tmp","qpackages","md", self.domainname)
            ##self._ensureHgConnectionsAreInitialized()


    def saveConfig(self):
        """
        Saves changes to the qpackages4 config file
        """
        cfg = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackages4', 'sources.cfg'))
        if not cfg.checkSection(self.domainname):
            cfg.addSection(self.domainname)
        cfg.setParam(self.domainname, 'bundleDownload', self.bundleDownload)
        cfg.setParam(self.domainname, 'bundleUpload', self.bundleUpload)
        cfg.setParam(self.domainname, 'metadataBranch', self.metadataBranch)
        cfg.setParam(self.domainname, 'metadataFromMercurial', self.metadataFromMercurial)
        cfg.setParam(self.domainname, 'metadataFromTgz', int(self.metadataFromTgz))
        cfg.write()

    def _ensureHgConnectionsAreInitialized(self):
        """
        Ensures we are connected to hg
        Don't do this in the constructor because the mercurial extension may noy yet have been loaded

        """

        if self.metadataFromTgz:
            raise RuntimeError('Meta data is comming from tar, cannot make connection to mercurial server ')

        if self._hgclient==None:
            self._hgclient=q.clients.mercurial.getclient(self.metadatadir, self.metadataFromMercurial, branchname=self._metadataBranch)
            if not q.system.fs.exists(self._metadatadirTmp):
                q.system.fs.createDir(self._metadatadirTmp)
                q.system.fs.copyDirTree(self.metadatadir,self._metadatadirTmp)
                self._hgclientTmp=q.clients.mercurial.getclient(self._metadatadirTmp,self.metadataFromMercurial,"default")
                self._hgclientTmp.update("default")
            self._hgclientTmp=q.clients.mercurial.getclient(self._metadatadirTmp,self.metadataFromMercurial)

    def hasModifiedMetadata(self):
        """
        Checks for the entire domain if it has any modified metadata
        """
        #check mercurial
        if not self.metadataFromTgz:
            self._ensureInitialized()
            return (self.hgclient.hasModifiedFiles())
        else:
            return False

    def hasModifiedFiles(self): #This is the prepared files?
        """
        Checks for the entire domain if it has any modified files
        """
        for qpackage in self.getQPackages():
            if qpackage.hasModifiedFiles():
                return True
        return False

    def _mercurialLinesToPackageTuples(self, changedFiles):
        changedPackages = set()
        for line in changedFiles: # @todo test on windows
                #  exampleline: zookeeper/1.0/qpackage.cfg
                #  exampleline: zookeeper/1.0/tasklets/sometasklet.py
            line=line.replace("\\","/") #try to get it to work on windows
            splitted=line.split('/')
            if len(splitted)>1:
                name    = splitted[0]
                version = splitted[1]
                qpackage = (self.domainname, name, version)
                changedPackages.add(qpackage)
        return list(changedPackages)

    def getQPackageTuplesWithNewMetadata(self):
        changedFiles = self.hgclient.getModifiedFiles()
        changedFiles = changedFiles["added"] + changedFiles["nottracked"]
        return self._mercurialLinesToPackageTuples(changedFiles)

    def getQPackageTuplesWithModifiedMetadata(self):
        changedFiles = self.hgclient.getModifiedFiles()
        changedFiles = changedFiles["modified"]
        return self._mercurialLinesToPackageTuples(changedFiles)

    def getQPackageTuplesWithDeletedMetadata(self):
        changedFiles = self.hgclient.getModifiedFiles()
        changedFiles = changedFiles["removed"] + changedFiles['missing']
        return self._mercurialLinesToPackageTuples(changedFiles)

    # Packages that have been deleted will never have modified files
    def getQPackageTuplesWithModifiedFiles(self):
        # Add packages with modified files
        changedQPackages=set()
        for qpackage in self.getQPackages():
            if qpackage.hasModifiedFiles():
                changedQPackages.add((qpackage.domain, qpackage.name, qpackage.version))
        return list(changedQPackages)

    def getModifiedQPackages(self):
        """
        Returns a list with all the packages whose files or metadata have been changed in the currently active domain
        """      
        changedFiles = self.hgclient.getModifiedFiles()
        changedFiles=changedFiles["removed"] + changedFiles['missing']+changedFiles["modified"]+changedFiles["added"] + changedFiles["nottracked"]
        modpackages= self._mercurialLinesToPackageTuples(changedFiles)
        modpackages.extend(self.getQPackageTuplesWithModifiedFiles())
        return modpackages

    def hasDomainChanged(self):
        return self.hasModifiedMetadata() or self.hasModifiedFiles()

    def switchToBranch(self, branch): # a tar is not switchable, the userRepo is also not switchable
        """
        Switches to another branch of the currently active domain
        """
        q.logger.log("Switch metadata for domain %s to other branch." % self.domainname,2)
        if not self.metadataFromTgz:
            self._ensureInitialized()
            return(self.hgclient.switchbranch(branch)) # should this not switch the temporary repo?
        else:
            raise RuntimeError("Cannot switch to branch when domain metadata comes from tgz. Domain=%s" % self.domainname)

    def publishMetadata(self, commitMessage=''): # tars are not uploadable
        """
        Publishes all metadata of the currently active domain
        """
        q.logger.log("Publish metadata for domain %s" % self.domainname,2)

        if not self.metadataFromTgz:
            self.hgclient.commitpush(commitMessage=commitMessage,ignorechanges=False,addRemoveUntrackedFiles=True,trymerge=True, release=self.metadataBranch)
        else:
            raise RuntimeError('Meta data is comming from tar for domain ' + domain + ', cannot publish modified metadata.')

    def _publishMetadataTemp(self): 
        q.logger.log("Publish temp metadata for domain %s" % self.domainname,2)
        if self.metadataFromTgz:
            raise RuntimeError("A tgz source does not have a tmp repo!")
        self.hgclientTmp.commitpush(commitMessage="update buildnrs on head",ignorechanges=False,addRemoveUntrackedFiles=True,trymerge=True, release=self.metadataBranch)


    def publish(self, commitMessage):
        """
        Publishes the currently active domain's bundles & metadata
        """
        q.logger.log("Publish metadata for qpackage domain: %s " % self.domainname ,2)

        # determine which packages changed
        newPackagesMetaData      = self.getQPackageTuplesWithNewMetadata()
        modifiedPackagesMetaData = self.getQPackageTuplesWithModifiedMetadata() + newPackagesMetaData
        deletedPackagesMetaData  = self.getQPackageTuplesWithDeletedMetadata()
        modifiedPackagesFiles    = self.getQPackageTuplesWithModifiedFiles()
        modifiedPackages         = list(set(newPackagesMetaData + modifiedPackagesMetaData + deletedPackagesMetaData + modifiedPackagesFiles))

        # If there are no packages to do something with don't bother the user
        # with annoying questions
        if not modifiedPackages:
            q.logger.log("There where no modified packages for domain: %s " % self.domainname , 1)
            return

        # report to the user what will happen if he proceeds
        q.logger.log('The following packages will be published:', 1)
        just = 15
        mess  = ' ' * 4 + 'domain:'.ljust(just) + 'name:'.ljust(just) + 'version:'.ljust(just)
        mess +=           'metachanged:'.ljust(just) + 'fileschanged:'.ljust(just) + 'status:'.ljust(just) + '\n'
        for package in modifiedPackages:
            metachanged  = package in modifiedPackagesMetaData
            fileschanged = package in modifiedPackagesFiles

            status = 'UNKOWN-ERROR'
            if package in newPackagesMetaData:
                status = 'NEW'
            elif package in modifiedPackagesMetaData:
                status = 'MODIFIED'
            elif package in deletedPackagesMetaData:
                status = 'DELETED'
            elif package in modifiedPackagesFiles:
                status = 'FILES MODIFIED'
            else:
                raise RuntimeError('Unkown status!')

            mess += ' ' * 4 + package[0].ljust(just) + package[1].ljust(just) + package[2].ljust(just)
            mess +=           str(metachanged).ljust(just) + str(fileschanged).ljust(just) + str(status).ljust(just) + '\n'

        q.logger.log('publishing packages for domain %s:\n' % self.domainname + mess, 1)
        if q.qshellconfig.interactive:
            if not q.console.askYesNo('continue?'):
                return

        q.logger.log('publishing packages:\n' + mess, 5)

        if not commitMessage:
            commitMessage = q.console.askString('please enter a commit message')

        # If the mercurial source for this domain is not trunck
        # We update the tmprepo only if branch of active <> "default"
        # We get a qpackage from trunk which will come from tmprepo if active branch <> "default"
        # we build the corresponding package for each modified package in the trunck repo
        # We update its buildnumber by two
        # We upload the alternative repo
        # We then update the buildnumber of each package in the current branch
        # Incrementing the trunck and incrementing the buildnumbers of the branch should be in one transaction,
        # But we don't have the means to do this
        # we should minimize the time to commit, this minimizes the change of concurrent modification errors!
        # This is why bundles are uploaded afterwards
        # @type source DomainSource

        q.logger.log("1) Updating buildNumbers in metadata and uploading files", 1)

        # The build numbers are not modified, but we already committed?
        # How does this work again?
        # Tmp is not updated here?
        # This is actually an update and merge
        self.updateMetadata(commitMessage=commitMessage)  #makes sure metadata from tmp & active repo is updated
        # self._updateMetadataTmpLocation() Where will the tmp repo get updated??

        q.logger.log("2) Updating buildNumbers in metadata and uploading files", 1)

        for qpackageActive in modifiedPackages:
            if qpackageActive in deletedPackagesMetaData:
                q.logger.log("Deleting files of package " + str(qpackageActive), 1)
                if self.metadataBranch<>"default":
                    pass # Do nothing here
                else:
                    # The package should no longer exists on other branches
                    # Todo verify this
                    pass
                # Delete the files of the package
                q.system.fs.removeDirTree(q.qp.getDataPath(*qpackageActive))
            else:
            #if qpackageActive in newPackagesMetaData or qpackageActive in modifiedPackagesMetaData:
                qpackageActiveObject = q.qp.get(qpackageActive[0], qpackageActive[1], qpackageActive[2])
                q.logger.log("For qpackage: " + str(qpackageActiveObject), 1)
                q.logger.log("current numbers : " + qpackageActiveObject.reportNumbers(), 1)
                # Update build number
                if self.metadataBranch<>"default":
                    qpackageDefault=q.qp.get(package.domain,package.name,package.version,branch="default")  #qpackage will be from tmp or from active
                    lastBuildNr = qpackageDefault.buildNr
                    qpackageDefault.buildNr      = lastBuildNr + 2
                    qpackageActiveObject.buildNr = lastBuildNr + 1
                    qpackageDefault.save()
                else:
                    qpackageActiveObject.buildNr  = qpackageActiveObject.buildNr + 1

                # Update meta and bundle number
                if qpackageActive in modifiedPackagesMetaData:
                    qpackageActiveObject.metaNr = qpackageActiveObject.buildNr
                if qpackageActive in modifiedPackagesFiles:
                    qpackageActiveObject.bundleNr = qpackageActiveObject.buildNr
                q.logger.log("updated to new numbers : " + qpackageActiveObject.reportNumbers(), 1)
                qpackageActiveObject.save()

            # At this point we may be
            if qpackageActive in modifiedPackagesFiles:
                qpackageActiveObject = q.qp.get(qpackageActive[0], qpackageActive[1], qpackageActive[2])
                qpackageActiveObject._compress(overwriteIfExists=True)
                qpackageActiveObject._upload()

        # If we are here and the network drops out
        # What is the result? The tasklets of the last buildNr have changed without incrementing the buildNr
        # Next time we run this the meta data no longer changed and we dont increment the metaNr as a result of it
        #@feedback kristof: this is no issue, above will happen again in next run, the metadata was not uploaded yet so no issue

        # import pdb
        # pdb.set_trace()
        q.logger.log("3) Commiting and uploadind metadata with updated buildNumbers", 1)
        self.publishMetadata(commitMessage=commitMessage)
        if self.metadataBranch<>"default":
            self._publishMetadataTemp(commitMessage=commitMessage)

        # Only do this after complete success!
        # If something goes wrong we know which files where modified
        for qpackageActive in modifiedPackagesFiles:
            qpackageActiveObject = q.qp.get(qpackageActive[0], qpackageActive[1], qpackageActive[2])
            qpackageActiveObject._resetPreparedForUpdatingFiles()


    def updateMetadata(self, commitMessage="",force=False):
        """
        Get all metadata of the currently active domain's repo servers and store locally
        """
        self._ensureInitialized()
        if not self.metadataFromTgz:
            q.action.start("updateqpackage metadata for domain %s" % self.domainname,\
                           "Could not update the metadata for the domain",\
                           "go to directory %s and update the metadata yourself using mercurial" % self.metadatadir)
            self.hgclient.pull()
            #Why is this commented out?
            self.hgclient.updatemerge(commitMessage=commitMessage,ignorechanges=False,addRemoveUntrackedFiles=True,trymerge=True, release=self.metadataBranch)
            # self.hgclient.update(force=force, release=self.metadataBranch)
            #self.hgclientTmp.pullupdate(commitMessage=commitMessage) ? not needed no?
            q.action.stop()
        else:
            repoUrl        = self.bundleDownload
            targetTarDir   = q.qp.getMetaTarPath(self.domainname)
            remoteTarFile  = q.system.fs.joinPaths(repoUrl, self.metadataBranch + '.branch.tgz')
            q.logger.log("Getting meta data for a tar: %s" % remoteTarFile, 1)
            if not q.system.fs.exists(targetTarDir):
                q.system.fs.createDir(targetTarDir)
            q.cloud.system.fs.copyFile(remoteTarFile, 'file://' +  targetTarDir) # Add protocol
            ## Extract the tar to the correct location
            if q.system.fs.exists(self.metadatadir):
                q.system.fs.removeDirTree(self.metadatadir)
            targetTarFile = q.system.fs.joinPaths(targetTarDir, self.metadataBranch + '.branch.tgz')
            q.system.fs.targzUncompress(targetTarFile, self.metadatadir)

        # Reload all packages
        for package in self.getQPackages():
            package.reload()

    def mergeMetadata(self, commitMessage=""):
        """
        #@todo doc
        """
        self._ensureInitialized()
        if not self.metadataFromTgz:
            q.action.start("update & merge qpackage metadata for domain %s" % self.domainname,\
                           "Could not update/merge the metadata for the domain",\
                           "go to directory %s and update/merge/commit the metadata yourself using mercurial" % self.metadatadir)
            self.hgclient.pull()
            self.hgclient.updatemerge(commitMessage=commitMessage,ignorechanges=False,addRemoveUntrackedFiles=True,trymerge=True, release=self.metadataBranch)	    
            #self.hgclientTmp.pullupdate(commitMessage=commitMessage) ? not needed no?
            q.action.stop()
        else:
            raise RuntimeError("Cannot merge metadata from tgz info, make sure in sources.cfg file this domain %s metadata is not coming from a tgz file"% self.domainname)

        # Reload all packages
        for package in self.getQPackages():
            package.reload()	    

    def buildTar(self):
        """
        Builds a tar file from the metadata in the user repo
        """
        self._ensureInitialized()
        revisionTxt = q.system.fs.joinPaths(self.metadatadir, 'revision.txt')
        q.system.fs.writeFile(revisionTxt, self.hgclient.id())
        targetTarDir  = q.qp.getMetaTarPath(self.domainname)
        targetTarFile = q.system.fs.joinPaths(targetTarDir, self.metadataBranch + '.branch.tgz')
        q.logger.log("Building tar file from " + self.metadatadir + " to location " + targetTarFile)
        q.system.fs.targzCompress(self.metadatadir, targetTarFile, pathRegexExcludes=['.*\/\.hg\/.*'])
        q.system.fs.removeFile(revisionTxt)

    def publishTar(self):
        """
        Upload the tar from the metatars directory to the ftp server remote
        """
        targetTarDir  = q.qp.getMetaTarPath(self.domainname)
        targetTarFile = q.system.fs.joinPaths(targetTarDir, self.metadataBranch + '.branch.tgz')
        remoteTarDir  = self.bundleUpload
        q.logger.log("Uploading tar file " + targetTarFile + " to location " + remoteTarDir)
        q.cloud.system.fs.copyFile('file://' +  targetTarFile, remoteTarDir + "/")

    def _updateMetadataTmpLocation(self,branch="default"):
        self.hgclientTmp.pull()
        self.hgclientTmp.update(branch)

    def _isTrackingFile(self, file):
        # test if the file is commited
        self._ensureHgConnectionsAreInitialized()
        return self.hgclient.isTrackingFile(file)

    def getLatestBuildNrForQPackage(self,domain,name,version):
        """
        Returns the lastest buildnumber
        Buildnr comes from default tip of mercurial repo
        """        
        qpackage=q.qp.get(domain,name,version,"default",fromTmp=True)
        return qpackage.buildNr

    def getQPackages(self):
        """
        Returns a list of all qpackages of the currently active domain
        """
        return q.qp.find(domain=self.domainname)

    def __str__(self):
        self._ensureInitialized()
        return "domain:%s\nbundleDownload:%s\nbundleUpload:%s\nmetadataBranch:%s\nmetadataFromMercurial:%s\nmetadataFromTgz:%s\n" % \
               (self.domainname,self.bundleDownload,self.bundleUpload,self.metadataBranch,self.metadataFromMercurial,self.metadataFromTgz)

    def __repr__(self):
        return self.__str__()

    def _ensureDomainCanBeUpdated(self):
        if self.metadataFromTgz:
            raise RuntimeError('For domain: ' + self.domainname + ': Meta data comes from tgz, cannot update domain.')
        if self.bundleUpload == None:
            raise RuntimeError('For domain: ' + self.domainname + ': Not bundleUpload location specified, cannot update domain.')
