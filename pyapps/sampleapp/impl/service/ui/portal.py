import os.path

from pylabs import q, p

from alkira.lfw import *
from actionservice import ActionService
basedir = os.path.join(q.dirs.pyAppsDir, p.api.appname)


class portal(LFWService, ActionService):
    def __init__(self):
	
        # Initialize API
        self.connection = p.api.model.ui
        module = os.path.abspath(os.path.dirname(__file__))
        tasklet_path = os.path.abspath(os.path.join(module, '..', '..', 'portal'))
        self._tasklet_engine = q.taskletengine.get(tasklet_path)
        self.db_config_path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'dbconnections.cfg')

    @q.manage.applicationserver.expose_authorized()
    def page(self, space, name):
        return super(portal, self).page(space, name)
    def checkAuthentication(self, request, domain, service, methodname, args, kwargs):
        #if not request.username or not request.password: return False
        tags = ('authenticate',)
        params = dict()
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        _authenticate = q.taskletengine.get(os.path.join(basedir, 'impl', 'authenticate'))
        
        _authenticate.execute(params, tags=tags)
        return params.get('result', False)

    def checkAuthorization(self, criteria, request, domain, service, methodname, args, kwargs):
        tags = ('authorize',)
        params = dict()
        params['criteria'] = criteria
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        _authorize = q.taskletengine.get(os.path.join(basedir, 'impl', 'authorize'))
   
        _authorize.execute(params, tags=tags)
        return params.get('result', False)
