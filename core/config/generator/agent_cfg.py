from pylabs import q
join = q.system.fs.joinPaths

class AgentPyApps:

    def __init__(self, appName):
        self.appName = appName
    
    def generate_cfg(self):
        configfile = q.config.getInifile('agent')
        if not configfile.checkSection(self.appName):
            configfile.addSection(self.appName)
        configfile.addParam(self.appName, "domain", self.appName)
        configfile.addParam(self.appName, 
                        "agentcontrollerguid", "agentcontroller")
        configfile.addParam(self.appName, "hostname", self.appName)
        configfile.addParam(self.appName, "xmppserver", "127.0.0.1")
        configfile.addParam(self.appName, "agentguid", "agent1")
        configfile.addParam(self.appName, "password", self.appName)
        configfile.write()
