from pylabs.InitBase import *
from pylabs.Shell import *
from lib.TestEnv import *

q.application.appname = "ssoTestMgmt"
q.application.start()

q.logger.maxlevel=6 
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True

hosts=["10.100.159.253","10.100.159.252"]

cl=q.cluster.create("ssotest","ssotest",hosts,"rooter")

#preparation
def prepareOnce(cl):
    cl.mkdir("/opt/qbase5/var/tmp",hosts)

def  getSmartInfo(cl):

    #ca=i.config.cloudApiConnection.find("main")
    
    qscript="""
monitoringOsisConnection=i.config.osisconnection.find("monitoring")
devicesmonGuids=monitoringOsisConnection.devicemon.find(mon.devicemon.getFilterObject())
smartinfo=[]
for devicesmonGuid in devicesmonGuids:
    devicemonObject=monitoringOsisConnection.devicemon.get(devicesmonGuid)
    smartinfo.append( devicemonObject.disks[1].smartinfo)
print smartinfo"""
    
    cl.executeQshell(qscript)
    

#prepareOnce()

testEnvironments={}
testEnvironments["tenv159"]=TestEnv("10.100.159.253",["10.100.159.251","10.100.159.252"],"rooter")
testEnvironments["tenv160"]=TestEnv("10.100.159.253",["10.100.159.251","10.100.159.252"],"rooter")

executeOn=["tenv159","tenv160"]



for tenvName in executeOn:
    tenv=testEnvironments[tenvName]
    clMaster=q.cluster.create("ssotestmaster","ssotest",[tenv.masterip],tenv.passwd)    
    for node in  tenv.nodeIps:
        nodeips.append(nodeip)
    clNodes=q.cluster.create("ssotestnodes","ssotest",nodeips,tenv.passwd)    
    print getSmartInfo(clMaster)
    


ipshell()

q.application.stop()


