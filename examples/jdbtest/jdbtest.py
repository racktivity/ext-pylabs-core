from pymonkey.InitBase import *
from pymonkey.Shell import *

q.application.appname = "jdbtest"
q.application.start()

start=q.base.time.getTimeEpoch()
newnamespace=False
namespacename="test2"
total=1000000
startnr=total*1
nrsec=0
passwd="xxx"

if newnamespace:
    q.jdb.client.removeNamespace(namespacename,"1111")
    q.jdb.client.addNamespace(namespacename,"1111")
    
for t in range(startnr,total+startnr):
    q.jdb.client.put(namespacename,passwd,"%s" % t,"%s" % t)
    if (t+0.0)/1000 == round((t)/1000):
        now=q.base.time.getTimeEpoch()
        if now-start<>0:
            nrsec=round((t-startnr)/(now-start),0)
            lastnrsec=nrsec
        print "nritems:%s nrpersecavg:%s" % (t, nrsec)
        previous=now
print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"

start=q.base.time.getTimeEpoch()        
iterator=q.jdb.client.listKeys(namespacename,passwd)
for t in range(startnr,total+startnr):
    key=iterator.pop()
    if q.jdb.client.get(namespacename,passwd,key).value<> "%s" % key:
        raise "error in DB for key %s with value %s" % (key,q.jdb.client.get("test","kds007",key).value)
    if (t+0.0)/1000 == round((t)/1000):
        now=q.base.time.getTimeEpoch()
        if now-start<>0:
            nrsec=round((t-startnr)/(now-start),0)
        print "nritems:%s nrpersecavg:%s" % (t, nrsec)
        previous=now
    
print "performance of last import %s " % lastnrsec

q.application.stop()
