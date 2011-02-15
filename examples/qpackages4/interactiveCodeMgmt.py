from pylabs.InitBase import *
from pylabs.Shell import *
from pprint import pprint

q.application.appname = "interactivecodemgmt"
q.application.start()

q.qshellconfig.interactive=True
#q.logger.consoleloglevel=2

#reponames=i.codemgmt.findBitbucketReponames("http","despiegk","dct007")
#i.codemgmt.checkoutBitbucketRepos("http","","despiegk","dct007")
ipshell()

#ipshell()

q.application.stop()

        
    