from pymonkey import q
from cloud_api_rootobjects import cloud_api_cmc
from cloud_api.BaseCloudAPI import BaseCloudAPI

class cmc(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_cmc.cmc()

    @q.manage.applicationserver.expose_authenticated
    def checkCredentials(self):
        return True

    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getRootPolicyJobList(joblimit,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getRootMonitoringJobList(joblimit,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listAvailableTreeItems(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getChildApplications(parentapplicationguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listMachineDisks(machineguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getVirtualDesktopOverview(cloudspaceguid,istemplate,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listAvailableCommands(objecttype,objectguid,screenname,clouduserguid,cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getRootJobsList(joblimit,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getDashboard (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the dashboard page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getDashboard(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getRootErrorConditionsList(errorconditionslimit,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def GetSmartClientDevices (self, jobguid = "", executionparams = {}):
        """
        
        Gets all SMARTCLIENT devices

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.GetSmartClientDevices(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getPDiskInfo(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getMaintenanceEnviromnentOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the maintenance environment overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getMaintenanceEnviromnentOverview(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getCDUDevices (self, jobguid = "", executionparams = {}):
        """
        
        Gets all CDU devices

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getCDUDevices(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getLogicalDisks(machineguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getRRDGraph(rrdParams,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getAccessControlList (self, jobguid = "", executionparams = {}):
        """
        
        Returns the access control list for an authenticated clouduser        

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of all access items in CMC
        @type executionparams:      dictionary

        @return:                    dict
        
	"""
	return self._rootobject.getAccessControlList(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listVDisks(machineguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getTreeData (self, jobguid = "", executionparams = {}):
        """
        
        Gets all needed data to build up the cmc tree

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getTreeData(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getLoggingInformation(joblogguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getCombinedNodesOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the combined nodes overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getCombinedNodesOverview(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getUserTreeData(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getProductionEnviromnentOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the production environment overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getProductionEnviromnentOverview(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getNetworkOverview(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listAvailablePlugins(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getResourceNodesOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the resource nodes overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getResourceNodesOverview(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.updateCloudServicePosition(vdcguid,cloudserviceguid,positionx,positiony,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getDiskManagementOverview(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getCloudService(name,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getStorageNodesOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the storage nodes overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getStorageNodesOverview(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getVirtualServerOverview(cloudspaceguid,istemplate,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getSmartclientsOverview(cloudspaceguid,istemplate,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getAdministrationEnviromnentOverview (self, jobguid = "", executionparams = {}):
        """
        
        Gets all details needed to load the administration environment overview page in cmc

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getAdministrationEnviromnentOverview(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getDevices (self, jobguid = "", executionparams = {}):
        """
        
        Gets all non SMARTCLIENT devices

        @execution_method = sync

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
	"""
	return self._rootobject.getDevices(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getMachineRootJobsList(machineguid,joblimit,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getMachineDetails(machineguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getPhysicalDisks(machineguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getRaidDeviceDetails(diskguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getVdcTemplates(cloudspaceGuid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getVirtualDatacenterOverview(cloudspaceguid,jobguid,executionparams)


