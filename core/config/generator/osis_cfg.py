from pylabs import q

class OsisPyApps:

    def __init__(self, appName):
        self.appName = appName
        self.components = [('passwd', 'pass123'), ('login', 'qbase'), 
                        ('database', self.appName),('ip', '127.0.0.1')]

    def generate_cfg(self):
        iniFile = q.system.fs.joinPaths(q.dirs.cfgDir, 'osisdb.cfg')
        ini = q.tools.inifile.new(iniFile)

        exists = ini.checkSection(self.appName)
        if not exists:
            ini.addSection(self.appName)
            for key, value in self.components:
                ini.addParam(self.appName, key, value)
        ini.write()
