from cloud_api_client.Exceptions import CloudApiException

class device:
    def __init__(self, proxy):
        self._proxy = proxy


    def getXMLSchema (self, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the device rootobject structure.

        @execution_method = sync
        
        @param deviceguid:           Guid of the device rootobject
        @type deviceguid:            guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     XSD representation of the device structure.
        @rtype:                      string

        @raise e:                    In case an error occurred, exception is raised

        @todo:                       Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_device.getXMLSchema(deviceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addPDisk (self, deviceguid, status, diskinterfacetype, deviceid = "", size = "", rpm = "", jobguid = "", executionparams = {}):
        """
        
        Add pdisk to pdisks array of device
        
        @execution_method = sync
        
        @param deviceguid:          Guid of the device rootobject
        @type deviceguid:           guid
        
        @param status:              status of disk
        @type status:               devicediskstatustype
        
        @param diskinterfacetype:   interface type of pdisk
        @type diskinterfacetype:    diskinterfacetype
        
        @param deviceid:            id of the pdisk
        @type deviceid:             string
        
        @param size:                size of pdisk
        @type size:                 integer
        
        @param rpm:                 rpm of pdisk
        @type rpm:                  integer
      
        @return:                    dictionary with device guid as result and jobguid: {'result': deviceguid, 'jobguid': guid}
        @rtype:                     dictionary
        
        @raise e:                   In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.addPDisk(deviceguid,status,diskinterfacetype,deviceid,size,rpm,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, name, devicetype, description = "", template = False, rackguid = "", datacenterguid = "", racku = 1, racky = 0, rackz = 0, modelnr = "", serialnr = "", firmware = "", lastcheck = "", status = "", parentdeviceguid = "", components = [], pdisks = [], nicports = [], powerports = [], lastrealitycheck = "", capacityunitsconsumed = [], capacityunitsprovided = [], accounts = "", cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Create a new device.

        @execution_method = sync
        
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

        @param  capacityunitsconsumed: list of capacity units, consumed
        @type capacityunitsconsumed:   array(core.capacityplanning/capacityunit)

        @param capacityunitsprovided:  list of capacity units, provided
        @type capacityunitsprovided:   array(core.capacityplanning/capacityunit)

        @param  accounts:              list of accounts available in this device (e.g. bios accounts)
        @type  accounts:               array(account)

        @param cloudspaceguid:         guid of the space to which this machine belongs
        @type cloudspaceguid:          guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with deviceguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.create(name,devicetype,description,template,rackguid,datacenterguid,racku,racky,rackz,modelnr,serialnr,firmware,lastcheck,status,parentdeviceguid,components,pdisks,nicports,powerports,lastrealitycheck,capacityunitsconsumed,capacityunitsprovided,accounts,cloudspaceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, deviceguid = "", jobguid = "", executionparams = {}):
        """
        
        List all devices.

        @execution_method = sync
        
        @param deviceguid:              Guid of the device specified
        @type deviceguid:               guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of device info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.list(deviceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the device rootobject.

        @execution_method = sync
        
        @param deviceguid:            Guid of the device rootobject
        @type deviceguid:             guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the device
        @rtype:                       string
        
        """
        try:
            result = self._proxy.cloud_api_device.getYAML(deviceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listPowerPorts (self, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Lists information about power ports of the device  
        
        @execution_method = sync
        
        @param deviceguid:          Guid of the device rootobject
        @type deviceguid:           guid
        
        @return:                    dictionary with device guid as result
        @rtype:                     dictionary
        
        @raise e:                   In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.listPowerPorts(deviceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:        Guid of the device rootobject
        @type rootobjectguid:         guid

        @return:                      rootobject
        @rtype:                       string

        @warning:                     Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_device.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['device'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, deviceguid, name = "", devicetype = "", description = "", template = False, rackguid = "", datacenterguid = "", racku = 1, racky = 0, rackz = 0, modelnr = "", serialnr = "", firmware = "", lastcheck = "", status = "", parentdeviceguid = "", components = [], pdisks = [], nicports = [], powerports = [], lastrealitycheck = "", capacityunitsconsumed = [], capacityunitsprovided = [], accounts = "", cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
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

        @param  capacityunitsconsumed:  list of capacity units, consumed
        @type capacityunitsconsumed:    array(core.capacityplanning/capacityunit)

        @param capacityunitsprovided:   list of capacity units, provided
        @type capacityunitsprovided:    array(core.capacityplanning/capacityunit)

        @param  accounts:               list of accounts available in this device (e.g. bios accounts)
        @type  accounts:                array(account)

        @param cloudspaceguid:          guid of the space to which this machine belongs
        @type cloudspaceguid:           guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with device guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.updateModelProperties(deviceguid,name,devicetype,description,template,rackguid,datacenterguid,racku,racky,rackz,modelnr,serialnr,firmware,lastcheck,status,parentdeviceguid,components,pdisks,nicports,powerports,lastrealitycheck,capacityunitsconsumed,capacityunitsprovided,accounts,cloudspaceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the device rootobject.

        @execution_method = sync
        
        @param deviceguid:           Guid of the device rootobject
        @type deviceguid:            guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     XML representation of the device
        @rtype:                      string

        @raise e:                    In case an error occurred, exception is raised

        @todo:                       Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_device.getXML(deviceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addNic (self, deviceguid, status, nicporttype, name = "", sequence = "", hwaddr = "", backplaneguid = "", cableguid = "", jobguid = "", executionparams = {}):
        """
        
        Add nicport property
        
        @execution_method = sync
        
        @param deviceguid:        Guid of the device rootobject
        @type deviceguid:         guid
        
        @param status:            status of nicport
        @type status:             nicportstatustype
        
        @param nicporttype:       hardware type of nicport
        @type nicporttype:        nicporttype
        
        @param name:              name of the nic port
        @type name:               string
        
        @param sequence:          sequence of nic port
        @type sequence:           integer
        
        @param hwaddr:            hardware address like macaddr
        @type hwaddr:             string
        
        @param backplaneguid:     backplane to which the nicport is connected
        @type backplaneguid:      guid
        
        @param cableguid:         cable to which the nicport is connected
        @type cableguid:          guid
        
        @return:                  dictionary with device guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                   dictionary
        
        @raise e:                 In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.addNic(deviceguid,status,nicporttype,name,sequence,hwaddr,backplaneguid,cableguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, name = "", macaddress = "", status = "", devicetype = "", description = "", template = "", modelnr = "", serialnr = "", firmware = "", rackguid = "", datacenterguid = "", parentdeviceguid = "", cloudspaceguid = "", jobguid = "", executionparams = {}):
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

        @param cloudspaceguid:            Guid of the space to which this machine belongs
        @type cloudspaceguid:             guid

        @param jobguid:                   Guid of the job if avalailable else empty string
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          Array of device guids which met the find criteria specified.
        @rtype:                           array

        @note:                            Example return value:
        @note:                            {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                             'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                         In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.find(name,macaddress,status,devicetype,description,template,modelnr,serialnr,firmware,rackguid,datacenterguid,parentdeviceguid,cloudspaceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Delete a device.

        @execution_method = sync
        
        @security administrators
        
        @param deviceguid:            Guid of the device rootobject to delete.
        @type deviceguid:             guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_device.delete(deviceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



