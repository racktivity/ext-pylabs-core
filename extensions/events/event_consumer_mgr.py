from pylabs import q
from events import MULTICONSUME_NAME

import sys
import os
import signal
import traceback

event_consumer = q.system.fs.joinPaths(q.system.fs.getDirName(__file__), "event_consumer.py")

def buildCmd(bindingKey, workPoolDir, queueName, appName):
    cmd = [
        sys.executable,
        event_consumer,
        queueName,
        bindingKey,
        workPoolDir,
        appName
    ]
    return cmd

class EventConsumerMgr:
    def __init__ (self, appName, baseDir):
        self.piddir = q.system.fs.joinPaths(q.dirs.pidDir, 'event_consumers', q.tools.hash.md5_string(baseDir))
        q.system.fs.createDir(self.piddir)
        self._appName = appName
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
            bindingKey = cfgFile.getValue('main', 'eventKey')
            queueName = q.tools.hash.md5_string(workerPool)
            if cfgFile.checkParam('main', 'multiconsume') and cfgFile.getBooleanValue('main', 'multiconsume'):
                queueName = MULTICONSUME_NAME #make it MULTICONSUME_NAME so multiple consumers can each process the events
            cmd = buildCmd(bindingKey, workerPool, queueName, self._appName)
            for i in xrange(workers):
                pid = q.system.process.runDaemon(" ".join(cmd))
                self._savePid(pid, workerPool, i)

    def stop(self):
        for pidfile in q.system.fs.listFilesInDir(self.piddir):
            pid = q.system.fs.fileGetContents(pidfile)
            if pid.isdigit():
                q.logger.log("Terminating event consumer with PID %s" % pid, 7)
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except OSError:
                    t = traceback.format_exc()
                    q.logger.log("Failed to kill event consumer with PID %s: %s" % (pid, t), 3)
            else:
                q.logger.log("PID in PID file %s is not a digit" % pidfile, 3)
            q.system.fs.removeFile(pidfile)


if __name__ == '__main__' :
    from pylabs.InitBase import q
    cmdArgs = sys.argv
    if len(cmdArgs) != 2:
        raise RuntimeError("Usage: event_consumer_mgr.py pylabs_workers_base_dir")

    mgr = EventConsumerMgr( cmdArgs[1] )
    mgr.start()
