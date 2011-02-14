from pymonkey import q
from pymonkey.Shell import *
from ClusterSSHClient import ClusterSSHClient
import random
        
class ClusterNode():
    
    def __init__(self,cluster):
        self.hostname=""
        self.ipaddr=""
        self.ismaster=False
        self.cluster=cluster
        self.isPreparedForSSODebug=False
        self.ubuntuPackagesUpdated=False
        self.ubuntuPackagesInstalled=[]
        self.sshclient=ClusterSSHClient(cluster,self)
        
    def execute(self,commands,dieOnError=True,silent=False,timeout=60):
        q.transaction.start("Execute %s on node %s %s" % (commands, self.hostname,self.ipaddr),silent=silent)
        result=self.sshclient.execute(commands,dieOnError,timeout=timeout)
        q.transaction.stop()
        return result
    
    def executeQshell(self,commands,dieOnError=True,silent=False,timeout=60):
        if not commands:
            raise RuntimeError('Commands is empty!')
        print 'COMMANDS: ' + commands
        q.transaction.start("Execute qshellcmd %s on node %s %s" % (commands, self.hostname,self.ipaddr),silent=silent)
        tmpfilepath=q.system.fs.getTmpFilePath()
        
        #
        # p = """ some texts %s blabla """ % 'insert me' 
        # does not work so we do a replace.
        template="""
from pymonkey.InitBase import *
from pymonkey.Shell import *

q.application.appname = "qshellexecute"
q.application.start()

q.logger.maxlevel=6 #to make sure we see output from SSH sessions 
q.logger.consoleloglevel=2
q.qshellconfig.interactive=False
$COMMANDS
q.application.stop()
"""
        commands = template.replace('$COMMANDS', commands)
        
        q.system.fs.writeFile(tmpfilepath,commands)
        self.sendfile(tmpfilepath,tmpfilepath)
        result=self.sshclient.execute("/opt/qbase3/qshell -f %s" % tmpfilepath, dieOnError,timeout=timeout)
        q.system.fs.removeFile(tmpfilepath)
        q.transaction.stop()
        return result

    
    def sendfile(self,source,dest):
        q.transaction.start("send file %s to %s on %s" %(source,dest,self.ipaddr))
        ftp=self.getSftpConnection()
        if not q.system.fs.exists(source):
            raise RuntimeError("Could not find source file %s" % source)

        # If source == dest and we are on localhost and we do a put, the end result will be that the source files has been emptied
        # we we check here and do nothing in that case
        if source == dest and q.system.net.checkIpAddressIsLocal(self.ipaddr):
            pass # do nothing
        else:
            ftp.put(source,dest)
        # trying to fix problem paramico wait_for_event() SSHException: Channel closed.
        # ftp.close() # Closing the connecrions did not work, now trying to keep the same connection open
        q.transaction.stop()     
    
        
    def ping(self):
        return q.system.net.pingMachine(self.ipaddr,5)
    
    def sshtest(self):
        return self.sshclient.sshtest()
    
    def connect(self):
        return self.sshclient.connect()
    
    def activateAvahi(self):
        self.prepare(avahiInstallOnly=True)
        
    def prepare(self,avahiInstallOnly=False,ignoreUpgradeError=False):
        """
        prepare a node for cluster operation
        uses ssh
        only works for ubuntu        
        """        
        content="""<?xml version=\"1.0\" standalone=\'no\'?>
<!--*-nxml-*-->
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<!-- $Id$ -->
<service-group>
<name replace-wildcards="yes">daascluster %h</name>

<service>
<type>_daascluster._tcp</type>
<port>9999</port>
</service>

<service>
<type>_ssh._tcp</type>
<port>22</port>
</service>

</service-group>
"""
        content=content.replace("daascluster",self.cluster.domainname.replace(".","__"))
        tmpfile=q.system.fs.joinPaths(q.dirs.tmpDir,"avahi")
        q.system.fs.writeFile(tmpfile,content)        
        
        q.transaction.start("Try to configure nodes for cluster usage (will use SSH to do so).")       
        q.transaction.start("Ping machine %s" %self.ipaddr)
        if not q.system.net.pingMachine(self.ipaddr,5):
            q.console.echo("ERROR: Could not ping to machine %s, please check machine is reacheable."%self.ipaddr)
            q.transaction.stop()
        else:
            q.transaction.stop() #ping
            ##q.transaction.start("Open SSH connection to %s" %self.ipaddr)
            ##sshclient=q.clients.ssh.createClient(ipaddr,"root",rootpasswd,60)            
            if avahiInstallOnly==False:
                q.transaction.start("Upgrade ubuntu on %s to newest packages, this can take a long time (apt-get update & upgrade)." %self.ipaddr)                            
                self.execute("apt-get update",False)
                #returncode,stdout,stderr=self.execute("apt-get upgrade -y",False)
                #if returncode>0:
                    #if not ignoreUpgradeError or q.qshellconfig.interactive==False or not q.console.askYesNo("Could not upgrade system, do you want to ignore and continue?"):
                        #raise "Could not upgrade system (apt-get upgrade), probably because there was interactivity required."
                q.transaction.start("Install mc on %s" %self.ipaddr)   
                self.execute("apt-get install mc -y")
                q.transaction.stop()
                q.transaction.stop()
            else:
                q.transaction.start("Update ubuntu package metadata on %s (apt-get update)." %self.ipaddr)                                                
                self.execute("apt-get update",False)
                q.transaction.stop()                
                
            q.transaction.start("Install avahi on %s" %self.ipaddr)                        
            self.execute("apt-get install avahi-daemon avahi-utils -y",False)
            self.execute("mkdir -p /etc/avahi/services")            
            ftp=self.getSftpConnection()
            q.logger.log("put %s to /etc/avahi/services/daascluster.service" % tmpfile)
            ftp.put(tmpfile,"/etc/avahi/services/daascluster.service")
            q.transaction.stop() #reload avahi
            q.transaction.start("Reload Avahi Config")
            self.execute("avahi-daemon --reload")
            q.transaction.stop() #end of avahi
            q.transaction.start("Disable ssh name resolution")
            self.execute("echo 'UseDNS no' >> /etc/ssh/sshd_config",silent=True)
            self.execute("/etc/init.d/ssh restart",silent=True)
            q.transaction.stop()           
            
        q.transaction.stop() #end of ssh connection
                
                
            #if q.qshellconfig.interactive:
                #if copyqbase or q.console.askYesNo("Do you want to copy qbasedir to remote node over ssh?"):
                    ##self._removeRedundantFiles()
                    #if rsync==False:
                        #sshclient.copyDirTree("/opt/qbase3/")
                        #sshclient.copyDirTree("/opt/code/")
                    #else:
                        #q.system.process.executeWithoutPipe("rsync -avzEp -e ssh /opt/qbase3/ root@%s:/opt/qbase3/ " %self.ipaddr)
                        #q.system.process.executeWithoutPipe("rsync -avzEp -e ssh /opt/qbase3/ root@%s:/opt/code/ " %self.ipaddr)
        
    def halt(self):
        q.transaction.start("Halt node %s %s" % (self.hostname,self.ipaddr)) 
        self.execute("halt")
        q.transaction.stop()
        
    def copyQbase(self,sandboxname="",deletesandbox=True):        
        sandboxdir=q.system.fs.joinPaths(q.dirs.baseDir,"..","sandboxes")  
        if not q.system.fs.exists(sandboxdir):
            raise RuntimeError("Cannot find sandbox in %s" % sandboxdir)
        if sandboxname=="":            
            sandboxes=q.system.fs.listFilesInDir(sandboxdir)
            sandboxname=q.console.askChoice(sandboxes,"Select sandbox to copy",True)
        sandboxpath=q.system.fs.joinPaths(sandboxdir,sandboxname)
        q.transaction.start("Connect over ssh to %s" % self.ipaddr)
        q.transaction.start("Copy sandbox %s over sftp to remote /tmp dir" % sandboxpath)
        ftp=self.getSftpConnection()
        ftp.put(sandboxpath,"/tmp/qbase3.tgz")
        q.transaction.stop() #sftp
        q.transaction.start("Expand remote sandbox /tmp/qbase3.tgz to /opt/qbase3")         
        if deletesandbox:
            self.execute("rm -rf /opt/qbase3",timeout=10)
        self.execute("mkdir -p opt ; cd /opt ; tar xvfz /tmp/qbase3.tgz",timeout=60) #tar xvfz /tmp/qbase3.tgz #@todo complete
        q.transaction.stop() #expand
        q.transaction.stop() #sshconnection
        q.console.echo("Qbase copied and expanded into %s" % self.ipaddr)
               
    def sendQbaseDebug(self):
        sandboxdir="/opt/qbase3debug_*"   
        tarfile="/tmp/qbase3debug.tgz"
        q.transaction.start("Copy tgz sandbox %s over sftp to remote /tmp dir %s" % (sandboxdir,self.ipaddr))
        ftp=self.getSftpConnection()
        ftp.put(tarfile,tarfile)
        q.transaction.stop() #sftp
        q.transaction.start("Expand remote sandbox /tmp/qbase3debug.tgz to /opt/qbase3")         
        self.execute("cd /opt ; tar xvfz /tmp/qbase3debug.tgz",timeout=10) 
        q.transaction.stop()
        
    def sendExportedQbase(self,sandboxname):
        q.transaction.start("Copy tgz sandbox %s over sftp to remote /tmp dir %s" % (sandboxname,self.ipaddr))
        ftp=self.getSftpConnection()
        tarfile=q.system.fs.joinPaths(q.dirs.baseDir,"..","sandboxes","%s.tgz" %sandboxname)
        tarfiledest="/tmp/qbase3debug.tgz"
        ftp.put(tarfile,tarfiledest)
        q.transaction.stop() #sftp
        q.transaction.start("Expand remote sandbox /tmp/qbase3debug.tgz to /opt/qbase3")         
        self.execute("cd /opt ; tar xvfz /tmp/qbase3debug.tgz",timeout=10) 
        q.transaction.stop()
        
    def getSftpConnection(self):
        return self.sshclient.getSFtpConnection()
    
    def mkdir(self,destpath,silent=False):
        q.transaction.start("mkdir %s on %s" % (destpath,self.ipaddr),silent=silent)
        self.execute("mkdir -p %s" % destpath,silent=True,dieOnError=False,timeout=2)
        q.transaction.stop()
    
    def writeFile(self,destpath,fileContent,silent=False):
        q.transaction.start("writefile %s on %s" % (destpath,self.ipaddr),silent=silent)
        self.mkdir(q.system.fs.getDirName(destpath),silent=False)
        tmpfile=q.system.fs.joinPaths(q.dirs.tmpDir,str(random.randint(0,10000)))
        q.system.fs.writeFile(tmpfile,fileContent)
        ftp=self.getSftpConnection()
        q.logger.log("ftpput: %s to %s" % (tmpfile,destpath))
        ftp.put(tmpfile,destpath)
        q.transaction.stop()
        
    def writeTemplate(self,destpath,templatepath,replace=[],silent=False):
        """
        @param destpath: path of node where writing to is starting from root
            if destpath=="" will be same as templatepath but in qbase in other words destpath=/opt/qbase3/$templatepath
        @param templatepath : /opt/qbase3/utils/defaults/$templatepath
        @param replace  [[find,replacewith],[find2,replace2]]
        """
        q.transaction.start("write file %s from template utils/defaults/%s" % (destpath,templatepath),silent=silent)
        if destpath=="":
            destpath=q.system.fs.joinPaths(q.dirs.baseDir,templatepath)
        q.logger.log("clusternode.writetemplate: templatepath=%s destpath=%s"%(templatepath,destpath)),5
        templatepath=q.system.fs.joinPaths(q.dirs.baseDir,"utils","defaults",templatepath)        
        if not q.system.fs.exists(templatepath):
            raise RuntimeError("Cannot find template on %s" % templatepath)
        fileContent=q.system.fs.fileGetContents(templatepath)        
        for replaceitem in replace:
            fileContent=fileContent.replace(replaceitem[0],replaceitem[1])        
        self.writeFile(destpath,fileContent,silent=False)
        q.transaction.stop()
    
    def changeRootPassword(self,newPassword,silent=False):
        q.transaction.start("Change root passwd ",silent=False)
        self.writeTemplate("","utils/sysadminscripts/changePassword.sh",[["$passwd$",newPassword]])
        try:
            self.execute(q.system.fs.joinPaths(q.dirs.baseDir,"utils","sysadminscripts","changePassword.sh"))  
        except:
            self.install("expect")
            self.execute("expect "+q.system.fs.joinPaths(q.dirs.baseDir,"utils","sysadminscripts","changePassword.sh"))  
        q.transaction.stop()
        
        
    def setHostname(self,newhostname,silent=False):
        q.transaction.start("Set hostname to %" % newhostname,silent=silent)
        self.execute("echo %s > /etc/hostname"%newhostname,silent=True)
        self.execute("hostname %s"%newhostname,silent=True)
        q.transaction.stop()
        
    
    def install(self,packagename,silent=False):        
        if self.ubuntuPackagesUpdated==False:
            q.transaction.start("Upgrade ubuntu package metadata")                            
            self.execute("apt-get update",False)
            q.transaction.stop()
        q.transaction.start("Install ubuntu package %s" %packagename,silent=silent)    
        if packagename not in self.ubuntuPackagesInstalled:
            self.execute("apt-get install %s -y"%packagename,True)
            self.ubuntuPackagesInstalled.append(packagename)
        q.transaction.stop()
            
        
    def createCifsShare(self,sharename="opt",sharepath="/opt",rootpasswd="rooter"):
        """
        only creates 1 cifs share, other shares will be lost
        """
        self.install("samba")
        self.writeTemplate("/etc/samba/smb.conf",q.system.fs.joinPaths(q.dirs.baseDir,"utils","defaults","etc","smb.conf"),[["$sharename$",sharename],["$sharepath$",sharepath]])
        self.execute("echo -ne \"%s\\n%s\\n\" | smbpasswd -a -s root" %(rootpasswd,rootpasswd))
        self.execute("/etc/init.d/samba restart")
        
    
    def createPublicNfsShare(self,sharepath="/opt"):
        """
        only creates 1 nfs share, no passwords for now!!!!
        """
        self.prepareForSSODebug()        
        self.install("nfs-kernel-server")
        self.writeFile("/etc/exports","/opt *(rw,sync,no_root_squash,no_subtree_check)")        
        self.execute("echo '' > /etc/hosts.allow",dieOnError=True)
        self.execute("echo '' > /etc/hosts.deny",dieOnError=True)
        self.execute("exportfs -rav")
        
    def connectCodedir(self,ipaddr):
        """
        mount /opt/code to /opt/code of the specified node (ipaddr)
        """
        dirpath="/opt/code"
        self.connectToNFSServer(dirpath,ipaddr)

    def connectQpackagedir(self,ipaddr,delete=False):
        """
        mount /opt/code to /opt/code of the specified node (ipaddr)
        """
        dirpath="/opt/qbase3/var/qpackages4"
        self.connectToNFSServer(dirpath,ipaddr,delete)
        
    def installQPackage(self, name, domain, version, reconfigure=True):
        """
        install qpackage name, domain, version onto cluster node
        """
        installPackageCommand = """p = q.qp.find(name="%(name)s", domain="%(domain)s", version="%(version)s")
if not p:
    raise valueError("Package %(domain)s, %(name)s, %(version)s not found")
elif len(p) <> 1:
    raise valueError("Too many packages found with search criteria %(domain)s, %(name)s, %(version)s")
elif not p[0].isInstalled():
    p[0].install()
else:
    print "Package %(domain)s, %(name)s, %(version)s is already installed"
"""%{'name':name,'version':version,'domain':domain,'reconfigure':reconfigure}
        self.executeQshell(installPackageCommand)
        if reconfigure:
            self.executeQshell("q.qp._runPendingReconfigeFiles()")
        
    def connectToNFSServer(self,dirpath, ipaddr,delete=False):
        """
        e.g. if dirpath=/opt/code
        then: this code will mount /opt/code to /opt/code of the specified node (ipaddr)
        """
        q.transaction.start("mount %s to %s:%s" % (dirpath,ipaddr,dirpath))        
        self.install("nfs-common")
        self.execute("umount %s" % dirpath,dieOnError=False)
        #if delete:
        outp=self.execute("mount | grep %s" % dirpath,dieOnError=False)
        if len(outp)>5:
            raise RuntimeError("There is still a mount on the directory %s, could not umount")
        self.execute("rm -rf %s" % dirpath)        
        self.execute("mkdir -p %s" % dirpath)
        self.execute("mount %s:%s/ %s" % (ipaddr,dirpath,dirpath))
        q.transaction.stop()

        
    def symlink(self,target, linkname):
        # @type linkname
#        if linkname.find('//') != -1:
#            print 'Raising exception////////////////////////////'
#            raise
        # replace double //
        target   = target.replace('//', '/')
        linkname = linkname.replace('//', '/')
        if len(linkname)<3:
            raise RuntimeError("Linkname should be more than 2 chars to be valid, is check to make sure we don't remove / of system")
        q.transaction.start("Creating symlink %s -> %s on %s" % (target, linkname, self.ipaddr))
        # It the file exists remove it 
        #if self.execute("test -e '%s'" % (linkname), False)[0] == 0: # the file exists
            #if linkname == '/': # just to be sure we don't delete the harddrive!
                #raise
        self.execute("rm  -Rf '%s'" % (linkname), False)
        # if the directory does not exist create it
        dir = q.system.fs.getDirName(linkname)
        self.execute("mkdir -p '%s'" % (dir), True)

            # make the directory
            #self.execute("rm '%s'" % (linkname), True)
        # Make the link
        self.execute("ln -s %s %s" % (target, linkname), False)
        q.transaction.stop()

    def backupQbase(self):
        q.transaction.start("Backup opt/qbase3 on %s" % self.ipaddr)
        path="/opt/backups/qbase3_%s.tgz" % q.base.time.getLocalTimeHRForFilesystem()
        self.execute("mkdir -p /opt/backups", False)
        self.execute("tar zcvfh %s /opt/qbase3" % path, False)
        self.execute("echo '%s' >  /opt/backups/path_to_last_backup.txt" % path, True)
        q.transaction.stop()

    def restoreQbase(self):
        q.transaction.start("Restoring opt/qbase3 on %s" % self.ipaddr)
        exitcode, path = self.execute("cat '/opt/backups/path_to_last_backup.txt'", True)
        self.execute("rm -Rf /opt/qbase3", False)
        # cd /; is redundant, don't know why it wont work without it?
        self.execute("cd /; tar vxzf %s -C /" % path, False)
        q.transaction.stop()
        
    def backupQbaseCode(self):
        """
        backup only the small files, excludes the 30 biggest files, iso's, .so's and stuff ..
        """
        q.transaction.start("Backup /opt/qbase pylabs code on %s" % self.ipaddr)
        self.execute("mkdir -p /opt/backups", False)
        path="/opt/backups/pylabscore_%s.tgz" % q.base.time.getLocalTimeHRForFilesystem()
        pathstobackup='/opt/qbase3/lib/pymonkey/extensions /opt/code/pylabs-core/code/utils /opt/code/pylabs-core/code/packages/pymonkey/core'
        # compress them
        self.execute("tar zcvfh %s %s " % (path, pathstobackup) , False)
        # remember last compressed
        self.execute("echo '%s' >  /opt/backups/path_to_last_pylabscode_backup.txt" % path, True)
        q.transaction.stop()

    def restoreQbaseCode(self):
        q.transaction.start("Restore partial /opt/qbase/ pylabscode on %s" % self.ipaddr)
        exitcode, path = self.execute("cat '/opt/backups/path_to_last_pylabscode_backup.txt'")
        # remove all files in the tar, cd is needed or wont work!
        self.execute("cd /; tar zft '%s' | grep -v ^d | awk {'print $6'} | xargs rm" % path, False)
        # extract all files in the tar
        self.execute("echo 'cd /; tar xzf '%s' -C /' > /tmp/out.tmp" % path, False)
        print self.execute("cd /; tar xzf '%s' -C /" % path, False)
        q.transaction.stop()
        
    def prepareForSSODebug(self):
        if self.isPreparedForSSODebug==False:
            q.transaction.start("Prepare for debug on %s" % self.ipaddr)
            self.execute("cp /etc/apt/sources.list.disabled /etc/apt/sources.list",False)
            self.execute("apt-get update",False)
            self.install("mc")
            q.transaction.stop()
            self.isPreparedForSSODebug=True
        
    def __str__(self):
        #return "%s %s master:%s" % (self.hostname,self.ipaddr,self.ismaster)
        return "%s %s" % (self.hostname,self.ipaddr)
    
    __repr__=__str__
