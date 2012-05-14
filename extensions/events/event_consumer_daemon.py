from pylabs.InitBase import q, p
import event_consumer
import sys
import os
import signal
import event_consumer
import time

#import the next modules here although not used, so when forked, python doesn't reimport for child processes (become shared)
import rabbitmqclient as rmq
from events import EXCHG_NAME, EXCHG_TYPE, MULTICONSUME_NAME
from functools import wraps
import traceback

respawn = True

def main(appname):
    global respawn
    #initialize API
    p.api = p.application.getAPI(appname, context=q.enumerators.AppContext.EVENT)
    globalhost = p.application.getRabbitMqHost(appname)
    pids = {}
    workersPool = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "impl", "events")
    
    class Spawn:
        NOTRUNNING = 5
        MAXWAIT = 60
        WAITTIME = 3

        def __init__(self, appname, workername, args):
            self.appname = appname
            self.workername = workername
            self.args = args
            self.pid = None
            self.starttime = None
            self.retry = 0
    
        def sleep(self):
            now = time.time()
            if not self.starttime:
                return
            if now - self.starttime < self.NOTRUNNING:
                self.retry += 1
                sleeptime = self.retry * self.WAITTIME
                sleeptime = sleeptime if sleeptime < self.MAXWAIT else self.MAXWAIT
                time.sleep(sleeptime)
            else:
                self.retry = 0
 
        def start(self):
            self.sleep()
            self.starttime = time.time()
            pid = os.fork()
            if pid == 0:
                #child
                #restore default handler for child process so it doesn't try to do shutdown.
                for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
                    signal.signal(sig, signal.SIG_DFL)
                consumer = event_consumer.EventConsumer(*self.args)
                q.application.appname = "../%s/eventconsumer/%s" % (self.appname, self.workername)
                q.application.start()
                try:
                    consumer.consume()
                except Exception, e:
                    q.logger.log("Consumer process died: %s" % e)
                finally:
                    q.application.stop(0)
                os.exit(0)
                
            self.pid = pid
    
    for workerPool in q.system.fs.listDirsInDir(workersPool):
        workerName = q.system.fs.getBaseName(workerPool)
        cfgFilePath = q.system.fs.joinPaths(workerPool, "consumer.cfg")
        if not q.system.fs.exists(cfgFilePath):
            continue
        
        cfgFile = q.tools.inifile.open(cfgFilePath)
        workers = cfgFile.getIntValue('main', 'workers')
        bindingKey = cfgFile.getValue('main', 'eventKey')
        queueName = q.tools.hash.md5_string(workerPool)
        host = globalhost
        if cfgFile.checkSection('server'):
            host = cfgFile.getValue('server', 'host')
        multiconsumer = cfgFile.checkParam('main', 'multiconsume') and cfgFile.getBooleanValue('main', 'multiconsume')
        #multiconsumers do not require multiple works and should as events will be processed multiple times on same node
        if multiconsumer:
            workers = 1
        
        for i in xrange(workers):
            args = (queueName, bindingKey, workerPool, host, multiconsumer)
            worker = Spawn(appname, workerName, args)
            worker.start()
            pids[worker.pid] = worker
    
    def shutdown(sig, sf):
        global respawn
        respawn = False
        for pid in pids:
            os.kill(pid, sig)
    
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
        signal.signal(sig, shutdown)
    
    #wait for children
    while pids:
        try:
            pid, sigstatus = os.wait()
            if pid in pids:
                msg = "Consumer of PID: %d has been killed" % pid
                q.logger.log(msg)
                worker = pids.pop(pid)
                if respawn:
                    worker.start()
                    pids[worker.pid] = worker
                    
        except Exception, e:
            msg = "Event consumer for app '%s' died for an unknown reason: %s" % (appname, e)
            q.logger.log(msg)
            shutdown(signal.SIGTERM, None)
            
if __name__ == "__main__":
    main(sys.argv[1])
