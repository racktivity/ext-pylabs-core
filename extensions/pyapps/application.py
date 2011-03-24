import sys
from pylabs import q, p
from pylabs.baseclasses import BaseEnumeration
from pylabs.config.generator import PyAppsConfigGen
import pymodel
import osis

class AppContext(BaseEnumeration):
    def __repr__(self):
        return str(self)

AppContext.registerItem('appserver')
AppContext.registerItem('wfe')
AppContext.registerItem('client')
AppContext.finishItemRegistration()


class AppManager(object):
    
    def __init__(self):
        pass
    
    def getAPI(self, appname, host=None, context=None):
        '''Retrieve api object for an application'''
        return ApplicationAPI(appname, host, context)
    
    def initialize(self, appname):
        p.core.codemanagement.api.generate(appname)
        gen = PyAppsConfigGen(appname)
        gen.generateAll()
        gen.setup()
        
    def start(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.start()
    
    def stop(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.stop()
        
class ApplicationAPI(object):
    
    def __init__(self, appname, host=None, context=None):
        app_path = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', appname)
        self._app_path = app_path
        
        api_path = q.system.fs.joinPaths(app_path)
        sys.path.append(api_path)

        self.appname = appname
        self.action = self._get_actions(appname, context)
        
        if not context == q.enumerators.AppContext.CLIENT:
            self.model = self._get_model(appname, context)
            
            if context == q.enumerators.AppContext.WFE:
                self.actor = self._get_actors(appname, context)
            
        
    def _get_actors(self, appname, context):
        from client.actor import actors
        return actors()

    def _get_actions(self, appname, context):
        from client.action import actions
        return actions()
    
    def _get_model(self, appname, context):
        
        pymodel.init_domain(q.system.fs.joinPaths(self._app_path, 'interface', 'pymodel'))
        osis.init()
        
        from pymodel.serializers import ThriftSerializer
        from osis.client.xmlrpc import XMLRPCTransport
        from osis.client import OsisConnection
        
        transporturl = 'http://127.0.0.1/%s/appserver/xmlrpc/' % appname
        transport = XMLRPCTransport(transporturl, 'osissvc')
        connection = OsisConnection(transport, ThriftSerializer)

        return connection

        
        
        
    
        
        
        
        
