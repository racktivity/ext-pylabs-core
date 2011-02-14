
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Sso extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_sso';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Sso()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTSMARTCLIENTDEVICES:String = 'listSmartClientDevices_response';
        /**
        *         Lists all available smart client devices for a Smart Style Office environment
        *         @execution_method = sync
        *         @param  isfree              Boolean value indicating if only non-occupied smart client devices should be returned
        *         @type isfree                boolean
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary of array of dictionaries with guid, name, description, modelnr, serialnr,  status, isfree.
        *         @rtype:                     dictionary
        *         @note:                      Example return value:
        *         @note:                      {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "sc_reception", "description": "Smart client at reception desk", "modelnr": "model1234", "serialnr":"12345-6789", "status": "ACTIVE", "isfree": False},
        *         @note:                                  {"guid": "D48CCFB4-207D-469F-8DA8-471304C3CCA7", "name": "sc_meeting_room", "description": "Smart client at meeting room 1", "modelnr": "model1234", "serialnr":"67890-1234", "status": "ACTIVE", "isfree": True}],
        *         @note:                       'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listSmartClientDevices (isfree:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listSmartClientDevices', listSmartClientDevices_ResultReceived, getError, isfree,jobguid,executionparams);

        }

        private function listSmartClientDevices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSMARTCLIENTDEVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CHANGEPASSWORDONPMACHINES:String = 'changePasswordOnPMachines_response';
        /**
        *         Changes the password on each pmachine using new pass word
        *         
        *         @security admin
        *         
        *         @param machineguid:           guid of the physical machine
        *         @type machineguid:            guid
        *         
        *         @param username               username
        *         @type username                string
        *         
        *         @param newpassword            new password of the user
        *         @type newpassword             string
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function changePasswordOnPMachines (username:Object,newpassword:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'changePasswordOnPMachines', changePasswordOnPMachines_ResultReceived, getError, username,newpassword,jobguid,executionparams);

        }

        private function changePasswordOnPMachines_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CHANGEPASSWORDONPMACHINES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSYSTEMNASMACHINETEMPLATES:String = 'listSystemNASMachineTemplates_response';
        /**
        *         Lists machine templates available on the SystemNAS
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with available templates and their paths
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function listSystemNASMachineTemplates (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listSystemNASMachineTemplates', listSystemNASMachineTemplates_ResultReceived, getError, jobguid,executionparams);

        }

        private function listSystemNASMachineTemplates_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSYSTEMNASMACHINETEMPLATES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SYNCMODEL:String = 'syncModel_response';
        /**
        *         Cleans snapshots on the volume driver which did not make it in the model
        *         Cleans snapshots in the model that has no snapshots at the backend
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         
        *         @param interval:            Interval of when model must be synced (depends which items are synced)
        *         @param interval:            float
        *         
        *         @return:                    Dictionary with jobguid as result of pending model update and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function syncModel (interval:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'syncModel', syncModel_ResultReceived, getError, interval,jobguid,executionparams);

        }

        private function syncModel_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SYNCMODEL, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EDITMACHINE:String = 'editMachine_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         
        *         @param machineguid:                guid of the machine specified
        *         @type machineguid:                 guid
        *         
        *         @param name:                       Name of the machine.
        *         @type name:                        string
        *         
        *         @param description:                Description for this machine
        *         @type description:                 string
        *         
        *         @param cloudspaceguid:             guid of the space to which this machine belongs
        *         @type cloudspaceguid:              guid
        *         
        *         @param machinetype:                Machine type.
        *         @type machinetype:                 string
        *         
        *         @param osguid:                     guid of the OS.
        *         @type osguid:                      guid
        *         
        *         @param assetid:                    Asset ID.
        *         @type assetid:                     string
        *         
        *         @param alias:                      Alias of the machine.
        *         @type alias:                       string
        *         
        *         @param hostname:                   Hostname of the machine.
        *         @type hostname:                    string
        *         
        *         @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        *         @type nrcpu:                       int
        *         
        *         @param cpufrequency:               CPU frequency in MHz.
        *         @type cpufrequency:                int
        *         
        *         @param memory:                     Memory for the machine in MB. Same as template if not provided.
        *         @type memory:                      int
        *         
        *         @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        *         @type memoryminimal:               int
        *         
        *         @param importancefactor:           Importance of the virtual machine
        *         @type importancefactor:            int
        *         
        *         @param deviceguid:                 guid of the parent device
        *         @type deviceguid:                  guid
        *         @param boot:                       flag indicating that this machine must be automatically started when rebooting the parent machine
        *         @type boot:                        bool
        *         @param backup:                     Backup flag
        *         @type backup:                      bool
        *         @param clouduserguid:              guid of the clouduser, owning this machine
        *         @type clouduserguid:               guid
        *         @param ownerguid:                  guid of the owner.
        *         @type ownerguid:                   guid
        *         
        *         @param iconname:                   Icon for the machine.
        *         @type iconname:                    string
        *         @param bootstatus:                 Machine boot status (INSTALL|FROMDISK|RECOVERY)
        *         @type bootstatus:                  string
        *         @param retentionpolicyguids:       Retention policy for the disks of the machine {'diskguid': 'policyguid'}
        *         @type retentionpolicyguids:        dictionary
        *         
        *         @param customerapplications:       Customer applications to be running on machine
        *         @type customerapplications:        list
        *          
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function editMachine (machineguid:String,name:String="",description:String="",cloudspaceguid:String="",machinetype:String="",osguid:String="",assetid:String="",alias:String="",hostname:String="",nrcpu:Number=0,cpufrequency:Number=0,memory:Number=0,memoryminimal:Number=0,importancefactor:Number=0,deviceguid:String="",boot:Object=null,backup:Object=null,clouduserguid:String="",ownerguid:String="",iconname:String="",bootstatus:String="",retentionpolicyguids:Object=null,customerapplications:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'editMachine', editMachine_ResultReceived, getError, machineguid,name,description,cloudspaceguid,machinetype,osguid,assetid,alias,hostname,nrcpu,cpufrequency,memory,memoryminimal,importancefactor,deviceguid,boot,backup,clouduserguid,ownerguid,iconname,bootstatus,retentionpolicyguids,customerapplications,jobguid,executionparams);

        }

        private function editMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EDITMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDPOWERSWITCHDEVICE:String = 'addPowerSwitchDevice_response';
        /**
        *         Adds a new powerswitch device to a Smart Style Office environment
        *         @param  name                name of the device
        *         @type name                  string
        *         @param macaddress           MAC address of the new resource node
        *         @type macaddress            string
        *         @param description          remarks on the device
        *         @type description           type_description
        *         @param racku                size of the device, measured in u e.g. 1u high
        *         @type racku                 int
        *         @param racky                physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        *         @type racky                 int
        *         @param rackz                physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        *         @type rackz                 int
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function addPowerSwitchDevice (name:Object,macaddress:Object,cloudspaceguid:Object,description:Object=null,racku:Object=null,racky:Object=null,rackz:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addPowerSwitchDevice', addPowerSwitchDevice_ResultReceived, getError, name,macaddress,cloudspaceguid,description,racku,racky,rackz,jobguid,executionparams);

        }

        private function addPowerSwitchDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDPOWERSWITCHDEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAVAILABLETEMPDISKSIZES:String = 'getAvailableTempDiskSizes_response';
        /**
        *         Lists available disk sizes for creation of temp disks 
        *         @param diskroletype:        SSDTEMP or TEMP
        *         @type  diskroletype:        string
        *         
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getAvailableTempDiskSizes (diskroletype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAvailableTempDiskSizes', getAvailableTempDiskSizes_ResultReceived, getError, diskroletype,jobguid,executionparams);

        }

        private function getAvailableTempDiskSizes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAVAILABLETEMPDISKSIZES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATESNAPSHOTS:String = 'createSnapshots_response';
        /**
        *         Creates snapshots off all disks
        *         @param snapshottype:        If PAUSED, the machine will be paused before snapshot is taken.
        *         @type snapshottype:         string
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function createSnapshots (snapshottype:String="REGULAR",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'createSnapshots', createSnapshots_ResultReceived, getError, snapshottype,jobguid,executionparams);

        }

        private function createSnapshots_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATESNAPSHOTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SNAPSHOTMACHINE:String = 'snapshotMachine_response';
        /**
        *         Snapshots a machine and updating the model asynchronnically
        *         
        *         @param machineguid:         Guid of the snapshot machine 
        *         @type machineguid:          guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        *         @return:                    Dictionary  {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function snapshotMachine (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'snapshotMachine', snapshotMachine_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function snapshotMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SNAPSHOTMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETKIOSKMODESMARTCLIENTINFO:String = 'getKioskModeSmartClientInfo_response';
        /**
        *         Gets the information of a smartclient in kiosk mode
        *         @execution_method = sync
        *         @param machineguid          guid of machine
        *         @type machineguid:          guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    information { description , iqn , ip }
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getKioskModeSmartClientInfo (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getKioskModeSmartClientInfo', getKioskModeSmartClientInfo_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getKioskModeSmartClientInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETKIOSKMODESMARTCLIENTINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTVIRTUALDESKTOPS:String = 'listVirtualDesktops_response';
        /**
        *         Lists all vistual desktop for a certain cloud space
        *         Execute method in WFE to get list of current authenticated user
        *         @execution_method = async
        *         @execution_param_wait = True
        *         @param cloudspaceguid       guid of an existing cloudspaceguid to whom the virtual desktops belong
        *         @type cloudspaceguid        guid
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary with jobguid and result 
        *         @rtype:                     dictionary
        *         
        *         @note                         {'jobguid': '386e7985-4871-4c59-a90c-4a43a2698188',
        *         @note                          'result': [{'address': '10.100.143.3',
        *         @note                                      'backup': None,
        *         @note                                      'description': 'Virtual Desktop John',
        *         @note                                      'guid': 'b56c2c6d-d143-4d69-9f15-10679ba2117c',
        *         @note                                      'hostname': 'vdjohn',
        *         @note                                      'hypervisor': 'VIRTUALBOX30',
        *         @note                                      'memory': 1024,
        *         @note                                      'name': 'vdjohn',
        *         @note                                      'nrcpu': 2,
        *         @note                                      'osname': 'windows7',
        *         @note                                      'parentmachinename': 'A3NODE3',
        *         @note                                      'portnr': 23000}]}
        *         
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listVirtualDesktops (cloudspaceguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listVirtualDesktops', listVirtualDesktops_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function listVirtualDesktops_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTVIRTUALDESKTOPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SCRUBVOLUMES:String = 'scrubVolumes_response';
        /**
        *         Scrubs volumes on a timely basis (used in a policy)
        *                                           
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function scrubVolumes (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'scrubVolumes', scrubVolumes_ResultReceived, getError, jobguid,executionparams);

        }

        private function scrubVolumes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SCRUBVOLUMES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAVAILABLEFOCNODE:String = 'getAvailableFOCNode_response';
        /**
        *  
        *         List available node for defining new FailOver Cache on  
        *         
        *         @param machineguid:           guid of the machine to list the FOC volumes
        *         @type  machineguid:           guid
        *         
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with node name , management ip , port of node where FOC can be initialized
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function getAvailableFOCNode (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAvailableFOCNode', getAvailableFOCNode_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getAvailableFOCNode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAVAILABLEFOCNODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETPHYSICALDISKSCOUNT:String = 'getPhysicalDisksCount_response';
        /**
        *         Gets the number of physical disks on given pmachine 
        *         @param machineguid:       guid of the pmachine 
        *         @type machineguid:        guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function getPhysicalDisksCount (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getPhysicalDisksCount', getPhysicalDisksCount_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getPhysicalDisksCount_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETPHYSICALDISKSCOUNT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SHUTDOWN:String = 'shutdown_response';
        /**
        *         shutdown the sso environment
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function shutdown (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'shutdown', shutdown_ResultReceived, getError, jobguid,executionparams);

        }

        private function shutdown_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SHUTDOWN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SENDMESSAGETONOC:String = 'sendMessageToNoc_response';
        /**
        *         Sends a message to the NOC for a certain domain
        *         
        *         @param customerguid       Guid of the customer unregistering the domain
        *         @type customerguid        guid
        *         
        *         @param username           ITPS portal username
        *         @type username            string
        *         
        *         @param password           ITPS portal password
        *         @type password            string
        *         
        *         @param domain             Domain to unregister
        *         @type domain              string
        *         
        *         @param message            message to be sent
        *         @type message             string
        *         
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function sendMessageToNoc (customerguid:Object,username:Object,password:Object,domain:Object,message:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'sendMessageToNoc', sendMessageToNoc_ResultReceived, getError, customerguid,username,password,domain,message,jobguid,executionparams);

        }

        private function sendMessageToNoc_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SENDMESSAGETONOC, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTAVAILABLECPUNODES:String = 'listAvailableCPUNodes_response';
        /**
        *         Lists all cpu/combined nodes with at least memorymin memory available for a Virtual Machine.
        *         * No backups or templates.
        *         * Not the CPU node on which the appliance is running.
        *         @execution_method = sync
        *         @param  memorymin:            Minimum available memory required in MB.
        *         @type memorymin:              integer
        *         @param  hypervisor:           Hypervisor running on the node (optional)
        *         @type hypervisor:             string
        *         @param includeappliancehost:  Include the host of the appliance machine in the list
        *         @type includeappliancehost:   boolean
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'MyWebServer',
        *         @note:                                          'description': 'My Personal Web Server',
        *         @note:                                          'status': 'RUNNING',
        *         @note:                                          'os': 'LINUX',
        *         @note:                                          'hostname': 'web001',
        *         @note:                                          'memory': 4096,
        *         @note:                                          'nrcpu': 2,
        *         @note:                                          'memoryavailable': 2048,
        *         @note:                                          'hypervisor': 'VIRTUALBOX30',
        *         @note:                                          'importancefactor': 3},
        *         @note:                                        { 'machineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'MyDbServer',
        *         @note:                                          'description': 'My Personal DB Server',
        *         @note:                                          'status': 'RUNNING',
        *         @note:                                          'os': 'LINUX',
        *         @note:                                          'hostname': 'db001',
        *         @note:                                          'memory': 4096,
        *         @note:                                          'nrcpu': 4,
        *         @note:                                          'memoryavailable': 2048,
        *         @note:                                          'hypervisor': 'VIRTUALBOX30',
        *         @note:                                          'importancefactor': 2}]}
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function listAvailableCPUNodes (memorymin:Object,hypervisor:Object=null,includeappliancehost:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAvailableCPUNodes', listAvailableCPUNodes_ResultReceived, getError, memorymin,hypervisor,includeappliancehost,jobguid,executionparams);

        }

        private function listAvailableCPUNodes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTAVAILABLECPUNODES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SENDMAIL:String = 'sendMail_response';
        /**
        *         Sends a mail using smtp 
        *         @param subject:           Subject for the email 
        *         @type subject:            string
        *         @param body:              Body of the mail
        *         @type body:               string
        *         
        *         @param sender:            The email address of the sender
        *         @type sender:             string
        *         
        *         @param to:                The email address of the addressee (when None admin is the target)
        *         @type to:                 string
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function sendMail (subject:String,body:String="",sender:String="",to:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'sendMail', sendMail_ResultReceived, getError, subject,body,sender,to,jobguid,executionparams);

        }

        private function sendMail_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SENDMAIL, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_STARTMACHINES:String = 'startMachines_response';
        /**
        *         Starts multiple machines at once 
        *         @param machineguids:      guids of the machines to start
        *         @type machineguids:       list
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function startMachines (machineguids:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'startMachines', startMachines_ResultReceived, getError, machineguids,jobguid,executionparams);

        }

        private function startMachines_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_STARTMACHINES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSMARTCLIENTBYDEVICE:String = 'listSmartclientByDevice_response';
        /**
        *         Gets the list of smartclients by deviceguid
        *         @param deviceguid           Guid of the device
        *         @type deviceguid:           guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    information [{ description , iqn , address, machinename }]
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listSmartclientByDevice (deviceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listSmartclientByDevice', listSmartclientByDevice_ResultReceived, getError, deviceguid,jobguid,executionparams);

        }

        private function listSmartclientByDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSMARTCLIENTBYDEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAVAILABLEHYPERVISORS:String = 'getAvailableHypervisors_response';
        /**
        *         Lists available hypervisors
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getAvailableHypervisors (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAvailableHypervisors', getAvailableHypervisors_ResultReceived, getError, jobguid,executionparams);

        }

        private function getAvailableHypervisors_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAVAILABLEHYPERVISORS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CHANGEAGENTPASSWORD:String = 'changeAgentPassword_response';
        /**
        *         Modify the password of the agent v4.
        *         
        *         @param oldpwd:                current password of the agent
        *         @type oldpwd:                 string
        *         
        *         @param newpwd:                new password for the agent
        *         @type newpwd:                 string
        *         
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function changeAgentPassword (oldpwd:String,newpwd:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'changeAgentPassword', changeAgentPassword_ResultReceived, getError, oldpwd,newpwd,jobguid,executionparams);

        }

        private function changeAgentPassword_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CHANGEAGENTPASSWORD, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_STARTAPPLICATIONS:String = 'startApplications_response';
        /**
        *         Starts a list of applications     
        *         @param machineguid:           List of applications guids
        *         @type machineguid:            list
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function startApplications (applicationguids:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'startApplications', startApplications_ResultReceived, getError, applicationguids,jobguid,executionparams);

        }

        private function startApplications_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_STARTAPPLICATIONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_VALIDATEDOMAIN:String = 'validateDomain_response';
        /**
        *         validates a domain for a customer
        *         @param machineguids:      list of machineguids to be validated (if none are passed all pmachineguids are tested) 
        *         @type machineguids:       list
        *         @param domain:            Domain to validate
        *         @type domain:             string
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function validateDomain (machineguids:Object=null,domain:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'validateDomain', validateDomain_ResultReceived, getError, machineguids,domain,jobguid,executionparams);

        }

        private function validateDomain_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_VALIDATEDOMAIN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETESNAPSHOTS:String = 'deleteSnapshots_response';
        /**
        *         Deletes all outdated snapshots off all disks
        *         @param policyguid:          Guid of the snapshot retention policy to detect outdated snapshots
        *         @type policyguid:           guid
        *         
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function deleteSnapshots (policyguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteSnapshots', deleteSnapshots_ResultReceived, getError, policyguid,jobguid,executionparams);

        }

        private function deleteSnapshots_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETESNAPSHOTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDDATADISKS:String = 'addDataDisks_response';
        /**
        *         Adds multiple data disks at once to a machine
        *         
        *         @param machineguid:           guid of the machine rootobject
        *         @type machineguid:            guid
        *     
        *         @param diskinfo:              [ { name: , size: , description, retentionpolicyguid} ]
        *         @type diskinfo:               list
        *         
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with added diskguids e.g. params  { 'result': [diskguids] }  
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function addDataDisks (machineguid:String,diskinfo:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addDataDisks', addDataDisks_ResultReceived, getError, machineguid,diskinfo,jobguid,executionparams);

        }

        private function addDataDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDDATADISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDSMARTCLIENTDEVICE:String = 'addSmartClientDevice_response';
        /**
        *         Adds a new smart client device to a Smart Style Office environment
        *         @param  name                name of the device
        *         @type name                  string
        *         @param macaddress           MAC address of the new resource node
        *         @type macaddress            string
        *         @param description          remarks on the device
        *         @type description           type_description
        *         @param racku                size of the device, measured in u e.g. 1u high
        *         @type racku                 int
        *         @param racky                physical position of the device in a rack (y coordinate) measured in u slots. The position starts at bottom of rack, starting with 1
        *         @type racky                 int
        *         @param rackz                physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
        *         @type rackz                 int
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function addSmartClientDevice (name:Object,macaddress:Object,cloudspaceguid:Object,description:Object=null,racku:Object=null,racky:Object=null,rackz:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addSmartClientDevice', addSmartClientDevice_ResultReceived, getError, name,macaddress,cloudspaceguid,description,racku,racky,rackz,jobguid,executionparams);

        }

        private function addSmartClientDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDSMARTCLIENTDEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CLEANUP:String = 'cleanup_response';
        /**
        *         DRP model cleansing:
        *           Removes versioning information on all rootobjects
        *           Removes events and jobs older than maxage
        *                              
        *         @param maxage:            how long the information is kept
        *         @type maxage:             int
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function cleanup (maxage:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'cleanup', cleanup_ResultReceived, getError, maxage,jobguid,executionparams);

        }

        private function cleanup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CLEANUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSYSTEMNASISOIMAGES:String = 'listSystemNASISOImages_response';
        /**
        *         Lists iso images available on the SystemNAS
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with available iso images and their paths
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function listSystemNASISOImages (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listSystemNASISOImages', listSystemNASISOImages_ResultReceived, getError, jobguid,executionparams);

        }

        private function listSystemNASISOImages_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSYSTEMNASISOIMAGES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MAINTENANCE:String = 'maintenance_response';
        /**
        *         Execute maintenance tasks on SSO environment.
        *         
        *         @param duration:            duration of the maintenance tasks (seconds)
        *         @type duration:             int
        *         
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function maintenance (duration:Number=3600,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'maintenance', maintenance_ResultReceived, getError, duration,jobguid,executionparams);

        }

        private function maintenance_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MAINTENANCE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDVIRTUALSERVERFROMTEMPLATE:String = 'addVirtualServerFromTemplate_response';
        /**
        *         Adds a new virtual server to a Smart Style Office environment
        *         @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:              guid
        *         @param templatemachineguid:         guid of the machine this machine will be based on.
        *         @type  templatemachineguid:         guid
        *         @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                         string
        *         @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        *         @type languids:                     array
        *         @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                  string
        *         @param parentmachineguid:           guid of the machine this machine will be created upon.
        *         @type  parentmachineguid:           guid
        *         
        *         @param userinfo:                    {clouduserguid,login,password,email, firstname,lastname}
        *         @type userinfo:                     dictionary
        *         @param vdcinfo:                     {vdcguid,posx,posy}
        *         @type vdcinfo:                      dictionary
        *         
        *         @param defaultgateway:              Default gateway for the machine
        *         @type defaultgateway:               string
        *         @param jobguid:                     Guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:              dictionary
        *         @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                           In case an error occurred, exception is raised
        *         
        */
        public function addVirtualServerFromTemplate (cloudspaceguid:String,templatemachineguid:String,name:String,languids:Array=null,description:String="",parentmachineguid:String="",userinfo:Object="",vdcinfo:Object="",defaultgateway:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addVirtualServerFromTemplate', addVirtualServerFromTemplate_ResultReceived, getError, cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,userinfo,vdcinfo,defaultgateway,jobguid,executionparams);

        }

        private function addVirtualServerFromTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDVIRTUALSERVERFROMTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALMACHINEDISKINFO:String = 'getVirtualMachineDiskInfo_response';
        /**
        *         returns information about the virtual machine disk information 
        *         @security administrators
        *         @param machineguid:         machineguid of the virtual machine
        *         @type machineguid:          guid
        *                 
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary 
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getVirtualMachineDiskInfo (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualMachineDiskInfo', getVirtualMachineDiskInfo_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getVirtualMachineDiskInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALMACHINEDISKINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDVIRTUALDESKTOP:String = 'addVirtualDesktop_response';
        /**
        *         Creates a new virtual desktop.
        *         @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:             guid
        *         @param name:                       Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                        string
        *         @param machinetype:                machinetype of the machine. IMAGEONLY|SMARTCLIENT|VIRTUALDESKTOP|PHYSICAL|SNAPSHOT|VIRTUALSERVER.
        *         @type machinetype:                 string
        *         @param status:                     status of the machine. CONFIGURED|IMAGEONLY|RUNNING|TODELETE|DELETING|OVERLOADED|STARTING|HALTED|PAUSED|STOPPING
        *         @type status:                      string
        *         @param bootstatus:                 bootstatus of the machine. FROMDISK|RECOVERY|INSTALL
        *         @type bootstatus:                  string
        *         @param assetid:                    Unique name of the machine. (Can be used as external reference by the user)
        *         @type assetid:                     string
        *         @param memory:                     Memory for the machine in MB. Same as template if not provided.
        *         @type memory:                      int
        *         @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        *         @type memoryminimal:               int
        *         @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        *         @type nrcpu:                       int
        *         @param cpufrequency:               CPU frequency in MHz.
        *         @type cpufrequency:                int
        *         @param description:                Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                 string
        *         @param parentmachineguid:          guid of the physical machine this machine will be created upon.
        *         @type  parentmachineguid:          guid
        *         @param networkinfo:                network information {nr_nics: , info { languid, ip} }
        *         @type networkinfo:                 dictionary
        *         @param diskinfo:                   disk information info [{ diskguid, size, role}]
        *         @type diskinfo:                    list
        *         @param osguid:                     osguid of the machine.
        *         @type  osguid:                     guid
        *         @param deviceguid:                 deviceguid of the machine.
        *         @type  deviceguid:                 guid
        *         @param hostname:                   hostname of the machine
        *         @type hostname:                    string
        *         @param backup:                     whether to backup the machine
        *         @type backup:                      boolean
        *         @param boot:                       whether to boot the machine when pmachine starts
        *         @type boot:                        boolean
        *         @param alias:                      alias of the machine
        *         @type alias:                       string
        *         @param userinfo:                   {clouduserguid,login,password,email, firstname,lastname}
        *         @type userinfo:                    dictionary
        *         @param hypervisor:                 hypervisor of the machine.
        *         @type hypervisor:                  string
        *         @param importancefactor:           hypervisor of the machine.
        *         @type importancefactor:            string
        *         @param defaultgateway:             Default gateway for the machine
        *         @type defaultgateway:              string
        *         
        *         @param monitors:                   monitors configuration ['1024x768x24','800x600x24']
        *         @type monitors:                    list
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addVirtualDesktop (cloudspaceguid:String,name:String,machinetype:String="PHYSICAL",status:String="CONFIGURED",bootstatus:String="FROMDISK",assetid:String="",memory:Number=0,memoryminimal:Number=0,nrcpu:Number=1,cpufrequency:Number=0,description:String="",parentmachineguid:String="",networkinfo:Object=null,diskinfo:Object=null,osguid:String="",deviceguid:String="",hostname:String="",backup:Boolean=false,boot:Boolean=false,alias:String="",userinfo:Object="",hypervisor:String="",importancefactor:String="",defaultgateway:String="",monitors:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addVirtualDesktop', addVirtualDesktop_ResultReceived, getError, cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,osguid,deviceguid,hostname,backup,boot,alias,userinfo,hypervisor,importancefactor,defaultgateway,monitors,jobguid,executionparams);

        }

        private function addVirtualDesktop_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDVIRTUALDESKTOP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALSERVERINFO:String = 'getVirtualServerInfo_response';
        /**
        *         Returns information about the virtual server
        *         @param macaddress:          macaddress of the virtual server
        *         @type macaddress:           string
        *                 
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getVirtualServerInfo (macaddress:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualServerInfo', getVirtualServerInfo_ResultReceived, getError, macaddress,jobguid,executionparams);

        }

        private function getVirtualServerInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALSERVERINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDSMARTCLIENTKIOSKMODEFROMTEMPLATE:String = 'addSmartClientKioskModeFromTemplate_response';
        /**
        *         Adds a new smart client based on a template to a Smart Style Office environment
        *         @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:              guid
        *         @param templatemachineguid:         guid of the machine this machine will be based on.
        *         @type  templatemachineguid:         guid
        *         @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                         string
        *         @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        *         @type languids:                     array
        *         @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                  string
        *         @param parentmachineguid:           guid of the machine this machine will be created upon.
        *         @type  parentmachineguid:           guid
        *         @param deviceguid                   guid of an existing smart client device to which this virtual desktop is linked
        *         @type deviceguid                    guid
        *         @param  devicename                  name for the new smart client device to which this virtual desktop is linked
        *         @type devicename                    string
        *         @param  macaddress                  mac address for the new smart client device to which this virtual desktop is linked
        *         @type macaddress                    string
        *         @param vdcinfo:                     {vdcguid,posx,posy}
        *         @type vdcinfo:                      dictionary
        *         @param jobguid:                     Guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:              dictionary
        *         @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                           In case an error occurred, exception is raised
        *         
        */
        public function addSmartClientKioskModeFromTemplate (cloudspaceguid:String,templatemachineguid:String,name:String,languids:Array=null,description:String="",parentmachineguid:Object=null,deviceguid:Object=null,devicename:Object=null,macaddress:Object=null,vdcinfo:Object="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addSmartClientKioskModeFromTemplate', addSmartClientKioskModeFromTemplate_ResultReceived, getError, cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,deviceguid,devicename,macaddress,vdcinfo,jobguid,executionparams);

        }

        private function addSmartClientKioskModeFromTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDSMARTCLIENTKIOSKMODEFROMTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTFOCVOLUMES:String = 'listFOCVolumes_response';
        /**
        *  
        *         List FailOver Cache volumes on a given machine
        *         
        *         @execution_method = sync
        *         
        *         @param machineguid:           guid of the machine to list the FOC volumes
        *         @type  machineguid:           guid
        *         
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      list of volumes having the FOC on this node 
        *         @rtype:                       list
        *         @raise e:                     In case an error occurred, exception is raised        
        *         
        */
        public function listFOCVolumes (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listFOCVolumes', listFOCVolumes_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listFOCVolumes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTFOCVOLUMES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDNODE:String = 'addNode_response';
        /**
        *         Adds a new node to a Smart Style Office environment
        *         @security administrators
        *         @param macaddress:          MAC address of the new node
        *         @type macaddress:           string
        *         @param name:                Name for the new node
        *         @type name:                 string
        *         @param description:         Description for the new node
        *         @type description:          string
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary with the new device guid  as result and jobguid: {'result': '2388d3d3-4de4-45fe-b17f-4f1ca05ff062', 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function addNode (macaddress:String,name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addNode', addNode_ResultReceived, getError, macaddress,name,description,jobguid,executionparams);

        }

        private function addNode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDNODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALDESKTOPINFO:String = 'getVirtualDesktopInfo_response';
        /**
        *         returns information about the virtual desktop 
        *         @param macaddress:          macaddress of the virtual desktop
        *         @type macaddress:           string
        *                 
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getVirtualDesktopInfo (macaddress:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualDesktopInfo', getVirtualDesktopInfo_ResultReceived, getError, macaddress,jobguid,executionparams);

        }

        private function getVirtualDesktopInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALDESKTOPINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDVIRTUALDESKTOPFROMTEMPLATE:String = 'addVirtualDesktopFromTemplate_response';
        /**
        *         Adds a new virtual desktop to a Smart Style Office environment
        *         @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:              guid
        *         @param templatemachineguid:         guid of the machine this machine will be based on.
        *         @type  templatemachineguid:         guid
        *         @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                         string
        *         @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        *         @type languids:                     array
        *         @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                  string
        *         @param parentmachineguid:           guid of the machine this machine will be created upon.
        *         @type  parentmachineguid:           guid
        *         @param userinfo:                    {clouduserguid,login,password,email, firstname,lastname}
        *         @type userinfo:                     dictionary
        *         @param vdcinfo:                     {vdcguid,posx,posy}
        *         @type vdcinfo:                      dictionary
        *         
        *         @param defaultgateway:              Default gateway for the machine
        *         @type defaultgateway:               string
        *         @param jobguid:                     Guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:              dictionary
        *         @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                           In case an error occurred, exception is raised
        *         
        */
        public function addVirtualDesktopFromTemplate (cloudspaceguid:String,templatemachineguid:String,name:String,languids:Array=null,description:String="",parentmachineguid:String="",userinfo:Object="",vdcinfo:Object="",defaultgateway:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addVirtualDesktopFromTemplate', addVirtualDesktopFromTemplate_ResultReceived, getError, cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,userinfo,vdcinfo,defaultgateway,jobguid,executionparams);

        }

        private function addVirtualDesktopFromTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDVIRTUALDESKTOPFROMTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ASSIGNDEVICETOPOWERPORT:String = 'assignDeviceToPowerPort_response';
        /**
        *         Assigns a device to a power port of a powerswitch
        *         @param deviceguid:              guid of the device assigned to the power port
        *         @type deviceguid:               guid
        *         
        *         @param powerswitchdeviceguid:   guid of the powerswitch device
        *         @type powerswitchdeviceguid:    guid
        *         
        *         @param powerportsequence:       sequence of the powerport
        *         @type powerportsequence:        int        
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary
        *         @rtype:                         dictionary
        *  
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function assignDeviceToPowerPort (deviceguid:String,powerswitchdeviceguid:String,powerportsequence:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'assignDeviceToPowerPort', assignDeviceToPowerPort_ResultReceived, getError, deviceguid,powerswitchdeviceguid,powerportsequence,jobguid,executionparams);

        }

        private function assignDeviceToPowerPort_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ASSIGNDEVICETOPOWERPORT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALDESKTOPCLIENT:String = 'getVirtualDesktopClient_response';
        /**
        *         returns current user connected to the virtual desktop 
        *         @param macaddress:          macaddress of the virtual desktop
        *         @type macaddress:           string
        *                 
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary having Ipaddress of the client connected to the Vmachine
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getVirtualDesktopClient (macaddress:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualDesktopClient', getVirtualDesktopClient_ResultReceived, getError, macaddress,jobguid,executionparams);

        }

        private function getVirtualDesktopClient_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALDESKTOPCLIENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CANMOVE:String = 'canMove_response';
        /**
        *         Checks whether vmachine(s) can be moved to other node(s) 
        *         @param movementplan:          dict of movement plan of the machines { sourcevmachine : target host }
        *         @type movementplan:           dict
        *         @param failover:              flag to use failovering workflow
        *         type failover:                boolean
        *         
        *         @param minimalcapacity:       flag to use minimal capacity workflow (e.g. minimal memory...)
        *         @type minimalcapacity:        boolean
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      True or False 
        *         @rtype:                       boolean
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function canMove (movementplan:Object=null,failover:Object=null,minimalcapacity:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'canMove', canMove_ResultReceived, getError, movementplan,failover,minimalcapacity,jobguid,executionparams);

        }

        private function canMove_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CANMOVE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTAVAILABLESTORAGEDAEMONS:String = 'listAvailableStorageDaemons_response';
        /**
        *         Lists all available storage daemons
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21435',
        *         @note:                              'result: [{ 'applicationguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'machineguid': '55544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'diskguid': '977cf8ee-8845-494f-bbc5-6ac559660201',
        *         @note:                                          'ipaddress': '192.168.0.1',
        *         @note:                                          'port': '23514',
        *         @note:                                          'path': '/mnt/dss/disk/977cf8ee-8845-494f-bbc5-6ac559660201',
        *         @note:                                          'status': 'ONLINE',
        *         @note:                                          'freespace': '465000'},
        *         @note:                                        { 'applicationguid': '33544B07-4129-47B1-8690-B92C0DB21435',
        *         @note:                                          'machineguid': '55544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'diskguid': '977cf8ee-8845-494f-bbc5-6ac559660202',
        *         @note:                                          'ipaddress': '192.168.0.1',
        *         @note:                                          'port': '23515',
        *         @note:                                          'path': '/mnt/dss/disk/977cf8ee-8845-494f-bbc5-6ac559660202',
        *         @note:                                          'status': 'ONLINE',
        *         @note:                                          'freespace': '465000'}]}
        *         
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listAvailableStorageDaemons (jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAvailableStorageDaemons', listAvailableStorageDaemons_ResultReceived, getError, jobguid,executionparams);

        }

        private function listAvailableStorageDaemons_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTAVAILABLESTORAGEDAEMONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDSMARTCLIENTUSERMODEFROMTEMPLATE:String = 'addSmartClientUserModeFromTemplate_response';
        /**
        *         Adds a new smart client from a template to a Smart Style Office environment
        *         @param cloudspaceguid:              guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:              guid
        *         @param templatemachineguid:         guid of the machine this machine will be based on.
        *         @type  templatemachineguid:         guid
        *         @param name:                        Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                         string
        *         @param languids:                    Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        *         @type languids:                     array
        *         @param description:                 Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                  string
        *         @param parentmachineguid:           guid of the machine this machine will be created upon.
        *         @type  parentmachineguid:           guid
        *         @param userinfo:                    {clouduserguid,login,password,email, firstname,lastname}
        *         @type userinfo:                     dictionary
        *         @param vdcinfo:                     {vdcguid,posx,posy}
        *         @type vdcinfo:                      dictionary
        *         @param jobguid:                     Guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:              dictionary
        *         @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                           In case an error occurred, exception is raised
        *         
        */
        public function addSmartClientUserModeFromTemplate (cloudspaceguid:String,templatemachineguid:String,name:String,languids:Array=null,description:String="",parentmachineguid:String="",userinfo:Object="",vdcinfo:Object="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addSmartClientUserModeFromTemplate', addSmartClientUserModeFromTemplate_ResultReceived, getError, cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,userinfo,vdcinfo,jobguid,executionparams);

        }

        private function addSmartClientUserModeFromTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDSMARTCLIENTUSERMODEFROMTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETSSOVERSION:String = 'getSSOVersion_response';
        /**
        *         Lists version of the current SSO
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getSSOVersion (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getSSOVersion', getSSOVersion_ResultReceived, getError, jobguid,executionparams);

        }

        private function getSSOVersion_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETSSOVERSION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_APPLYTEMPLATE:String = 'applyTemplate_response';
        /**
        *         apply template to specific machine
        *         @param diskguid             guid of orignial boot disk
        *         @type diskguid:             guid
        *         @param machineguid:         guid of the machine rootobject
        *         @type machineguid:          guid
        *         @param overwrite:           boolean value indicating whether the old boot disk in the machine will be overwritten
        *         @type overwrite:            boolean
        *         @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function applyTemplate (diskguid:String,machineguid:String,overwrite:Boolean=false,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'applyTemplate', applyTemplate_ResultReceived, getError, diskguid,machineguid,overwrite,jobguid,executionparams);

        }

        private function applyTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_APPLYTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_INITIALIZE:String = 'initialize_response';
        /**
        *         Initializes a new Smart Style Office environment
        *         @security administrators
        *         @param email                Email for the administrator account. All system level communication will be send to this email address.
        *         @type email                 string
        *         @param password             Password for the administrator account.
        *         @type password              string
        *         @param ipaddress            The public IP address for the appliance.
        *         @type ipaddress             string
        *         @param netmask              Netmask of the customer LAN.
        *         @type netmask               string
        *         @param gateway              Gateway IP address of the customer LAN.
        *         @type gateway               string
        *         @param dnsserver            IP address of the DSN server of the customer LAN.
        *         @type dnsserver             string
        *         @param network              Network range to be used as public LAN. Will be used if Smart Style Office environment is NOT integrated into customer LAN.
        *         @type network               string
        *         @param netmaskpublic        Netmask of the new public LAN that will be created.
        *         @type netmaskpublic         string
        *         @param startip              Start IP address of the public LAN. Will be used if Smart Style Office environment is integrated into customer LAN.
        *         @type startip               string
        *         @param endip                End IP address of the public LAN. Will be used if Smart Style Office environment is integrated into customer LAN.
        *         @type endip                 string
        *         @param sitename             Name for this Smart Style Office site.
        *         @type sitename              string
        *         @param sitedescription      Description for this Smart Style Office site.
        *         @type sitedescription       string
        *         @param siteaddress          Address for this Smart Style Office site.
        *         @type siteaddress           string
        *         @param sitecity             City for this Smart Style Office site.
        *         @type sitecity              string
        *         @param sitecountry          County for this Smart Style Office site.
        *         @type sitecountry           string
        *         
        *         @param setuptype:           Define setup type configuration [SSO | CLOUDMIRROR]
        *         @type setuptype:            string
        *         @param firstnodetype:       Define node type configuration for first node [COMBINEDNODE | CPUNODE]
        *         @type firstnodetype:        string
        *         
        *         @param networkname:         name of the public network 
        *         @type networkname:          string
        *         @param timezonename:        timezone to be set for physical machines 
        *         @type timezonename:         string        
        *         
        *         @param timezonedelta:       delta of timeZone for the location.
        *         @type timezonedelta:        float        
        *         
        *         @param smtpserver:          Smtp server
        *         @type smtpserver:           string
        *         
        *         @param smtplogin:           Login for the Smtp server
        *         @type smtplogin:            string
        *         
        *         @param smtppassword:        Password for the Smtp server
        *         @type smtppassword:         string
        *         
        *         @param nrreservedip:        Number of reserved ip addresses for the sso nodes
        *         @type  nrreservedip:        integer 
        *         
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function initialize (email:Object,password:Object,ipaddress:Object,netmask:Object,gateway:Object,dnsserver:Object,network:Object=null,netmaskpublic:Object=null,startip:Object=null,endip:Object=null,sitename:Object=null,sitedescription:Object=null,siteaddress:Object=null,sitecity:Object=null,sitecountry:Object=null,setuptype:String="SSO",firstnodetype:String="COMBINEDNODE",networkname:String="",timezonename:String="",timezonedelta:Object=null,smtpserver:String="",smtplogin:String="",smtppassword:String="",nrreservedip:Number=-1,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'initialize', initialize_ResultReceived, getError, email,password,ipaddress,netmask,gateway,dnsserver,network,netmaskpublic,startip,endip,sitename,sitedescription,siteaddress,sitecity,sitecountry,setuptype,firstnodetype,networkname,timezonename,timezonedelta,smtpserver,smtplogin,smtppassword,nrreservedip,jobguid,executionparams);

        }

        private function initialize_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_INITIALIZE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVEMACHINE:String = 'moveMachine_response';
        /**
        *         Moves a machine to another node     
        *         @param movementplan:          dict of movement plan of the machines { sourcevmachine : target host }
        *         @type movementplan:           dict
        *         @param failover:              flag to use failovering workflow
        *         type failover:                boolean
        *         
        *         @param minimalcapacity:       flag to use minimal capacity workflow (e.g. minimal memory...)
        *         @type minimalcapacity:        boolean
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function moveMachine (movementplan:Object=null,failover:Object=null,minimalcapacity:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveMachine', moveMachine_ResultReceived, getError, movementplan,failover,minimalcapacity,jobguid,executionparams);

        }

        private function moveMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVEMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_READCONFIGURATIONINFO:String = 'readConfigurationInfo_response';
        /**
        *         Get information about a specified image configuration 
        *         @param sourceuri:             URI where the configuration resides
        *         @type sourceuri:              string
        *         
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with available templates and its path
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function readConfigurationInfo (sourceuri:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'readConfigurationInfo', readConfigurationInfo_ResultReceived, getError, sourceuri,jobguid,executionparams);

        }

        private function readConfigurationInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_READCONFIGURATIONINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_STOPAPPLICATIONS:String = 'stopApplications_response';
        /**
        *         Stops a list of applications     
        *         @param machineguid:           List of applications guids
        *         @type machineguid:            list
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function stopApplications (applicationguids:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'stopApplications', stopApplications_ResultReceived, getError, applicationguids,jobguid,executionparams);

        }

        private function stopApplications_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_STOPAPPLICATIONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESTARTAPPLICATIONS:String = 'restartApplications_response';
        /**
        *         Restarts a list of applications     
        *         @param machineguid:           List of applications guids
        *         @type machineguid:            list
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function restartApplications (applicationguids:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'restartApplications', restartApplications_ResultReceived, getError, applicationguids,jobguid,executionparams);

        }

        private function restartApplications_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESTARTAPPLICATIONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDSMARTCLIENTKIOSKMODE:String = 'addSmartClientKioskMode_response';
        /**
        *         Creates a new machine based on a template, but allows you to overrule capacity properties of the machine.
        *         @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:             guid
        *         @param name:                       Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                        string
        *         @param machinetype:                machinetype of the machine. IMAGEONLY|SMARTCLIENT|VIRTUALDESKTOP|PHYSICAL|SNAPSHOT|VIRTUALSERVER.
        *         @type machinetype:                 string
        *         @param status:                     status of the machine. CONFIGURED|IMAGEONLY|RUNNING|TODELETE|DELETING|OVERLOADED|STARTING|HALTED|PAUSED|STOPPING
        *         @type status:                      string
        *         @param bootstatus:                 bootstatus of the machine. FROMDISK|RECOVERY|INSTALL
        *         @type bootstatus:                  string
        *         @param assetid:                    Unique name of the machine. (Can be used as external reference by the user)
        *         @type assetid:                     string
        *         @param memory:                     Memory for the machine in MB. Same as template if not provided.
        *         @type memory:                      int
        *         @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        *         @type memoryminimal:               int
        *         @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        *         @type nrcpu:                       int
        *         @param cpufrequency:               CPU frequency in MHz.
        *         @type cpufrequency:                int
        *         @param description:                Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                 string
        *         @param parentmachineguid:          guid of the physical machine this machine will be created upon.
        *         @type  parentmachineguid:          guid
        *         @param networkinfo:                network information {nr_nics: , info { languid, ip} }
        *         @type networkinfo:                 dictionary
        *         @param diskinfo:                   disk information info [{ diskguid, size, role}]
        *         @type diskinfo:                    list
        *         @param osguid:                     osguid of the machine.
        *         @type  osguid:                     guid
        *         @param deviceguid:                 deviceguid of the machine.
        *         @type  deviceguid:                 guid
        *         @param hostname:                   hostname of the machine
        *         @type hostname:                    string
        *         @param importancefactor:           importancefactor of the machine
        *         @type importancefactor:            int
        *         @param backup:                     whether to backup the machine
        *         @type backup:                      boolean
        *         @param boot:                       whether to boot the machine when pmachine starts
        *         @type boot:                        boolean
        *         @param alias:                       alias of the machine
        *         @type alias:                        string
        *         @param  devicename                  name for the new smart client device to which this virtual desktop is linked
        *         @type devicename                    string
        *         @param  macaddress                  mac address for the new smart client device to which this virtual desktop is linked
        *         @type macaddress                    string
        *         @param jobguid:                     Guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @param executionparams:             Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:              dictionary
        *         @return:                            Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addSmartClientKioskMode (cloudspaceguid:String,name:String,machinetype:String="PHYSICAL",status:String="CONFIGURED",bootstatus:String="FROMDISK",assetid:String="",memory:Number=0,memoryminimal:Number=0,nrcpu:Number=1,cpufrequency:Number=0,description:String="",parentmachineguid:String="",networkinfo:Object=null,diskinfo:Object=null,osguid:String="",deviceguid:String="",hostname:String="",importancefactor:Number=0,backup:Boolean=false,boot:Boolean=false,alias:Object=null,devicename:Object=null,macaddress:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addSmartClientKioskMode', addSmartClientKioskMode_ResultReceived, getError, cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,osguid,deviceguid,hostname,importancefactor,backup,boot,alias,devicename,macaddress,jobguid,executionparams);

        }

        private function addSmartClientKioskMode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDSMARTCLIENTKIOSKMODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAPPLIANCEINFO:String = 'getApplianceInfo_response';
        /**
        *         Lists info about the appliance vmachine
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getApplianceInfo (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getApplianceInfo', getApplianceInfo_ResultReceived, getError, jobguid,executionparams);

        }

        private function getApplianceInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAPPLIANCEINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESETFAILOVERCACHE:String = 'resetFailoverCache_response';
        /**
        *         Resets the Failover Cache of a disk (eg when degraded)
        *         @param diskguid:          guid of the disk
        *         @type diskguid:           guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  string containing status OK_SYNC, OK_STANDALONE, CATCHUP , DEGRADED or None
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function resetFailoverCache (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'resetFailoverCache', resetFailoverCache_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function resetFailoverCache_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESETFAILOVERCACHE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETFAILOVERCACHESTATUS:String = 'getFailoverCacheStatus_response';
        /**
        *         Returns the Failover Cache status of a disk when existing
        *         @param diskguid:          guid of the disk
        *         @type diskguid:           guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  string containing status OK_SYNC, OK_STANDALONE, CATCHUP , DEGRADED or None
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function getFailoverCacheStatus (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getFailoverCacheStatus', getFailoverCacheStatus_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getFailoverCacheStatus_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETFAILOVERCACHESTATUS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTWEBSERVICES:String = 'listWebservices_response';
        /**
        *         
        *         Lists the webservice urls for a certain action
        *         
        *         @execution_method = sync
        *         
        *         @param action                 The webservice needed (REGISTER, UNREGISTER, KEEPALIVE)
        *         @param action                 string
        *         
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *                 
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function listWebservices (action:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listWebservices', listWebservices_ResultReceived, getError, action,jobguid,executionparams);

        }

        private function listWebservices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTWEBSERVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETSYSTEMNASINFO:String = 'getSystemNasInfo_response';
        /**
        *         Lists info systemnas
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getSystemNasInfo (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getSystemNasInfo', getSystemNasInfo_ResultReceived, getError, jobguid,executionparams);

        }

        private function getSystemNasInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETSYSTEMNASINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FAILOVERMANAGEMENT:String = 'failoverManagement_response';
        /**
        *         Moves and Initializes all management applications to node with specified machineguid
        *         @execution_method = async
        *         @param machineguid:          Guid of the machine to fail over the management applications to
        *         @type machineguid:          guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function failoverManagement (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'failoverManagement', failoverManagement_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function failoverManagement_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FAILOVERMANAGEMENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDSMARTCLIENTUSERMODE:String = 'addSmartClientUserMode_response';
        /**
        *         Creates a new machine based on a template, but allows you to overrule capacity properties of the machine.
        *         @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:             guid
        *         @param name:                       Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                        string
        *         @param machinetype:                machinetype of the machine. IMAGEONLY|SMARTCLIENT|VIRTUALDESKTOP|PHYSICAL|SNAPSHOT|VIRTUALSERVER.
        *         @type machinetype:                 string
        *         @param status:                     status of the machine. CONFIGURED|IMAGEONLY|RUNNING|TODELETE|DELETING|OVERLOADED|STARTING|HALTED|PAUSED|STOPPING
        *         @type status:                      string
        *         @param bootstatus:                 bootstatus of the machine. FROMDISK|RECOVERY|INSTALL
        *         @type bootstatus:                  string
        *         @param assetid:                    Unique name of the machine. (Can be used as external reference by the user)
        *         @type assetid:                     string
        *         @param memory:                     Memory for the machine in MB. Same as template if not provided.
        *         @type memory:                      int
        *         @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        *         @type memoryminimal:               int
        *         @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        *         @type nrcpu:                       int
        *         @param cpufrequency:               CPU frequency in MHz.
        *         @type cpufrequency:                int
        *         @param description:                Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                 string
        *         @param parentmachineguid:          guid of the physical machine this machine will be created upon.
        *         @type  parentmachineguid:          guid
        *         @param networkinfo:                network information {nr_nics: , info { languid, ip} }
        *         @type networkinfo:                 dictionary
        *         @param diskinfo:                   disk information info [{ diskguid, size, role}]
        *         @type diskinfo:                    list
        *         @param osguid:                     osguid of the machine.
        *         @type  osguid:                     guid
        *         @param deviceguid:                 deviceguid of the machine.
        *         @type  deviceguid:                 guid
        *         @param hostname:                   hostname of the machine
        *         @type hostname:                    string
        *         @param backup:                     whether to backup the machine
        *         @type backup:                      boolean
        *         @param boot:                       whether to boot the machine when pmachine starts
        *         @type boot:                        boolean
        *         @param alias:                      alias of the machine
        *         @type alias:                       string
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addSmartClientUserMode (cloudspaceguid:String,name:String,machinetype:String="PHYSICAL",status:String="CONFIGURED",bootstatus:String="FROMDISK",assetid:String="",memory:Number=0,memoryminimal:Number=0,nrcpu:Number=1,cpufrequency:Number=0,description:String="",parentmachineguid:String="",networkinfo:Object=null,diskinfo:Object=null,osguid:String="",deviceguid:String="",hostname:String="",backup:Boolean=false,boot:Boolean=false,alias:String="",userinfo:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addSmartClientUserMode', addSmartClientUserMode_ResultReceived, getError, cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,osguid,deviceguid,hostname,backup,boot,alias,userinfo,jobguid,executionparams);

        }

        private function addSmartClientUserMode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDSMARTCLIENTUSERMODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OPTIMIZEDISKS:String = 'optimizeDisks_response';
        /**
        *         Optimizes a disk. E.g. defragments a Physical disk or scrubs a DSS disks
        *         @param diskguid:                guids of the disks to optimize.
        *         @type diskguid:                 list
        *         @param scrubagentmachineguid:   guid of the machine where scrubbing agent is running
        *         @type scrubagentmachineguid:    guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function optimizeDisks (diskguids:Object=null,scrubagentmachineguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'optimizeDisks', optimizeDisks_ResultReceived, getError, diskguids,scrubagentmachineguid,jobguid,executionparams);

        }

        private function optimizeDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OPTIMIZEDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETASSIGNEDFOCNODE:String = 'getAssignedFOCNode_response';
        /**
        *         Retrieves the pmachine of the FailOver Cache for the given disk 
        *         @execution_method = sync
        *         
        *         @param diskguid:          guid of the disk
        *         @type diskguid:           guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dict with applicationguid and foc machineguid
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function getAssignedFOCNode (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAssignedFOCNode', getAssignedFOCNode_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getAssignedFOCNode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETASSIGNEDFOCNODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTAVAILABLESTORAGENODES:String = 'listAvailableStorageNodes_response';
        /**
        *         Lists all available storage nodes
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listAvailableStorageNodes (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAvailableStorageNodes', listAvailableStorageNodes_ResultReceived, getError, jobguid,executionparams);

        }

        private function listAvailableStorageNodes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTAVAILABLESTORAGENODES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SENDSNMPTRAP:String = 'sendSNMPTrap_response';
        /**
        *         Generate a notification (trap) to report an event to the SNMP manager with the specified message.
        *         @param message:           Message of notification 
        *         @type message:            string
        *         @param hostdestination:   Specifies the target network manager host to which the trap message will be sent. 
        *         @type hostdestination:    string
        *         
        *         @param port:              Port number on host
        *         @type port:               int
        *         
        *         @param community:         Specifies community name to use
        *         @type community:          string
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function sendSNMPTrap (message:String,hostdestination:String="127.0.0.1",port:Number=126,community:String="aserver",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'sendSNMPTrap', sendSNMPTrap_ResultReceived, getError, message,hostdestination,port,community,jobguid,executionparams);

        }

        private function sendSNMPTrap_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SENDSNMPTRAP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_INITIALIZENODE:String = 'initializeNode_response';
        /**
        *         Initializes a device as a specified node type in the Smart Style Office environment.
        *         @security administrators
        *         @param deviceguid:          Guid of the device to install
        *         @type deviceguid:           guid
        *         @param nodetype:            Node type of the device to add (CPU, STORAGE or COMBINED)
        *         @type nodetype:             string
        *         @param name:                Name for the new node
        *         @type name:                 string
        *         @param description:         Description for the new node
        *         @type description:          string
        *         
        *         @param hypervisor:          Hypervisor for the new node
        *         @type hypervisor:           string
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function initializeNode (deviceguid:String,nodetype:String,name:String="",description:String="",hypervisor:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'initializeNode', initializeNode_ResultReceived, getError, deviceguid,nodetype,name,description,hypervisor,jobguid,executionparams);

        }

        private function initializeNode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_INITIALIZENODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETTIMEZONE:String = 'setTimezone_response';
        /**
        *         sets timezone for the sso environment
        *         @param timezone:            Timezone to be set
        *         @type timezone:             string
        *         
        *         @param timezonedelta:       delta of timeZone for the location.
        *         @type timezonedelta:        float
        *         
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function setTimezone (timezone:String,timezonedelta:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setTimezone', setTimezone_ResultReceived, getError, timezone,timezonedelta,jobguid,executionparams);

        }

        private function setTimezone_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETTIMEZONE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GENERATEMACADDRESS:String = 'generateMacAddress_response';
        /**
        *         Generates a new MAC address depending on LAN and customer
        *         @execution_method = sync
        *         @param languid              guid of languid
        *         @type languid:              guid
        *         @param customerguid         guid of customerguid
        *         @type customerguid:         guid
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    mac address
        *         @rtype:                     string
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function generateMacAddress (languid:Object,customerguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'generateMacAddress', generateMacAddress_ResultReceived, getError, languid,customerguid,jobguid,executionparams);

        }

        private function generateMacAddress_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GENERATEMACADDRESS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSMARTCLIENTBYUSER:String = 'listSmartclientByUser_response';
        /**
        *         Gets the list of smartclients for a specific user
        *         @execution_method = sync
        *         @param clouduserguid        guid of clouduser
        *         @type clouduserguid:        guid
        *         @param customerguid         guid of customerguid
        *         @type customerguid:         guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    information [{ description , iqn , address, machinename }]
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listSmartclientByUser (clouduserguid:Object,customerguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listSmartclientByUser', listSmartclientByUser_ResultReceived, getError, clouduserguid,customerguid,jobguid,executionparams);

        }

        private function listSmartclientByUser_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSMARTCLIENTBYUSER, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALMACHINEINFO:String = 'getVirtualMachineInfo_response';
        /**
        *         Returns information about the virtual machine
        *         @param macaddress:          macaddress of the virtual machine
        *         @type macaddress:           string
        *         
        *         @param machinetype:         type of the virtual machine (VIRTUALSERVER | VIRTUALDESKTOP)
        *         @type machinetype:          string
        *                 
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function getVirtualMachineInfo (macaddress:String,machinetype:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualMachineInfo', getVirtualMachineInfo_ResultReceived, getError, macaddress,machinetype,jobguid,executionparams);

        }

        private function getVirtualMachineInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALMACHINEINFO, false, false, e.result));
            srv.disconnect();
        }


    }
}

