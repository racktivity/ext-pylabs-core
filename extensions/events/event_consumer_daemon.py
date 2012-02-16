from pylabs.InitBase import q, p
import event_consumer
import sys
import os
import signal
import event_consumer

#import the next modules here although not used, so when forked, python doesn't reimport for child processes (become shared)
import rabbitmqclient as rmq
from events import EXCHG_NAME, EXCHG_TYPE, MULTICONSUME_NAME
from functools import wraps
import traceback

def main(appname):
    #initialize API
    p.api = p.application.getAPI(appname)
    p.api.model = p.application.getAPI(appname, context=q.enumerators.AppContext.APPSERVER).model
    host = p.application.getRabbitMqHost(appname)
    pids = []
    workersPool = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "impl", "events")
    
    for workerPool in q.system.fs.listDirsInDir(workersPool):
        workerName = q.system.fs.getBaseName(workerPool)
        cfgFilePath = q.system.fs.joinPaths(workerPool, "consumer.cfg")
        if not q.system.fs.exists(cfgFilePath):
            continue
        
        cfgFile = q.tools.inifile.open(cfgFilePath)
        workers = cfgFile.getIntValue('main', 'workers')
        bindingKey = cfgFile.getValue('main', 'eventKey')
        queueName = q.tools.hash.md5_string(workerPool)
        multiconsumer = cfgFile.checkParam('main', 'multiconsume') and cfgFile.getBooleanValue('main', 'multiconsume')
        #multiconsumers do not require multiple works and should as events will be processed multiple times on same node
        if multiconsumer:
            workers = 1
        for i in xrange(workers):
            consumer = event_consumer.EventConsumer(queueName, bindingKey, workerPool, host, multiconsumer)
            pid = os.fork()
            if pid == 0:
                #child
                q.application.appname = "../%s/eventconsumer/%s" % (appname, workerName)
                q.application.start()
                consumer.consume()
                exit(0)
            else:
                pids.append(pid)
    
    def shutdown(sig, sf):
        for pid in pids:
            os.kill(pid, sig)
    
    for sig in (signal.SIGTERM, signal.SIGQUIT):
        signal.signal(sig, shutdown)
    
    #wait for children
    while pids:
        try:
            pid, sigstatus = os.wait()
            if pid in pids:
                q.logger.log("Consumer of PID: %d has been killed" % pid)
                pids.remove(pid)
        except Exception, e:
            q.logger.log("Event consumer for app '%s' died for an unknown reason: %s" % (appname, e))
            shutdown(signal.SIGTERM, None)
        
if __name__ == "__main__":
    main(sys.argv[1])