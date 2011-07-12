'''Utility methods to work with hg repositories'''

from pylabs import q
from mercurial import hg, ui, commands

class NewUI(ui.ui):
    def write(self, *args, **opts):
         if self._buffers:
            self._buffers[-1].extend([str(a) for a in args])

        
class HgClient4:    
    
    def __init__(self,hgbasedir,remoteUrl="",branchname=None, username=None, cleandir=None):
        """
        @param base dir where local hgrepository will be stored
        @param remote url of hg repository, can be empty if local repo is created
        @param cleandir: If True, files in that directory will be deleted before doing clone (if it wasn't an mercurial) if set to False,
                         an exception will be raised if directory has files, if None, the user will be asked interactively.
        """
        self.remoteUrl=remoteUrl.strip()
        self.basedir=hgbasedir
        self.branchname=branchname
        self.reponame=""
        self.repokey=""
        self.username=username
        self._ui = NewUI()
        self._log("Init hgclient: basedir:%s remoteurl:%s branchname:%s" %(hgbasedir,remoteUrl,branchname))
        
        if (not isinstance(hgbasedir, basestring) or not isinstance(remoteUrl, basestring))\
         or (branchname and not isinstance(branchname, basestring)):
            raise ValueError("Input to hgclient need to be all strings")

        if q.system.fs.exists(self.basedir) and not q.system.fs.exists(q.system.fs.joinPaths(self.basedir,".hg")):
            if not self.remoteUrl:
                raise RuntimeError(".hg not found and remote url is not supplied")
            if len(q.system.fs.listFilesInDir(self.basedir,recursive=True))==0:
                self._clone()
            else:
                #did not find the mercurial dir
                if q.qshellconfig.interactive:
                    if cleandir == None:
                        cleandir = q.gui.dialog.askYesNo("\nDid find a directory but there was no mercurial metadata inside.\n\tdir: %s\n\turl:%s\n\tIs it ok to remove all files from the target destination before cloning the repository?"\
                                                       % (self.basedir,self.remoteUrl))
                        
                if cleandir:
                    q.system.fs.removeDirTree(self.basedir)
                    q.system.fs.createDir(self.basedir)
                    self._clone()
                else:
                    self._raise("Could not clone %s to %s, target dir was not empty" % (self.basedir,self.remoteUrl))
                    
        if not q.system.fs.exists(self.basedir):
            if not self.remoteUrl:
                raise RuntimeError(".hg not found and remote url is not supplied")            
            q.system.fs.createDir(self.basedir)
            self._clone()
                
        if q.system.fs.exists(self.basedir) and q.system.fs.exists(q.system.fs.joinPaths(self.basedir,".hg")):
            self._repo = hg.repository(self._ui, self.basedir)

    def _getRepoInfo(self):
        """
        get info from dir e.g. from pylabs-core___default
        """
        dirname=q.system.fs.getBaseName(self.basedir)
        if dirname.count("___")==1:
            #keyname can be filled in

            reponame,branchname=dirname.split("___")
            if branchname<>self.branchname:
                self._raise("branchname part of repodir is not the same as the parameter with which this class has been called: %s<>%s" % (branchname,self.branchname))
            self.reponame=reponame
            self.repokey=dirname.strip()
            self._log("Local mercurial repo has branchname in name of directory, repokey:%s" % self.repokey,7)
        else:
            self.repokey="%s___%s" % (dirname,self.branchname)
            self._log("Local mercurial repo does not have branchname in name of directory, repokey: %s" % self.repokey,7)
            
                
    ##def checkConnection(self):
        ##return
        ### try to ping the remote machine
        ##o      = urlparse(self.remoteUrl)
        ###@todo check if ip address or hostname
        ##ipAdrr = q.system.net.getHostByName(o.hostname)
        ##if not q.system.net.pingMachine(ipAdrr,pingtimeout=10):
            ##raise RuntimeError("Cannot reach mercurial server on %s.\nPlease check your network connection." % o.netloc)

    def checkConnection(self): #??
        # check the remoteUrl for the correct credentials
        # request the reader status code through wget?
        # @type o urlparse.ParseResult
        ##o   = urlparse(self.remoteUrl)
        ##con = httplib.HTTPConnection(o.netloc)
        ##con.request("head", o.path)
        ##res = con.getresponse()
        ##if res.status==401 or res.status==403:
        ##    raise RuntimeError('Authentication failed for url %s. Please change check your credentials' % (self.remoteUrl))
        
        #@TODO implement
        ##install httpclient_extension
        #conn = q.clients.http.getconnection()
        #conn.addAuthentication('username','password')
        #conn.get('http://bitbucket.org/aserver/drpdb/src/tip/model/tasklets/cloud/view_add_cloud_list.py')
        pass
    
    def verify(self):
        cmd="verify"
        exitCode, output = self._hgCmdExecutor(cmd,autoCheckFix=False)
        if exitCode>0:
            self._raise("invalid repo, output verify: <<<<<<<<<<<<<<<<<<<<\n" + output + "\n>>>>>>>>>>>>>>>>>>")

    def verifyfix(self):
        """
        verify repo and try to fix
        @return True if fixed
        """
        self._log("mercurial verify %s" % (self.basedir),2)
        cmd="verify"
        exitCode, output = self._hgCmdExecutor(cmd,autoCheckFix=False)
        if exitCode>0:
            msg="Mercurial directory on %s is corrupt./n%s" % (self.basedir,output)
            if q.qshellconfig.interactive:
                q.console.echo(msg)
                if q.gui.dialog.askYesNo("/nDo you want to repair the situation by removing the corrupt directory and clone again?"):
                    q.system.fs.removeDirTree(self.basedir)
                    self.__init__(self.basedir,self.remoteUrl)                  
                    return True
            else:
                self._raise("Mercurial directory on %s is corrupt./n%s" % (self.basedir,output))
        self.checkConnection()
        self._log("Verified repo on %s, no issues found" % self.basedir)
        return False

    
    def _log(self, message, level=5):
        message="hglclient, repo:%s \n%s" % (self.reponame,message) 
        q.logger.log(message, level)

    def _raise(self, message):        
        message="ERROR hgclient: %s\nPlease fix the merurial local repo manually and restart failed mercurial action.\nRepo is %s" % (message, self.basedir)
        raise RuntimeError(message)

    def _hgCmdExecutor(self,cmd, *args, **kwargs):

        recursivedepth = kwargs.pop('recursivedepth', 0)
        autoCheckFix = kwargs.pop('autoCheckFix', True)
        die = kwargs.pop('die', True)
        output = ''
        exitCode = ''
        error = 0
        self._ui.pushbuffer()
        
        try:
            command = getattr(commands, cmd)
            if cmd == 'clone':
                exitCode = command(self._ui, *args, **kwargs)
            else:
                exitCode = command(self._ui, self._repo, *args, **kwargs)
            output = self._ui.popbuffer()
            if exitCode is False:
                exitCode = 0
            if exitCode is True:
                exitCode = 1
        except Exception , e:
            output = str(e)
            error = 1

        self._log("executing command: '" + cmd + "' in dir " + self.basedir)
        if output.find("authorization failed") <> -1:
            raise RuntimeError("ERROR: hgclient %s\nAuthorization failed cannot execute mercurial command: %s" % (self.reponame,cmd))
        if output.find("unknown revision 'default'")<>-1 and die==False:
            return 999,output
        if output.find("abort") <> -1 and exitCode == 0:
            raise RuntimeError("ERROR: hgclient %s\nInvalid exitcode on cmd %s!" % (self.reponame,cmd))
        if exitCode > 0 or error:
            msg="ERROR: hgclient %s\nCould not execute hg cmd: \n%s\nOutput:\n%s" % (self.reponame,cmd,output)
            if die:
                raise RuntimeError(msg)
            else:
                self._log(msg,4)                
        if exitCode > 0 and autoCheckFix:            
            result=False
            if recursivedepth==0:
                #unknown error
                result=self.verifyfix()
                #repo has been verified and possibly fixed
                if result:
                    #repo has been fixed
                    self._log("Repo %s has been fixed, will try to execute relevant hg command again" % self.basedir)
                    exitCode,output = self._hgCmdExecutor(cmd, *args, **kwargs)
            if not result:
                self._raise("Could not execute mercurial command: %s.\nOutput: %s\n%s" % (cmd,exitCode,output))
        return exitCode,output
    
    def pull(self):
        # Do a clone if no repo found
        self._log("pull %s" % (self.basedir))
        self.checkConnection()
        self._log("pull %s to %s" % (self.remoteUrl,self.basedir))
        cmd="pull"
        url = self.getUrl()
        self._hgCmdExecutor(cmd, source=url)

    def isTrackingFile(self, file):
        self._log("isTrackingFile of %s" % (self.basedir))
        cmd = 'status'
        exitCode, output = self._hgCmdExecutor(cmd, file)
        return output==''

    def getModifiedFiles(self):
        """
        return array with changed files in repo
        @return {"added":added,"missing":missing,"modified":modified,"ignored":ignored,"removed":removed,"nottracked":nottracked} is dict
        remarks
        - missing means, file referenced in mercurial local repo but no longer on filesystem (! in hg status) 
        - notracked mans, file is on filesystem but not in repo (?)
        - removed means, mercurial repo knows file has been removed from filesystem (R)
        - ignored, means hg has been instructed to ignore that file (I)
        
        
        """
        self._log("getChangedFiles of %s" % (self.basedir))
        
        # first remove backup files as these confuse the system
        # If the system contains backup files raise an exception
        files  = q.system.fs.listFilesInDir(self.basedir, recursive=True)
        for file in files:
            if file[-1] == '~': # if backupfile
                q.system.fs.removeFile(file)
                cmd = 'remove'
                self._hgCmdExecutor(cmd, file)
                cmd = 'commit'
                message = "removed backup file '%s' " % (file)
                self._hgCmdExecutor(cmd, message=message, user=self.username)

        self._removeRedundantFiles()
        output = self.status()
        lines=output.split("\n")
        modified=[]
        added=[]
        ignored=[]
        removed=[]
        missing=[]
        nottracked=[]
        for line in lines:
            if line.strip()<>"":
                code=line[0]
                path=line[2:]
                if code=="!":
                    missing.append(path)
                elif code=="I":
                    ignored.append(path)
                elif code=="?":
                    nottracked.append(path)
                elif code.lower()=="m":
                    modified.append(path)
                elif code.lower()=="a":
                    added.append(path)
                elif code.lower()=="r":
                    removed.append(path)      
        return {"added":added,"missing":missing,"modified":modified,"ignored":ignored,"removed":removed,"nottracked":nottracked}
    
    def hasModifiedFiles(self):
        r=self.getModifiedFiles()
        if len(r["added"])>0 or len(r["removed"])>0 or len(r["modified"])>0 or len(r["ignored"])>0 or len(r["missing"])>0 or len(r["nottracked"])>0:
            return True
        else:
            return False            
            
    def updatemerge(self,commitMessage="",ignorechanges=False,addRemoveUntrackedFiles=False,trymerge=True, release=0):
        self._log("updatemerge %s" % (self.basedir))
        if ignorechanges and trymerge:
            self._raise("Cannot ignore changes and try to do a merge at the same time")
        if ignorechanges and addRemoveUntrackedFiles:
            self._raise("Cannot ignore changes and try to add remove untracked files at same time")
            
        result=self.getModifiedFiles()

        # means files are in repo but no longer on filesystem
        if len(result["ignored"])>0 or len(result["nottracked"]) or len(result["missing"])>0:
            #there are files not added yet
            if q.qshellconfig.interactive:
                q.console.echo("\n\nFound files not added yet to repo or deleted from filesystem")

                if len(result["missing"])>0:
                    q.console.echo("\n".join(["Missing: %s" % item for item in result["missing"]]))
                    if not q.gui.dialog.askYesNo("Above files are in repo but no longer on filesystem, is it ok to delete these files from repo?"):
                        self._raise("Cannot update repo because files are deleted on filesystem which should not have.")
                    else:
                        for path in result["missing"]:
                            self.remove(path)
                            
                if len(result["nottracked"])>0 or len(result["ignored"])>0:
                    q.console.echo("\n".join(["Nottracked/Ignored: %s" % item for item in result["nottracked"] + result["ignored"]]))
                    q.console.echo("\n\Above files are not added yet to repo but on filesystem")
                    action = q.gui.dialog.askChoice("What do you want to do with these files" , ["RemoveTheseFiles", "AddRemove", "Abort"])
                    if action == "RemoveTheseFiles":
                        for path in result["nottracked"] + result["ignored"]:
                            if q.system.fs.exists(q.system.fs.joinPaths(self.basedir,path)):
                                if q.system.fs.isDir(q.system.fs.joinPaths(self.basedir,path)):
                                    q.system.fs.removeDir(q.system.fs.joinPaths(self.basedir,path))
                                else:
                                    q.system.fs.removeFile(q.system.fs.joinPaths(self.basedir,path))
                    elif action == "AddRemove":
                        self.addremove(message="",commit=False)
                    elif action == "Abort":
                        self._raise("Cannot update repo because there are files which are not added or removed yet to local repo." )                    
                
            else:
                if len(result["missing"])>0 and ignorechanges==False:
                    self._raise("Cannot update repo because files are deleted on filesystem which should not be.")
                if len(result["nottracked"])>0 and addRemoveUntrackedFiles==False:
                    self._raise("Cannot update repo because there are files which are not added or removed yet to local repo.")
                if ignorechanges:
                    #remove the files
                    for path in result["nottracked"]:
                        q.system.fs.removeFile(q.system.fs.joinPaths(self.basedir,path)) 
                self.addremove(message="add remove untracked files for %s" % commitMessage,commit=False)
            
        result=self.getModifiedFiles()   
        if len(result["added"])>0 or len(result["removed"])>0 or len(result["modified"])>0:
            if q.qshellconfig.interactive:
                q.console.echo("\nFound modified, added, deleted files not committed yet")
                #if q.gui.dialog.askYesNo("\nDo you want to view these files?"):
                q.console.echo("\n".join(["Added:    %s" % item for item in result["added"]]))
                q.console.echo("\n".join(["Removed:  %s" % item for item in result["removed"]]))
                q.console.echo("\n".join(["Modified: %s" % item for item in result["modified"]]))                    
                if q.gui.dialog.askYesNo("\nDo you want to commit the files?"):
                    commitMessage=self.commit(commitMessage)
                    result=self.update(release,die=False)
                    if result>0:
                        q.console.echo("cannot update will try a merge")
                        result=self.merge(commitMessage=commitMessage)
                        if result ==1 or result ==2:
                            q.console.log("There was nothing to merge")
                        result=self.update(release)
                    
                elif q.gui.dialog.askYesNo("\nDo you want to ignore the changed files? The changes will be lost"):
                    self.update(release,force=True)
                else:
                    self._raise("Cannot update repo because uncommitted files in %s" % self.basedir)
            else:
                if trymerge:
                    self.commit(commitMessage)
                    self.merge(commitMessage=commitMessage)
                    self.update(release)
                elif ignorechanges:
                    self.update(release)
                else:
                    self._raise("Cannot update repo because uncommitted files in %s" % self.basedir)
        else:
            # nothing changed in the local repo, just update
            self.update(release)
        self.checkbranch()

    # If there are local changes in the repo should we crash?
    def update(self,release=0,force=False,die=True, strict=False):
        clean = False
        check = False
        if release==0 and self.branchname:
            release=self.branchname
        self._log("update %s to release: %s" % (self.basedir,release))
        if force:
            clean = True
        elif strict:
            check = True
        else:
            force=""   # allow automatic merge to occur..       see hg help update
        cmd = 'update'
        if release:
			result,output=self._hgCmdExecutor(cmd, die=False, check=check, clean=clean, rev=release)
        else:
			result,output=self._hgCmdExecutor(cmd, die=False, check=check, clean=clean)
        
        if result==999:
            #means default does not exist
            cmd="update"
            result,output=self._hgCmdExecutor(cmd, die=False, check=check, clean=clean)
        output.replace("***ERROR***\n","")
        if output.find("abort")<>-1 or result>0:
            if die:
                self._raise("Cannot update, %s" % output)
            else:
                return 2
        return result
         
    def remove(self,path):
        """
        remove file with path from local repo
        """
        self._log("remove file from local repo with path %s" % path,8)
        cmd="remove"
        self._hgCmdExecutor(cmd, path)

    def merge(self,commitMessage="",commit=True,silent=False):
        self._log("merge '%s'" % (self.basedir))
        self.checkbranch()
        self._removeRedundantFiles()
        if self.hasModifiedFiles():
            self._raise("Cannot merge %s because there are untracked files." % self.basedir)
        cmd="merge"
        returncode,out=self._hgCmdExecutor(cmd,autoCheckFix=False,die=False)
        skip=False
        if out.find("there is nothing to merge")<>-1 or out.find("has one head")<>-1 :
            self._log("Nothing to merge",5)
            skip =True
            return 1
        if out.find("conflicts during merge")<>-1:
            self._raise("conflicts in merge")
        
        if returncode>0 and silent==False and skip==False:
            self._raise("cannot merge, cmd was hg merge in dir %s" % self.basedir)            
        #when log says:
        ##log: abort: branch 'xxx' has one head - please merge with an explicit rev there is nothing to do
        if commit and skip==False:
            self.commit(commitMessage, force=True)
        return 0
                    
    def switchbranch(self,branchname):
        self._log("switchbranch %s" % (self.basedir))
        if branchname<>self.getbranchname():
            self.updatemerge(commitMessage="switch branch",ignorechanges=False,addRemoveUntrackedFiles=False,trymerge=True, release=branchname)
        
    def pullupdate(self,force=False, release=0, commitMessage=""):
        self._log("pullupdate %s" % (self.basedir))
        self.pull()    
        self.update(force=force)

    def pullmerge(self,commitMessage="",release=0):
        self._log("pullmerge %s" % (self.basedir))
        self.pull()    
        self.updatemerge(commitMessage=commitMessage,ignorechanges=False,trymerge=True, release=release)

    def _clone(self):
        self._log("clone %s" % (self.basedir))
        
        self.checkConnection()
        self._log("clone %s to %s" % (self.remoteUrl,self.basedir))
        cmd="clone"
        options = dict()
        if self.branchname:
            options['rev'] = [self.branchname]
        exitCode,output=self._hgCmdExecutor(cmd, source=self.remoteUrl, dest=self.basedir ,autoCheckFix=False, die=False, **options)
        if exitCode==999:
            #could not find default try to checkout using no revision
            cmd="clone"
            exitCode,output=self._hgCmdExecutor(cmd, source=self.remoteUrl, dest=self.basedir, autoCheckFix=False)
        if exitCode>0:
            raise RuntimeError("Could not clone %s, error message %s" % (self.remoteUrl,output))
            
        self._repo = hg.repository(self._ui, self.basedir)
        self.verify()

    def getbranchname(self):
        cmd="branch" 
        returncode,output=self._hgCmdExecutor(cmd)
        return output.strip()

    def checkbranch(self):
        """
        check if branch of client is consistent with branch found on local repo
        will raise error if not ok
        """
        if self.branchname:
			if self.getbranchname() != self.branchname:
				self._raise("Branchnames conflict for repo, qshell mercurial client has branchname: %s and branchname on filesystem: %s" % (self.branchname,self.getbranchname()))
    
    def getbranches(self):
        cmd="branches"
        returncode , output=self._hgCmdExecutor(cmd)
        return [l.split()[0] for l in output.splitlines()]
        
    def status(self):
        cmd="status"
        returncode,output=self._hgCmdExecutor(cmd)
        return output
    
    def id(self):
        cmd="identify"
        returncode , output=self._hgCmdExecutor(cmd, id='-i')
        return output[:-1]
        
    identify = id

    def commit(self, message="", force=False, username=None):
        """
        does not work interactive
        """
        self._log("commit %s" % (self.basedir))
        self.checkbranch()   
        if self.status().strip()=="" and not force:
            self._log("Nothing to commit, e.g. after a merge which had nothing to do.",5)
            return 
        if q.qshellconfig.interactive:
            if message=="":
                message=q.gui.dialog.askString("give commit message:")
                
        else:
            if message=="":
                self._raise("cannot commit because commit message is empty")
        self._log("commit %s" % (self.basedir))
        cmd="commit"

        if not username:
            username = self.username
        self._hgCmdExecutor(cmd, message=message, user=username)
        return message

    def addremove(self,message="",commit=True):
        """
        does not work interactive, to work interactive use self.updateMerge() which will have same effect
        """
        self._log("addremove '%s'" % (self.basedir))
        self.checkbranch()   
        if self.status().strip()=="":
            self._log("Nothing to addremove",2)
            return 
        self._removeRedundantFiles()
        cmd="addremove"
        self._hgCmdExecutor(cmd)
        if commit:
            self.commit(message)        
        
    def push(self):
        self.checkbranch()
        self._log("push %s to %s" % (self.basedir, self.remoteUrl))
        self.checkConnection()
        cmd="push"
        url = self.getUrl()
        self._hgCmdExecutor(cmd, dest=url)
        
    def pushcommit(self,commitMessage="",ignorechanges=False,addRemoveUntrackedFiles=False,trymerge=True, release=0):
        """
        alias of  commitpush
        """
        self.commitpush(commitMessage,ignorechanges,addRemoveUntrackedFiles,trymerge, release)
        
    def commitpush(self,commitMessage="",ignorechanges=False,addRemoveUntrackedFiles=False,trymerge=True, release=0):
        """
        reponame is name under which we are going checkout in dir targetdir, if not specified same as name repository
        """
        self._log("commitpush %s" % (self.basedir))
        self.pull()
        self.updatemerge(commitMessage,ignorechanges,addRemoveUntrackedFiles,trymerge, release)
        self.push()        

    def _removeRedundantFiles(self):
        self._log("removeredundantfiles %s" % (self.basedir))
        dirs2delete=[]
        def process(args, path):
            if path[-4:].lower()==".pyc" or path[-4:].lower()==".pyo" or path[-4:].lower()==".pyw" or path[-1]=="~":
                q.system.fs.removeFile(path)
            if path.find("/.cache")<>-1 and path.find("/.hg/")==-1:
                dirs2delete.append(path)
        q.system.fswalker.walk(self.basedir,process,"",True,True) 
        for cachedir in dirs2delete:
            q.system.fs.removeDirTree(cachedir)

    def export(self, destination, source=None, branch=''):

        ''' Svn Export like mercurial top level directory copy

        This function exports a source repository to a destination

        @param destination: Export Destination
        @type add_source_path: string
        @param source : The source that is to be exported
        @type source: string
        @param branch_name: Branch name under remote_name
        @type branch_name : string

        '''

        destination= q.system.fs.joinPaths(q.dirs.baseDir, destination)
        archive = q.system.fs.joinPaths(q.dirs.tmpDir, 'hg', 'archive')
        if q.system.fs.exists(archive): q.system.fs.removeDirTree(archive)

        ###pull lastest changes first
        self.pull()
            
        cmd = 'archive'
        options = dict()
        options['rev'] = branch or self.getbranchname()
        exitCode, output = self._hgCmdExecutor(cmd, dest=archive, prefix='', **options)


        if source and not q.system.fs.exists(q.system.fs.joinPaths(archive, source)):
          raise IOError('%s does not exist '%q.system.fs.joinPaths(archive, source))
        if source:
            source=q.system.fs.joinPaths(archive,source)
        else:
            source = archive

        q.system.fs.copyDirTree(source, destination)
        archivalFile = q.system.fs.joinPaths(destination, '.hg_archival.txt')
        if q.system.fs.exists(archivalFile):
          q.system.fs.removeFile(archivalFile)

        q.system.fs.removeDirTree(archive)

    def getUrl(self):
        if self.remoteUrl:
            return self.remoteUrl
        else:
            if not q.system.fs.exists(q.system.fs.joinPaths(self._repo.path,"hgrc")):
                raise RuntimeError("ERROR: Cant retrieve remote url. hgrc file doesnt exist")
            self._ui.readconfig(self._repo.path + '/hgrc')
            config = self._ui.configitems('paths')
            for item in config:
                if item[0]=='default':
                    return item[1]
        
    def log(self,fromdaysago=0,fromdate=0,fromkey=""):
        """
        @fromdate needs to be in epoch
        """
        cmd = 'log' 
        
        if fromdaysago<>0:
            datecmd=fromdaysago
        elif fromdate<>0:
            datecmd=fromdate        
        else:
            datecmd=""
            
        if fromkey:
            result,content=self._hgCmdExecutor(cmd, date = datecmd, rev=fromkey, template =  '{date}[BR]{author}[BR]{rev}[BR]{desc}\\n ----------------------------------------------------- \\n', follow = True, user='')
        else:
            result,content=self._hgCmdExecutor(cmd, date = datecmd, template =  '{date}[BR]{author}[BR]{rev}[BR]{desc}\\n ----------------------------------------------------- \\n', follow = True, user='')            
        
        lines=q.codetools.regex.extractBlocks(content,[" -* "],includeMatchingLine=False)
        changes=[]
        for item in lines:
            if item.strip()<>"":
                if item.count("[BR]")<>3:
                    self._raise("Output of log command was wrong syntax, needs to have 4x [BR], line was \n%s" % item)
                epochraw,author,rev,description=item.split("[BR]")
                if epochraw.find(".")<>-1:
                    date=int(epochraw.split(".")[0].strip())
                else:
                    date=int(epochraw)
                changes.append(HgChange(author,rev,description,date,self.repokey))
        return changes
        
    
    def __str__(self):
        msg="%s %s %s" % (self.remoteUrl, self.basedir,self.branchname)
        return msg
    
    def __repr__(self):
        return self.__str__()
    
    
class HgChange():
    def __init__(self,author,revision,description,date,repokey,files=""):
        self.author=author
        self.description=description
        self.date=date
        self.repokey=repokey
        self.files=files
        self.revision=revision
    
    def __str__(self):
        date=q.base.time.epoch2HRDateTime(self.date)
        msg="%s %s %s %s %s" % (self.repokey,self.author,date,self.revision,self.description.replace("\n","\\n"))
        return msg
    
    def __repr__(self):
        return self.__str__()        
