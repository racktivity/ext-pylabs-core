from pymonkey import q

class backplane:
    def listLans (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        List of all related lans to the backplane.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane rootobject
        @type backplaneguid:            guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of lans info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'listLans', params, jobguid=jobguid, executionparams=executionparams)

    def getXMLSchema (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the backplane rootobject structure.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane rootobject
        @type backplaneguid:            guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the backplane structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, name, backplanetype, description = "", publicflag = False, managementflag = False, storageflag = False, jobguid = "", executionparams = {}):
        """
        
        Create a new backplane.

        @param name:                   Name for the backplane.
        @type name:                    string

        @param backplanetype:          Type of the backplane (ETHERNET, INFINIBAND)
        @type backplanetype:           string

        @param description:            Description for the backplane.
        @type description:             string

        @param publicflag:             Indicates if the backplane is a public backplane.
        @type publicflag:              boolean

        @param storageflag:            Indicates if the backplane is a storage backplane.
        @type storageflag:             boolean

        @param managementflag:         Indicates if the backplane is a management backplane.
        @type managementflag:          boolean

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with backplaneguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['publicflag'] = publicflag
        params['name'] = name
        params['storageflag'] = storageflag
        params['backplanetype'] = backplanetype
        params['managementflag'] = managementflag
        params['description'] = description
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectAction('backplane', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def list (self, backplaneguid = "", jobguid = "", executionparams = {}):
        """
        
        List all backplanes.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane
        @type backplaneguid:            guid
 
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of backplane info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'backplaneguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'Storage Backplane',
        @note:                                      'backplanetype': 'INFINIBAND',
        @note:                                      'public': False,
        @note:                                      'storage': True,
        @note:                                      'management': False},
        @note:                                    { 'backplaneguid': '789544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'Management Backplane',
        @note:                                      'backplanetype': 'ETHERNET',
        @note:                                      'public': False,
        @note:                                      'storage': False,
        @note:                                      'management': False}]}
        
        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'list', params, jobguid=jobguid, executionparams=executionparams)

    def getYAML (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the backplane rootobject.

        @execution_method = sync
        
        @param backplaneguid:    Guid of the backplane rootobject
        @type backplaneguid:     guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 YAML representation of the backplane
        @rtype:                  string
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    Guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def updateModelProperties (self, backplaneguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @param backplaneguid:          Guid of the backplane specified
        @type backplaneguid:           guid

        @param name:                   Name for this backplane
        @type name:                    string

        @param description:            Description for this backplane
        @type description:             string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with backplane guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['description'] = description
        params['name'] = name
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectAction('backplane', 'updateModelProperties', params, jobguid=jobguid, executionparams=executionparams)

    def setFlags (self, backplaneguid, publicflag = False, managementflag = False, storageflag = False, jobguid = "", executionparams = {}):
        """
        
        Sets the role flags for the specified backplane.

        @param backplaneguid:          Guid of the backplane
        @type backplaneguid:           guid

        @param publicflag:             Defines if the backplane is used as a public backplane. Not modified if empty.
        @type publicflag:              boolean

        @param managementflag:         Defines if the backplane is used as a management backplane. Not modified if empty.
        @type managementflag:          boolean

        @param storageflag:            Defines if the backplane is used as a storage backplane. Not modified if empty.
        @type storageflag:             boolean

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['managementflag'] = managementflag
        params['storageflag'] = storageflag
        params['publicflag'] = publicflag
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectAction('backplane', 'setFlags', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the backplane rootobject.
        
        @execution_method = sync

        @param backplaneguid:    Guid of the backplane rootobject
        @type backplaneguid:     guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid


        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 XML representation of the backplane
        @rtype:                  string

        @raise e:                In case an error occurred, exception is raised

        @todo:                   Will be implemented in phase2
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, name = "", managementflag = "", publicflag = "", storageflag = "", backplanetype = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of backplane guids which met the find criteria.
        
        @execution_method = sync

        @param name:                    Name of the backplanes to include in the search criteria.
        @type name:                     string

        @param managementflag:          managementflag of the backplanes to include in the search criteria.
        @type managementflag:           boolean

        @param publicflag:              publicflag of the backplanes to include in the search criteria.
        @type publicflag:               boolean

        @param storageflag:             storageflag of the backplanes to include in the search criteria.
        @type storageflag:              boolean

        @param backplanetype:           Type of the backplanes to include in the search criteria.
        @type backplanetype:            int

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of backplane guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['managementflag'] = managementflag
        params['storageflag'] = storageflag
        params['publicflag'] = publicflag
        params['backplanetype'] = backplanetype
        params['name'] = name
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def listResourcegroups (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        List of all related resourcegroups to the backplane.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane rootobject
        @type backplaneguid:            guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of resourcegroups info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('backplane', 'listResourcegroups', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Delete a backplane.

        @param backplaneguid:          Guid of the backplane rootobject to delete.
        @type backplaneguid:           guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjectguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'backplane'

        
        return q.workflowengine.actionmanager.startRootobjectAction('backplane', 'delete', params, jobguid=jobguid, executionparams=executionparams)


