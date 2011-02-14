from cloud_api_client.Exceptions import CloudApiException

class cable:
    def __init__(self, proxy):
        self._proxy = proxy


    def getXMLSchema (self, cableguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the cable rootobject structure.

        @execution_method = sync
        
        @param cableguid:               Guid of the cable rootobject
        @type cableguid:                guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the cable structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_cable.getXMLSchema(cableguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, name, cabletype, description = "", label = "", jobguid = "", executionparams = {}):
        """
        
        Create a new cable.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the cable.
        @type name:                    string

        @param description:            description of the cable
        @type description:             string

        @param cabletype:              cable type
        @type cabletype:               cabletype

        @param label:                  label attached to cable
        @type label:                   string(60)

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with cableguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_cable.create(name,cabletype,description,label,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, cableguid = "", jobguid = "", executionparams = {}):
        """
        
        List all cables.

        @execution_method = sync
        
        @param cableguid:               Guid of the cable specified
        @type cableguid:                guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of cable info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'cableguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'cable0001',
        @note:                                      'description': 'cable 0001',
        @note:                                      'cabletype': 'USBCABLE'
        @note:                                      'label': ''}]}
        
        @raise e:                       In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_cable.list(cableguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, cableguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the cable rootobject.

        @execution_method = sync
        
        @param cableguid:             Guid of the cable rootobject
        @type cableguid:              guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the cable
        @rtype:                       string
        
        """
        try:
            result = self._proxy.cloud_api_cable.getYAML(cableguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the cable rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_cable.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['cable'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, cableguid, name = "", cabletype = "", description = "", label = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @security administrators
        @param cableguid:              Guid of the cable specified
        @type cableguid:               guid

        @param name:                   Name for the cable.
        @type name:                    string

        @param description:            description of the cable
        @type description:             string

        @param cabletype:              cable type
        @type cabletype:               cabletype

        @param label:                  label attached to cable
        @type label:                   string(60)

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with cable guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_cable.updateModelProperties(cableguid,name,cabletype,description,label,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, cableguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the cable rootobject.

        @execution_method = sync
        
        @param cableguid:               Guid of the cable rootobject
        @type cableguid:                guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the cable
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_cable.getXML(cableguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, name = "", cabletype = "", description = "", label = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cable guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the cable.
        @type name:                    string

        @param description:            description of the cable
        @type description:             string

        @param cabletype:              cable type
        @type cabletype:               cabletype

        @param label:                  label attached to cable
        @type label:                   string(60)

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Array of cable guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_cable.find(name,cabletype,description,label,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, cableguid, jobguid = "", executionparams = {}):
        """
        
        Delete a cable.

        @execution_method = sync
        
        @security administrators
        @param cableguid:             Guid of the cable rootobject to delete.
        @type cableguid:              guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid


        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_cable.delete(cableguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



