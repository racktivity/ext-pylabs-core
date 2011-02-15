from pylabs.InitBase import *

q.application.appname="generate code"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True

q.core.codemanagement.tasklets.generate(path="")  #uses current path if not specified, generate all tasklets for defined interfaces if not existing yet (rootobjects & actors)
q.core.codemanagement.api.generate(path="")  #generate all api for appserver, extensions for rootobjects & actors


q.application.stop()
