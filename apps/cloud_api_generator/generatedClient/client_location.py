from cloud_api_client.Exceptions import CloudApiException

class location:
    def __init__(self, proxy):
        self._proxy = proxy


    def getXMLSchema (self, locationguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the location rootobject structure.

        @execution_method = sync
        
        @param locationguid:            Guid of the location rootobject
        @type locationguid:             guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the location structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_location.getXMLSchema(locationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, name, description = "", alias = "", address = "", city = "", country = "", public = False, jobguid = "", executionparams = {}):
        """
        
        Create a new location.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the location.
        @type name:                    string

        @param description:            Description for the location.
        @type description:             string

        @param alias:                  Alias for the location.
        @type alias:                   string

        @param address:                Address for the location.
        @type address:                 string

        @param city:                   City for the location.
        @type city:                    string

        @param country:                Country for the location.
        @type country:                 string

        @param public:                 Indicates if the location is a public location.
        @type public:                  boolean

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with locationguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_location.create(name,description,alias,address,city,country,public,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, locationguid = "", jobguid = "", executionparams = {}):
        """
        
        List all locations.

        @execution_method = sync
        
        @param locationguid:            Guid of the location specified
        @type locationguid:             guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of location info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised

        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'locationguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'LOCATION0001',
        @note:                                      'description': 'Location 0001',
        @note:                                      'alias': 'LOC-0001',
        @note:                                      'address': 'Antwerpsesteenweg 19',
        @note:                                      'city': 'Lochristi'
        @note:                                      'country': 'Belgium'
        @note:                                      'public': False},
        @note:                                    { 'locationguid': '1351F79F-D65A-4F65-A96B-AC4A6246C033',
        @note:                                      'name': 'LOCATION0001',
        @note:                                      'description': 'Location 0001',
        @note:                                      'alias': 'LOC-0001',
        @note:                                      'address': 'Antwerpsesteenweg 19',
        @note:                                      'city': 'Lochristi'
        @note:                                      'country': 'Belgium'
        @note:                                      'public': False}]}
        
        """
        try:
            result = self._proxy.cloud_api_location.list(locationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, locationguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the location rootobject.

        @execution_method = sync
        
        @param locationguid:          Guid of the location rootobject
        @type locationguid:           guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the location
        @rtype:                       string
        
        """
        try:
            result = self._proxy.cloud_api_location.getYAML(locationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:        Guid of the location rootobject
        @type rootobjectguid:         guid

        @return:                      rootobject
        @rtype:                       string

        @warning:                     Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_location.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['location'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, locationguid, name = "", description = "", alias = "", address = "", city = "", country = "", public = False, timezonename = "", timezonedelta = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @security administrators
        @param locationguid:           Guid of the location specified
        @type locationguid:            guid

        @param name:                   Name for the location.
        @type name:                    string

        @param description:            Description for the location.
        @type description:             string

        @param alias:                  Alias for the location.
        @type alias:                   string

        @param address:                Address for the location.
        @type address:                 string

        @param city:                   City for the location.
        @type city:                    string

        @param country:                Country for the location.
        @type country:                 string

        @param public:                 Indicates if the location is a public location.
        @type public:                  boolean

        @param timezonename:           name of timeZone for the location.
        @type timezonename:            string

        @param timezonedelta:          delta of timeZone for the location.
        @type timezonedelta:           float

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with location guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_location.updateModelProperties(locationguid,name,description,alias,address,city,country,public,timezonename,timezonedelta,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listDatacenters (self, locationguid, jobguid = "", executionparams = {}):
        """
        
        List all datacenters of the location.
        
        @execution_method = sync
        
        @param locationguid:            Guid of the location rootobject
        @type locationguid:             guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of datacenters
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_location.listDatacenters(locationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, locationguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the location rootobject.

        @execution_method = sync
        
        @param locationguid:            Guid of the location rootobject
        @type locationguid:             guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the location
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_location.getXML(locationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def setTimeZone (self, locationguid, timezonename, timezonedelta = "", jobguid = "", executionparams = {}):
        """
        
        Changes the time zone for a certain location
        
        @security administrators
        
        @param locationguid:            Guid of the location rootobject
        @type locationguid:             guid
        
        @param timezonename:            name of timeZone for the location.
        @type timezonename:             string

        @param timezonedelta:           delta of timeZone for the location.
        @type timezonedelta:            float
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary
        
        @return:                        dictionary with True as a result when succeeded
        @rtype:                         dictionary
        
        @raise e:                       In case an error occurred, exception is raised        
        
        """
        try:
            result = self._proxy.cloud_api_location.setTimeZone(locationguid,timezonename,timezonedelta,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, name = "", description = "", alias = "", address = "", city = "", country = "", public = False, jobguid = "", executionparams = {}):
        """
        
        Returns a list of location guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the location.
        @type name:                    string

        @param description:            Description for the location.
        @type description:             string

        @param alias:                  Alias for the location.
        @type alias:                   string

        @param address:                Address for the location.
        @type address:                 string

        @param city:                   City for the location.
        @type city:                    string

        @param country:                Country for the location.
        @type country:                 string

        @param public:                 Indicates if the location is a public location.
        @type public:                  boolean

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Array of location guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_location.find(name,description,alias,address,city,country,public,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, locationguid, jobguid = "", executionparams = {}):
        """
        
        Delete a location.

        @execution_method = sync
        
        @security administrators
        @param locationguid:          Guid of the location rootobject to delete.
        @type locationguid:           guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_location.delete(locationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



