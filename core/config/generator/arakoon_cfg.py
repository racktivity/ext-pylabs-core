from pylabs import q
join = q.system.fs.joinPaths

class ArakoonPyApps:

    def __init__(self, appName):
        self.appName = appName
    
    
    def generate_cfg(self, client_port, server_port):
        self.arakoon_pyapp_cfg(client_port, server_port)
        self.arakoon_pyapp_nodes(client_port)
        self.arakoon_pyapp_servernodes()

    def arakoon_pyapp_cfg(self, client_port, server_port):
        cfgFile = 'arakoon_'+self.appName

        arakoonCfg = q.config.getInifile(cfgFile)
        node = self.appName + '_0'
        arakoonCfg.addSection('global')
        arakoonCfg.addParam('global', 'nodes', node)
        arakoonCfg.addParam('global', 'cluster_id', self.appName)
        arakoonCfg.addParam('global', 'lease period', 10)
        arakoonCfg.addSection(node)
        arakoonCfg.addParam(node, 'log_level', 'debug')
        arakoonCfg.addParam(node, 'name', 'sturdy_0')
        arakoonCfg.addParam(node, 'ip', '127.0.0.1')
        logDir = join(q.dirs.logDir, 'arakoon_%s' % self.appName,  
                                    "%s_0.log" % self.appName)
        home = join(q.dirs.varDir, 'db', 'arakoon_%s' % self.appName, 
                                    '%s_0.db' % self.appName)
        arakoonCfg.addParam(node, 'log_dir', logDir)
        arakoonCfg.addParam(node, 'home', home)
        arakoonCfg.addParam(node, 'client_port', client_port)
        arakoonCfg.addParam(node, 'messaging_port', server_port)
        arakoonCfg.write()
   
    def arakoon_pyapp_nodes(self, client_port):
        nodesFile = 'arakoon_' + self.appName + '_nodes'
        arakoonNodesCfg = q.config.getInifile(nodesFile)
        node = self.appName + '_0'
        arakoonNodesCfg.addSection('global')
        arakoonNodesCfg.addParam('global', 'nodes', node)
        arakoonNodesCfg.addParam('global', 'cluster_id', self.appName)
        arakoonNodesCfg.addSection(node)
        arakoonNodesCfg.addParam(node, 'name', node)
        arakoonNodesCfg.addParam(node, 'ip', '127.0.0.1')
        arakoonNodesCfg.addParam(node, 'client_port', client_port)
        arakoonNodesCfg.write()


    def arakoon_pyapp_servernodes(self):
        serverNodesFile = 'arakoon_' + self.appName + '_servernodes'
        arakoonServerNodesCfg = q.config.getInifile(serverNodesFile)
        node = self.appName + '_0'
        arakoonServerNodesCfg.addSection('global')
        arakoonServerNodesCfg.addParam('global', 'nodes', node)
        arakoonServerNodesCfg.write()
