from pylabs import q

class AppServerPyApps:

    def __init__(self, appName):
        self.appName = appName

    def generate_cfg(self, xmlrpc_port, rest_port, amf_port):
        cfgPath = '/opt/qbase5/pyapps/' + self.appName + '/cfg'
        if not q.system.fs.exists(cfgPath):
            q.system.fs.createDir(cfgPath)
        appserverCfgPath =  '/opt/qbase5/pyapps/' + self.appName + '/cfg/applicationserver'
        appServerCfg = q.config.getInifile(appserverCfgPath)
        appServerCfg.addSection('main')
        if xmlrpc_port:
            appServerCfg.addParam('main', 'xmlrpc_port', xmlrpc_port)
            appServerCfg.addParam('main', 'xmlrpcip', '127.0.0.1')
        if rest_port:
            appServerCfg.addParam('main', 'rest_port', rest_port)
            appServerCfg.addParam('main', 'rest_ip', '127.0.0.1')
        if amf_port:
            appServerCfg.addParam('main', 'amf_port', amf_port)
            appServerCfg.addParam('main', 'amf_ip', '127.0.0.1')
        appServerCfg.addParam('main', 'allow_none', 'True')
        appServerCfg.addParam('main', 'mail_incoming_server', '')
        appServerCfg.write()





