from pylabs import q
from pylabs.Shell import *
from ClusterNode import ClusterNode
from pylabs.baseclasses import BaseType
import os

                    
class Cluster(BaseType):
    domainname=q.basetype.string(doc="domain name of cluster")
    superadminpassword=q.basetype.string(doc="superadmin password of cluster")
    _superadminpasswords=q.basetype.list()
    nodes=q.basetype.list()
    
    def __init__(self,clustername,domainname,ipaddresses,superadminpassword,superadminpasswords=[],masteripaddress=""):
        self.domainname=domainname
        self.superadminpassword=superadminpassword
        self._superadminpasswords=superadminpasswords
        self.nodes=[]
        
        self.localip=""
        
        #import pdb
        #pdb.set_trace()

        if ipaddresses==[]:
            services=q.cmdtools.avahi.getServices()
            sshservices=services.find(port=22,partofdescription=domainname.replace(".","__"))
            for sshservice in sshservices:
                node=ClusterNode(self)
                node.hostname=sshservice.hostname
                node.ipaddr=sshservice.address
                self.nodes.append(node)
        else:
            for ipaddr in ipaddresses:
                node=ClusterNode(self)
                node.hostname=ipaddr
                node.ipaddr=ipaddr
                node.ismaster=True if masteripaddress == ipaddr else False
                self.nodes.append(node)
                
    #def getSuperadminPassword(self):
        #if len(self.superadminpasswords)>1:
            #raise RuntimeError("There can only be one superadmin password specified, use cluster.setSuperadminPassword(), which will make sure password has been set on all nodes")
        #if len(self.superadminpasswords)<1:
            #raise RuntimeError("No superadmin password specified")
        #return self.superadminpasswords[0]

    def listnodes(self, type='all'):
        if type == 'all':
            return [ node.hostname for node in self.nodes]
        if type == 'master':
            for node in self.nodes:
                if node.ismaster: return [node.hostname]
        return []
    
    def copyQbase(self,sandboxname="",hostnames=[],deletesandbox=None): 
        """
        sandboxes are $sandboxname.tgz in /opt/sandboxes
        @param sandboxname is name of a sandbox in that directory
        """
        nodes=self.selectNodes("Select which nodes",hostnames)
        q.transaction.start("Copy qbase onto cluster.")
        sandboxdir=q.system.fs.joinPaths(q.dirs.baseDir,"..","sandboxes")
        sandboxes=q.system.fs.listFilesInDir(sandboxdir)
        if sandboxname=="":
            sandboxname=q.console.askChoice(sandboxes,"Select sandbox to copy",True)        
        if deletesandbox==None:
            deletesandbox=q.console.askYesNo("    Do you want to remove remote qbase3 directory (if it exists?)")
        for node in nodes:
            node.copyQbase(sandboxname=sandboxname,deletesandbox=deletesandbox)
        q.transaction.stop()        

    def sendQbaseDebug(self,hostnames=[]): 
        """
        /opt/qbase3debug_* will be sent to remote node
        """
        nodes=self.selectNodes("Select which nodes",hostnames)
        q.transaction.start("Copy qbase3debug_* onto cluster.")  
        masterSandboxDir=q.system.fs.joinPatsh(os.sep, 'opt', 'qbase3debug_master')
        allSandboxDir=q.system.fs.joinPaths(os.sep, 'opt', 'qbase3debug_all')        
        if not q.system.fs.exists(allSandboxDir) and not q.system.fs.exists(masterSandboxDir):
            raise RuntimeError("Cannot find sandbox in qbase3debug_*")
        q.transaction.start("Targz the debug sandbox" )
        #q.cloud.cluster._removeRedundantFiles()
        excludes=[".*\.pyc$",".*\.pyo$",".*~$",".*\.bak$",".*/var/.*",".*/cfg/.*"]
        excludes.append(".*/.hg/.*")
        excludes.append(".*/.cvs/.*")
        tarfile="/tmp/qbase3debug.tgz"
        q.system.fs.targzCompress(masterSandboxDir,tarfile,False,destInTar="qbase3",pathRegexExcludes=excludes,extrafiles=[[allSandboxDir,tarfile],])
        q.transaction.stop()                         

        for node in nodes:
            node.sendQbaseDebug()
        q.transaction.stop()          

    def sendExportedQbase(self,sandboxname=None,hostnames=[]):
        nodes=self.selectNodes("Select which nodes",hostnames)
        q.transaction.start("Copy exported qbase3 onto cluster.")  
        sandboxdir=q.system.fs.joinPaths(q.dirs.baseDir,"..","sandboxes")
        choices=[q.system.fs.getBaseName(item).replace(".tgz","") for item in q.system.fs.listFilesInDir(sandboxdir)] 
        q.console.echo("Select sandbox to sent to cluster")
        sandboxname=q.console.askChoice(choices)        
        for node in nodes:
            node.sendExportedQbase(sandboxname)
        q.transaction.stop()          
        
        
    def sshtest(self):
        q.transaction.start("SSH STATUS TEST:")
        results={}
        for node in self.nodes:
            result=node.sshtest()
            if q.qshellconfig.interactive:
                q.console.echo("sshtest %s %s %s" % (node.hostname,node.ipaddr,result))
            results[node.hostname]=result
        q.transaction.stop()
        if q.qshellconfig.interactive==False:
            return results            

    def connect(self):
        q.transaction.start("cluster connect")
        for node in self.nodes:
            result=node.connect()
        q.transaction.stop()
        
    def ping(self):
        q.transaction.start("PING STATUS TEST:")
        results={}
        for node in self.nodes:
            result=node.ping()
            if q.qshellconfig.interactive:
                q.console.echo("ping %s %s %s" % (node.hostname,node.ipaddr,result))
            results[node.hostname]=result
        q.transaction.stop()
        if q.qshellconfig.interactive==False:
            return results  

    def execute(self,command,hostnames=[],dieOnError=True):        
        """
        execute a command on every node of the cluster, only output the result
        """
        q.transaction.start("Execute %s on cluster."%command)
        nodes=self.selectNodes("Select which nodes",hostnames)
        results={}
        for node in nodes:            
            returncode,stdout=node.execute(command,dieOnError)
            ##stdout=q.console.formatMessage(stdout,prefix="stdout")
            results[node.hostname]=[returncode,stdout]
            if q.qshellconfig.interactive:
                q.console.echo(stdout)
        q.transaction.stop()
        if q.qshellconfig.interactive==False:
            return results
 
    def executeQshell(self,command,hostnames=[],dieOnError=True):        
        """
        execute a command on every node of the cluster, only output the result
        """
        q.transaction.start("Execute qshell cmd %s on cluster."%command)
        nodes=self.selectNodes("Select which nodes",hostnames)
        results={}
        for node in nodes:            
            returncode,stdout=node.executeQshell(command,dieOnError)
            ##stdout=q.console.formatMessage(stdout,prefix="stdout")
            results[node.hostname]=[returncode,stdout]
            if q.qshellconfig.interactive:
                q.console.echo(stdout)
        q.transaction.stop()
        if q.qshellconfig.interactive==False:
            return results
        else:
            return results

    def syncRootPasswords(self, newPasswd):
        '''
        Reset all root passwords of nodes in this cluster to the specified value.
        Remark: requires that cluster is created with correct root passwords provided.
        
        @param newPasswd The root password to set on the nodes
        @type newPasswd String
        ''' 
        for node in self.nodes:
            node.changeRootPassword(newPasswd)            
        
    def get(self,name):
        for node in self.nodes:
            if node.hostname==name:
                return node
        raise RuntimeError("Could not find node %s in cluster." % name)
    
    def __str__(self):
        msg="domain:%s\n"% self.domainname
        for node in self.nodes:
            msg+=" * %s\n" % str(node)
        return msg
    
    __repr__=__str__
    
    def selectNodes(self,message="",hostnames=[]):
        """
        only for interactive usage
        """
        if hostnames<>[]:
            return [self.get(name) for name in hostnames]
        choices=hostnames
        if choices==[] and q.qshellconfig.interactive==False:
            raise RuntimeError("cluster.selectNodes() can only be used in interactive mode")        
        if choices==[]:
            choices=[str(node.hostname) for node in self.nodes]
            choices.append("ALL")
            choices=q.console.askChoiceMultiple(choices,message or "select nodes",True)
            if "ALL"==choices[0]:
                choices=[str(node.hostname) for node in self.nodes]
        result=[self.get(name) for name in choices]
        return result

    def halt(self,hostnames=[]):
        q.transaction.start("Stop nodes over ssh")
        nodes=self.selectNodes("Select which nodes you want to halt",hostnames)
        for node in nodes:
            node.halt()
        q.transaction.stop()  

    def sendfile(self,source,dest="",hostnames=[]):
        if dest=="":
            dest=source
        q.transaction.start("Send file %s to dest %s on nodes over ssh" % (source,dest))
        nodes=self.selectNodes("Select which nodes you want to halt",hostnames)
        for node in nodes:
            node.sendfile(source,dest)
        q.transaction.stop()          
        
    def activateAvahi(self,hostnames=[]):
        q.transaction.start("Activate avahi on nodes for cluster")
        nodes=self.selectNodes("Select which nodes you want to activate",hostnames)
        for node in nodes:
            node.activateAvahi()
        q.transaction.stop()  

    def prepare(self,hostnames=[]):
        q.transaction.start("Prepare nodes for cluster")
        nodes=self.selectNodes("Select which nodes you want to prepare",hostnames)
        for node in nodes:
            node.prepare()
        q.transaction.stop()        
        
    def createCifsShare(self,sharename="opt",sharepath="/opt",rootpasswd="rooter",hostnames=[]):
        """
        per node only creates 1 cifs share, other shares will be lost
        carefull will overwrite previous shares
        """
        q.transaction.start("Create cifs share on selected cluster nodes")
        nodes=self.selectNodes("Select which nodes you want to create a cifs share upon",hostnames)
        for node in nodes:
            node.createCifsShare(sharename,sharepath,rootpasswd)
        q.transaction.stop()
    
    def createPublicNfsShare(self,sharepath="/opt",hostnames=[]):
        """
        per node only creates 1 nfs share, no passwords for now!!!!
        carefull will overwrite previous shares
        """
        q.transaction.start("Create nfs share on selected cluster nodes")
        nodes=self.selectNodes("Select which nodes you want to create a nfs share upon",hostnames)
        for node in nodes:
            node.createPublicNfsShare(sharepath)
        q.transaction.stop()
        
    def connectMeToNfsShares(self,sharepath="/opt",hostnames=[]):
        """
        make connections between me and the nodes in the cluster
        will be mounted on, /mnt/$hostname/$sharepath e.g. /mnt/node1/opt 
        """
        q.transaction.start("Create nfs connection to selected cluster nodes, will be mounted on, /mnt/$hostname/$sharepath e.g. /mnt/node1/opt ")
        nodes=self.selectNodes("Select which nodes you want to create a nfs share upon",hostnames)
        if not q.system.fs.exists("/usr/sbin/nfsstat"):
            q.transaction.start("install nfs client")
            q.system.process.execute("apt-get update",dieOnNonZeroExitCode=False)
            q.system.process.execute("apt-get install nfs-common -y",dieOnNonZeroExitCode=False)
            q.transaction.stop()
        for node in nodes:    
            q.transaction.start("mount to %s" % node.hostname)
            mntpath=q.system.fs.joinPaths("/mnt",node.hostname,sharepath.replace("/",""))
            q.system.process.execute("umount %s" % mntpath,dieOnNonZeroExitCode=False)
            q.system.fs.createDir(mntpath)
            q.system.process.execute("mount %s:%s/ %s" % (node.ipaddr,sharepath,mntpath),dieOnNonZeroExitCode=False)#@todo make code better, should check if mount is the right mount
            q.transaction.stop()
        q.transaction.stop()    
        
    def shareMyNodeToCluster(self):
        """
        over NFS & CIFS
        CAREFULL: will overwrite existing config
        will export /opt
        for cifs passwd is root/rooter
        """            
        q.system.process.execute("apt-get update",dieOnNonZeroExitCode=False)
        q.system.process.execute("apt-get install samba nfs-kernel-server -y",dieOnNonZeroExitCode=False)
        replace=[["$sharename$","opt"],["$sharepath$","/opt"]]
        fileContent=q.system.fs.fileGetContents(q.system.fs.joinPaths(q.dirs.baseDir,"utils","defaults","etc","smb.conf"))        
        for replaceitem in replace:
            fileContent=fileContent.replace(replaceitem[0],replaceitem[1])        
        q.system.fs.writeFile("/etc/samba/smb.conf",fileContent)        
        q.system.fs.writeFile("/etc/exports","/opt *(rw,sync,no_root_squash,no_subtree_check)")
        #if q.console.askYesNo('Allow me to overwrite /etc/hosts.allow and /etc/hosts.deny?'):
        q.system.fs.writeFile('/etc/hosts.allow', '')
        q.system.fs.writeFile('/etc/hosts.deny', '')
        #else:
        #    q.console.echo('Please ensure you /etc/hosts.allow and /etc/hosts.deny are configured to allow sharing of you /opt folder!')
        q.system.process.execute("exportfs -rav")
        
        # q.system.process.execute("echo -ne \"%s\\n%s\\n\" | smbpasswd -a -s root" %("rooter","rooter"))
        # -> does not work, reported bug in jira, this is a workaround
        q.system.fs.writeFile('/tmp/smbpasswdset', 'rooter\nrooter\n')           # workaround
        q.system.process.execute('cat /tmp/smbpasswdset | smbpasswd -a -s root') # workaround
        
        q.system.process.execute("/etc/init.d/samba restart")  
        
    def getMyClusterIp(self):
        if self.localip<>"":
            return self.localip
        interfaces=["eth0","eth1","br0","br1","br2","wlan0","wlan1"]
        ipaddresses=[]
        localip=""
        for interface in interfaces:
            ipaddr=q.system.net.getIpAddress(interface)
            if ipaddr<>[]:
                ipaddr=ipaddr[0][0]
                ipaddresses.append(ipaddr)
        knownips=[node.ipaddr for node in self.nodes]
        for ip in knownips:
            if ip in ipaddresses:
                localip=ip
                break
        if localip=="":
            localip=q.console.askString("Give ipaddress of localmachine")
        self.localip=localip
        return localip
    
    def connectClusterToMyCode(self,hostnames=[]):
        """
        will connect mount /opt/code on each node to my /opt/code over nfs
        """
        q.transaction.start("Connect cluster to my /opt/code")
        nodes=self.selectNodes("Select which nodes you want to let connect to your code",hostnames)
        localip=self.getMyClusterIp()
        for node in nodes:
            node.connectCodedir(localip)
        q.transaction.stop()
        
    def connectClusterToMyQpackages(self,hostnames=[]):
        """
        connect the nodes of the cluster to my /opt/qbase3/var/qpackages4 directory
        also push my qpackages configuration to the other clusternodes
        allows the cluster to install from my local qpackages (not from the central repo)
        """
        q.transaction.start("Connect cluster to my qpackages 4 directory")
        nodes=self.selectNodes("Select which nodes you want to let connect to your code",hostnames)
        localip=self.getMyClusterIp()
        for node in nodes:
            node.connectQpackagedir(localip)
        q.transaction.stop()
    
    def installQPackage(self, name, domain, version, reconfigure, hostnames=[]):
        """
        install a qpackage on the specified nodes in the cluster
        """
        q.transaction.start("Install package on cluster")
        nodes = self.selectNodes("Select which on which nodes you want to install this qpackage", hostnames)
        for node in nodes:
            node.installQPackage(name, domain, version, reconfigure)
        q.transaction.stop()
        
    def symlink(self,target,linkname, hostnames=[]):
        """
        symlink a source to a dest using a symlink
        
        """
#        print "ln -s %s %s" % (target,linkname)
#        self.execute("ln -s %s %s" % (target,linkname))
        nodes=self.selectNodes("Select which nodes you want to let connect to your code",hostnames)
        for node in nodes:
            node.symlink(target, linkname)

    def backupQbase(self,hostnames=[]):
        nodes=self.selectNodes("Select which nodes you want to let connect to your code",hostnames)
        for node in nodes:
            node.backupQbase()

    def restoreQbase(self,hostnames=[]):
        nodes=self.selectNodes("Select which nodes you want to let connect to your code",hostnames)
        for node in nodes:
            node.restoreQbase()

    def backupQbaseCode(self,hostnames=[]):
        nodes=self.selectNodes("Select which nodes you want to let connect to your code",hostnames)
        for node in nodes:
            node.backupQbaseCode()

    def restoreQbaseCode(self,hostnames=[]):
        nodes=self.selectNodes("Select which nodes you want to let connect to your code",hostnames)
        for node in nodes:
            node.restoreQbaseCode()

    def mkdir(self,path,hostnames=[]):
        nodes=self.selectNodes("Select which nodes you want to create a dir on",hostnames)
        for node in nodes:
            node.mkdir(path)            

            
                     
    #def activateSSODebugMode(self):
        #"""
        #will checkout pylabs and many required repo's for SSO
        #will share the local sandbox over nfs
        #will create links between repo's and local sandbox        
        #will link log directories from cluster node to local log dir
        #"""
        
        