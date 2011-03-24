from pylabs import q
from wfe_cfg import WfePyApps
from arakoon_cfg import ArakoonPyApps
from osis_cfg import OsisPyApps
from applicationserver_cfg import AppServerPyApps
POSTGRESUSER = "postgres"

join = q.system.fs.joinPaths

def min_range(pyappsCfg):
    sections = pyappsCfg.getSections()
    if sections == []:
        return 20000
    minRange = [21000]
    for section in sections:
        portrange = pyappsCfg.getValue(section, 'port_range')
        minRange.append(int(portrange.split(':')[0]))
    return max(minRange)


class PyAppsConfigGen:

    def __init__(self, appName):
        self.appName = appName
        self.config = None
        self.components = None
        self._load_config()
    
    def _load_config(self):
        self.config = q.config.getConfig('pyapps').get(self.appName)
        self.components = self.list_needed_components()

    def pyapps_configuration(self):
        pyappsCfg = q.config.getInifile('pyapps')
        exists = pyappsCfg.checkSection(self.appName)
        if not exists:
            min_ = min_range(pyappsCfg)
            max_ = min_ + 1000
            port_range = "%s:%s" % (min_, max_)
            pyappsCfg.addSection(self.appName)
            pyappsCfg.addParam(self.appName, 'port_range', port_range)
            params = self.get_needed_params(min_)
            for key, value in params.iteritems():
                pyappsCfg.addParam(self.appName, key, value)
            pyappsCfg.write()
            self._load_config()
    
    def setup(self):
        if 'postgresql' in self.components:
            if self.appName not in q.manage.postgresql8.cmdb.databases:
                q.manage.postgresql8.startChanges()
                if not q.manage.postgresql8.cmdb.initialized:
                    q.manage.postgresql8.cmdb.initialized = True
                    q.manage.postgresql8.cmdb.rootLogin = POSTGRESUSER
                    q.manage.postgresql8.cmdb.addLogin(POSTGRESUSER)
                q.manage.postgresql8.cmdb.addLogin
                q.manage.postgresql8.cmdb.addDatabase(self.appName)
                q.manage.postgresql8.save()
                q.manage.postgresql8.applyConfig()
        if 'wfe' in self.components:
            if self.appName not in q.manage.ejabberd.cmdb.hosts:
                q.manage.ejabberd.startChanges()
                q.manage.ejabberd.cmdb.addHost(self.appName)
                q.manage.ejabberd.cmdb.addUser('agent', self.appName, 'agent')
                q.manage.ejabberd.cmdb.addUser('agentcontroller', self.appName, 'agentcontroller')
                q.manage.ejabberd.save()
                q.manage.ejabberd.applyConfig()
        taskletpath = join(q.dirs.pyAppsDir, self.appName, 'setup')
        if q.system.fs.exists(taskletpath):
            te = q.getTaskletEngine(taskletpath)
            te.execute({})

    def start(self):
        if 'appserver' in self.components:
            q.manage.applicationserver.start(self.appName)
            q.manage.nginx.start()
        if 'wfe' in self.components:
            q.manage.workflowengine.start(self.appName)
        if 'postgresql' in self.components:
            q.manage.postgresql.start()

    
    def stop(self):
        if 'appserver' in self.components:
            q.manage.applicationserver.stop(self.appName)
        if 'wfe' in self.components:
            q.manage.workflowengine.stop(self.appName)
    
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
    
    def list_needed_components(self):
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
            params.add('wfe')
        if 'osis' in dirBaseNames:
            params.add('arakoon')
            params.add('osis')
            params.add('postgresql')
        types = ('osis', 'pymodel', 'service')
        if any( (type_ in dirBaseNames) for type_ in  types):
            params.add('appserver')
        return params
    
    def get_needed_params(self, minRange):
        params = dict()
        if 'wfe' in self.components:
            value = minRange + 200
            params['wfe_port'] = value
        if 'arakoon' in self.components:
            value = minRange + 100
            params['arakoon_client_port'] = value
            value = minRange + 101
            params['arakoon_server_port'] = value
        if 'appserver' in self.components:
            value = minRange + 300
            params['app_server_xmlrpc_port'] = value
            value = minRange + 301
            params['app_server_rest_port'] = value
            value = minRange + 302
            params['app_server_amf_port'] = value
        return params
