class MeteringDevice():
    """
    root object actions on a meteringdevice
    these actions do modify the DRP and call the actor actions to do the work in the reality
    """
    
    def create(self, name, id, meteringdevicetype, template, rackguid, parentmeteringdeviceguid=None, clouduserguid=None, height=1, positionx=0, positiony=0, positionz=0, attributes={}, networkinfo=None, powerinputinfo=[], poweroutputinfo=[], portsinfo=[], sensorinfo=[],  accounts=[], tags=None, meteringdeviceconfigstatus="CONFIGURED", request=None, jobguid=None, executionparams=dict()):
        """
        Create a meteringdevice.
       
        @security administrators
        
        @param name:                   Name for the meteringdevice.
        @type name:                    string
        
        @param id:                     id of the device (e.g T1, P1, ...)
        @type id:                      string 

        @param meteringdevicetype:     Type of the rack meteringdevice. Can be one of the following values PM0816-ZB, PM0816, PM0816-ZB-S10, PM0816-S10
        @type meteringdevicetype:      string
        
        @param template:               is template, when template used as example for a meteringdevice
        @type template:                bool

        @param rackguid:               Guid of the rack in which the meteringdevice is located.
        @type rackguid:                guid

        @param parentmeteringdeviceguid:   Guid of the master controller in case of a slave meteringdevice.
        @type parentmeteringdeviceguid:    guid

        @param clouduserguid:          Guid of the cloud user who owns this meteringdevice
        @type clouduserguid:           guid

        @param height:                 Height of the meteringdevice in U.
        @type height:                  integer

        @param positionx:              X position of the meteringdevice in rack.
        @type positionx:               integer

        @param positiony:              Y position of the meteringdevice in rack.
        @type positiony:               integer

        @param positionz:              Z position of the meteringdevice in rack. 0 means at the front side of the rack, 1 at the back side.
        @type positionz:               integer
        
        @param networkinfo:            network information {ipaddress:"", port:"", protocol:""}
        @param networkinfo:            dictionary
                
        @param powerinputinfo:         list of powerinputinfo information [{label:"", sequence:0, cableguid: ""}]
        @type powerinputinfo:            array
        
        @param poweroutputinfo:        list of poweroutputinfor information [{label:"", sequence:0, cableguid: ""}]
        @type poweroutputinfo:           array
        
        @param portsinfo:              list port information [{label:"", sequence:0, porttype:""}]
        @type portsinfo:                 array    
        
        @param sensors:                list port information [{label:"", sequence:0, sensortype:""}]
        @type sensors                    array

        @param accounts:            accounts which has access to the meteringdevice [{login:"",password:''}] 
        @type accounts:               array

        @param tags:                   string of tags
        @type tags:                    string
        
        @param meteringdeviceconfigstatus: config status
        @type meteringdeviceconfigstatus: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and meteringdevice guid as result and jobguid: {'result':{'returncode':True, 'meteringdeviceguid':guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """
        
    def delete(self, meteringdeviceguid, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a meteringdevice.
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice to delete.
        @type meteringdeviceguid:      guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode  as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def updateModelProperties(self, meteringdeviceguid, name=None, id=None, meteringdevicetype=None, template=False, rackguid=None, parentmeteringdeviceguid=None, clouduserguid=None, networkinfo=None, \
                              height=1, positionx=0, positiony=0, positionz=0, attributes=None, accounts = [], tags=None, meteringdeviceconfigstatus=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)
     
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice specified
        @type meteringdeviceguid:      guid

        @param name:                   Name for the meteringdevice.
        @type name:                    string
        
        @param id:                     Id for the meteringdevice.
        @type id:                      string

        @param meteringdevicetype:     Type of the meteringdevice. Can be one of the following values PM0816-ZB, PM0816, PM0816-ZB-S10, PM0816-S10
        @type meteringdevicetype:      string
        
        @param template:                is template, when template used as example meteringdevice
        @type template:                 bool

        @param rackguid:               Guid of the rack in which the meteringdevice is located.
        @type rackguid:                guid

        @param parentmeteringdeviceguid:   Guid of the master controller in case of a slave meteringdevice.
        @type parentmeteringdeviceguid:    guid

        @param clouduserguid:          Guid of the cloud user who owns this meteringdevice
        @type clouduserguid:           guid

        @param networkinfo:            network information {ipaddress:"", port:"", protocol:""}
        @param networkinfo:            dictionary

        @param height:                 Height of the meteringdevice in U.
        @type height:                  integer

        @param positionx:              X position of the meteringdevice in rack.
        @type positionx:               integer

        @param positiony:              Y position of the meteringdevice in rack.
        @type positiony:               integer

        @param positionz:              Z position of the meteringdevice in rack. 0 means at the front side of the rack, 1 at the back side.
        @type positionz:               integer
        
        @param attributes:             dictionary of specific attributes for this metering device
        @type attributes:              dictionary
        
        @param accounts:            accounts which has access to the meteringdevice [{login:"",password:''}] 
        @type accounts:               array
        
        @param tags:                   string of tags
        @type tags:                    string

        @param meteringdeviceconfigstatus: config status
        @type meteringdeviceconfigstatus: string


        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and meteringdevice guid as result and jobguid: {result:{'returncode':True, 'meteringdeviceguid':guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name=None, id=None, meteringdevicetype=None, template=None, rackguid=None, parentmeteringdeviceguid=None, clouduserguid=None, \
             height=None, positionx=None, positiony=None, positionz=None, ipaddress=None,  cableguid=None, tags=None, \
             meteringdeviceconfigstatus=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of meteringdevice guids which are matching the find criteria.
        
        @security administrators
        
        @param name:                   Name for the meteringdevice.
        @type name:                    string
        
        @param id:                     Id of the meteringdevice
        @type id:                      string

        @param meteringdevicetype:     Type of the meteringdevice. Can be one of the following values PM0816-ZB, PM0816, PM0816-ZB-S10, PM0816-S10
        @type meteringdevicetype:      string
       
        @param template: If True, find all the meteringdevice with template flag on True
        @type template:             boolean
        
        @param rackguid:               Guid of the rack in which the meteringdevice is located.
        @type rackguid:                guid

        @param parentmeteringdeviceguid:   Guid of the master controller in case of a slave meteringdevice.
        @type parentmeteringdeviceguid:    guid

        @param clouduserguid:          Guid of the cloud user who owns this meteringdevice
        @type clouduserguid:           guid

        @param height:                 Height of the meteringdevice in U.
        @type height:                  integer

        @param positionx:              X position of the meteringdevice in rack.
        @type positionx:               integer

        @param positiony:              Y position of the meteringdevice in rack.
        @type positiony:               integer

        @param positionz:              Z position of the meteringdevice in rack. 0 means at the front side of the rack, 1 at the back side.
        @type positionz:               integer

        @param ipaddress:              Ip address of this meteringdevice (i.e. "127.0.0.1")
        @type ipaddress:               string

        @param cableguid:         Guid of the cable to which the device is connected via his powerport
        @type cableguid:            guid
        
        @param tags: string of tags
        @type tags: string
        
        @param meteringdeviceconfigstatus: config status
        @type meteringdeviceconfigstatus: string

        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       returncod and guidlist(Array of meteringdevice guids which met the find criteria specified).
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': {'returncode':True', 'guidlist':["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, meteringdevicetype=None, rackguid=None, parentmeteringdeviceguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all meteringdevice.

        @security administrators
        
        @param meteringdevicetype: type of the meteringdevices to list.
        @type meteringdevicetype: meteringdevicetype
        
        @param rackguid: Location of the meteringdevices to list.
        @type rackguid: guid
        
        @param parentmeteringdeviceguid: parentmeteringdevice of this meteringdevice.
        @type parentmeteringdeviceguid: guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of meteringdevice info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {'returncode':'True', 'meteringdeviceinfo':[{ 'meteringdeviceguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'BXL-RC0001',
        @note:                                      'meteringdevicetype': 'PM0816-ZB-S10',
        @note:                                      'rackguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803',,
        @note:                                      'parentmeteringdeviceguid': '0B564F4E-5823-4893-B300-E66B4E5C0C2A',
        @note:                                      'clouduserguid': 'A8639879-5FEC-4D13-A091-BA111E050B72',
        @note:                                      'height': '1',
        @note:                                      'positionx': '1',
        @note:                                      'positiony': '10',
        @note:                                      'positionz': '0',
        @note:                          }        ]}
        
        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.
        
        @execution_method = sync
       
        @param meteringdeviceguid:  Guid of the meteringdevice rootobject
        @type meteringdeviceguid:   guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        """

    def powerOnPowerPort(self, meteringdeviceguid, label, request=None, jobguid=None, executionparams=dict()):
        """
        Power on a port of a meteringdevice.
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice.
        @type meteringdeviceguid:      guid

        @param label:                  Label of the port to power on.
        @type label:                   string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def powerOffPowerPort(self, meteringdeviceguid, label, request=None, jobguid=None, executionparams=dict()):
        """
        Power off a port of a meteringdevice.
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice.
        @type meteringdeviceguid:      guid

        @param label:                  Label of the port to power off.
        @type label:                   string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def togglePowerPort(self, meteringdeviceguid, label, request=None, jobguid=None, executionparams=dict()):
        """
        Toggle a power port of a meteringdevice.
        (Power off the port if on  and power on a port if on on a meteringdevice)
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice.
        @type meteringdeviceguid:      guid

        @param label:                  Label of the port to toggle.
        @type label:                   string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def setPowerPortStartupDelay(self, meteringdeviceguid, label,delay, request=None, jobguid=None, executionparams=dict()):
        """
        Change the startup delay of a specific port on the metering device
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice.
        @type meteringdeviceguid:      guid

        @param label:                  Label of the port to set delay for
        @type label:                   string

        @param delay:                  Delay in seconds
        @type delay:                   int

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def enableDHCP(self, meteringdeviceguid, request=None, jobguid=None, executionparams=dict()):
        """
        Enable DHCP for a meteringdevice.
      
        @security administrators

        @param meteringdeviceguid:     Guid of the rack meteringdevice.
        @type meteringdeviceguid:      guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def disableDHCP(self, meteringdeviceguid, request=None, jobguid=None, executionparams=dict()):
        """
        Disable DHCP for a meteringdevice.
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice.
        @type meteringdeviceguid:      guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def setFixedIPAddress(self, meteringdeviceguid, ipaddress, subnetmask, defaultgateway, request=None, jobguid=None, executionparams=dict()):
        """
        Set a fixed ipaddress on the meteringdevice and update the meteringdevice model
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice
        @type meteringdeviceguid:      guid

        @param ipaddress:              IP address to use for the meteringdevice
        @type ipaddress:               string

        @param subnetmask:             Subnet mask to use for the meteringdevice.
        @type subnetmask:              string

        @param defaultgateway:         Default gateway to use for the meteringdevice.
        @type defaultgateway:          string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised
        """   
    
    def addInputPowerPort(self, meteringdeviceguid, label, sequence=None, request=None, jobguid=None, executionparams=dict()):
        """
        Add a input powerport to the meteringdevice.
        
        @security administrators
        
        @param meteringdeviceguid: Guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label for the new inputport
        @type label: string
        
        @param sequence: sequence of the port, if empty the sequence is the last portsequence+1
        @type sequence: integer
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
        
        
    def addOutputPowerPort(self, meteringdeviceguid, label, sequence=None, request=None, jobguid=None, executionparams=dict()):
        """
        Add a output powerport to the meteringdevice.
        
        @security administrators
        
        @param meteringdeviceguid: Guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label for the new inputport
        @type label: string
        
        @param sequence: sequence of the port, if empty the sequence is the last portsequence+1
        @type sequence: integer
        
        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
        
    def deleteOutputPowerPort(self, meteringdeviceguid, label, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a output powerport from the meteringdevice.
        
        @security administrators
        
        @param meteringdeviceguid: Guid of the meteringdevice
        @type: meteringdeviceguid: guid
        
        @param label: label of the outputport which should be removed
        @type label: string
        
        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
        
    def deleteInputPowerPort(self, meteringdeviceguid, label, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a input powerport from the meteringdevice.
        
        @security administrators
        
        @param meteringdeviceguid: Guid of the meteringdevice
        @type: meteringdeviceguid: guid
        
        @param label: label of the outputport which should be removed
        @type label: string
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
    
    def addPort(self, meteringdeviceguid, label, porttype, sequence=0, request=None, jobguid=None, executionparams=dict()):
        """
        Add a port to the meteringdevice
        
        @security administrators
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label of the port 
        @type label: string
        
        @param porttype: type of the port(SERIAL, ZIGBEE)
        @type porttype: string
        
        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
        
    def deletePort(self, meteringdeviceguid, label, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a port from the meteringdevice
        
        @security administrators
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label of the port
        @type label: string
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
        
        
    def addSensor(self, meteringdeviceguid, label, sensortype, sequence=0, request=None, jobguid=None, executionparams=dict()):
        """
        Add a sensor to the meteringdevice
        
        @security administrators
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label of the sensor
        @type label: string
        
        @param porttype: type of the sensor(AIRFLOWSENSOR, HUMIDITYSENSOR, TEMPERATURESENSOR )
        @type porttype: string
        
        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
                
    
    def deleteSensor(self, meteringdeviceguid, label, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a sensor from the meteringdevice
        
        @security administrators
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label of the sensor
        @type label: string
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
           
    def connectPowerInputPort(self, meteringdeviceguid, portlabel, cableguid, request=None, jobguid=None, executionparams=dict()):
        """
        Connect a cable to the powerinput of the meteringdevice 
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label of the power input port
        @type label: string
        
        @param cableguid: cabel which will be connected to the power Onput Port
        @type cableguid: guid
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
        
    def connectPowerOutputPort(self, meteringdeviceguid, portlabel, cableguid, request=None, jobguid=None, executionparams=dict()):
        """
        Connect a cable to the poweroutput of the meteringdevice 
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param label: label of the power output port
        @type label: string
        
        @param cableguid: cabel which will be connected to the power Output Port
        @type cableguid: guid
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """  
        
    def disconnectPowerInputPort(self, meteringdeviceguid, portlabel=None, cableguid=None,  request=None, jobguid=None, executionparams=dict()):
        """
        Disconnect a cable from a power input port of the meteringdevice
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param portlabel: label of the power input port
        @type portlabel: string
        
        @param cableguid: disconnect port connected to this cable if no portlabel is provided
        @type cableguid: guid
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """
        
    def disconnectPowerOutputPort(self, meteringdeviceguid, portlabel=None, cableguid=None,  request=None, jobguid=None, executionparams=dict()):
        """
        Disconnect a cable from a power output port of the meteringdevice
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param portlabell: label of the power output port
        @type portlabel: string
        
        @param cableguid: disconnect port connected to this cable if no portlabel is provided
        @type cableguid: guid
        
        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary
        """   
        
    def updatePowerInputPort(self, meteringdeviceguid, portlabel, newportlabel=None, sequence=None, attributes=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update a powerinput port identified by portlabel, set portlabel, honsequence, and optional attributes in the model and the meteringdevice
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param portlabel: label of the power input port
        @type portlabel: string
        
        @param newportlabel: new label for the port
        @param newportlabel: string
        
        @param sequence: sequence of the power input port
        @type sequence: integer
        
        @param attributes: dictionary of values to set on the power input port
        @type attributes: dictionary
        
        @return:    dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:    dictionary
        """
        
    def updatePowerOutputPort(self, meteringdeviceguid, portlabel, newportlabel=None, sequence=None, attributes=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update a poweroutput port , set portlabel, sequence, threshold and optional attributes in the model and the meteringdevice
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param portlabel: label of the power output port which will be updated
        @type portlabel: string
        
        @param newportlabel: new label for the port
        @param newportlabel: string
        
        @param sequence: sequence of the power output port
        @type sequence: integer
        
        @param attributes: dictionary of values to set on the power output port
        @type attributes: dictionary
        
        @return:    dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:    dictionary
        """
        
    def updateSensor(self, meteringdeviceguid, sensorlabel, newsensorlabel=None,  sequence=None, sensortype=None, attributes=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update sensor settings in the model and on the meteringdevice
            
            @param meteringdeviceguid: guid of the meteringdevice
            @type meteringdeviceguid: guid
            
            @param sensorlabel: identification of the sensor on the meteringdevice
            @type sensorlabel: string 
            
            @param newsensorlabel: new label for the sensor
            @param newsensorlabe: string
            
            @param sequence: sequence of the power output port
            @type sequence: integer
        
           @param attributes: dictionary of values to set on the power output port
           @type attributes: dictionary
        
            @return:    dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
            @rtype:    dictionary
        """
        


    def setAccount(self, meteringdeviceguid, login, password, usertype, request=None, jobguid=None, executionparams=dict()):
        """
        Configure account information on the meteringdevice.
      
        @security administrators

        @param meteringdeviceguid:     Guid of the meteringdevice.
        @type meteringdeviceguid:      guid

        @param login:     New login
        @type login:      str
        
        @param password:     New Password
        @type password:      str
        
        @param usertype:     valid types are ("admin", "user", "restricted")
        @type usertype:      str
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
        
    def getPowerPortStatus(self, meteringdeviceguid, portlabel, request=None, jobguid=None, executionparams=dict()):
        """
        Get the current status of a powerport
        
        @param meteringdeviceguid:     Guid of the meteringdevice.
        @type meteringdeviceguid:      guid
        
        @param portlabel: label of the power port from which you get the status.
        @type portlabel: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and status(e.g True if on, False if off) as result and jobguid: {'result': {'returncode':True,  'status':}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
    
    def getCurrentPowerPortData(self, meteringdeviceguid, portlabel, meteringtype, request=None, jobguid=None, executionparams=dict()):
        """
        Get the current value of a certain meteringtype on a powerport, this can be power, voltage ...
        
        @param meteringdeviceguid: Guid of the meteringdevice.
        @type meteringdeviceguid: guid
        
        @param portlabel: label of the power port
        @type portlabel: string
        
        @param meteringtype: Type of metering information requested(e.g current, voltage)
        @type meteringtype: string
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and values as result and jobguid, and the value of the requested sensor information: {'result': {'returncode':'True','value':} 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised       
        """
     
    def getCurrentDeviceData(self, meteringdeviceguid, meteringtype, request=None, jobguid=None, executionparams=dict()):
        """
        Get the current value of a certain meteringtype on a powerport, this can be power, voltage ...
        If the meteringtype is 'all', all currentdata(also from ports and sensors is returned in a dict() format).
        The  result format will be:
        
           {Voltage:, MaxTotalCurrent:, MaxVoltage:, MinVoltage:, Frequency:,
              Ports:[{sequence:, ActiveEnergy:,ApparentEnergy: Power:, CurrentPortState:, Current:, MaxCurrent:, MaxPower},...],
              Sensors: [{sequence:, type:,sensorvalue:, maxvalue:, minvalue:}]
           }
         
        
        @param meteringdeviceguid: Guid of the meteringdevice.
        @type meteringdeviceguid: guid
        
        @param meteringtype: Type of metering information requested(e.g current, voltage.
        @type meteringtype: string
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode, True and requested values as result and jobguid, {'result':{returncode:True,'values':} ,'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised       
        """

    def getCurrentSensorData(self, meteringdeviceguid, sensorlabel, meteringtype, request=None, jobguid=None, executionparams=dict()):       
        """
        Get the current value of a certain meteringtype on a sensor, this can be temperature, humidity.
        
        @param meteringdeviceguid: Guid of the meteringdevice.
        @type meteringdeviceguid: guid
        
        @param sensorlabel: label of the sensor
        @type sensorlabel: string
        
        @param meteringtype: Type of metering information requested(e.g temperature, humidity)
        @type meteringtype: string
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode, True and requested values as result and jobguid, {'result':{returncode:True,'values':} ,'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised       
        """
    
    def getCo2UsageData(self, meteringdeviceguid, request=None, jobguid=None, executionparams=dict()):
        """
        Get the current co2 usage of a meteringdevice and ports on a meteringdevice.
        The  result format will be:
        
           {meteringdevice:co2usage
              Ports:{sequence:co2usage,...}
           }
         
        
        @param meteringdeviceguid: Guid of the meteringdevice.
        @type meteringdeviceguid: guid
       
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode, True and requested values as result and jobguid, {'result':{returncode:True,'values':} ,'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised       
        """

    def setThresholdOnPowerPort(self, meteringdeviceguid, powerportlabel, thresholdtype, thresholdvalue, request=None, jobguid=None, executionparams=dict()):
        """
        Set threshold on a powerport
        
        @param meteringdeviceguid: Guid of the meteringdevice.
        @type meteringdeviceguid: guid
        
        @param powerportlabel: label of the powerport
        @type powerportlabel: string
        
        @param thresholdtype: Type of the threshold you want to set its value
        @type thresholdtype: String
       
        @param thresholdvalue: Threshold value to set on the device
        @type thresholdvalue: String
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised       
        """
        
    def setThreshold(self, meteringdeviceguid, thresholdtype, thresholdvalue, request=None, jobguid=None, executionparams=dict()):
        """
        Set threshold on a device
        
        @param meteringdeviceguid: Guid of the meteringdevice.
        @type meteringdeviceguid: guid
        
        @param thresholdtype: Type of the threshold you want to set its value
        @type thresholdtype: String
       
        @param thresholdvalue: Threshold value to set on the device
        @type thresholdvalue: String
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised       
        """
        
    def getThresholdOnPowerPort(self, meteringdeviceguid, powerportlabel, thresholdtype, request=None, jobguid=None, executionparams=dict()):
        """
        Get threshold on power port
        
        @param meteringdeviceguid: Guid of the meteringdevice.
        @type meteringdeviceguid: guid
        
        @param powerportlabel: label of the powerport
        @type powerportlabel: string
        
        @param thresholdtype: Type of the threshold you want to get its value
        @type thresholdtype: String
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                     In case an error occurred, exception is raised       
        """

    def getViewData(self, rootobjectguid, portlabel = '', request=None, jobguid=None, executionparams=dict()):
        """
        Returns view data as a list for this rootobject.

        @param portlabel:     Metering device port label
        @type portlabel:      str

        @param sensorlabel:     Metering device Sensor label
        @type sensorlabel:      str

        @return: [{viewdatatype:, viewdatavalue:, viewdataunit:},]
        """
        
    def getTree(meteringdeviceguid, depth=2, jobguid=None, executionparams=dict()):
        """
        Returns a json dict with a tree structure.
        
        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param depth: depth to return, default 2. 0 means unlimited depth
        @type depth: integer
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid
        
        @return:                  dictionary with returncode(True) as result and 'result': {'name','type',children = []}
        @rtype:                   dictionary                
        """

    def getJSON(self, meteringdeviceguid, request=None, jobguid=None,executionparams=dict()):
        """
        Returns a JSON dict of the energyswitch.
        This is the format:
            {name: , id:, meteringdevicetype:, parentmeteringdeviceguid:, rackguid:, clouduserguid:, positionx:, positiony:, positionz:, powerintputs:[{label:, sequence: cableguid:, attributes:{}}], poweroutputs:[{label:, sequence:,cableguid: attributes{}}], sensors:[{label:, sequence:, sensortype:, attributes:{}}], ipaddress:, attributes:{}, ports:[{label:, sequence:, porttype:, attributes:{}}, accounts:{login:, password:}], tags:, meteringdeviceconfigstatus:}

        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return: returns a json representation of a energyswitch
        @rtype:                   dictionary
        """


    def updateACL(self, rootobjectguid, cloudusergroupnames={}, request=None, jobguid=None, executionparams=dict()):
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

    def addGroup(self, rootobjectguid, group, action=None, recursive=False, request=None, jobguid=None, executionparams=dict()):
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


    def deleteGroup(self, rootobjectguid, group, action=None, recursive=False, request=None, jobguid=None, executionparams=dict()):
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

    def getPduHealthStatus(self, guid, timing = [3600, 86400], jobguid=None, executionparams=dict()):
        """
        getPduHealtStatus, returns a list of 3 values, the first list contains the amount of pdus  which monitoring data is more recent then currenttime-timing[0], the second the  # of pdus  which are last monitored between currenttime - timing[0] and currenttime - timing[1] and the last list contains the amount of pdus which are monitored later then currenttime - timing[1]
        
        E.g:  [200, 5, 2]
        
        Timing contains the time intervals in seconds.(defaults are set on one hour and 1 day)
        
        @params guid: meteringdevice guid 
        @type timing: guid
        
        @params timing: timing intervals
        @type timing: list
        
        @return: a dictionary containing this information {'result': {returncode:'True', healthstatus:[],} jobguid:guid}
        @type: dict
        """
