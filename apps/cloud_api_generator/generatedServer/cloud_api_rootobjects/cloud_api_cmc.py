from pymonkey import q

class cmc:
    def getRootPolicyJobList (self, joblimit = 40, jobguid = "", executionparams = {}):
        """
        
        Gets all root policy jobs used as overview in cmc

        @execution_method = sync

        @param joblimit             number of jobs to display
        @type joblimit              int

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['joblimit'] = joblimit
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getRootPolicyJobList', params, jobguid=jobguid, executionparams=executionparams)

    def getRootMonitoringJobList (self, joblimit = 40, jobguid = "", executionparams = {}):
        """
        
        Gets all root monitoring jobs used as overview in cmc

        @execution_method = sync

        @param joblimit             number of jobs to display
        @type joblimit              int

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['joblimit'] = joblimit
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getRootMonitoringJobList', params, jobguid=jobguid, executionparams=executionparams)

    def listAvailableTreeItems (self, clouduserguid = "", jobguid = "", executionparams = {}):
        """
        
        @execution_method = sync
        
        @param jobguid:              Guid of the cloud user
        @type jobguid:               guid
        
        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of tree info (as dict) as result and jobguid
        @rtype:                      dictionary
        
	"""
        params =dict()
        params['clouduserguid'] = clouduserguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'listAvailableTreeItems', params, jobguid=jobguid, executionparams=executionparams)

    def getChildApplications (self, parentapplicationguid, jobguid = "", executionparams = {}):
        """
        
        Returns the applicationguid(s) of the instanciated cloudservice

        @execution_method = sync

        @param parentapplicationguid:   guid of the application
        @type parentapplicationguid:    guid

        @param jobguid:                 Guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dict

        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['parentapplicationguid'] = parentapplicationguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getChildApplications', params, jobguid=jobguid, executionparams=executionparams)

    def listMachineDisks (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        List the disks for a given machine.

        @execution_method = sync
        
        @param machineguid:          guid of the machine to list the backups from.
        @type  machineguid:          guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of disks info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'listMachineDisks', params, jobguid=jobguid, executionparams=executionparams)

    def getVirtualDesktopOverview (self, cloudspaceguid, istemplate = False, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the virtual desktop overview page in cmc

        @execution_method = sync

        @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        @type cloudspaceGuid:       guid

		@param istemplate:          Boolean indicating if the list returns templates or not
        @type istemplate:           Boolean

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['istemplate'] = istemplate
        params['cloudspaceguid'] = cloudspaceguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getVirtualDesktopOverview', params, jobguid=jobguid, executionparams=executionparams)

    def listAvailableCommands (self, objecttype = "", objectguid = "", screenname = "", clouduserguid = "", cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of available commands for the user on a given object of a given type for a given screen.

        @execution_method = sync

        @param objecttype:          Name of the object type for which you want to list the actions
        @type objecttype:           string

        @param objectguid:          Guid of the object for which you want to retrieve the action for (for the current user)
        @type objectguid:           guid

        @param screenname:          Name of the screen for which you want to retrieve the actions for
        @type screenname:           string
        
        @param clouduserguid:       Guid of the user for which you want to retrieve the action for 
        @type clouduserguid:        guid

        @param cloudspaceguid:      Guid of the cloudspace for which you want to retrieve the action for 
        @type cloudspaceguid:       guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dict

        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'icon': 'machine_start.ico',
        @note:                                      'name': 'machine_start',
        @note:                                      'label': 'Start Machine',
        @note:                                      'description': 'Start Machine Command',
        @note:                                      'parameters': {
        @note:                                           'guid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                       }},
        @note:                                   {  'icon': 'machine_stop.ico',
        @note:                                      'name': 'machine_stop',
        @note:                                      'label': 'Stop Machine'
        @note:                                      'description': 'Stop Machine Command',,
        @note:                                      'parameters': {
        @note:                                           'machineguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                       }}]}
        
	"""
        params =dict()
        params['clouduserguid'] = clouduserguid
        params['screenname'] = screenname
        params['objectguid'] = objectguid
        params['cloudspaceguid'] = cloudspaceguid
        params['objecttype'] = objecttype
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'listAvailableCommands', params, jobguid=jobguid, executionparams=executionparams)

    def getRootJobsList (self, joblimit = 40, jobguid = "", executionparams = {}):
        """
        
        Gets all root jobs used as overview in cmc

        @execution_method = sync

        @param joblimit             number of jobs to display
        @type joblimit              int

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['joblimit'] = joblimit
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getRootJobsList', params, jobguid=jobguid, executionparams=executionparams)

    def getDashboard (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the dashboard page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getDashboard', params, jobguid=jobguid, executionparams=executionparams)

    def getRootErrorConditionsList (self, errorconditionslimit = 40, jobguid = "", executionparams = {}):
        """
        
        Gets all root error conditions used as overview in cmc

        @execution_method = sync

        @param errorconditionslimit     number of error conditions to display
        @type errorconditionslimit      int

        @param jobguid:                 Guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary
        
	"""
        params =dict()
        params['errorconditionslimit'] = errorconditionslimit
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getRootErrorConditionsList', params, jobguid=jobguid, executionparams=executionparams)

    def GetSmartClientDevices (self, jobguid = "", executionparams = {}):
        """
        
        Gets all SMARTCLIENT devices

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'GetSmartClientDevices', params, jobguid=jobguid, executionparams=executionparams)

    def getPDiskInfo (self, jobguid = "", executionparams = {}):
        """
        
        Returns pdisk information

        @execution_method = sync
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     path to the generated graph
        @type executionparams:      dictionary

        @return:                    dict
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getPDiskInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getMaintenanceEnviromnentOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the maintenance environment overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getMaintenanceEnviromnentOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getCDUDevices (self, jobguid = "", executionparams = {}):
        """
        
        Gets all CDU devices

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getCDUDevices', params, jobguid=jobguid, executionparams=executionparams)

    def getLogicalDisks (self, machineguid = "", jobguid = "", executionparams = {}):
        """
        
        Get all logical disks for specified pmachine or all physical disks from the environment.
        
        @execution_method = sync
        
        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getLogicalDisks', params, jobguid=jobguid, executionparams=executionparams)

    def getRRDGraph (self, rrdParams = {}, jobguid = "", executionparams = {}):
        """
        
        Returns the path to the generated RRD graph

        @execution_method = sync
        
        @param rrdParams:           Dictionary of all parameters needed to generate the RRD graph
        @type rrdParams:            dictionary

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     path to the generated graph
        @type executionparams:      dictionary

        @return:                    dict
        
	"""
        params =dict()
        params['rrdParams'] = rrdParams
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getRRDGraph', params, jobguid=jobguid, executionparams=executionparams)

    def getAccessControlList (self, jobguid = "", executionparams = {}):
        """
        
        Returns the access control list for an authenticated clouduser        

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of all access items in CMC
        @type executionparams:      dictionary

        @return:                    dict
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectAction('cmc', 'getAccessControlList', params, jobguid=jobguid, executionparams=executionparams)

    def listVDisks (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets all vdisks attached to specified pmachine

        @execution_method = sync

        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'listVDisks', params, jobguid=jobguid, executionparams=executionparams)

    def getTreeData (self, jobguid = "", executionparams = {}):
        """
        
        Gets all needed data to build up the cmc tree

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getTreeData', params, jobguid=jobguid, executionparams=executionparams)

    def getLoggingInformation (self, joblogguid, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the logging page (jobs and events) in cmc

        @execution_method = sync

        @param joblogguid:          Guid of the job from which to get the logging information
        @type joblogguid:           guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['joblogguid'] = joblogguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getLoggingInformation', params, jobguid=jobguid, executionparams=executionparams)

    def getCombinedNodesOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the combined nodes overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getCombinedNodesOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getUserTreeData (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Gets all needed data to build up the cmc user management tree

        @execution_method = sync

        @param customerguid:        Guid of the customer
        @type customerguid:         guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['customerguid'] = customerguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getUserTreeData', params, jobguid=jobguid, executionparams=executionparams)

    def getProductionEnviromnentOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the production environment overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getProductionEnviromnentOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getNetworkOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the network overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @todo:                      Will be implemented in phase2
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getNetworkOverview', params, jobguid=jobguid, executionparams=executionparams)

    def listAvailablePlugins (self, jobguid = "", executionparams = {}):
        """
        
        @execution_method = sync
        
        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of plugin info (as dict) as result and jobguid
        @rtype:                      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'listAvailablePlugins', params, jobguid=jobguid, executionparams=executionparams)

    def getResourceNodesOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the resource nodes overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getResourceNodesOverview', params, jobguid=jobguid, executionparams=executionparams)

    def updateCloudServicePosition (self, vdcguid, cloudserviceguid, positionx, positiony, jobguid = "", executionparams = {}):
        """
        
        Updates the coordinates of a cloudservcie in the database

        @execution_method = sync

        @param vdcguid:             Guid of the vdc
        @type vdcguid:              guid

        @param cloudserviceguid:    Guid of the cloudservice
        @type cloudserviceguid:     guid

        @param positionx:           X coordinates of the item in the vdc gui
        @type positionx:            int

        @param positiony:           Y coordinates of the item in the vdc gui
        @type positiony:            int

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['positionx'] = positionx
        params['positiony'] = positiony
        params['vdcguid'] = vdcguid
        params['cloudserviceguid'] = cloudserviceguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'updateCloudServicePosition', params, jobguid=jobguid, executionparams=executionparams)

    def getDiskManagementOverview (self, cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns disk information on virtual disks in SSO

        @execution_method = sync
        
        @param cloudspaceguid:      Guid of the cloudspace to filter on
        @type cloudspaceguid:       guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     path to the generated graph
        @type executionparams:      dictionary

        @return:                    dict
        
	"""
        params =dict()
        params['cloudspaceguid'] = cloudspaceguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getDiskManagementOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getCloudService (self, name = "", jobguid = "", executionparams = {}):
        """
        
        Returns the applicationguid(s) of the instanciated cloudservice

        @execution_method = sync

        @param name:                Name of the cloud service template
        @type name:                 string

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dict

        @todo:                      Will be implemented in phase2
        
	"""
        params =dict()
        params['name'] = name
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getCloudService', params, jobguid=jobguid, executionparams=executionparams)

    def getStorageNodesOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the storage nodes overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getStorageNodesOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getVirtualServerOverview (self, cloudspaceguid, istemplate = False, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the virtual server overview page in cmc

        @execution_method = sync

        @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        @type cloudspaceGuid:       guid

	    @param istemplate:          Boolean indicating if the list returns templates or not
        @type istemplate:           Boolean

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['istemplate'] = istemplate
        params['cloudspaceguid'] = cloudspaceguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getVirtualServerOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getSmartclientsOverview (self, cloudspaceguid, istemplate = False, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the smartclients overview page in cmc

        @execution_method = sync

        @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        @type cloudspaceGuid:       guid

		@param istemplate:          Boolean indicating if the list returns templates or not
        @type istemplate:           Boolean

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['istemplate'] = istemplate
        params['cloudspaceguid'] = cloudspaceguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getSmartclientsOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getAdministrationEnviromnentOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the administration environment overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getAdministrationEnviromnentOverview', params, jobguid=jobguid, executionparams=executionparams)

    def getDevices (self, jobguid = "", executionparams = {}):
        """
        
        Gets all non SMARTCLIENT devices

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getDevices', params, jobguid=jobguid, executionparams=executionparams)

    def getMachineRootJobsList (self, machineguid, joblimit = 40, jobguid = "", executionparams = {}):
        """
        
        Gets all root jobs from the specified machine

        @execution_method = sync

        @param machineguid:         Guid of the machine
        @type machineguid:          guid
        
        @param joblimit             number of jobs to display
        @type joblimit              int


        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['joblimit'] = joblimit
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getMachineRootJobsList', params, jobguid=jobguid, executionparams=executionparams)

    def getMachineDetails (self, machineguid = "", jobguid = "", executionparams = {}):
        """
        
        Get information about a single machine
        
        @execution_method = sync
        
        @param machineguid:         Guid of the machine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getMachineDetails', params, jobguid=jobguid, executionparams=executionparams)

    def getPhysicalDisks (self, machineguid = "", jobguid = "", executionparams = {}):
        """
        
        Get all physical disks for specified pmachine or all physical disks from the environment.
        
        @execution_method = sync
        
        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getPhysicalDisks', params, jobguid=jobguid, executionparams=executionparams)

    def getRaidDeviceDetails (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Retrieve RAID device details for specified disk (partition level).
        
        @execution_method = sync
        
        @param diskguid:            Guid of the disk
        @type diskguid:             guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getRaidDeviceDetails', params, jobguid=jobguid, executionparams=executionparams)

    def getVdcTemplates (self, cloudspaceGuid = "", jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load a vdc in cmc

        @execution_method = sync

        @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        @type cloudspaceGuid:       guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
        params =dict()
        params['cloudspaceGuid'] = cloudspaceGuid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getVdcTemplates', params, jobguid=jobguid, executionparams=executionparams)

    def getVirtualDatacenterOverview (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the virtual datacenter overview page in cmc

        @execution_method = sync

        @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        @type cloudspaceGuid:       guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @todo:                      Will be implemented in phase2
        
	"""
        params =dict()
        params['cloudspaceguid'] = cloudspaceguid
        executionparams['rootobjecttype'] = 'cmc'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('cmc', 'getVirtualDatacenterOverview', params, jobguid=jobguid, executionparams=executionparams)


