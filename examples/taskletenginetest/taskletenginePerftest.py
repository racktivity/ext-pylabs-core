from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "taskletenginetest"
q.application.start()

taskletengine=q.taskletengine.get("taskletsPerfTest")
params={}
params["counter"]=0

nrruns=10000
for t in range(nrruns):
    taskletengine.execute(params)
print params["counter"]

q.application.stop()
