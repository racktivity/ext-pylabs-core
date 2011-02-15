

'''Utility methods to work with hg repositories'''

import os.path
from urlparse import urlparse, urlunparse
import re
import pylabs
from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.Shell import *

class HgToolTemp:    
    
    def checkout(self, hgurl, targetdir, reponame="", branchName='tip'):
        """
        reponame is name under which we are going checkout in dir targetdir, if not specified same as name repository
        """
        if not q.system.fs.exists(targetdir):
            raise RuntimeError("Cannot find targetdir %s" % targetdir)
        if reponame=="":
            while hgurl[-1]=="/":
                hgurl=hgurl[0:-1]
            reponame=hgurl.split("/")[-1]
        target=q.system.fs.joinPaths(targetdir, reponame)
        
        if q.system.fs.exists(target):
            # pull, but the repo may be corrupt than delete and call myself again
            try:
                cmd="cd %s ; hg pull " % (target)
                q.system.process.executeWithoutPipe(cmd)
                cmd="cd %s ; hg up %s" % (target, branch)
                q.system.process.executeWithoutPipe(cmd)
            except:
                if q.gui.dialog.askYesNo('!! need to delete %s to continue, is this ok? ' % target):
                    q.system.fs.removeDirTree(target)
                    self.checkout(hgurl,branchName,targetdir,reponame)
                else:
                    raise RuntimeError("could not delete invalid repo " + target)
        else:
            #clone
            q.system.fs.createDir(target)
            cmd="cd %s ;hg clone %s %s ;cd %s ;hg update %s" % (targetdir, hgurl, reponame, reponame, branchName)
            process=q.system.process.executeWithoutPipe(cmd)

    def checkoutQpackageRepo(self,hgbaseurl,reponame,qpackagedomainname):
        targetdir=q.system.fs.joinPaths(q.dirs.varDir,"qpackages4","metadata")
        hgurl="%s/%s" % (hgbaseurl,reponame)
        self.checkout(hgurl,targetdir,reponame=qpackagedomainname)
        
        
    def checkin(self, hgurl, targetdir, commitMessage, reponame=''):
        """
        reponame is name under which we are going checkout in dir targetdir, if not specified same as name repository
        """
        if reponame=="":
            while hgurl[-1]=="/":
                hgurl=hgurl[0:-1]
            reponame=hgurl.split("/")[-1]
            
        target=q.system.fs.joinPaths(targetdir, reponame)
        
        if not q.system.fs.exists(target):
            raise RuntimeError("Cannot find repository %s" % targetPath)
        
        q.logger.log('checking in code of repo ' + target)
        
        # addremove
        command = ''' cd $localrepo$; hg addremove '''
        command = command.replace('$localrepo$', target)
        q.console.echo('executing command: ' + command)
        q.system.process.executeWithoutPipe(command)
    
        # commit
        command = ''' cd $localrepo$; hg commit -m '$commitMessage$' '''
        command = command.replace('$localrepo$', target)
        command = command.replace('$commitMessage$', commitMessage)
        q.console.echo('executing command: ' + command)
        q.system.process.executeWithoutPipe(command)
        
        # pull
        command = ''' cd $localrepo$; hg pull $url$ '''
        command = command.replace('$localrepo$', target)
        command = command.replace('$url$', hgurl)
        q.console.echo('executing command: ' + command)
        q.system.process.executeWithoutPipe(command)
        
        # merge
        try:
            command = ''' cd $localrepo$; hg merge '''
            command = command.replace('$localrepo$', target)
            q.console.echo('executing command: ' + command)
            exitcode, output = q.system.process.execute(command)
        except Exception, e:
            if str(e).find('there is nothing to merge') != -1:
                pass
            else:
                print str(e)
                raise e
            
        
        # commit
        command = ''' cd $localrepo$; hg commit -m 'merge' ''' 
        command = command.replace('$localrepo$', target)
        q.console.echo('executing command: ' + command)
        q.system.process.executeWithoutPipe(command)
        
        # Push
        command = ''' cd $localrepo$; hg push $url$ '''
        command = command.replace('$localrepo$', target)
        command = command.replace('$url$', hgurl)
        q.console.echo('executing command: ' + command)
        q.system.process.executeWithoutPipe(command)
        
        
        
        