from cloud_api_client.Exceptions import CloudApiException

class datacenter:
    def __init__(self, proxy):
        self._proxy = proxy


    def listClouds (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        List all clouds of the datacenter.

        @execution_method = sync
        
        @param datacenterguid:          Guid of the datacenter specified
        @type datacenterguid:           guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of clouds
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.listClouds(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXMLSchema (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the datacenter rootobject structure.

        @execution_method = sync
        
        @param datacenterguid:           Guid of the datacenter rootobject
        @type datacenterguid:            guid

        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XSD representation of the datacenter structure.
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.getXMLSchema(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listRacks (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        List all racks of the datacenter.

        @execution_method = sync
        
        @param datacenterguid:           Guid of the datacenter specified
        @type datacenterguid:            guid
        
        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with array of racks
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        @todo:                           Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.listRacks(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, name, description = "", locationguid = "", clouduserguid = "", jobguid = "", executionparams = {}):
        """
        
        Create a new datacenter.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the datacenter.
        @type name:                    string

        @param description:            Description for the datacenter.
        @type description:             string

        @param locationguid:           guid of the location of the datacenter
        @type locationguid:            guid

        @param clouduserguid:          guid of the clouduser owning the datacenter
        @type clouduserguid:           guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with datacenterguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.create(name,description,locationguid,clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, datacenterguid = "", jobguid = "", executionparams = {}):
        """
        
        List all datacenters.

        @execution_method = sync
        
        @param datacenterguid:          Guid of the datacenter specified
        @type datacenterguid:           guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of datacenter info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'datacenterguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'datacenter0001',
        @note:                                      'description': 'datacenter 0001',
        @note:                                      'locationguid': '3351FF9F-D65A-4F65-A96B-AC4A6246C033',
        @note:                                      'clouduserguid': 'F353F79F-D65A-4F65-A96B-AC4A6246C033'}]}
        @note:                                    { 'datacenterguid': '1351F79F-D65A-4F65-A96B-AC4A6246C033',
        @note:                                      'name': 'datacenter0001',
        @note:                                      'description': 'datacenter 0001',
        @note:                                      'locationguid': '2351FF9F-D65A-4F65-A96B-AC4A6246C033',
        @note:                                      'clouduserguid': '7353F79F-D65A-4F65-A96B-AC4A6246C033'}]}
        
        @raise e:                       In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.list(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the datacenter rootobject.

        @execution_method = sync
        
        @param datacenterguid:        Guid of the datacenter rootobject
        @type datacenterguid:         guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the datacenter
        @rtype:                       string
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.getYAML(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the datacenter rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['datacenter'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listNetworkzones (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        List all network zones of the datacenter.

        @execution_method = sync
        
        @param datacenterguid:          Guid of the datacenter specified
        @type datacenterguid:           guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of network zones
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.listNetworkzones(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, datacenterguid, name = "", description = "", locationguid = "", clouduserguid = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @security administrators
        @param datacenterguid:         Guid of the datacenter specified
        @type datacenterguid:          guid

        @param name:                   Name for the datacenter.
        @type name:                    string

        @param description:            Description for the datacenter.
        @type description:             string

        @param locationguid:           guid of the location of the datacenter
        @type locationguid:            guid

        @param clouduserguid:          guid of the clouduser owning the datacenter
        @type clouduserguid:           guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with datacenter guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.updateModelProperties(datacenterguid,name,description,locationguid,clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the datacenter rootobject.

        @execution_method = sync
        
        @param datacenterguid:           Guid of the datacenter rootobject
        @type datacenterguid:            guid

        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XML representation of the datacenter
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.getXML(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, name = "", description = "", locationguid = "", clouduserguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of datacenter guids which met the find criteria.

        @execution_method = sync
        
        @security administrators

        @param name:                   Name for the datacenter.
        @type name:                    string

        @param description:            Description for the datacenter.
        @type description:             string

        @param locationguid:           guid of the location of the datacenter
        @type locationguid:            guid

        @param clouduserguid:          guid of the clouduser owning the datacenter
        @type clouduserguid:           guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Array of datacenter guids which met the find criteria specified.
        @rtype:                        array
        @note:                         Example return value:
        @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.find(name,description,locationguid,clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listResourceGroups (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        List all resource groups of the datacenter.

        @execution_method = sync
        
        @param datacenterguid:           Guid of the datacenter specified
        @type datacenterguid:            guid
        
        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with array of clouds
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        @todo:                           Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.listResourceGroups(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        Delete a datacenter.

        @execution_method = sync
        
        @security administrators
        @param datacenterguid:        Guid of the datacenter rootobject to delete.
        @type datacenterguid:         guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_datacenter.delete(datacenterguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



