from pylabs import q

class WfePyApps:

    def __init__(self, appName):
        self.appName = appName
        self.jid = 'agentcontroller@'+self.appName
        self.components = [('xmpp_server_host', '127.0.0.1'), 
                            ('xmpp_server_port ', '5222'), 
                            ('password', self.appName), 
                            ('jid', self.jid)]

    def generate_cfg(self, wfe_port):
        self.components.append(('port', wfe_port))
        cfgPath = '/opt/qbase5/pyapps/' + self.appName + '/cfg'
        if not q.system.fs.exists(cfgPath):
            q.system.fs.createDir(cfgPath)
        wfeCfgPath =  '/opt/qbase5/pyapps/' + self.appName + '/cfg/wfe'
        wfeCfg = q.config.getInifile(wfeCfgPath)
        wfeCfg.addSection('main')
        for key, value in self.components:
            wfeCfg.addParam('main', key, value)

