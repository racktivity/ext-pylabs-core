
from pylabs import q,i 
from QPackageObject4 import QPackageObject4
from QPackageObject3 import QPackageObject3
from DependencyDef4 import DependencyDef4
from TestRunner import TestRunner

class Convertor:


    #testRunner = TestRunner()

    # Coments
    def installAll(self):
        problems = []
        for p in q.qp.getQPackageTuples():
            package = q.qp.get(*p)
            #if package.name == 'cloud_portal_client':
            #    continue
            #if package.name == 'trac_extension':
            #    continue
            if package.name == 'qpackages4':
                continue
            if package.name.find('python 2.6.2') != -1:
                continue
            if package.name.find('python 2.5') != -1:
                continue
            try:
                package.install()
            except Exception, e:
                q.console.echo( str(p) + '->' + str(e) )
                problems.append((e, p))
        return problems
    
    # Todo check if this is correct!!
    def getLastBuild(self, domain, name, version):
        packagepathV3 = q.system.fs.joinPaths(q.dirs.baseDir, 'var', 'qpackages', domain, name, version)
        builds = q.system.fs.listDirsInDir(q.system.fs.joinPaths(packagepathV3), dirNameOnly=True)
        builds.sort()
        builds.pop()
        buildnr = builds[-1]
        return str(buildnr)
    
    # Returns the unique latest versions of all qpackages3
    def qpackage3FindUnique(self):
        i.qpackages.updateQPackageList()
        toskip=["bootimage","bootserver"]
        packages = q.qp.find()
        checkduplicates = {}
        uniquepackages  = set()
        for package in packages:
            for skipitem in toskip:
                if package.name.find(skipitem) != -1:
                    toprocess=False
            if package.state == 'SERVER':
                continue
            #key = "%s_%s_%s" % (package.domain, package.name, package.version)
            uniquepackages.add((package.domain, package.name, package.version))     
        uniquelatestpackages = []
        for p in uniquepackages:
            lastbuild = self.getLastBuild(domain=p[0], name=p[1], version=p[2])
            try: 
                latest = q.qpackages.qpackageFindFirst(domain=p[0], name=p[1], version=p[2], buildNr=str(lastbuild))
                if latest == None:
                    raise RuntimeError()
                uniquelatestpackages.append(latest)
            except Exception, e:
                q.console.echo( 'problem with ' + str(p) + ' ' + str(e) + ' buildnr ' + lastbuild)
        return uniquelatestpackages

    # gets all qpackages3 that have a qpackage4 with a lower build number
    # or those where the qp4 does not exist
    def getOutOfDateQPackages4(self):
        res = []
        packagesout = self.qpackage3FindUnique()
        for package3 in packagesout:
            # packagedir = "/opt/qbase3/var/qpackages/%s/%s/%s" % (package.domain, package.name, package.version)
            try:
                package4 = q.qp.get(domain=package3.domain, name=package3.name, version=package3.version)
            except:
                res.append((package3.domain, package3.name, package3.version))
                continue
            if package3.buildNr != package4.buildNr:
                res.append((package3.domain, package3.name, package3.version))
        return res
    
    
    # for each qpackage3 it finds this function copies the files to 
    # the qpackage4
    def copyFilesFromQP3(self, qpackages3):
        for qp3 in qpackages3:       
            build = self.getLastBuild(domain = qp3.domain, name = qp3.name, version = qp3.version)     
            fromFilesDir = q.system.fs.joinPaths(q.dirs.packageDir, qp3.domain, qp3.name, qp3.version, build, 'files')
            toFilesDir   = q.system.fs.joinPaths(q.dirs.packageDir + '4', 'files', qp3.domain, qp3.name, qp3.version)
            if q.system.fs.exists(fromFilesDir):
                q.system.fs.copyDirTree(fromFilesDir, toFilesDir)
            else:
                q.console.echo(fromFilesDir + ' does not exist, may be error?')
    
    def __init__(self):
        self.pathPartToChange = '' 
        self.newPathPart= ''

    testRunner = TestRunner()
    
    def _replaceAll_old(self, files, fromStr, toStr, report):
        writtenfiles = []
        for f in files:
            content = q.system.fs.fileGetContents(f)
            f = f.replace(self.pathPartToChange, self.newPathPart)
            #if f.find('install') != -1:
            if content.find(fromStr) == -1:
                if report:
                    q.console.echo( "String wasn't found in: " + f)
            content    = content.replace(fromStr, toStr, 1000000)
            q.system.fs.createDir(q.system.fs.getDirName(f))
            q.system.fs.writeFile(f, content)
            writtenfiles.append(f)
        return writtenfiles
    
    def _replaceAll(self, content, fromStr, toStr, report):
        if content.find(fromStr) == -1:
            if report:
                q.console.echo( "String wasn't found in: " + f)
        content    = content.replace(fromStr, toStr, 1000000)
        return content
    
                    
    def applyRegex(self, content):
        
        fromStr = 'activeQPackage'
        toStr   = 'qpackage'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = 'activeQpackage'
        toStr   = 'qpackage'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = 'activeqpackage'
        toStr   = 'qpackage'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        
        fromStr = 'package.copyFiles()'
        toStr   = 'qpackage.copyFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = 'qqpackage.copyFiles()'
        toStr   = 'qpackage.copyFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = 'qqqpackage.copyFiles()'
        toStr   = 'qpackage.copyFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = 'q.qpackagetools.copyFiles(qpackage)'
        toStr   = 'qpackage.copyFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)
                   
        fromStr = 'qpackage.packageDir, "files"'
        toStr   = 'qpackage.getPathFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = 'qpackage.packageDir,"files"'
        toStr   = 'qpackage.getPathFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = "qpackage.packageDir, 'files'"
        toStr   = 'qpackage.getPathFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = "qpackage.packageDir,'files'"
        toStr   = 'qpackage.getPathFiles()'
        content = self._replaceAll(content, fromStr, toStr, False)

        fromStr = 'qpackage.packageDir,'
        toStr   = 'qpackage.getPathFiles(),'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = 'qpackage.uploadDir, "files"'
        toStr   = 'qpackage.getPathSourceCode()'
        content = self._replaceAll(content, fromStr, toStr, False) 
            
        fromStr = 'qpackage.uploadDir,"files"'
        toStr   = 'qpackage.getPathSourceCode()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = "qpackage.uploadDir, 'files'"
        toStr   = 'qpackage.getPathSourceCode()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        fromStr = "qpackage.uploadDir,'files'"
        toStr   = 'qpackage.getPathSourceCode()'
        content = self._replaceAll(content, fromStr, toStr, False)

        fromStr = "q.qpackagetools.signalConfigurationNeeded(qpackage)"
        toStr   = 'qpackage.signalConfigurationNeeded()'
        content = self._replaceAll(content, fromStr, toStr, False)
        
        return content
        
    def replaceOperatingSystemsDirs(self):
        """
        rename generic to tasklet..
        list   list packages that have more than generic
        """
        files    = q.system.fs.walk('/tmp/new_qpackages/qpackages4/metadata', recurse=True, return_folders=True, return_files=True)
        q.console.echo( str(files))
        for f in files:
            if any([f.find(str(pl)) != -1 for pl in q.platform.ALL]): # if the path contains a platform
                newF = f
                for pl in q.platform.ALL:
                    newF = newF.replace(str(pl), 'tasklets')
                q.console.echo( f + ' -> ' + newF)
                if q.system.fs.isFile(f) and not q.system.fs.exists(newF):
                    # write to new file
                    q.console.echo( f + ' -> ' + newF + ' replacing now..')
                    content = q.system.fs.fileGetContents(f)
                    self.createDir(newF, False)
                    q.system.fs.createEmptyFile(newF)
                    q.system.fs.writeFile(newF, content)
                    # remove the old file
                    q.system.fs.removeFile(f)
                else: 
                    q.console.echo( 'Problem with ' + f)
        for f in files:
            #remove empty directories that contain an operating system
            if any([f.find(str(pl)) != -1 for pl in q.platform.ALL]): # if the path contains a platform
                if q.system.fs.isDir(f) and len(q.system.fs.listDirsInDir(f) + q.system.fs.listFilesInDir(f)) == 0:
                    q.console.echo('removing dir: ' + f) 
                    q.system.fs.removeDir(f)
                    
    def createDir(self, dirStr, CreateDir = True):
        q.console.echo( 'In create dir: ' + dirStr)
        if not q.system.fs.exists(dirStr):
            # create the parent
            self.createDir(q.system.fs.getDirName(dirStr).rstrip('/')) #??
            if CreateDir:
                q.system.fs.createDir(dirStr)
        if not CreateDir and q.system.fs.exists(dirStr) and len(q.system.fs.listDirsInDir(dirStr) + q.system.fs.listFilesInDir(dirStr)) == 0:
            #remove the dir, its a mistake from a previous iteration
            q.system.fs.removeDir(dirStr)
                    
    def buildAllBundles(self):
        # clear the bundles directory
        failed = list()
        files    = q.system.fs.walk('/opt/qbase3/var/qpackages4/bundles', recurse=True, return_folders=True, return_files=False)
        for f in files:
            q.system.fs.removeDirTree(f)
        # create new bundles
        listing = q.qp._getQPackageTuples()
        for l in listing:
            try:
                package = q.qp.get(l[0], l[1], l[2])
                q.console.echo( 'Package created: ' + str(package))
                package._compress()
            except Exception, e:
                failed.append(l)
                raise
        return {'failed': failed}
    
    def uploadAll(self):
        failed = list()
        listing = q.qp._getQPackageTuples()
        for l in listing:
            try:
                package = q.qp.get(*l)
                q.console.echo( 'uploading package: ' + str(package))
                package._upload()
            except Exception, e:
                failed.append(l)
                print e
        return {'failed': failed}
    
    #
    # Coversion QP3 -> QP4
    #
    
    
    def downloadAllPackages(self):
        i.qpackages.updateQPackageList()
        packages = q.qpackages.qpackageFind()
        checkduplicates = {}
        packagesout = []
        for package in packages:
            key = "%s_%s_%s" % (package.domain, package.name, package.version)
            if checkduplicates.has_key(key) == False:
                checkduplicates[key] = 1
                packagesout.append(package)

        while True:
            for package in packagesout:
                packagedir = "/opt/qbase3/var/qpackages/%s/%s/%s" % (package.domain, package.name, package.version)
                print packagedir
                if q.system.fs.exists(packagedir) == False or q.system.fs.exists("%s/ok2" % packagedir) == False:
                    try:
                        package.download(False, downloadAllPlatformFiles = True)
                        q.system.fs.writeFile("%s/ok2" % packagedir,"%s" % q.base.time.getTimeEpoch())
                    except:
                        print "ERROR: COULD NOT DOWNLOAD %s" % package

    def getMetadata(self):
        res=[] #array of array [[domain,name,version]]
        domains=q.system.fs.listDirsInDir(q.dirs.packageDir,dirNameOnly=True)
        for domainName in domains:
            domainpath=q.system.fs.joinPaths(q.dirs.packageDir,domainName)
            packages=q.system.fs.listDirsInDir(domainpath,dirNameOnly=True)
            for packagename in packages:
                packagepath=q.system.fs.joinPaths(domainpath,packagename)
                versions=q.system.fs.listDirsInDir(packagepath,dirNameOnly=True)
                for version in versions:
                    res.append([domainName,packagename,version])
        return res
                        
    def _getPackageDir(self):
        """
        get qpackage for v3 version
        """
        packagedir = q.dirs.packageDir
        return packagedir
    
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

    def migrateToV4(self):
        q.system.fs.createDir(q.dirs.packageDir + "4")
        problematics = []
        unrecognized = []
        for packagItem in self.getMetadata():
            try:
                self.migrateQP3(packagItem, problematics, unrecognized)
            except Exception, e:
                import traceback
                import sys
                traceback.print_exc(file=sys.stdout)
                print 'Failed: ' + str(packagItem)
                problematics.append(packagItem)

        print 'Problematic:'
        for p in problematics:
            print p

        print 'Unrecognized:'
        for p in unrecognized:
            print p

    # Migrates one qp3
    def migrateQP3(self, packagItem, problematics=[], unrecognized=[]):
        #if packagItem[1] != 'cloud_central_db':

        #continue
        self.qpackageMigrateToV4(packagItem[0], packagItem[1], packagItem[2])
        problems = self.copyTasklets(packagItem[0], packagItem[1], packagItem[2], '/opt/overwrite_metadata')
        problematics += problems[0]
        unrecognized += problems[1]

        self.copyScripts(packagItem[0], packagItem[1], packagItem[2], '/opt/overwrite_metadata')
        
        # get files dir

        build = self.getLastBuild(*packagItem)
        fromFilesDir = q.system.fs.joinPaths(q.dirs.packageDir, packagItem[0], packagItem[1], packagItem[2], build, 'files')
        toFilesDir   = q.system.fs.joinPaths(q.dirs.packageDir + '4', 'files', packagItem[0], packagItem[1], packagItem[2])
        if q.system.fs.exists(fromFilesDir):
            q.system.fs.copyDirTree(fromFilesDir, toFilesDir)
        else:
            print fromFilesDir + ' does not exist, may be error?'


    def mirgateOutOfDatePackages(self):

        problematics = []
        unrecognized = []

        for packagItem in self.getOutOfDateQPackages4():
            self.migrateQP3(packagItem, problematics, unrecognized)
            try:
                package = q.qp.get(packagItem[0], packagItem[1], packagItem[2])
                q.console.echo( 'Compressiong Package : ' + str(package))
                package._compress()
                package.upload()
            except Exception, e:
                failed.append(l)
                raise

        print 'Problematic:'
        for p in problematics:
            print p

        print 'Unrecognized:'
        for p in unrecognized:
            print p


            
    def qpackageMigrateToV4(self, domain, name, version):
        package       = self.get(domain,name,version)
        packagepathV3 = q.system.fs.joinPaths(q.dirs.baseDir, 'var', 'qpackages', domain, name, version)
        
        def getDirDest(domain, name, version, typedir):
            path = q.system.fs.joinPaths(self._getPackageDir() + "4", typedir, domain, name, version)
            q.system.fs.createDir(path)
            return path
        #q.console.echo("process package %s" % package)
        
        buildnr = self.getLastBuild(domain=domain, name=name, version=version)
        # remove files if needed    
        if True:
            typedir = "metadata"
            path = q.system.fs.joinPaths(self._getPackageDir() + "4", typedir, domain, name, version)
            q.system.fs.removeDirTree(path)
            typedir = "files"
            path = q.system.fs.joinPaths(self._getPackageDir() + "4", typedir, domain, name, version)
            q.system.fs.removeDirTree(path)            
        #rewrite metadata        
        newPackage = None
        if q.qp.exists(domain, name, version):
            newPackage = q.qp.get(domain, name, version)
        else:
            newPackage = QPackageObject4(domain, name, version, branch="default", new=True)
        newPackage.name = package.name
        newPackage.version=package.version
        newPackage.domain=package.domain
        newPackage.tags=package.tags
        newPackage.supportedPlatforms=package.supportedPlatforms
        for dependency3 in package.dependencies:
            dep4=DependencyDef4()
            dep4.dependencytype=q.enumerators.DependencyType4.getByName(str(dependency3.dependencytype))
            dep4.domain=dependency3.domain
            dep4.maxversion=dependency3.maxversion
            dep4.minversion=dependency3.minversion
            dep4.name=dependency3.name
            dep4.supportedPlatforms=dependency3.supportedPlatforms
            newPackage.dependencies.append(dep4)
        newPackage.description = 'please describe me'
        if package.description != "":
            newPackage.description = package.description
        print 'Buildnr: ' + buildnr
        if int(buildnr) > 0:
            newPackage.buildNr  = int(buildnr)
            newPackage.metaNr   = int(buildnr)
            newPackage.bundleNr = int(buildnr)
            print 'Setting buildnr'
        else:
            raise RuntimeError("Cannot find buildnr for %s" % package)
        newPackage.save()

    def ensureDirPathExists(self, path):
        if path == '/':
            return
        #q.console.echo(path + ' ->getDirName: ' + q.system.fs.getParent(path) + '\n\n')
        #print path + ' ->getDirName: ' + q.system.fs.getParent(path) + '\n\n'
        self.ensureDirPathExists(q.system.fs.getParent(path))
        if not q.system.fs.exists(path):
            q.system.fs.createDir(path)


    def copyScripts(self, domain, name, version, overwriteSourceBasePath):
        buildnr            = self.getLastBuild(domain=domain, name=name, version=version)
        newPackage         = QPackageObject4(domain, name, version, branch="default")
        metaPath           = q.system.fs.joinPaths(newPackage.getPathMetadata(), 'tasklets')
        
        scriptsSourcePath  = q.system.fs.joinPaths(overwriteSourceBasePath, domain, name, version, 'tasklets', 'scripts')
        scriptsTargetPath  = q.system.fs.joinPaths(metaPath, 'scripts')
        print 'EXISTS?: : ' + scriptsSourcePath
        if q.system.fs.exists(scriptsSourcePath):
            print 'COPY SCIPTS TO : ' + scriptsTargetPath
            q.system.fs.copyDirTree(scriptsSourcePath, scriptsTargetPath)
        else:
            pass

    def copyTasklets(self, domain, name, version, overwriteSourceBasePath):
        problematic   = {'install':[], 'configure':[], 'codemanagement':[], 'package':[], 'compile': [], 'startstop':[]}
        package       = self.get(domain,name,version)
        packagepathV3 = q.system.fs.joinPaths(q.dirs.baseDir, 'var', 'qpackages', domain, name, version)
        
        buildnr = self.getLastBuild(domain=domain, name=name, version=version)
        
        packagePath  = q.system.fs.joinPaths(self.qpackageGetpath(domain,name,version), buildnr, 'tasklets')
        
        #print str(q.system.fs.walk(root=packagePath, return_folders=1))
        # if len(q.system.fs.walk(root=packagePath, return_folders=1)) > 1:
            # print 'checkout ' + package.domain + ' ' +  str(package)
        
        taskletPaths = q.system.fs.walk(recurse=True, root=packagePath)
        tasklets     = {'install':None, 'configure':None, 'codemanagement':None, 'package':None, 'compile': None, 'startstop':None }
        #print 'taskletPaths for package: ' + str(package) + ' taskletPaths: ' + str(taskletPaths)
        
        def isIgnorefile(x):
             basename = q.system.fs.getBaseName(x)
             return basename.find('.pyc') != -1 or basename.find('~') != -1 or basename.startswith('.') or basename.find('.qshellc') != -1
        
        def isInstallTasklet(x):
             if isIgnorefile(x):
                 return False
             basename = q.system.fs.getBaseName(x)
             return basename.lower().find('install') != -1
         
        def isPackageTasklet(x):
            if isIgnorefile(x):
                 return False
            basename = q.system.fs.getBaseName(x)
            return basename.lower().find('package') != -1 or basename.lower().find('packaging') != -1
        
        def isCodeManagementTasklet(x):
            if isIgnorefile(x):
                 return False
            basename = q.system.fs.getBaseName(x)
            return basename.lower().find('codemanagement') != -1
        
        def isConfigureTasklet(x):
            if isIgnorefile(x):
                 return False
            basename = q.system.fs.getBaseName(x)
            return basename.lower().find('configure') != -1 or basename.lower().find('configuration') != -1
        
        def isCompileTasklet(x):
            if isIgnorefile(x):
                 return False
            basename = q.system.fs.getBaseName(x)
            return basename.lower().find('compile') != -1 or basename.lower().find('build') != -1

        def isStartStopTasklet(x):
            if isIgnorefile(x):
                 return False
            basename = q.system.fs.getBaseName(x)
            result = basename.lower().find('startstop') != -1 or basename.lower().find('stop') != -1 or basename.lower().find('start') != -1
            return  result or basename.lower().find('restart') != -1 or basename.lower().find('getstatus') != -1

        unclassified=[]
        for t in taskletPaths:
            basename = q.system.fs.getBaseName(t)
            if isIgnorefile(t):
                continue
            if isInstallTasklet(t):
                #print 'Processing ' + t
                if tasklets['install'] == None:
                    tasklets['install'] = t
                else:
                    #print 'Processing duplicate..'
                    problematic['install'].append(tasklets['install'])
                    problematic['install'].append(t)
                    tasklets['install'] = None
                continue
            if isConfigureTasklet(t):
                if tasklets['configure'] == None:
                    tasklets['configure'] = t
                else:
                    problematic['configure'].append(tasklets['configure'])
                    problematic['configure'].append(t)
                    tasklets['configure'] = None
                continue
            if isCodeManagementTasklet(t):
                if tasklets['codemanagement'] == None:
                    tasklets['codemanagement'] = t
                else:
                    problematic['codemanagement'].append(tasklets['codemanagement'])
                    problematic['codemanagement'].append(t)
                    tasklets['codemanagement'] = None
                continue
            if isPackageTasklet(t):
                if  tasklets['package'] == None:
                    tasklets['package'] = t
                else:
                    problematic['package'].append(tasklets['package'])
                    problematic['package'].append(t)
                    tasklets['package'] = None
                continue
            if isCompileTasklet(t):
                if tasklets['compile'] == None:
                    tasklets['compile'] = t
                else:
                    problematic['compile'].append(tasklets['compile'])
                    problematic['compile'].append(t)
                    tasklets['compile'] = None
                continue
            if isStartStopTasklet(t):
                if tasklets['startstop'] == None:
                    tasklets['startstop'] = t
                else:
                    problematic['startstop'].append(tasklets['startstop'])
                    problematic['startstop'].append(t)
                    tasklets['startstop'] = None
                continue
            unclassified.append(t)
            print 'Could not classify ' + t
            
        #if len(q.system.fs.walk(root=packagePath, return_folders=1)) > 1:
            #print 'map: ' + str(tasklets) + ' ' + str(problematic)
            #print 'paths ' + str(taskletPaths) 
            
        #print 'Map: ' + str(tasklets)
        
        def findTasklet(overwriteBasePath, filter):
            files = q.system.fs.walk(root=overwriteBasePath, return_folders=0)
            res = [f for f in files if filter(f)]
            if len(res) > 1:
                raise RuntimeError(overwriteBasePath)
            if not res:
                return 'Does not exists'
            return res[0]
        
        def processFile(source, target):
            content = q.system.fs.fileGetContents(source)
            content = self.applyRegex(content)
            self.ensureDirPathExists(q.system.fs.getDirName(target))
            q.system.fs.writeFile(target, content)
        
        newPackage = QPackageObject4(domain, name, version, branch="default")
        metaPath   = q.system.fs.joinPaths(newPackage.getPathMetadata(), 'tasklets')
        problematic_res=[]
        for type, path in tasklets.items():
            overwriteBasePath = q.system.fs.joinPaths(overwriteSourceBasePath, newPackage.domain, newPackage.name, newPackage.version, 'tasklets')
            if type == 'install':
                targetFile       = q.system.fs.joinPaths(metaPath, 'install.py')
                overwriteSource  = findTasklet(overwriteBasePath, isInstallTasklet)
                qpackages3Source = tasklets['install']
                source           = None
                if q.system.fs.exists(overwriteSource):
                    print 'overwriteSource: ' + overwriteSource
                    #print 'using overwrite source ' + overwriteSource
                    source = overwriteSource
                elif qpackages3Source != None:
                    source = qpackages3Source
                elif problematic['install']:
                    #print overwriteSourceBasePath + '/' + domain + '/' + name + '/' + version + '/tasklets/' + 'install.py'
                    problematic_res.append(str(newPackage))
                    print 'using overwriteSource: ' + overwriteSource + ' in ' + overwriteBasePath
                    print 'Problematic install tasklets found for package ' + str(newPackage) + ': ' + str(problematic['install']) + '\n'
                if source:
                     processFile(source, targetFile)
            if type == 'configure':
                targetFile       = q.system.fs.joinPaths(metaPath, 'configure.py')
                overwriteSource  = findTasklet(overwriteBasePath, isConfigureTasklet)
                qpackages3Source = tasklets['configure']
                source           = None
                if q.system.fs.exists(overwriteSource):
                    print 'overwriteSource: ' + overwriteSource
                    source = overwriteSource
                elif qpackages3Source != None:
                    source = qpackages3Source
                elif problematic['configure']:
                    problematic_res.append(str(newPackage))
                    #print overwriteSourceBasePath + '/' + domain + '/' + name + '/' + version + '/tasklets/' + 'configure.py'
                    print 'Problematic configure tasklets found for package ' + str(newPackage) + ': ' + str(problematic['configure']) + '\n'
                if source:
                     processFile(source, targetFile)
            if type == 'package':
                targetFile       = q.system.fs.joinPaths(metaPath, 'package.py')
                overwriteSource  = findTasklet(overwriteBasePath, isPackageTasklet)
                qpackages3Source = tasklets['package']
                source           = None
                if q.system.fs.exists(overwriteSource):
                    print 'overwriteSource: ' + overwriteSource
                    source = overwriteSource
                elif qpackages3Source != None:
                    source = qpackages3Source
                elif problematic['package']:
                    problematic_res.append(str(newPackage))
                    #print overwriteSourceBasePath + '/' + domain + '/' + name + '/' + version + '/tasklets/' + 'package.py'
                    print 'Problematic package tasklets found for package ' + str(newPackage) + ': ' + str(problematic['package']) + '\n'
                if source:
                     processFile(source, targetFile)
            if type == 'codemanagement':
                targetFile       = q.system.fs.joinPaths(metaPath, 'codemanagement.py')
                overwriteSource  = findTasklet(overwriteBasePath, isCodeManagementTasklet)
                qpackages3Source = tasklets['codemanagement']
                source           = None
                if q.system.fs.exists(overwriteSource):
                    print 'overwriteSource: ' + overwriteSource
                    source = overwriteSource
                elif qpackages3Source != None:
                    source = qpackages3Source
                elif problematic['codemanagement']:
                    problematic_res.append(str(newPackage))
                    #print overwriteSourceBasePath + '/' + domain + '/' + name + '/' + version + '/tasklets/' + 'codemanagement.py' 
                    print 'Problematic codemanagement tasklets found for package ' + str(newPackage) + ': ' + str(problematic['codemanagement']) + '\n'
                if source:
                     processFile(source, targetFile)
            if type == 'compile':
                targetFile       = q.system.fs.joinPaths(metaPath, 'compile.py')
                overwriteSource  = findTasklet(overwriteBasePath, isCompileTasklet)
                qpackages3Source = tasklets['compile']
                source           = None
                if q.system.fs.exists(overwriteSource):
                    print 'overwriteSource: ' + overwriteSource
                    source = overwriteSource
                elif qpackages3Source != None:
                    source = qpackages3Source
                elif problematic['compile']:
                    problematic_res.append(str(newPackage))
                    print 'Problematic compile tasklets found for package ' + str(newPackage) + ': ' + str(problematic['compile']) + '\n'
                    #print overwriteSourceBasePath + '/' + domain + '/' + name + '/' + version + '/tasklets/' + 'compile.py' 
                if source:
                     processFile(source, targetFile)
            if type == 'startstop':
                targetFile       = q.system.fs.joinPaths(metaPath, 'startstop.py')
                overwriteSource  = findTasklet(overwriteBasePath, isStartStopTasklet)
                qpackages3Source = tasklets['startstop']
                source           = None
                if q.system.fs.exists(overwriteSource):
                    print 'overwriteSource: ' + overwriteSource
                    source = overwriteSource
                elif qpackages3Source != None:
                    source = qpackages3Source
                elif problematic['startstop']:
                    problematic_res.append(str(newPackage))
                    print 'Problematic startstop tasklets found for package ' + str(newPackage) + ': ' + str(problematic['startstop']) + '\n'
                    #print overwriteSourceBasePath + '/' + domain + '/' + name + '/' + version + '/tasklets/' + 'compile.py'
                if source:
                     processFile(source, targetFile)

        return (problematic_res, unclassified)

        
    # reports packages that fail to download
    # Todo
    #def verifyPackagesDownLoad(self):
        #failed_to_get         = list()
        #failed_to_download    = list()
        #failed_to_install     = list()
        #succeeded_to_install  = list()
        #for package in self.packageslist:
            #try:
                #pq = self.get(*package)
            #except:
                #q.console.echo('failed to get : ' + str(package))
                #failed_to_get.append(package)
                #continue
            #try:
                #pq.download()
            #except:
                #q.console.echo('failed to download : ' + str(package))
                #failed_to_download.append(package)
                #continue
            #try:
                #pq.install()
            #except:
                #q.console.echo('failed to install : ' + str(package))
                #failed_to_install.append(package)
                #continue
            #q.console.echo('succeeded to install : ' + str(package))
            #succeeded_to_install.append(package)
        #return {'failed_to_get':failed_to_get, 'failed_to_download': failed_to_download, 
                #'failed_to_install':failed_to_install, 'succeeded_to_install':succeeded_to_install}
    
    ## reports packages that fail to download
    #def verifyPackagesDownLoad(self):
        #failed_to_get         = list()
        #failed_to_download    = list()
        #failed_to_install     = list()
        #succeeded_to_install  = list()
        #for package in self.packageslist:
            #try:
                #pq = self.get(*package)
            #except:
                #q.console.echo('failed to get : ' + str(package))
                #failed_to_get.append(package)
                #continue
            #try:
                #pq.download()
            #except:
                #q.console.echo('failed to download : ' + str(package))
                #failed_to_download.append(package)
                #continue
            #try:
                #pq.install()
            #except:
                #q.console.echo('failed to install : ' + str(package))
                #failed_to_install.append(package)
                #continue
            #q.console.echo('succeeded to install : ' + str(package))
            #succeeded_to_install.append(package)
        #return {'failed_to_get':failed_to_get, 'failed_to_download': failed_to_download, 
                #'failed_to_install':failed_to_install, 'succeeded_to_install':succeeded_to_install}
        
        
            
            
            
        