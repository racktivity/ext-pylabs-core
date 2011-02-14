from pymonkey import q
from cloud_api_rootobjects import cloud_api_vdc
from cloud_api.BaseCloudAPI import BaseCloudAPI

class vdc(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_vdc.vdc()

    @q.manage.applicationserver.expose_authenticated
    def restore (self, sourcevdcguid, destinationvdcguid = "", jobguid = "", executionparams = {}):
        """
        
        @param sourcevdcguid defines which machines need to be restored (all machines in that VDC)
        
        @param destinationvdcguid is the VDC where will be restored to if not specified will be the original VDC where the backup originated from and machines in that VDC will be overwritten !!!
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.restore(sourcevdcguid,destinationvdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listCloudServices (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud services for a given VDC.

        @execution_method = sync
        
        @param vdcguid:          guid of the VDC for which to retrieve the list of cloud services.
        @type vdcguid:           guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of dictionaries with applicationguid, applicationname, languid, lanname, machineguid, machinename, positionx, positiony, status and array of connections for each cloud service.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '[{"cloudserviceguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                   "applicationguid": "", "applicationname": "",
        @note:                                 "languid":"", "lanname": "",
        @note:                                   "machineguid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "machinename": "SQL 2005",
        @note:                                   "positionx":"10", "positiony":"10",
        @note:                                   "status":"DEPLOYED",
        @note:                                   "connections":"E1734C86-AC26-46CA-82C7-216C91B44C8A",
        @note:                                   "icon": ""}',
        @note:                                 {"cloudserviceguid": "E1734C86-AC26-46CA-82C7-216C91B44C8A",
        @note:                                   "applicationguid": "", "applicationname": "",
        @note:                                 "languid":"A475F49E-9B98-41B5-AA19-2F69B2393B40", "lanname": "qlan1",
        @note:                                   "machineguid": "", "machinename": "",
        @note:                                   "positionx":"100", "positiony":"100",
        @note:                                   "status":"DEPLOYED",
        @note:                                   "connections":['22544B07-4129-47B1-8690-B92C0DB21434'],
        @note:                                   "icon": ""}',"}]'
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.listCloudServices(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addApplication (self, vdcguid, applicationguid, positionx, positiony, jobguid = "", executionparams = {}):
        """
        
        Adds an application as a cloudservice to the specified VDC.

        @execution_method = sync
        
        @param vdcguid:          guid of the VDC specified
        @type vdcguid:           guid

        @param applicationguid:  guid of the application to add to the specified VDC
        @type applicationguid:   guid

        @param positionx:        X coodinate on the VDC canvas
        @type positionx:         int

        @param positiony:        Y coodinate on the VDC canvas
        @type positiony:         int

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.addApplication(vdcguid,applicationguid,positionx,positiony,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listExportedImages (self, vdcguid, cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Gets a the list of exported vdc images on the systemNAS for a specific vdc

        @param vdcguid:           guid of the vdc rootobject
        @type vdcguid:            guid

        @param cloudspaceguid:    guid of the machine rootobject
        @type cloudspaceguid:     guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  list of exported images.
        @rtype:                   array

        @raise e:                 In case an error occurred, exception is raised              
        
	"""
	return self._rootobject.listExportedImages(vdcguid,cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addConnection (self, vdcguid, sourcerootobjectguid, destinationrootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Adds a connection between two cloud services in the specified VDC.

        @execution_method = sync
        
        @param vdcguid:                     guid of the VDC specified
        @type vdcguid:                      guid

        @param sourcerootobjectguid:        guid of the source rootobject
        @type sourcerootobjectguid:         guid

        @param destinationrootobjectguid:   guid of the destination rootobject
        @type destinationrootobjectguid:    guid

        @param jobguid:                     guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @return:                            dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
	"""
	return self._rootobject.addConnection(vdcguid,sourcerootobjectguid,destinationrootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def find (self, cloudspaceguid = "", name = "", status = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of VDC guids which met the find criteria.

        @execution_method = sync
        
        @param cloudspaceguid:    guid of the parent cloudspace to include in the search criteria.
        @type cloudspaceguid:     guid

        @param name:              Name of the VDC to include in the search criteria.
        @type name:               string

        @param status:            Status of the  VDC to include in the search criteria. See listStatuses().
        @type status:             string

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Array of VDC guids which met the find criteria specified.
        @rtype:                   array
        @note:                    Example return value:
        @note:                    {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                 In case an error occurred, exception is raised
        
	"""
	return self._rootobject.find(cloudspaceguid,name,status,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def removeMachine (self, vdcguid, machineguid, jobguid = "", executionparams = {}):
        """
        
        Removes a machine from the specified VDC.

        @execution_method = sync
        
        @param vdcguid:         guid of the VDC specified
        @type vdcguid:          guid

        @param machineguid:     guid of the machine to add to the specified VDC
        @type machineguid:      guid

        @param jobguid:         guid of the job if available else empty string
        @type jobguid:          guid

        @param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:  dictionary

        @return:                dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                 dictionary

        @raise e:               In case an error occurred, exception is raised
        
	"""
	return self._rootobject.removeMachine(vdcguid,machineguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def pause (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Pauses all machines in VDC

        @param vdcguid:          guid of the VDC to specified.
        @type vdcguid:           guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.pause(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addLan (self, vdcguid, languid, positionx, positiony, jobguid = "", executionparams = {}):
        """
        
        Adds a lan as a cloudservice to the specified VDC.

        @execution_method = sync
        
        @param vdcguid:           guid of the VDC specified
        @type vdcguid:            guid

        @param languid:           guid of the lan to add to the specified VDC
        @type languid:            guid

        @param positionx:         X coodinate on the VDC canvas
        @type positionx:          int

        @param positiony:         Y coodinate on the VDC canvas
        @type positiony:          int

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
	return self._rootobject.addLan(vdcguid,languid,positionx,positiony,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def create (self, cloudspaceguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new VDC in the space specified

        @execution_method = sync
        
        @param cloudspaceguid:        guid of the cloud space specified
        @type cloudspaceguid:         guid

        @param name:                  Name for this new VDC
        @type name:                   string

        @param description:           Description for this new VDC
        @type description:            string

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with cloud space guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
	return self._rootobject.create(cloudspaceguid,name,description,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def reboot (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Reboots all machines in VDC

        @param vdcguid:          guid of the VDC to specified.
        @type vdcguid:           guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.reboot(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def executeQshellScript (self, vdcguid, qshellScriptContent, jobguid = "", executionparams = {}):
        """
        
        Execute a Q-Shell script on all machines in VDC.
        This function requires a Q-Agent on every machine
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.executeQshellScript(vdcguid,qshellScriptContent,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def moveToSpace (self, vdcguid, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Moves the VDC specified to an other space. VDC can only be moved to spaces for which the authenticated user has sufficient rights.

        @param vdcguid:          guid of the VDC to move.
        @type vdcguid:           guid

        @param cloudspaceguid:   guid of the cloud space to which the VDC will be moved.
        @type cloudspaceguid:    guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.moveToSpace(vdcguid,cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def start (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Starts all machines in VDC

        @param vdcguid:          guid of the VDC to specified.
        @type vdcguid:           guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.start(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def updateModelProperties (self, vdcguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @param vdcguid:          guid of the vdc specified
        @type vdcguid:           guid

        @param name:             Name for this new VDC
        @type name:              string

        @param description:      Description for this new VDC
        @type description:       string

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with vdc guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.updateModelProperties(vdcguid,name,description,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addMachine (self, vdcguid, machineguid, positionx, positiony, jobguid = "", executionparams = {}):
        """
        
        Adds a machine as a cloudservice to the specified VDC.

        @execution_method = sync
        
        @param vdcguid:         guid of the VDC specified
        @type vdcguid:          guid

        @param machineguid:     guid of the machine to add to the specified VDC
        @type machineguid:      guid

        @param positionx:       X coodinate on the VDC canvas
        @type positionx:        int

        @param positiony:       Y coodinate on the VDC canvas
        @type positiony:        int

        @param jobguid:         guid of the job if avalailable else empty string
        @type jobguid:          guid

        @param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:  dictionary

        @return:                dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                 dictionary

        @raise e:               In case an error occurred, exception is raised
        
	"""
	return self._rootobject.addMachine(vdcguid,machineguid,positionx,positiony,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def rollback (self, vdcguid, backuplabel, jobguid = "", executionparams = {}):
        """
        
        Rolls back a snapshot for all machines in VDC.

        @param vdcguid:          guid of the VDC to specified.
        @type vdcguid:           guid

        @param backuplabel:      Label of the backupset to use for restore.
        @type backuplabel:       string

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.rollback(vdcguid,backuplabel,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def resume (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Resumes all machines in VDC

        @param vdcguid:          guid of the VDC to specified.
        @type vdcguid:           guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.resume(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def clone (self, sourcevdcguid, destinationcloudspaceguid = "", copynetworkinfo = True, maintenancemode = False, autostart = True, jobguid = "", executionparams = {}):
        """
        
        Create a clone of a complete VDC.
        For the machines: cloning means the blocks on the disks are not copied, only the changes are remembered.

        @param sourcevdcguid:                 guid of the VDC rootobject
        @type sourcevdcguid:                  guid

        @param destinationcloudspaceguid:     guid of the VDC rootobject. If not specified, VDC will be cloned in the same space as the source VDC.
        @type destinationcloudspaceguid:      guid
        @note:                                if in same space:
        @note:                                -----------------
        @note:                                * all rootobject properties will be copied over apart from
        @note:                                ** new guid's
        @note:                                ** the machine.name = original + _clone_vX (x being incremental nr)
        @note:                                * For the network lan's, the machine's stay connected to the same LAN's but new ip addresses are looked for on those LAN's

        @note:                                if in different space
        @note:                                ---------------------
        @note:                                * all rootobject properties will be copied over
        @note:                                * new network LAN's are created with as name $originalLanName_clone_vX X being incremental nr
        @note:                                * the ip addresses are 100% the same as the original ip addresses
        @note:                                * for the private LAN's: the VLAN's are ALL NEW!!! There is always 100% separation between spaces for private LAN's
        @note:                                * for the public LAN's: the machine's stay connected to the same LAN's but new ip addresses are looked for on those LAN's

        @param copynetworkinfo:               Boolean value indicating if the network info should be copied. Default is True.
        @type copynetworkinfo:                boolean

        @param maintenancemode:               Boolean value indicating if cloned VDC should be put in maintenance mode. Default is False.
        @type maintenancemode:                boolean
        @note:                                 if maintenancemode==True
        @note:                                ------------------------
        @note:                                * then all LAN's will get a different vlan tag
        @note:                                * new network LAN's are created with as name $originalLanName_clone_vX X being incremental nr
        @note:                                * the ip addresses are 100% the same as the original ip addresses

        @param autostart:                     Boolean value indicating if the machine of the new VDC should start automatically. Default is True.
        @type autostart:                      boolean

        @param jobguid:                       guid of the job if avalailable else empty string
        @type jobguid:                        guid

        @param executionparams:               dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:                dictionary

        @return:                              dictionary with vdc guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                               dictionary

        
	"""
	return self._rootobject.clone(sourcevdcguid,destinationcloudspaceguid,copynetworkinfo,maintenancemode,autostart,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def stop (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Stops all machines in VDC
        Leaves storage connections & network bridges intact

        @param vdcguid:            guid of the VDC to specified.
        @type vdcguid:             guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                    dictionary
        
        @raise e:                  In case an error occurred, exception is raised
        
	"""
	return self._rootobject.stop(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def initialize (self, vdcguid, start = False, jobguid = "", executionparams = {}):
        """
        

        Initializes a vdc based on the model (walk through all cloud services of that vdc and do an initialize).

        @param vdcguid:                    guid of the VDC to initialize.
        @type vdcguid:                     guid

        @param start:                      Start machines after initialize.
        @type start:                       boolean

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @todo:                             Will be implemented in phase2
        
	"""
	return self._rootobject.initialize(vdcguid,start,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXML (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the VDC rootobject.

        @execution_method = sync
        
        @param vdcguid:            guid of the VDC rootobject
        @type vdcguid:             guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   XML representation of the VDC
        @rtype:                    string

        @raise e:                  In case an error occurred, exception is raised

        @todo:                     Will be implemented in phase2
        
	"""
	return self._rootobject.getXML(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def importFromURI (self, vdcguid, sourceuri, executormachineguid = "", jobguid = "", cloudspaceguid = "", executionparams = {}):
        """
        
        Imports a VDC from the source location specified.
        Export rootobject info

        @param vdcguid:                    guid of the VDC to specified.
        @type vdcguid:                     guid

        @param sourceuri:                  URI of the location holding an exported VDC. (e.g ftp://login:passwd@myhost.com/backups/myvdc/)
        @type sourceuri:                   string

        @param executormachineguid:        guid of the machine which should convert the disk to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:         guid

        @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:             guid

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
	return self._rootobject.importFromURI(vdcguid,sourceuri,executormachineguid,jobguid,cloudspaceguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def copy (self, sourcevdcguid, destinationcloudspaceguid = "", copynetworkinfo = True, maintenancemode = False, autostart = True, jobguid = "", executionparams = {}):
        """
        
        See clone action but this case is copy instead of clone.
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        
	"""
	return self._rootobject.copy(sourcevdcguid,destinationcloudspaceguid,copynetworkinfo,maintenancemode,autostart,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def removeLan (self, vdcguid, languid, jobguid = "", executionparams = {}):
        """
        
        Removes a lan from to the specified VDC.

        @execution_method = sync
        
        @param vdcguid:          guid of the VDC specified
        @type vdcguid:           guid

        @param languid:          guid of the lan to add to the specified VDC
        @type languid:           guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.removeLan(vdcguid,languid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXMLSchema (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the VDC rootobject structure.

        @execution_method = sync
        
        @param vdcguid:            guid of the VDC rootobject
        @type vdcguid:             guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   XSD representation of the VDC structure.
        @rtype:                    string

        @raise e:                  In case an error occurred, exception is raised

        @todo:                     Will be implemented in phase2
        
	"""
	return self._rootobject.getXMLSchema(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def exportToURI (self, vdcguid, destinationuri, executormachineguid = "", compressed = True, imagetype = "vdi", jobguid = "", executionparams = {}):
        """
        
        Exports all macine of the VDC specified as vdi image on defined destination.
        Export rootobject info

        @param vdcguid:              guid of the VDC to specified.
        @type vdcguid:               guid

        @param destinationuri:       URI of the location where the VDI should be stored. (e.g ftp://login:passwd@myhost.com/backups/myvdc/)
        @type destinationuri:        string

        @param executormachineguid:  guid of the machine which should convert the disk to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:   guid

        @param compressed            Boolean value indicating if all exported machines should be compressed. Compression used is 7zip
        @type:                       boolean

        @param imagetype             Type of image format to use.
        @type imagetype:             string
        @note:                       Supported export formats are : "vdi", "parallels", "qcow2", "vvfat", "vpc", "bochs", "dmg", "cloop", "vmdk", "qcow", "cow", "host_device", "raw"

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised

        
	"""
	return self._rootobject.exportToURI(vdcguid,destinationuri,executormachineguid,compressed,imagetype,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def list (self, cloudspaceguid = "", vdcguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of virtual datacenters (VDCs) for a given cloudspace/vdc.

        @execution_method = sync
        
        @param cloudspaceguid:   guid of the cloudspace for which to retrieve the list of VDCs.
        @type cloudspaceguid:    guid

        @param vdcguid:          guid of the vdc
        @type vdcguid:           guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of dictionaries with guid, name and status for each VDC.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "vdc1", "status": "DEPLOYED"},
        @note:                                {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "name": "vdc2", "status": "DEPLOYING"}]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.list(cloudspaceguid,vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getYAML (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the vdc rootobject.

        @execution_method = sync
        
        @param vdcguid:            guid of the vdc rootobject
        @type vdcguid:             guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   YAML representation of the vdc
        @rtype:                    string
        
	"""
	return self._rootobject.getYAML(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def removeConnection (self, vdcguid, sourcecloudserviceguid, destinationcloudserviceguid, jobguid = "", executionparams = {}):
        """
        
        Removes a connection between two cloud services in the specified VDC.

        @execution_method = sync
        
        @param vdcguid:                      guid of the VDC specified
        @type vdcguid:                       guid

        @param sourcecloudserviceguid:       guid of the cloud service to connect
        @type sourcecloudserviceguid:        guid

        @param destinationcloudserviceguid:  guid of the cloud service to connect
        @type destinationcloudserviceguid:   guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
	"""
	return self._rootobject.removeConnection(vdcguid,sourcecloudserviceguid,destinationcloudserviceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listStatuses (self, jobguid = "", executionparams = {}):
        """
        
        Returns a list of possible VDC statuses.

        @execution_method = sync
        
        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of statuses.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '["DELETED","DEPLOYED","DEPLOYING","DISABLED","ERROR","MODIFIED"]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.listStatuses(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def removeApplication (self, vdcguid, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Removes an application from to the specified VDC.

        @execution_method = sync
        
        @param vdcguid:          guid of the VDC specified
        @type vdcguid:           guid

        @param applicationguid:  guid of the application to add to the specified VDC
        @type applicationguid:   guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.removeApplication(vdcguid,applicationguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def snapshot (self, vdcguid, backuplabel, jobguid = "", executionparams = {}):
        """
        
        Creates snapshots of all machines in VDC

        @param vdcguid:          guid of the VDC to specified.
        @type vdcguid:           guid

        @param backuplabel:      Label which will be put on all snapshots of all machines of this VDC.
        @type backuplabel:       string

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.snapshot(vdcguid,backuplabel,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getConfigurationString (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Generate the configuration string for the given vdc 

        @param vdcguid:           guid of the vdc
        @type vdcguid:            guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  string containing configuration data
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised
        
	"""
	return self._rootobject.getConfigurationString(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def backup (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        backup all machines in VDC
        also backup all metadata to do with VDC (e.g. network info)
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.backup(vdcguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def delete (self, vdcguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the VDC specified.

        @param vdcguid:            guid of the VDC to delete.
        @type vdcguid:             guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                    dictionary
        
        @raise e:                  In case an error occurred, exception is raised
        
	"""
	return self._rootobject.delete(vdcguid,jobguid,executionparams)


