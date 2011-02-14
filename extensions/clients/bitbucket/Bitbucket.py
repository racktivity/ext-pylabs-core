
from pymonkey import q
from pymonkey import i
from pymonkey.Shell import *
import json

class Bitbucket:    
    """
    @property accounts = account on bitbucket e.g. despieg, value is array of mercurial repo's
    """
    def __init__(self):
        self.accountsLocalRepoNames={}
        self.accountsRemoteRepoNames={}
        self._accountnames=[]
        
        self._initialized=False
        self.codedir=q.system.fs.joinPaths(q.dirs.baseDir,"..","code")
        q.system.fs.createDir(self.codedir)   

    def init(self,force=False):
        if force or not self._initialized:
            self._getAccountNames()
            for account in self._accountnames:
                repos=self._getRepoNamesFromCodeDir(account)
                self.accountsLocalRepoNames[account]=repos
                
                

    def _getAccountNames(self):
        names=q.clients.bitbucket._config.list()
        self._accountnames=names
        return names
        
    def accountAdd(self,account="",login="",passwd=""):
        """
        all params need to be filled in, when 1 not filled in will ask all of them
        """
        if account<>"" and login<>"" and passwd<>"":
            try:
                self._config.remove(account)
            except:
                pass            
            self._config.add(account,{"login":login,"passwd":passwd})
        else:
            self._config.add()
        self._syncBitbucketConfigToMercurialConfig()
        
    def accountsReview(self):
        self._config.review()
        self._syncBitbucketConfigToMercurialConfig()
        
    def accountsShow(self):
        self._config.show()

    def accountsRemove(self,accountName=""):
        self._config.remove(accountName)
        self._syncBitbucketConfigToMercurialConfig()

    def accountGetConfig(self,accountName=""):
        return self._config.getConfig(accountName)
        
    def accountGetLoginInfo(self,accountName=""):
        """
        """
        self.init()
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())      
        config=self.accountGetConfig(accountName)
        login=config["login"]
        passwd=config["passwd"]
        if login=="" or passwd=="":
            self.accountsReview(accountName)
        url=" https://%s:%s@bitbucket.org/%s/" % (login,passwd,accountName)
        return url,login,passwd        
        
##    def _syncBitbucketConfigToMercurialConfig(self):
##        mercurialconnections=q.clients.mercurial.config.list()
##        for mercurialconnection in mercurialconnections:
##            if mercurialconnection.find("bitbucket_")==0:
##                q.clients.mercurial.config.remove(mercurialconnection.replace("bitbucket_",""))
##        for account in self._getAccountNames():
##            login=self.accountGetConfig(account)["login"]
##            passwd=self.accountGetConfig(account)["passwd"]
##            url = "http://bitbucket.org/%s/" % account
##            q.clients.mercurial.config.add("bitbucket_%s"%account,{"url":url,"login":login,"passwd":passwd})
##            #print "bitbucket_%s"%account
##        
    def _getAccountPathLocal(self,accountName):
        return q.system.fs.joinPaths(self.codedir,"bitbucket_%s"%accountName) 

    def getRepoPathLocal(self,accountName="",repoName="",die=True):
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())        
        if repoName=="":
            repoName=q.gui.dialog.askChoice("Select repo",self._getRepoNamesFromCodeDir(accountName))                
            if repoName==None:
                if die:
                    raise RuntimeError("Cannot find repo for accountName %s" % accountName)
                else:
                    return ""
        path=q.system.fs.joinPaths(self._getAccountPathLocal(accountName),repoName)
        q.system.fs.createDir(path)
        return path 

    def _getRepoNamesFromCodeDir(self,accountName=""):
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        path=self._getAccountPathLocal(accountName)
        if q.system.fs.exists(path):
            return q.system.fs.listDirsInDir(path,False,True)
        else:
            return []

    def getRepoPathRemote(self,accountName="",repoName=""):
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        url,login,passwd=self.accountGetLoginInfo(accountName)
        if repoName=="":
            repoName=q.gui.dialog.askChoice("Select repo from bitbucket",self.getRepoNamesFromBitbucket(accountName))
        return "%s%s" % (url,repoName)
    
        

    def _callBitbucketRestAPI(self,accountName, call):
        url,login,passwd=self.accountGetLoginInfo(accountName)
        #http=q.clients.http.getconnection()
        #http.addAuthentication(login,passwd)
        #url="https://api.bitbucket.org/1.0/users/%s/" % self._getBitbucketUsernameFromUrl(url)
        #content=http.get(url)
        #@todo need better way then curl, the authentication doesnt seem to work when using the http pylabs extension
        q.platform.ubuntu.checkInstall("curl","curl")
        tmpfile=q.system.fs.joinPaths(q.dirs.tmpDir,q.base.idgenerator.generateGUID())
        url,login,passwd=self.accountGetLoginInfo(accountName)
        cmd="curl -u %s:%s https://api.bitbucket.org/1.0/%s > %s" % (login, passwd,call,  tmpfile)
        resultcode,  content=q.system.process.execute(cmd, False, True)
        if resultcode>0:
            raise RuntimeError("Cannot get reponames from repo. Cannot execute %s"% cmd)
        content=q.system.fs.fileGetContents(tmpfile )
        q.system.fs.removeFile(tmpfile)
        try:
            object=json.loads(content)
        except:
            raise RuntimeError("Cannot call rest api of bitbicket, call was %s" % cmd)
        return object

    def _getBitbucketRepoInfo(self,accountName):
        if accountName=="":
            raise RuntimeError("Cannot get repo info when account name not specified. Please call this function with accountName")
        call="users/%s/" %  accountName
        return self._callBitbucketRestAPI(accountName, call)
    
    def findRepoFromBitbucket(self,accountName="",partofName=None,reload=False):
        """
        will use bbitbucket api to retrieven all repo information
        @param reload means reload from bitbucket   
        """
        names=self.getRepoNamesFromBitbucket(accountName,partofName,reload)
        if partofName==None:
            q.gui.dialog.message("Select bitbucket repository")
            reposFound2=q.gui.dialog.askChoice("",names)                    
        else:
            reposFound2=[]
            for repo in repoNames:
                if repo.find(partofName)<>-1:
                    reposFound2.append(repo)
        if len(reposFound2)>1:
            raise RuntimeError("Found more than 1 choice, please use better search criteria")
        return reposFound2
    
    def getRepoNamesFromBitbucket(self,accountName="",partOfRepoName="",reload=False):
        """
        will use bbitbucket api to retrieven all repo information
        @param reload means reload from bitbucket   
        """
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        if self.accountsRemoteRepoNames.has_key(accountName) and reload==False:
            return self.accountsRemoteRepoNames[accountName]
        repos=self._getBitbucketRepoInfo(accountName)
        #ipshell()
        repoNames=[str(repo["slug"]) for repo in repos["repositories"]] 
        if partOfRepoName<>"":
            if partOfRepoName.find("*")<>-1:
                partOfRepoName=partOfRepoName.replace("*","").replace("?","").lower()
                repoNames2=[]
                for name in repoNames:
                    name2=name.lower()
                    if name2.find(partOfRepoName)<>-1:
                        repoNames2.append(name)
            else:
                partOfRepoName=partOfRepoName.replace("*","").replace("?","").lower()
                repoNames2=[]
                for name in repoNames:
                    name2=name.lower()
                    if name2==partOfRepoName:
                        repoNames2.append(name)
            
                #print name2 + " " + partOfRepoName + " " + str(name2.find(partOfRepoName))
            repoNames=repoNames2
        
        return repoNames

    def checkoutRepo(self,accountName="",repoName="",branch="",forceUpdate=None):
        """
        @param branch when "" defaults to "default", when None will be asked
        """
        self.init()
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        if repoName=="":
            repoName=q.gui.dialog.askString("Reponame (wildcards are allowed e.g. kds_*)","*")
        #if repoName.find("*")<>-1:
        #    #wildcard
        #    repoName=reponame.replace("*","")
        # else:

        names=self.getRepoNamesFromBitbucket(accountName,repoName)

        if len(names)==1:
            if repoName=="":
                repoName=q.gui.dialog.askString("Reponame found = (press enter if yes or change)",names[0])
            repoName=names[0]
        if len(names)==0:
            repoName=q.gui.dialog.askString("Could not find matching name on repo please specify")
        if len(names)>1:
            repoName=q.gui.dialog.askChoice("select repoName",names,pageSize=300, sortChoices=True)

        if branch==None:
            branch=q.gui.dialog.askString("Branchname","default")      
        if branch=="":
            branch="default"
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge)")  
        
        url,login,passwd=self.accountGetLoginInfo(accountName)
        if url[-1]<>"/":
            url=url+"/"
        return q.clients.mercurial.getclient("/opt/code/%s/%s/" % (accountName,repoName) ,"%s%s" % (url,repoName),branch)
