from pylabs import q
import time
import sys
import signal
import re

_join = q.system.fs.joinPaths

APPNAME = "discoveryagent"
EXECUTABLE = "discoveryagentservice.py"
LOG_DIR = _join(q.dirs.varDir, "log", APPNAME)
PID_DIR = _join(q.dirs.varDir, "pid")
PID_FILE = _join(PID_DIR, "%s.%%s.pid" % APPNAME)
APP_DIR = _join(q.dirs.appDir, APPNAME)
PROCESS_FILE = _join(q.dirs.appDir, APPNAME, EXECUTABLE)
    
class AutodiscoveryagentCMDTools(object):
    def start(self, workers=1, timeout=5):
        """
        Starts a number of autodiscovery agents, if this number of agents is already running
        nothing will happen, if the requested workers number are more that what is already  
        running, more agents will be started to fullfill the request.
        if the requested workers number is less that the number of already running agents,..
        some agents will be stopped to fullfill the request
        
        @param workers: number of workers to start
        @param timout: number of seconds to wait before reporting failing to start the server
        @type timeout: integer
        
        @return: True if success False otherwise  
        """
        
        if not q.system.fs.isDir(LOG_DIR):
            q.system.fs.createDir(LOG_DIR)
            
        error = 0
        agents = self.getRunnintAgents()
        nagents = len(agents)
        if nagents == workers:
            return (0, "Agents are already running")
        elif workers < nagents:
            return self.stop(nagetns - workers, timeout)
        else:
            #reuse IDs
            idset = set(range(workers))
            tostart = idset.difference(agents)
            for agent in tostart:
                cmd = "%(exec)s %(process)s -p %(pid)s" % {"exec": sys.executable,
                                                            "process": PROCESS_FILE,
                                                            "pid" : PID_FILE % agent}
                
                q.system.process.runDaemon(cmd,
                                           stdout = _join(LOG_DIR, "stdout.%s.log" % agent),
                                           stderr = _join(LOG_DIR, "stderr.%s.log" % agent))
                while timeout:
                    if self.isRunning(agent):
                        break
                    time.sleep(1)
                    timeout -= 1
                if not self.isRunning(agent):
                    error += 1
        if error:
            return (1, "One or more agents failed to start, please check the logs under '%s' only '%s' are running" % (LOG_DIR, self.getNumerOfRunningAgents()))
        
        return (0, "Agents have been started successfully")
    
    def stop(self, workers=0, timeout=5):
        """
        Stops number of agents
         
        @param workers: Number of workers to kill, kill all if 0
        @param timeout: number of seconds to wait before trying to kill the consumer process abruptly
        @type timeout: integer
        """
        agents = self.getRunnintAgents()
        tokill = workers if workers else len(agents)
        tokill = min(tokill, len(agents))
        
        for i in range(tokill):
            agent = agents[i]
            q.system.process.kill(self._getPID(agent), signal.SIGTERM)
            
            while timeout:
                if not self.isRunning(agent):
                    break
                time.sleep(1)
                timeout -= 1
            
            #force kill
            if self.isRunning(agent):
                q.system.process.kill(self._getPID(agent), signal.SIGKILL)
        
        return (0, "Agents have been stopped successfully")
    
    def discover(self, address, port=161, communitystring='private'):
        if not q.system.net.validateIpAddress(address):
            raise ValueError("Invalid ip address '%s'" % address)
        
        taskletsdir = _join(APP_DIR, "tasklets")
        te = q.taskletengine.get(taskletsdir)
        
        params = {'ipaddress': address,
                  'port': port,
                  'password': communitystring}
        
        te.execute(params, tags=('discovery', 'meteringdevice', 'single'))
        return params['device']
    
    def _getPIDFromFile(self, pidfile):
        if not q.system.fs.isFile(pidfile):
            return 0
        return int(q.system.fs.fileGetContents(pidfile).strip())
    
    def _getPID(self, agent):
        pidfile = PID_FILE % agent
        return self._getPIDFromFile(pidfile)

    def restartAll(self, timeout=5):
        running = self.getNumerOfRunningAgents()
        self.stop(timeout=timeout)
        self.start(running, timeout)
    
    def getRunnintAgents(self):
        pidfiles = q.system.fs.listFilesInDir(PID_DIR, filter="%s*" % APPNAME)
        agents = list()
        for pidfile in pidfiles:
            m = re.match("%s\.(\d+)\.pid" % APPNAME, q.system.fs.getBaseName(pidfile))
            if not m:
                continue
            agent = int(m.group(1))
            if self.isRunning(agent):
                agents.append(agent)
                
        return agents
    
    def getNumerOfRunningAgents(self):
        return len(self.getRunnintAgents())
    
    def isRunning(self, agent=1):
        """
        Get the status of the racktivityconsumer
        """
        pid = self._getPID(agent)
        if pid:
            return not bool(q.system.process.checkProcessForPid(pid, "python"))
        return False
    
    def getStatus(self, agent=1):
        return q.enumerators.AppStatusType.RUNNING if self.isRunning(agent) else q.enumerators.AppStatusType.HALTED