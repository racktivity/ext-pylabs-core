from pylabs import q, i, p
import os
basedir = os.path.join(q.dirs.pyAppsDir, p.api.appname)

class ActionService:
    
    _authenticate = q.taskletengine.get(os.path.join(basedir, 'impl', 'authenticate'))
    _authorize = q.taskletengine.get(os.path.join(basedir, 'impl', 'authorize'))
    
    def checkAuthentication(self, request, domain, service, methodname, args, kwargs):
        tags = ('authenticate',)
        params = dict()
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        ActionService._authenticate.execute(params, tags=tags)
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
        ActionService._authorize.execute(params, tags=tags)
        return params.get('result', False)
