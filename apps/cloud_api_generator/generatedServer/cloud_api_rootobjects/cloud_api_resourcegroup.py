from pymonkey import q

class resourcegroup:
    def removeDevice (self, resourcegroupguid, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Removes an existing device from the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:           Guid of the resource group specified
        @type resourcegroupguid:            guid

        @param deviceguid:                  Guid of the device to remove from the resource group specified
        @type deviceguid:                   guid

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['deviceguid'] = deviceguid
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'removeDevice', params, jobguid=jobguid, executionparams=executionparams)

    def getXMLSchema (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the resource group rootobject structure.

        @execution_method = sync
        
        @param resourcegroupguid:       Guid of the resource group rootobject
        @type resourcegroupguid:        guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the resource group structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def addBackplane (self, resourcegroupguid, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Add an existing backplane to the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:   Guid of the resource group specified
        @type resourcegroupguid:    guid

        @param backplaneguid:       Guid of the backplane to add to the resource group specified
        @type backplaneguid:        guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'addBackplane', params, jobguid=jobguid, executionparams=executionparams)

    def addDevice (self, resourcegroupguid, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Adds an existing device to the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:           Guid of the resource group specified
        @type resourcegroupguid:            guid

        @param deviceguid:                  Guid of the device to add to the resource group specified
        @type deviceguid:                   guid

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['deviceguid'] = deviceguid
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'addDevice', params, jobguid=jobguid, executionparams=executionparams)

    def list (self, datacenterguid = "", resourcegroupguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of resource groups which are related to the customer specified.

        @execution_method = sync
        
        @param datacenterguid:      Guid of the datacenter to which this resource group is related
        @type datacenterguid:       guid

        @param resourcegroupguid:   Guid of the resource group specified
        @type resourcegroupguid:    guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary of array of dictionaries with customerguid, and an array of resource groups with resourcegroupguid, datacenterguid, name, description.
        @rtype:                     dictionary
        @note:                      Example return value:
        @note:                      {'result': {"datacenterguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                  "groups": "[{"resourcegroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                               "datacenterguid": "D51AD737-D29E-4505-989C-8D4E18BCAAE0",
        @note:                                               "name": "RESGROUPCUSTX",
        @note:                                               "description": "Resource group of customer x"},
        @note:                                              {"resourcegroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                               "datacenterguid": "D51AD737-D29E-4505-989C-8D4E18BCAAE0",
        @note:                                               "name": "RESGROUPCUSTX",
        @note:                                               "description": "Resource group of customer y"}]"},
        @note:                       'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['datacenterguid'] = datacenterguid
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'list', params, jobguid=jobguid, executionparams=executionparams)

    def updateModelPropertiesAdvanced (self, resourcegroupguid, datacenterguid = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties, every parameter which is not passed or passed as empty string is not updated.

        @execution_method = sync
        
        @param resourcegroupguid:   Guid of the resource group specified
        @type resourcegroupguid:    guid

        @param datacenterguid:      Guid of the datacenter to which this resource group is related
        @type datacenterguid:       guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with resource group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['datacenterguid'] = datacenterguid
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'updateModelPropertiesAdvanced', params, jobguid=jobguid, executionparams=executionparams)

    def getYAML (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the resource group rootobject.

        @execution_method = sync
        
        @param resourcegroupguid:  Guid of the resource group rootobject
        @type resourcegroupguid:   guid

        @param jobguid:            Guid of the job if avalailable else empty string
        @type jobguid:             guid

        @return:                   YAML representation of the resource group
        @rtype:                    string
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    Guid of the lan rootobject
        @type rootobjectguid:     guid

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def listMachines (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of machines which are related to the resourcegroup specified.

        @execution_method = sync
        
        @param resourcegroupguid:     Guid of the resource group specified
        @type resourcegroupguid:      guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      Dictionary of array of machines
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        @todo:                        Will be implemented in phase2
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'listMachines', params, jobguid=jobguid, executionparams=executionparams)

    def updateModelProperties (self, resourcegroupguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties, every parameter which is not passed or passed as empty string is not updated.

        @execution_method = sync
        
        @param resourcegroupguid:   Guid of the resource group specified
        @type resourcegroupguid:    guid

        @param name:                Name for this resource group
        @type name:                 string

        @param description:         Description for this resource group
        @type description:          string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with resource group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['description'] = description
        params['name'] = name
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'updateModelProperties', params, jobguid=jobguid, executionparams=executionparams)

    def listCustomers (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of customers which are related to the resourcegroup specified.

        @execution_method = sync
        
        @param resourcegroupguid:    Guid of the resource group specified
        @type resourcegroupguid:     guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     Dictionary of array of customers
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'listCustomers', params, jobguid=jobguid, executionparams=executionparams)

    def listBackplanes (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of backplanes which are related to the resourcegroup specified.

        @execution_method = sync
        
        @param resourcegroupguid:      Guid of the resource group specified
        @type resourcegroupguid:       guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary of array of backplanes
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        @todo:                         Will be implemented in phase2
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'listBackplanes', params, jobguid=jobguid, executionparams=executionparams)

    def removeBackplane (self, resourcegroupguid, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Removes an existing backplane from the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:   Guid of the resource group specified
        @type resourcegroupguid:    guid

        @param backplaneguid:       Guid of the backplane to remove from the resource group specified
        @type backplaneguid:        guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['backplaneguid'] = backplaneguid
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'removeBackplane', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the resource group rootobject.

        @execution_method = sync
        
        @param resourcegroupguid:       Guid of the resource group rootobject
        @type resourcegroupguid:        guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the resource group
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def listDevices (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of devices which are related to the resourcegroup specified.

        @execution_method = sync
        
        @param resourcegroupguid:      Guid of the resource group specified
        @type resourcegroupguid:       guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary of array of dictionaries of .
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        @todo:                         Will be implemented in phase2
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'listDevices', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, datacenterguid, name, description = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new resource group

        @execution_method = sync
        
        @param datacenterguid:      Guid of the datacenter to which this resource group is related
        @type datacenterguid:       guid

        @param name:                Name for this new resource group
        @type name:                 string

        @param description:         Description for this new resource group
        @type description:          string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with resource group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        params['datacenterguid'] = datacenterguid
        params['description'] = description
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, name = "", description = "", datacenterguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of resource groups guids which met the find criteria.

        @execution_method = sync
        
        @param name:                    Name of the resource group to include in the search criteria.
        @type name:                     string

        @param description:             Description for this new resource group
        @type description:              string

        @param datacenterguid:          Guid of the datacenter to which this resource group is related
        @type datacenterguid:           guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of resource group guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        params['datacenterguid'] = datacenterguid
        params['description'] = description
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, resourcegroupguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:       Guid of the resource group to delete.
        @type resourcegroupguid:        guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['resourcegroupguid'] = resourcegroupguid
        executionparams['rootobjectguid'] = resourcegroupguid
        executionparams['rootobjecttype'] = 'resourcegroup'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('resourcegroup', 'delete', params, jobguid=jobguid, executionparams=executionparams)


