import os
from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.enumerators import AppStatusType
import time

class NginxCmd(CommandWrapper):
    """
    Nginx cmdtools SAL extension.
    """

    def __init__(self):
        self._basecmd = q.system.fs.joinPaths(os.sep, 'etc', 'init.d', 'nginx')
        self._status_cmd   = '%s %s' %(self._basecmd, 'status')
        self._start_cmd    = '%s %s' %(self._basecmd, 'start')
        self._stop_cmd     = '%s %s' %(self._basecmd, 'stop')
        self._restart_cmd  = '%s %s' %(self._basecmd, 'restart')
        self._reload_cmd  = '%s %s' %(self._basecmd, 'reload')
        self._configtest_cmd  = '%s %s' %(self._basecmd, 'configtest')
        self._pidfilepath = q.system.fs.joinPaths(os.sep, 'var', 'run', 'nginx.pid')
        self._configFilePath = q.system.fs.joinPaths(os.sep, 'etc', 'nginx', 'nginx.conf')

    def getStatus(self):
        """
        Retrieve the status of Nginx service.

        @return Running, Halted or Unknown.
        @rtype AppStatusType.
        """
        try:
            exitcode, output = q.system.process.execute(self._status_cmd, outputToStdout=False)
            if exitcode == os.EX_OK and output.find('* nginx is running') != -1:
                return AppStatusType.RUNNING
        except:
            ex_string = q.errorconditionhandler.getCurrentExceptionString()
            if ex_string.find('* could not access PID file for nginx') != -1:
                return AppStatusType.HALTED

            raise

        return AppStatusType.UNKNOWN

    def start(self, timeout=30):
        """
        Start Nginx server.

        @param timeout: Time in seconds within which Nginx server should be started.
        @type timeout:  integer.
        @return True if Nginx server started successfully, False or raises an exception otherwise.
        """
        if self.getStatus() == AppStatusType.RUNNING:
            q.gui.dialog.message('Nginx is already running.')
            return False

        if self.getStatus() == AppStatusType.UNKNOWN:
            q.gui.dialog.message('Nginx seems to be crashed. Check with admin please.')
            return False

        q.gui.dialog.message('Nginx is starting...')
        exitcode, output = q.system.process.execute(self._start_cmd, outputToStdout=False)
        t = timeout
        started = False
        while t > 0:
            if q.system.fs.exists(self._getPifFilePath()):
                pid = int(q.system.fs.fileGetContents(self._getPifFilePath()))
                if q.system.process.isPidAlive(pid):
                    if q.system.process.checkProcess('nginx') == 0:
                        started = True
                        break
            t = t - 1
            time.sleep(1)

        if not started:
            q.errorconditionhandler.raiseError('Nginx (pidfile [%s]) could not be started in %d seconds.' %(self._getPifFilePath(), timeout))

        q.gui.dialog.message('Nginx started successfully.')
        return True

    def stop(self, timeout=30):
        """
        Stop Nginx server.

        @param timeout: Time in seconds within which Nginx server should be halted.
        @type timeout:  integer.
        @return True if Nginx server halted successfully, False or raises an exception otherwise.
        """
        if self.getStatus() == AppStatusType.HALTED:
            q.gui.dialog.message('Nginx is already halted.')
            return False

        if self.getStatus() == AppStatusType.UNKNOWN:
            q.gui.dialog.message('Nginx seems to be crashed. Check with admin please.')
            return False

        q.gui.dialog.message('Nginx is halting...')
        exitcode, output = q.system.process.execute(self._stop_cmd, outputToStdout=False)
        t = timeout
        halted = False
        while t > 0:
            if not q.system.fs.exists(self._getPifFilePath()):
                if q.system.process.checkProcess('nginx'):
                    halted = True
                    break

            t = t - 1
            time.sleep(1)

        if not halted:
            q.errorconditionhandler.raiseError('Nginx (pidfile [%s]) could not be halted in %d seconds.' %(self._getPifFilePath(), timeout))

        q.gui.dialog.message('Nginx halted successfully.')
        return True

    def restart(self, timeout=30):
        """
        Restart Nginx server.

        @param timeout: Time in seconds within which Nginx server should be restarted.
        @type timeout:  integer.
        @return True if Nginx server restarted successfully, False or raises an exception otherwise.
        """
        self.stop(timeout)
        return self.start(timeout)

    def reload(self):
        """
        Reload Nginx server configuration.

        @return True if Nginx server configuration reloaded successfully, False or raises an exception otherwise.
        """
        q.gui.dialog.message('Relaoding Nginx server configuration...')
        exitcode, output = q.system.process.execute(self._reload_cmd, outputToStdout=False)
        if os.EX_OK == exitcode:
            q.gui.dialog.message('Nginx server configuration reloaded successfully.')
            return True

        q.errorconditionhandler.raiseError(output)

    def configtest(self):
        """
        Test Nginx server configuration.

        @return True if Nginx server configuration is correct, False otherwise.
        """
        try:
            q.gui.dialog.message('Nginx configuration testing started...')
            q.system.process.execute(self._configtest_cmd, outputToStdout=False)
            q.gui.dialog.message('Nginx configuration testing done successfully.')
        except:
            exc_string = q.eventhandler.getCurrentExceptionString()
            q.gui.dialog.message('Nginx configuration testing done with errors...')
            q.gui.dialog.message("Configuration file ['%s'] has syntax errors." %self._configFilePath)
            q.logger.log('Error received: %s.' %exc_string, 3)
            q.logger.log("Error executing ['%s']." %self._configtest_cmd, 3)
            return False

        return True

    def _getPifFilePath(self):
        return self._pidfilepath

    def _getConfigFilePath(self):
        return self._configFilePath
