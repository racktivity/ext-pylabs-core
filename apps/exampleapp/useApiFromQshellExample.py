from pylabs.InitBase import *

q.application.appname="test api"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True


#p is the new cleaned up Pylabs root namespace

api=p.application.getApiDebug($applicationName)  #returns sync api, which runs tasklets immediately, no workflowengine involved, qshell can be used
api=p.application.getApi($applicationName)  #returns async api, calls appserver which will execute async or sync depending how implemented on appserver

api.ui.wizards.$wizardname.run($params...) #in console
api.ui.forms.$formname.run($params...)  #starts required backend for forms to run in debug mode, starts firefox with right params

api.rootobjects.$rootobjectname.$methodname($params)
api.rootobjects.$actorname.$methodname($params)





q.application.stop()
