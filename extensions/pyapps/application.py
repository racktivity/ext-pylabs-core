import sys
from pylabs import q, p
from pylabs.baseclasses import BaseEnumeration
from pylabs.config.generator import PyAppsConfigGen

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
    
    def getAPI(self, appname, host='127.0.0.1', context=None):
        '''Retrieve api object for an application'''
        return ApplicationAPI(appname, host, context)
    
    def install (self, appname):
        p.core.codemanagement.api.generate(appname)
        gen = PyAppsConfigGen(appname)
        q.action.start("Generating config for %s" % appname)
        gen.generateAll()
        q.action.stop()
        q.action.start("Setting up %s" % appname)
        gen.setup()
        q.action.stop()
        q.action.start("Restarting %s" % appname)
        gen.stop()
        gen.start()
        q.action.stop()
        q.action.start("Initializing %s" % appname)
        gen.init()
        q.action.stop()

    def syncPortal(self, appname):
        from alkira.sync_md_to_lfw import sync_to_alkira
        sync_to_alkira(appname)
        
    def start(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.start()
    
    def stop(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.stop()
 
    def restart(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.stop()
        gen.start()

    def getOsisConnection(self, appname):
        from osis.store.OsisDB import OsisDB
        osis = OsisDB().getConnection(appname)
        return osis

class ApplicationAPI(object):
    
    def __init__(self, appname, host=None, context=None):
        
        # Default to client context
        context = context or q.enumerators.AppContext.CLIENT
        
        app_path = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', appname)
        self._app_path = app_path
        self._host = host
        
        api_path = q.system.fs.joinPaths(app_path)
        sys.path.append(api_path)

        self.appname = appname
        self.action = self._get_actions(appname, context)

        categories = ('model', 'config', 'monitoring')
        
        if not context == q.enumerators.AppContext.CLIENT:
            for category in categories:
                client = self._get_osis_client(appname, category)
                setattr(self, category, client)

            if context == q.enumerators.AppContext.WFE:
                self.actor = self._get_actors(appname, context)
            
        
    def _get_actors(self, appname, context):
        from client.actor import actors
        return actors()

    def _get_actions(self, appname, context):
        
        proxy = None
        if context == q.enumerators.AppContext.CLIENT:
            proxy = XmlRpcActionProxy('http://%s/%s/appserver/xmlrpc/' % (self._host, appname))
        
        from client.action import actions
        return actions(proxy=proxy)
    
    def _get_osis_client(self, appname, category):
        import os.path

        import pymodel
        from pymodel import serializers

        from osis.client import connection, xmlrpc

        def list_(path_):
            subdirs = ((entry, os.path.join(path_, entry)) for entry in os.listdir(path_)
                if os.path.isdir(os.path.join(path_, entry)))

            for (name, subdir) in subdirs:
                models = pymodel.load_models(subdir)

                for model in models:
                    yield ((category, name, model.__name__), model)

        def load(path_, transport_, serializer_):
            return connection.generate_client(list_(path_), transport_, serializer_)

        path = os.path.join(self._app_path, 'interface', category)
        transport_uri = 'http://%s/%s/appserver/xmlrpc/' % (self._host, appname)
        transport = xmlrpc.XMLRPCTransport(transport_uri, 'osissvc')
        serializer = serializers.ThriftSerializer

        return load(path, transport, serializer)
        
import xmlrpclib
class XmlRpcActionProxy(object):
    
    def __init__(self, url):
        self.client = xmlrpclib.ServerProxy(url, allow_none=True)
    
    def __call__(self, domainname, classname, methodname, *args):

        try:
            m = getattr(self.client, domainname)
            m = getattr(m, classname)
            m = getattr(m, methodname)
            
            return m(*args)
        except AttributeError, ae:
            raise 
        except Exception, e:
            raise
        

        
