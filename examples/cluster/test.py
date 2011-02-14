from pymonkey.InitBase import *
from pymonkey.Shell import *

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

ipshell()

q.application.stop()


