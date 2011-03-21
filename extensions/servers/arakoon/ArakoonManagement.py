"""
This file is part of Arakoon, a distributed key-value store. Copyright
(C) 2010 Incubaid BVBA

Licensees holding a valid Incubaid license may use this file in
accordance with Incubaid's Arakoon commercial license agreement. For
more information on how to enter into this agreement, please contact
Incubaid (contact details can be found on www.arakoon.org/licensing).

Alternatively, this file may be redistributed and/or modified under
the terms of the GNU Affero General Public License version 3, as
published by the Free Software Foundation. Under this license, this
file is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.

See the GNU Affero General Public License for more details.
You should have received a copy of the
GNU Affero General Public License along with this program (file "COPYING").
If not, see <http://www.gnu.org/licenses/>.
"""

from pylabs import q
import os 
import ArakoonRemoteControl
import os.path
import itertools
import subprocess
import time
import string
import logging

class ArakoonManagement:
    def getCluster(self, clusterId):
        """
        @type clusterId: string
        @return a helper to config that cluster
        """
        return ArakoonCluster(clusterId)

    def upgrade(self):
        """
        update configs for the 'arakoon' cluster from 0.8.2 to 0.9.0
        """
        fs = q.system.fs
        jp = fs.joinPaths
        cfgDir = jp(q.dirs.cfgDir,'qconfig')
        if fs.exists(jp(cfgDir,'arakoon.cfg')):
            cfg = q.config.getInifile('arakoon')
            cfg.addParam('global','cluster_id','arakoon')
            cfg.write()

        nodes_source = jp(cfgDir,'arakoonnodes.cfg')
        nodes_target = jp(cfgDir,'arakoon_nodes.cfg')
        if fs.exists(nodes_source):
            fs.moveFile(nodes_source,nodes_target)

        servernodes_source = jp(cfgDir,'arakoonservernodes.cfg')
        servernodes_target = jp(cfgDir,'arakoon_servernodes.cfg')
        if fs.exists(servernodes_source):
            fs.moveFile(servernodes_source, servernodes_target)
        

class ArakoonCluster:

    def __init__(self, clusterId):
        self.__validateName(clusterId)
        self._clusterId = clusterId
        self._binary = "arakoon"
        self._cfgPath = q.system.fs.joinPaths(q.dirs.cfgDir, "qconfig")


    
    def _servernodes(self):
        return '%s_servernodes' % self._clusterId

    def __repr__(self):
        return "<ArakoonCluster:%s>" % self._clusterId

    def _getConfigFile(self):
        config = q.config.getInifile(self._clusterId)
        return config
    
    def addNode(self,
                name,
                ip = "127.0.0.1",
                clientPort = 7080,
                messagingPort = 10000,
                logLevel = "info",
                logDir = None,
                home = None,
                tlogDir = None,
                user = None,
                group = None,
                isLocal = True):
        """
        Add a node to the configuration of the supplied cluster

        The function also creates 
        @param name the name of the node, should be unique across the environment
        @param ip the ip this node shoulc be contacted on
        @param clientPort the port the clients should use to contact this node
        @param messagingPort the port the other nodes should use to contact this node
        @param logLevel the loglevel (debug info notice warning error fatal)
        @param logDir the directory used for logging
        @param home the directory used for the nodes data
        @param tlogDir the directory used for tlogs (if none, home will be used)

        """
        self.__validateName(name)
        self.__validateLogLevel(logLevel)


        config = self._getConfigFile()
        if not config.checkSection("global"):
            config.addSection("global")
            config.addParam("global","cluster_id",self._clusterId)
            config.addParam("global","nodes", "")

        nodes = self.__getNodes(config)

        if name in nodes:
            raise Exception("node %s already present" % name )

        nodes.append(name)
        config.addSection(name)
        config.addParam(name, "name", name)
        config.addParam(name, "ip", ip)
        self.__validateInt("clientPort", clientPort)
        config.addParam(name, "client_port", clientPort)
        self.__validateInt("messagingPort", messagingPort)
        config.addParam(name, "messaging_port", messagingPort)
        config.addParam(name, "log_level", logLevel)
        
        if user is not None:
            config.addParam(name, "user", user)
        
        if group is not None:
            config.addParam(name, "group", group)

        if logDir is None:
            logDir = q.system.fs.joinPaths(q.dirs.logDir, self._clusterId, name)
        config.addParam(name, "log_dir", logDir) 

        if home is None:
            home = q.system.fs.joinPaths(q.dirs.varDir, "db", self._clusterId, name)
        config.addParam(name, "home", home)

        if tlogDir:
            config.addParam(name,"tlog_dir", tlogDir)
        
        config.setParam("global","nodes", ",".join(nodes))

        config.write()

    def removeNode(self, name):
        """
        Remove a node from the configuration of the supplied cluster

        @param name the name of the node as configured in the config file
        """
        self.__validateName(name)

        config = self._getConfigFile()
        if not config.checkSection("global"):
            raise Exception("No node with name %s" % name)

        nodes = self.__getNodes(config)
        
        if name in nodes:
            self.removeLocalNode(name)
            config.removeSection(name)
            nodes.remove(name)
            config.setParam("global","nodes", ",".join(nodes))
            config.write()
            return

        raise Exception("No node with name %s" % name)

    def setMasterLease(self, duration=None):
        """
        Set the master lease duration in the supplied cluster

        @param duration The duration of the master lease in seconds
        @param clusterId the id of the arakoon cluster
        """
        section = "global"
        key = "lease_period"
        
        config = q.config.getInifile(self._clusterId)

        if not config.checkSection( section ):
            raise Exception("Section '%s' not found in config" % section )

        if duration:
            if not isinstance( duration, int ) :
                raise AttributeError( "Invalid value for lease duration (expected int, got: '%s')" % duration)
            if config.checkParam(section, key):
                config.setParam(section, key, duration)
            else:
                config.addParam(section, key, duration)
        else:
            config.removeParam(section, key)

        config.write()
        
    def forceMaster(self, name=None):
        """
        Force a master in the supplied cluster

        @param name the name of the master to force. If None there is no longer a forced master
        @param clusterId: the id of the arakoon cluster
        """
        config = self._getConfigFile()
        if not config.checkSection("global"):
            raise Exception("No node with name %s configured" % name)

        if name:
            nodes = self.__getNodes(config)

            self.__validateName(name)
            if not name in nodes:
                raise Exception("No node with name %s configured in cluster %s" % name)

            if config.checkParam("global", "master"):
                config.setParam("global", "master", name)
            else:
                config.addParam("global", "master", name)
        else:
            config.removeParam("global", "master")

        config.write()

    def setQuorum(self, quorum=None):
        """
        Set the quorum for the supplied cluster

        The quorum dictates on how many nodes need to acknowledge the new value before it becomes accepted.
        The default is (nodes/2)+1

        @param quorum the forced quorom. If None, the default is used 
        """
        config = self._getConfigFile()

        if not config.checkSection("global"):
            config.addSection("global")
            config.addParam("global","nodes", "")

        if quorum:
            try :
                if ( int(quorum) != quorum or
                     quorum < 0 or
                     quorum > len( self.listNodes())) :
                    raise Exception ( "Illegal value for quorum %s" % quorum )
                
            except:
                raise Exception("Illegal value for quorum %s " % quorum)
            
            if config.checkParam("global", "quorum"):
                config.setParam("global", "quorum", int(quorum))
            else:
                config.addParam("global", "quorum", int(quorum))
        else: 
            config.removeParam("global", "quorum")
            
        config.write()


    def getClientConfig(self):
        """
        Get an object that contains all node information in the supplied cluster
        @return dict the dict can be used as param for the ArakoonConfig object
        """
        config = self._getConfigFile()
        clientconfig = dict()

        if config.checkSection("global"):
            nodes = self.__getNodes(config)

            for name in nodes:
                clientconfig[name] = (config.getValue(name, "ip"),
                                      int(config.getValue(name, "client_port")))

        return clientconfig

    def listNodes(self):
        """
        Get a list of all node names in the supplied cluster
        @return list of strings containing the node names
        """
        config = self._getConfigFile()
        return self.__getNodes(config)

    def getNodeConfig(self,name):
        """
        Get the parameters of a node section 

        @param name the name of the node
        @return dict keys and values of the nodes parameters
        """
        self.__validateName(name)

        config = self._getConfigFile()

        nodes = self.__getNodes(config)

        if name in nodes:
            return config.getSectionAsDict(name)
        else:
            raise Exception("No node with name %s configured" % name)


    def createDirs(self, name):
        """
        Create the Directories for a local arakoon node in the supplied cluster

        @param name the name of the node as configured in the config file
        """
        self.__validateName(name)

        config = self._getConfigFile()
        if not config.checkSection("global"):
            raise Exception("No node with name %s configured" % name)

        nodes = self.__getNodes(config)

        if name in nodes:
            home = config.getValue(name, "home")
            q.system.fs.createDir(home)

            if config.checkParam(name, "tlog_dir"):
                tlogDir = config.getValue(name, "tlog_dir")
                q.system.fs.createDir(tlogDir)

            logDir = config.getValue(name, "log_dir")
            q.system.fs.createDir(logDir)

            return

        msg = "No node %s configured" % name
        raise Exception(msg)

    def removeDirs(self, name):
        """
        Remove the Directories for a local arakoon node in the supplied cluster

        @param name the name of the node as configured in the config file
        """
        self.__validateName(name)

        config = self._getConfigFile()
        if not config.checkSection('global'):
            raise Exception("No node with name %s" % name )


        nodes = self.__getNodes(config)

        if name in nodes:
            home = config.getValue(name, "home")
            q.system.fs.removeDirTree(home)

            if config.checkParam(name, "tlog_dir"):
                tlogDir = config.getValue(name, "tlog_dir")
                q.system.fs.removeDirTree(tlogDir)
            
            logDir = config.getValue(name, "log_dir")
            q.system.fs.removeDirTree(logDir)
            return
        
        raise Exception("No node %s" % name)



    def addLocalNode(self, name):
        """
        Add a node to the list of nodes that have to be started locally
        from the supplied cluster

        @param name the name of the node as configured in the config file
        """
        self.__validateName(name)

        config = self._getConfigFile()

        if not config.checkSection("global"):
            raise Exception("No node %s" % name )

        nodes = self.__getNodes(config)
        config_name = self._servernodes()
        if name in nodes:
            nodesconfig = q.config.getInifile(config_name)

            if not nodesconfig.checkSection("global"):
                nodesconfig.addSection("global")
                nodesconfig.addParam("global","nodes", "")

            nodes = self.__getNodes(nodesconfig)
            if name in nodes:
                raise Exception("node %s already present" % name)
            nodes.append(name)
            nodesconfig.setParam("global","nodes", ",".join(nodes))

            nodesconfig.write()

            return
        
        raise Exception("No node %s" % name)

    def removeLocalNode(self, name):
        """
        Remove a node from the list of nodes that have to be started locally
        from the supplied cluster

        @param name the name of the node as configured in the config file
        """
        self.__validateName(name)
        config_name = self._servernodes()
        config = q.config.getInifile(config_name)

        if not config.checkSection("global"):
            return

        nodes = self.__getNodes(config)

        if name in nodes:
            nodes.remove(name)
            config.setParam("global","nodes", ",".join(nodes))
            config.write()

    def listLocalNodes(self):
        """
        Get a list of the local nodes in the supplied cluster

        @return list of strings containing the node names
        """
        config_name = self._servernodes()
        config = q.config.getInifile(config_name)

        return self.__getNodes(config)

    def setUp(self, numberOfNodes):
        """
        Sets up a local environment

        @param numberOfNodes the number of nodes in the environment
        @return the dict that can be used as a param for the ArakoonConfig object
        """
        cid = self._clusterId
        for i in range(0, numberOfNodes):
            nodeName = "%s_%i" %(cid, i)
            self.addNode(name = nodeName,
                         clientPort = 7080+i,
                         messagingPort = 10000+i)
            self.addLocalNode(nodeName)
            self.createDirs(nodeName)

        if numberOfNodes > 0:
            self.forceMaster("%s_0" % cid)
        
        config = self._getConfigFile()
        config.addParam( 'global', 'cluster_id', cid)

    def tearDown(self, removeDirs=True ):
        """
        Tears down a local environment

        @param removeDirs remove the log and home dir
        @param cluster the name of the arakoon cluster
        """
        config = self._getConfigFile()

        if not config.checkSection('global'):
            return


        nodes = self.__getNodes(config)
        
        for node in nodes:
            if removeDirs:
                self.removeDirs(node)

            self.removeNode(node)
        
        if self.__getForcedMaster(config):
            self.forceMaster(None)

    def __getForcedMaster(self, config):
        if not config.checkSection("global"):
            return []
        
        if config.checkParam("global", "master"):
            return config.getValue("global", "master").strip()
        else:
            return []

    def __getNodes(self, config):
        if not config.checkSection("global"):
            return []

        nodes = config.getValue("global", "nodes").strip()
        # "".split(",") -> ['']
        if nodes == "":
            return []
        nodes = nodes.split(",")
        nodes = map(lambda x: x.strip(), nodes)

        return nodes

    def __validateInt(self,name, value):
        typ = type(value)
        if not typ == type(1):
            raise Exception("%s=%s (type = %s) but should be an int" % (name, value, typ))
    def __validateName(self, name):
        if name is None:
            raise Exception("A name should be passed. None is not an option")

        if not type(name) == type(str()):
            raise Exception("Name should be of type strinq.config.getInifile(clusterId)g")

        for char in [' ', ',', '#']:
            if char in name:
                raise Exception("name should not contain %s" % char)

    def __validateLogLevel(self, name):
        if not name in ["info", "debug", "notice", "warning", "error", "fatal"]:
            raise Exception("%s is not a valid log level" % name)


    def start(self):
        """
        start all nodes in the cluster
        """
        for name in self.listLocalNodes():
            self._startOne(name)

    def stop(self):
        """
        stop all nodes in the supplied cluster
        
        @param cluster the arakoon cluster name
        """
        for name in self.listLocalNodes():
            self._stopOne(name)


    def restart(self):
        """
        Restart all nodes in the supplied cluster
        
        @param clusterId the arakoon cluster name
        """
        for name in self.listLocalNodes():
            self._restartOne(name)

    def getStatus(self):
        """
        Get the status of all nodes in the supplied cluster

        @return dict node name -> status (q.enumerators.AppStatusType)
        """
        status = {}
        for name in self.listLocalNodes():
            status[name] = self._getStatusOne(name)

        return status

    def _requireLocal(self, nodeName):
        if not nodeName in self.listLocalNodes():
            raise Exception(EXC_MSG_NOT_LOCAL_FMT % nodeName)
    
    def startOne(self, nodeName):
        """
        Start the node with a given name
        @param nodeName The name of the node

        """
        self._requireLocal(nodeName)
        self._startOne(nodeName)

    
    def catchupOnly(self, nodeName):
        """
        make the node catchup, but don't start it.
        (This is handy if you want to minimize downtime before you,
         go from a 1 node setup to a 2 node setup)
        """
        self._requireLocal(nodeName)
        cmd = self._getCommand(nodeName)
        cmd.append('-catchup-only')
        subprocess.call(cmd)
        
    def stopOne(self, nodeName):
        """
        Stop the node with a given name
        @param nodeName The name of the node

        """
        self._requireLocal(nodeName)
        self._stopOne(nodeName)

    def remoteCollapse(self, nodeName, n):
        """
        Tell the targetted node to collapse n tlog files
        @type nodeName: string
        @type n: int
        """
        config = self.getNodeConfig(nodeName)
        ip = config['ip']
        port = int(config['client_port'])
        ArakoonRemoteControl.collapse(ip,port,self._clusterId, n)
        
    def restartOne(self, nodeName):
        """
        Restart the node with a given name in the supplied cluster
        @param nodeName The name of the node

        """
        self._requireLocal( nodeName)
        self._restartOne(nodeName)

    def getStatusOne(self, nodeName):
        """
        Get the status node with a given name in the supplied cluster
        @param nodeName The name of the node
        """
        self._requireLocal(nodeName)
        return self._getStatusOne(nodeName)

    def _startOne(self, name):
        if self._getStatusOne(name) == q.enumerators.AppStatusType.RUNNING:
            return
        
        kwargs = { }
        config = self.getNodeConfig(name)
        if 'user' in config :
            kwargs['user'] = config ['user']
            
        if 'group' in config :
            kwargs ['group'] = config ['group']
        
        
        arakoon_command = self._getCommandString(name)
        pid = q.system.process.runDaemon(arakoon_command, **kwargs)

    def _stopOne(self, name):
        arakoon_command = self._getCommandString(name)
        cmd = ['pkill', 
               '-f', 
               arakoon_command]
        logging.debug("stopping '%s' with: %s", name, string.join(cmd, ' '))
        subprocess.call(cmd, close_fds=True)

        i = 0
        while(self._getStatusOne(name) == q.enumerators.AppStatusType.RUNNING):
            time.sleep(1)
            i += 1

            if i == 10:
                logging.debug("stopping '%s' with -9")
                subprocess.call(['pkill', 
                                 '-9', 
                                 '-f', 
                                 arakoon_command],
                                close_fds=True)
                break
            else:
                subprocess.call(cmd, close_fds=True)
    
    def _restartOne(self, name):
        self._stopOne(name)
        self._startOne(name)


    def _getPid(self, name):
        if self._getStatusOne(name) == q.enumerators.AppStatusType.HALTED:
            return None
        
        arakoon_command = self._getCommandString(name)
        cmd = 'pgrep -o -f "%s"' % arakoon_command
        (exitCode, stdout, stderr) = q.system.process.run( cmd )
        if exitCode != 0 :
            return None
        else :
            return int(stdout)
                
    def _getStatusOne(self, name):
        arakoon_command = self._getCommandString(name)
        cmd = ['pgrep','-f', arakoon_command]
        ret = subprocess.call(cmd,close_fds=True, stdout=subprocess.PIPE)
        result = q.enumerators.AppStatusType.HALTED
        if ret == 0:
            result = q.enumerators.AppStatusType.RUNNING

        return result

    def getStorageUtilization(self, node = None):
        """Calculate and return the disk usage of the supplied arakoon cluster on the system

        When no node name is given, the aggregate consumption of all nodes
        configured in the supplied cluster on the system is returned.

        Return format is a dictionary containing 3 keys: 'db', 'tlog' and
        'log', whose values denote the size of database files
        (*.db, *.db.wall), TLog files (*.tlc, *.tlog) and log files (*).

        :param node: Name of the node to check
        :type node: `str`
        
        :param cluster: Name of the arakoon cluster
        :type cluster: `str`

        :return: Storage utilization of the node(s)
        :rtype: `dict`

        :raise ValueError: No such local node
        """
        local_nodes = self.listLocalNodes()

        if node is not None and node not in local_nodes:
            raise ValueError(EXC_MSG_NOT_LOCAL_FMT % node)

        def helper(config):
            home = config['home']
            log_dir = config['log_dir']

            files_in_dir = lambda dir_: itertools.ifilter(os.path.isfile,
                (os.path.join(dir_, name) for name in os.listdir(dir_)))
            matching_files = lambda *exts: lambda files: \
                (file_ for file_ in files
                    if any(file_.endswith(ext) for ext in exts))

            tlog_files = matching_files('.tlc', '.tlog','.tlf')
            db_files = matching_files('.db', '.db.wal')
            log_files = matching_files('') # Every string ends with ''

            sum_size = lambda files: sum(os.path.getsize(file_)
                for file_ in files)

            return {
                'tlog': sum_size(tlog_files(files_in_dir(home))),
                'db': sum_size(db_files(files_in_dir(home))),
                'log': sum_size(log_files(files_in_dir(log_dir)))
            }

        nodes = (node, ) if node is not None else local_nodes
        stats = (helper(cluster.getNodeConfig(node)) for node in nodes)

        result = {}
        for stat in stats:
            for key, value in stat.iteritems():
                result[key] = result.get(key, 0) + value

        return result

    def _getCommand(self, nodeName):
        return [self._binary,
               '-daemonize',
               '-config',
               '%s/%s.cfg' % (self._cfgPath, self._clusterId),
               '--node',
               nodeName]

    def _getCommandString(self, nodeName):
        return " ".join(self._getCommand(nodeName))
