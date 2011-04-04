from pylabs import q

import sys
import os
import signal

event_consumer = q.system.fs.joinPaths(q.system.fs.getDirName(__file__), "event_consumer.py")

def buildCmd(bindingKey, workPoolDir, queueName):
    cmd = [
        sys.executable,
        event_consumer,
        queueName,
        bindingKey,
        workPoolDir ]
    return cmd

class EventConsumerMgr:
    def __init__ (self, baseDir):
        
        self.piddir = q.system.fs.joinPaths(q.dirs.pidDir, 'event_consumers', q.tools.hash.md5_string(baseDir))
        q.system.fs.createDir(self.piddir)
        self._workerPools = q.system.fs.listDirsInDir(baseDir)

    def _savePid(self, pid, workerPool, idx):
        name = "%s_%d.pid" % (q.system.fs.getBaseName(workerPool), idx)
        file_ = q.system.fs.joinPaths(self.piddir, name)
        q.system.fs.writeFile(file_, str(pid))
        

    def start(self):
        for workerPool in self._workerPools:
            cfgFilePath = q.system.fs.joinPaths(workerPool, "consumer")
            cfgFile = q.config.getInifile( cfgFilePath )
            workers = cfgFile.getIntValue('main', 'workers')
            bindingKey = cfgFile.getValue('main','eventKey')
            queueName = q.tools.hash.md5_string(workerPool)
            cmd = buildCmd(bindingKey, workerPool, queueName)
            for i in xrange(workers):
                pid = q.system.process.runDaemon(" ".join(cmd))
                self._savePid(pid, workerPool, i)
    
    def stop(self):
        for pidfile in q.system.fs.listFilesInDir(self.piddir):
            pid = q.system.fs.fileGetContents(pidfile)
            if pid.isdigit():
                os.kill(int(pid), signal.SIGTERM)
            q.system.fs.removeFile(pidfile)
        


if __name__ == '__main__' :
    from pylabs.InitBase import q
    cmdArgs = sys.argv
    if len(cmdArgs) != 2:
        raise RuntimeError("Usage: event_consumer_mgr.py pylabs_workers_base_dir")

    mgr = EventConsumerMgr( cmdArgs[1] ) 
    mgr.start()
