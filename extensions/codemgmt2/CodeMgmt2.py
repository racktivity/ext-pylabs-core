from pymonkey import *
from pymonkey import q
from pymonkey.Shell import *

class CodeMgmt2():

    def __init__(self):
        self.lastcommitmessage="" 
        self._hgconnections={}
        self.repos=[]
        self._initialized = False

    def findRepo(self,reponame="",branch="default",die=False):
        self.init()
        if reponame=="":
            if len(self._getRepoNames())<20:
                reponame=q.gui.dialog.askChoice("Select Repo",self._getRepoNames())
        partofname=""
        if reponame.find("*")<>-1:
            partofname=reponame.replace("*","")
        if reponame=="" and partofname=="":
            partofname=q.gui.dialog.askString("Give part of repo name")
        if partofname<>"":
                result=[]
                for repo in self._getRepoNames():
                    if repo.find(partofname)<>-1:
                        result.append(repo)
                    if len(result)>20:
                        q.gui.dialog.message("Too many results, please provider more narrow filter for repo name")
                        reponame=self.getRepo(reponame="",branch,die)
                    else:
                        reponame=q.gui.dialog.askChoice("Select Repo",result)
        if branch=="":
            partofname=q.gui.dialog.askString("Give branchname (default=default)","default")
        key="%s___%s" % (reponame,branch)
        if self._hgconnections.has_key(key):
            return self._hgconnections[key]
        else:
            if die:
                raise RuntimeError("could not find repo %s with branch %s" % (reponame,branch))
            return None

    def _getRepos(self):
        self.init()
        return [self._hgconnections[key] for key in self._hgconnections.keys()]

    def _getRepoNames(self):
        self.init()
        return [key for key in self._hgconnections.keys()]        

    def init(self):
        """
        find repo's and load
        """
        if not self._initialized:
            self.connections=q.clients.mercurial.config
            self.connections._review=q.clients.mercurial.config.review
            def configure():
                connections=["aserver","pylabs"]
                urls={"aserver":"http://bitbucket.org/aserver/","pylabs":"http://bitbucket.org/despiegk/"}
                cfg=q.config.getConfig("mercurialconnection")
                for connectionname in connections:
                    if not cfg.has_key(connectionname):
                        q.console.echo("Add connection for %s" % connectionname)
                        q.clients.mercurial.config.add(connectionname,params={"url":urls[connectionname]})
            self.connections.configure=configure
            def review():
                if len(q.clients.mercurial.config.list()) < 4:
                    self.connections.configure()
                return q.clients.mercurial.config._review()
            self.connections.review=review

            sandboxdir=q.system.fs.joinPaths(q.dirs.baseDir,"..","sandboxes")
            q.system.fs.createDir(sandboxdir)

            codedir=q.system.fs.joinPaths(q.dirs.baseDir,"..","code")
            q.system.fs.createDir(codedir)        

            repos=q.system.fs.listDirsInDir(codedir,dirNameOnly=True)
            repos=[repo for repo in repos if repo[0]<>"_"]     
            repos=[repo for repo in repos if repo.count("___")==1]
            for repo in repos:     
                reponame=repo.split("___")[0]
                branchname=repo.split("___")[-1]                
                repo="%s___%s" % (reponame,branchname)                
                repopath=q.system.fs.joinPaths(q.dirs.baseDir,"..","code",repo)
                repokey="%s___%s" % (reponame,branchname)
                if not self._hgconnections.has_key(repokey):                
                    if q.system.fs.exists(q.system.fs.joinPaths(repopath,".hg")):
                        c=q.clients.mercurial.getclient(repopath, "", branchname=branchname)                
                        self._hgconnections[repo]=c
                        self.repos.append(c)
            self._initialized = True


    def _checkoutRepo(self,url="",branch="",login="",passwd="",forceUpdate=False):
        self.init()
        if url=="":
            url=q.gui.dialog.askString("give url of repo e.g. http://bitbucket.org/despiegk/pylabs-core/")
        q.logger.log("Checkout %s on branch %s" % (url,branch),2)
        if branch=="":
            branch=q.gui.dialog.askString("Give branchname","default")
        reponame=url.split("/")[-1] or url.split("/")[-2]
        repohg=self.getRepo(reponame,branch)
        if repohg<>None:
            if forceUpdate:
                repohg.pullupdate(force=True,release=branch)
            else:
                repohg.pullmerge(release=branch)
        else:
            if login=="":
                login=q.gui.dialog.askString("Login")
            if passwd=="" and login<>"guest":
                passwd=q.gui.dialog.askString("Password")
            if url[-1]<>"/":
                url+="/"
            if url.strip().find("http://")<>0:
                raise RuntimeError("Url is not proper format, you entered %s, should be something like\n  http://bitbucket.org/despiegk/pylabs-core/" % (url))
            url=url.replace("http://","")
            url="http://%s:%s@%s" % (login,passwd,url)

            reponame=url.split("/")[-1] or url.split("/")[-2]
            repokey=str(reponame)+"___"+str(branch)
            repopath=q.system.fs.joinPaths(q.dirs.baseDir,"..","code",repokey)

            if not self._hgconnections.has_key(repokey):
                q.logger.log("Will checkout %s to /opt/qbase/code/%s" % (url,repopath))
                #if q.gui.dialog.askYesNo("OK?"):
                c=q.clients.mercurial.getclient(repopath, url, branch)
                self._hgconnections[repokey]=c
                self.repos.append(c)
                #self.repos.__setattr__(repokey,c)  #@todo is not working yet, cannot access it later?                    
                #else:
                #    q.logger.log("DID NOT CHECKOUT %s to /opt/qbase/code/%s because did already exist." % (url,repopath))
            if forceUpdate:
                self._hgconnections[repokey].pullupdate(force=True, release=branch)
            else:
                self._hgconnections[repokey].pullmerge(release=branch)

    def checkoutPylabs(self,forceUpdate=None,branch=""):
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge)")
        self.init()
        if branch=="":
            branch=q.gui.dialog.askString("branch for pylabs","default")
        self.checkoutRepo("pylabs","pylabs-core",branch,forceUpdate=forceUpdate)
        return branch

    def _actionOnRepo(self,repo,action):
        self.init()
        if not self._hgconnections.has_key(repo):
            raise RuntimeError("Cannot find repo %s" % repo)
        hgclient=self._hgconnections[repo]
        if action=="update":
            hgclient.update()
        if action=="pullmerge":
            hgclient.pullmerge()
        if action=="pull":
            hgclient.pull()
        if action=="updatemerge":
            hgclient.updatemerge()            
        if action=="commit":
            hgclient.commit()
        if action=="pullupdate":
            hgclient.status()            
            hgclient.pullupdate()
        if action=="addremove":
            hgclient.addremove()
        if action=="pushcommit":
            hgclient.pull()
            hgclient.updatemerge()
            hgclient.pushcommit()

    def pullUpdateRepos(self):
        """
        update all repos, changes will be lost
        """
        self.init()
        repos=q.gui.dialog.askChoiceMultiple("Select repo's you would like to pull and update",self._getRepoNames(),sortChoices=True,pageSize=40)     
        for repo in repos:
            if not self._hgconnections.has_key(repo):
                raise RuntimeError("Cannot find repo %s" % repo)
            hgclient=self._hgconnections[repo]
            if hgclient.hasModifiedFiles():
                ##print hgclient.status()
                if q.gui.dialog.askYesNo("Are you sure you want to ignore changes made on local repo, update will remove them"):
                    hgclient.pullupdate(force=True)

    def pullMergeRepos(self):
        self.init()
        repos=q.gui.dialog.askChoiceMultiple("Select repo's you would like to pull and merge ",self._getRepoNames(),sortChoices=True,pageSize=40)        
        for repo in repos:
            if not self._hgconnections.has_key(repo):
                raise RuntimeError("Cannot find repo %s" % repo)
            hgclient=self._hgconnections[repo]
            hgclient.pullmerge()

    def pushCommitRepos(self):
        self.init()
        repos=q.gui.dialog.askChoiceMultiple("Select repo's you would like to commit and push",self._getRepoNames(),sortChoices=True,pageSize=40)        
        for repo in repos:
            self._actionOnRepo(repo,"pushcommit")

    def commitRepos(self):
        self.init()
        repos=q.gui.dialog.askChoiceMultiple("Select repo's you would like to commit",self._getRepoNames(),sortChoices=True,pageSize=200)        
        for repo in repos:
            self._actionOnRepo(repo,"addremove")
            self._actionOnRepo(repo,"commit")

    def checkoutPylabsInSandbox(self,remove=None,link=None,local=True,cluster=None,hostnames=[],branch=None,clone=False,forceUpdate=None):
        """
        clone pylabs into /opt/code dir and link or copy to appropriate locations in sandbox
        this will allow you to more easily develop on pylabs
        this works independant of qpackages
        """
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge)")        
        self.init()
        branch=self.checkoutPylabs(branch=branch,forceUpdate=forceUpdate)
        if remove==None:
            remove = q.gui.dialog.askYesNo("\nInstall script will remove pylabs core & extensions before installing, ok?")
        if link==None:
            link = q.gui.dialog.askYesNo("\nDo you want to symlink in stead of copying code from pylabs to qbase. Y/N")
        def link(source, dest,remove,link, ask=False):
            if clone:
                dest=dest.replace("qbase3","qbase3debug_all")
            if local:
                if q.system.fs.isLink(dest):
                    q.system.fs.unlink(dest)
                if not q.system.fs.isLink(dest) and q.system.fs.exists(dest) and q.system.fs.isDir(dest):        
                    if remove:
                        q.system.fs.removeDirTree(dest)
                if q.system.fs.exists(dest):
                    raise RuntimeError("cannot link %s to %s, have to abort configuration, qpackage is not properly installed" % (source, dest))
                if link:
                    q.logger.log( "Link %s to %s" % (source, dest),2)
                    q.system.fs.symlink(source,dest)
                else:
                    q.logger.log("Copy %s to %s" % (source, dest),2)
                    q.system.fs.copyDirTree(source, dest)
            if cluster<>None:
                cluster.symlink(source, dest, hostnames)                


        name="pylabs-core"
        base="%s___%s" % (name,branch)
        codedir = q.system.fs.joinPaths(q.dirs.baseDir, "../", "code")
        link('%s/%s/code/packages/pymonkey/core/' % (codedir,base), '%slib/pymonkey/core/pymonkey' % q.dirs.baseDir,remove,link)
        link('%s/%s/code/utils/' % (codedir,base), '%sutils' % q.dirs.baseDir,remove,link)
        link('%s/%s/code/examples' % (codedir,base), '%sapps/pylabsexamples' % q.dirs.baseDir,remove,link)
        link('%s/%s/code/utils/ssodebug' % (codedir,base), '%sssodebug' % q.dirs.baseDir, remove, link=False, ask=True)
        extensionpath="%s/pylabs-core___%s/code/packages/pymonkey/extensions/"% (codedir,branch)
        extensions=q.system.fs.listDirsInDir(extensionpath, recursive=False, dirNameOnly=True, findDirectorySymlinks=True)
        for extension in extensions:
            link('%s/%s/code/packages/pymonkey/extensions/%s/' % (codedir,base,extension),\
                 '%slib/pymonkey/extensions/%s' % (q.dirs.baseDir,extension),\
                 remove,link)


    def checkoutSSOInCluster(self,domainname="",clusterrootpassword="rooter",hostnames=[],forceUpdate=None):
        """
        same as checkoutSSOInSandbox but make sure specified cluster gets properly configured
        """
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge")
        self.init()
        q.console.askYesNo("THIS IS A DANGEROUS ACTION, ONLY DO THIS IF YOU ARE VERY SURE, WE RECOMMEND YOU DONT DO THIS")
        if len(q.cluster.clusters)==0:
            raise RuntimeError("Please use q.cluster.create... to create a cluster")
        clusters=[cluster.domain for cluster in q.cluster.clusters]
        domainname=q.console.askChoice(clusters,"Select Cluster")
        cluster=q.cluster.get(domainname)
        #@todo check if cluster not empty and raise error if...
        if hostnames==[]:
            hostnames = [n.hostname for n in cluster.selectNodes()]

        if q.console.askYesNo("Init share infrastructure, share & mount all required dirs in cluster e.g. /opt/ & logs (N if already done)"):
            #cluster.shareMyNodeToCluster()   # Share my /opt            
            cluster.createPublicNfsShare(hostnames=hostnames)   # Share the remote /opt's
            cluster.connectMeToNfsShares(hostnames=hostnames)   # Mount remote /opt's to my /mnt/remote
            cluster.connectClusterToMyCode(hostnames=hostnames) # Mount /opt/code to point to me /opt/code

        self.checkoutSSOInSandbox(link=True,remove=True,cluster=cluster,hostnames=hostnames,forceUpdate=forceUpdate)
        self.checkoutPylabsInSandbox(branch="default",link=True, remove=True, cluster=cluster,hostnames=hostnames,local=False,forceUpdate=forceUpdate)

    def checkoutSSOInQbaseDebug(self,forceUpdate=None,clean=True):
        """
        this is the method you should use to checkout the code locally for editing
        it is copied to a parallel qbase called qbase3debug to make sure editing of files is not interfering with local qbase3
        """
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge)")
        if not clean and q.system.fs.exists(q.system.fs.joinPaths(os.sep, 'opt', 'qbase3debug_all')):
            clean=q.gui.dialog.askYesNo("\n!!! qbase3debug_* directories already exists !!!\nWhen switching recipes it is advised to clean this directory\nDo you want to remove the existing qbase3debug_* directories?")
        if clean:
            q.system.fs.removeDirTree(q.system.fs.joinPaths(os.sep, 'opt', 'qbase3debug_master'))
            q.system.fs.removeDirTree(q.system.fs.joinPaths(os.sep, 'opt', 'qbase3debug_all'))
        self.init()
        # the checkout of pylabs should also be in qbase3debug?
        self.checkoutPylabsInSandbox(remove=True,link=True,local=True,branch="default",cluster=None,clone=True,forceUpdate=forceUpdate)
        self.checkoutSSOInSandbox(link=True, remove=True,cluster=None,hostnames=[],clone=True,forceUpdate=forceUpdate)

    def removeLinksInCluster(self,cluster=None,hostnames=[]):
        self.init()
        cl=q.cluster.get()
        items=self.getRecipeDirs()
        for item in items:            
            cl.execute("rm -f %s" % item,cl.listnodes(),dieOnError=False)

    def checkoutSSOInSandbox(self,link=None, remove=None, cluster=None,hostnames=[],clone=None,forceUpdate=None):
        """
        clone SSO into /opt/code dir and link or copy to appropriate locations in sandbox
        this will allow you to more easily develop on pylabs
        this works independant loadRecipeof qpackages
        """
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge)")
        self.init()
        if clone=="":
            clone=q.console.askYesNo("Do you want to checkout to a clone of the sandbox (for development mode), recommend yes")
        q.console.echo("Checkout SSO in sandbox")       
        q.transaction.start("Configure Mercurial Connections")
        self.connections.configure()
        q.transaction.stop("")
        checkedoutrepos=[]
        self.init()
        if remove==None:
            remove = q.gui.dialog.askYesNo("\nInstall script will remove all main SSO repo's before installing, ok?")
        if link==None:
            link = q.gui.dialog.askYesNo("\nDo you want to symlink in stead of copying code from pylabs to qbase. Y/N")

        def link(source, dest, remove, link, nodetype):
            if clone:
                dest=dest.replace("qbase3","qbase3debug_%s"%nodetype)
            q.logger.log("checkoutSSOInSandbox link %s to %s "%(source,dest))
            source = source.replace('//', '/').replace('//', '/').replace('//', '/')
            dest   = dest.replace('//', '/').replace('//', '/').replace('//', '/')
            if dest[-1]=="/":
                dest=dest[:-1]
            if q.system.fs.isLink(dest):
                q.system.fs.unlink(dest)
            if q.system.fs.exists(dest):# and q.system.fs.isDir(dest):
                if remove:
                    q.system.fs.removeDirTree(dest)
            if q.system.fs.exists(dest):
                raise RuntimeError("cannot link %s to %s, have to abort configuration, qpackage is not properly installed" % (source, dest))

            if link:
                q.logger.log( "Link %s to %s" % (source, dest),2)
                q.system.fs.createDir(q.system.fs.getDirName(dest))
                q.system.fs.symlink(source,dest)
                if not q.system.fs.exists(source):
                    raise RuntimeError('source folder ' + source + ' not found!')
                if cluster<>None:
                    cluster.symlink(source, dest, hostnames) #@todo order could be other way around (target, linkname...)
            else:
                q.logger.log("Copy %s to %s" % (source, dest),2)
                q.system.fs.copyDirTree(source, dest)
        lines=self._getRecipeLines()

        # check that we dont have double link targets!
        linktargets = []
        for line in lines:
            if line.strip() == '':
                continue
            if len(line.split(","))==6:
                items=line.split(",")
                items=[item.strip() for item in items]
                [connectionname,reponame,branchname,pathinrepo,pathinqbase,sync2nodes]= items
                if pathinqbase in linktargets:
                    raise RuntimeError('duplicate link target found in ' + q.system.fs.joinPaths( q.dirs.baseDir,"utils","ssodebug","recipes","recipe.txt"))
                linktargets += [pathinqbase]
            else:
                raise RuntimeError("recipe not well structured, line: " + line)

        # perform real linking
        for line in lines:
            if line.strip() == '':
                continue
            if len(line.split(","))==6:
                items=line.split(",")  
                items=[item.strip() for item in items]
                [connectionname,reponame,branchname,pathinrepo,pathinqbase,sync2nodes]= items
            else:
                raise RuntimeError("recipe not well structured, line: " + line)
            key=connectionname + reponame + branchname
            if not (key in checkedoutrepos):
                self.checkoutRepo(connectionname=connectionname, reponame=reponame, branch=branchname,forceUpdate=forceUpdate)
                checkedoutrepos.append(key)
            base="%s___%s" % (reponame,branchname)
            codedir = q.system.fs.joinPaths(q.dirs.baseDir, "../", "code")
            ##print '////////////// pathinqbase: ' + pathinqbase
            link('%s/%s/%s/' % (codedir,base,pathinrepo), '%s/%s' % (q.dirs.baseDir,pathinqbase), remove, link, sync2nodes)

    def _printAll(self, header, list):
        q.console.echo(header + '\n')
        for item in list:
            q.console.echo(str(item))

    def getConnectionDetails(self,connectionname=""):
        """
        """
        self.init()
        if connectionname=="":
            connectionname=q.gui.dialog.askChoice("Connectionname",self.connections.list())
        config=self.connections.getConfig(connectionname)
        url=config["url"]
        if url=="":
            url=q.gui.dialog.askString("url","http://bitbucket.org/despiegk/")
        login=config["login"].strip()
        if login=="":
            login=q.gui.dialog.askString("login","")
        passwd=config["passwd"].strip()
        if passwd=="":
            passwd=q.gui.dialog.askString("passwd","")
        if login.strip()=="" or passwd.strip()=="":
            raise RuntimeError("Login or passwd cannot be empty in mercurial connection config file for %s, see /opt/qbase3/cfg/qconfig/mercurialconnection.cfg" % connectionname)
        #bitbucketsitename=url.replace("://bitbucket.org","").replace("/","").strip().replace("https","").replace("http","")
        return url,login,passwd

    def _getBitbucketUsernameFromUrl(self, url):
        username= url.replace("http://bitbucket.org", "").replace("/","").strip()#@todo need better parsing here, this is very errorprone
        return username

    def _callBitbucketRestAPI(self,connectionname, call):
        url,login,passwd=self.getConnectionDetails(connectionname)
        #http=q.clients.http.getconnection()
        #http.addAuthentication(login,passwd)
        #url="https://api.bitbucket.org/1.0/users/%s/" % self._getBitbucketUsernameFromUrl(url)
        #content=http.get(url)
        #@todo need better way then curl, the authentication doesnt seem to work when using the http pylabs extension
        q.platform.ubuntu.checkInstall("curl","curl")
        tmpfile=q.system.fs.joinPaths(q.dirs.tmpDir,q.base.idgenerator.generateGUID())
        cmd="curl -u %s:%s https://api.bitbucket.org/1.0/%s > %s" % (login, passwd,call,  tmpfile)
        resultcode,  content=q.system.process.execute(cmd, False, True)
        if resultcode>0:
            raise RuntimeError("Cannot get reponames from repo. Cannot execute %s"% cmd)
        content=q.system.fs.fileGetContents(tmpfile )
        q.system.fs.removeFile(tmpfile)
        return json.loads(content)

    def _getBitbucketRepoInfo(self,connectionname=""):
        url,login,passwd=self.getConnectionDetails(connectionname)
        call="users/%s/" %  self._getBitbucketUsernameFromUrl(url)
        return self._callBitbucketRestAPI(connectionname, call)
    
    def getRepoNamesFromBitbucket(self,connectionname="",partofName=None):
        """
        will use bbitbucket api to retrieven all repo information
        """
        repos=self._getBitbucketRepoInfo(connectionname)
        if partofName==None:
            partofName=q.gui.dialog.askString("Give part of reponame on bitbucket")                    
        reposFound=[str(repo["name"]) for repo in repos["repositories"]] 
        reposFound2=[]
        for repo in reposFound:
            if repo.find(partofName)<>-1:
                reposFound2.append(repo)
        return reposFound2

    def checkoutRepo(self,connectionname="",reponame="",branch="",forceUpdate=None):
        self.init()
        if connectionname=="":
            connectionname=q.gui.dialog.askChoice("Connectionname",self.connections.list())
        if reponame=="":
            reponame=q.gui.dialog.askString("Reponame (wildcards are allowed e.g. kds_*)","*")
            if reponame.find("*")<>-1:
                #wildcard
                reponame=reponame.replace("*","")
                names=self.getRepoNamesFromBitbucket(connectionname,reponame)
                if len(names)==1:
                    reponame=q.gui.dialog.askString("Reponame found = (press enter if yes or change)",names[0])
                if len(names)==0:
                    reponame=q.gui.dialog.askString("Could not find matching name on repo please specify")
                if len(names)>1:
                    reponame=q.gui.dialog.askChoice("select reponame",names,pageSize=300, sortChoices=True)
        if branch=="":
            branch=q.gui.dialog.askString("Branchname","default")      
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge)")  
        #@todo need clean errorhandling in case connectionname is not found
        config=self.connections.getConfig(connectionname)
        url=config["url"]+"/"+reponame
        if url.strip()=="":
            raise RuntimeError("Url for repo name cannot be empty, please check configuration of mercurial connections")
        url=url[:10] + url[10:].replace("//","/")
        self._checkoutRepo(url=url,branch=branch,login=config["login"],passwd=config["passwd"],forceUpdate=forceUpdate)    

    def logall(self,fromdaysago=0,fromdate=0,fromkey=""):
        self.init()
        if fromdaysago==0:
            fromdaysago=q.console.askInteger("log from X days ago",0)
        if fromdate==0:
            datestr=q.console.askString("log from date (dd/mm/yyyy)",0)
            if datestr<>"":
                fromdate=q.base.time.humanReadableDatetoEpoch(datestr)
        if fromkey=="":
            fromkey=q.console.askString("log from key","")                            
        result=[]
        for repo in self.repos:
            result.extend(repo.log(fromdaysago,fromdate,fromkey))
        return result

    def exportSandbox(self,name="",ftpupload=None,ftppasswd=""):
        """

        """
        self.init()
        if name=="":
            name=q.console.askString("Provide name of sandbox, will be exported to /opt/sandboxes/",defaultparam="qbase4")
        else:
            q.console.askString("Sandbox will be exported to /opt/sandboxes/%s.tgz"%name)
        if name.find(".tgz")==-1:
            name=name+".tgz"

        sandboxdir=q.system.fs.joinPaths(q.dirs.baseDir,"..","sandboxes")
        q.system.fs.createDir(sandboxdir)        
        tarfile=q.system.fs.joinPaths(sandboxdir,name)

        #q.cloud.cluster._removeRedundantFiles()
        excludes=[".*\.pyc$",".*\.pyo$",".*~$",".*\.bak$",".*qbase3/var/.*",".*qbase3/tmp/.*",".*qbase3/share/.*"]
        excludes.append(".*qbase3/apps/tortoisehg/.*")
        excludes.append(".*/terminfo/.*")
        excludes.append(".*/.hg/.*")
        excludes.append(".*/.cvs/.*")
        excludes.append(".*qbase3/lib/gconv/.*")
        excludes.append(".*qbase3/cfg/qpackage.*")
        extrafiles=[]
        extrafiles.append([q.system.fs.joinPaths(q.dirs.baseDir,"utils","defaults","sources.cfg"),"cfg/qpackages4/sources.cfg"])
        q.system.fs.targzCompress(q.dirs.baseDir,tarfile,False,destInTar="qbase3",pathRegexExcludes=excludes,extrafiles=extrafiles)
        if ftpupload==None:
            if q.console.askYesNo("Do you want to upload the sandbox to the central reposerver?",False):
                passwd=q.console.askString("Password for ftp account on repodev")
                q.cloud.system.fs.copyFile("file:/%s" % tarfile,"ftp://ftpuser:%ss@repodev.aserver.com/pylabs.org/%s" % (passwd,name))

    def rsyncShareQbaseDebug(self, clustername='', modulename='qbase3debug'):
        cluster = q.cluster.get(clustername)
        if not hasattr(q, 'manage') or not hasattr(q.manage, 'rsync'):
            print "Installing rsync_extension qpackage"
            q.qp.updateMetaData()
            p = q.qp.find(name='rsync_extension', domain='qpackages.org', version='3.0')
            if len(p) == 1:
                p[0].install()
            else:
                raise("None or multiple packages found when trying to install rsync_extension, unable to continue")
                
        q.manage.rsync.startChanges()
        if not modulename in q.manage.rsync.cmdb.modules:
            q.manage.rsync.cmdb.addModule(modulename, q.system.fs.joinPaths(os.sep, 'opt'))
            q.manage.rsync.cmdb.modules[modulename].mungeSymlinks = False
            q.manage.rsync.cmdb.modules[modulename].readOnly = True
        if not q.manage.rsync.cmdb.ipaddress in q.system.net.getIpAdresses() or q.manage.rsync.cmdb.ipaddress == '127.0.0.1':
            q.manage.rsync.cmdb.ipaddress = cluster.getMyClusterIp()
        q.manage.rsync.cmdb.save()
        q.manage.rsync.applyConfig()
