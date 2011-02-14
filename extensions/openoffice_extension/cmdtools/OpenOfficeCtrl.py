from pymonkey import q
from pymonkey.baseclasses.CommandWrapper import CommandWrapper
from pymonkey.enumerators import AppStatusType
import os
import signal

OPENOFFICECTRL = 'soffice -accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" -norestore -nofirstwizard -nologo -headless'

class OpenOfficeCtrl(CommandWrapper):
    
    name = 'openoffice'

    def start(self, timeout=5):
        """
        Starts Open Office
        @return: 0 if success 1 otherwise
        """
        errorMessage = 'Failed to start %s' % self.name

        if self.getStatus() is AppStatusType.RUNNING:
            q.logger.log("Start aborted! %s is already running" % self.name, 2)
            return 0, "%s already running" % self.name

        try:
            q.logger.log('Starting %s' % self.name, 1)
            q.logger.log('Executing command %s' % OPENOFFICECTRL, 3)

            pid = q.system.process.runDaemon(OPENOFFICECTRL)
            if not q.system.process.isPidAlive(pid):
                q.logger.log("Error executing ['%s']- check %s logs found in %s" % (OPENOFFICECTRL, q.system.fs.joinPaths(q.dirs.logDir, self.name), self.name), 1)
                return 1, 'Failed to start %s' % self.name
            else:
                pidfile = self._getPidFile()
                q.system.fs.writeFile(pidfile, str(pid))

            times = timeout
            import time
            while times > 0 and q.enumerators.AppStatusType.RUNNING != q.manage.openoffice.getStatus():
                time.sleep(1)
                times = times - 1

            if times == 0:
                return 1, "Start executed successfully but server not available"
        except:
            exc = q.eventhandler.getCurrentExceptionString()
            q.logger.log("Error received: %s" % exc, 2)
            return 1, errorMessage + exc

        return 0, '%s started successfully' % self.name

    def stop(self, timeout=5):
        """
        Stops Open Office
        """
        errorMessage = 'Failed to stop %s' % self.name
        if self.getStatus() != AppStatusType.RUNNING or not self._getPid():
            q.logger.log("Stop aborted! %s is not running" % self.name, 2)
            return 0, "%s is not running" % self.name

        q.logger.log('Stopping %s' % self.name, 2)
        pid = self._getPid()
        try:
            os.kill(pid, signal.SIGTERM)
            q.logger.log('%s stopped' % self.name, 2)
            q.system.fs.removeFile(self._getPidFile())
            return 0, '%s Stopped' % self.name
        except Exception, e:
            q.logger.log("Error killing process %s\n %s" % (self.name, str(e)), 3)
            return 1, errorMessage + str(e)

        while timeout > 0 and self.getStatus() is AppStatusType.RUNNING:
            q.logger.log("waiting on Open Office to stop running...", 5)
            time.sleep(1)
            timeout -= 1

        if timeout > 0:
            q.logger.log("Open Office stopped.", 2)
            return 0, "Open Office stopped"
        else:
            q.logger.log("Timed out [%s] seconds, while stopping Open Office" % timeout, 3)
            return 1, errorMessage

        if q.system.process.isPidAlive(pid):
            q.system.process.run('kill %s' % pid)

    def getStatus(self):
        """
            Get the status of Open Office
        """
        pid = self._getPid()
        if pid:
            if q.system.process.isPidAlive(pid):
                return AppStatusType.RUNNING
        return AppStatusType.HALTED

    def restart(self, timeout=5):
        """
        Restart Open Office
        @param timeout: number of seconds to wait before trying to kill the open office process abruptly
        @type timeout: integer
        """
        self.stop(timeout)
        self.start()

    def _getPidFile(self):
        return q.system.fs.joinPaths(q.dirs.pidDir, 'openoffice.pid')

    def _getPid(self):
        pid = None
        pidfile = self._getPidFile()
        if q.system.fs.isFile(pidfile):
            pid = q.system.fs.fileGetContents(pidfile)
            pid = int(pid)
        return pid
