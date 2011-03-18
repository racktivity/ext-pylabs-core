import sys
from pylabs import q
from pylabs.baseclasses import BaseEnumeration

class AppContext(BaseEnumeration):
    def __repr__(self):
        return str(self)

AppContext.registerItem('action')
AppContext.registerItem('actor')
AppContext.registerItem('client')
AppContext.finishItemRegistration()


class AppManager(object):
    
    def __init__(self):
        pass
    
    def getAPI(self, appname, host=None, context=None):
        '''Retrieve api object for an application'''
        return ApplicationAPI(appname, host, context)
        
        
        
class ApplicationAPI(object):
    
    def __init__(self, appname, host=None, context=None):
        app_path = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', appname)
        api_path = q.system.fs.joinPaths(app_path, 'impl')
        sys.path.append(api_path)
        
        # @todo:  load depending on context
        self.appname = appname
        self.action = self._get_actions(appname, context)
        self.actor = self._get_actors(appname, context)
        self.model = None
        
    def _get_actors(self, appname, context):
        from actor import actors
        return actors()

    def _get_actions(self, appname, context):
        from action import actions
        return actions()
        
        
        
    
        
        
        
        