from pylabs import q
import time
import sys
import signal

_join = q.system.fs.joinPaths

APPNAME = "oauthservice"
EXECUTABLE = "server.py"
LOG_DIR = _join(q.dirs.varDir, "log", APPNAME)
PID_FILE = _join(q.dirs.varDir, "pid", "%s.pid" % APPNAME)
PROCESS_FILE = _join(q.dirs.appDir, APPNAME, EXECUTABLE)
    
class OAuthServiceCMDTools(object):
    def start(self, timeout=5):
        """
        Starts the OAuth service
        
        @param timout: number of seconds to wait before reporting failing to start the server
        @type timeout: integer
        
        @return: True if success False otherwise  
        """
        if not q.system.fs.isDir(LOG_DIR):
            q.system.fs.createDir(LOG_DIR)
        
        if self.isRunning():
            return (0, "OAuth service already running")
        
        cmd = "%(exec)s %(process)s -p %(pid)s" % {"exec": sys.executable,
                                                                        "process": PROCESS_FILE,
                                                                        "pid" : PID_FILE}
        
        q.system.process.runDaemon(cmd,
                                   stdout = _join(LOG_DIR, "stdout.log"),
                                   stderr = _join(LOG_DIR, "stderr.log"))
        while timeout:
            if self.isRunning():
                return (0, "OAuth service has been started successfully")
            time.sleep(1)
            timeout -= 1
        
        return (1, "OAuth service failed to start, please check the logs under '%s'" % LOG_DIR)
    
    def stop(self, timeout=5):
        """
        Stops the OAuth service 
        @param timeout: number of seconds to wait before trying to kill the OAuth service process abruptly
        @type timeout: integer
        """
        if not self.isRunning():
            return (0, "OAuth service is already stopped")
        
        q.system.process.kill(self._getPID(), signal.SIGTERM)
        
        while timeout:
            if not self.isRunning():
                return (0, "OAuth service has been stopped successfully")
            time.sleep(1)
            timeout -= 1
        
        q.system.process.kill(self._getPID(), signal.SIGKILL)
        return (0, "OAuth service has been forced to die")

    def _getPID(self):
        if not q.system.fs.isFile(PID_FILE):
            return 0
        return int(q.system.fs.fileGetContents(PID_FILE).strip())
    
    def restart(self, timeout=5):
        """
        Restart the OAuth service
        """
        self.stop(timeout)
        self.start(timeout)

    def isRunning(self):
        """
        Get the status of the OAuth service
        """
        pid = self._getPID()
        if pid:
            return not bool(q.system.process.checkProcessForPid(pid, "python"))
        return False
    
    def getStatus(self):
        return q.enumerators.AppStatusType.RUNNING if self.isRunning() else q.enumerators.AppStatusType.HALTED