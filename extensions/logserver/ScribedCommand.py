
 
from pymonkey import q
from pymonkey.inifile import IniFile
from pymonkey.baseclasses.CommandWrapper import CommandWrapper
from pymonkey.enumerators import AppStatusType
import time

class ScribedCommand(CommandWrapper):
    """
    A basic ScribedCommandWrapper to start/stop/restart the Scribe server
    """

#    def _getPidFile(self):
#        return q.system.fs.joinPaths(q.dirs.pidDir, "scribed.pid")
        
    def _getScribedBinary(self):
        return q.system.fs.joinPaths(q.dirs.binDir,"scribed")
    def _getScribeCTRLBinary(self):
        return q.system.fs.joinPaths(q.dirs.binDir, "scribe_ctrl")	

    def _getDefaultConfigFile(self):
	return q.system.fs.joinPaths(q.dirs.cfgDir, 'scribe_logserver.conf')        
    
    def _getPort(self):
	serverIniFile = IniFile(q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'logservermain.cfg'))
	return serverIniFile.getValue('main', 'port')
	
    def _getStatus(self, port):
        #@todo: use the status coammand instead of the version command to get the server status once the status problem resolved
	command =  "%(SCRIBECTRLCommand)s version %(port)s" % {"SCRIBECTRLCommand":self._getScribeCTRLBinary(), "port":port}
        exitCode, output = q.system.process.execute(command, dieOnNonZeroExitCode = False, outputToStdout = False)
        #status command returns 2 if scribe is alive else returns 3 ?????
        if exitCode :
            return AppStatusType.HALTED

        return AppStatusType.RUNNING
	
    def start(self, configFile = None, timeout = 5):
        """
        Start Scribe Server
        @param configFile: configuration file for describing the different stores
        @type  configFile: string
        """
        port = self._getPort()
        if self._getStatus(port) == AppStatusType.RUNNING:
            q.console.echo('Scribe Server on port %s already running'%port)
            return 
        if not configFile:
	    configFile = self._getDefaultConfigFile()
        q.logger.log('Starting scribe server with port %s using config file %s'%(port, configFile), 5)
        command =  "%(SCRIBEDCommand)s -p %(port)s -c %(configFile)s 2> %(scribeout)s&" % {"SCRIBEDCommand":self._getScribedBinary(), "port": port, "configFile":configFile, 'scribeout': q.system.fs.joinPaths(q.dirs.logDir, 'logserver.out')}
	exitCode, output = q.system.process.execute(command, dieOnNonZeroExitCode = False, outputToStdout = True)
        
        t = timeout
        started = False
        while t>0:
            if q.system.process.checkProcess('bin/scribed') == 0:
                started = True
                break
            t = t - 1
            time.sleep(1)
        if not started:
            q.logger.log("Scribe could not be started in %d seconds" % timeout, 8)
            raise RuntimeError("Scribe could not be started in %d seconds" % timeout)
        
        q.logger.log('Scribe server on port %s and config file %s started Successfully'%(port, configFile), 3)
        q.console.echo("Scribe started successfully.")
        
    def stop(self):
        """
        Stop Scribe Server
        """
        port = self._getPort() 
        if self._getStatus(port) == AppStatusType.HALTED:
            q.console.echo('Scribe Server on port %s is not running'%port)
            return
        
        command =  "%(SCRIBECTRLCommand)s stop %(port)s" % {"SCRIBECTRLCommand":self._getScribeCTRLBinary(), "port":port}
        exitCode, output = q.system.process.execute(command, dieOnNonZeroExitCode = False, outputToStdout = True)

        if  exitCode and output:
            raise RuntimeError("Scribe could not be stopped. Reason: %s"%output)
        
        q.console.echo("Scribe stopped successfully")
	
    
    def restart(self):
        """
        Restart Scribe Server
        """
            
        self.stop()
        self.start()
        
    def getStatus(self):
        """
        Check the live status of the scribe server
        """
        return self._getStatus(self._getPort())
       
    
    def getDetailedStatus(self):
        """
	Used the status command to get detailed status of the scribe server
	"""
	command =  "%(SCRIBECTRLCommand)s status %(port)s" % {"SCRIBECTRLCommand":self._getScribeCTRLBinary(), "port":self._getPort()}
        exitCode, output = q.system.process.execute(command, dieOnNonZeroExitCode = False, outputToStdout = False)
        #status command returns 2 if scribe is alive else returns 3 ?????
        if exitCode == 3:
            return AppStatusType.HALTED

        return AppStatusType.RUNNING
