from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "testAppPlist"
q.application.start()

plist=q.system.plists.find("/opt/qbase3/apps")
plist.copyTo("/tmp") #copies all files to /tmp from plist

q.application.stop()
