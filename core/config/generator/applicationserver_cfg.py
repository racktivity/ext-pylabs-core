from pylabs import q
join = q.system.fs.joinPaths

def add_service(config, domain, service):
    if not service.endswith(".py"):
        return
    else:
        service = service[:-3]
    section = service if not domain else "%s.%s" % (domain, service)
    if not config.checkSection(section):
        config.addSection(section)
    config.addParam(section, 'classspec', "%s.%s" % (service, service))

class AppServerPyApps:

    def __init__(self, appName):
        self.appName = appName

    def generate_cfg(self, xmlrpc_port, rest_port, amf_port):
        cfgPath = join(q.dirs.pyAppsDir, self.appName, 'cfg')
        if not q.system.fs.exists(cfgPath):
            q.system.fs.createDir(cfgPath)
        appserverCfgPath = join(cfgPath, 'applicationserver')
        appServerCfg = q.config.getInifile(appserverCfgPath)
        if not appServerCfg.checkSection('main'):
            appServerCfg.addSection('main')
        if xmlrpc_port:
            appServerCfg.addParam('main', 'xmlrpc_port', xmlrpc_port)
            appServerCfg.addParam('main', 'xmlrpc_ip', '127.0.0.1')
        if rest_port:
            appServerCfg.addParam('main', 'rest_port', rest_port)
            appServerCfg.addParam('main', 'rest_ip', '127.0.0.1')
        if amf_port:
            appServerCfg.addParam('main', 'amf_port', amf_port)
            appServerCfg.addParam('main', 'amf_ip', '127.0.0.1')
        appServerCfg.addParam('main', 'allow_none', 'True')
        appServerCfg.addParam('main', 'mail_incoming_server', '')
        appServerCfg.write()
        self.generate_services()
        self.configure_reversieproxy(xmlrpc=xmlrpc_port, 
                                     rest=rest_port,
                                     amf=amf_port)

    def configure_reversieproxy(self, **kwargs):
        q.manage.nginx.startChanges()
        vhost = q.manage.nginx.cmdb.virtualHosts.get('80') 
        if not vhost:
            vhost = q.manage.nginx.cmdb.addVirtualHost('80')
        for name, port in kwargs.iteritems():
            reverseproxyname = "%s_%s" % (self.appName, name)
            if reverseproxyname not in vhost.reverseproxies:
                if port:
                    url = "http://127.0.0.1:%s" % port
                    location = "/%s/appserver/%s" % (self.appName, name)
                    if name == "amf":
                        url += "/"
                        location += "/"
                    vhost.addReverseProxy(reverseproxyname, url, location)
        q.manage.nginx.cmdb.save()
        q.manage.nginx.applyConfig()
        
        

    def generate_services(self):
        servicespath = join(q.dirs.pyAppsDir, self.appName, 'impl', 'service')
        cfgpath = join(q.dirs.pyAppsDir, self.appName, 'cfg', 'applicationserverservice')
        config = q.config.getInifile(cfgpath)
        if q.system.fs.exists(servicespath):
            for domainpath in q.system.fs.listDirsInDir(servicespath):
                domain = q.system.fs.getBaseName(domainpath)
                for servicepath in q.system.fs.listFilesInDir(domainpath):
                    service = q.system.fs.getBaseName(servicepath)
                    add_service(config, domain, service)
            for servicepath in q.system.fs.listFilesInDir(servicespath):
                service = q.system.fs.getBaseName(servicepath)
                add_service(config, None, service)
        config.write()
                    

