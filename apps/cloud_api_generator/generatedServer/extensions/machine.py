from cloud_api_rootobjects import cloud_api_machine

class machine:

    def __init__(self):
        self._rootobject = cloud_api_machine.machine()

    def restore (self, backupmachineguid, restoremachineguid = "", jobguid = "", executionparams = {}):
        """
        
        Restores a snapshot of a machine on another machine.

        @param backupmachineguid:          guid of the backup machine to restore.
        @type  backupmachineguid:          guid

        @param restoremachineguid:         guid of the machine to restore the backup on.  If not specified, the backup will be restored on the machine from which the backup was taken from.
        @type  restoremachineguid:         guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.restore(backupmachineguid,restoremachineguid,jobguid,executionparams)
        return result


    def bootInRecoverMode (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        make sure machine boots in recovery mode (a special network booted linux which gives access to local disk, ...)
        on recovery machine applications like mc, krusader, disk mgmt tools, ... are installed
        the pmachine will be booted with ip network config as specified in DRP
        
        when vmachine: use minimal memory properties
        
        FLOW
        #set machine.bootstatus=... to go to recovery mode
        #actor:  Installserver.bootInRecoverMode(...

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the physical machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        """
        result = self._rootobject.bootInRecoverMode(machineguid,jobguid,executionparams)
        return result


    def attachToDevice (self, machineguid, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Forces a machine to run on a particular device.
        (will use resourcegroups underneath)

        @param machineguid:                guid of the machine to attach to a device.
        @type  machineguid:                guid

        @param deviceguid:                 guid of the device to attach the machine to.
        @type  deviceguid:                 guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.attachToDevice(machineguid,deviceguid,jobguid,executionparams)
        return result


    def changePassword (self, machineguid, username, newpassword, jobguid = "", executionparams = {}):
        """
        
        Changes the password on a pmachine using new pass word
        
        @security admin
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param username               username
        @type username                string
        
        @param newpassword            new password of the user
        @type newpassword             string

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.changePassword(machineguid,username,newpassword,jobguid,executionparams)
        return result


    def addCapacityProvided (self, machineguid, amount, capacityunittype, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Adds provided capacity for the machine specified.

        @param machineguid:          guid of the machine specified
        @type machineguid:           guid

        @param amount:               Amount of capacity units to add
        @type amount:                integer

        @param capacityunittype:     Type of capacity units to add. See ca.capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param name:                 Name of capacity units to add.
        @type name:                  string

        @param description:          Description of capacity units to add.
        @type type:                  string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
        """
        result = self._rootobject.addCapacityProvided(machineguid,amount,capacityunittype,name,description,jobguid,executionparams)
        return result


    def getMaximumAllowedIPCount (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Retrieve the maximum allowed ip addresses on the specified machine
        
        @param machineguid:           guid of the machine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      number of maximum allowed ip addresses or -1 for unlimited number
        @rtype:                       integer

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getMaximumAllowedIPCount(machineguid,jobguid,executionparams)
        return result


    def find (self, name = "", assetid = "", alias = "", description = "", macaddress = "", hostname = "", status = "", hypervisor = "", defaultgateway = "", agentguid = "", deviceguid = "", parentmachineguid = "", osguid = "", clouduserguid = "", ownerguid = "", cloudspaceguid = "", resourcegroupguid = "", machinetype = "", template = "", boot = "", customsettings = "", backup = "", backuplabel = "", consistent = "", isbackup = "", ipaddress = "", machinerole = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of machine guids which met the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the machine.
        @type name:                        string

        @param assetid:                    Asset ID.
        @type assetid:                     string

        @param alias:                      Alias of the machine.
        @type alias:                       string

        @param description:                Description for this machine
        @type description:                 string

        @param macaddress:                 MAC address of a NIC on the machine.
        @type macaddress:                  string

        @param hostname:                   Hostname of the machine.
        @type hostname:                    string

        @param status:                     Status of the machine   CONFIGURED|IMAGEONLY|HALTED|RUNNING|OVERLOADED|PAUSED|TODELETE|STOPPING|STARTING|DELETING
        @type status:                      string

        @param hypervisor:                 Hypervisor of the machine.
        @type hypervisor:                  string

        @param defaultgateway:             Default gateway ip addr
        @type defaultgateway:              ipaddress

        @param agentguid:                  Guid of the agent.
        @type agentguid:                   guid

        @param deviceguid:                 Guid of the device.
        @type deviceguid:                  guid

        @param parentmachineguid:          Guid of the parent machine
        @type parentmachineguid:           guid

        @param osguid:                     Guid of the OS.
        @type osguid:                      guid

        @param clouduserguid:              Guid of the clouduser, owning this machine
        @type clouduserguid:               guid

        @param ownerguid:                  Guid of the owner.
        @type ownerguid:                   guid

        @param cloudspaceguid:             Guid of the space to which this machine belongs
        @type cloudspaceguid:              guid

        @param resourcegroupguid:          Guid of the resource group to which this machine belongs
        @type resourcegroupguid:           guid

        @param machinetype:                Machine type.
        @type machinetype:                 string

        @param template:                   Is template, when template used as example for an machine
        @type template:                    bool

        @param boot:                       Flag indicating that this machine must be automatically started when rebooting the parent machine
        @type boot:                        bool

        @param customsettings:             Custom settings and configuration of machine, is XML, to be used freely
        @type customsettings:              string

        @param backup:                     Indicates if the machine should be included in the backup policies.
        @type backup:                      boolean

        @param backuplabel:                Backuplabel of the machine.
        @type backuplabel:                 string

        @param consistent:                 Indicates if consitent backups are taken.
        @type consistent:                  boolean

        @param isbackup:                   Indicates if the machine is a backup.
        @type isbackup:                    boolean
        
        @param ipaddress:                  ipaddress of the machine.
        @type ipaddress:                   string

        @param machinerole:                role of the machine.
        @type machinerole:                 string       

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of machine guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.find(name,assetid,alias,description,macaddress,hostname,status,hypervisor,defaultgateway,agentguid,deviceguid,parentmachineguid,osguid,clouduserguid,ownerguid,cloudspaceguid,resourcegroupguid,machinetype,template,boot,customsettings,backup,backuplabel,consistent,isbackup,ipaddress,machinerole,jobguid,executionparams)
        return result


    def createFromTemplate (self, cloudspaceguid, templatemachineguid, name, languids = [], description = "", parentmachineguid = "", defaultgateway = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new machine based on a template, template defined as machine identified by templatemachineguid.

        @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:             guid

        @param templatemachineguid:        guid of the machine this machine will be based on.
        @type  templatemachineguid:        guid

        @param name:                       Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                        string

        @param languids:                   Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        @type languids:                    array

        @param description:                Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type description:                 string
        
        @param parentmachineguid:          guid of the machine this machine will be created upon.
        @type  parentmachineguid:          guid
        
        @param defaultgateway:             Default gateway of the machine (can be of a private/public lan)
        @type defaultgateway:              string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.createFromTemplate(cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,defaultgateway,jobguid,executionparams)
        return result


    def pause (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Pauses a machine.

        @param machineguid:                guid of the machine to pause.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.pause(machineguid,jobguid,executionparams)
        return result


    def exportMachineTemplates (self, templates = [], jobguid = "", executionparams = {}):
        """
        
        Exports template machines to the SystemNAS
       
        @params templates         list of template of dict containing machine guids and destination URI
        @type template            list
         
        @param jobguid:           Guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        """
        result = self._rootobject.exportMachineTemplates(templates,jobguid,executionparams)
        return result


    def rollback (self, machineguid, snapshotmachineguid, jobguid = "", executionparams = {}):
        """
        
        Rolls a machine back to a given machine snapshot.

        @param machineguid:                guid of the machine to rollback.
        @type  machineguid:                guid

        @param snapshotmachineguid:        guid of the machine snapshot to rollback to.
        @type  snapshotmachineguid:        guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.rollback(machineguid,snapshotmachineguid,jobguid,executionparams)
        return result


    def updateMonitor (self, machineguid, order, name = "", width = "", height = "", bpp = "", jobguid = "", executionparams = {}):
        """
        
        Update monitor configuration of the specified machine
        
        @param machineguid:           Guid of the machine
        @type machineguid:            guid
        
        @param order:                 Order of the monitor [0-7]
        @type order:                  integer
        
        @param name:                  Name of the monitor
        @type name:                   string
        
        @param width:                 monitor width
        @type width:                  integer
        
        @param height:                monitor height
        @type height:                 integer
        
        @param bpp:                   bits per pixel of the monitor
        @type bpp:                    integer
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with result and jobguid: {'result': boolean, 'jobguid': guid} 
        @rtype:                       dict
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.updateMonitor(machineguid,order,name,width,height,bpp,jobguid,executionparams)
        return result


    def stop (self, machineguid, clean = True, timeout = 900, jobguid = "", executionparams = {}):
        """
        
        Stops a machine.

        @param machineguid:                guid of the machine to stop.
        @type  machineguid:                guid
        
        @param clean:                      soft shutdown if true else power off
        @type clean:                       boolean
        
        @param timeout:                    time (in seconds) to wait for the machine to stop 
        @type timeout:                     int

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.stop(machineguid,clean,timeout,jobguid,executionparams)
        return result


    def resizeCPU (self, machineguid, nrcpu = 1, cpufrequency = 0, jobguid = "", executionparams = {}):
        """
        
        for vmachine resize cpu
        when pmachine certain maintenance actions will happen to make sure machine is initialized to be used in cloud

        Updates the memory of a machine.

        @param machineguid:                guid of the machine to rollback.
        @type  machineguid:                guid

        @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided. Not updated if empty.
        @type nrcpu:                       int

        @param cpufrequency:               CPU frequency in MHz. Not updated if empty.
        @type cpufrequency:                int

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.resizeCPU(machineguid,nrcpu,cpufrequency,jobguid,executionparams)
        return result


    def setSnapshotRetentionPolicy (self, machineguid, policyguid, jobguid = "", executionparams = {}):
        """
        
        Sets the snapshot retention policy for machine

        @param machineguid:                guid of the machine to set retention policy.
        @type machineguid:                 guid
        
        @param policyguid:                 guid of the retention policy to set
        @type policyguid:                  guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.setSnapshotRetentionPolicy(machineguid,policyguid,jobguid,executionparams)
        return result


    def setVideoMode (self, machineguid, order, xres, yres, bpp, jobguid = "", executionparams = {}):
        """
        
        Gets the video mode for a machine controlled by its hypervisor.
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param order:                 Number of the monitor [0-7]
        @type order:                  integer
        
        @param xres:                  horizontal resolution
        @type xres:                   int
        
        @param yres:                  vertical resolution
        @type yres:                   int
        
        @param bpp:                   bits per pixel
        @type bpp:                    int

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with jobguid and result True/False
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.setVideoMode(machineguid,order,xres,yres,bpp,jobguid,executionparams)
        return result


    def getXML (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the machine rootobject.

        @execution_method = sync
        
        @param machineguid:             guid of the machine rootobject
        @type machineguid:              guid

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid
        
        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the machine
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        result = self._rootobject.getXML(machineguid,jobguid,executionparams)
        return result


    def getRole (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Retrieves the role for a machine. Possible roles are CPUNODE, STORAGENODE, COMBINEDNODE

        @execution_method = sync
        
        @param machineguid:                  guid of the machine rootobject
        @type machineguid:                   guid

        @param jobguid:                      guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with machine role as result and jobguid: {'result': string, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        @security administrators
        
        """
        result = self._rootobject.getRole(machineguid,jobguid,executionparams)
        return result


    def getApplianceAgent (self, jobguid = "", executionparams = {}):
        """
        
        Retrieves the Agent GUID for the Appliance.

        @execution_method = sync
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with Appliance machine.agentguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getApplianceAgent(jobguid,executionparams)
        return result


    def exportToURI (self, machineguid, destinationuri, executormachineguid = "", compressed = True, diskimagetype = "vdi", jobguid = "", executionparams = {}):
        """
        
        Exports a machine to a given URI.
        Export is set of vdi's in a given directory (no metadata is being stored).

        @param machineguid:                guid of the machine to export.
        @type  machineguid:                guid

        @param destinationuri:             URI of the location where export should be stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/)
        @type destinationuri:              string

        @param executormachineguid:        guid of the machine which should export the machine. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:         guid

        @param compressed:                 If True, the machine export will be compressed using 7zip compression
        @type compressed:                  boolean

        @param diskimagetype:              Type of the disk image format (VDI, RAW, VMDK, ...)
        @type diskimagetype:               string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.exportToURI(machineguid,destinationuri,executormachineguid,compressed,diskimagetype,jobguid,executionparams)
        return result


    def list (self, spaceguid = "", machinetype = "", hypervisor = "", machineguid = "", machinerole = "", jobguid = "", executionparams = {}):
        """
        
        List the machines in a cloud space.

        @execution_method = sync
        
        @param spaceguid:            guid of the space.
        @type spaceguid:             guid

        @param machinetype:          type of the machine
        @type machinetype:           string

        @param hypervisor:           hypervisor of the machine
        @param hypervisor:           string

        @param machineguid:          guid of the machine.
        @type machineguid:           guid   
        
        @param machinerole:          Role of the machine.
        @type machinerole:           string       
                
        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'MyWebServer',
        @note:                                          'description': 'My Personal Web Server',
        @note:                                          'status': 'RUNNING',
        @note:                                          'machinetype': 'VIRTUALSERVER',
        @note:                                          'backup': True,
        @note:                                          'os': 'LINUX',
        @note:                                          'hostname': 'web001',
        @note:                                          'memory': 4096,
        @note:                                          'nrcpu': 2,
        @note:                                          'isbackup': False,
        @note:                                          'template': False,
        @note:                                          'importancefactor': 3},
        @note:                                        { 'machineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'MyDbServer',
        @note:                                          'description': 'My Personal DB Server',
        @note:                                          'status': 'RUNNING',
        @note:                                          'machinetype': 'VIRTUALSERVER',
        @note:                                          'backup': True,
        @note:                                          'os': 'LINUX',
        @note:                                          'hostname': 'db001',
        @note:                                          'memory': 4096,
        @note:                                          'nrcpu': 4,
        @note:                                          'isbackup': True,
        @note:                                          'template': False,
        @note:                                          'importancefactor': 2}]}
        
        @raise e:                    In case an error occurred, exception is raised
        
        """
        result = self._rootobject.list(spaceguid,machinetype,hypervisor,machineguid,machinerole,jobguid,executionparams)
        return result


    def iscsiUnexpose (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Unexposes a machine using iSCSI

        @param machineguid:                guid of the machine to set retention policy.
        @type machineguid:                 guid
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.iscsiUnexpose(machineguid,jobguid,executionparams)
        return result


    def listVdcs (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        List the vdcs the machine is used in.

        @execution_method = sync
        
        @param machineguid:          guid of the machine to list the vdc's for.
        @type  machineguid:          guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listVdcs(machineguid,jobguid,executionparams)
        return result


    def exists (self, name = "", assetid = "", cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        @param name:                  Name of the machine (exact match)
        @type name:                   string
        
        @param assetid:               Asset id of the machine (exact match)
        @type assetid:                string
        
        @param cloudspaceguid:        Guid of the cloudspace
        @type cloudspaceguid:         guid        
           
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid} 
        @rtype:                       list
        
        @raise e:                     In case an error occurred, exception is raised       
        
        """
        result = self._rootobject.exists(name,assetid,cloudspaceguid,jobguid,executionparams)
        return result


    def getVideoMode (self, machineguid, order, jobguid = "", executionparams = {}):
        """
        
        Gets the video mode for a machine controlled by its hypervisor
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param order:                 Number of the monitor [0-7]
        @type order:                  integer

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with jobguid and result a dict = { xres : , yres: , bpp : } 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getVideoMode(machineguid,order,jobguid,executionparams)
        return result


    def installDCOS (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        install DCOS on pmachine        
        
        FLOW
        # check is pmachine
        #set machine.bootstatus=... to go to install dcos mode
        #actor:  Installserver.installDCOS(...
        @todo complete

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param pmachineguid:     Guid of the physical machine
        @type pmachineguid:      guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        """
        result = self._rootobject.installDCOS(pmachineguid,jobguid,executionparams)
        return result


    def addCapacityConsumed (self, machineguid, amount, capacityunittype, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Adds consumed capacity for the machine specified.

        @param machineguid:          guid of the customer specified
        @type machineguid:           guid

        @param amount:               Amount of capacity units to add
        @type amount:                integer

        @param capacityunittype:     Type of capacity units to add. See ca.capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param name:                 Name of capacity units to add.
        @type name:                  string

        @param description:          Description of capacity units to add.
        @type type:                  string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
        """
        result = self._rootobject.addCapacityConsumed(machineguid,amount,capacityunittype,name,description,jobguid,executionparams)
        return result


    def listExportedImages (self, machineguid, cloudspaceguid = "", machinetype = "", jobguid = "", executionparams = {}):
        """
        
        Gets a the list of exported machine images on the systemNAS for a specific machine

        @param machineguid:       guid of the machine rootobject
        @type machineguid:        guid

        @param cloudspaceguid:    guid of the machine rootobject
        @type cloudspaceguid:     guid

        @param machinetype:       filter on machine type
        @type machinetype:        string

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  list of exported images.
        @rtype:                   array

        @raise e:                 In case an error occurred, exception is raised              
        
        """
        result = self._rootobject.listExportedImages(machineguid,cloudspaceguid,machinetype,jobguid,executionparams)
        return result


    def disconnectFromHost (self, machineguid, hostmachineguid, leavecacheintact = False, jobguid = "", executionparams = {}):
        """
        
        Disconnects a machine on the specified host machine.

        on specified host
        * remove bridges for virtual nics
        * disconnect volumes to storage (remove DSS cache data), or make sure vdi's are removed

        @security administrator only

        @param machineguid:                guid of the machine to connect to the host machine.
        @type  machineguid:                guid

        @param hostmachineguid:            guid of the host machine to connect to the machine on.
        @type  hostmachineguid:            guid

        @param leavecacheintact:           If true means cache will not be emptied for e.g. DSS storagesystem
        @type leavecacheintact:            boolean

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.disconnectFromHost(machineguid,hostmachineguid,leavecacheintact,jobguid,executionparams)
        return result


    def addMonitor (self, machineguid, width, height, bpp, order = "", name = "", jobguid = "", executionparams = {}):
        """
        
        Add new monitor configuration to the specified machine
        
        @param machineguid:           Guid of the machine
        @type machineguid:            guid
        
        @param width:                 monitor width
        @type width:                  integer
        
        @param height:                monitor height
        @type height:                 integer
        
        @param bpp:                   bits per pixel of the monitor
        @type bpp:                    integer
        
        @param order:                 Order of the monitor [1-7]
        @type order:                  integer
        
        @param name:                  Name for the monitor
        @type name:                   string
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with result and jobguid: {'result': boolean, 'jobguid': guid} 
        @rtype:                       dict
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addMonitor(machineguid,width,height,bpp,order,name,jobguid,executionparams)
        return result


    def setTimeZone (self, machineguid, timezone, jobguid = "", executionparams = {}):
        """
        
        set timezone for a pmachine
        
        @param machineguid:         machineguid of the pmachine
        @type machineguid:          machineguid
       
        @param timezone:            name of the timezone
        @type timezone:             string
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary 
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.setTimeZone(machineguid,timezone,jobguid,executionparams)
        return result


    def listSnapshots (self, machineguid, includeinconsistent = False, timestampfrom = "", timestampuntil = "", jobguid = "", executionparams = {}):
        """
        
        List the snapshots for a given machine.

        @execution_method = sync
        
        @param machineguid:                guid of the machine to list the snapshots from.
        @type  machineguid:                guid
        
        @param timestampfrom:              Filter snapshots from given timestamp 
        @type timestampfrom:               datetime

        @param timestampuntil:             Filter snapshots until given timestamp
        @type timestampuntil:              datetime
        
        @param includeinconsistent:        Flag to include snapshot machines in inconsistent state (eg snapshots that are being snapshotted asynchronically)

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'parentmachineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'MyWebServer',
        @note:                                          'description': 'My Personal Web Server',
        @note:                                          'timestampcreated': '2009-09-12 00:00:12',
        @note:                                          'consistent': 'False'}]}
        
        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listSnapshots(machineguid,includeinconsistent,timestampfrom,timestampuntil,jobguid,executionparams)
        return result


    def resizeMemory (self, machineguid, memory, jobguid = "", executionparams = {}):
        """
        
        Updates the memory of a machine.

        @param machineguid:                guid of the machine to rollback.
        @type  machineguid:                guid

        @param memory:                     New value for memory in MB.
        @type  memory:                     int

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.resizeMemory(machineguid,memory,jobguid,executionparams)
        return result


    def listAccounts (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        List the accounts of a given machine.

        @execution_method = sync
        
        @param machineguid:                guid of the machine to list the accounts for.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of account info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'login': 'root',
        @note:                                          'accounttype': 'SYSTEMACCOUNT'},
        @note:                              '         { 'login': 'backup',
        @note:                                          'accounttype': 'SYSTEMACCOUNT'},
        @note:                              '         { 'login': 'postgres',
        @note:                                          'accounttype': 'SYSTEMACCOUNT'}]}
        
        """
        result = self._rootobject.listAccounts(machineguid,jobguid,executionparams)
        return result


    def listTemplates (self, spaceguid = "", machinetype = "", jobguid = "", executionparams = {}):
        """
        
        List the machines templates in a cloud space (of a given machinetype).

        @execution_method = sync
        
        @param spaceguid:                  guid of the space.
        @type spaceguid:                   guid

        @param machinetype:                Type of the machine (PHYSICAL, VIRTUALSERVER, VIRTUALDESKTOP,VIRTUALSERVER, IMAGEONLY, SMARTCLIENT)
        @type machinetype:                 string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             [{'description': 'Windows XP',
        @note:                             'machineguid': 'fbc0c990-d5f8-46f3-b7fe-e412abcc5bee',
        @note:                                  'machinetype': 'VIRTUALDESKTOP',
        @note:                                  'memory': None,
        @note:                                  'name': 'template_virtual_desktop_windowsxp',
        @note:                                  'nrcpu': None,
        @note:                                  'osdescription': 'Windows XP',
        @note:                                  'osguid': '5acdc4d4-12d3-4fc5-8271-78d886f68385',
        @note:                                  'osicon': 'windowsxp.png',
        @note:                                  'osname': 'windowsxp'},
        @note:                                 {'description': 'Windows Vista',
        @note:                                  'machineguid': 'a6254007-aa92-4598-887b-7fc48d334cfa',
        @note:                                  'machinetype': 'VIRTUALDESKTOP',
        @note:                                  'memory': None,
        @note:                                  'name': 'template_virtual_desktop_windowsvista',
        @note:                                  'nrcpu': None,
        @note:                                 'osdescription': 'Windows Vista',
        @note:                                  'osguid': 'f3ea862e-52f9-4704-9574-4bbac31d9e7e',
        @note:                                  'osicon': 'windowsvista.png',
        @note:                                  'osname': 'windowsvista'}]}
        
        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listTemplates(spaceguid,machinetype,jobguid,executionparams)
        return result


    def reboot (self, machineguid, clean = True, jobguid = "", executionparams = {}):
        """
        
        Reboots a machine.

        @param machineguid:                guid of the machine to reboot.
        @type  machineguid:                guid

        @param clean:                      soft reboot if true else hard reboot
        @type clean:                       boolean

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.reboot(machineguid,clean,jobguid,executionparams)
        return result


    def resume (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Resumes a machine.

        @param machineguid:                guid of the machine to resume.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.resume(machineguid,jobguid,executionparams)
        return result


    def listBackups (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        List the backups for a given machine.

        @execution_method = sync
        
        @param machineguid:                guid of the machine to list the backups from.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of backup machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'parentmachineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'MyWebServer',
        @note:                                          'description': 'My Personal Web Server',
        @note:                                          'backuplabel': 'DAILY-2009-09-12',
        @note:                                          'timestampcreated': '2009-09-12 00:00:12',
        @note:                                          'consistent': 'True'}]}
        
        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listBackups(machineguid,jobguid,executionparams)
        return result


    def addTempDisk (self, machineguid, size, name = "", role = "TEMP", retentionpolicyguid = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new temp disk for a machine.

        @param machineguid:                guid of the machine to create a new data disk for.
        @type  machineguid:                guid

        @param size:                       Size of disk in MB
        @type size:                        int

        @param name:                       Name of the temp disk.
        @type name:                        string
        
        @param role:                       Role of the temp disk. ('TEMP' OR 'SSDTEMP')
        @type role:                        string

        @param retentionpolicyguid:        Policy to be used for retention of snapshots
        @type retentionpolicyguid:         guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addTempDisk(machineguid,size,name,role,retentionpolicyguid,jobguid,executionparams)
        return result


    def initialize (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Initializes a machine based on the model.

        @param machineguid:                guid of the machine to initialize.
        @type machineguid:                 guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised


        @security administrators

        check is indeed a pmachine
        #will make sure appropriate applications are installed & configured (the agent and basic qbase is always installed)
        #will make sure that the backplanes get configured on the pmachine
        ... @todo check what more
        
        """
        result = self._rootobject.initialize(machineguid,jobguid,executionparams)
        return result


    def getCustomerGuid (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Returns the customer related to the machine

        @execution_method = sync
        
        @param machineguid:       guid of the machine rootobject
        @type machineguid:        guid

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  guid of the customer
        @rtype:                   guid

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getCustomerGuid(machineguid,jobguid,executionparams)
        return result


    def getXMLSchema (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the machine rootobject structure.

        @execution_method = sync
        
        @param machineguid:             guid of the machine rootobject
        @type machineguid:              guid

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the machine structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        result = self._rootobject.getXMLSchema(machineguid,jobguid,executionparams)
        return result


    def registerAgent (self, macaddress, jobguid = "", executionparams = {}):
        """
        
        Initializes a machine based on the model.

        @param macaddress:               MAC address of the machine on which to register a new agent.
        @type macaddress:                string

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                          dictionary
        @note:                           Example return value
        @note:                           {"result": "{"agentguid": "C149425F-16AE-451E-A439-0DE7D1EE86F6",
                                                      "xmppserver": "172.23.23.254",
                                                      "password": "12345",
                                                      "agentcontrollerguid": "EDFA459E-1A24-4F98-98CB-C995D2973B3D"}",
                                          "jobguid": "8D763680-ED8A-463F-AA25-EBF3EA7A1894"}"


        @raise e:                        In case an error occurred, exception is raised

        @security administrators
        
        """
        result = self._rootobject.registerAgent(macaddress,jobguid,executionparams)
        return result


    def importMachineTemplates (self, templates = [], cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Imports machines from the SystemNAS and converts them into templates
       
        @params templates         [ { name : Uri } ]
        @type template            list
        
        @param cloudspaceguid:    guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:    guid
 
        @param jobguid:           Guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary        
        
        """
        result = self._rootobject.importMachineTemplates(templates,cloudspaceguid,jobguid,executionparams)
        return result


    def getYAML (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the machine rootobject.

        @execution_method = sync
        
        @param machineguid:       guid of the machine rootobject
        @type machineguid:        guid

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @return:                  YAML representation of the machine
        @rtype:                   string
        
        """
        result = self._rootobject.getYAML(machineguid,jobguid,executionparams)
        return result


    def removeDataDisk (self, machineguid, diskguid, jobguid = "", executionparams = {}):
        """
        
        Removes a data disk from a machine.

        @param machineguid:                guid of the machine to create a remove the data disk from.
        @type  machineguid:                guid

        @param diskguid:                   guid of the disk to remove.
        @type diskguid:                    guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.removeDataDisk(machineguid,diskguid,jobguid,executionparams)
        return result


    def removeIpaddress (self, machineguid, macaddress, ipaddress, jobguid = "", executionparams = {}):
        """
        
        Removes an ipaddress from a NIC on a machine.

        @param machineguid:                guid of the machine to remove the ipaddress from.
        @type  machineguid:                guid

        @param macaddress:                 MAC address of the NIC to remove ipaddress from.
        @param macaddress:                 string

        @param ipaddress:                  Ipaddress to remove from the NIC.
        @type ipaddress:                   string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.removeIpaddress(machineguid,macaddress,ipaddress,jobguid,executionparams)
        return result


    def canConnectTempdisks (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Checks if there is enough available storage for a vmachine
                        
        @param machineguid:           guid of the vmachine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      true if there is space enough
        @rtype:                       boolean

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.canConnectTempdisks(machineguid,jobguid,executionparams)
        return result


    def getManagementIpaddress (self, machineguid, includevirtual = True, jobguid = "", executionparams = {}):
        """
        
        Retrieve the management ipaddress of the given machine

        @execution_method = sync
        
        @param machineguid:                  guid of the machine rootobject
        @type machineguid:                   guid
        
        @param includevirtual:               whether to include VIPA
        @type includevirtual:                boolean

        @param jobguid:                      guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with ipaddress as result and jobguid: {'result': '172.17.11.19', 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getManagementIpaddress(machineguid,includevirtual,jobguid,executionparams)
        return result


    def getConfigurationString (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Generate the configuration string for the given machine

        @param machineguid:           guid of the machine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      string with configuration data
        @rtype:                       string

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getConfigurationString(machineguid,jobguid,executionparams)
        return result


    def getDiskSequences (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Returns the disksequence as they will be attached to the hypervisor

        @param machineguid:           guid of the machine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with sorted array of disks info as result and jobguid: {'result': array, 'jobguid': guid} 
        @rtype:                       list
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getDiskSequences(machineguid,jobguid,executionparams)
        return result


    def setAccountPassword (self, machineguid, accounttype, login, currentpassword, newpassword, jobguid = "", executionparams = {}):
        """
        
        Updates the password of a machine account.

        @param machineguid:                guid of the machine to update account for.
        @type  machineguid:                guid

        @param accounttype:                Type of account to update (PUBLICACCOUNT, SYSTEMACCOUNT).
        @type accounttype:                 string

        @param login:                      Account login to update password for.
        @type login:                       string

        @param currentpassword:            Account's current password.
        @type currentpassword:             string

        @param newpassword:                Account's new p.
        @type newpassword:                 string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.setAccountPassword(machineguid,accounttype,login,currentpassword,newpassword,jobguid,executionparams)
        return result


    def listMonitors (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Returns list of all available monitors of the specified machine
        
        @param machineguid:           Guid of the machine
        @type machineguid:            guid
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with list of monitor configuration and jobguid: {'result': list, 'jobguid': guid} 
        @rtype:                       dict
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listMonitors(machineguid,jobguid,executionparams)
        return result


    def connectToNetworkService (self, machineguid, networkservicename, agentguid, jobguid = "", executionparams = {}):
        """
        
        Connect to given networkservice of given machine

        @param machineguid:        guid of the machine rootobject
        @type machineguid:         guid

        @param networkservicename: name of the networkservice to connect to
        @type networkservicename:  string
        
        @param agentguid:          guid of the agent which want to connect to KVM
        @type agentguid:           guid

        @param jobguid:            guid of the job if available else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with Trueas result and jobguid: {'result':True, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
        """
        result = self._rootobject.connectToNetworkService(machineguid,networkservicename,agentguid,jobguid,executionparams)
        return result


    def listIpaddresses (self, machineguid, publicflag = "", jobguid = "", executionparams = {}):
        """
        
        Retrieve the ipaddress of the given machine

        @execution_method = sync
        
        @param machineguid:                  guid of the machine rootobject
        @type machineguid:                   guid
        
        @param publicflag:                   flag to filter on public or private
        @type publicflag:                    boolean

        @param jobguid:                      guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with ipaddress as result and jobguid: {'result': '172.17.11.19', 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listIpaddresses(machineguid,publicflag,jobguid,executionparams)
        return result


    def removeNic (self, machineguid, macaddress, jobguid = "", executionparams = {}):
        """
        
        Removes a NIC from a machine.

        @param machineguid:                guid of the machine to remove the NIC from.
        @type  machineguid:                guid

        @param macaddress:                 MAC address of the NIC to remove.
        @param macaddress:                 string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.removeNic(machineguid,macaddress,jobguid,executionparams)
        return result


    def replace (self, machineguid, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Replaces an exisiting pmachine on an unmanaged device

        @param machineguid:                guid of the machine to initialize.
        @type machineguid:                 guid
        
        @param deviceguid:                 guid of the unmanaged machine to initialize.
        @type deviceguid:                  guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised


        @security administrators
        
        """
        result = self._rootobject.replace(machineguid,deviceguid,jobguid,executionparams)
        return result


    def addAccount (self, machineguid, accounttype, login, password = "", jobguid = "", executionparams = {}):
        """
        
        Adds an account for a machine.

        @param machineguid:                guid of the machine to add an account to.
        @type  machineguid:                guid

        @param accounttype:                Type of account to add (PUBLICACCOUNT, SYSTEMACCOUNT).
        @type accounttype:                 string

        @param login:                      Account login.
        @type login:                       string

        @param password:                   Account password.
        @type password:                    string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary
        
        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addAccount(machineguid,accounttype,login,password,jobguid,executionparams)
        return result


    def reactivate (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Reactivate physical machine (e.g. after reboot/failure, restart volumes)

        @param machineguid:           guid of the physical machine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.reactivate(machineguid,jobguid,executionparams)
        return result


    def checkAgent (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Checks whether for the agent is still running on given machine

        @param machineguid:           guid of the machine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      string with configuration data
        @rtype:                       string

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.checkAgent(machineguid,jobguid,executionparams)
        return result


    def create (self, cloudspaceguid, name, machinetype = "PHYSICAL", status = "CONFIGURED", bootstatus = "FROMDISK", assetid = "", memory = 0, memoryminimal = 0, nrcpu = 1, cpufrequency = 0, description = "", parentmachineguid = "", networkinfo = [], diskinfo = [], machinerole = "", hypervisor = "", osguid = "", deviceguid = "", hostname = "", importancefactor = "", backup = "", boot = "", alias = "", customerapplications = [], defaultgateway = "", monitors = [], jobguid = "", executionparams = {}):
        """
        
        Creates a new machine based on a template, but allows you to overrule capacity properties of the machine.
        
        @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:             guid
        
        @param name:                       Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                        string
        
        @param machinetype:                machinetype of the machine. IMAGEONLY|SMARTCLIENT|VIRTUALDESKTOP|PHYSICAL|SNAPSHOT|VIRTUALSERVER.
        @type machinetype:                 string
        
        @param status:                     status of the machine. CONFIGURED|IMAGEONLY|RUNNING|TODELETE|DELETING|OVERLOADED|STARTING|HALTED|PAUSED|STOPPING
        @type status:                      string
        
        @param bootstatus:                 bootstatus of the machine. FROMDISK|RECOVERY|INSTALL
        @type bootstatus:                  string
        
        @param assetid:                    Unique name of the machine. (Can be used as external reference by the user)
        @type assetid:                     string
        
        @param memory:                     Memory for the machine in MB. Same as template if not provided.
        @type memory:                      int
        
        @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        @type memoryminimal:               int
        
        @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        @type nrcpu:                       int
        
        @param cpufrequency:               CPU frequency in MHz.
        @type cpufrequency:                int
        
        @param description:                Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type description:                 string
        
        @param parentmachineguid:          guid of the physical machine this machine will be created upon.
        @type  parentmachineguid:          guid
        
        @param networkinfo:                network information [ { languid, ip , iptype } ]
        @type networkinfo:                 dictionary
        
        @param diskinfo:                   disk information {nr_disks: , info { diskguid, size, role,name,description} }
        @type diskinfo:                    dictionary
        
        @param machinerole:                machinerole of the machine. 
        @type machinerole:                 string
        
        @param hypervisor:                 hypervisor of the machine. 
        @type hypervisor:                  string
        
        @param osguid:                     osguid of the machine.
        @type  osguid:                     guid
        
        @param deviceguid:                 deviceguid of the machine.
        @type  deviceguid:                 guid
        
        @param hostname:                   hostname of the machine
        @type hostname:                    string
        
        @param importancefactor:           importancefactor of the machine
        @type importancefactor:            int
        
        @param backup:                     whether to backup the machine
        @type backup:                      boolean
        
        @param boot:                       whether to boot the machine when pmachine starts
        @type boot:                        boolean
        
        @param alias:                      alias of the machine
        @type alias:                       string
        
        @param customerapplications:       list of applicationguids that runs on the machine
        @type customerapplications:        list
        
        @param defaultgateway:             default gateway of the machine (can be of a private/public lan)
        @type defaultgateway:              string
        
        @param monitors:                   monitors configuration (widthxheightxbpp) ['1024x768x32','800x600x24']
        @type monitors:                    list
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.create(cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,machinerole,hypervisor,osguid,deviceguid,hostname,importancefactor,backup,boot,alias,customerapplications,defaultgateway,monitors,jobguid,executionparams)
        return result


    def executeQshellScript (self, machineguid, qshellscriptcontent, jobguid = "", executionparams = {}):
        """
        
        Execute a Q-Shell script on a pmachine.

        @security administrator only
        
        @param machineguid:                guid of the pmachine to execute the script on
        @type  machineguid:                guid

        @param qshellscriptcontent:        Content of the script to execute.
        @type  qshellscriptcontent:        string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.executeQshellScript(machineguid,qshellscriptcontent,jobguid,executionparams)
        return result


    def start (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Starts a machine.

        @param machineguid:                guid of the machine to start.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.start(machineguid,jobguid,executionparams)
        return result


    def getAvailableTempdiskSize (self, machineguid, role, jobguid = "", executionparams = {}):
        """
        
        Gets the available temp disk size left on the node where  machineguid is situated
                        
        @param machineguid:           guid of the machine
        @type machineguid:            guid
        
        @param role:                  TEMP or SSDTEMP
        @type role:                   string
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      the available space on SSD
        @rtype:                       int

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getAvailableTempdiskSize(machineguid,role,jobguid,executionparams)
        return result


    def updateNic (self, machineguid, macaddress, order, nictype = "", nicstatustype = "", ipaddresses = [], jobguid = "", executionparams = {}):
        """
        
        Update a NIC of the machine.

        @param machineguid:                guid of the machine to update the NIC to.
        @type  machineguid:                guid

        @param macaddress:                 MAC address of the NIC.
        @param macaddress:                 string
        
        @param order:                      Order of NIC.
        @type order:                       int
        
        @param nictype:                    Type of the NIC. L{core.machine.nic}
        @type nictype:                     string
        
        @param nicstatustype:              Status type of the NIC. (ACTIVE | BROKEN | DISABLED | NOTCONNECTED)
        @param nicstatustype:              string
        
        @param ipaddresses:                Array of new IP addresses configured for this NIC. (only adding new ipaddresses)
        @type ipaddresses:                 array
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid
        
        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.updateNic(machineguid,macaddress,order,nictype,nicstatustype,ipaddresses,jobguid,executionparams)
        return result


    def addDataDisk (self, machineguid, size, retentionpolicyguid, name = "", description = "", disksafetytype = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new data disk for a machine.

        @param machineguid:                guid of the machine to create a new data disk for.
        @type  machineguid:                guid

        @param size:                       Size of disk in MB
        @type size:                        int

        @param retentionpolicyguid:        Guid of the retention policy
        @type retentionpolicyguid:         guid

        @param name:                       Name of the data disk.
        @type name:                        string

        @param description:                Description of the datadisk
        @type description:                 string

        @param disksafetytype:             Type of disk safety (SSO,MIRRORCLOUD...)
        @type disksafetytype:              string
        
        @param jobguid:                    Guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addDataDisk(machineguid,size,retentionpolicyguid,name,description,disksafetytype,jobguid,executionparams)
        return result


    def listCustomerApplications (self, machineguid = "", cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns the Customer applications for a machine in a cloudspace when defined

        @param machineguid:           Guid of the machine
        @type machineguid:            guid
        
        @param cloudspaceguid:        Guid of the cloudspace to filter on
        @type cloudspaceguid:         guid
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with array of application info as result and jobguid: {'result': array, 'jobguid': guid} 
        @rtype:                       list
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listCustomerApplications(machineguid,cloudspaceguid,jobguid,executionparams)
        return result


    def addIpaddress (self, machineguid, macaddress, languid, ipaddress = "", jobguid = "", executionparams = {}):
        """
        
        Adds an ipaddress to a NIC on a machine.

        @param machineguid:                guid of the machine to add the ipaddress to.
        @type  machineguid:                guid

        @param macaddress:                 MAC address of the NIC to add ipaddress to.
        @param macaddress:                 string

        @param languid:                    guid of the lan to from which the ipaddress is part of.
        @type  languid:                    guid

        @param ipaddress:                  Ipaddress part of the lan to assign to the NIC. If not specified, an available ip will be selected from the lan.
        @type ipaddress:                   string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addIpaddress(machineguid,macaddress,languid,ipaddress,jobguid,executionparams)
        return result


    def copy (self, jobguid = "", executionparams = {}):
        """
        
        Same as clone, but all blocks on disks will be copied instead of cloned.
        
        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary
        
        @todo:                       Will be implemented in phase2
        
        """
        result = self._rootobject.copy(jobguid,executionparams)
        return result


    def connectToHost (self, machineguid, hostmachineguid, failover = False, jobguid = "", executionparams = {}):
        """
        
        Connects a machine on a specified host machine.

        on specified host
        * create bridges or virtual nics
        * connect volumes to storage, or make sure vdi's are available
        * when failover=True then the move of machine is forced and to always succeed
        
        @security administrator only

        @param machineguid:                guid of the machine to connect to the host machine.
        @type  machineguid:                guid

        @param hostmachineguid:            guid of the pmachine hosting the vmachine.
        @type  hostmachineguid:            guid
        
        @param failover:                   flags whether failover workflow needs to be followed
        @type  failover:                   boolean

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.connectToHost(machineguid,hostmachineguid,failover,jobguid,executionparams)
        return result


    def listDisks (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        List the disks for a given machine.

        @execution_method = sync
        
        @param machineguid:          guid of the machine to list the backups from.
        @type  machineguid:          guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of disks info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listDisks(machineguid,jobguid,executionparams)
        return result


    def restartAgent (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Restarts the agent if it is not running on given machine

        @param machineguid:           guid of the machine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      string with configuration data
        @rtype:                       string

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.restartAgent(machineguid,jobguid,executionparams)
        return result


    def delete (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Deletes a machine.

        @param machineguid:                guid of the machine to delete.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.delete(machineguid,jobguid,executionparams)
        return result


    def getMachineAgent (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Retrieves the Agent GUID for a machine.

        @execution_method = sync
        
        @param machineguid:      guid of the machine rootobject
        @type machineguid:       guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with Appliance machine.agentguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getMachineAgent(machineguid,jobguid,executionparams)
        return result


    def canRollback (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Checks whether a snaphot machine can be rolledback

        @param machineguid:           guid of the snapshotted machine
        @type machineguid:            guid

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      True or False 
        @rtype:                       boolean
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.canRollback(machineguid,jobguid,executionparams)
        return result


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the machine rootobject
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
        result = ROOTOBJECT_TYPES['machine'].deserialize(ThriftSerializer, result)
        return result


    def getParentMachine (self, machineguid, machinetype = "", jobguid = "", executionparams = {}):
        """
        
        Returns the ancestor/parent machine related to the machine (based upon the optional machinetype parameter)

        @execution_method = sync
        
        @param machineguid:       guid of the machine rootobject
        @type machineguid:        guid
        
        @param machinetype:       machinetype of the machine. IMAGEONLY|SMARTCLIENT|VIRTUALDESKTOP|PHYSICAL|SNAPSHOT|VIRTUALSERVER.
        @type machinetype:        string

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  guid of parent machine
        @rtype:                   guid

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getParentMachine(machineguid,machinetype,jobguid,executionparams)
        return result


    def setRole (self, machineguid, machinerole, jobguid = "", executionparams = {}):
        """
        
        Retrieves the role for a machine.

        @param machineguid:                  guid of the machine rootobject
        @type machineguid:                   guid

        @param machinerole:                  Role of the machine. Possible roles are CPUNODE, STORAGENODE, COMBINEDNODE
        @type machinerole:                   string

        @param jobguid:                      guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with machine role as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        @security administrators
        
        """
        result = self._rootobject.setRole(machineguid,machinerole,jobguid,executionparams)
        return result


    def addISOImage (self, machineguid, sourceuri, name = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new ISO image for a machine.

        @param machineguid:                guid of the machine to create a new ISO image for.
        @type  machineguid:                guid
        
        @param sourceuri:                  Uri for the iso image
        @type sourceuri:                   string

        @param name:                       Name of the temp disk.
        @type name:                        string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.addISOImage(machineguid,sourceuri,name,jobguid,executionparams)
        return result


    def changeGateway (self, machineguid, defaultgateway = "", jobguid = "", executionparams = {}):
        """
        
        Change the default gateway of a machine.
        
        @param machineguid:             guid of the machine on which we will change the default gateway.
        @type machineguid:              guid
        
        @param defaultgateway:          default gateway of the machine
        @type defaultgateway:           string
        
        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary
        
        @return:                        number of maximum allowed ip addresses
        @rtype:                         integer
        
        @raise e: In case an error occurred, exception is raised
        
        """
        result = self._rootobject.changeGateway(machineguid,defaultgateway,jobguid,executionparams)
        return result


    def removeCapacityProvided (self, machineguid, capacityunittype, jobguid = "", executionparams = {}):
        """
        
        Removes provided capacity for the machine specified.

        @param machineguid:          guid of the machine specified
        @type machineguid:           guid

        @param capacityunittype:     Type of capacity units to remove. See ca.capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
        """
        result = self._rootobject.removeCapacityProvided(machineguid,capacityunittype,jobguid,executionparams)
        return result


    def iscsiExpose (self, machineguid, targetIQN = "", username = "", password = "", initiatorIQN = "", ipaddress = "", jobguid = "", executionparams = {}):
        """
        
        Exposes a machine using iSCSI (except for its tempdisks)

        @param machineguid:             Guid of the machine to expose over ISCSI.
        @type machineguid:              guid

        @param username:                Username that is allowed to connect
        @type username:                 string

        @param targetIQN:               iSCSI Qualified Name representing the iscsi target
        @type targetIQN:                string
        
        @param password:                Password of user that is allowed to connect
        @type password:                 string
        
        @param initiatorIQN:            iSCSI Qualified Name allowed to connect
        @type initiatorIQN:             string
        
        @param ipaddress:               ip address allowed to connect to the iscsi target
        @type ipaddress:                string

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with a dictionary with list of ipaddress and iqn of the ISCSI exposed disk as result and jobguid: {'result': {'diskguid': guid, 'ipaddress': ip, 'iqn': iqn}, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        """
        result = self._rootobject.iscsiExpose(machineguid,targetIQN,username,password,initiatorIQN,ipaddress,jobguid,executionparams)
        return result


    def moveToCloudspace (self, machineguid, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Moves a machine from one cloud space to another.

        @param machineguid:                guid of the machine to move.
        @type  machineguid:                guid

        @param cloudspaceguid:             guid of the cloud space to move the machine to.
        @type  cloudspaceguid:             guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.moveToCloudspace(machineguid,cloudspaceguid,jobguid,executionparams)
        return result


    def bootFromDiskConfigure (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        make sure pmachine boots from disk next time it is restarted
        when vmachine: use normal memory properties
        
        FLOW
        # check is pmachine
        # set machine.bootstatus=... to boot from disk
        #todo complete
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param pmachineguid:     Guid of the physical machine
        @type pmachineguid:      guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        """
        result = self._rootobject.bootFromDiskConfigure(machineguid,jobguid,executionparams)
        return result


    def refreshStatus (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @param machineguid:      guid of the machine rootobject
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 rootobject
        @rtype:                  string

        @warning:                Only usable using the python client.
        
        """
        result = self._rootobject.refreshStatus(machineguid,jobguid,executionparams)
        return result


    def connectToKvm (self, machineguid, agentguid, jobguid = "", executionparams = {}):
        """
        
        Connect to Kvm of given machine

        @param machineguid:       guid of the machine rootobject
        @type machineguid:        guid
        
        @param agentguid:         guid of the agent which want to connect to KVM
        @type agentguid:          guid

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with Trueas result and jobguid: {'result':True, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.connectToKvm(machineguid,agentguid,jobguid,executionparams)
        return result


    def updateModelProperties (self, machineguid, name = "", description = "", cloudspaceguid = "", machinetype = "", osguid = "", assetid = "", alias = "", template = "", hostname = "", nrcpu = "", cpufrequency = "", memory = "", memoryminimal = "", importancefactor = "", lastrealitycheck = "", deviceguid = "", boot = "", customsettings = "", defaultgateway = "", status = "", clouduserguid = "", parentmachineguid = "", hypervisor = "", accounts = "", capacityunitsconsumed = "", capacityunitsprovided = "", nics = "", resourcegroupguid = "", agentguid = "", ownerguid = "", backup = True, backuplabel = "", consistent = "", isbackup = False, iconname = "", timestamp = "", bootstatus = "", monitors = [], jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @param machineguid:                guid of the machine specified
        @type machineguid:                 guid

        @param name:                       Name of the machine.
        @type name:                        string

        @param description:                Description for this machine
        @type description:                 string

        @param cloudspaceguid:             guid of the space to which this machine belongs
        @type cloudspaceguid:              guid

        @param machinetype:                Machine type.
        @type machinetype:                 string

        @param osguid:                     guid of the OS.
        @type osguid:                      guid

        @param assetid:                    Asset ID.
        @type assetid:                     string

        @param alias:                      Alias of the machine.
        @type alias:                       string

        @param template:                   is template, when template used as example for an machine
        @type template:                    bool

        @param hostname:                   Hostname of the machine.
        @type hostname:                    string

        @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        @type nrcpu:                       int

        @param cpufrequency:               CPU frequency in MHz.
        @type cpufrequency:                int

        @param memory:                     Memory for the machine in MB. Same as template if not provided.
        @type memory:                      int

        @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        @type memoryminimal:               int

        @param importancefactor:           an integer which defines how important a machine is, std=5, when having a disaster this will define order of recovery (nr between 0 & 10, 10 being most important e.g. 10 means this is the most important machine, 0 means no importance=will always be last)
        @type importancefactor:            int

        @param lastrealitycheck:           date and time of last check on the machine
        @type lastrealitycheck:            datetime

        @param deviceguid:                 guid of the parent device
        @type deviceguid:                  guid

        @param boot:                       flag indicating that this machine must be automatically started when rebooting the parent machine
        @type boot:                        bool

        @param customsettings:             custom settings and configuration of machine, is XML, to be used freely
        @type customsettings:              string

        @param defaultgateway:             default gateway ip addr
        @type defaultgateway:              ipaddress

        @param status:                     status of the machine   CONFIGURED|IMAGEONLY|HALTED|RUNNING|OVERLOADED|PAUSED|TODELETE|STOPPING|STARTING|DELETING
        @type status:                      string

        @param clouduserguid:              guid of the clouduser, owning this machine
        @type clouduserguid:               guid

        @param parentmachineguid:          guid of the parent machine
        @type parentmachineguid:           guid

        @param hypervisor:                 Hypervisor of the machine.
        @type hypervisor:                  string

        @param agentguid:                  guid of the agent.
        @type agentguid:                   guid

        @param ownerguid:                  guid of the owner.
        @type ownerguid:                   guid

        @param defaultgateway:             Default gateway
        @type defaultgateway:              ipaddress

        @param deviceguid:                 guid of the device.
        @type deviceguid:                  guid

        @param hostname:                   Hostname of the machine.
        @type hostname:                    string

        @param hypervisor:                 Hypervisor of the machine.
        @type hypervisor:                  string

        @param backup:                     Indicates if the machine should be included in the backup policies.
        @type backup:                      boolean

        @param isbackup:                   Indicates if the machine is a backup.
        @type isbackup:                    boolean

        @param backuplabel:                Backuplabel of the machine.
        @type backuplabel:                 string
        
        @param timestamp:                  Timestamp of creation date in reality
        @type timestamp:                   datetime
        
        @param bootstatus:                 Machine boot status (INSTALL|FROMDISK|RECOVERY)
        @type bootstatus:                  string
        
        @param monitors:                   monitors configuration (widthxheightxbpp) ['1024x768x32','800x600x24']
        @type monitors:                    list

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.updateModelProperties(machineguid,name,description,cloudspaceguid,machinetype,osguid,assetid,alias,template,hostname,nrcpu,cpufrequency,memory,memoryminimal,importancefactor,lastrealitycheck,deviceguid,boot,customsettings,defaultgateway,status,clouduserguid,parentmachineguid,hypervisor,accounts,capacityunitsconsumed,capacityunitsprovided,nics,resourcegroupguid,agentguid,ownerguid,backup,backuplabel,consistent,isbackup,iconname,timestamp,bootstatus,monitors,jobguid,executionparams)
        return result


    def makeTemplate (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Create template from a machine.

        @param machineguid:                guid of the machine to create template from.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.makeTemplate(machineguid,jobguid,executionparams)
        return result


    def snapshot (self, machineguid, label = "", description = "", automated = False, async = False, snapshottype = "PAUSED", jobguid = "", executionparams = {}):
        """
        
        Creates a snapshot of a machine.

        means
        - backup metadata of machine 
        - pause machine (When snapshottype = PAUSED)
        - snapshot all disks of machine if not async
        - resume machine (When snapshottype = PAUSED)

        @param machineguid:                guid of the machine to snapshot.
        @type  machineguid:                guid
        
        @param label:                      label for the snapshot
        @type label:                       string
        
        @param description:                description for the snapshot
        @type description:                 string
        
        @param automated:                  Flags whether the snapshot is being taken scheduled or manually (is used for retention of snapshots)
        @type automated:                   boolean
        
        @param async:                      Flags whether the snapshot will be taken asynchronically afterwards (by calling the sso.snapshotmachine method)
        @type async:                       boolean
        
        @param snapshottype:               type of the snapshot (REGULAR, PAUSED, VSS, CSBA)
        @type snapshottype:                string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with snapshot machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.snapshot(machineguid,label,description,automated,async,snapshottype,jobguid,executionparams)
        return result


    def addNic (self, machineguid, nictype, order = 0, macaddress = "", ipaddresses = [], nicstatustype = "", jobguid = "", executionparams = {}):
        """
        
        Adds a NIC to the machine.

        @param machineguid:                guid of the machine to add the NIC to.
        @type  machineguid:                guid

        @param nictype:                    Type of the NIC. L{core.machine.nic}
        @type nictype:                     string

        @param order:                      Order of NIC. Next available if not specified.
        @type order:                       int

        @param macaddress:                 MAC address of the NIC. Generated if not provided.
        @param macaddress:                 string

        @param ipaddresses:                Array of IP addresses configured for this NIC.
        @type ipaddresses:                 array

        @param nicstatustype:              Status type of the NIC. (ACTIVE | BROKEN | DISABLED | NOTCONNECTED)
        @param nicstatustype:              string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addNic(machineguid,nictype,order,macaddress,ipaddresses,nicstatustype,jobguid,executionparams)
        return result


    def getPublicIpaddress (self, machineguid, includevirtual = True, jobguid = "", executionparams = {}):
        """
        
        Retrieve the public ipaddress of the given machine

        @execution_method = sync
        
        @param machineguid:                  guid of the machine rootobject
        @type machineguid:                   guid

        @param includevirtual:               whether to include VIPA
        @type includevirtual:                boolean

        @param jobguid:                      guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with ipaddress as result and jobguid: {'result': '172.17.11.19', 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getPublicIpaddress(machineguid,includevirtual,jobguid,executionparams)
        return result


    def clone (self, machineguid, cloudspaceguid, vdcguid = "", copynetworkinfo = True, maintenancemode = True, name = "", snapshotguid = None, hostmachineguid = None, jobguid = "", executionparams = {}):
        """
        
        clone existing machine into defined space and into defined destinationVDC
        if space=="" then in same space
        if destinationVDC=="" then same VDC (maintenanceMode is not possible then)
        @param copyNetworkInfo if False: do not copy network info

        if in same space:
        ---------------
        * all rootobject properties will be copied over appart from
        ** new guid's
        ** the machine.name = original + <timestamp>
        * For the network lan's, the machine stays connected to the same LAN's but new ip addresses are looked for on those LAN's

        if in different space
        ------------------
        * all rootobject properties will be copied over
        * new network LAN's are created with as name $originalLanName_clone_<timestamp> 
        * the ip addresses are 100% the same as the original ip addresses
        * for the private LAN's: the VLAN's are ALL NEW!!! There is always 100% separation between spaces for private LAN's
        * for the public LAN's: the machine's stay connected to the same LAN's but new ip addresses are looked for on those LAN's

        if maintenanceMode==True
        ----------------------
        * then all LAN's will get a different vlan tag
        * new network LAN's are created with as name $originalLanName_clone_<timestamp>
        * the ip addresses are 100% the same as the original ip addresses

        cloning means the blocks on the disks are not copied, only the changes are remembered
        recovery mode is only possible if copied to a maintenance VDC

        @param machineguid:                guid of the machine to clone.
        @type  machineguid:                guid

        @param cloudspaceguid:             guid of cloud space to create the machine in. Same cloud space if not provided.
        @type  cloudspaceguid:             guid

        @param vdcguid:                    guid of the VDC to create the machine in. Same VDC if not specified, in that case maintenanceMode is always False.
        @type  vdcguid:                    guid

        @param copynetworkinfo:            If True, all networking info will be copied as well. Private networks will be created in new Vlans, public networks are not created, but the machine will receive an ip in the same public lan.
        @type copynetworkinfo:             boolean
        @note:                             Only possible if cloned to a different VDC and in the same cloud space.

        @param maintenancemode:            If True, all networking info will be copied as well, even for public vlans.
        @type maintenancemode:             boolean
        
        @param name:                       name for new clone
        @type name:                        string
        
        @param snapshotguid:               guid of the snapshot to clone from
        @type  snapshotguid:               guid
        
        
        @param hostmachineguid:            host for the clone
        @type hostmachineguid:             guid
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary
        
        """
        result = self._rootobject.clone(machineguid,cloudspaceguid,vdcguid,copynetworkinfo,maintenancemode,name,snapshotguid,hostmachineguid,jobguid,executionparams)
        return result


    def removeAccount (self, machineguid, accounttype, login, jobguid = "", executionparams = {}):
        """
        
        Removes an account from a machine.

        @param machineguid:                guid of the machine to remove an account from.
        @type  machineguid:                guid

        @param accounttype:                Type of account to remove (PUBLICACCOUNT, SYSTEMACCOUNT).
        @type accounttype:                 string

        @param login:                      Account login.
        @type login:                       string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.removeAccount(machineguid,accounttype,login,jobguid,executionparams)
        return result


    def disable (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @raise e:                In case an error occurred, exception is raised
        
        @todo:                   Will be implemented in phase2
        
        """
        result = self._rootobject.disable(machineguid,jobguid,executionparams)
        return result


    def importFromURI (self, machineguid, sourceuri, executormachineguid = "", compressed = True, diskimagetype = "vdi", cloudspaceguid = "", clouduserguid = "", jobguid = "", executionparams = {}):
        """
        
        Import a machine from a given URI.
        Machine object in drp needs to be created first.

        @param machineguid:                guid of the machine to import to.
        @type  machineguid:                guid

        @param sourceuri:                  URI of the location where the export is stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/)
        @type sourceuri:                   string

        @param executormachineguid:        guid of the machine which should import the export. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:         guid

        @param compressed:                 Should be True if the machine export is compressed using 7zip compression
        @type compressed:                  boolean

        @param diskimagetype:              Type of the disk image format used (VDI, RAW, VMDK, ...)
        @type diskimagetype:               string

        @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:             guid

        @param clouduserguid:              guid of the related clouduser
        @type clouduserguid:               guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.importFromURI(machineguid,sourceuri,executormachineguid,compressed,diskimagetype,cloudspaceguid,clouduserguid,jobguid,executionparams)
        return result


    def addFloppyImage (self, machineguid, sourceuri, name = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new floppy image for a machine.

        @param machineguid:                guid of the machine to create a new floppy disk for.
        @type  machineguid:                guid

        @param sourceuri:                  Uri for the iso image
        @type sourceuri:                   string

        @param name:                       Name of the temp disk.
        @type name:                        string

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.addFloppyImage(machineguid,sourceuri,name,jobguid,executionparams)
        return result


    def removeCapacityConsumed (self, machineguid, capacityunittype, jobguid = "", executionparams = {}):
        """
        
        Removes consumed capacity for the machine specified.

        @param machineguid:          guid of the customer specified
        @type machineguid:           guid

        @param capacityunittype:     Type of capacity units to remove. See ca.capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary
         
        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
        """
        result = self._rootobject.removeCapacityConsumed(machineguid,capacityunittype,jobguid,executionparams)
        return result


    def detachFromDevice (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Unforces a machine to run on a particular device.
        (will use resourcegroups underneath)

        @param machineguid:                guid of the machine to attach to a device.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        @todo:                             Will be implemented in phase2
        
        """
        result = self._rootobject.detachFromDevice(machineguid,jobguid,executionparams)
        return result


    def removeMonitor (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Remove the last monitor of the specified machine
        (Primary monitor [0] can not be removed)
        
        @param machineguid:           Guid of the machine
        @type machineguid:            guid
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with result and jobguid: {'result': boolean, 'jobguid': guid} 
        @rtype:                       dict
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.removeMonitor(machineguid,jobguid,executionparams)
        return result


    def exportToSecondary (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Creates a backup of a machine.

        create a backup of the machine, will result in an exported vdi image (7zipped)
        (in case of SSO onto DSS)
        also the metadata is being stored

        @param machineguid:                guid of the machine to backup.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with backup machineguid as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @todo:                             Will be implemented in phase2
        @todo:                             naming
        
        """
        result = self._rootobject.exportToSecondary(machineguid,jobguid,executionparams)
        return result


    def listNics (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        List the NICs for a given machine.

        @execution_method = sync
        
        @param machineguid:                guid of the machine to list the NICs for.
        @type  machineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of NIC info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'order': 0,
        @note:                                          'macaddress': '0a:00:27:00:00:00',
        @note:                                          'status': 'ACTIVE',
        @note:                                          'nictype': 'ETHERNET_100MB',
        @note:                                          'ipaddresses': [{'ipaddress': '192.168.1.2',
        @note:                                                           'netmask': '255.255.255.0',
        @note:                                                           'iptype': 'IPV4',
        @note:                                                           'lan':{'languid': '22544B07-4129-47B1-8690-B92C0DB21433'
        @note:                                                                  'name': 'ManagementLan',
        @note:                                                                  'dns': '192.168.1.1',
        @note:                                                                  'startip': '192.168.1.1',
        @note:                                                                  'endip': '192.168.1.10',
        @note:                                                                  'gateway': '192.168.1.254',
        @note:                                                                  'network': '192.168.1.0',
        @note:                                                                  'storageflag': True,
        @note:                                                                  'managementflag': True,
        @note:                                                                  'publicflag': False,
        @note:                                                                  'vlantag': '0'}},
        @note:                                                          {'ipaddress': '192.168.5.2',
        @note:                                                           'netmask': '255.255.255.0',
        @note:                                                           'iptype': 'IPV4',
        @note:                                                           'lan':{'languid': '22544B07-4129-47B1-8690-B92C0DB21435'
        @note:                                                                  'name': 'SmartClientLan',
        @note:                                                                  'dns': '192.168.1.1',
        @note:                                                                  'startip': '192.168.5.1',
        @note:                                                                  'endip': '192.168.5.100',
        @note:                                                                  'gateway': '192.168.5.1',
        @note:                                                                  'network': '192.168.5.0',
        @note:                                                                  'storageflag': False,
        @note:                                                                  'managementflag': False,
        @note:                                                                  'publicflag': True,        
        @note:                                                                  'vlantag': '0'}}]},
        @note:                                        { 'order': 1,
        @note:                                          'macaddress': '0a:00:28:00:00:00',
        @note:                                          'status': 'ACTIVE',
        @note:                                          'nictype': 'ETHERNET_100MB',
        @note:                                          'ipaddresses': [{'ipaddress': 10.100.32.12',
        @note:                                                           'netmask': '255.255.255.0',
        @note:                                                           'iptype': 'IPV4',
        @note:                                                           'lan':{'languid': '22544B07-4129-47B1-8690-B92C0DB21436'
        @note:                                                                  'name': 'PublicLan',
        @note:                                                                  'dns': '10.100.0.1',
        @note:                                                                  'startip': '10.100.32.10',
        @note:                                                                  'endip': '10.100.32.254',
        @note:                                                                  'gateway': '10.100.32.254',
        @note:                                                                  'network': '10.100.32.0',
        @note:                                                                  'vlantag': '0'}}]}]}
        
        """
        result = self._rootobject.listNics(machineguid,jobguid,executionparams)
        return result


    def listGuestMachines (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        List the guests for a given host machine.

        @execution_method = sync
        
        @param machineguid:                  guid of the host machine to list the guests from.
        @type  machineguid:                  guid

        @param jobguid:                      guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                              dictionary
        @note:                               {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                            'parentmachineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                            'name': 'MyWebServer',
        @note:                                            'description': 'My Personal Web Server',
        @note:                                            'status': 'RUNNING',
        @note:                                            'os': 'windows2003',
        @note:                                            'iconname': 'vamchine.ico'}]}
        
        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listGuestMachines(machineguid,jobguid,executionparams)
        return result


