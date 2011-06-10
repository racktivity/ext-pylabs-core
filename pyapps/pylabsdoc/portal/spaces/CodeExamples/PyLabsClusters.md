# Pylabs Clusters Example


## create a cluster

[[code]]
q.cluster.create(?
Definition: q.cluster.create(self, clustername='', domainname='', ipaddresses=[], superadminpassword='', superadminpasswords=[], masteripaddress='')
Documentation:
    domainname needs to be unique
    clustername is only a name which makes it easy for you to remember and used to store in config file
[[/code]]


## get a cluster

[[code]]
q.cluster.get(?                                                                                                                                                
Definition: q.cluster.get(self, clustername='', domainname='')
Documentation:
    return cluster for specified domain or shortname, 
    there needs to be a cluster defined already before otherwise no nodes will be found
    config file which stores this info is at $qbasedir/cfg/qconfig/clusterconfig.cfg
    only one of the 2 params is required
[[/code]]


## the cluster factory class methods

    q.cluster.                                                                                                                                                              
    q.cluster.clusters                   q.cluster.create(                    q.cluster.list(                      q.cluster.replicator
    q.cluster.config                     q.cluster.get(                       q.cluster.listAvahiEnabledMachines( 


## fetch cluster & show methods on cluster object

    In [4]: cl=q.cluster.get()                                                                                                                                                      
     select cluster
        1: me
        2: 144
        Select Nr (1-2): 2
    
    In [5]: cl.                                                                                                                                                                     
    cl.activateAvahi(           cl.connectMeToNfsShares(    cl.execute(                 cl.mkdir(                   cl.restoreQbaseCode(        cl.sshtest(
    cl.backupQbase(             cl.copyQbase(               cl.executeQshell(           cl.nodes                    cl.selectNodes(             cl.superadminpassword
    cl.backupQbaseCode(         cl.createCifsShare(         cl.get(                     cl.ping(                    cl.sendQbaseDebug(          cl.symlink(
    cl.connect(                 cl.createPublicNfsShare(    cl.halt(                    cl.prepare(                 cl.sendfile(                
    cl.connectClusterToMyCode(  cl.domainname               cl.listnodes(               cl.restoreQbase(            cl.shareMyNodeToCluster(


## an example

[[code]]
from pylabs.InitBase import *
#from pylabs.Shell import *

q.application.appname = "cluster"
q.application.start()

q.logger.maxlevel=6 #to make sure we see output from SSH sessions
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True

cl=q.cluster.create("me","daascluster1.com",["192.168.16.106","10.10.10.10"],"1234",["rooter"],["192.168.16.106"])

cl=q.cluster.get()

print cl
cl.ping()
cl.sshtest()
cl.activateAvahi()
cl.prepare()

cl.execute("ls /")

cl.copyQbaseToClusterNodes()


cl.nodes[0].createCifsShare(sharepath="/opt",rootpasswd="rooter")
cl.nodes[1].createPublicNfsShare()

#do the same for all modes
cl.createPublicNfsShare()
cl.connectMeToNfsShares()

#ipshell()

q.application.stop()
[[/code]]