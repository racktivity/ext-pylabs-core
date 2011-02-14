from cloud_api_client.Exceptions import CloudApiException

class networkzone:
    def __init__(self, proxy):
        self._proxy = proxy


    def getXMLSchema (self, networkzoneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the networkzone rootobject structure.

        @execution_method = sync
        
        @param networkzoneguid:         Guid of the networkzone rootobject
        @type networkzoneguid:          guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the networkzone structure.
        @rtype:                          string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.getXMLSchema(networkzoneguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, name, description = "", public = False, datacenterguid = "", parentnetworkzoneguid = "", ranges = [], jobguid = "", executionparams = {}):
        """
        
        Create a new networkzone.

        @security administrators
        @param name:                   name of the networkzone
        @type name:                    string

        @param description:            description of the object
        @type description:             string

        @param public:                 is this network zone public to the internet
        @type public:                  bool

        @param datacenterguid:         guid of the datacenter
        @type datacenterguid:          guid

        @param parentnetworkzoneguid:  guid of the parantnetworkzoneguid
        @type parentnetworkzoneguid:   guid

        @param ranges:                 list of networkzoneranges
        @type ranges:                  array(networkzonerange)

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with networkzoneguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.create(name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, networkzoneguid = "", jobguid = "", executionparams = {}):
        """
        
        List all networkzones.

        @execution_method = sync
        
        @param networkzoneguid:         Guid of the networkzone specified
        @type networkzoneguid:          guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of networkzone info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'networkzoneguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'networkzone0001',
        @note:                                      'description': 'networkzone 0001',
        @note:                                      'public': False
        @note:                                      'datacenterguid': 'B2744B07-4129-47B1-8690-B92C0DB21434'
        @note:                                      'parentnetworkzoneguid': 'A2744B07-4129-47B1-8690-B92C0DB21434'
        @note:                                      'ranges': []}]}
        
        @raise e:                       In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.list(networkzoneguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, networkzoneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the networkzone rootobject.

        @execution_method = sync
        
        @param networkzoneguid:       Guid of the networkzone rootobject
        @type networkzoneguid:        guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the networkzone
        @rtype:                       string
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.getYAML(networkzoneguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the networkzone rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['networkzone'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, networkzoneguid, name = "", description = "", public = False, datacenterguid = "", parentnetworkzoneguid = "", ranges = [], jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @security administrators

        @param networkzoneguid:        Guid of the networkzone specified
        @type networkzoneguid:         guid

        @param name:                   name of the networkzone
        @type name:                    string

        @param description:            description of the object
        @type description:             string

        @param public:                 is this network zone public to the internet
        @type public:                  bool

        @param datacenterguid:         guid of the datacenter
        @type datacenterguid:          guid

        @param parentnetworkzoneguid:  guid of the parantnetworkzoneguid
        @type parentnetworkzoneguid:   guid

        @param ranges:                 list of networkzoneranges
        @type ranges:                  array(networkzonerange)

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with networkzone guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.updateModelProperties(networkzoneguid,name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, networkzoneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the networkzone rootobject.

        @execution_method = sync
        
        @param networkzoneguid:         Guid of the networkzone rootobject
        @type networkzoneguid:          guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the networkzone
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.getXML(networkzoneguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, name = "", description = "", public = False, datacenterguid = "", parentnetworkzoneguid = "", ranges = [], jobguid = "", executionparams = {}):
        """
        
        Returns a list of networkzone guids which met the find criteria.

        @execution_method = sync
        
        @security administrators

        @param name:                   name of the networkzone
        @type name:                    string

        @param description:            description of the object
        @type description:             string

        @param public:                 is this network zone public to the internet
        @type public:                  bool

        @param datacenterguid:         guid of the datacenter
        @type datacenterguid:          guid

        @param parentnetworkzoneguid:  guid of the parantnetworkzoneguid
        @type parentnetworkzoneguid:   guid

        @param ranges:                 list of networkzoneranges
        @type ranges:                  array(networkzonerange)

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Array of networkzone guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.find(name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, networkzoneguid, jobguid = "", executionparams = {}):
        """
        
        Delete a networkzone.

        @security administrators

        @param networkzoneguid:       Guid of the networkzone rootobject to delete.
        @type networkzoneguid:        guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_networkzone.delete(networkzoneguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



