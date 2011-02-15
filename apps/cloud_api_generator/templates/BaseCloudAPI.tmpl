from pylabs import q, i
from osis.store.OsisDB import OsisDB

class BaseCloudAPI:
    connection = OsisDB().getConnection('main')
    def checkAuthentication(self, request, methodname, args, kwargs):
        if not request.username or not request.password: return False
        filterObject = self.connection.getFilterObject()
        filterObject.add('view_clouduser_list', 'login',request.username, True)
        filterObject.add('view_clouduser_list', 'password',request.password, True)
        clouduser_guids =  self.connection.objectsFind('clouduser', filterObject)
        if clouduser_guids and len(clouduser_guids) == 1:
            self.updateExecutionParams(args, kwargs, clouduser_guids[0])
            return True
        return False

    def updateExecutionParams(self, args, kwargs, clouduserguid):
        executionparams = self.getExecutionparams(args, kwargs)
        executionparams['clouduserguid']  = clouduserguid

    def getExecutionparams(self, args, kwargs):
        executionparams = dict()
        if args and len(args) >=2:
            executionparams = args[-1]
        else:
            kwargs = kwargs or dict()
            executionparams = kwargs.get('executionparams', dict())
            kwargs['executionparams'] = executionparams
        return executionparams

    def checkAuthorization(self, criteria, request, methodname, args, kwargs):
        clouduserguid = self.getExecutionparams(args, kwargs).get('clouduserguid', None)
        if not clouduserguid:
            return False
        for group in criteria['groups']:
            filterObject = self.connection.getFilterObject()
            filterObject.add('view_cloudusergroup_clouduser_list', 'name', group, True)
            filterObject.add('view_cloudusergroup_clouduser_list', 'clouduserguid', clouduserguid)
            if self.connection.objectsFind('cloudusergroup', filterObject):return True
        return False