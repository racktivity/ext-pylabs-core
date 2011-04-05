import os
import os.path
import re
from pylabs import q, p
from wfe_cfg import WfePyApps
from arakoon_cfg import ArakoonPyApps
from osis_cfg import OsisPyApps
from agent_cfg import AgentPyApps
from applicationserver_cfg import AppServerPyApps
import osis
from osis.client import OsisConnection
from osis.client.xmlrpc import XMLRPCTransport
import pymodel
from pymodel.serializers import ThriftSerializer


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
        #create user with applicationname
        if not q.system.unix.unixUserExists(self.appName):
            q.system.unix.addSystemUser(self.appName)
        if 'postgresql' in self.components:
            postgres = q.manage.postgresql8
            if self.appName not in postgres.cmdb.databases:
                postgres.startChanges()
                if not postgres.cmdb.initialized:
                    postgres.cmdb.initialized = True
                    postgres.cmdb.rootLogin = POSTGRESUSER
                    postgres.cmdb.addLogin(POSTGRESUSER)
                db = postgres.cmdb.addDatabase(self.appName, self.appName)
                db.addACE(self.appName, '', q.enumerators.PostgresqlAccessRightType.WRITE)
                postgres.cmdb.addLogin(self.appName,  type='host', 
                        cidr_address='127.0.0.1/32',database=self.appName)
                postgres.save()
                postgres.applyConfig()
        if 'wfe' in self.components:
            if self.appName not in q.manage.ejabberd.cmdb.hosts:
                agent_cfg = AgentPyApps(self.appName)
                password = agent_cfg.password
                agentguid = agent_cfg.agentguid
                agentcontrollerguid = agent_cfg.agentcontrollerguid
                hostname = agent_cfg.hostname

                q.manage.ejabberd.startChanges()
                q.manage.ejabberd.cmdb.addHost(hostname)
                q.manage.ejabberd.cmdb.addUser(agentguid, hostname, password)
                q.manage.ejabberd.cmdb.addUser(agentcontrollerguid, hostname, agentcontrollerguid)

                q.manage.ejabberd.save()
                q.manage.ejabberd.applyConfig()

        self._configurePortal()
        # self._populatePortal()

        taskletpath = join(q.dirs.pyAppsDir, self.appName, 'impl', 'setup')
        if q.system.fs.exists(taskletpath):
            te = q.taskletengine.get(taskletpath)
            params = {"appname": self.appName}
            te.execute(params)

    def start(self):
        if 'appserver' in self.components:
            q.manage.applicationserver.start(self.appName)
            q.manage.nginx.start()
        if 'wfe' in self.components:
            q.manage.workflowengine.start(self.appName)
        if 'postgresql' in self.components:
            q.manage.postgresql8.start()
        if 'arakoon' in self.components:
            cluster = q.manage.arakoon.getCluster(self.appName)
            cluster.start()
        if 'event_consumers' in self.components:
            p.events.startConsumers(self.appName)

    
    def stop(self):
        if 'appserver' in self.components:
            q.manage.applicationserver.stop(self.appName)
        if 'wfe' in self.components:
            q.manage.workflowengine.stop(self.appName)
        if 'arakoon' in self.components:
            cluster = q.manage.arakoon.getCluster(self.appName)
            cluster.stop()
        if 'event_consumers' in self.components:
            p.events.stopConsumers(self.appName)
    
    def generateAll(self):
        self.pyapps_configuration()
        if 'wfe_port' in self.config:
            self.generateWfeConfig()
            AgentPyApps(self.appName).generate_cfg()
        if 'arakoon_baseport' in self.config:
            self.generateArakoonConfig()
            self.generateOsisConfig()
        if 'app_server_xmlrpc_port' in self.config:
            self.generateAppServerConfig()
    
    def generateWfeConfig(self):
        wfe = WfePyApps(self.appName)
        wfe.generate_cfg(self.config['wfe_port'])
    
    def generateArakoonConfig(self):
        arakoon = ArakoonPyApps(self.appName)
        arakoon.generate_cfg(self.config['arakoon_baseport'])
    
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
        if 'events' in dirBaseNames:
            params.add('event_consumers')
        return params
    
    def get_needed_params(self, minRange):
        params = dict()
        if 'wfe' in self.components:
            value = minRange + 200
            params['wfe_port'] = value
        if 'arakoon' in self.components:
            value = minRange + 100
            params['arakoon_baseport'] = value
        if 'appserver' in self.components:
            value = minRange + 300
            params['app_server_xmlrpc_port'] = value
            value = minRange + 301
            params['app_server_rest_port'] = value
            value = minRange + 302
            params['app_server_amf_port'] = value
        return params

    def _configurePortal(self):
        nginx = q.manage.nginx

        nginx.startChanges()

        vhost = nginx.cmdb.virtualHosts.get('80')
        if not vhost:
            vhost = nginx.cmdb.addVirtualHost('80')

        if '@lfw' not in vhost.sites:
            lfw = vhost.addSite('@lfw', '@lfw')
            lfw.addOption('root', '/opt/qbase5/www/lfw/')

        root = os.path.join(q.dirs.pyAppsDir, self.appName, 'portal', 'static')
        if not os.path.isdir(root):
            os.makedirs(root, 0755)

        if not self.appName in vhost.sites:
            site = vhost.addSite(self.appName, '/%s' % self.appName)
            site.addOption('root', root)
            site.addOption('try_files', '$uri $uri/ @lfw')
            # Since the nginx manage 'extension' doesn't like users to set the
            # same option multiple times (which is perfectly allowed in nginx
            # configuration files for some options), we use this 1337 'space'
            # trick
            site.addOption('rewrite', '^/%s$ /%s/ permanent' % \
                (self.appName, self.appName))
            site.addOption('rewrite ', '^/%s/$ /index.html break' % \
                self.appName)
            site.addOption('rewrite  ', '^/%s/(.*) /$1 break' % self.appName)

        nginx.cmdb.save()
        nginx.applyConfig()

        config_template = '''
LFW_CONFIG = {
    'uris': {
        'listSpaces': '/%(appname)s/appserver/rest/ui/portal/spaces',
        'completion': '/%(appname)s/appserver/rest/ui/portal/tags',
        'search': '/%(appname)s/appserver/rest/ui/portal/search',
        'tags': '/%(appname)s/appserver/rest/ui/portal/tags',
        'title': '/%(appname)s/appserver/rest/ui/portal/pages',
        'pages': '/%(appname)s/appserver/rest/ui/portal/page',
        'macros': '/%(appname)s/js/macros/'
    },
    'appname' : '%(appname)s'
};
''' 

        config = config_template % {
            'appname': self.appName,
        }

        config_dir = os.path.join(root, 'js')
        config_file = os.path.join(config_dir, 'config.js')

        if not os.path.exists(config_file):
            if not os.path.isdir(config_dir):
                os.makedirs(config_dir, 0755)

            fd = open(config_file, 'w')
            try:
                fd.write(config)
            finally:
                fd.close()

    def _populatePortal (self):
        
        appName = self.appName
        appDir = q.system.fs.joinPaths( q.dirs.pyAppsDir, appName )
        modelDir = q.system.fs.joinPaths( appDir, 'interface', 'model')
        pymodel.init_domain( modelDir )
        osis.init()
        xmlRpcURL = 'http://127.0.0.1/%s/appserver/xmlrpc/' % appName
        transport = XMLRPCTransport( xmlRpcURL, 'model')
        serializer = ThriftSerializer()
        connection = OsisConnection(transport, serializer)
        MD_PATH = q.system.fs.joinPaths( appDir, 'portal', 'spaces' )
        
        macros_homepage = None
        
        for folder in q.system.fs.listDirsInDir(MD_PATH):
            files = q.system.fs.listFilesInDir(folder, filter='*.md', recursive=True)
            space = folder.split(os.sep)[-1]
        
            for f in files:
                name = q.system.fs.getBaseName(f).split('.')[0]
                content = q.system.fs.fileGetContents(f)
        
                # Check if page exists
                f = connection.ui.page.getFilterObject()
                f.add('ui_view_page_list', 'name', name, True)
                f.add('ui_view_page_list', 'space', space, True)
                page_info = connection.ui.page.findAsView(f, 'ui_view_page_list')
                if len(page_info) > 1:
                    raise ValueError('Multiple pages found ?')
                elif len(page_info) == 1:
                    page = connection.ui.page.get(page_info[0]['guid'])
                else:
                    page = connection.ui.page.new()
                    page.name = name
                    page.space = space
                    page.category = 'portal'
        
                if name.startswith('Macro') and name not in ['Macros_Home', 'Macros']:
                    if not macros_homepage:
                        #check if Macros_Home page is already created, then get its guid to set it as parent guid to other macro pages
                        filter = connection.ui.page.getFilterObject()
                        filter.add('ui_view_page_list', 'name', 'Macros_Home', True)
                        filter.add('ui_view_page_list', 'space', space, True)
                        macros_page_info = connection.ui.page.findAsView(filter, 'ui_view_page_list')
                        if len(macros_page_info) == 1:
                            macros_homepage = connection.ui.page.get(macros_page_info[0]['guid'])
                    page.parent = macros_homepage.guid
        
                # content
                page.content = content if content else 'empty'
        
                # tags
                if page.tags:
                    t = page.tags.split(' ')
                else:
                    t = []
                tags = set(t)
        
                # page and space 
                tags.add('space:%s' % space)
                tags.add('page:%s' % name)
        
                # split CamelCase in tags
                for tag in re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', name).strip().split(' '):
                    tags.add(tag)
        
                page.tags = ' '.join(tags)
                connection.ui.page.save(page)

