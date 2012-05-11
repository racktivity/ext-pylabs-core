import os
import os.path
from pylabs import q, p
from wfe_cfg import WfePyApps
from arakoon_cfg import ArakoonPyApps
from osis_cfg import OsisPyApps
from agent_cfg import AgentPyApps
from applicationserver_cfg import AppServerPyApps

POSTGRESUSER = "postgres"
join = q.system.fs.joinPaths

def min_range(pyappsCfg):
    sections = pyappsCfg.getSections()
    if not sections:
        return 20000
    minRange = list()
    for section in sections:
        portrange = pyappsCfg.getValue(section, 'port_range')
        minRange.append(int(portrange.split(':')[1]))
    return max(minRange)


class PyAppsConfigGen:

    def __init__(self, appName):
        self.appName = appName
        self.config = None
        self.components = None
        self.user = None
        self.group = None
        self._load_config()

    def _load_config(self):
        self.config = q.config.getConfig('pyapps').get(self.appName)

        # Get the user and group used for running pyapps
        mainConfig = q.config.getConfig('main').get('main', {})
        self.user = mainConfig.get('user')
        self.group = mainConfig.get('group')

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

    def setup_postgres(self):
        from pylabs.db import DBConnection
        dbconnections = q.config.getInifile('dbconnections')
        section = "db_%s" % self.appName
        dbhost = '127.0.0.1'
        if not dbconnections.checkSection(section):
            dbconnections.addSection(section)
            dbconnections.addParam(section, 'dbtype', 'postgresql')
            dbconnections.addParam(section, 'dbserver', '127.0.0.1')
            dbconnections.addParam(section, 'dblogin', self.appName)
            dbconnections.addParam(section, 'dbpasswd', '')
            dbconnections.addParam(section, 'dbname', self.appName)
            dbconnections.write()
        else:
            dbhost = dbconnections.getValue(section, 'dbserver')

        islocal = dbhost in ('localhost', '127.0.0.1')
        postgres = q.manage.postgresql8
        if islocal and self.appName not in postgres.cmdb.databases:
            postgres.startChanges()
            if not postgres.cmdb.initialized:
                postgres.cmdb.initialized = True
                postgres.cmdb.rootLogin = POSTGRESUSER
                postgres.cmdb.addLogin(POSTGRESUSER)
            db = postgres.cmdb.addDatabase(self.appName, self.appName)
            db.initDone = True
            db.new = False
            db.addACE(self.appName, '', q.enumerators.PostgresqlAccessRightType.WRITE)
            postgres.cmdb.addLogin(self.appName,  type='host',
                    cidr_address='127.0.0.1/32',database=self.appName)
            postgres.save()
            postgres.applyConfig()
            q.manage.postgresql8.start()
            conn = DBConnection.DBConnection('127.0.0.1', 'postgres', POSTGRESUSER)
            createdb = True
            if {'datname': self.appName} in conn.sqlexecute("select datname from pg_catalog.pg_database").dictresult():
                if q.console.askYesNo('Database already exists, overwrite existing database?'):
                    q.cmdtools.postgresql8.dropdb(self.appName, POSTGRESUSER)
                else:
                    createdb = False
            if createdb:
                q.cmdtools.postgresql8.createdb(self.appName, POSTGRESUSER, self.appName)


    def setup(self):
        #create user with applicationname
        if not q.system.unix.unixUserExists(self.appName):
            q.system.unix.addSystemUser(self.appName)
        # create the user and group to be used by the new pyapp
        if self.group and not q.system.unix.unixGroupExists(self.group):
            q.system.unix.addSystemGroup(self.group)
        if self.user and self.group and not q.system.unix.unixUserExists(self.user):
            q.system.unix.addSystemUser(username=self.user, groupname=self.group, homeDir=q.dirs.baseDir)


        if 'postgresql' in self.components:
            self.setup_postgres()
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
        self._configureAuth()

        taskletpath = join(q.dirs.pyAppsDir, self.appName, 'impl', 'setup')
        if q.system.fs.exists(taskletpath):
            te = q.taskletengine.get(taskletpath)
            params = {"appname": self.appName}
            te.execute(params)

    def init(self):
        taskletpath = join(q.dirs.pyAppsDir, self.appName, 'impl', 'init')
        if q.system.fs.exists(taskletpath):
            te = q.taskletengine.get(taskletpath)
            params = {"appname": self.appName}
            te.execute(params)


    def start(self):
        params = {'appname': self.appName}
        te = None
        startpath = q.system.fs.joinPaths(q.dirs.pyAppsDir, self.appName, 'impl', 'start')
        if q.system.fs.exists(startpath):
            te = q.taskletengine.get(startpath)
            te.execute(params, tags=('pre',))
        if 'postgresql' in self.components:
            q.manage.postgresql8.start()
        if 'arakoon' in self.components:
            cluster = q.manage.arakoon.getCluster(self.appName)
            cluster.start()
        if 'appserver' in self.components:
            q.manage.applicationserver.start(self.appName)
            q.manage.nginx.start()
        if 'wfe' in self.components:
            q.manage.ejabberd.start()
            q.manage.workflowengine.start(self.appName)
        if 'event_consumers' in self.components:
            p.events.startConsumers(self.appName)
        if te:
            te.execute(params, tags=('post',))

    def stop(self):
        params = {'appname': self.appName}
        te = None
        stop = q.system.fs.joinPaths(q.dirs.pyAppsDir, self.appName, 'impl', 'stop')
        if q.system.fs.exists(stop):
            te = q.taskletengine.get(stop)
            te.execute(params, tags=('pre',))
        if 'appserver' in self.components:
            q.manage.applicationserver.stop(self.appName)
        if 'wfe' in self.components:
            q.manage.workflowengine.stop(self.appName)
        if 'arakoon' in self.components:
            cluster = q.manage.arakoon.getCluster(self.appName)
            cluster.stop()
        if 'event_consumers' in self.components:
            p.events.stopConsumers(self.appName)
        if te:
            te.execute(params, tags=('post',))

    def generateAll(self):
        # Create and set ownership for directory used to store arakoon and event consumer logs
        logDir = q.system.fs.joinPaths(q.dirs.logDir, self.appName)
        if not q.system.fs.exists(logDir):
            q.system.fs.createDir(logDir)
            if self.user and self.group:
                q.system.unix.chown(logDir, self.user, self.group)

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
        arakoon = ArakoonPyApps(self.appName, self.user, self.group)
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
        if '@lfw_macros' not in vhost.sites:
            lfw = vhost.addSite('@lfw_macros', '@lfw_macros')
            lfw.addOption('root', '/opt/qbase5/www/lfw/js/macros/')

        root = os.path.join(q.dirs.pyAppsDir, self.appName, 'portal', 'static')
        if not os.path.isdir(root):
            os.makedirs(root, 0755)

        if not self.appName in vhost.sites:
            site = vhost.addSite(self.appName, '/%s' % self.appName)
            site.addOption('root', root)
            site.addOption('try_files', '$uri $uri/ @lfw')
            site.addOption('rewrite', '^/%s$ http://$host/%s/ permanent' % \
                (self.appName, self.appName))
            site.addOption('rewrite', '^/%s/$ /index.html break' % \
                self.appName)
            site.addOption('rewrite', '^/%s/(.*) /$1 break' % self.appName)

        jsmacros = os.path.join(q.dirs.pyAppsDir, self.appName, 'impl', 'portal', 'jsmacros')
        if not os.path.isdir(jsmacros):
            os.makedirs(jsmacros, 0755)

        sitename = "%s_macros" % self.appName
        if not sitename in vhost.sites:
            site = vhost.addSite(sitename, '/%s/js/macros' % self.appName)
            site.addOption('root', jsmacros)
            site.addOption('try_files', '$uri $uri/ @lfw_macros')
            site.addOption('rewrite', '^/%s/js/macros/(.*) /$1 break' % self.appName)

        sitename = "%s_jswizards" % self.appName
        if not sitename in vhost.sites:
            site = vhost.addSite(sitename, '/%s/jswizards' % self.appName)
            site.addOption('root', '/opt/qbase5/www/jswizards/')
            site.addOption('rewrite', '^/%s/jswizards/(.*) /$1 break' % self.appName)


        nginx.cmdb.save()
        nginx.applyConfig()

        config_template = '''
LFW_CONFIG = {
    'uris': {
        'listSpaces': '/%(appname)s/appserver/rest/ui/portal/listSpaces',
        'completion': '/%(appname)s/appserver/rest/ui/portal/tags',
        'search': '/%(appname)s/appserver/rest/ui/portal/search',
        'tags': '/%(appname)s/appserver/rest/ui/portal/tags',
        'title': '/%(appname)s/appserver/rest/ui/portal/listPages',
        'pages': '/%(appname)s/appserver/rest/ui/portal/getPage',
        'breadcrumbs': '/%(appname)s/appserver/rest/ui/portal/breadcrumbs',
        'createPage': '/%(appname)s/appserver/rest/ui/portal/createPage',
        'updatePage': '/%(appname)s/appserver/rest/ui/portal/updatePage',
        'deletePage': '/%(appname)s/appserver/rest/ui/portal/deletePage',
        'users': '/%(appname)s/appserver/rest/ui/portal/listUsersInfo',
        'groups': '/%(appname)s/appserver/rest/ui/portal/listGroupsInfo',
        'rules': '/%(appname)s/appserver/rest/ui/portal/listRulesInfo',
        'createUser': '/%(appname)s/appserver/rest/ui/portal/createUser',
        'updateUser': '/%(appname)s/appserver/rest/ui/portal/updateUser',
        'deleteUser': '/%(appname)s/appserver/rest/ui/portal/deleteUser',
        'addUserToGroup': '/%(appname)s/appserver/rest/ui/portal/addUserToGroup',
        'removeUserFromGroup': '/%(appname)s/appserver/rest/ui/portal/removeUserFromGroup',
        'createGroup': '/%(appname)s/appserver/rest/ui/portal/createGroup',
        'updateGroup': '/%(appname)s/appserver/rest/ui/portal/updateGroup',
        'deleteGroup': '/%(appname)s/appserver/rest/ui/portal/deleteGroup',
        'assignRule': '/%(appname)s/appserver/rest/ui/portal/assignRule',
        'revokeRule': '/%(appname)s/appserver/rest/ui/portal/revokeRule',
        'listPossibleRules': '/%(appname)s/appserver/rest/ui/portal/listPossibleRules',
        'createSpace': '/%(appname)s/appserver/rest/ui/portal/createSpace',
        'deleteSpace': '/%(appname)s/appserver/rest/ui/portal/deleteSpace',
        'updateSpace': '/%(appname)s/appserver/rest/ui/portal/updateSpace',
        'sortSpaces': '/%(appname)s/appserver/rest/ui/portal/sortSpaces',
        'importSpace': '/%(appname)s/appserver/rest/ui/portal/importSpace',
        'exportSpace': '/%(appname)s/appserver/rest/ui/portal/exportSpace',
        'hgPushSpace': '/%(appname)s/appserver/rest/ui/portal/hgPushSpace',
        'hgPullSpace': '/%(appname)s/appserver/rest/ui/portal/hgPullSpace',
        'space': '/%(appname)s/appserver/rest/ui/portal/getSpace',
        'macros': '/%(appname)s/js/macros/',
        'macroConfig': '/%(appname)s/appserver/rest/ui/portal/macroConfig',
        'updateMacroConfig': '/%(appname)s/appserver/rest/ui/portal/updateMacroConfig',
        'oauthservice': '/%(appname)s/appserver/rest/ui/oauth/getToken',
        'checkAuthorization': '/%(appname)s/appserver/rest/ui/auth/isAuthorised',
        'myGroups': '/%(appname)s/appserver/rest/ui/portal/getMyGroups'
    },
    'appname' : '%(appname)s',
    'development'  : true
};
'''

        config = config_template % {
            'appname': self.appName}

        config_dir = os.path.join(root, 'js')
        config_file = os.path.join(config_dir, 'config.js')

        if not os.path.exists(config_file):
            if not os.path.isdir(config_dir):
                os.makedirs(config_dir, 0755)
                if self.user and self.group:
                    q.system.unix.chown(config_dir, self.user, self.group)

            fd = open(config_file, 'w')
            try:
                fd.write(config)
                if self.user and self.group:
                    q.system.unix.chown(config_file, self.user, self.group)
            finally:
                fd.close()

    def _configureAuth(self):
        def createConfig(name, template):
            configdir = os.path.join(q.dirs.pyAppsDir, self.appName, "cfg")

            if not os.path.isdir(configdir):
                os.makedirs(configdir, 0755)
                if self.user and self.group:
                    q.system.unix.chown(configdir, self.user, self.group)

            fn = os.path.join(configdir, name)

            if not os.path.exists(fn):
                fd = open(fn, "w")
                try:
                    fd.write(template)
                    if self.user and self.group:
                        q.system.unix.chown(fn, self.user, self.group)
                finally:
                    fd.close()


        auth_template = """[auth]
backend=local
insecure=1

[oauth]
hoursvalid=1
tokencleanup=10
"""

        authlocal_template = ""

        authldap_template = """[LDAP]
hostname=172.19.8.158
port=389
people_rdn=ou=people
base_dn=dc=example,dc=com
"""

        createConfig("auth.cfg", auth_template)
        createConfig("auth_local.cfg", authlocal_template)
        createConfig("auth_ldap.cfg", authldap_template)
