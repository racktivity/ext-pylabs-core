from pylabs import q

class OsisPyApps:

    def __init__(self, appName):
        self.appName = appName
        self.components = [('passwd', 'pass123'), ('login', 'qbase'), 
                        ('database', self.appName),('ip', '127.0.0.1')]

    def generate_cfg(self):
        cfgPath = '/opt/qbase5/pyapps/' + self.appName + '/cfg'
        if not q.system.fs.exists(cfgPath):
            q.system.fs.createDir(cfgPath)
        osisCfgPath =  '/opt/qbase5/pyapps/' + self.appName + '/cfg/osisdb'
        osisCfg = q.config.getInifile(osisCfgPath)
        exists = osisCfg.checkSection(self.appName)
        if not exists:
            osisCfg.addSection(self.appName)
            for key, value in self.components:
                osisCfg.addParam(self.appName, key, value)
        osisCfg.write()


