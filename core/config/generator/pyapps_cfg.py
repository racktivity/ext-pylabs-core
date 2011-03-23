from pylabs import q
from wfe_cfg import WfePyApps
from arakoon_cfg import ArakoonPyApps
from osis_cfg import OsisPyApps
from applicationserver_cfg import AppServerPyApps
join = q.system.fs.joinPaths

class PyAppsConfigGen:

    def __init__(self, appName):
        self.appName = appName
        self._load_config()
    
    def _load_config(self):
        self.config = q.config.getConfig('pyapps').get(self.appName)

    def pyapps_configuration(self):
        pyappsCfg = q.config.getInifile('pyapps')
        exists = pyappsCfg.checkSection(self.appName)
        if not exists:
            min_ = self.min_range(pyappsCfg)
            max_ = min_ + 1000
            port_range = "%s:%s" % (min_, max_)
            pyappsCfg.addSection(self.appName)
            pyappsCfg.addParam(self.appName, 'port_range', port_range)
            params = self.list_needed_components(min_)
            for key, value in params:
                pyappsCfg.addParam(self.appName, key, value)
            pyappsCfg.write()
            self._load_config()
    
    def generateAll(self):
        self.pyapps_configuration()
        if 'wfe_port' in self.config:
            self.generateWfeConfig()
        if 'arakoon_client_port' in self.config:
            self.generateArakoonConfig()
            self.generateOsisConfig()
        if 'app_server_xmlrpc_port' in self.config:
            self.generateAppServerConfig()
    
    def generateWfeConfig(self):
        wfe = WfePyApps(self.appName)
        wfe.generate_cfg(self.config['wfe_port'])
    
    def generateArakoonConfig(self):
        arakoon = ArakoonPyApps(self.appName)
        arakoon.generate_cfg(self.config['arakoon_client_port'], 
                        self.config['arakoon_server_port'])
    
    def generateOsisConfig(self):
        osis = OsisPyApps(self.appName)
        osis.generate_cfg()
    
    def generateAppServerConfig(self):
        appserver = AppServerPyApps(self.appName)
        appserver.generate_cfg(self.config['app_server_xmlrpc_port'],
                                self.config['app_server_rest_port'],
                                self.config['app_server_amf_port'])
    
    def list_needed_components(self, minRange):
        implPath =  join(q.dirs.pyAppsDir, self.appName, 'impl')
        interfacePath = join(q.dirs.pyAppsDir, self.appName, 'interface')
        dirs = set()
        if q.system.fs.exists(implPath):
            dirs.update(q.system.fs.listDirsInDir(implPath))
        if q.system.fs.exists(interfacePath):
            dirs.update(q.system.fs.listDirsInDir(interfacePath))
        dirBaseNames = set([q.system.fs.getBaseName(dir_) for dir_ in dirs])
        params = set()
        if 'actor' in dirBaseNames or 'action' in dirBaseNames:
            value = minRange + 200
            params.add(('wfe_port', value))
        if 'osis' in dirBaseNames:
            value = minRange + 100
            params.add(('arakoon_client_port', value))
            value = minRange + 101
            params.add(('arakoon_server_port', value))
        if 'osis' in dirBaseNames or 'pymodel' in dirBaseNames or 'service' in dirBaseNames:
            value = minRange + 300
            params.add(('app_server_xmlrpc_port', value))
            value = minRange + 301
            params.add(('app_server_rest_port', value))
            value = minRange + 302
            params.add(('app_server_amf_port', value))
        return params


    def min_range(self, pyappsCfg):
        sections = pyappsCfg.getSections()
        if sections == []:
            return 20000
        minRange = [21000]
        for section in sections:
            portrange = pyappsCfg.getValue(section, 'port_range')
            minRange.append(int(portrange.split(':')[0]))
        return max(minRange)
