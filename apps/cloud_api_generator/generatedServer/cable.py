from pymonkey import q
from cloud_api_rootobjects import cloud_api_cable
from cloud_api.BaseCloudAPI import BaseCloudAPI

class cable(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_cable.cable()

    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getXMLSchema(cableguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.create(name,cabletype,description,label,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.list(cableguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getYAML(cableguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.updateModelProperties(cableguid,name,cabletype,description,label,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getXML(cableguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.find(name,cabletype,description,label,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
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
	return self._rootobject.delete(cableguid,jobguid,executionparams)


