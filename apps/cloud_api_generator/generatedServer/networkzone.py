from pylabs import q
from cloud_api_rootobjects import cloud_api_networkzone
from cloud_api.BaseCloudAPI import BaseCloudAPI

class networkzone(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_networkzone.networkzone()

    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getXMLSchema(networkzoneguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.create(name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.list(networkzoneguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getYAML(networkzoneguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.updateModelProperties(networkzoneguid,name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getXML(networkzoneguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.find(name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.delete(networkzoneguid,jobguid,executionparams)


