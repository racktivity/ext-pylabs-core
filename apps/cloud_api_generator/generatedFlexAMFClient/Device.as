
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Device extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_device';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Device()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the device rootobject structure.
        *         @execution_method = sync
        *         
        *         @param deviceguid:           Guid of the device rootobject
        *         @type deviceguid:            guid
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     XSD representation of the device structure.
        *         @rtype:                      string
        *         @raise e:                    In case an error occurred, exception is raised
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function getXMLSchema (deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, deviceguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDPDISK:String = 'addPDisk_response';
        /**
        *         Add pdisk to pdisks array of device
        *         
        *         @execution_method = sync
        *         
        *         @param deviceguid:          Guid of the device rootobject
        *         @type deviceguid:           guid
        *         
        *         @param status:              status of disk
        *         @type status:               devicediskstatustype
        *         
        *         @param diskinterfacetype:   interface type of pdisk
        *         @type diskinterfacetype:    diskinterfacetype
        *         
        *         @param deviceid:            id of the pdisk
        *         @type deviceid:             string
        *         
        *         @param size:                size of pdisk
        *         @type size:                 integer
        *         
        *         @param rpm:                 rpm of pdisk
        *         @type rpm:                  integer
        *       
        *         @return:                    dictionary with device guid as result and jobguid: {'result': deviceguid, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function addPDisk (deviceguid:String,status:Object,diskinterfacetype:Object,deviceid:String="",size:Number=0,rpm:Number=0,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addPDisk', addPDisk_ResultReceived, getError, deviceguid,status,diskinterfacetype,deviceid,size,rpm,jobguid,executionparams);

        }

        private function addPDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDPDISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new device.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @doc  name:                    name of the device
        *         @type name:                    string
        *         @param devicetype:             device type
        *         @type devicetype:              devicetype
        *         @param  description:           remarks on the device
        *         @type description:             type_description
        *         @param template:               is template, when template used as example for an application
        *         @type template:                bool
        *         @param rackguid:               guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
        *         @type rackguid:                guid
        *         @param datacenterguid :        guid of the datacenter to which the device belongs - can be None e.g. for devices in stock or in repair
        *         @type datacenterguid:          guid
        *         @param  racku:                 size of the device, measured in u e.g. 1u high
        *         @type racku:                   int
        *         @param racky:                  physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        *         @type racky:                   int
        *         @param  rackz:                 physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        *         @type rackz:                   int
        *         @param  modelnr:               model number of the device
        *         @type modelnr:                 string(60)
        *         @param  serialnr:              serial number of the device
        *         @type serialnr:                string(60)
        *         @param firmware:               firmware identifier of the device
        *         @type firmware:                string(60)
        *         @param lastcheck:              last time device was inspected
        *         @type lastcheck:               type_date
        *         @param  status:                device status
        *         @type status:                  devicestatustype
        *         @param parentdeviceguid:       parent device, e.g. blade belongs to bladechasis
        *         @type parentdeviceguid:        guid
        *         @param components:             list of components which are part of the device , do not use fo disks & nics
        *         @type components:              array(component)
        *         @param  pdisks:                physical disks which are part of device
        *         @type pdisks:                  array(pdisk)
        *         @param  nicports:              nicports which are part of device
        *         @type nicports:                array(nicport)
        *         @param  powerports:            powerports which are part of device
        *         @type powerports:              array(powerport)
        *         @param  lastrealitycheck:      date and time of last check on the device with reality
        *         @type lastrealitycheck:        type_date
        *         @param  capacityunitsconsumed: list of capacity units, consumed
        *         @type capacityunitsconsumed:   array(core.capacityplanning/capacityunit)
        *         @param capacityunitsprovided:  list of capacity units, provided
        *         @type capacityunitsprovided:   array(core.capacityplanning/capacityunit)
        *         @param  accounts:              list of accounts available in this device (e.g. bios accounts)
        *         @type  accounts:               array(account)
        *         @param cloudspaceguid:         guid of the space to which this machine belongs
        *         @type cloudspaceguid:          guid
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with deviceguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,devicetype:Object,description:Object=null,template:Object=null,rackguid:String="",datacenterguid:String="",racku:Number=1,racky:Number=0,rackz:Number=0,modelnr:Object=null,serialnr:Object=null,firmware:Object=null,lastcheck:Object=null,status:Object=null,parentdeviceguid:String="",components:Object=null,pdisks:Object=null,nicports:Object=null,powerports:Object=null,lastrealitycheck:Object=null,capacityunitsconsumed:Object=null,capacityunitsprovided:Object=null,accounts:Object=null,cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,devicetype,description,template,rackguid,datacenterguid,racku,racky,rackz,modelnr,serialnr,firmware,lastcheck,status,parentdeviceguid,components,pdisks,nicports,powerports,lastrealitycheck,capacityunitsconsumed,capacityunitsprovided,accounts,cloudspaceguid,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all devices.
        *         @execution_method = sync
        *         
        *         @param deviceguid:              Guid of the device specified
        *         @type deviceguid:               guid
        *         @security administrators
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of device info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function list (deviceguid:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, deviceguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the device rootobject.
        *         @execution_method = sync
        *         
        *         @param deviceguid:            Guid of the device rootobject
        *         @type deviceguid:             guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the device
        *         @rtype:                       string
        *         
        */
        public function getYAML (deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, deviceguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTPOWERPORTS:String = 'listPowerPorts_response';
        /**
        *         Lists information about power ports of the device  
        *         
        *         @execution_method = sync
        *         
        *         @param deviceguid:          Guid of the device rootobject
        *         @type deviceguid:           guid
        *         
        *         @return:                    dictionary with device guid as result
        *         @rtype:                     dictionary
        *         
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listPowerPorts (deviceguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listPowerPorts', listPowerPorts_ResultReceived, getError, deviceguid,jobguid,executionparams);

        }

        private function listPowerPorts_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTPOWERPORTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:        Guid of the device rootobject
        *         @type rootobjectguid:         guid
        *         @return:                      rootobject
        *         @rtype:                       string
        *         @warning:                     Only usable using the python client.
        *         
        */
        public function getObject (rootobjectguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getObject', getObject_ResultReceived, getError, rootobjectguid,jobguid,executionparams);

        }

        private function getObject_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETOBJECT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @execution_method = sync
        *         
        *         @security administrators
        *         
        *         @param deviceguid:              Guid of the device specified
        *         @type deviceguid:               guid
        *         @doc  name:                     name of the device
        *         @type name:                     string
        *         @param devicetype:              device type
        *         @type devicetype:               devicetype
        *         @param  description:            remarks on the device
        *         @type description:              type_description
        *         @param template:                is template, when template used as example for an application
        *         @type template:                 bool
        *         @param rackguid:                guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
        *         @type rackguid:                 guid
        *         @param datacenterguid :         guid of the datacenter to which the device belongs - can be None e.g. for devices in stock or in repair
        *         @type datacenterguid:           guid
        *         @param  racku:                  size of the device, measured in u e.g. 1u high
        *         @type racku:                    int
        *         @param racky:                   physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        *         @type racky:                    int
        *         @param  rackz:                  physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        *         @type rackz:                    int
        *         @param  modelnr:                model number of the device
        *         @type modelnr:                  string(60)
        *         @param  serialnr:               serial number of the device
        *         @type serialnr:                 string(60)
        *         @param firmware:                firmware identifier of the device
        *         @type firmware:                 string(60)
        *         @param lastcheck:               last time device was inspected
        *         @type lastcheck:                type_date
        *         @param  status:                 device status
        *         @type status:                   devicestatustype
        *         @param parentdeviceguid:        parent device, e.g. blade belongs to bladechasis
        *         @type parentdeviceguid:         guid
        *         @param components:              list of components which are part of the device , do not use fo disks & nics
        *         @type components:               array(component)
        *         @param  pdisks:                 physical disks which are part of device
        *         @type pdisks:                   array(pdisk)
        *         @param  nicports:               nicports which are part of device
        *         @type nicports:                 array(nicport)
        *         @param  powerports:             powerports which are part of device
        *         @type powerports:               array(powerport)
        *         @param  lastrealitycheck:       date and time of last check on the device with reality
        *         @type lastrealitycheck:         type_date
        *         @param  capacityunitsconsumed:  list of capacity units, consumed
        *         @type capacityunitsconsumed:    array(core.capacityplanning/capacityunit)
        *         @param capacityunitsprovided:   list of capacity units, provided
        *         @type capacityunitsprovided:    array(core.capacityplanning/capacityunit)
        *         @param  accounts:               list of accounts available in this device (e.g. bios accounts)
        *         @type  accounts:                array(account)
        *         @param cloudspaceguid:          guid of the space to which this machine belongs
        *         @type cloudspaceguid:           guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with device guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (deviceguid:String,name:String="",devicetype:Object=null,description:Object=null,template:Object=null,rackguid:String="",datacenterguid:String="",racku:Number=1,racky:Number=0,rackz:Number=0,modelnr:Object=null,serialnr:Object=null,firmware:Object=null,lastcheck:Object=null,status:Object=null,parentdeviceguid:String="",components:Object=null,pdisks:Object=null,nicports:Object=null,powerports:Object=null,lastrealitycheck:Object=null,capacityunitsconsumed:Object=null,capacityunitsprovided:Object=null,accounts:Object=null,cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, deviceguid,name,devicetype,description,template,rackguid,datacenterguid,racku,racky,rackz,modelnr,serialnr,firmware,lastcheck,status,parentdeviceguid,components,pdisks,nicports,powerports,lastrealitycheck,capacityunitsconsumed,capacityunitsprovided,accounts,cloudspaceguid,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the device rootobject.
        *         @execution_method = sync
        *         
        *         @param deviceguid:           Guid of the device rootobject
        *         @type deviceguid:            guid
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     XML representation of the device
        *         @rtype:                      string
        *         @raise e:                    In case an error occurred, exception is raised
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function getXML (deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, deviceguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDNIC:String = 'addNic_response';
        /**
        *         Add nicport property
        *         
        *         @execution_method = sync
        *         
        *         @param deviceguid:        Guid of the device rootobject
        *         @type deviceguid:         guid
        *         
        *         @param status:            status of nicport
        *         @type status:             nicportstatustype
        *         
        *         @param nicporttype:       hardware type of nicport
        *         @type nicporttype:        nicporttype
        *         
        *         @param name:              name of the nic port
        *         @type name:               string
        *         
        *         @param sequence:          sequence of nic port
        *         @type sequence:           integer
        *         
        *         @param hwaddr:            hardware address like macaddr
        *         @type hwaddr:             string
        *         
        *         @param backplaneguid:     backplane to which the nicport is connected
        *         @type backplaneguid:      guid
        *         
        *         @param cableguid:         cable to which the nicport is connected
        *         @type cableguid:          guid
        *         
        *         @return:                  dictionary with device guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function addNic (deviceguid:String,status:Object,nicporttype:Object,name:String="",sequence:Number=0,hwaddr:String="",backplaneguid:String="",cableguid:String="",jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addNic', addNic_ResultReceived, getError, deviceguid,status,nicporttype,name,sequence,hwaddr,backplaneguid,cableguid,jobguid,executionparams);

        }

        private function addNic_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDNIC, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of device guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @doc  name:                       Name of the device
        *         @type name:                       string
        *         @doc  macaddress:                 MAC address of the device
        *         @type name:                       string
        *         @param  status:                   Device status
        *         @type status:                     devicestatustype
        *         @param devicetype:                Device type
        *         @type devicetype:                 string
        *         @param  description:              Remarks on the device
        *         @type description:                string
        *         @param template:                  Is template, when template used as example for an application
        *         @type template:                   bool
        *         @param  modelnr:                  Model number of the device
        *         @type modelnr:                    string
        *         @param  serialnr:                 Serial number of the device
        *         @type serialnr:                   string
        *         @param firmware:                  Firmware identifier of the device
        *         @type firmware:                   string
        *         @param rackguid:                  Guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
        *         @type rackguid:                   guid
        *         @param datacenterguid :           Guid of the datacenter to which the device belongs - can be None e.g. for devices in stock or in repair
        *         @type datacenterguid:             guid
        *         @param parentdeviceguid:          Guid of the parent device, e.g. blade belongs to bladechasis
        *         @type parentdeviceguid:           guid
        *         @param cloudspaceguid:            Guid of the space to which this machine belongs
        *         @type cloudspaceguid:             guid
        *         @param jobguid:                   Guid of the job if avalailable else empty string
        *         @type jobguid:                    guid
        *         @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:            dictionary
        *         @return:                          Array of device guids which met the find criteria specified.
        *         @rtype:                           array
        *         @note:                            Example return value:
        *         @note:                            {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                             'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                         In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,macaddress:Object=null,status:Object=null,devicetype:Object=null,description:Object=null,template:Object=null,modelnr:Object=null,serialnr:Object=null,firmware:Object=null,rackguid:Object=null,datacenterguid:Object=null,parentdeviceguid:Object=null,cloudspaceguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,macaddress,status,devicetype,description,template,modelnr,serialnr,firmware,rackguid,datacenterguid,parentdeviceguid,cloudspaceguid,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a device.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         
        *         @param deviceguid:            Guid of the device rootobject to delete.
        *         @type deviceguid:             guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function deleteDevice (deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteDevice', delete_ResultReceived, getError, deviceguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

