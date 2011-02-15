from pylabs import q
from cloud_api_rootobjects import cloud_api_drpdb
from cloud_api.BaseCloudAPI import BaseCloudAPI

class drpdb(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_drpdb.drpdb()

    @q.manage.applicationserver.expose_authenticated
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string
        
	"""
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def find (self, name = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of drpdb guids which met the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the machine.
        @type name:                        string
        
        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of drpdb guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
	return self._rootobject.find(name,jobguid,executionparams)


