
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Machine extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_machine';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Machine()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_RESTORE:String = 'restore_response';
        /**
        *         Restores a snapshot of a machine on another machine.
        *         @param backupmachineguid:          guid of the backup machine to restore.
        *         @type  backupmachineguid:          guid
        *         @param restoremachineguid:         guid of the machine to restore the backup on.  If not specified, the backup will be restored on the machine from which the backup was taken from.
        *         @type  restoremachineguid:         guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function restore (backupmachineguid:String,restoremachineguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'restore', restore_ResultReceived, getError, backupmachineguid,restoremachineguid,jobguid,executionparams);

        }

        private function restore_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESTORE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_BOOTINRECOVERMODE:String = 'bootInRecoverMode_response';
        /**
        *         make sure machine boots in recovery mode (a special network booted linux which gives access to local disk, ...)
        *         on recovery machine applications like mc, krusader, disk mgmt tools, ... are installed
        *         the pmachine will be booted with ip network config as specified in DRP
        *         
        *         when vmachine: use minimal memory properties
        *         
        *         FLOW
        *         #set machine.bootstatus=... to go to recovery mode
        *         #actor:  Installserver.bootInRecoverMode(...
        *         @param jobguid:          Guid of the job
        *         @type jobguid:           guid
        *         @param machineguid:      Guid of the physical machine
        *         @type machineguid:       guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        */
        public function bootInRecoverMode (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'bootInRecoverMode', bootInRecoverMode_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function bootInRecoverMode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_BOOTINRECOVERMODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ATTACHTODEVICE:String = 'attachToDevice_response';
        /**
        *         Forces a machine to run on a particular device.
        *         (will use resourcegroups underneath)
        *         @param machineguid:                guid of the machine to attach to a device.
        *         @type  machineguid:                guid
        *         @param deviceguid:                 guid of the device to attach the machine to.
        *         @type  deviceguid:                 guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function attachToDevice (machineguid:String,deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'attachToDevice', attachToDevice_ResultReceived, getError, machineguid,deviceguid,jobguid,executionparams);

        }

        private function attachToDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ATTACHTODEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CHANGEPASSWORD:String = 'changePassword_response';
        /**
        *         Changes the password on a pmachine using new pass word
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
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function changePassword (machineguid:Object,username:Object,newpassword:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'changePassword', changePassword_ResultReceived, getError, machineguid,username,newpassword,jobguid,executionparams);

        }

        private function changePassword_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CHANGEPASSWORD, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCAPACITYPROVIDED:String = 'addCapacityProvided_response';
        /**
        *         Adds provided capacity for the machine specified.
        *         @param machineguid:          guid of the machine specified
        *         @type machineguid:           guid
        *         @param amount:               Amount of capacity units to add
        *         @type amount:                integer
        *         @param capacityunittype:     Type of capacity units to add. See ca.capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param name:                 Name of capacity units to add.
        *         @type name:                  string
        *         @param description:          Description of capacity units to add.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function addCapacityProvided (machineguid:String,amount:Number,capacityunittype:String,name:String="",description:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addCapacityProvided', addCapacityProvided_ResultReceived, getError, machineguid,amount,capacityunittype,name,description,jobguid,executionparams);

        }

        private function addCapacityProvided_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCAPACITYPROVIDED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETMAXIMUMALLOWEDIPCOUNT:String = 'getMaximumAllowedIPCount_response';
        /**
        *         Retrieve the maximum allowed ip addresses on the specified machine
        *         
        *         @param machineguid:           guid of the machine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      number of maximum allowed ip addresses or -1 for unlimited number
        *         @rtype:                       integer
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function getMaximumAllowedIPCount (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getMaximumAllowedIPCount', getMaximumAllowedIPCount_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getMaximumAllowedIPCount_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETMAXIMUMALLOWEDIPCOUNT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of machine guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:                       Name of the machine.
        *         @type name:                        string
        *         @param assetid:                    Asset ID.
        *         @type assetid:                     string
        *         @param alias:                      Alias of the machine.
        *         @type alias:                       string
        *         @param description:                Description for this machine
        *         @type description:                 string
        *         @param macaddress:                 MAC address of a NIC on the machine.
        *         @type macaddress:                  string
        *         @param hostname:                   Hostname of the machine.
        *         @type hostname:                    string
        *         @param status:                     Status of the machine   CONFIGURED|IMAGEONLY|HALTED|RUNNING|OVERLOADED|PAUSED|TODELETE|STOPPING|STARTING|DELETING
        *         @type status:                      string
        *         @param hypervisor:                 Hypervisor of the machine.
        *         @type hypervisor:                  string
        *         @param defaultgateway:             Default gateway ip addr
        *         @type defaultgateway:              ipaddress
        *         @param agentguid:                  Guid of the agent.
        *         @type agentguid:                   guid
        *         @param deviceguid:                 Guid of the device.
        *         @type deviceguid:                  guid
        *         @param parentmachineguid:          Guid of the parent machine
        *         @type parentmachineguid:           guid
        *         @param osguid:                     Guid of the OS.
        *         @type osguid:                      guid
        *         @param clouduserguid:              Guid of the clouduser, owning this machine
        *         @type clouduserguid:               guid
        *         @param ownerguid:                  Guid of the owner.
        *         @type ownerguid:                   guid
        *         @param cloudspaceguid:             Guid of the space to which this machine belongs
        *         @type cloudspaceguid:              guid
        *         @param resourcegroupguid:          Guid of the resource group to which this machine belongs
        *         @type resourcegroupguid:           guid
        *         @param machinetype:                Machine type.
        *         @type machinetype:                 string
        *         @param template:                   Is template, when template used as example for an machine
        *         @type template:                    bool
        *         @param boot:                       Flag indicating that this machine must be automatically started when rebooting the parent machine
        *         @type boot:                        bool
        *         @param customsettings:             Custom settings and configuration of machine, is XML, to be used freely
        *         @type customsettings:              string
        *         @param backup:                     Indicates if the machine should be included in the backup policies.
        *         @type backup:                      boolean
        *         @param backuplabel:                Backuplabel of the machine.
        *         @type backuplabel:                 string
        *         @param consistent:                 Indicates if consitent backups are taken.
        *         @type consistent:                  boolean
        *         @param isbackup:                   Indicates if the machine is a backup.
        *         @type isbackup:                    boolean
        *         
        *         @param ipaddress:                  ipaddress of the machine.
        *         @type ipaddress:                   string
        *         @param machinerole:                role of the machine.
        *         @type machinerole:                 string       
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with an array of machine guids as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function find (name:String="",assetid:String="",alias:String="",description:String="",macaddress:String="",hostname:String="",status:String="",hypervisor:String="",defaultgateway:String="",agentguid:String="",deviceguid:String="",parentmachineguid:String="",osguid:String="",clouduserguid:String="",ownerguid:String="",cloudspaceguid:String="",resourcegroupguid:String="",machinetype:String="",template:Object=null,boot:Object=null,customsettings:String="",backup:Boolean=false,backuplabel:String="",consistent:Boolean=false,isbackup:Boolean=false,ipaddress:String="",machinerole:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,assetid,alias,description,macaddress,hostname,status,hypervisor,defaultgateway,agentguid,deviceguid,parentmachineguid,osguid,clouduserguid,ownerguid,cloudspaceguid,resourcegroupguid,machinetype,template,boot,customsettings,backup,backuplabel,consistent,isbackup,ipaddress,machinerole,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATEFROMTEMPLATE:String = 'createFromTemplate_response';
        /**
        *         Creates a new machine based on a template, template defined as machine identified by templatemachineguid.
        *         @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:             guid
        *         @param templatemachineguid:        guid of the machine this machine will be based on.
        *         @type  templatemachineguid:        guid
        *         @param name:                       Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                        string
        *         @param languids:                   Array of lan guids. For each lan a nic will be created with an ip in the specified lan.
        *         @type languids:                    array
        *         @param description:                Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                 string
        *         
        *         @param parentmachineguid:          guid of the machine this machine will be created upon.
        *         @type  parentmachineguid:          guid
        *         
        *         @param defaultgateway:             Default gateway of the machine (can be of a private/public lan)
        *         @type defaultgateway:              string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function createFromTemplate (cloudspaceguid:String,templatemachineguid:String,name:String,languids:Array=null,description:String="",parentmachineguid:String="",defaultgateway:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'createFromTemplate', createFromTemplate_ResultReceived, getError, cloudspaceguid,templatemachineguid,name,languids,description,parentmachineguid,defaultgateway,jobguid,executionparams);

        }

        private function createFromTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATEFROMTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_PAUSE:String = 'pause_response';
        /**
        *         Pauses a machine.
        *         @param machineguid:                guid of the machine to pause.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function pause (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'pause', pause_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function pause_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_PAUSE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXPORTMACHINETEMPLATES:String = 'exportMachineTemplates_response';
        /**
        *         Exports template machines to the SystemNAS
        *        
        *         @params templates         list of template of dict containing machine guids and destination URI
        *         @type template            list
        *          
        *         @param jobguid:           Guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         
        */
        public function exportMachineTemplates (templates:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exportMachineTemplates', exportMachineTemplates_ResultReceived, getError, templates,jobguid,executionparams);

        }

        private function exportMachineTemplates_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXPORTMACHINETEMPLATES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ROLLBACK:String = 'rollback_response';
        /**
        *         Rolls a machine back to a given machine snapshot.
        *         @param machineguid:                guid of the machine to rollback.
        *         @type  machineguid:                guid
        *         @param snapshotmachineguid:        guid of the machine snapshot to rollback to.
        *         @type  snapshotmachineguid:        guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function rollback (machineguid:String,snapshotmachineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'rollback', rollback_ResultReceived, getError, machineguid,snapshotmachineguid,jobguid,executionparams);

        }

        private function rollback_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ROLLBACK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMONITOR:String = 'updateMonitor_response';
        /**
        *         Update monitor configuration of the specified machine
        *         
        *         @param machineguid:           Guid of the machine
        *         @type machineguid:            guid
        *         
        *         @param order:                 Order of the monitor [0-7]
        *         @type order:                  integer
        *         
        *         @param name:                  Name of the monitor
        *         @type name:                   string
        *         
        *         @param width:                 monitor width
        *         @type width:                  integer
        *         
        *         @param height:                monitor height
        *         @type height:                 integer
        *         
        *         @param bpp:                   bits per pixel of the monitor
        *         @type bpp:                    integer
        *         
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with result and jobguid: {'result': boolean, 'jobguid': guid} 
        *         @rtype:                       dict
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function updateMonitor (machineguid:String,order:Number,name:String="",width:Number=0,height:Number=0,bpp:Number=0,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateMonitor', updateMonitor_ResultReceived, getError, machineguid,order,name,width,height,bpp,jobguid,executionparams);

        }

        private function updateMonitor_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMONITOR, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_STOP:String = 'stop_response';
        /**
        *         Stops a machine.
        *         @param machineguid:                guid of the machine to stop.
        *         @type  machineguid:                guid
        *         
        *         @param clean:                      soft shutdown if true else power off
        *         @type clean:                       boolean
        *         
        *         @param timeout:                    time (in seconds) to wait for the machine to stop 
        *         @type timeout:                     int
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function stop (machineguid:String,clean:Boolean=true,timeout:Number=900,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'stop', stop_ResultReceived, getError, machineguid,clean,timeout,jobguid,executionparams);

        }

        private function stop_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_STOP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESIZECPU:String = 'resizeCPU_response';
        /**
        *         for vmachine resize cpu
        *         when pmachine certain maintenance actions will happen to make sure machine is initialized to be used in cloud
        *         Updates the memory of a machine.
        *         @param machineguid:                guid of the machine to rollback.
        *         @type  machineguid:                guid
        *         @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided. Not updated if empty.
        *         @type nrcpu:                       int
        *         @param cpufrequency:               CPU frequency in MHz. Not updated if empty.
        *         @type cpufrequency:                int
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function resizeCPU (machineguid:String,nrcpu:Number=1,cpufrequency:Number=0,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'resizeCPU', resizeCPU_ResultReceived, getError, machineguid,nrcpu,cpufrequency,jobguid,executionparams);

        }

        private function resizeCPU_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESIZECPU, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETSNAPSHOTRETENTIONPOLICY:String = 'setSnapshotRetentionPolicy_response';
        /**
        *         Sets the snapshot retention policy for machine
        *         @param machineguid:                guid of the machine to set retention policy.
        *         @type machineguid:                 guid
        *         
        *         @param policyguid:                 guid of the retention policy to set
        *         @type policyguid:                  guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function setSnapshotRetentionPolicy (machineguid:String,policyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setSnapshotRetentionPolicy', setSnapshotRetentionPolicy_ResultReceived, getError, machineguid,policyguid,jobguid,executionparams);

        }

        private function setSnapshotRetentionPolicy_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETSNAPSHOTRETENTIONPOLICY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETVIDEOMODE:String = 'setVideoMode_response';
        /**
        *         Gets the video mode for a machine controlled by its hypervisor.
        *         
        *         @param machineguid:           guid of the physical machine
        *         @type machineguid:            guid
        *         
        *         @param order:                 Number of the monitor [0-7]
        *         @type order:                  integer
        *         
        *         @param xres:                  horizontal resolution
        *         @type xres:                   int
        *         
        *         @param yres:                  vertical resolution
        *         @type yres:                   int
        *         
        *         @param bpp:                   bits per pixel
        *         @type bpp:                    int
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with jobguid and result True/False
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function setVideoMode (machineguid:String,order:Number,xres:Number,yres:Number,bpp:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setVideoMode', setVideoMode_ResultReceived, getError, machineguid,order,xres,yres,bpp,jobguid,executionparams);

        }

        private function setVideoMode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETVIDEOMODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the machine rootobject.
        *         @execution_method = sync
        *         
        *         @param machineguid:             guid of the machine rootobject
        *         @type machineguid:              guid
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the machine
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETROLE:String = 'getRole_response';
        /**
        *         Retrieves the role for a machine. Possible roles are CPUNODE, STORAGENODE, COMBINEDNODE
        *         @execution_method = sync
        *         
        *         @param machineguid:                  guid of the machine rootobject
        *         @type machineguid:                   guid
        *         @param jobguid:                      guid of the job if available else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with machine role as result and jobguid: {'result': string, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        *         @security administrators
        *         
        */
        public function getRole (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getRole', getRole_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getRole_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETROLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAPPLIANCEAGENT:String = 'getApplianceAgent_response';
        /**
        *         Retrieves the Agent GUID for the Appliance.
        *         @execution_method = sync
        *         
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with Appliance machine.agentguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function getApplianceAgent (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getApplianceAgent', getApplianceAgent_ResultReceived, getError, jobguid,executionparams);

        }

        private function getApplianceAgent_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAPPLIANCEAGENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXPORTTOURI:String = 'exportToURI_response';
        /**
        *         Exports a machine to a given URI.
        *         Export is set of vdi's in a given directory (no metadata is being stored).
        *         @param machineguid:                guid of the machine to export.
        *         @type  machineguid:                guid
        *         @param destinationuri:             URI of the location where export should be stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/)
        *         @type destinationuri:              string
        *         @param executormachineguid:        guid of the machine which should export the machine. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:         guid
        *         @param compressed:                 If True, the machine export will be compressed using 7zip compression
        *         @type compressed:                  boolean
        *         @param diskimagetype:              Type of the disk image format (VDI, RAW, VMDK, ...)
        *         @type diskimagetype:               string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function exportToURI (machineguid:String,destinationuri:String,executormachineguid:String="",compressed:Boolean=true,diskimagetype:String="vdi",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exportToURI', exportToURI_ResultReceived, getError, machineguid,destinationuri,executormachineguid,compressed,diskimagetype,jobguid,executionparams);

        }

        private function exportToURI_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXPORTTOURI, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List the machines in a cloud space.
        *         @execution_method = sync
        *         
        *         @param spaceguid:            guid of the space.
        *         @type spaceguid:             guid
        *         @param machinetype:          type of the machine
        *         @type machinetype:           string
        *         @param hypervisor:           hypervisor of the machine
        *         @param hypervisor:           string
        *         @param machineguid:          guid of the machine.
        *         @type machineguid:           guid   
        *         
        *         @param machinerole:          Role of the machine.
        *         @type machinerole:           string       
        *                 
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'MyWebServer',
        *         @note:                                          'description': 'My Personal Web Server',
        *         @note:                                          'status': 'RUNNING',
        *         @note:                                          'machinetype': 'VIRTUALSERVER',
        *         @note:                                          'backup': True,
        *         @note:                                          'os': 'LINUX',
        *         @note:                                          'hostname': 'web001',
        *         @note:                                          'memory': 4096,
        *         @note:                                          'nrcpu': 2,
        *         @note:                                          'isbackup': False,
        *         @note:                                          'template': False,
        *         @note:                                          'importancefactor': 3},
        *         @note:                                        { 'machineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'MyDbServer',
        *         @note:                                          'description': 'My Personal DB Server',
        *         @note:                                          'status': 'RUNNING',
        *         @note:                                          'machinetype': 'VIRTUALSERVER',
        *         @note:                                          'backup': True,
        *         @note:                                          'os': 'LINUX',
        *         @note:                                          'hostname': 'db001',
        *         @note:                                          'memory': 4096,
        *         @note:                                          'nrcpu': 4,
        *         @note:                                          'isbackup': True,
        *         @note:                                          'template': False,
        *         @note:                                          'importancefactor': 2}]}
        *         
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function list (spaceguid:Object=null,machinetype:Object=null,hypervisor:Object=null,machineguid:Object=null,machinerole:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, spaceguid,machinetype,hypervisor,machineguid,machinerole,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ISCSIUNEXPOSE:String = 'iscsiUnexpose_response';
        /**
        *         Unexposes a machine using iSCSI
        *         @param machineguid:                guid of the machine to set retention policy.
        *         @type machineguid:                 guid
        *         
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function iscsiUnexpose (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'iscsiUnexpose', iscsiUnexpose_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function iscsiUnexpose_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ISCSIUNEXPOSE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTVDCS:String = 'listVdcs_response';
        /**
        *         List the vdcs the machine is used in.
        *         @execution_method = sync
        *         
        *         @param machineguid:          guid of the machine to list the vdc's for.
        *         @type  machineguid:          guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listVdcs (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listVdcs', listVdcs_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listVdcs_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTVDCS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXISTS:String = 'exists_response';
        /**
        *         @param name:                  Name of the machine (exact match)
        *         @type name:                   string
        *         
        *         @param assetid:               Asset id of the machine (exact match)
        *         @type assetid:                string
        *         
        *         @param cloudspaceguid:        Guid of the cloudspace
        *         @type cloudspaceguid:         guid        
        *            
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid} 
        *         @rtype:                       list
        *         
        *         @raise e:                     In case an error occurred, exception is raised       
        *         
        */
        public function exists (name:String="",assetid:String="",cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exists', exists_ResultReceived, getError, name,assetid,cloudspaceguid,jobguid,executionparams);

        }

        private function exists_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXISTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIDEOMODE:String = 'getVideoMode_response';
        /**
        *         Gets the video mode for a machine controlled by its hypervisor
        *         
        *         @param machineguid:           guid of the physical machine
        *         @type machineguid:            guid
        *         
        *         @param order:                 Number of the monitor [0-7]
        *         @type order:                  integer
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with jobguid and result a dict = { xres : , yres: , bpp : } 
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function getVideoMode (machineguid:String,order:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVideoMode', getVideoMode_ResultReceived, getError, machineguid,order,jobguid,executionparams);

        }

        private function getVideoMode_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIDEOMODE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_INSTALLDCOS:String = 'installDCOS_response';
        /**
        *         install DCOS on pmachine        
        *         
        *         FLOW
        *         # check is pmachine
        *         #set machine.bootstatus=... to go to install dcos mode
        *         #actor:  Installserver.installDCOS(...
        *         @todo complete
        *         @param jobguid:          Guid of the job
        *         @type jobguid:           guid
        *         @param pmachineguid:     Guid of the physical machine
        *         @type pmachineguid:      guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        */
        public function installDCOS (pmachineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'installDCOS', installDCOS_ResultReceived, getError, pmachineguid,jobguid,executionparams);

        }

        private function installDCOS_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_INSTALLDCOS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCAPACITYCONSUMED:String = 'addCapacityConsumed_response';
        /**
        *         Adds consumed capacity for the machine specified.
        *         @param machineguid:          guid of the customer specified
        *         @type machineguid:           guid
        *         @param amount:               Amount of capacity units to add
        *         @type amount:                integer
        *         @param capacityunittype:     Type of capacity units to add. See ca.capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param name:                 Name of capacity units to add.
        *         @type name:                  string
        *         @param description:          Description of capacity units to add.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function addCapacityConsumed (machineguid:String,amount:Number,capacityunittype:String,name:String="",description:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addCapacityConsumed', addCapacityConsumed_ResultReceived, getError, machineguid,amount,capacityunittype,name,description,jobguid,executionparams);

        }

        private function addCapacityConsumed_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCAPACITYCONSUMED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTEXPORTEDIMAGES:String = 'listExportedImages_response';
        /**
        *         Gets a the list of exported machine images on the systemNAS for a specific machine
        *         @param machineguid:       guid of the machine rootobject
        *         @type machineguid:        guid
        *         @param cloudspaceguid:    guid of the machine rootobject
        *         @type cloudspaceguid:     guid
        *         @param machinetype:       filter on machine type
        *         @type machinetype:        string
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  list of exported images.
        *         @rtype:                   array
        *         @raise e:                 In case an error occurred, exception is raised              
        *         
        */
        public function listExportedImages (machineguid:String,cloudspaceguid:String="",machinetype:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listExportedImages', listExportedImages_ResultReceived, getError, machineguid,cloudspaceguid,machinetype,jobguid,executionparams);

        }

        private function listExportedImages_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTEXPORTEDIMAGES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DISCONNECTFROMHOST:String = 'disconnectFromHost_response';
        /**
        *         Disconnects a machine on the specified host machine.
        *         on specified host
        *         * remove bridges for virtual nics
        *         * disconnect volumes to storage (remove DSS cache data), or make sure vdi's are removed
        *         @security administrator only
        *         @param machineguid:                guid of the machine to connect to the host machine.
        *         @type  machineguid:                guid
        *         @param hostmachineguid:            guid of the host machine to connect to the machine on.
        *         @type  hostmachineguid:            guid
        *         @param leavecacheintact:           If true means cache will not be emptied for e.g. DSS storagesystem
        *         @type leavecacheintact:            boolean
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function disconnectFromHost (machineguid:String,hostmachineguid:String,leavecacheintact:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'disconnectFromHost', disconnectFromHost_ResultReceived, getError, machineguid,hostmachineguid,leavecacheintact,jobguid,executionparams);

        }

        private function disconnectFromHost_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DISCONNECTFROMHOST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDMONITOR:String = 'addMonitor_response';
        /**
        *         Add new monitor configuration to the specified machine
        *         
        *         @param machineguid:           Guid of the machine
        *         @type machineguid:            guid
        *         
        *         @param width:                 monitor width
        *         @type width:                  integer
        *         
        *         @param height:                monitor height
        *         @type height:                 integer
        *         
        *         @param bpp:                   bits per pixel of the monitor
        *         @type bpp:                    integer
        *         
        *         @param order:                 Order of the monitor [1-7]
        *         @type order:                  integer
        *         
        *         @param name:                  Name for the monitor
        *         @type name:                   string
        *         
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with result and jobguid: {'result': boolean, 'jobguid': guid} 
        *         @rtype:                       dict
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function addMonitor (machineguid:String,width:Number,height:Number,bpp:Number,order:Number=0,name:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addMonitor', addMonitor_ResultReceived, getError, machineguid,width,height,bpp,order,name,jobguid,executionparams);

        }

        private function addMonitor_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDMONITOR, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETTIMEZONE:String = 'setTimeZone_response';
        /**
        *         set timezone for a pmachine
        *         
        *         @param machineguid:         machineguid of the pmachine
        *         @type machineguid:          machineguid
        *        
        *         @param timezone:            name of the timezone
        *         @type timezone:             string
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary 
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function setTimeZone (machineguid:Object,timezone:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setTimeZone', setTimeZone_ResultReceived, getError, machineguid,timezone,jobguid,executionparams);

        }

        private function setTimeZone_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETTIMEZONE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSNAPSHOTS:String = 'listSnapshots_response';
        /**
        *         List the snapshots for a given machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:                guid of the machine to list the snapshots from.
        *         @type  machineguid:                guid
        *         
        *         @param timestampfrom:              Filter snapshots from given timestamp 
        *         @type timestampfrom:               datetime
        *         @param timestampuntil:             Filter snapshots until given timestamp
        *         @type timestampuntil:              datetime
        *         
        *         @param includeinconsistent:        Flag to include snapshot machines in inconsistent state (eg snapshots that are being snapshotted asynchronically)
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'parentmachineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'MyWebServer',
        *         @note:                                          'description': 'My Personal Web Server',
        *         @note:                                          'timestampcreated': '2009-09-12 00:00:12',
        *         @note:                                          'consistent': 'False'}]}
        *         
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function listSnapshots (machineguid:Object,includeinconsistent:Object=null,timestampfrom:Object=null,timestampuntil:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listSnapshots', listSnapshots_ResultReceived, getError, machineguid,includeinconsistent,timestampfrom,timestampuntil,jobguid,executionparams);

        }

        private function listSnapshots_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSNAPSHOTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESIZEMEMORY:String = 'resizeMemory_response';
        /**
        *         Updates the memory of a machine.
        *         @param machineguid:                guid of the machine to rollback.
        *         @type  machineguid:                guid
        *         @param memory:                     New value for memory in MB.
        *         @type  memory:                     int
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function resizeMemory (machineguid:String,memory:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'resizeMemory', resizeMemory_ResultReceived, getError, machineguid,memory,jobguid,executionparams);

        }

        private function resizeMemory_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESIZEMEMORY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTACCOUNTS:String = 'listAccounts_response';
        /**
        *         List the accounts of a given machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:                guid of the machine to list the accounts for.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of account info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'login': 'root',
        *         @note:                                          'accounttype': 'SYSTEMACCOUNT'},
        *         @note:                              '         { 'login': 'backup',
        *         @note:                                          'accounttype': 'SYSTEMACCOUNT'},
        *         @note:                              '         { 'login': 'postgres',
        *         @note:                                          'accounttype': 'SYSTEMACCOUNT'}]}
        *         
        */
        public function listAccounts (machineguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAccounts', listAccounts_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listAccounts_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTACCOUNTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTTEMPLATES:String = 'listTemplates_response';
        /**
        *         List the machines templates in a cloud space (of a given machinetype).
        *         @execution_method = sync
        *         
        *         @param spaceguid:                  guid of the space.
        *         @type spaceguid:                   guid
        *         @param machinetype:                Type of the machine (PHYSICAL, VIRTUALSERVER, VIRTUALDESKTOP,VIRTUALSERVER, IMAGEONLY, SMARTCLIENT)
        *         @type machinetype:                 string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @note:                             [{'description': 'Windows XP',
        *         @note:                             'machineguid': 'fbc0c990-d5f8-46f3-b7fe-e412abcc5bee',
        *         @note:                                  'machinetype': 'VIRTUALDESKTOP',
        *         @note:                                  'memory': None,
        *         @note:                                  'name': 'template_virtual_desktop_windowsxp',
        *         @note:                                  'nrcpu': None,
        *         @note:                                  'osdescription': 'Windows XP',
        *         @note:                                  'osguid': '5acdc4d4-12d3-4fc5-8271-78d886f68385',
        *         @note:                                  'osicon': 'windowsxp.png',
        *         @note:                                  'osname': 'windowsxp'},
        *         @note:                                 {'description': 'Windows Vista',
        *         @note:                                  'machineguid': 'a6254007-aa92-4598-887b-7fc48d334cfa',
        *         @note:                                  'machinetype': 'VIRTUALDESKTOP',
        *         @note:                                  'memory': None,
        *         @note:                                  'name': 'template_virtual_desktop_windowsvista',
        *         @note:                                  'nrcpu': None,
        *         @note:                                 'osdescription': 'Windows Vista',
        *         @note:                                  'osguid': 'f3ea862e-52f9-4704-9574-4bbac31d9e7e',
        *         @note:                                  'osicon': 'windowsvista.png',
        *         @note:                                  'osname': 'windowsvista'}]}
        *         
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function listTemplates (spaceguid:Object=null,machinetype:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listTemplates', listTemplates_ResultReceived, getError, spaceguid,machinetype,jobguid,executionparams);

        }

        private function listTemplates_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTTEMPLATES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REBOOT:String = 'reboot_response';
        /**
        *         Reboots a machine.
        *         @param machineguid:                guid of the machine to reboot.
        *         @type  machineguid:                guid
        *         @param clean:                      soft reboot if true else hard reboot
        *         @type clean:                       boolean
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function reboot (machineguid:String,clean:Boolean=true,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'reboot', reboot_ResultReceived, getError, machineguid,clean,jobguid,executionparams);

        }

        private function reboot_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REBOOT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESUME:String = 'resume_response';
        /**
        *         Resumes a machine.
        *         @param machineguid:                guid of the machine to resume.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function resume (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'resume', resume_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function resume_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESUME, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTBACKUPS:String = 'listBackups_response';
        /**
        *         List the backups for a given machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:                guid of the machine to list the backups from.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of backup machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'parentmachineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'MyWebServer',
        *         @note:                                          'description': 'My Personal Web Server',
        *         @note:                                          'backuplabel': 'DAILY-2009-09-12',
        *         @note:                                          'timestampcreated': '2009-09-12 00:00:12',
        *         @note:                                          'consistent': 'True'}]}
        *         
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function listBackups (machineguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listBackups', listBackups_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listBackups_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTBACKUPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDTEMPDISK:String = 'addTempDisk_response';
        /**
        *         Creates a new temp disk for a machine.
        *         @param machineguid:                guid of the machine to create a new data disk for.
        *         @type  machineguid:                guid
        *         @param size:                       Size of disk in MB
        *         @type size:                        int
        *         @param name:                       Name of the temp disk.
        *         @type name:                        string
        *         
        *         @param role:                       Role of the temp disk. ('TEMP' OR 'SSDTEMP')
        *         @type role:                        string
        *         @param retentionpolicyguid:        Policy to be used for retention of snapshots
        *         @type retentionpolicyguid:         guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addTempDisk (machineguid:String,size:Number,name:String="",role:String="TEMP",retentionpolicyguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addTempDisk', addTempDisk_ResultReceived, getError, machineguid,size,name,role,retentionpolicyguid,jobguid,executionparams);

        }

        private function addTempDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDTEMPDISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_INITIALIZE:String = 'initialize_response';
        /**
        *         Initializes a machine based on the model.
        *         @param machineguid:                guid of the machine to initialize.
        *         @type machineguid:                 guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @security administrators
        *         check is indeed a pmachine
        *         #will make sure appropriate applications are installed & configured (the agent and basic qbase is always installed)
        *         #will make sure that the backplanes get configured on the pmachine
        *         ... @todo check what more
        *         
        */
        public function initialize (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'initialize', initialize_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function initialize_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_INITIALIZE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCUSTOMERGUID:String = 'getCustomerGuid_response';
        /**
        *         Returns the customer related to the machine
        *         @execution_method = sync
        *         
        *         @param machineguid:       guid of the machine rootobject
        *         @type machineguid:        guid
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  guid of the customer
        *         @rtype:                   guid
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function getCustomerGuid (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getCustomerGuid', getCustomerGuid_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getCustomerGuid_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCUSTOMERGUID, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the machine rootobject structure.
        *         @execution_method = sync
        *         
        *         @param machineguid:             guid of the machine rootobject
        *         @type machineguid:              guid
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the machine structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REGISTERAGENT:String = 'registerAgent_response';
        /**
        *         Initializes a machine based on the model.
        *         @param macaddress:               MAC address of the machine on which to register a new agent.
        *         @type macaddress:                string
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @note:                           Example return value
        *         @note:                           {"result": "{"agentguid": "C149425F-16AE-451E-A439-0DE7D1EE86F6",
        *                                                       "xmppserver": "172.23.23.254",
        *                                                       "password": "12345",
        *                                                       "agentcontrollerguid": "EDFA459E-1A24-4F98-98CB-C995D2973B3D"}",
        *                                           "jobguid": "8D763680-ED8A-463F-AA25-EBF3EA7A1894"}"
        *         @raise e:                        In case an error occurred, exception is raised
        *         @security administrators
        *         
        */
        public function registerAgent (macaddress:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'registerAgent', registerAgent_ResultReceived, getError, macaddress,jobguid,executionparams);

        }

        private function registerAgent_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REGISTERAGENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_IMPORTMACHINETEMPLATES:String = 'importMachineTemplates_response';
        /**
        *         Imports machines from the SystemNAS and converts them into templates
        *        
        *         @params templates         [ { name : Uri } ]
        *         @type template            list
        *         
        *         @param cloudspaceguid:    guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:    guid
        *  
        *         @param jobguid:           Guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary        
        *         
        */
        public function importMachineTemplates (templates:Object=null,cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'importMachineTemplates', importMachineTemplates_ResultReceived, getError, templates,cloudspaceguid,jobguid,executionparams);

        }

        private function importMachineTemplates_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_IMPORTMACHINETEMPLATES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the machine rootobject.
        *         @execution_method = sync
        *         
        *         @param machineguid:       guid of the machine rootobject
        *         @type machineguid:        guid
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @return:                  YAML representation of the machine
        *         @rtype:                   string
        *         
        */
        public function getYAML (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEDATADISK:String = 'removeDataDisk_response';
        /**
        *         Removes a data disk from a machine.
        *         @param machineguid:                guid of the machine to create a remove the data disk from.
        *         @type  machineguid:                guid
        *         @param diskguid:                   guid of the disk to remove.
        *         @type diskguid:                    guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function removeDataDisk (machineguid:String,diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeDataDisk', removeDataDisk_ResultReceived, getError, machineguid,diskguid,jobguid,executionparams);

        }

        private function removeDataDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEDATADISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEIPADDRESS:String = 'removeIpaddress_response';
        /**
        *         Removes an ipaddress from a NIC on a machine.
        *         @param machineguid:                guid of the machine to remove the ipaddress from.
        *         @type  machineguid:                guid
        *         @param macaddress:                 MAC address of the NIC to remove ipaddress from.
        *         @param macaddress:                 string
        *         @param ipaddress:                  Ipaddress to remove from the NIC.
        *         @type ipaddress:                   string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function removeIpaddress (machineguid:String,macaddress:Object,ipaddress:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeIpaddress', removeIpaddress_ResultReceived, getError, machineguid,macaddress,ipaddress,jobguid,executionparams);

        }

        private function removeIpaddress_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEIPADDRESS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CANCONNECTTEMPDISKS:String = 'canConnectTempdisks_response';
        /**
        *         Checks if there is enough available storage for a vmachine
        *                         
        *         @param machineguid:           guid of the vmachine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      true if there is space enough
        *         @rtype:                       boolean
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function canConnectTempdisks (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'canConnectTempdisks', canConnectTempdisks_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function canConnectTempdisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CANCONNECTTEMPDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETMANAGEMENTIPADDRESS:String = 'getManagementIpaddress_response';
        /**
        *         Retrieve the management ipaddress of the given machine
        *         @execution_method = sync
        *         
        *         @param machineguid:                  guid of the machine rootobject
        *         @type machineguid:                   guid
        *         
        *         @param includevirtual:               whether to include VIPA
        *         @type includevirtual:                boolean
        *         @param jobguid:                      guid of the job if available else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with ipaddress as result and jobguid: {'result': '172.17.11.19', 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function getManagementIpaddress (machineguid:String,includevirtual:Boolean=true,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getManagementIpaddress', getManagementIpaddress_ResultReceived, getError, machineguid,includevirtual,jobguid,executionparams);

        }

        private function getManagementIpaddress_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETMANAGEMENTIPADDRESS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCONFIGURATIONSTRING:String = 'getConfigurationString_response';
        /**
        *         Generate the configuration string for the given machine
        *         @param machineguid:           guid of the machine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      string with configuration data
        *         @rtype:                       string
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function getConfigurationString (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getConfigurationString', getConfigurationString_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getConfigurationString_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCONFIGURATIONSTRING, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETDISKSEQUENCES:String = 'getDiskSequences_response';
        /**
        *         Returns the disksequence as they will be attached to the hypervisor
        *         @param machineguid:           guid of the machine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with sorted array of disks info as result and jobguid: {'result': array, 'jobguid': guid} 
        *         @rtype:                       list
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function getDiskSequences (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getDiskSequences', getDiskSequences_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getDiskSequences_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETDISKSEQUENCES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETACCOUNTPASSWORD:String = 'setAccountPassword_response';
        /**
        *         Updates the password of a machine account.
        *         @param machineguid:                guid of the machine to update account for.
        *         @type  machineguid:                guid
        *         @param accounttype:                Type of account to update (PUBLICACCOUNT, SYSTEMACCOUNT).
        *         @type accounttype:                 string
        *         @param login:                      Account login to update password for.
        *         @type login:                       string
        *         @param currentpassword:            Account's current password.
        *         @type currentpassword:             string
        *         @param newpassword:                Account's new p.
        *         @type newpassword:                 string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function setAccountPassword (machineguid:String,accounttype:String,login:String,currentpassword:String,newpassword:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setAccountPassword', setAccountPassword_ResultReceived, getError, machineguid,accounttype,login,currentpassword,newpassword,jobguid,executionparams);

        }

        private function setAccountPassword_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETACCOUNTPASSWORD, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTMONITORS:String = 'listMonitors_response';
        /**
        *         Returns list of all available monitors of the specified machine
        *         
        *         @param machineguid:           Guid of the machine
        *         @type machineguid:            guid
        *         
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with list of monitor configuration and jobguid: {'result': list, 'jobguid': guid} 
        *         @rtype:                       dict
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function listMonitors (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listMonitors', listMonitors_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listMonitors_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTMONITORS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CONNECTTONETWORKSERVICE:String = 'connectToNetworkService_response';
        /**
        *         Connect to given networkservice of given machine
        *         @param machineguid:        guid of the machine rootobject
        *         @type machineguid:         guid
        *         @param networkservicename: name of the networkservice to connect to
        *         @type networkservicename:  string
        *         
        *         @param agentguid:          guid of the agent which want to connect to KVM
        *         @type agentguid:           guid
        *         @param jobguid:            guid of the job if available else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with Trueas result and jobguid: {'result':True, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function connectToNetworkService (machineguid:String,networkservicename:String,agentguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'connectToNetworkService', connectToNetworkService_ResultReceived, getError, machineguid,networkservicename,agentguid,jobguid,executionparams);

        }

        private function connectToNetworkService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CONNECTTONETWORKSERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTIPADDRESSES:String = 'listIpaddresses_response';
        /**
        *         Retrieve the ipaddress of the given machine
        *         @execution_method = sync
        *         
        *         @param machineguid:                  guid of the machine rootobject
        *         @type machineguid:                   guid
        *         
        *         @param publicflag:                   flag to filter on public or private
        *         @type publicflag:                    boolean
        *         @param jobguid:                      guid of the job if available else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with ipaddress as result and jobguid: {'result': '172.17.11.19', 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function listIpaddresses (machineguid:String,publicflag:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listIpaddresses', listIpaddresses_ResultReceived, getError, machineguid,publicflag,jobguid,executionparams);

        }

        private function listIpaddresses_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTIPADDRESSES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVENIC:String = 'removeNic_response';
        /**
        *         Removes a NIC from a machine.
        *         @param machineguid:                guid of the machine to remove the NIC from.
        *         @type  machineguid:                guid
        *         @param macaddress:                 MAC address of the NIC to remove.
        *         @param macaddress:                 string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function removeNic (machineguid:String,macaddress:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeNic', removeNic_ResultReceived, getError, machineguid,macaddress,jobguid,executionparams);

        }

        private function removeNic_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVENIC, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REPLACE:String = 'replace_response';
        /**
        *         Replaces an exisiting pmachine on an unmanaged device
        *         @param machineguid:                guid of the machine to initialize.
        *         @type machineguid:                 guid
        *         
        *         @param deviceguid:                 guid of the unmanaged machine to initialize.
        *         @type deviceguid:                  guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @security administrators
        *         
        */
        public function replace (machineguid:String,deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'replace', replace_ResultReceived, getError, machineguid,deviceguid,jobguid,executionparams);

        }

        private function replace_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REPLACE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDACCOUNT:String = 'addAccount_response';
        /**
        *         Adds an account for a machine.
        *         @param machineguid:                guid of the machine to add an account to.
        *         @type  machineguid:                guid
        *         @param accounttype:                Type of account to add (PUBLICACCOUNT, SYSTEMACCOUNT).
        *         @type accounttype:                 string
        *         @param login:                      Account login.
        *         @type login:                       string
        *         @param password:                   Account password.
        *         @type password:                    string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addAccount (machineguid:String,accounttype:String,login:String,password:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addAccount', addAccount_ResultReceived, getError, machineguid,accounttype,login,password,jobguid,executionparams);

        }

        private function addAccount_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDACCOUNT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REACTIVATE:String = 'reactivate_response';
        /**
        *         Reactivate physical machine (e.g. after reboot/failure, restart volumes)
        *         @param machineguid:           guid of the physical machine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function reactivate (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'reactivate', reactivate_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function reactivate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REACTIVATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CHECKAGENT:String = 'checkAgent_response';
        /**
        *         Checks whether for the agent is still running on given machine
        *         @param machineguid:           guid of the machine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      string with configuration data
        *         @rtype:                       string
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function checkAgent (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'checkAgent', checkAgent_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function checkAgent_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CHECKAGENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new machine based on a template, but allows you to overrule capacity properties of the machine.
        *         
        *         @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:             guid
        *         
        *         @param name:                       Name of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                        string
        *         
        *         @param machinetype:                machinetype of the machine. IMAGEONLY|SMARTCLIENT|VIRTUALDESKTOP|PHYSICAL|SNAPSHOT|VIRTUALSERVER.
        *         @type machinetype:                 string
        *         
        *         @param status:                     status of the machine. CONFIGURED|IMAGEONLY|RUNNING|TODELETE|DELETING|OVERLOADED|STARTING|HALTED|PAUSED|STOPPING
        *         @type status:                      string
        *         
        *         @param bootstatus:                 bootstatus of the machine. FROMDISK|RECOVERY|INSTALL
        *         @type bootstatus:                  string
        *         
        *         @param assetid:                    Unique name of the machine. (Can be used as external reference by the user)
        *         @type assetid:                     string
        *         
        *         @param memory:                     Memory for the machine in MB. Same as template if not provided.
        *         @type memory:                      int
        *         
        *         @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        *         @type memoryminimal:               int
        *         
        *         @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        *         @type nrcpu:                       int
        *         
        *         @param cpufrequency:               CPU frequency in MHz.
        *         @type cpufrequency:                int
        *         
        *         @param description:                Description of the machine. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type description:                 string
        *         
        *         @param parentmachineguid:          guid of the physical machine this machine will be created upon.
        *         @type  parentmachineguid:          guid
        *         
        *         @param networkinfo:                network information [ { languid, ip , iptype } ]
        *         @type networkinfo:                 dictionary
        *         
        *         @param diskinfo:                   disk information {nr_disks: , info { diskguid, size, role,name,description} }
        *         @type diskinfo:                    dictionary
        *         
        *         @param machinerole:                machinerole of the machine. 
        *         @type machinerole:                 string
        *         
        *         @param hypervisor:                 hypervisor of the machine. 
        *         @type hypervisor:                  string
        *         
        *         @param osguid:                     osguid of the machine.
        *         @type  osguid:                     guid
        *         
        *         @param deviceguid:                 deviceguid of the machine.
        *         @type  deviceguid:                 guid
        *         
        *         @param hostname:                   hostname of the machine
        *         @type hostname:                    string
        *         
        *         @param importancefactor:           importancefactor of the machine
        *         @type importancefactor:            int
        *         
        *         @param backup:                     whether to backup the machine
        *         @type backup:                      boolean
        *         
        *         @param boot:                       whether to boot the machine when pmachine starts
        *         @type boot:                        boolean
        *         
        *         @param alias:                      alias of the machine
        *         @type alias:                       string
        *         
        *         @param customerapplications:       list of applicationguids that runs on the machine
        *         @type customerapplications:        list
        *         
        *         @param defaultgateway:             default gateway of the machine (can be of a private/public lan)
        *         @type defaultgateway:              string
        *         
        *         @param monitors:                   monitors configuration (widthxheightxbpp) ['1024x768x32','800x600x24']
        *         @type monitors:                    list
        *         
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function create (cloudspaceguid:String,name:String,machinetype:String="PHYSICAL",status:String="CONFIGURED",bootstatus:String="FROMDISK",assetid:String="",memory:Number=0,memoryminimal:Number=0,nrcpu:Number=1,cpufrequency:Number=0,description:String="",parentmachineguid:String="",networkinfo:Object=null,diskinfo:Object=null,machinerole:String="",hypervisor:String="",osguid:String="",deviceguid:String="",hostname:String="",importancefactor:Number=0,backup:Boolean=false,boot:Boolean=false,alias:String="",customerapplications:Object=null,defaultgateway:String="",monitors:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, cloudspaceguid,name,machinetype,status,bootstatus,assetid,memory,memoryminimal,nrcpu,cpufrequency,description,parentmachineguid,networkinfo,diskinfo,machinerole,hypervisor,osguid,deviceguid,hostname,importancefactor,backup,boot,alias,customerapplications,defaultgateway,monitors,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXECUTEQSHELLSCRIPT:String = 'executeQshellScript_response';
        /**
        *         Execute a Q-Shell script on a pmachine.
        *         @security administrator only
        *         
        *         @param machineguid:                guid of the pmachine to execute the script on
        *         @type  machineguid:                guid
        *         @param qshellscriptcontent:        Content of the script to execute.
        *         @type  qshellscriptcontent:        string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function executeQshellScript (machineguid:String,qshellscriptcontent:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'executeQshellScript', executeQshellScript_ResultReceived, getError, machineguid,qshellscriptcontent,jobguid,executionparams);

        }

        private function executeQshellScript_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXECUTEQSHELLSCRIPT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_START:String = 'start_response';
        /**
        *         Starts a machine.
        *         @param machineguid:                guid of the machine to start.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function start (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'start', start_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function start_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_START, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAVAILABLETEMPDISKSIZE:String = 'getAvailableTempdiskSize_response';
        /**
        *         Gets the available temp disk size left on the node where  machineguid is situated
        *                         
        *         @param machineguid:           guid of the machine
        *         @type machineguid:            guid
        *         
        *         @param role:                  TEMP or SSDTEMP
        *         @type role:                   string
        *         
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      the available space on SSD
        *         @rtype:                       int
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function getAvailableTempdiskSize (machineguid:String,role:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAvailableTempdiskSize', getAvailableTempdiskSize_ResultReceived, getError, machineguid,role,jobguid,executionparams);

        }

        private function getAvailableTempdiskSize_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAVAILABLETEMPDISKSIZE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATENIC:String = 'updateNic_response';
        /**
        *         Update a NIC of the machine.
        *         @param machineguid:                guid of the machine to update the NIC to.
        *         @type  machineguid:                guid
        *         @param macaddress:                 MAC address of the NIC.
        *         @param macaddress:                 string
        *         
        *         @param order:                      Order of NIC.
        *         @type order:                       int
        *         
        *         @param nictype:                    Type of the NIC. L{core.machine.nic}
        *         @type nictype:                     string
        *         
        *         @param nicstatustype:              Status type of the NIC. (ACTIVE | BROKEN | DISABLED | NOTCONNECTED)
        *         @param nicstatustype:              string
        *         
        *         @param ipaddresses:                Array of new IP addresses configured for this NIC. (only adding new ipaddresses)
        *         @type ipaddresses:                 array
        *         
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function updateNic (machineguid:String,macaddress:Object,order:Number,nictype:String="",nicstatustype:Object=null,ipaddresses:Array=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateNic', updateNic_ResultReceived, getError, machineguid,macaddress,order,nictype,nicstatustype,ipaddresses,jobguid,executionparams);

        }

        private function updateNic_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATENIC, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDDATADISK:String = 'addDataDisk_response';
        /**
        *         Creates a new data disk for a machine.
        *         @param machineguid:                guid of the machine to create a new data disk for.
        *         @type  machineguid:                guid
        *         @param size:                       Size of disk in MB
        *         @type size:                        int
        *         @param retentionpolicyguid:        Guid of the retention policy
        *         @type retentionpolicyguid:         guid
        *         @param name:                       Name of the data disk.
        *         @type name:                        string
        *         @param description:                Description of the datadisk
        *         @type description:                 string
        *         @param disksafetytype:             Type of disk safety (SSO,MIRRORCLOUD...)
        *         @type disksafetytype:              string
        *         
        *         @param jobguid:                    Guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addDataDisk (machineguid:String,size:Number,retentionpolicyguid:String,name:String="",description:String="",disksafetytype:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addDataDisk', addDataDisk_ResultReceived, getError, machineguid,size,retentionpolicyguid,name,description,disksafetytype,jobguid,executionparams);

        }

        private function addDataDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDDATADISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTCUSTOMERAPPLICATIONS:String = 'listCustomerApplications_response';
        /**
        *         Returns the Customer applications for a machine in a cloudspace when defined
        *         @param machineguid:           Guid of the machine
        *         @type machineguid:            guid
        *         
        *         @param cloudspaceguid:        Guid of the cloudspace to filter on
        *         @type cloudspaceguid:         guid
        *         
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with array of application info as result and jobguid: {'result': array, 'jobguid': guid} 
        *         @rtype:                       list
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function listCustomerApplications (machineguid:String="",cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listCustomerApplications', listCustomerApplications_ResultReceived, getError, machineguid,cloudspaceguid,jobguid,executionparams);

        }

        private function listCustomerApplications_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCUSTOMERAPPLICATIONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDIPADDRESS:String = 'addIpaddress_response';
        /**
        *         Adds an ipaddress to a NIC on a machine.
        *         @param machineguid:                guid of the machine to add the ipaddress to.
        *         @type  machineguid:                guid
        *         @param macaddress:                 MAC address of the NIC to add ipaddress to.
        *         @param macaddress:                 string
        *         @param languid:                    guid of the lan to from which the ipaddress is part of.
        *         @type  languid:                    guid
        *         @param ipaddress:                  Ipaddress part of the lan to assign to the NIC. If not specified, an available ip will be selected from the lan.
        *         @type ipaddress:                   string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addIpaddress (machineguid:String,macaddress:Object,languid:String,ipaddress:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addIpaddress', addIpaddress_ResultReceived, getError, machineguid,macaddress,languid,ipaddress,jobguid,executionparams);

        }

        private function addIpaddress_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDIPADDRESS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_COPY:String = 'copy_response';
        /**
        *         Same as clone, but all blocks on disks will be copied instead of cloned.
        *         
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function copy (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'copy', copy_ResultReceived, getError, jobguid,executionparams);

        }

        private function copy_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_COPY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CONNECTTOHOST:String = 'connectToHost_response';
        /**
        *         Connects a machine on a specified host machine.
        *         on specified host
        *         * create bridges or virtual nics
        *         * connect volumes to storage, or make sure vdi's are available
        *         * when failover=True then the move of machine is forced and to always succeed
        *         
        *         @security administrator only
        *         @param machineguid:                guid of the machine to connect to the host machine.
        *         @type  machineguid:                guid
        *         @param hostmachineguid:            guid of the pmachine hosting the vmachine.
        *         @type  hostmachineguid:            guid
        *         
        *         @param failover:                   flags whether failover workflow needs to be followed
        *         @type  failover:                   boolean
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function connectToHost (machineguid:String,hostmachineguid:String,failover:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'connectToHost', connectToHost_ResultReceived, getError, machineguid,hostmachineguid,failover,jobguid,executionparams);

        }

        private function connectToHost_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CONNECTTOHOST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTDISKS:String = 'listDisks_response';
        /**
        *         List the disks for a given machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:          guid of the machine to list the backups from.
        *         @type  machineguid:          guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of disks info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listDisks (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listDisks', listDisks_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESTARTAGENT:String = 'restartAgent_response';
        /**
        *         Restarts the agent if it is not running on given machine
        *         @param machineguid:           guid of the machine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      string with configuration data
        *         @rtype:                       string
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function restartAgent (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'restartAgent', restartAgent_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function restartAgent_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESTARTAGENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes a machine.
        *         @param machineguid:                guid of the machine to delete.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function deleteMachine (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteMachine', delete_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETMACHINEAGENT:String = 'getMachineAgent_response';
        /**
        *         Retrieves the Agent GUID for a machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:      guid of the machine rootobject
        *         @type machineguid:       guid
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with Appliance machine.agentguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function getMachineAgent (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getMachineAgent', getMachineAgent_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getMachineAgent_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETMACHINEAGENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CANROLLBACK:String = 'canRollback_response';
        /**
        *         Checks whether a snaphot machine can be rolledback
        *         @param machineguid:           guid of the snapshotted machine
        *         @type machineguid:            guid
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      True or False 
        *         @rtype:                       boolean
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function canRollback (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'canRollback', canRollback_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function canRollback_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CANROLLBACK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:    guid of the machine rootobject
        *         @type rootobjectguid:     guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  rootobject
        *         @rtype:                   string
        *         @warning:                 Only usable using the python client.
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




        public const EVENTTYPE_GETPARENTMACHINE:String = 'getParentMachine_response';
        /**
        *         Returns the ancestor/parent machine related to the machine (based upon the optional machinetype parameter)
        *         @execution_method = sync
        *         
        *         @param machineguid:       guid of the machine rootobject
        *         @type machineguid:        guid
        *         
        *         @param machinetype:       machinetype of the machine. IMAGEONLY|SMARTCLIENT|VIRTUALDESKTOP|PHYSICAL|SNAPSHOT|VIRTUALSERVER.
        *         @type machinetype:        string
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  guid of parent machine
        *         @rtype:                   guid
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function getParentMachine (machineguid:String,machinetype:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getParentMachine', getParentMachine_ResultReceived, getError, machineguid,machinetype,jobguid,executionparams);

        }

        private function getParentMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETPARENTMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETROLE:String = 'setRole_response';
        /**
        *         Retrieves the role for a machine.
        *         @param machineguid:                  guid of the machine rootobject
        *         @type machineguid:                   guid
        *         @param machinerole:                  Role of the machine. Possible roles are CPUNODE, STORAGENODE, COMBINEDNODE
        *         @type machinerole:                   string
        *         @param jobguid:                      guid of the job if available else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with machine role as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        *         @security administrators
        *         
        */
        public function setRole (machineguid:String,machinerole:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setRole', setRole_ResultReceived, getError, machineguid,machinerole,jobguid,executionparams);

        }

        private function setRole_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETROLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDISOIMAGE:String = 'addISOImage_response';
        /**
        *         Creates a new ISO image for a machine.
        *         @param machineguid:                guid of the machine to create a new ISO image for.
        *         @type  machineguid:                guid
        *         
        *         @param sourceuri:                  Uri for the iso image
        *         @type sourceuri:                   string
        *         @param name:                       Name of the temp disk.
        *         @type name:                        string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function addISOImage (machineguid:String,sourceuri:String,name:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addISOImage', addISOImage_ResultReceived, getError, machineguid,sourceuri,name,jobguid,executionparams);

        }

        private function addISOImage_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDISOIMAGE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CHANGEGATEWAY:String = 'changeGateway_response';
        /**
        *         Change the default gateway of a machine.
        *         
        *         @param machineguid:             guid of the machine on which we will change the default gateway.
        *         @type machineguid:              guid
        *         
        *         @param defaultgateway:          default gateway of the machine
        *         @type defaultgateway:           string
        *         
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         
        *         @return:                        number of maximum allowed ip addresses
        *         @rtype:                         integer
        *         
        *         @raise e: In case an error occurred, exception is raised
        *         
        */
        public function changeGateway (machineguid:String,defaultgateway:String="",jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'changeGateway', changeGateway_ResultReceived, getError, machineguid,defaultgateway,jobguid,executionparams);

        }

        private function changeGateway_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CHANGEGATEWAY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVECAPACITYPROVIDED:String = 'removeCapacityProvided_response';
        /**
        *         Removes provided capacity for the machine specified.
        *         @param machineguid:          guid of the machine specified
        *         @type machineguid:           guid
        *         @param capacityunittype:     Type of capacity units to remove. See ca.capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function removeCapacityProvided (machineguid:String,capacityunittype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeCapacityProvided', removeCapacityProvided_ResultReceived, getError, machineguid,capacityunittype,jobguid,executionparams);

        }

        private function removeCapacityProvided_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECAPACITYPROVIDED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ISCSIEXPOSE:String = 'iscsiExpose_response';
        /**
        *         Exposes a machine using iSCSI (except for its tempdisks)
        *         @param machineguid:             Guid of the machine to expose over ISCSI.
        *         @type machineguid:              guid
        *         @param username:                Username that is allowed to connect
        *         @type username:                 string
        *         @param targetIQN:               iSCSI Qualified Name representing the iscsi target
        *         @type targetIQN:                string
        *         
        *         @param password:                Password of user that is allowed to connect
        *         @type password:                 string
        *         
        *         @param initiatorIQN:            iSCSI Qualified Name allowed to connect
        *         @type initiatorIQN:             string
        *         
        *         @param ipaddress:               ip address allowed to connect to the iscsi target
        *         @type ipaddress:                string
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with a dictionary with list of ipaddress and iqn of the ISCSI exposed disk as result and jobguid: {'result': {'diskguid': guid, 'ipaddress': ip, 'iqn': iqn}, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function iscsiExpose (machineguid:String,targetIQN:String="",username:String="",password:String="",initiatorIQN:String="",ipaddress:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'iscsiExpose', iscsiExpose_ResultReceived, getError, machineguid,targetIQN,username,password,initiatorIQN,ipaddress,jobguid,executionparams);

        }

        private function iscsiExpose_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ISCSIEXPOSE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVETOCLOUDSPACE:String = 'moveToCloudspace_response';
        /**
        *         Moves a machine from one cloud space to another.
        *         @param machineguid:                guid of the machine to move.
        *         @type  machineguid:                guid
        *         @param cloudspaceguid:             guid of the cloud space to move the machine to.
        *         @type  cloudspaceguid:             guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function moveToCloudspace (machineguid:String,cloudspaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveToCloudspace', moveToCloudspace_ResultReceived, getError, machineguid,cloudspaceguid,jobguid,executionparams);

        }

        private function moveToCloudspace_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVETOCLOUDSPACE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_BOOTFROMDISKCONFIGURE:String = 'bootFromDiskConfigure_response';
        /**
        *         make sure pmachine boots from disk next time it is restarted
        *         when vmachine: use normal memory properties
        *         
        *         FLOW
        *         # check is pmachine
        *         # set machine.bootstatus=... to boot from disk
        *         #todo complete
        *         
        *         @param jobguid:          Guid of the job
        *         @type jobguid:           guid
        *         @param pmachineguid:     Guid of the physical machine
        *         @type pmachineguid:      guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        */
        public function bootFromDiskConfigure (machineguid:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'bootFromDiskConfigure', bootFromDiskConfigure_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function bootFromDiskConfigure_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_BOOTFROMDISKCONFIGURE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REFRESHSTATUS:String = 'refreshStatus_response';
        /**
        *         Gets the rootobject.
        *         @param machineguid:      guid of the machine rootobject
        *         @type machineguid:       guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 rootobject
        *         @rtype:                  string
        *         @warning:                Only usable using the python client.
        *         
        */
        public function refreshStatus (machineguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'refreshStatus', refreshStatus_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function refreshStatus_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REFRESHSTATUS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CONNECTTOKVM:String = 'connectToKvm_response';
        /**
        *         Connect to Kvm of given machine
        *         @param machineguid:       guid of the machine rootobject
        *         @type machineguid:        guid
        *         
        *         @param agentguid:         guid of the agent which want to connect to KVM
        *         @type agentguid:          guid
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with Trueas result and jobguid: {'result':True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function connectToKvm (machineguid:String,agentguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'connectToKvm', connectToKvm_ResultReceived, getError, machineguid,agentguid,jobguid,executionparams);

        }

        private function connectToKvm_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CONNECTTOKVM, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @param machineguid:                guid of the machine specified
        *         @type machineguid:                 guid
        *         @param name:                       Name of the machine.
        *         @type name:                        string
        *         @param description:                Description for this machine
        *         @type description:                 string
        *         @param cloudspaceguid:             guid of the space to which this machine belongs
        *         @type cloudspaceguid:              guid
        *         @param machinetype:                Machine type.
        *         @type machinetype:                 string
        *         @param osguid:                     guid of the OS.
        *         @type osguid:                      guid
        *         @param assetid:                    Asset ID.
        *         @type assetid:                     string
        *         @param alias:                      Alias of the machine.
        *         @type alias:                       string
        *         @param template:                   is template, when template used as example for an machine
        *         @type template:                    bool
        *         @param hostname:                   Hostname of the machine.
        *         @type hostname:                    string
        *         @param nrcpu:                      Number of CPUs for the machine. Same as template if not provided.
        *         @type nrcpu:                       int
        *         @param cpufrequency:               CPU frequency in MHz.
        *         @type cpufrequency:                int
        *         @param memory:                     Memory for the machine in MB. Same as template if not provided.
        *         @type memory:                      int
        *         @param memoryminimal:              Minumum amount of memory required for the machine in MB. Same as template if not provided.
        *         @type memoryminimal:               int
        *         @param importancefactor:           an integer which defines how important a machine is, std=5, when having a disaster this will define order of recovery (nr between 0 & 10, 10 being most important e.g. 10 means this is the most important machine, 0 means no importance=will always be last)
        *         @type importancefactor:            int
        *         @param lastrealitycheck:           date and time of last check on the machine
        *         @type lastrealitycheck:            datetime
        *         @param deviceguid:                 guid of the parent device
        *         @type deviceguid:                  guid
        *         @param boot:                       flag indicating that this machine must be automatically started when rebooting the parent machine
        *         @type boot:                        bool
        *         @param customsettings:             custom settings and configuration of machine, is XML, to be used freely
        *         @type customsettings:              string
        *         @param defaultgateway:             default gateway ip addr
        *         @type defaultgateway:              ipaddress
        *         @param status:                     status of the machine   CONFIGURED|IMAGEONLY|HALTED|RUNNING|OVERLOADED|PAUSED|TODELETE|STOPPING|STARTING|DELETING
        *         @type status:                      string
        *         @param clouduserguid:              guid of the clouduser, owning this machine
        *         @type clouduserguid:               guid
        *         @param parentmachineguid:          guid of the parent machine
        *         @type parentmachineguid:           guid
        *         @param hypervisor:                 Hypervisor of the machine.
        *         @type hypervisor:                  string
        *         @param agentguid:                  guid of the agent.
        *         @type agentguid:                   guid
        *         @param ownerguid:                  guid of the owner.
        *         @type ownerguid:                   guid
        *         @param defaultgateway:             Default gateway
        *         @type defaultgateway:              ipaddress
        *         @param deviceguid:                 guid of the device.
        *         @type deviceguid:                  guid
        *         @param hostname:                   Hostname of the machine.
        *         @type hostname:                    string
        *         @param hypervisor:                 Hypervisor of the machine.
        *         @type hypervisor:                  string
        *         @param backup:                     Indicates if the machine should be included in the backup policies.
        *         @type backup:                      boolean
        *         @param isbackup:                   Indicates if the machine is a backup.
        *         @type isbackup:                    boolean
        *         @param backuplabel:                Backuplabel of the machine.
        *         @type backuplabel:                 string
        *         
        *         @param timestamp:                  Timestamp of creation date in reality
        *         @type timestamp:                   datetime
        *         
        *         @param bootstatus:                 Machine boot status (INSTALL|FROMDISK|RECOVERY)
        *         @type bootstatus:                  string
        *         
        *         @param monitors:                   monitors configuration (widthxheightxbpp) ['1024x768x32','800x600x24']
        *         @type monitors:                    list
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (machineguid:String,name:String="",description:String="",cloudspaceguid:String="",machinetype:String="",osguid:String="",assetid:String="",alias:String="",template:Object=null,hostname:String="",nrcpu:Number=0,cpufrequency:Number=0,memory:Number=0,memoryminimal:Number=0,importancefactor:Number=0,lastrealitycheck:String="",deviceguid:String="",boot:Object=null,customsettings:String="",defaultgateway:String="",status:String="",clouduserguid:String="",parentmachineguid:String="",hypervisor:String="",accounts:Object=null,capacityunitsconsumed:Object=null,capacityunitsprovided:Object=null,nics:Object=null,resourcegroupguid:Object=null,agentguid:String="",ownerguid:String="",backup:Boolean=true,backuplabel:String="",consistent:Object=null,isbackup:Boolean=false,iconname:Object=null,timestamp:String="",bootstatus:String="",monitors:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, machineguid,name,description,cloudspaceguid,machinetype,osguid,assetid,alias,template,hostname,nrcpu,cpufrequency,memory,memoryminimal,importancefactor,lastrealitycheck,deviceguid,boot,customsettings,defaultgateway,status,clouduserguid,parentmachineguid,hypervisor,accounts,capacityunitsconsumed,capacityunitsprovided,nics,resourcegroupguid,agentguid,ownerguid,backup,backuplabel,consistent,isbackup,iconname,timestamp,bootstatus,monitors,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MAKETEMPLATE:String = 'makeTemplate_response';
        /**
        *         Create template from a machine.
        *         @param machineguid:                guid of the machine to create template from.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function makeTemplate (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'makeTemplate', makeTemplate_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function makeTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MAKETEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SNAPSHOT:String = 'snapshot_response';
        /**
        *         Creates a snapshot of a machine.
        *         means
        *         - backup metadata of machine 
        *         - pause machine (When snapshottype = PAUSED)
        *         - snapshot all disks of machine if not async
        *         - resume machine (When snapshottype = PAUSED)
        *         @param machineguid:                guid of the machine to snapshot.
        *         @type  machineguid:                guid
        *         
        *         @param label:                      label for the snapshot
        *         @type label:                       string
        *         
        *         @param description:                description for the snapshot
        *         @type description:                 string
        *         
        *         @param automated:                  Flags whether the snapshot is being taken scheduled or manually (is used for retention of snapshots)
        *         @type automated:                   boolean
        *         
        *         @param async:                      Flags whether the snapshot will be taken asynchronically afterwards (by calling the sso.snapshotmachine method)
        *         @type async:                       boolean
        *         
        *         @param snapshottype:               type of the snapshot (REGULAR, PAUSED, VSS, CSBA)
        *         @type snapshottype:                string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with snapshot machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function snapshot (machineguid:Object,label:Object=null,description:Object=null,automated:Object=null,async:Object=null,snapshottype:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'snapshot', snapshot_ResultReceived, getError, machineguid,label,description,automated,async,snapshottype,jobguid,executionparams);

        }

        private function snapshot_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SNAPSHOT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDNIC:String = 'addNic_response';
        /**
        *         Adds a NIC to the machine.
        *         @param machineguid:                guid of the machine to add the NIC to.
        *         @type  machineguid:                guid
        *         @param nictype:                    Type of the NIC. L{core.machine.nic}
        *         @type nictype:                     string
        *         @param order:                      Order of NIC. Next available if not specified.
        *         @type order:                       int
        *         @param macaddress:                 MAC address of the NIC. Generated if not provided.
        *         @param macaddress:                 string
        *         @param ipaddresses:                Array of IP addresses configured for this NIC.
        *         @type ipaddresses:                 array
        *         @param nicstatustype:              Status type of the NIC. (ACTIVE | BROKEN | DISABLED | NOTCONNECTED)
        *         @param nicstatustype:              string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function addNic (machineguid:String,nictype:String,order:Number=0,macaddress:Object=null,ipaddresses:Array=null,nicstatustype:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addNic', addNic_ResultReceived, getError, machineguid,nictype,order,macaddress,ipaddresses,nicstatustype,jobguid,executionparams);

        }

        private function addNic_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDNIC, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETPUBLICIPADDRESS:String = 'getPublicIpaddress_response';
        /**
        *         Retrieve the public ipaddress of the given machine
        *         @execution_method = sync
        *         
        *         @param machineguid:                  guid of the machine rootobject
        *         @type machineguid:                   guid
        *         @param includevirtual:               whether to include VIPA
        *         @type includevirtual:                boolean
        *         @param jobguid:                      guid of the job if available else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with ipaddress as result and jobguid: {'result': '172.17.11.19', 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function getPublicIpaddress (machineguid:String,includevirtual:Boolean=true,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getPublicIpaddress', getPublicIpaddress_ResultReceived, getError, machineguid,includevirtual,jobguid,executionparams);

        }

        private function getPublicIpaddress_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETPUBLICIPADDRESS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CLONE:String = 'clone_response';
        /**
        *         clone existing machine into defined space and into defined destinationVDC
        *         if space=="" then in same space
        *         if destinationVDC=="" then same VDC (maintenanceMode is not possible then)
        *         @param copyNetworkInfo if False: do not copy network info
        *         if in same space:
        *         ---------------
        *         * all rootobject properties will be copied over appart from
        *         ** new guid's
        *         ** the machine.name = original + <timestamp>
        *         * For the network lan's, the machine stays connected to the same LAN's but new ip addresses are looked for on those LAN's
        *         if in different space
        *         ------------------
        *         * all rootobject properties will be copied over
        *         * new network LAN's are created with as name $originalLanName_clone_<timestamp> 
        *         * the ip addresses are 100% the same as the original ip addresses
        *         * for the private LAN's: the VLAN's are ALL NEW!!! There is always 100% separation between spaces for private LAN's
        *         * for the public LAN's: the machine's stay connected to the same LAN's but new ip addresses are looked for on those LAN's
        *         if maintenanceMode==True
        *         ----------------------
        *         * then all LAN's will get a different vlan tag
        *         * new network LAN's are created with as name $originalLanName_clone_<timestamp>
        *         * the ip addresses are 100% the same as the original ip addresses
        *         cloning means the blocks on the disks are not copied, only the changes are remembered
        *         recovery mode is only possible if copied to a maintenance VDC
        *         @param machineguid:                guid of the machine to clone.
        *         @type  machineguid:                guid
        *         @param cloudspaceguid:             guid of cloud space to create the machine in. Same cloud space if not provided.
        *         @type  cloudspaceguid:             guid
        *         @param vdcguid:                    guid of the VDC to create the machine in. Same VDC if not specified, in that case maintenanceMode is always False.
        *         @type  vdcguid:                    guid
        *         @param copynetworkinfo:            If True, all networking info will be copied as well. Private networks will be created in new Vlans, public networks are not created, but the machine will receive an ip in the same public lan.
        *         @type copynetworkinfo:             boolean
        *         @note:                             Only possible if cloned to a different VDC and in the same cloud space.
        *         @param maintenancemode:            If True, all networking info will be copied as well, even for public vlans.
        *         @type maintenancemode:             boolean
        *         
        *         @param name:                       name for new clone
        *         @type name:                        string
        *         
        *         @param snapshotguid:               guid of the snapshot to clone from
        *         @type  snapshotguid:               guid
        *         
        *         
        *         @param hostmachineguid:            host for the clone
        *         @type hostmachineguid:             guid
        *         
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machineguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        */
        public function clone (machineguid:String,cloudspaceguid:String,vdcguid:String="",copynetworkinfo:Boolean=true,maintenancemode:Boolean=true,name:String="",snapshotguid:String="None",hostmachineguid:String="None",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'clone', clone_ResultReceived, getError, machineguid,cloudspaceguid,vdcguid,copynetworkinfo,maintenancemode,name,snapshotguid,hostmachineguid,jobguid,executionparams);

        }

        private function clone_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CLONE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEACCOUNT:String = 'removeAccount_response';
        /**
        *         Removes an account from a machine.
        *         @param machineguid:                guid of the machine to remove an account from.
        *         @type  machineguid:                guid
        *         @param accounttype:                Type of account to remove (PUBLICACCOUNT, SYSTEMACCOUNT).
        *         @type accounttype:                 string
        *         @param login:                      Account login.
        *         @type login:                       string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function removeAccount (machineguid:String,accounttype:String,login:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeAccount', removeAccount_ResultReceived, getError, machineguid,accounttype,login,jobguid,executionparams);

        }

        private function removeAccount_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEACCOUNT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DISABLE:String = 'disable_response';
        /**
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function disable (machineguid:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'disable', disable_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function disable_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DISABLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_IMPORTFROMURI:String = 'importFromURI_response';
        /**
        *         Import a machine from a given URI.
        *         Machine object in drp needs to be created first.
        *         @param machineguid:                guid of the machine to import to.
        *         @type  machineguid:                guid
        *         @param sourceuri:                  URI of the location where the export is stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/)
        *         @type sourceuri:                   string
        *         @param executormachineguid:        guid of the machine which should import the export. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:         guid
        *         @param compressed:                 Should be True if the machine export is compressed using 7zip compression
        *         @type compressed:                  boolean
        *         @param diskimagetype:              Type of the disk image format used (VDI, RAW, VMDK, ...)
        *         @type diskimagetype:               string
        *         @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:             guid
        *         @param clouduserguid:              guid of the related clouduser
        *         @type clouduserguid:               guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function importFromURI (machineguid:String,sourceuri:String,executormachineguid:String="",compressed:Boolean=true,diskimagetype:String="vdi",cloudspaceguid:String="",clouduserguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'importFromURI', importFromURI_ResultReceived, getError, machineguid,sourceuri,executormachineguid,compressed,diskimagetype,cloudspaceguid,clouduserguid,jobguid,executionparams);

        }

        private function importFromURI_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_IMPORTFROMURI, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDFLOPPYIMAGE:String = 'addFloppyImage_response';
        /**
        *         Creates a new floppy image for a machine.
        *         @param machineguid:                guid of the machine to create a new floppy disk for.
        *         @type  machineguid:                guid
        *         @param sourceuri:                  Uri for the iso image
        *         @type sourceuri:                   string
        *         @param name:                       Name of the temp disk.
        *         @type name:                        string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function addFloppyImage (machineguid:String,sourceuri:String,name:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addFloppyImage', addFloppyImage_ResultReceived, getError, machineguid,sourceuri,name,jobguid,executionparams);

        }

        private function addFloppyImage_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDFLOPPYIMAGE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVECAPACITYCONSUMED:String = 'removeCapacityConsumed_response';
        /**
        *         Removes consumed capacity for the machine specified.
        *         @param machineguid:          guid of the customer specified
        *         @type machineguid:           guid
        *         @param capacityunittype:     Type of capacity units to remove. See ca.capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *          
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function removeCapacityConsumed (machineguid:String,capacityunittype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeCapacityConsumed', removeCapacityConsumed_ResultReceived, getError, machineguid,capacityunittype,jobguid,executionparams);

        }

        private function removeCapacityConsumed_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECAPACITYCONSUMED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DETACHFROMDEVICE:String = 'detachFromDevice_response';
        /**
        *         Unforces a machine to run on a particular device.
        *         (will use resourcegroups underneath)
        *         @param machineguid:                guid of the machine to attach to a device.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function detachFromDevice (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'detachFromDevice', detachFromDevice_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function detachFromDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DETACHFROMDEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEMONITOR:String = 'removeMonitor_response';
        /**
        *         Remove the last monitor of the specified machine
        *         (Primary monitor [0] can not be removed)
        *         
        *         @param machineguid:           Guid of the machine
        *         @type machineguid:            guid
        *         
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         
        *         @return:                      dictionary with result and jobguid: {'result': boolean, 'jobguid': guid} 
        *         @rtype:                       dict
        *         
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function removeMonitor (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeMonitor', removeMonitor_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function removeMonitor_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEMONITOR, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXPORTTOSECONDARY:String = 'exportToSecondary_response';
        /**
        *         Creates a backup of a machine.
        *         create a backup of the machine, will result in an exported vdi image (7zipped)
        *         (in case of SSO onto DSS)
        *         also the metadata is being stored
        *         @param machineguid:                guid of the machine to backup.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with backup machineguid as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @todo:                             Will be implemented in phase2
        *         @todo:                             naming
        *         
        */
        public function exportToSecondary (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exportToSecondary', exportToSecondary_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function exportToSecondary_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXPORTTOSECONDARY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTNICS:String = 'listNics_response';
        /**
        *         List the NICs for a given machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:                guid of the machine to list the NICs for.
        *         @type  machineguid:                guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of NIC info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'order': 0,
        *         @note:                                          'macaddress': '0a:00:27:00:00:00',
        *         @note:                                          'status': 'ACTIVE',
        *         @note:                                          'nictype': 'ETHERNET_100MB',
        *         @note:                                          'ipaddresses': [{'ipaddress': '192.168.1.2',
        *         @note:                                                           'netmask': '255.255.255.0',
        *         @note:                                                           'iptype': 'IPV4',
        *         @note:                                                           'lan':{'languid': '22544B07-4129-47B1-8690-B92C0DB21433'
        *         @note:                                                                  'name': 'ManagementLan',
        *         @note:                                                                  'dns': '192.168.1.1',
        *         @note:                                                                  'startip': '192.168.1.1',
        *         @note:                                                                  'endip': '192.168.1.10',
        *         @note:                                                                  'gateway': '192.168.1.254',
        *         @note:                                                                  'network': '192.168.1.0',
        *         @note:                                                                  'storageflag': True,
        *         @note:                                                                  'managementflag': True,
        *         @note:                                                                  'publicflag': False,
        *         @note:                                                                  'vlantag': '0'}},
        *         @note:                                                          {'ipaddress': '192.168.5.2',
        *         @note:                                                           'netmask': '255.255.255.0',
        *         @note:                                                           'iptype': 'IPV4',
        *         @note:                                                           'lan':{'languid': '22544B07-4129-47B1-8690-B92C0DB21435'
        *         @note:                                                                  'name': 'SmartClientLan',
        *         @note:                                                                  'dns': '192.168.1.1',
        *         @note:                                                                  'startip': '192.168.5.1',
        *         @note:                                                                  'endip': '192.168.5.100',
        *         @note:                                                                  'gateway': '192.168.5.1',
        *         @note:                                                                  'network': '192.168.5.0',
        *         @note:                                                                  'storageflag': False,
        *         @note:                                                                  'managementflag': False,
        *         @note:                                                                  'publicflag': True,        
        *         @note:                                                                  'vlantag': '0'}}]},
        *         @note:                                        { 'order': 1,
        *         @note:                                          'macaddress': '0a:00:28:00:00:00',
        *         @note:                                          'status': 'ACTIVE',
        *         @note:                                          'nictype': 'ETHERNET_100MB',
        *         @note:                                          'ipaddresses': [{'ipaddress': 10.100.32.12',
        *         @note:                                                           'netmask': '255.255.255.0',
        *         @note:                                                           'iptype': 'IPV4',
        *         @note:                                                           'lan':{'languid': '22544B07-4129-47B1-8690-B92C0DB21436'
        *         @note:                                                                  'name': 'PublicLan',
        *         @note:                                                                  'dns': '10.100.0.1',
        *         @note:                                                                  'startip': '10.100.32.10',
        *         @note:                                                                  'endip': '10.100.32.254',
        *         @note:                                                                  'gateway': '10.100.32.254',
        *         @note:                                                                  'network': '10.100.32.0',
        *         @note:                                                                  'vlantag': '0'}}]}]}
        *         
        */
        public function listNics (machineguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listNics', listNics_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listNics_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTNICS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTGUESTMACHINES:String = 'listGuestMachines_response';
        /**
        *         List the guests for a given host machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:                  guid of the host machine to list the guests from.
        *         @type  machineguid:                  guid
        *         @param jobguid:                      guid of the job if available else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @note:                               {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                            'parentmachineguid': '44544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                            'name': 'MyWebServer',
        *         @note:                                            'description': 'My Personal Web Server',
        *         @note:                                            'status': 'RUNNING',
        *         @note:                                            'os': 'windows2003',
        *         @note:                                            'iconname': 'vamchine.ico'}]}
        *         
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function listGuestMachines (machineguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listGuestMachines', listGuestMachines_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listGuestMachines_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTGUESTMACHINES, false, false, e.result));
            srv.disconnect();
        }


    }
}

