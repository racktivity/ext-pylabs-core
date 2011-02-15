from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "taskletenginetest"
q.application.start()

taskletengine=q.taskletengine.get("tasklets")
params={}
params["user"]="kds"

print "will find 3 tasklets"
taskletengine.execute(params)
print

print "will find 2 tasklets"
taskletengine.execute(params,tags=["tag1"])
print

print "will find tasklet3, because has highest priority and only 1 can be found"
taskletengine.executeFirst(params)


q.application.stop()
