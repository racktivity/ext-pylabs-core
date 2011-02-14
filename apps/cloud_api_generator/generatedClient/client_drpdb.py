from cloud_api_client.Exceptions import CloudApiException

class drpdb:
    def __init__(self, proxy):
        self._proxy = proxy


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
        try:
            result = self._proxy.cloud_api_drpdb.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['drpdb'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


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
        try:
            result = self._proxy.cloud_api_drpdb.find(name,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



