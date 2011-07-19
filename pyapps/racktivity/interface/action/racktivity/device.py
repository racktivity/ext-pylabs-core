class device():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name,devicetype,description="",template=False,rackguid="",datacenterguid="",racku = 0,racky = 0,rackz = 0,modelnr="",serialnr="",firmware="",\
               lastcheck="",status="",parentdeviceguid="",components=list(),pdisks=list(),nicports=list(),powerports=list(),lastrealitycheck="", accounts="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Create a new device.

        
        @security administrators

        @doc  name:                    name of the device
        @type name:                    string

        @param devicetype:             device type
        @type devicetype:              devicetype

        @param  description:           remarks on the device
        @type description:             type_description

        @param template:               is template, when template used as example for an application
        @type template:                bool

        @param rackguid:               guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
        @type rackguid:                guid

        @param datacenterguid :        guid of the datacenter to which the device belongs - can be None e.g. for devices in stock or in repair
        @type datacenterguid:          guid

        @param  racku:                 size of the device, measured in u e.g. 1u high
        @type racku:                   int

        @param racky:                  physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        @type racky:                   int

        @param  rackz:                 physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        @type rackz:                   int

        @param  modelnr:               model number of the device
        @type modelnr:                 string(60)

        @param  serialnr:              serial number of the device
        @type serialnr:                string(60)

        @param firmware:               firmware identifier of the device
        @type firmware:                string(60)

        @param lastcheck:              last time device was inspected
        @type lastcheck:               type_date

        @param  status:                device status
        @type status:                  devicestatustype

        @param parentdeviceguid:       parent device, e.g. blade belongs to bladechasis
        @type parentdeviceguid:        guid

        @param components:             list of components which are part of the device , do not use fo disks & nics
        @type components:              array(component)

        @param  pdisks:                physical disks which are part of device
        @type pdisks:                  array(pdisk)

        @param  nicports:              nicports which are part of device
        @type nicports:                array(nicport)

        @param  powerports:            powerports which are part of device
        @type powerports:              array(powerport)

        @param  lastrealitycheck:      date and time of last check on the device with reality
        @type lastrealitycheck:        type_date

        @param  accounts:              list of accounts available in this device (e.g. bios accounts)
        @type  accounts:               array(account)
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) and deviceguid as result and jobguid: {'result':{returncode:'True', deviceguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, deviceguid, request="", jobguid="", executionparams=dict()):
        """
        Delete a device.

        
        @security administrators
        
        @param deviceguid:            Guid of the device rootobject to delete.
        @type deviceguid:             guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def updateModelProperties(self, deviceguid,name="",devicetype="",description="",template=False,rackguid="",datacenterguid="",racku = 1,racky = 0,rackz = 0,modelnr="",serialnr="",firmware="",\
                              lastcheck="",status="",parentdeviceguid="",components=list(),pdisks=list(),nicports=list(),powerports=list(),lastrealitycheck="",accounts="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        
        @security administrators
        
        @param deviceguid:              Guid of the device specified
        @type deviceguid:               guid

        @doc  name:                     name of the device
        @type name:                     string

        @param devicetype:              device type
        @type devicetype:               devicetype

        @param  description:            remarks on the device
        @type description:              type_description

        @param template:                is template, when template used as example for an application
        @type template:                 bool

        @param rackguid:                guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
        @type rackguid:                 guid

        @param datacenterguid :         guid of the datacenter to which the device belongs - can be None e.g. for devices in stock or in repair
        @type datacenterguid:           guid

        @param  racku:                  size of the device, measured in u e.g. 1u high
        @type racku:                    int

        @param racky:                   physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        @type racky:                    int

        @param  rackz:                  physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        @type rackz:                    int

        @param  modelnr:                model number of the device
        @type modelnr:                  string(60)

        @param  serialnr:               serial number of the device
        @type serialnr:                 string(60)

        @param firmware:                firmware identifier of the device
        @type firmware:                 string(60)

        @param lastcheck:               last time device was inspected
        @type lastcheck:                type_date

        @param  status:                 device status
        @type status:                   devicestatustype

        @param parentdeviceguid:        parent device, e.g. blade belongs to bladechasis
        @type parentdeviceguid:         guid

        @param components:              list of components which are part of the device , do not use fo disks & nics
        @type components:               array(component)

        @param  pdisks:                 physical disks which are part of device
        @type pdisks:                   array(pdisk)

        @param  nicports:               nicports which are part of device
        @type nicports:                 array(nicport)

        @param  powerports:             powerports which are part of device
        @type powerports:               array(powerport)

        @param  lastrealitycheck:       date and time of last check on the device with reality
        @type lastrealitycheck:         type_date

        @param  accounts:               list of accounts available in this device (e.g. bios accounts)
        @type  accounts:                array(account)
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with returncode(True) and deviceguid as result and jobguid: {'result':{returncode:'True', deviceguid:guid}, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        """

    def find(self, name="", macaddress="", status="", devicetype="", description="", template="", modelnr="",serialnr="",firmware="", \
             rackguid="",datacenterguid="", parentdeviceguid="",cableguid="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of device guids which met the find criteria.

        @execution_method = sync
        
        @security administrators

        @doc  name:                       Name of the device
        @type name:                       string

        @doc  macaddress:                 MAC address of the device
        @type name:                       string

        @param  status:                   Device status
        @type status:                     devicestatustype

        @param devicetype:                Device type
        @type devicetype:                 string

        @param  description:              Remarks on the device
        @type description:                string

        @param template:                  Is template, when template used as example for an application
        @type template:                   bool

        @param  modelnr:                  Model number of the device
        @type modelnr:                    string

        @param  serialnr:                 Serial number of the device
        @type serialnr:                   string

        @param firmware:                  Firmware identifier of the device
        @type firmware:                   string

        @param rackguid:                  Guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
        @type rackguid:                   guid

        @param datacenterguid :           Guid of the datacenter to which the device belongs - can be None e.g. for devices in stock or in repair
        @type datacenterguid:             guid

        @param parentdeviceguid:          Guid of the parent device, e.g. blade belongs to bladechasis
        @type parentdeviceguid:           guid
        
        @param cableguid:                 Guid of the cable to which the device is connected via his powerport
        @type cableguid:                  guid
        
        @param tags:                      string of tags
        @type tags:                       string
        
        @param jobguid:                   Guid of the job if avalailable else empty string
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                         result dict with returncode(True) and  Array of device guids(guidlist) which met the find criteria specified.
        @rtype:                           array

        @note:                            Example return value:
        @note:                            {'result': {returncode:True, guidlist: '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                             'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                         In case an error occurred, exception is raised
        """

    def list(self, deviceguid="", request="", jobguid="", executionparams=dict()):
        """
        List all devices.

        @execution_method = sync
        
        @param deviceguid:              Guid of the device specified
        @type deviceguid:               guid
        
        @param meteringinfo: If metering info is True, also the latest meteringinfo for this object is listed(current/power & powerfactor)
        @type meteringinfo: boolean(default false)
    
        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        result dict with returncode(True) and  dictionary with array of device info(deviceinfo) as result and jobguid: {'result':{returncode:True, deviceinfo: array}, 'jobguid': guid}, 
        deviceinfo contains the device data but also connectioninfo:{powerportsequence:{meteringdeviceguid:, label:}...} if the port is not connected the values are not defined.
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:        Guid of the device rootobject
        @type rootobjectguid:         guid

        @return:                      rootobject
        @rtype:                       string

        @warning:                     Only usable using the python client.
        """

       
    def listPowerPorts(self, deviceguid, request="", jobguid="", executionparams=dict()):
        """
        Lists information about power ports of the device  
        
        @execution_method = sync
        
        @param deviceguid:          Guid of the device rootobject
        @type deviceguid:           guid
        
        @return:                    result is a dict with returncode(True) and a list of powerports(
        @rtype:                     dictionary
        
        @raise e:                   In case an error occurred, exception is raised
        """
        
    def connectPowerPort(self, deviceguid, portname, cableguid, request="", jobguid="", executionparams=dict()):
        """
        Connect a cable to the powerport of the device 
        
        @param deviceguid: guid of the device
        @type deviceguid: guid
        
        @param portname: name of the power  port
        @type label: string
        
        @param cableguid: cable which will be connected to the power  Port
        @type cableguid: guid
        
        @return:                      dictionary with returncode(True) and deviceguid as result and jobguid: {'result':{returncode:'True', deviceguid:guid}, 'jobguid': guid}
        @rtype:                       dictionary
        """  
        
    def disconnectPowerPort(self, deviceguid, portname="", cableguid="",request="", jobguid="", executionparams=dict()):
        """
        Disonnect a cable from the device  
        
        @param deviceguid: guid of the device
        @type deviceguid: guid
        
        @param portname: name of the power port
        @type label: string
        
        @param cableguid: guid of the cable which is connected to the power port, used when no portname is known.
        @type cableguid: guid
              
        @return:                      dictionary with returncode(True) and deviceguid as result and jobguid: {'result':{returncode:'True', deviceguid:guid}, 'jobguid': guid}
        @rtype:                       dictionary
        """
    
    def getTree(deviceguid, depth=2, jobguid="", executionparams=dict()):
        """
        Returns a json dict with a tree structure.
        
        @param deviceguid: guid of the device
        @type deviceguid: guid
        
        @param depth: depth to return, default 2. 0 means unlimited depth
        @type depth: integer
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and 'result': {'name','type',children = []}
        @rtype:                   dictionary
        """

    def updateACL(self, rootobjectguid, cloudusergroupnames={}, request="", jobguid="", executionparams=dict()):
        """
        Update ACL in a rootobject.
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param cloudusergroupnames:          Dict with keys in the form of cloudusergroupguid_actionname and empty values for now.
        @type cloudusergroupnames:           dict

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """

    def addGroup(self, rootobjectguid, group, action="", recursive=False, request="", jobguid="", executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to add to the specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group gets access to all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is added to all children objects
        @type recursive:                     Boolean 
        
        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def deleteGroup(self, rootobjectguid, group, action="", recursive=False, request="", jobguid="", executionparams=dict()):
        """
        Delete a group in the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to delete for a specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group is deleted from all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is deleted from all children objects
        @type recursive:                     Boolean         

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def hasAccess(self, rootobjectguid, groups, action, request="", jobguid="", executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the selected root object.
        @type rootobjectguid:                guid

        @param groups:                       list of groups to be checked
        @type groups:                        list 

        @param action:                       name of the required action.
        @type action:                        String

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode as result and jobguid: {'result':{returncode:'True'}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """