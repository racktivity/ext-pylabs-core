from pylabs import q
from cloud_api_rootobjects import cloud_api_clouduserrole
from cloud_api.BaseCloudAPI import BaseCloudAPI

class clouduserrole(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_clouduserrole.clouduserrole()

    @q.manage.applicationserver.expose_authenticated
    def getXMLSchema (self, clouduserroleguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the disk rootobject structure.

        @execution_method = sync
        
        @param clouduserroleguid:       Guid of the clouduserrolerootobject
        @type clouduserroleguid:        guid

        @param jobguid:                 Guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the clouduserrole structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
	return self._rootobject.getXMLSchema(clouduserroleguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def list (self, name = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of clouduserroles info which met the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the cloud user role
        @type name:                        string
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of policy guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
	return self._rootobject.list(name,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getYAML (self, clouduserroleguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the clouduserrole rootobject.

        @execution_method = sync
        
        @param clouduserroleguid:       guid of the cloud user role rootobject
        @type clouduserroleguid:        guid

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @return:                        YAML representation of the clouduserrole
        @rtype:                         string
        
        @todo:                          Will be implemented in phase2
        
	"""
	return self._rootobject.getYAML(clouduserroleguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the cloud user role rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXML (self, clouduserroleguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the clouduserrole rootobject.

        @execution_method = sync
        
        @param clouduserroleguid:       Guid of the clouduserrole rootobject
        @type clouduserroleguid:        guid

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the clouduserrole
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
	return self._rootobject.getXML(clouduserroleguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def find (self, name = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of clouduserrole guids which meet the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the cloud user role.
        @type name:                        string
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of clouduserrole guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
	return self._rootobject.find(name,jobguid,executionparams)


