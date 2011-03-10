from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.db.DBConnection import DBConnection
from pylabs.enumerators import AppStatusType
import time, re, os

class PostgresqlControl(CommandWrapper):

    def __init__(self, configFile=None, dataDir = None):
        self._configFileDir = dataDir and dataDir or q.system.fs.joinPaths(os.sep, 'etc', 'postgresql', '8.4', 'main')
        self._serviceName = "pgsql-8.4"
        self._pgLogFile = q.system.fs.joinPaths(os.sep, 'var', 'log', 'postgresql', 'postgresql-8.4-main.log')
        self._binDir = q.system.fs.joinPaths(os.sep, 'usr', 'lib', 'postgresql', '8.4', 'bin')
        self._daemon = q.system.fs.joinPaths(self._binDir, 'pg_ctl')
        self._clibPath = q.system.fs.joinPaths(q.dirs.baseDir, 'lib')
        self._SKEL = "LD_LIBRARY_PATH=%s; export LD_LIBRARY_PATH; " % self._clibPath

    def start(self, username = 'postgres', dataDir = None):
        """
        Starts the PostgreSQL server using the specified user credentials

        @param username: username to use when starting the server
        @param  dataDir: data directory used to initialize system databases
        """

        exitCode, output, result = None, None, None
        q.logger.log("Starting [%s]"%self._serviceName, 1)

        if self.getStatus(username, self._configFileDir) == AppStatusType.RUNNING:
            q.logger.log("The service [%s] is already running"%self._serviceName, 1)
            return

        if q.platform.isWindows():
            result = q.system.windows.startService(self._serviceName)

        elif q.platform.isLinux():
            commandString = "%s start -D '%s' -w -l '%s' -o -i" % (self._daemon, self._configFileDir, self._pgLogFile)
            q.system.process.runDaemon(commandline = commandString, user = username)

        elif q.platform.isSolaris():
            commandString = "%s %s start -D '%s' -s -l '%s' -o -i" % (self._SKEL, self._daemon, self._configFileDir, self._pgLogFile)
            q.system.process.runDaemon(commandline = commandString, user = username)

        counter = 0
        maxWait = 30
        while(self.getStatus(username, dataDir) != AppStatusType.RUNNING and counter < maxWait):
            time.sleep(1)
            counter+=1

        if counter == maxWait and self.getStatus(username, dataDir) != AppStatusType.RUNNING:
            raise RuntimeError,"Server [%s] couldn't be started"%self._serviceName
        else:
            q.console.echo("Server [%s] is started"%self._serviceName)

    def stop(self, username = 'postgres', dataDir = None):
        """
        Stops the PostgreSQL server using the specified user credentials

        @param username: username to use when stopping the server
        @param  dataDir: data directory used to initialize system databases
        """

        q.logger.log("Stopping [%s]"%self._serviceName)

        if self.getStatus(username, self._configFileDir) == AppStatusType.HALTED:
            q.logger.log("The service [%s] is not running"%self._serviceName)
            return

        exitCode, output, result = None, None, None
        if q.platform.isWindows():
             result = q.system.windows.stopService(self._serviceName)

        elif q.platform.isLinux():
            commandString = "%s stop -D '%s' -s -m fast" % (self._daemon, self._configFileDir)
            exitCode, output = q.system.unix.executeAsUser(command = commandString, username = username, dieOnNonZeroExitCode = False)

        elif q.platform.isSolaris():
            commandString = "%s %s stop -D '%s' -s -m fast" % (self._SKEL, self._daemon, self._configFileDir)
            exitCode,output = q.system.unix.executeAsUser(command = commandString, username = username, dieOnNonZeroExitCode = False)

        if exitCode and exitCode != None or not result and result != None:
            raise RuntimeError, "stopping Server [%s] failed with error %s"%(self._serviceName,output)

        counter = 0
        maxWait = 30

        while(self.getStatus(username, dataDir) != AppStatusType.HALTED and counter < maxWait):
            time.sleep(1)
            counter+=1

        time.sleep(1)

        if counter == 10 and self.getStatus(username, dataDir) != AppStatusType.HALTED:
            raise RuntimeError,"Server [%s] couldn't be stopped"%self._serviceName
        else:
            q.console.echo("Server [%s] is stopped"%self._serviceName)

    def reload(self, username='postgres', dataDir = None):
        """
        Reloads the PostgreSQL server using the specified user credentials

        @param username: username to use when stopping the server
        @param  dataDir: data directory used to initialize system databases
        """

        q.logger.log("Reloading [%s]" % self._serviceName)

        exitCode, output, result = None, None, None

        if q.platform.isWindows():
             raise NotImplementedError("Postgres reload is not implemented on Windows")

        elif q.platform.isLinux():
            commandString = "%s reload -D '%s' -s" % (self._daemon, self._configFileDir)
            exitCode, output = q.system.unix.executeAsUser(command = commandString, username = username, dieOnNonZeroExitCode = False)

        elif q.platform.isSolaris():
            commandString = "%s %s reload -D '%s' -s" % (self._SKEL, self._daemon, self._configFileDir)
            exitCode,output = q.system.unix.executeAsUser(command = commandString, username = username, dieOnNonZeroExitCode = False)

        if exitCode and exitCode != None or not result and result != None:
            raise RuntimeError, "Reloading Postgresql Server [%s] failed with error %s"%(self._serviceName,output)

    def getStatus(self, username='postgres', dataDir = None):
        """
        Retrieves the PostgreSQL server status using the specified user credentials

        @param username: username to use when retrieving the status of the server
        @param  dataDir: data directory used to initialize system databases
        """

        if q.system.process.checkListenPort(5432): # 0 if running, 1 if not running
            return AppStatusType.HALTED
        try:
            dbCon = DBConnection('127.0.0.1', 'postgres', username)
            result = dbCon.sqlexecute("select datname from pg_database;")
        except Exception, e:
            q.logger.log("The following exception occurred while checking the postgres status.", 5)
            q.logger.log("Exceptions are nothing to worry about if the database is not running.", 5)
            q.logger.log(e.message, 5)
            return AppStatusType.HALTED

        return AppStatusType.RUNNING
