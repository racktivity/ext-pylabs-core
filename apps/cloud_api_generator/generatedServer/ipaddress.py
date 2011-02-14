from pymonkey import q
from cloud_api_rootobjects import cloud_api_ipaddress
from cloud_api.BaseCloudAPI import BaseCloudAPI

class ipaddress(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_ipaddress.ipaddress()

    @q.manage.applicationserver.expose_authenticated
    def getXMLSchema (self, ipaddressguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the ipaddress rootobject structure.

        @execution_method = sync
        
        @param ipaddressguid:           Guid of the ipaddress rootobject
        @type ipaddressguid:            guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the ipaddress structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
	return self._rootobject.getXMLSchema(ipaddressguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def create (self, name, description = "", address = "", netmask = "", block = False, iptype = "", ipversion = "", languid = "", virtual = False, jobguid = "", executionparams = {}):
        """
        
        Create a new ipaddress.

        @security administrators

        @param name:              name of the ipaddress
        @type name:               string

        @param  description:      description of the object
        @type description:        string

        @param  address:          IP address of the IP
        @type address:            type_ipaddress

        @param  netmask:          netmask of the IP object
        @type netmask:            type_netmaskaddress

        @param  block:            flag indicating if the IP is blocked
        @type block:              boolean

        @param  iptype:           type of the IP object, STATIC or DHCP
        @type iptype:             string

        @param ipversion:         version of the IP object, IPV4 or IPV6
        @type ipversion:          string

        @param languid:           lan to which the ip is connected
        @type languid:            guid

        @param virtual            flag is if ip is a VIPA
        @type virtual             boolean 

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with ipaddressguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
	return self._rootobject.create(name,description,address,netmask,block,iptype,ipversion,languid,virtual,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def list (self, ipaddressguid = "", jobguid = "", executionparams = {}):
        """
        
        List all ipaddresss.

        @execution_method = sync
        
        @param ipaddressguid:           Guid of the ipaddress rootobject
        @type ipaddressguid:            guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of ipaddress info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised

        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'ipaddressguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'ipaddress0001',
        @note:                                      'description': 'ipaddress 0001',
        @note:                                      'address': '192.148.0.1',
        @note:                                      'netmask': '255.255.255.255',
        @note:                                      'block': '',
        @note:                                      'iptype': 'STATIC',
        @note:                                      'ipversion':'IPV4',
        @note:                                      'languid': '77544B07-4129-47B1-8690-B92C0DB2143'}]}
        
	"""
	return self._rootobject.list(ipaddressguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getYAML (self, ipaddressguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the ipaddress rootobject.

        @execution_method = sync
        
        @param ipaddressguid:         Guid of the ipaddress rootobject
        @type ipaddressguid:          guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the ipaddress
        @rtype:                       string
        
	"""
	return self._rootobject.getYAML(ipaddressguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:        Guid of the ipaddress rootobject
        @type rootobjectguid:         guid

        @return:                      rootobject
        @rtype:                       string

        @warning:                     Only usable using the python client.
        
	"""
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def updateModelProperties (self, ipaddressguid, name = "", description = "", address = "", netmask = "", block = False, iptype = "", ipversion = "", virtual = None, languid = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @security administrators

        @param ipaddressguid:          Guid of the ipaddress specified
        @type ipaddressguid:           guid

        @param name:                   name of the ipaddress
        @type name:                    string

        @param  description:           description of the object
        @type description:             string

        @param  address:               IP address of the IP
        @type address:                 type_ipaddress

        @param  netmask:               netmask of the IP object
        @type netmask:                 type_netmaskaddress

        @param  block:                 flag indicating if the IP is blocked
        @type block:                   boolean

        @param  iptype:                type of the IP object, STATIC or DHCP
        @type iptype:                  string

        @param ipversion:              version of the IP object, IPV4 or IPV6
        @type ipversion:               string

        @param languid:                lan to which the ip is connected
        @type languid:                 guid
        
        @param virtual                 flags whether ipaddress is a VIPA
        @type virtual                  boolean 

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with ipaddress guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
	return self._rootobject.updateModelProperties(ipaddressguid,name,description,address,netmask,block,iptype,ipversion,virtual,languid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXML (self, ipaddressguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the ipaddress rootobject.

        @param ipaddressguid:           Guid of the ipaddress rootobject
        @type ipaddressguid:            guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the ipaddress
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
	return self._rootobject.getXML(ipaddressguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def setState (self, ipaddressguid, status, jobguid = "", executionparams = {}):
        """
        
        Sets the state of the ip address
        
        @param ipaddressguid:           Guid of the ipaddress rootobject
        @type ipaddressguid:            guid
        
        @param status:                  status of the ipaddress
        @type status:                   string

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with boolean as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised        
        
        
	"""
	return self._rootobject.setState(ipaddressguid,status,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def find (self, name = "", description = "", address = "", netmask = "", block = False, iptype = "", ipversion = "", languid = "", cloudspaceguid = "", virtual = None, jobguid = "", executionparams = {}):
        """
        
        Returns a list of ipaddress guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        
        @param name:                    name of the ipaddress
        @type name:                     string

        @param description:             description of the object
        @type description:              string

        @param address:                 IP address of the IP object
        @type address:                  type_ipaddress

        @param netmask:                 netmask of the IP object
        @type netmask:                  type_netmaskaddress

        @param block:                   flag indicating if the IP is blocked
        @type block:                    boolean

        @param iptype:                  type of the IP object, STATIC or DHCP
        @type iptype:                   string

        @param ipversion:               version of the IP object, IPV4 or IPV6
        @type ipversion:                string

        @param languid:                 lan to which the ip is connected
        @type languid:                  guid

        @param cloudspaceguid:          cloudspaceguid to which the ip is connected
        @type cloudspaceguid:           guid
        
        @param virtual                  flag whether to include VIPA
        @type virtual                   boolean 
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of ipaddress guids which met the find criteria specified.
        @rtype:                         array

        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
	return self._rootobject.find(name,description,address,netmask,block,iptype,ipversion,languid,cloudspaceguid,virtual,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def delete (self, ipaddressguid, jobguid = "", executionparams = {}):
        """
        
        Delete a ipaddress.

        @security administrators

        @param ipaddressguid:         Guid of the ipaddress rootobject to delete.
        @type ipaddressguid:          guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
	return self._rootobject.delete(ipaddressguid,jobguid,executionparams)


