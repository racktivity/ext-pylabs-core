from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.enumerators import AppStatusType
import os
import signal
import time

EJABBERDCTL = q.system.fs.joinPaths(os.sep,'usr','sbin', 'ejabberdctl')
EJABBERD = q.system.fs.joinPaths(os.sep,'usr','sbin', 'ejabberd')
class EjabberdCtl(CommandWrapper):

    def start(self, nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        errorMessage = 'Failed to start EJabberd'
        if self.getStatus(nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir) is AppStatusType.RUNNING:
            q.logger.log("Start aborted! EJabberd already running", 2)
            return 1, "EJabberd already running"

        cmd = self._formCommand(EJABBERD, '-noshell -detached', nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir)

        try:
            q.logger.log('Starting jabber server', 1)
            q.logger.log('Executing command [%s]'%cmd, 4)
            status, stdout, stderr = q.system.process.run(cmd, stopOnError=False)
            if status != 0:
                q.logger.log("Error executing ['%s'] - output %s" % (cmd, stdout), 3)
                return 1, stdout

            times = 10
            while times > 0 and q.enumerators.AppStatusType.RUNNING != self.getStatus(nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir, True):
                time.sleep(1)
                times = times - 1

            if times == 0:
                self.getStatus(nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir)
                return 1, "Start executed successfully but server not available"
        except:
            exc = q.eventhandler.getCurrentExceptionString()
            q.logger.log("Error received: %s" %exc, 4)
            q.logger.log("Error executing ['%s']" %cmd, 3)
            return 1, errorMessage

    def stop(self, nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        errorMessage = 'Failed to stop EJabberd'
        if self.getStatus(nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir) != AppStatusType.RUNNING:
            q.logger.log("Stop aborted! EJabberd is not running", 2)
            return 1, "EJabberd is not running"

        cmd = self._formCommand(EJABBERDCTL, 'stop', nodeName )
        q.logger.log("Executing [%s]"%cmd, 5)
        q.logger.log('Stopping jabber server', 2)
        try:
            status, stdout, stderr = q.system.process.run(cmd, stopOnError=False)
            if status != 0:
                q.logger.log("Error executing ['%s'] - output %s" % (cmd, stdout), 3)
                return 1, stdout
        except Exception, ex:
            q.logger.log("Error executing ['%s']: %s" % (cmd, ex), 3)
            return 1, errorMessage

        timeout = 60
        while timeout > 0 and self.getStatus() is AppStatusType.RUNNING:
            q.logger.log("Waiting for EJabberd to stop...", 5)
            time.sleep(1)
            timeout -= 1

        if timeout > 0:
            q.logger.log("EJabberd stopped.", 2)
            return 0, "EJabberd stopped"
        else:
            q.logger.log("Timed out [%s] seconds, while stopping EJabberd" % timeout, 3)
            return 1, errorMessage

    def getStatus(self, nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir="", starting=False):
        """
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        q.logger.log('Checking status of ejabberd', 3)
        cmd = self._formCommand(EJABBERDCTL, 'status', nodeName)
        status, stdout, stderr = q.system.process.run(cmd, stopOnError=False)
        if not status:
            return AppStatusType.RUNNING
        else:
            if not starting:
                for pid in q.system.process.getProcessPid('ejabberd'):
                    os.kill(int(pid), signal.SIGTERM)

            return AppStatusType.HALTED

    def restart(self, nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        self.stop(nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir)
        self.start(nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir)

    def register(self, user, server, password, nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        Register user with password at ejabberd virtual host server.

        @param user: name of the user to register
        @param server: name of the server to add the user to
        @param password: password of the user to register
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        params = {'User':user, 'Server':server, 'Password':password}
        self._checkParams(params)
        cmd = self._formCommand(command='register "%s" "%s" "%s"'%(user, server, password), nodeName=nodeName)
        exitCode, output = q.system.process.execute(cmd, outputToStdout=False)
        if exitCode != 0:
            q.logger.log("Error executing [%s] - output %s" % (cmd), 3)
            return 1, output

    def unregister(self, user, server, nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        Unregister user at ejabberd virtual host server.

        @param user: name of the user to unregister
        @param server: name of the server to unregister the user from
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        params = {'User':user, 'Server':server}
        self._checkParams(params)
        cmd = self._formCommand(command='unregister "%s" "%s"'%(user, server), nodeName=nodeName)

        exitCode, output = q.system.process.execute(cmd, outputToStdout=False)
        if exitCode != 0:
            q.logger.log("Error executing ['%s'] - output %s" % (cmd, output), 3)
            return 1, output

    def dump(self, dirPath=q.system.fs.joinPaths(q.dirs.varDir, 'ejabbered'), nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        Dump user database of the ejabberd server to text file filepath.

        @param dirPath: Directory path to dump user database at
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        if not q.system.fs.exists(dirPath):
            q.system.fs.createDir(dirPath)
        print '**************IN DUMP**********'
        dumpFile = q.system.fs.joinPaths(dirPath, 'dump.txt')
        cmd = self._formCommand(command='dump %s'%(dumpFile), nodeName=nodeName)
        exitCode, output = q.system.process.execute(cmd,outputToStdout=False)
        return q.system.fs.fileGetContents(dumpFile)

    def listRegisteredUsers(self, host, nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        List all registered users in host
        @param host: host to list registered users
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        cmd = self._formCommand(command='registered_users %s'%host, nodeName=nodeName)
        exitCode, users = q.system.process.execute(cmd, outputToStdout=False)
        return users.splitlines()

    def isRegistered(self, name, server, nodeName='', cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        check if user is already registered

        @param user: name of the user to register
        @param server: name of the server to add the user to
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        users = self.listRegisteredUsers(server, nodeName, cfgFile, ctlCfgFile, logsDir, spoolDir)
        return str(name) in users

    def listConnectedUsers(self,  nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        """
        Retrieves a list of all users connected to the server
        @param nodeName: a remote node
        @param cfgFile: Config file of ejabberd
        @param ctlCfgFile: file includes detailed information about each configurable option.
        @param logsDir: directory for the logs
        @param spoolDir: Database spool dir
        """
        cmd = self._formCommand(command='connected_users', nodeName = nodeName)
        exitCode, connectedUsers = q.system.process.execute(cmd, outputToStdout=False)
        return connectedUsers.splitlines()

    def _formCommand(self, ejabberdctl=EJABBERDCTL, command="", nodeName="", cfgFile="", ctlCfgFile="", logsDir="", spoolDir=""):
        options = {'--node':nodeName, '--config':cfgFile, '--ctl-config':ctlCfgFile, '--logs':logsDir, '--spool':spoolDir}
        
        for option, value in options.iteritems():
            if value:
                ejabberdctl += ' %s "%s"'%(option, value)

        ejabberdctl += ' %s'%command
        return ejabberdctl

    def _checkParams(self, params):
        for param, value in params.iteritems():
            if not value:
                raise ValueError('%s can not be None or empty string'%param)



