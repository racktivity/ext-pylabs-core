from cloud_api_rootobjects import cloud_api_clouduserrole

class clouduserrole:

    def __init__(self):
        self._rootobject = cloud_api_clouduserrole.clouduserrole()

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
        result = self._rootobject.getXMLSchema(clouduserroleguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.list(name,jobguid,executionparams)
        return result


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
        result = self._rootobject.getYAML(clouduserroleguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.getObject(rootobjectguid,jobguid,executionparams)

        from osis import ROOTOBJECT_TYPES
        import base64
        from osis.model.serializers import ThriftSerializer
        result = base64.decodestring(result['result'])
        result = ROOTOBJECT_TYPES['clouduserrole'].deserialize(ThriftSerializer, result)
        return result


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
        result = self._rootobject.getXML(clouduserroleguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.find(name,jobguid,executionparams)
        return result


