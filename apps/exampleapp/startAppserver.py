from pylabs.InitBase import *

q.application.appname="start appserver"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True

p.application.services.appserver.start(path="",appServerPort=4567,workflowEnginePort=4568)  #starts appserver in currentdir on port 4567 and workflow engine on 4568 (starts and returns)
p.application.services.appserver.debug(path="",appServerPort=4567,workflowEnginePort=4568)  
   #starts appserver in debug mode, means appserver will only run 1 thread and qshell can be used to debug, will wait till appserver stopped
   #wofklow engine is not used then but tasklet engine executes directly in thread specified above


q.application.stop()
