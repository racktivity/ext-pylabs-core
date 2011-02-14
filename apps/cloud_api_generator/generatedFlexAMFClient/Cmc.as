
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Cmc extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_cmc';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Cmc()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETROOTPOLICYJOBLIST:String = 'getRootPolicyJobList_response';
        /**
        *         Gets all root policy jobs used as overview in cmc
        *         @execution_method = sync
        *         @param joblimit             number of jobs to display
        *         @type joblimit              int
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getRootPolicyJobList (joblimit:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getRootPolicyJobList', getRootPolicyJobList_ResultReceived, getError, joblimit,jobguid,executionparams);

        }

        private function getRootPolicyJobList_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETROOTPOLICYJOBLIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETROOTMONITORINGJOBLIST:String = 'getRootMonitoringJobList_response';
        /**
        *         Gets all root monitoring jobs used as overview in cmc
        *         @execution_method = sync
        *         @param joblimit             number of jobs to display
        *         @type joblimit              int
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getRootMonitoringJobList (joblimit:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getRootMonitoringJobList', getRootMonitoringJobList_ResultReceived, getError, joblimit,jobguid,executionparams);

        }

        private function getRootMonitoringJobList_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETROOTMONITORINGJOBLIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTAVAILABLETREEITEMS:String = 'listAvailableTreeItems_response';
        /**
        *         @execution_method = sync
        *         
        *         @param jobguid:              Guid of the cloud user
        *         @type jobguid:               guid
        *         
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of tree info (as dict) as result and jobguid
        *         @rtype:                      dictionary
        *         
        */
        public function listAvailableTreeItems (clouduserguid:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAvailableTreeItems', listAvailableTreeItems_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function listAvailableTreeItems_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTAVAILABLETREEITEMS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCHILDAPPLICATIONS:String = 'getChildApplications_response';
        /**
        *         Returns the applicationguid(s) of the instanciated cloudservice
        *         @execution_method = sync
        *         @param parentapplicationguid:   guid of the application
        *         @type parentapplicationguid:    guid
        *         @param jobguid:                 Guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dict
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getChildApplications (parentapplicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getChildApplications', getChildApplications_ResultReceived, getError, parentapplicationguid,jobguid,executionparams);

        }

        private function getChildApplications_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCHILDAPPLICATIONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTMACHINEDISKS:String = 'listMachineDisks_response';
        /**
        *         List the disks for a given machine.
        *         @execution_method = sync
        *         
        *         @param machineguid:          guid of the machine to list the backups from.
        *         @type  machineguid:          guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of disks info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listMachineDisks (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listMachineDisks', listMachineDisks_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listMachineDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTMACHINEDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALDESKTOPOVERVIEW:String = 'getVirtualDesktopOverview_response';
        /**
        *         Gets all details needed to load the virtual desktop overview page in cmc
        *         @execution_method = sync
        *         @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        *         @type cloudspaceGuid:       guid
        * 		@param istemplate:          Boolean indicating if the list returns templates or not
        *         @type istemplate:           Boolean
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getVirtualDesktopOverview (cloudspaceguid:Object,istemplate:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualDesktopOverview', getVirtualDesktopOverview_ResultReceived, getError, cloudspaceguid,istemplate,jobguid,executionparams);

        }

        private function getVirtualDesktopOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALDESKTOPOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTAVAILABLECOMMANDS:String = 'listAvailableCommands_response';
        /**
        *         Returns a list of available commands for the user on a given object of a given type for a given screen.
        *         @execution_method = sync
        *         @param objecttype:          Name of the object type for which you want to list the actions
        *         @type objecttype:           string
        *         @param objectguid:          Guid of the object for which you want to retrieve the action for (for the current user)
        *         @type objectguid:           guid
        *         @param screenname:          Name of the screen for which you want to retrieve the actions for
        *         @type screenname:           string
        *         
        *         @param clouduserguid:       Guid of the user for which you want to retrieve the action for 
        *         @type clouduserguid:        guid
        *         @param cloudspaceguid:      Guid of the cloudspace for which you want to retrieve the action for 
        *         @type cloudspaceguid:       guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dict
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'icon': 'machine_start.ico',
        *         @note:                                      'name': 'machine_start',
        *         @note:                                      'label': 'Start Machine',
        *         @note:                                      'description': 'Start Machine Command',
        *         @note:                                      'parameters': {
        *         @note:                                           'guid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                       }},
        *         @note:                                   {  'icon': 'machine_stop.ico',
        *         @note:                                      'name': 'machine_stop',
        *         @note:                                      'label': 'Stop Machine'
        *         @note:                                      'description': 'Stop Machine Command',,
        *         @note:                                      'parameters': {
        *         @note:                                           'machineguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                       }}]}
        *         
        */
        public function listAvailableCommands (objecttype:Object=null,objectguid:Object=null,screenname:Object=null,clouduserguid:Object=null,cloudspaceguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAvailableCommands', listAvailableCommands_ResultReceived, getError, objecttype,objectguid,screenname,clouduserguid,cloudspaceguid,jobguid,executionparams);

        }

        private function listAvailableCommands_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTAVAILABLECOMMANDS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETROOTJOBSLIST:String = 'getRootJobsList_response';
        /**
        *         Gets all root jobs used as overview in cmc
        *         @execution_method = sync
        *         @param joblimit             number of jobs to display
        *         @type joblimit              int
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getRootJobsList (joblimit:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getRootJobsList', getRootJobsList_ResultReceived, getError, joblimit,jobguid,executionparams);

        }

        private function getRootJobsList_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETROOTJOBSLIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETDASHBOARD:String = 'getDashboard_response';
        /**
        *         Gets all details needed to load the dashboard page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getDashboard (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getDashboard', getDashboard_ResultReceived, getError, jobguid,executionparams);

        }

        private function getDashboard_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETDASHBOARD, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETROOTERRORCONDITIONSLIST:String = 'getRootErrorConditionsList_response';
        /**
        *         Gets all root error conditions used as overview in cmc
        *         @execution_method = sync
        *         @param errorconditionslimit     number of error conditions to display
        *         @type errorconditionslimit      int
        *         @param jobguid:                 Guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         
        */
        public function getRootErrorConditionsList (errorconditionslimit:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getRootErrorConditionsList', getRootErrorConditionsList_ResultReceived, getError, errorconditionslimit,jobguid,executionparams);

        }

        private function getRootErrorConditionsList_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETROOTERRORCONDITIONSLIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETSMARTCLIENTDEVICES:String = 'GetSmartClientDevices_response';
        /**
        *         Gets all SMARTCLIENT devices
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function GetSmartClientDevices (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'GetSmartClientDevices', GetSmartClientDevices_ResultReceived, getError, jobguid,executionparams);

        }

        private function GetSmartClientDevices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETSMARTCLIENTDEVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETPDISKINFO:String = 'getPDiskInfo_response';
        /**
        *         Returns pdisk information
        *         @execution_method = sync
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     path to the generated graph
        *         @type executionparams:      dictionary
        *         @return:                    dict
        *         
        */
        public function getPDiskInfo (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getPDiskInfo', getPDiskInfo_ResultReceived, getError, jobguid,executionparams);

        }

        private function getPDiskInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETPDISKINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETMAINTENANCEENVIROMNENTOVERVIEW:String = 'getMaintenanceEnviromnentOverview_response';
        /**
        *         Gets all details needed to load the maintenance environment overview page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getMaintenanceEnviromnentOverview (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getMaintenanceEnviromnentOverview', getMaintenanceEnviromnentOverview_ResultReceived, getError, jobguid,executionparams);

        }

        private function getMaintenanceEnviromnentOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETMAINTENANCEENVIROMNENTOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCDUDEVICES:String = 'getCDUDevices_response';
        /**
        *         Gets all CDU devices
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getCDUDevices (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getCDUDevices', getCDUDevices_ResultReceived, getError, jobguid,executionparams);

        }

        private function getCDUDevices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCDUDEVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETLOGICALDISKS:String = 'getLogicalDisks_response';
        /**
        *         Get all logical disks for specified pmachine or all physical disks from the environment.
        *         
        *         @execution_method = sync
        *         
        *         @param machineguid:         Guid of the pmachine
        *         @type machineguid:          guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getLogicalDisks (machineguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getLogicalDisks', getLogicalDisks_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getLogicalDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETLOGICALDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETRRDGRAPH:String = 'getRRDGraph_response';
        /**
        *         Returns the path to the generated RRD graph
        *         @execution_method = sync
        *         
        *         @param rrdParams:           Dictionary of all parameters needed to generate the RRD graph
        *         @type rrdParams:            dictionary
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     path to the generated graph
        *         @type executionparams:      dictionary
        *         @return:                    dict
        *         
        */
        public function getRRDGraph (rrdParams:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getRRDGraph', getRRDGraph_ResultReceived, getError, rrdParams,jobguid,executionparams);

        }

        private function getRRDGraph_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETRRDGRAPH, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETACCESSCONTROLLIST:String = 'getAccessControlList_response';
        /**
        *         Returns the access control list for an authenticated clouduser        
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of all access items in CMC
        *         @type executionparams:      dictionary
        *         @return:                    dict
        *         
        */
        public function getAccessControlList (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAccessControlList', getAccessControlList_ResultReceived, getError, jobguid,executionparams);

        }

        private function getAccessControlList_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETACCESSCONTROLLIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTVDISKS:String = 'listVDisks_response';
        /**
        *         Gets all vdisks attached to specified pmachine
        *         @execution_method = sync
        *         @param machineguid:         Guid of the pmachine
        *         @type machineguid:          guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function listVDisks (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listVDisks', listVDisks_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listVDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTVDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETTREEDATA:String = 'getTreeData_response';
        /**
        *         Gets all needed data to build up the cmc tree
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getTreeData (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getTreeData', getTreeData_ResultReceived, getError, jobguid,executionparams);

        }

        private function getTreeData_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETTREEDATA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETLOGGINGINFORMATION:String = 'getLoggingInformation_response';
        /**
        *         Gets all details needed to load the logging page (jobs and events) in cmc
        *         @execution_method = sync
        *         @param joblogguid:          Guid of the job from which to get the logging information
        *         @type joblogguid:           guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getLoggingInformation (joblogguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getLoggingInformation', getLoggingInformation_ResultReceived, getError, joblogguid,jobguid,executionparams);

        }

        private function getLoggingInformation_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETLOGGINGINFORMATION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCOMBINEDNODESOVERVIEW:String = 'getCombinedNodesOverview_response';
        /**
        *         Gets all details needed to load the combined nodes overview page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getCombinedNodesOverview (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getCombinedNodesOverview', getCombinedNodesOverview_ResultReceived, getError, jobguid,executionparams);

        }

        private function getCombinedNodesOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCOMBINEDNODESOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETUSERTREEDATA:String = 'getUserTreeData_response';
        /**
        *         Gets all needed data to build up the cmc user management tree
        *         @execution_method = sync
        *         @param customerguid:        Guid of the customer
        *         @type customerguid:         guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getUserTreeData (customerguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getUserTreeData', getUserTreeData_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function getUserTreeData_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETUSERTREEDATA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETPRODUCTIONENVIROMNENTOVERVIEW:String = 'getProductionEnviromnentOverview_response';
        /**
        *         Gets all details needed to load the production environment overview page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getProductionEnviromnentOverview (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getProductionEnviromnentOverview', getProductionEnviromnentOverview_ResultReceived, getError, jobguid,executionparams);

        }

        private function getProductionEnviromnentOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETPRODUCTIONENVIROMNENTOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETNETWORKOVERVIEW:String = 'getNetworkOverview_response';
        /**
        *         Gets all details needed to load the network overview page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @todo:                      Will be implemented in phase2
        *         
        */
        public function getNetworkOverview (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getNetworkOverview', getNetworkOverview_ResultReceived, getError, jobguid,executionparams);

        }

        private function getNetworkOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETNETWORKOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTAVAILABLEPLUGINS:String = 'listAvailablePlugins_response';
        /**
        *         @execution_method = sync
        *         
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of plugin info (as dict) as result and jobguid
        *         @rtype:                      dictionary
        *         
        */
        public function listAvailablePlugins (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAvailablePlugins', listAvailablePlugins_ResultReceived, getError, jobguid,executionparams);

        }

        private function listAvailablePlugins_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTAVAILABLEPLUGINS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETRESOURCENODESOVERVIEW:String = 'getResourceNodesOverview_response';
        /**
        *         Gets all details needed to load the resource nodes overview page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getResourceNodesOverview (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getResourceNodesOverview', getResourceNodesOverview_ResultReceived, getError, jobguid,executionparams);

        }

        private function getResourceNodesOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETRESOURCENODESOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATECLOUDSERVICEPOSITION:String = 'updateCloudServicePosition_response';
        /**
        *         Updates the coordinates of a cloudservcie in the database
        *         @execution_method = sync
        *         @param vdcguid:             Guid of the vdc
        *         @type vdcguid:              guid
        *         @param cloudserviceguid:    Guid of the cloudservice
        *         @type cloudserviceguid:     guid
        *         @param positionx:           X coordinates of the item in the vdc gui
        *         @type positionx:            int
        *         @param positiony:           Y coordinates of the item in the vdc gui
        *         @type positiony:            int
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function updateCloudServicePosition (vdcguid:String,cloudserviceguid:String,positionx:Number,positiony:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateCloudServicePosition', updateCloudServicePosition_ResultReceived, getError, vdcguid,cloudserviceguid,positionx,positiony,jobguid,executionparams);

        }

        private function updateCloudServicePosition_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATECLOUDSERVICEPOSITION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETDISKMANAGEMENTOVERVIEW:String = 'getDiskManagementOverview_response';
        /**
        *         Returns disk information on virtual disks in SSO
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:      Guid of the cloudspace to filter on
        *         @type cloudspaceguid:       guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     path to the generated graph
        *         @type executionparams:      dictionary
        *         @return:                    dict
        *         
        */
        public function getDiskManagementOverview (cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getDiskManagementOverview', getDiskManagementOverview_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function getDiskManagementOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETDISKMANAGEMENTOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCLOUDSERVICE:String = 'getCloudService_response';
        /**
        *         Returns the applicationguid(s) of the instanciated cloudservice
        *         @execution_method = sync
        *         @param name:                Name of the cloud service template
        *         @type name:                 string
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dict
        *         @todo:                      Will be implemented in phase2
        *         
        */
        public function getCloudService (name:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getCloudService', getCloudService_ResultReceived, getError, name,jobguid,executionparams);

        }

        private function getCloudService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCLOUDSERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETSTORAGENODESOVERVIEW:String = 'getStorageNodesOverview_response';
        /**
        *         Gets all details needed to load the storage nodes overview page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getStorageNodesOverview (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getStorageNodesOverview', getStorageNodesOverview_ResultReceived, getError, jobguid,executionparams);

        }

        private function getStorageNodesOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETSTORAGENODESOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALSERVEROVERVIEW:String = 'getVirtualServerOverview_response';
        /**
        *         Gets all details needed to load the virtual server overview page in cmc
        *         @execution_method = sync
        *         @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        *         @type cloudspaceGuid:       guid
        * 	    @param istemplate:          Boolean indicating if the list returns templates or not
        *         @type istemplate:           Boolean
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getVirtualServerOverview (cloudspaceguid:Object,istemplate:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualServerOverview', getVirtualServerOverview_ResultReceived, getError, cloudspaceguid,istemplate,jobguid,executionparams);

        }

        private function getVirtualServerOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALSERVEROVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETSMARTCLIENTSOVERVIEW:String = 'getSmartclientsOverview_response';
        /**
        *         Gets all details needed to load the smartclients overview page in cmc
        *         @execution_method = sync
        *         @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        *         @type cloudspaceGuid:       guid
        * 		@param istemplate:          Boolean indicating if the list returns templates or not
        *         @type istemplate:           Boolean
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getSmartclientsOverview (cloudspaceguid:Object,istemplate:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getSmartclientsOverview', getSmartclientsOverview_ResultReceived, getError, cloudspaceguid,istemplate,jobguid,executionparams);

        }

        private function getSmartclientsOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETSMARTCLIENTSOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETADMINISTRATIONENVIROMNENTOVERVIEW:String = 'getAdministrationEnviromnentOverview_response';
        /**
        *         Gets all details needed to load the administration environment overview page in cmc
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getAdministrationEnviromnentOverview (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAdministrationEnviromnentOverview', getAdministrationEnviromnentOverview_ResultReceived, getError, jobguid,executionparams);

        }

        private function getAdministrationEnviromnentOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETADMINISTRATIONENVIROMNENTOVERVIEW, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETDEVICES:String = 'getDevices_response';
        /**
        *         Gets all non SMARTCLIENT devices
        *         @execution_method = sync
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getDevices (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getDevices', getDevices_ResultReceived, getError, jobguid,executionparams);

        }

        private function getDevices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETDEVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETMACHINEROOTJOBSLIST:String = 'getMachineRootJobsList_response';
        /**
        *         Gets all root jobs from the specified machine
        *         @execution_method = sync
        *         @param machineguid:         Guid of the machine
        *         @type machineguid:          guid
        *         
        *         @param joblimit             number of jobs to display
        *         @type joblimit              int
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getMachineRootJobsList (machineguid:Object,joblimit:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getMachineRootJobsList', getMachineRootJobsList_ResultReceived, getError, machineguid,joblimit,jobguid,executionparams);

        }

        private function getMachineRootJobsList_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETMACHINEROOTJOBSLIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETMACHINEDETAILS:String = 'getMachineDetails_response';
        /**
        *         Get information about a single machine
        *         
        *         @execution_method = sync
        *         
        *         @param machineguid:         Guid of the machine
        *         @type machineguid:          guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getMachineDetails (machineguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getMachineDetails', getMachineDetails_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getMachineDetails_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETMACHINEDETAILS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETPHYSICALDISKS:String = 'getPhysicalDisks_response';
        /**
        *         Get all physical disks for specified pmachine or all physical disks from the environment.
        *         
        *         @execution_method = sync
        *         
        *         @param machineguid:         Guid of the pmachine
        *         @type machineguid:          guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getPhysicalDisks (machineguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getPhysicalDisks', getPhysicalDisks_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function getPhysicalDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETPHYSICALDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETRAIDDEVICEDETAILS:String = 'getRaidDeviceDetails_response';
        /**
        *         Retrieve RAID device details for specified disk (partition level).
        *         
        *         @execution_method = sync
        *         
        *         @param diskguid:            Guid of the disk
        *         @type diskguid:             guid
        *         
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getRaidDeviceDetails (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getRaidDeviceDetails', getRaidDeviceDetails_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getRaidDeviceDetails_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETRAIDDEVICEDETAILS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVDCTEMPLATES:String = 'getVdcTemplates_response';
        /**
        *         Gets all details needed to load a vdc in cmc
        *         @execution_method = sync
        *         @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        *         @type cloudspaceGuid:       guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         
        */
        public function getVdcTemplates (cloudspaceGuid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVdcTemplates', getVdcTemplates_ResultReceived, getError, cloudspaceGuid,jobguid,executionparams);

        }

        private function getVdcTemplates_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVDCTEMPLATES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETVIRTUALDATACENTEROVERVIEW:String = 'getVirtualDatacenterOverview_response';
        /**
        *         Gets all details needed to load the virtual datacenter overview page in cmc
        *         @execution_method = sync
        *         @param cloudspaceGuid:      Guid of the cloudspace from which to get lans, machines and templates
        *         @type cloudspaceGuid:       guid
        *         @param jobguid:             Guid of the job if available else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @todo:                      Will be implemented in phase2
        *         
        */
        public function getVirtualDatacenterOverview (cloudspaceguid:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getVirtualDatacenterOverview', getVirtualDatacenterOverview_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function getVirtualDatacenterOverview_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETVIRTUALDATACENTEROVERVIEW, false, false, e.result));
            srv.disconnect();
        }


    }
}

