from pylabs import q

class clouduserrole:
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
        params =dict()
        params['clouduserroleguid'] = clouduserroleguid
        executionparams['rootobjectguid'] = clouduserroleguid
        executionparams['rootobjecttype'] = 'clouduserrole'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('clouduserrole', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

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
        params =dict()
        params['name'] = name
        executionparams['rootobjecttype'] = 'clouduserrole'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('clouduserrole', 'list', params, jobguid=jobguid, executionparams=executionparams)

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
        params =dict()
        params['clouduserroleguid'] = clouduserroleguid
        executionparams['rootobjectguid'] = clouduserroleguid
        executionparams['rootobjecttype'] = 'clouduserrole'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('clouduserrole', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

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
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'clouduserrole'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('clouduserrole', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

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
        params =dict()
        params['clouduserroleguid'] = clouduserroleguid
        executionparams['rootobjectguid'] = clouduserroleguid
        executionparams['rootobjecttype'] = 'clouduserrole'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('clouduserrole', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

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
        params =dict()
        params['name'] = name
        executionparams['rootobjecttype'] = 'clouduserrole'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('clouduserrole', 'find', params, jobguid=jobguid, executionparams=executionparams)


