from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "mercurial"
q.application.start()

#ipshell()
q.logger.consoleloglevel=5

#@todo to be redone with q.clients.mercurial4...


q.application.stop()

