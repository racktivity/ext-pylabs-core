from cloud_api_rootobjects import cloud_api_sso

class sso:

    def __init__(self):
        self._rootobject = cloud_api_sso.sso()

    def listSmartClientDevices (self, isfree = "", jobguid = "", executionparams = {}):
        """
        
        Lists all available smart client devices for a Smart Style Office environment

        @execution_method = sync

        @param  isfree              Boolean value indicating if only non-occupied smart client devices should be returned
        @type isfree                boolean

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary of array of dictionaries with guid, name, description, modelnr, serialnr,  status, isfree.
        @rtype:                     dictionary
        @note:                      Example return value:
        @note:                      {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "sc_reception", "description": "Smart client at reception desk", "modelnr": "model1234", "serialnr":"12345-6789", "status": "ACTIVE", "isfree": False},
        @note:                                  {"guid": "D48CCFB4-207D-469F-8DA8-471304C3CCA7", "name": "sc_meeting_room", "description": "Smart client at meeting room 1", "modelnr": "model1234", "serialnr":"67890-1234", "status": "ACTIVE", "isfree": True}],
        @note:                       'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listSmartClientDevices(isfree,jobguid,executionparams)
        return result


    def changePasswordOnPMachines (self, username, newpassword, jobguid = "", executionparams = {}):
        """
        
        Changes the password on each pmachine using new pass word
        
        @security admin
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param username               username
        @type username                string
        
        @param newpassword            new password of the user
        @type newpassword             string

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.changePasswordOnPMachines(username,newpassword,jobguid,executionparams)
        return result


    def listSystemNASMachineTemplates (self, jobguid = "", executionparams = {}):
        """
        
        Lists machine templates available on the SystemNAS

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with available templates and their paths
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listSystemNASMachineTemplates(jobguid,executionparams)
        return result


    def syncModel (self, interval = 1440.0, jobguid = "", executionparams = {}):
        """
        
        Cleans snapshots on the volume driver which did not make it in the model
        Cleans snapshots in the model that has no snapshots at the backend
        

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid
        
        @param interval:            Interval of when model must be synced (depends which items are synced)
        @param interval:            float
        
        @return:                    Dictionary with jobguid as result of pending model update and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.syncModel(interval,jobguid,executionparams)
        return result


    def editMachine (self, machineguid, name = "", description = "", cloudspaceguid = "", machinetype = "", osguid = "", assetid = "", alias = "", hostname = "", nrcpu = "", cpufrequency = "", memory = "", memoryminimal = "", importancefactor = "", deviceguid = "", boot = "", backup = "", clouduserguid = "", ownerguid = "", iconname = "", bootstatus = "", retentionpolicyguids = {}, customerapplications = [], jobguid = "", executionparams = {}):
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
        
        @param importancefactor:           Importance of the virtual machine
        @type importancefactor:            int
        
        @param deviceguid:                 guid of the parent device
        @type deviceguid:                  guid

        @param boot:                       flag indicating that this machine must be automatically started when rebooting the parent machine
        @type boot:                        bool

        @param backup:                     Backup flag
        @type backup:                      bool

        @param clouduserguid:              guid of the clouduser, owning this machine
        @type clouduserguid:               guid

        @param ownerguid:                  guid of the owner.
        @type ownerguid:                   guid
        
        @param iconname:                   Icon for the machine.
        @type iconname:                    string

        @param bootstatus:                 Machine boot status (INSTALL|FROMDISK|RECOVERY)
        @type bootstatus:                  string

        @param retentionpolicyguids:       Retention policy for the disks of the machine {'diskguid': 'policyguid'}
        @type retentionpolicyguids:        dictionary
        
        @param customerapplications:       Customer applications to be running on machine
        @type customerapplications:        list
         
        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.editMachine(machineguid,name,description,cloudspaceguid,machinetype,osguid,assetid,alias,hostname,nrcpu,cpufrequency,memory,memoryminimal,importancefactor,deviceguid,boot,backup,clouduserguid,ownerguid,iconname,bootstatus,retentionpolicyguids,customerapplications,jobguid,executionparams)
        return result


    def addPowerSwitchDevice (self, name, macaddress, cloudspaceguid, description = "", racku = 1, racky = 0, rackz = 0, jobguid = "", executionparams = {}):
        """
        
        Adds a new powerswitch device to a Smart Style Office environment

        @param  name                name of the device
        @type name                  string

        @param macaddress           MAC address of the new resource node
        @type macaddress            string

        @param description          remarks on the device
        @type description           type_description

        @param racku                size of the device, measured in u e.g. 1u high
        @type racku                 int

        @param racky                physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        @type racky                 int

        @param rackz                physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        @type rackz                 int

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addPowerSwitchDevice(name,macaddress,cloudspaceguid,description,racku,racky,rackz,jobguid,executionparams)
        return result


    def getAvailableTempDiskSizes (self, diskroletype, jobguid = "", executionparams = {}):
        """
        
        Lists available disk sizes for creation of temp disks 

        @param diskroletype:        SSDTEMP or TEMP
        @type  diskroletype:        string
        
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getAvailableTempDiskSizes(diskroletype,jobguid,executionparams)
        return result


    def createSnapshots (self, snapshottype = "REGULAR", jobguid = "", executionparams = {}):
        """
        
        Creates snapshots off all disks

        @param snapshottype:        If PAUSED, the machine will be paused before snapshot is taken.
        @type snapshottype:         string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.createSnapshots(snapshottype,jobguid,executionparams)
        return result


    def snapshotMachine (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Snapshots a machine and updating the model asynchronnically
        
        @param machineguid:         Guid of the snapshot machine 
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary
        
        @return:                    Dictionary  {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.snapshotMachine(machineguid,jobguid,executionparams)
        return result


    def getKioskModeSmartClientInfo (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets the information of a smartclient in kiosk mode

        @execution_method = sync

        @param machineguid          guid of machine
        @type machineguid:          guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    information { description , iqn , ip }
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getKioskModeSmartClientInfo(machineguid,jobguid,executionparams)
        return result


    def listVirtualDesktops (self, cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Lists all vistual desktop for a certain cloud space

        Execute method in WFE to get list of current authenticated user
        @execution_method = async
        @execution_param_wait = True

        @param cloudspaceguid       guid of an existing cloudspaceguid to whom the virtual desktops belong
        @type cloudspaceguid        guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary with jobguid and result 
        @rtype:                     dictionary
        
        @note                         {'jobguid': '386e7985-4871-4c59-a90c-4a43a2698188',
        @note                          'result': [{'address': '10.100.143.3',
        @note                                      'backup': None,
        @note                                      'description': 'Virtual Desktop John',
        @note                                      'guid': 'b56c2c6d-d143-4d69-9f15-10679ba2117c',
        @note                                      'hostname': 'vdjohn',
        @note                                      'hypervisor': 'VIRTUALBOX30',
        @note                                      'memory': 1024,
        @note                                      'name': 'vdjohn',
        @note                                      'nrcpu': 2,
        @note                                      'osname': 'windows7',
        @note                                      'parentmachinename': 'A3NODE3',
        @note                                      'portnr': 23000}]}
        
        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listVirtualDesktops(cloudspaceguid,jobguid,executionparams)
        return result


    def scrubVolumes (self, jobguid = "", executionparams = {}):
        """
        
        Scrubs volumes on a timely basis (used in a policy)
                                          
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
        """
        result = self._rootobject.scrubVolumes(jobguid,executionparams)
        return result


    def getAvailableFOCNode (self, machineguid, jobguid = "", executionparams = {}):
        """
         
        List available node for defining new FailOver Cache on  
        
        @param machineguid:           guid of the machine to list the FOC volumes
        @type  machineguid:           guid
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with node name , management ip , port of node where FOC can be initialized
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getAvailableFOCNode(machineguid,jobguid,executionparams)
        return result


    def getPhysicalDisksCount (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets the number of physical disks on given pmachine 

        @param machineguid:       guid of the pmachine 
        @type machineguid:        guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getPhysicalDisksCount(machineguid,jobguid,executionparams)
        return result


    def shutdown (self, jobguid = "", executionparams = {}):
        """
        
        shutdown the sso environment

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.shutdown(jobguid,executionparams)
        return result


    def sendMessageToNoc (self, customerguid, username, password, domain, message, jobguid = "", executionparams = {}):
        """
        
        Sends a message to the NOC for a certain domain
        
        @param customerguid       Guid of the customer unregistering the domain
        @type customerguid        guid
        
        @param username           ITPS portal username
        @type username            string
        
        @param password           ITPS portal password
        @type password            string
        
        @param domain             Domain to unregister
        @type domain              string
        
        @param message            message to be sent
        @type message             string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
        """
        result = self._rootobject.sendMessageToNoc(customerguid,username,password,domain,message,jobguid,executionparams)
        return result


    def listAvailableCPUNodes (self, memorymin, hypervisor = "", includeappliancehost = "", jobguid = "", executionparams = {}):
        """
        
        Lists all cpu/combined nodes with at least memorymin memory available for a Virtual Machine.
        * No backups or templates.
        * Not the CPU node on which the appliance is running.

        @execution_method = sync

        @param  memorymin:            Minimum available memory required in MB.
        @type memorymin:              integer

        @param  hypervisor:           Hypervisor running on the node (optional)
        @type hypervisor:             string

        @param includeappliancehost:  Include the host of the appliance machine in the list
        @type includeappliancehost:   boolean

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary

        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'MyWebServer',
        @note:                                          'description': 'My Personal Web Server',
        @note:                                          'status': 'RUNNING',
        @note:                                          'os': 'LINUX',
        @note:                                          'hostname': 'web001',
        @note:                                          'memory': 4096,
        @note:                                          'nrcpu': 2,
        @note:                                          'memoryavailable': 2048,
        @note:                                          'hypervisor': 'VIRTUALBOX30',
        @note:                                          'importancefactor': 3},
        @note:                                        { 'machineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'MyDbServer',
        @note:                                          'description': 'My Personal DB Server',
        @note:                                          'status': 'RUNNING',
        @note:                                          'os': 'LINUX',
        @note:                                          'hostname': 'db001',
        @note:                                          'memory': 4096,
        @note:                                          'nrcpu': 4,
        @note:                                          'memoryavailable': 2048,
        @note:                                          'hypervisor': 'VIRTUALBOX30',
        @note:                                          'importancefactor': 2}]}
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listAvailableCPUNodes(memorymin,hypervisor,includeappliancehost,jobguid,executionparams)
        return result


    def sendMail (self, subject, body = "", sender = "", to = "", jobguid = "", executionparams = {}):
        """
        
        Sends a mail using smtp 

        @param subject:           Subject for the email 
        @type subject:            string

        @param body:              Body of the mail
        @type body:               string
        
        @param sender:            The email address of the sender
        @type sender:             string
        
        @param to:                The email address of the addressee (when None admin is the target)
        @type to:                 string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
        """
        result = self._rootobject.sendMail(subject,body,sender,to,jobguid,executionparams)
        return result


    def startMachines (self, machineguids = [], jobguid = "", executionparams = {}):
        """
        
        Starts multiple machines at once 

        @param machineguids:      guids of the machines to start
        @type machineguids:       list

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.startMachines(machineguids,jobguid,executionparams)
        return result


    def listSmartclientByDevice (self, deviceguid = "", jobguid = "", executionparams = {}):
        """
        
        Gets the list of smartclients by deviceguid

        @param deviceguid           Guid of the device
        @type deviceguid:           guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    information [{ description , iqn , address, machinename }]
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listSmartclientByDevice(deviceguid,jobguid,executionparams)
        return result


    def getAvailableHypervisors (self, jobguid = "", executionparams = {}):
        """
        
        Lists available hypervisors

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getAvailableHypervisors(jobguid,executionparams)
        return result


    def changeAgentPassword (self, oldpwd, newpwd, jobguid = "", executionparams = {}):
        """
        
        Modify the password of the agent v4.
        
        @param oldpwd:                current password of the agent
        @type oldpwd:                 string
        
        @param newpwd:                new password for the agent
        @type newpwd:                 string
        
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid
        
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.changeAgentPassword(oldpwd,newpwd,jobguid,executionparams)
        return result


    def startApplications (self, applicationguids = [], jobguid = "", executionparams = {}):
        """
        
        Starts a list of applications     

        @param machineguid:           List of applications guids
        @type machineguid:            list

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.startApplications(applicationguids,jobguid,executionparams)
        return result


    def validateDomain (self, machineguids = [], domain = "", jobguid = "", executionparams = {}):
        """
        
        validates a domain for a customer

        @param machineguids:      list of machineguids to be validated (if none are passed all pmachineguids are tested) 
        @type machineguids:       list

        @param domain:            Domain to validate
        @type domain:             string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
        """
        result = self._rootobject.validateDomain(machineguids,domain,jobguid,executionparams)
        return result


    def deleteSnapshots (self, policyguid = "", jobguid = "", executionparams = {}):
        """
        
        Deletes all outdated snapshots off all disks

        @param policyguid:          Guid of the snapshot retention policy to detect outdated snapshots
        @type policyguid:           guid
        
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid
        

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.deleteSnapshots(policyguid,jobguid,executionparams)
        return result


    def addDataDisks (self, machineguid, diskinfo = [], jobguid = "", executionparams = {}):
        """
        
        Adds multiple data disks at once to a machine
        
        @param machineguid:           guid of the machine rootobject
        @type machineguid:            guid
    
        @param diskinfo:              [ { name: , size: , description, retentionpolicyguid} ]
        @type diskinfo:               list
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with added diskguids e.g. params  { 'result': [diskguids] }  
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addDataDisks(machineguid,diskinfo,jobguid,executionparams)
        return result


    def addSmartClientDevice (self, name, macaddress, cloudspaceguid, description = "", racku = 1, racky = 0, rackz = 0, jobguid = "", executionparams = {}):
        """
        
        Adds a new smart client device to a Smart Style Office environment

        @param  name                name of the device
        @type name                  string

        @param macaddress           MAC address of the new resource node
        @type macaddress            string

        @param description          remarks on the device
        @type description           type_description

        @param racku                size of the device, measured in u e.g. 1u high
        @type racku                 int

        @param racky                physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        @type racky                 int

        @param rackz                physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        @type rackz                 int

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addSmartClientDevice(name,macaddress,cloudspaceguid,description,racku,racky,rackz,jobguid,executionparams)
        return result


    def cleanup (self, maxage = 30, jobguid = "", executionparams = {}):
        """
        
        DRP model cleansing:
          Removes versioning information on all rootobjects
          Removes events and jobs older than maxage
                             
        @param maxage:            how long the information is kept
        @type maxage:             int

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}

        @rtype:                   dictionary
        
        """
        result = self._rootobject.cleanup(maxage,jobguid,executionparams)
        return result


    def listSystemNASISOImages (self, jobguid = "", executionparams = {}):
        """
        
        Lists iso images available on the SystemNAS

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with available iso images and their paths
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listSystemNASISOImages(jobguid,executionparams)
        return result


    def maintenance (self, duration = 3600, jobguid = "", executionparams = {}):
        """
        
        Execute maintenance tasks on SSO environment.
        
        @param duration:            duration of the maintenance tasks (seconds)
        @type duration:             int
        
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.maintenance(duration,jobguid,executionparams)
        return result


    def addVirtualServerFromTemplate (self, cloudspaceguid, templatemachineguid, name, languids = [], description = "", parentmachineguid = "", userinfo = "", vdcinfo = "", defaultgateway = "", jobguid = "", executionparams = {}):
        """
        
        Adds a new virtual server to a Smart Style Office environment

        @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:              guid

        @param templatemachineguid:         guid of the machine this machine will be based on.
        @type  templatemachineguid:         guid

        @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                         string

        @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        @type languids:                     array

        @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type description:                  string

        @param parentmachineguid:           guid of the machine this machine will be created upon.
        @type  parentmachineguid:           guid
        
        @param userinfo:                    {clouduserguid,login,password,email, firstname,lastname}
        @type userinfo:                     dictionary

        @param vdcinfo:                     {vdcguid,posx,posy}
        @type vdcinfo:                      dictionary
        
        @param defaultgateway:              Default gateway for the machine
        @type defaultgateway:               string

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addVirtualServerFromTemplate(cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,userinfo,vdcinfo,defaultgateway,jobguid,executionparams)
        return result


    def getVirtualMachineDiskInfo (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        returns information about the virtual machine disk information 

        @security administrators

        @param machineguid:         machineguid of the virtual machine
        @type machineguid:          guid
                
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary 
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getVirtualMachineDiskInfo(machineguid,jobguid,executionparams)
        return result


    def addVirtualDesktop (self, cloudspaceguid, name, machinetype = "PHYSICAL", status = "CONFIGURED", bootstatus = "FROMDISK", assetid = "", memory = 0, memoryminimal = 0, nrcpu = 1, cpufrequency = 0, description = "", parentmachineguid = "", networkinfo = [], diskinfo = [], osguid = "", deviceguid = "", hostname = "", backup = "", boot = "", alias = "", userinfo = "", hypervisor = "", importancefactor = "", defaultgateway = "", monitors = [], jobguid = "", executionparams = {}):
        """
        
        Creates a new virtual desktop.

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

        @param networkinfo:                network information {nr_nics: , info { languid, ip} }
        @type networkinfo:                 dictionary

        @param diskinfo:                   disk information info [{ diskguid, size, role}]
        @type diskinfo:                    list

        @param osguid:                     osguid of the machine.
        @type  osguid:                     guid

        @param deviceguid:                 deviceguid of the machine.
        @type  deviceguid:                 guid

        @param hostname:                   hostname of the machine
        @type hostname:                    string

        @param backup:                     whether to backup the machine
        @type backup:                      boolean

        @param boot:                       whether to boot the machine when pmachine starts
        @type boot:                        boolean

        @param alias:                      alias of the machine
        @type alias:                       string

        @param userinfo:                   {clouduserguid,login,password,email, firstname,lastname}
        @type userinfo:                    dictionary

        @param hypervisor:                 hypervisor of the machine.
        @type hypervisor:                  string

        @param importancefactor:           hypervisor of the machine.
        @type importancefactor:            string

        @param defaultgateway:             Default gateway for the machine
        @type defaultgateway:              string
        
        @param monitors:                   monitors configuration ['1024x768x24','800x600x24']
        @type monitors:                    list

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addVirtualDesktop(cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,osguid,deviceguid,hostname,backup,boot,alias,userinfo,hypervisor,importancefactor,defaultgateway,monitors,jobguid,executionparams)
        return result


    def getVirtualServerInfo (self, macaddress, jobguid = "", executionparams = {}):
        """
        
        Returns information about the virtual server

        @param macaddress:          macaddress of the virtual server
        @type macaddress:           string
                
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getVirtualServerInfo(macaddress,jobguid,executionparams)
        return result


    def addSmartClientKioskModeFromTemplate (self, cloudspaceguid, templatemachineguid, name, languids = [], description = "", parentmachineguid = "", deviceguid = "", devicename = "", macaddress = "", vdcinfo = "", jobguid = "", executionparams = {}):
        """
        
        Adds a new smart client based on a template to a Smart Style Office environment

        @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:              guid

        @param templatemachineguid:         guid of the machine this machine will be based on.
        @type  templatemachineguid:         guid

        @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                         string

        @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        @type languids:                     array

        @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type description:                  string

        @param parentmachineguid:           guid of the machine this machine will be created upon.
        @type  parentmachineguid:           guid

        @param deviceguid                   guid of an existing smart client device to which this virtual desktop is linked
        @type deviceguid                    guid

        @param  devicename                  name for the new smart client device to which this virtual desktop is linked
        @type devicename                    string

        @param  macaddress                  mac address for the new smart client device to which this virtual desktop is linked
        @type macaddress                    string

        @param vdcinfo:                     {vdcguid,posx,posy}
        @type vdcinfo:                      dictionary

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addSmartClientKioskModeFromTemplate(cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,deviceguid,devicename,macaddress,vdcinfo,jobguid,executionparams)
        return result


    def listFOCVolumes (self, machineguid, jobguid = "", executionparams = {}):
        """
         
        List FailOver Cache volumes on a given machine
        
        @execution_method = sync
        
        @param machineguid:           guid of the machine to list the FOC volumes
        @type  machineguid:           guid
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      list of volumes having the FOC on this node 
        @rtype:                       list

        @raise e:                     In case an error occurred, exception is raised        
        
        """
        result = self._rootobject.listFOCVolumes(machineguid,jobguid,executionparams)
        return result


    def addNode (self, macaddress, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Adds a new node to a Smart Style Office environment

        @security administrators

        @param macaddress:          MAC address of the new node
        @type macaddress:           string

        @param name:                Name for the new node
        @type name:                 string

        @param description:         Description for the new node
        @type description:          string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary with the new device guid  as result and jobguid: {'result': '2388d3d3-4de4-45fe-b17f-4f1ca05ff062', 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addNode(macaddress,name,description,jobguid,executionparams)
        return result


    def getVirtualDesktopInfo (self, macaddress, jobguid = "", executionparams = {}):
        """
        
        returns information about the virtual desktop 

        @param macaddress:          macaddress of the virtual desktop
        @type macaddress:           string
                
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getVirtualDesktopInfo(macaddress,jobguid,executionparams)
        return result


    def addVirtualDesktopFromTemplate (self, cloudspaceguid, templatemachineguid, name, languids = [], description = "", parentmachineguid = "", userinfo = "", vdcinfo = "", defaultgateway = "", jobguid = "", executionparams = {}):
        """
        
        Adds a new virtual desktop to a Smart Style Office environment

        @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:              guid

        @param templatemachineguid:         guid of the machine this machine will be based on.
        @type  templatemachineguid:         guid

        @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                         string

        @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        @type languids:                     array

        @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type description:                  string

        @param parentmachineguid:           guid of the machine this machine will be created upon.
        @type  parentmachineguid:           guid

        @param userinfo:                    {clouduserguid,login,password,email, firstname,lastname}
        @type userinfo:                     dictionary

        @param vdcinfo:                     {vdcguid,posx,posy}
        @type vdcinfo:                      dictionary
        
        @param defaultgateway:              Default gateway for the machine
        @type defaultgateway:               string

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addVirtualDesktopFromTemplate(cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,userinfo,vdcinfo,defaultgateway,jobguid,executionparams)
        return result


    def assignDeviceToPowerPort (self, deviceguid, powerswitchdeviceguid, powerportsequence, jobguid = "", executionparams = {}):
        """
        
        Assigns a device to a power port of a powerswitch

        @param deviceguid:              guid of the device assigned to the power port
        @type deviceguid:               guid
        
        @param powerswitchdeviceguid:   guid of the powerswitch device
        @type powerswitchdeviceguid:    guid
        
        @param powerportsequence:       sequence of the powerport
        @type powerportsequence:        int        
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary
        @rtype:                         dictionary
 
        @raise e:                       In case an error occurred, exception is raised
        
        """
        result = self._rootobject.assignDeviceToPowerPort(deviceguid,powerswitchdeviceguid,powerportsequence,jobguid,executionparams)
        return result


    def getVirtualDesktopClient (self, macaddress, jobguid = "", executionparams = {}):
        """
        
        returns current user connected to the virtual desktop 

        @param macaddress:          macaddress of the virtual desktop
        @type macaddress:           string
                
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary having Ipaddress of the client connected to the Vmachine
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getVirtualDesktopClient(macaddress,jobguid,executionparams)
        return result


    def canMove (self, movementplan = {}, failover = False, minimalcapacity = False, jobguid = "", executionparams = {}):
        """
        
        Checks whether vmachine(s) can be moved to other node(s) 

        @param movementplan:          dict of movement plan of the machines { sourcevmachine : target host }
        @type movementplan:           dict

        @param failover:              flag to use failovering workflow
        type failover:                boolean
        
        @param minimalcapacity:       flag to use minimal capacity workflow (e.g. minimal memory...)
        @type minimalcapacity:        boolean

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      True or False 
        @rtype:                       boolean
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.canMove(movementplan,failover,minimalcapacity,jobguid,executionparams)
        return result


    def listAvailableStorageDaemons (self, jobguid = "", executionparams = {}):
        """
        
        Lists all available storage daemons

        @execution_method = sync

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21435',
        @note:                              'result: [{ 'applicationguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'machineguid': '55544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'diskguid': '977cf8ee-8845-494f-bbc5-6ac559660201',
        @note:                                          'ipaddress': '192.168.0.1',
        @note:                                          'port': '23514',
        @note:                                          'path': '/mnt/dss/disk/977cf8ee-8845-494f-bbc5-6ac559660201',
        @note:                                          'status': 'ONLINE',
        @note:                                          'freespace': '465000'},
        @note:                                        { 'applicationguid': '33544B07-4129-47B1-8690-B92C0DB21435',
        @note:                                          'machineguid': '55544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'diskguid': '977cf8ee-8845-494f-bbc5-6ac559660202',
        @note:                                          'ipaddress': '192.168.0.1',
        @note:                                          'port': '23515',
        @note:                                          'path': '/mnt/dss/disk/977cf8ee-8845-494f-bbc5-6ac559660202',
        @note:                                          'status': 'ONLINE',
        @note:                                          'freespace': '465000'}]}
        
        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listAvailableStorageDaemons(jobguid,executionparams)
        return result


    def addSmartClientUserModeFromTemplate (self, cloudspaceguid, templatemachineguid, name, languids = [], description = "", parentmachineguid = "", userinfo = "", vdcinfo = "", jobguid = "", executionparams = {}):
        """
        
        Adds a new smart client from a template to a Smart Style Office environment

        @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        @type  cloudspaceguid:              guid

        @param templatemachineguid:         guid of the machine this machine will be based on.
        @type  templatemachineguid:         guid

        @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                         string

        @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        @type languids:                     array

        @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        @type description:                  string

        @param parentmachineguid:           guid of the machine this machine will be created upon.
        @type  parentmachineguid:           guid

        @param userinfo:                    {clouduserguid,login,password,email, firstname,lastname}
        @type userinfo:                     dictionary

        @param vdcinfo:                     {vdcguid,posx,posy}
        @type vdcinfo:                      dictionary

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addSmartClientUserModeFromTemplate(cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,userinfo,vdcinfo,jobguid,executionparams)
        return result


    def getSSOVersion (self, jobguid = "", executionparams = {}):
        """
        
        Lists version of the current SSO

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getSSOVersion(jobguid,executionparams)
        return result


    def applyTemplate (self, diskguid, machineguid, overwrite = False, jobguid = "", executionparams = {}):
        """
        
        apply template to specific machine

        @param diskguid             guid of orignial boot disk
        @type diskguid:             guid

        @param machineguid:         guid of the machine rootobject
        @type machineguid:          guid

        @param overwrite:           boolean value indicating whether the old boot disk in the machine will be overwritten
        @type overwrite:            boolean

        @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.applyTemplate(diskguid,machineguid,overwrite,jobguid,executionparams)
        return result


    def initialize (self, email, password, ipaddress, netmask, gateway, dnsserver, network = "", netmaskpublic = "", startip = "", endip = "", sitename = "", sitedescription = "", siteaddress = "", sitecity = "", sitecountry = "", setuptype = "SSO", firstnodetype = "COMBINEDNODE", networkname = "", timezonename = "", timezonedelta = "", smtpserver = "", smtplogin = "", smtppassword = "", nrreservedip = -1, jobguid = "", executionparams = {}):
        """
        
        Initializes a new Smart Style Office environment

        @security administrators

        @param email                Email for the administrator account. All system level communication will be send to this email address.
        @type email                 string

        @param password             Password for the administrator account.
        @type password              string

        @param ipaddress            The public IP address for the appliance.
        @type ipaddress             string

        @param netmask              Netmask of the customer LAN.
        @type netmask               string

        @param gateway              Gateway IP address of the customer LAN.
        @type gateway               string

        @param dnsserver            IP address of the DSN server of the customer LAN.
        @type dnsserver             string

        @param network              Network range to be used as public LAN. Will be used if Smart Style Office environment is NOT integrated into customer LAN.
        @type network               string

        @param netmaskpublic        Netmask of the new public LAN that will be created.
        @type netmaskpublic         string

        @param startip              Start IP address of the public LAN. Will be used if Smart Style Office environment is integrated into customer LAN.
        @type startip               string

        @param endip                End IP address of the public LAN. Will be used if Smart Style Office environment is integrated into customer LAN.
        @type endip                 string

        @param sitename             Name for this Smart Style Office site.
        @type sitename              string

        @param sitedescription      Description for this Smart Style Office site.
        @type sitedescription       string

        @param siteaddress          Address for this Smart Style Office site.
        @type siteaddress           string

        @param sitecity             City for this Smart Style Office site.
        @type sitecity              string

        @param sitecountry          County for this Smart Style Office site.
        @type sitecountry           string
        
        @param setuptype:           Define setup type configuration [SSO | CLOUDMIRROR]
        @type setuptype:            string

        @param firstnodetype:       Define node type configuration for first node [COMBINEDNODE | CPUNODE]
        @type firstnodetype:        string
        
        @param networkname:         name of the public network 
        @type networkname:          string

        @param timezonename:        timezone to be set for physical machines 
        @type timezonename:         string        
        
        @param timezonedelta:       delta of timeZone for the location.
        @type timezonedelta:        float        
        
        @param smtpserver:          Smtp server
        @type smtpserver:           string
        
        @param smtplogin:           Login for the Smtp server
        @type smtplogin:            string
        
        @param smtppassword:        Password for the Smtp server
        @type smtppassword:         string
        
        @param nrreservedip:        Number of reserved ip addresses for the sso nodes
        @type  nrreservedip:        integer 
        
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.initialize(email,password,ipaddress,netmask,gateway,dnsserver,network,netmaskpublic,startip,endip,sitename,sitedescription,siteaddress,sitecity,sitecountry,setuptype,firstnodetype,networkname,timezonename,timezonedelta,smtpserver,smtplogin,smtppassword,nrreservedip,jobguid,executionparams)
        return result


    def moveMachine (self, movementplan = {}, failover = False, minimalcapacity = False, jobguid = "", executionparams = {}):
        """
        
        Moves a machine to another node     

        @param movementplan:          dict of movement plan of the machines { sourcevmachine : target host }
        @type movementplan:           dict

        @param failover:              flag to use failovering workflow
        type failover:                boolean
        
        @param minimalcapacity:       flag to use minimal capacity workflow (e.g. minimal memory...)
        @type minimalcapacity:        boolean

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.moveMachine(movementplan,failover,minimalcapacity,jobguid,executionparams)
        return result


    def readConfigurationInfo (self, sourceuri, jobguid = "", executionparams = {}):
        """
        
        Get information about a specified image configuration 

        @param sourceuri:             URI where the configuration resides
        @type sourceuri:              string
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with available templates and its path
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.readConfigurationInfo(sourceuri,jobguid,executionparams)
        return result


    def stopApplications (self, applicationguids = [], jobguid = "", executionparams = {}):
        """
        
        Stops a list of applications     

        @param machineguid:           List of applications guids
        @type machineguid:            list

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.stopApplications(applicationguids,jobguid,executionparams)
        return result


    def restartApplications (self, applicationguids = [], jobguid = "", executionparams = {}):
        """
        
        Restarts a list of applications     

        @param machineguid:           List of applications guids
        @type machineguid:            list

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary
        
        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.restartApplications(applicationguids,jobguid,executionparams)
        return result


    def addSmartClientKioskMode (self, cloudspaceguid, name, machinetype = "PHYSICAL", status = "CONFIGURED", bootstatus = "FROMDISK", assetid = "", memory = 0, memoryminimal = 0, nrcpu = 1, cpufrequency = 0, description = "", parentmachineguid = "", networkinfo = [], diskinfo = [], osguid = "", deviceguid = "", hostname = "", importancefactor = "", backup = "", boot = "", alias = "", devicename = "", macaddress = "", jobguid = "", executionparams = {}):
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

        @param networkinfo:                network information {nr_nics: , info { languid, ip} }
        @type networkinfo:                 dictionary

        @param diskinfo:                   disk information info [{ diskguid, size, role}]
        @type diskinfo:                    list

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

        @param alias:                       alias of the machine
        @type alias:                        string

        @param  devicename                  name for the new smart client device to which this virtual desktop is linked
        @type devicename                    string

        @param  macaddress                  mac address for the new smart client device to which this virtual desktop is linked
        @type macaddress                    string

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                             dictionary

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addSmartClientKioskMode(cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,osguid,deviceguid,hostname,importancefactor,backup,boot,alias,devicename,macaddress,jobguid,executionparams)
        return result


    def getApplianceInfo (self, jobguid = "", executionparams = {}):
        """
        
        Lists info about the appliance vmachine

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getApplianceInfo(jobguid,executionparams)
        return result


    def resetFailoverCache (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Resets the Failover Cache of a disk (eg when degraded)

        @param diskguid:          guid of the disk
        @type diskguid:           guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  string containing status OK_SYNC, OK_STANDALONE, CATCHUP , DEGRADED or None
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.resetFailoverCache(diskguid,jobguid,executionparams)
        return result


    def getFailoverCacheStatus (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Returns the Failover Cache status of a disk when existing

        @param diskguid:          guid of the disk
        @type diskguid:           guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  string containing status OK_SYNC, OK_STANDALONE, CATCHUP , DEGRADED or None
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getFailoverCacheStatus(diskguid,jobguid,executionparams)
        return result


    def listWebservices (self, action, jobguid = "", executionparams = {}):
        """
                
        Lists the webservice urls for a certain action
        
        @execution_method = sync
        
        @param action                 The webservice needed (REGISTER, UNREGISTER, KEEPALIVE)
        @param action                 string
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid
                
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listWebservices(action,jobguid,executionparams)
        return result


    def getSystemNasInfo (self, jobguid = "", executionparams = {}):
        """
        
        Lists info systemnas

        @execution_method = sync

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getSystemNasInfo(jobguid,executionparams)
        return result


    def failoverManagement (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Moves and Initializes all management applications to node with specified machineguid

        @execution_method = async

        @param machineguid:          Guid of the machine to fail over the management applications to
        @type machineguid:          guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised

        
        """
        result = self._rootobject.failoverManagement(machineguid,jobguid,executionparams)
        return result


    def addSmartClientUserMode (self, cloudspaceguid, name, machinetype = "PHYSICAL", status = "CONFIGURED", bootstatus = "FROMDISK", assetid = "", memory = 0, memoryminimal = 0, nrcpu = 1, cpufrequency = 0, description = "", parentmachineguid = "", networkinfo = [], diskinfo = [], osguid = "", deviceguid = "", hostname = "", backup = "", boot = "", alias = "", userinfo = "", jobguid = "", executionparams = {}):
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

        @param networkinfo:                network information {nr_nics: , info { languid, ip} }
        @type networkinfo:                 dictionary

        @param diskinfo:                   disk information info [{ diskguid, size, role}]
        @type diskinfo:                    list

        @param osguid:                     osguid of the machine.
        @type  osguid:                     guid

        @param deviceguid:                 deviceguid of the machine.
        @type  deviceguid:                 guid

        @param hostname:                   hostname of the machine
        @type hostname:                    string

        @param backup:                     whether to backup the machine
        @type backup:                      boolean

        @param boot:                       whether to boot the machine when pmachine starts
        @type boot:                        boolean

        @param alias:                      alias of the machine
        @type alias:                       string

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addSmartClientUserMode(cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,osguid,deviceguid,hostname,backup,boot,alias,userinfo,jobguid,executionparams)
        return result


    def optimizeDisks (self, diskguids = [], scrubagentmachineguid = "", jobguid = "", executionparams = {}):
        """
        
        Optimizes a disk. E.g. defragments a Physical disk or scrubs a DSS disks

        @param diskguid:                guids of the disks to optimize.
        @type diskguid:                 list

        @param scrubagentmachineguid:   guid of the machine where scrubbing agent is running
        @type scrubagentmachineguid:    guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        """
        result = self._rootobject.optimizeDisks(diskguids,scrubagentmachineguid,jobguid,executionparams)
        return result


    def getAssignedFOCNode (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Retrieves the pmachine of the FailOver Cache for the given disk 

        @execution_method = sync
        
        @param diskguid:          guid of the disk
        @type diskguid:           guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dict with applicationguid and foc machineguid
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getAssignedFOCNode(diskguid,jobguid,executionparams)
        return result


    def listAvailableStorageNodes (self, jobguid = "", executionparams = {}):
        """
        
        Lists all available storage nodes

        @execution_method = sync

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary
        
        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listAvailableStorageNodes(jobguid,executionparams)
        return result


    def sendSNMPTrap (self, message, hostdestination = "127.0.0.1", port = 126, community = "aserver", jobguid = "", executionparams = {}):
        """
        
        Generate a notification (trap) to report an event to the SNMP manager with the specified message.

        @param message:           Message of notification 
        @type message:            string

        @param hostdestination:   Specifies the target network manager host to which the trap message will be sent. 
        @type hostdestination:    string
        
        @param port:              Port number on host
        @type port:               int
        
        @param community:         Specifies community name to use
        @type community:          string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
        """
        result = self._rootobject.sendSNMPTrap(message,hostdestination,port,community,jobguid,executionparams)
        return result


    def initializeNode (self, deviceguid, nodetype, name = "", description = "", hypervisor = "", jobguid = "", executionparams = {}):
        """
        
        Initializes a device as a specified node type in the Smart Style Office environment.

        @security administrators

        @param deviceguid:          Guid of the device to install
        @type deviceguid:           guid

        @param nodetype:            Node type of the device to add (CPU, STORAGE or COMBINED)
        @type nodetype:             string

        @param name:                Name for the new node
        @type name:                 string

        @param description:         Description for the new node
        @type description:          string
        
        @param hypervisor:          Hypervisor for the new node
        @type hypervisor:           string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.initializeNode(deviceguid,nodetype,name,description,hypervisor,jobguid,executionparams)
        return result


    def setTimezone (self, timezone, timezonedelta = "", jobguid = "", executionparams = {}):
        """
        
        sets timezone for the sso environment

        @param timezone:            Timezone to be set
        @type timezone:             string
        
        @param timezonedelta:       delta of timeZone for the location.
        @type timezonedelta:        float
        
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.setTimezone(timezone,timezonedelta,jobguid,executionparams)
        return result


    def generateMacAddress (self, languid, customerguid, jobguid = "", executionparams = {}):
        """
        
        Generates a new MAC address depending on LAN and customer

        @execution_method = sync

        @param languid              guid of languid
        @type languid:              guid

        @param customerguid         guid of customerguid
        @type customerguid:         guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    mac address
        @rtype:                     string

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.generateMacAddress(languid,customerguid,jobguid,executionparams)
        return result


    def listSmartclientByUser (self, clouduserguid, customerguid = "", jobguid = "", executionparams = {}):
        """
        
        Gets the list of smartclients for a specific user

        @execution_method = sync

        @param clouduserguid        guid of clouduser
        @type clouduserguid:        guid

        @param customerguid         guid of customerguid
        @type customerguid:         guid

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    information [{ description , iqn , address, machinename }]
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listSmartclientByUser(clouduserguid,customerguid,jobguid,executionparams)
        return result


    def getVirtualMachineInfo (self, macaddress, machinetype = "", jobguid = "", executionparams = {}):
        """
        
        Returns information about the virtual machine

        @param macaddress:          macaddress of the virtual machine
        @type macaddress:           string
        
        @param machinetype:         type of the virtual machine (VIRTUALSERVER | VIRTUALDESKTOP)
        @type machinetype:          string
                
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.getVirtualMachineInfo(macaddress,machinetype,jobguid,executionparams)
        return result


