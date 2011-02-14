from pymonkey import q

class cloudusergroup:
    def listGroups (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user groups which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid: guid of the cloud user group specified
        @type cloudusergroupguid:  guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'listGroups', params, jobguid=jobguid, executionparams=executionparams)

    def getXMLSchema (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the cloud user group rootobject structure.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group rootobject
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XSD representation of the cloud user group structure.
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def addUser (self, cloudusergroupguid, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Add an existing cloud user to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param clouduserguid:        Gui of the cloud user to add to the cloud user group specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['clouduserguid'] = clouduserguid
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'addUser', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new cloud user group
        
        @execution_method = sync
        
        @param name:                Name for this new cloud user group
        @type name:                 string

        @param description:         Description for this new cloud user group
        @type description:          string

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with cloud user group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        params['description'] = description
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def removeUserRole (self, cloudusergroupguid, clouduserroleguid, jobguid = "", executionparams = {}):
        """
        
        Remove an existing cloud user role from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param clouduserroleguid:            Guid of the cloud user role who should be removed from the cloud user group specified
        @type clouduserroleguid:             guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        params['clouduserroleguid'] = clouduserroleguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'removeUserRole', params, jobguid=jobguid, executionparams=executionparams)

    def list (self, customerguid = "", cloudusergroupguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user groups which are related to the customer specified.

        @execution_method = sync
        
        @param customerguid:         guid of the customer for which to retrieve the list of cloud user groups.
        @type customerguid:          guid

        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                      dictionary
        @note:                       Example return value:
        @note:                       {'result': '[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                     "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                                  "name": "admins",
        @note:                                                  "description": "Cloud Administrators"},
        @note:                                                 {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                                  "name": "users",
        @note:                                                  "description": "cloud user groups"}]"}]',
        @note:                        'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                    In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        params['customerguid'] = customerguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'list', params, jobguid=jobguid, executionparams=executionparams)

    def removeGroup (self, cloudusergroupguid, membercloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Remove an existing cloud user group from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param membercloudusergroupguid:     Guid of the cloud user group who should be removed from the cloud user group specified
        @type membercloudusergroupguid:      guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        params['membercloudusergroupguid'] = membercloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'removeGroup', params, jobguid=jobguid, executionparams=executionparams)

    def getYAML (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the cloud user group rootobject.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group rootobject
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         YAML representation of the cloud user group
        @rtype:                          string
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def listUsers (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud users which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid:  guid of the cloud user group specified
        @type cloudusergroupguid:   guid

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'listUsers', params, jobguid=jobguid, executionparams=executionparams)

    def listRoles (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user roles of the cloud user group

        @execution_method = sync
        
        @param cloudusergroupguid: guid of the cloud user group specified
        @type cloudusergroupguid:  guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   Dictionary of array of dictionaries with an array of cloud user roles with cloudusergroupguid
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'listRoles', params, jobguid=jobguid, executionparams=executionparams)

    def removeUser (self, cloudusergroupguid, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Remove an existing cloud user from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param clouduserguid:        Gui of the cloud user to remove from the cloud user group specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['clouduserguid'] = clouduserguid
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'removeUser', params, jobguid=jobguid, executionparams=executionparams)

    def updateModelProperties (self, cloudusergroupguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties, every parameter which is not passed or passed as empty string is not updated.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param name:                 Name for this cloud user group
        @type name:                  string

        @param description:          Description for this cloud user group
        @type description:           string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with cloud user group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        params['name'] = name
        params['description'] = description
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'updateModelProperties', params, jobguid=jobguid, executionparams=executionparams)

    def listCustomers (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud users which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'listCustomers', params, jobguid=jobguid, executionparams=executionparams)

    def addGroup (self, cloudusergroupguid, membercloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Add an existing cloud user group to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param membercloudusergroupguid:     Guid of the cloud user group who should become a member of the cloud user group specified
        @type membercloudusergroupguid:      guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        params['membercloudusergroupguid'] = membercloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'addGroup', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the cloud user group rootobject.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group rootobject
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XML representation of the cloud user group
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def addUserRole (self, cloudusergroupguid, clouduserroleguid, jobguid = "", executionparams = {}):
        """
        
        Add an existing cloud user role to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param clouduserroleguid:            Guid of the cloud user role
        @type clouduserroleguid:             guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        params['clouduserroleguid'] = clouduserroleguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'addUserRole', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, name = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user groups guids which met the find criteria.

        @execution_method = sync
        
        @param name:                    Name of the cloud user group to include in the search criteria.
        @type name:                     string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of cloud user group guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group to delete.
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['cloudusergroupguid'] = cloudusergroupguid
        executionparams['rootobjectguid'] = cloudusergroupguid
        executionparams['rootobjecttype'] = 'cloudusergroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cloudusergroup', 'delete', params, jobguid=jobguid, executionparams=executionparams)


