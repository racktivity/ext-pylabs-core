from pymonkey.InitBase import *

q.application.appname="repo downloader"
q.application.start()

from pymonkey.Shell import *

q.qshellconfig.interactive=True

repoaccount="incubaid"
names=q.clients.bitbucket.getRepoNamesFromBitbucket(repoaccount)
for name in names:
    #if name.lower().find("pylabs-core")<>-1:
    #    print name
    q.clients.bitbucket.checkoutRepo(repoaccount,name,forceUpdate=False)
        