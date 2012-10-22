from pylabs import q

import sys
import os
import signal
import traceback

DAEMON = q.system.fs.joinPaths(q.system.fs.getDirName(__file__), "event_consumer_daemon.py")
PIDDIR = q.system.fs.joinPaths(q.dirs.pidDir, 'event_consumers')

def buildCmd(appName):
    cmd = [
        sys.executable,
        DAEMON,
        appName
    ]
    return cmd

class EventConsumerMgr:
    def __init__ (self, appName):
        q.system.fs.createDir(PIDDIR)
        self._appName = appName
        self._pidfile = q.system.fs.joinPaths(PIDDIR, "%s.pid" % appName)

        # user and group used to start the applicationserver
        config = q.config.getConfig('main').get('main', {})
        self.user = config.get('user')
        self.group = config.get('group')

        if q.platform.isUnix():
            if self.user and self.group:
                # change ownership of the pid dir
                q.system.unix.chown(PIDDIR, self.user, self.group)

    def _savePid(self, pid):
        q.system.fs.writeFile(self._pidfile, str(pid))

        if q.platform.isUnix():
            if self.user and self.group:
                # change ownership of the file
                q.system.unix.chown(self._pidfile, self.user, self.group)

    def _isRunning(self):
        if not q.system.fs.exists(self._pidfile):
            return False
        pid = q.system.fs.fileGetContents(self._pidfile)
        return q.system.process.isPidAlive(int(pid))

    def start(self):
        if self._isRunning():
            pid = q.system.fs.fileGetContents(self._pidfile)
            q.logger.log("Event consumer daemon with PID %s is already running" % pid)
            return
        pid = q.system.process.runDaemon(" ".join(buildCmd(self._appName)), user=self.user, group=self.group)
        self._savePid(pid)

    def stop(self):
        if not self._isRunning():
            return
        pid = q.system.fs.fileGetContents(self._pidfile)
        if pid.isdigit():
            q.logger.log("Terminating event consumer with PID %s" % pid, 7)
            try:
                os.kill(int(pid), signal.SIGTERM)
            except OSError:
                t = traceback.format_exc()
                q.logger.log("Failed to kill event consumer with PID %s: %s" % (pid, t), 3)
        else:
            q.logger.log("PID in PID file %s is not a digit" % self._pidfile, 3)
        q.system.fs.removeFile(self._pidfile)

    def restart(self):
        self.stop()
        self.start()

