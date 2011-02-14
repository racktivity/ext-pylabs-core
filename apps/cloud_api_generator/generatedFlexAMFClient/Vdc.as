
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Vdc extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_vdc';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Vdc()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_RESTORE:String = 'restore_response';
        /**
        *         @param sourcevdcguid defines which machines need to be restored (all machines in that VDC)
        *         
        *         @param destinationvdcguid is the VDC where will be restored to if not specified will be the original VDC where the backup originated from and machines in that VDC will be overwritten !!!
        *         
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function restore (sourcevdcguid:Object,destinationvdcguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'restore', restore_ResultReceived, getError, sourcevdcguid,destinationvdcguid,jobguid,executionparams);

        }

        private function restore_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESTORE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTCLOUDSERVICES:String = 'listCloudServices_response';
        /**
        *         Returns a list of cloud services for a given VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:          guid of the VDC for which to retrieve the list of cloud services.
        *         @type vdcguid:           guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of dictionaries with applicationguid, applicationname, languid, lanname, machineguid, machinename, positionx, positiony, status and array of connections for each cloud service.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '[{"cloudserviceguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                   "applicationguid": "", "applicationname": "",
        *         @note:                                 "languid":"", "lanname": "",
        *         @note:                                   "machineguid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "machinename": "SQL 2005",
        *         @note:                                   "positionx":"10", "positiony":"10",
        *         @note:                                   "status":"DEPLOYED",
        *         @note:                                   "connections":"E1734C86-AC26-46CA-82C7-216C91B44C8A",
        *         @note:                                   "icon": ""}',
        *         @note:                                 {"cloudserviceguid": "E1734C86-AC26-46CA-82C7-216C91B44C8A",
        *         @note:                                   "applicationguid": "", "applicationname": "",
        *         @note:                                 "languid":"A475F49E-9B98-41B5-AA19-2F69B2393B40", "lanname": "qlan1",
        *         @note:                                   "machineguid": "", "machinename": "",
        *         @note:                                   "positionx":"100", "positiony":"100",
        *         @note:                                   "status":"DEPLOYED",
        *         @note:                                   "connections":['22544B07-4129-47B1-8690-B92C0DB21434'],
        *         @note:                                   "icon": ""}',"}]'
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listCloudServices (vdcguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listCloudServices', listCloudServices_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function listCloudServices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCLOUDSERVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDAPPLICATION:String = 'addApplication_response';
        /**
        *         Adds an application as a cloudservice to the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:          guid of the VDC specified
        *         @type vdcguid:           guid
        *         @param applicationguid:  guid of the application to add to the specified VDC
        *         @type applicationguid:   guid
        *         @param positionx:        X coodinate on the VDC canvas
        *         @type positionx:         int
        *         @param positiony:        Y coodinate on the VDC canvas
        *         @type positiony:         int
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function addApplication (vdcguid:String,applicationguid:String,positionx:Number,positiony:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addApplication', addApplication_ResultReceived, getError, vdcguid,applicationguid,positionx,positiony,jobguid,executionparams);

        }

        private function addApplication_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDAPPLICATION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:    guid of the lan rootobject
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




        public const EVENTTYPE_LISTEXPORTEDIMAGES:String = 'listExportedImages_response';
        /**
        *         Gets a the list of exported vdc images on the systemNAS for a specific vdc
        *         @param vdcguid:           guid of the vdc rootobject
        *         @type vdcguid:            guid
        *         @param cloudspaceguid:    guid of the machine rootobject
        *         @type cloudspaceguid:     guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  list of exported images.
        *         @rtype:                   array
        *         @raise e:                 In case an error occurred, exception is raised              
        *         
        */
        public function listExportedImages (vdcguid:String,cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listExportedImages', listExportedImages_ResultReceived, getError, vdcguid,cloudspaceguid,jobguid,executionparams);

        }

        private function listExportedImages_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTEXPORTEDIMAGES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCONNECTION:String = 'addConnection_response';
        /**
        *         Adds a connection between two cloud services in the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:                     guid of the VDC specified
        *         @type vdcguid:                      guid
        *         @param sourcerootobjectguid:        guid of the source rootobject
        *         @type sourcerootobjectguid:         guid
        *         @param destinationrootobjectguid:   guid of the destination rootobject
        *         @type destinationrootobjectguid:    guid
        *         @param jobguid:                     guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @return:                            dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                           In case an error occurred, exception is raised
        *         
        */
        public function addConnection (vdcguid:String,sourcerootobjectguid:String,destinationrootobjectguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addConnection', addConnection_ResultReceived, getError, vdcguid,sourcerootobjectguid,destinationrootobjectguid,jobguid,executionparams);

        }

        private function addConnection_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCONNECTION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of VDC guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:    guid of the parent cloudspace to include in the search criteria.
        *         @type cloudspaceguid:     guid
        *         @param name:              Name of the VDC to include in the search criteria.
        *         @type name:               string
        *         @param status:            Status of the  VDC to include in the search criteria. See listStatuses().
        *         @type status:             string
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Array of VDC guids which met the find criteria specified.
        *         @rtype:                   array
        *         @note:                    Example return value:
        *         @note:                    {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function find (cloudspaceguid:Object=null,name:Object=null,status:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, cloudspaceguid,name,status,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEMACHINE:String = 'removeMachine_response';
        /**
        *         Removes a machine from the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:         guid of the VDC specified
        *         @type vdcguid:          guid
        *         @param machineguid:     guid of the machine to add to the specified VDC
        *         @type machineguid:      guid
        *         @param jobguid:         guid of the job if available else empty string
        *         @type jobguid:          guid
        *         @param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:  dictionary
        *         @return:                dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                 dictionary
        *         @raise e:               In case an error occurred, exception is raised
        *         
        */
        public function removeMachine (vdcguid:String,machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeMachine', removeMachine_ResultReceived, getError, vdcguid,machineguid,jobguid,executionparams);

        }

        private function removeMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_PAUSE:String = 'pause_response';
        /**
        *         Pauses all machines in VDC
        *         @param vdcguid:          guid of the VDC to specified.
        *         @type vdcguid:           guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function pause (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'pause', pause_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function pause_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_PAUSE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDLAN:String = 'addLan_response';
        /**
        *         Adds a lan as a cloudservice to the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:           guid of the VDC specified
        *         @type vdcguid:            guid
        *         @param languid:           guid of the lan to add to the specified VDC
        *         @type languid:            guid
        *         @param positionx:         X coodinate on the VDC canvas
        *         @type positionx:          int
        *         @param positiony:         Y coodinate on the VDC canvas
        *         @type positiony:          int
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function addLan (vdcguid:String,languid:String,positionx:Number,positiony:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addLan', addLan_ResultReceived, getError, vdcguid,languid,positionx,positiony,jobguid,executionparams);

        }

        private function addLan_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDLAN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new VDC in the space specified
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:        guid of the cloud space specified
        *         @type cloudspaceguid:         guid
        *         @param name:                  Name for this new VDC
        *         @type name:                   string
        *         @param description:           Description for this new VDC
        *         @type description:            string
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with cloud space guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function create (cloudspaceguid:String,name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, cloudspaceguid,name,description,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REBOOT:String = 'reboot_response';
        /**
        *         Reboots all machines in VDC
        *         @param vdcguid:          guid of the VDC to specified.
        *         @type vdcguid:           guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function reboot (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'reboot', reboot_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function reboot_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REBOOT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXECUTEQSHELLSCRIPT:String = 'executeQshellScript_response';
        /**
        *         Execute a Q-Shell script on all machines in VDC.
        *         This function requires a Q-Agent on every machine
        *         
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function executeQshellScript (vdcguid:Object,qshellScriptContent:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'executeQshellScript', executeQshellScript_ResultReceived, getError, vdcguid,qshellScriptContent,jobguid,executionparams);

        }

        private function executeQshellScript_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXECUTEQSHELLSCRIPT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVETOSPACE:String = 'moveToSpace_response';
        /**
        *         Moves the VDC specified to an other space. VDC can only be moved to spaces for which the authenticated user has sufficient rights.
        *         @param vdcguid:          guid of the VDC to move.
        *         @type vdcguid:           guid
        *         @param cloudspaceguid:   guid of the cloud space to which the VDC will be moved.
        *         @type cloudspaceguid:    guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function moveToSpace (vdcguid:String,cloudspaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveToSpace', moveToSpace_ResultReceived, getError, vdcguid,cloudspaceguid,jobguid,executionparams);

        }

        private function moveToSpace_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVETOSPACE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_START:String = 'start_response';
        /**
        *         Starts all machines in VDC
        *         @param vdcguid:          guid of the VDC to specified.
        *         @type vdcguid:           guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function start (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'start', start_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function start_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_START, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @execution_method = sync
        *         
        *         @param vdcguid:          guid of the vdc specified
        *         @type vdcguid:           guid
        *         @param name:             Name for this new VDC
        *         @type name:              string
        *         @param description:      Description for this new VDC
        *         @type description:       string
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with vdc guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (vdcguid:String,name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, vdcguid,name,description,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDMACHINE:String = 'addMachine_response';
        /**
        *         Adds a machine as a cloudservice to the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:         guid of the VDC specified
        *         @type vdcguid:          guid
        *         @param machineguid:     guid of the machine to add to the specified VDC
        *         @type machineguid:      guid
        *         @param positionx:       X coodinate on the VDC canvas
        *         @type positionx:        int
        *         @param positiony:       Y coodinate on the VDC canvas
        *         @type positiony:        int
        *         @param jobguid:         guid of the job if avalailable else empty string
        *         @type jobguid:          guid
        *         @param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:  dictionary
        *         @return:                dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                 dictionary
        *         @raise e:               In case an error occurred, exception is raised
        *         
        */
        public function addMachine (vdcguid:String,machineguid:String,positionx:Number,positiony:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addMachine', addMachine_ResultReceived, getError, vdcguid,machineguid,positionx,positiony,jobguid,executionparams);

        }

        private function addMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ROLLBACK:String = 'rollback_response';
        /**
        *         Rolls back a snapshot for all machines in VDC.
        *         @param vdcguid:          guid of the VDC to specified.
        *         @type vdcguid:           guid
        *         @param backuplabel:      Label of the backupset to use for restore.
        *         @type backuplabel:       string
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function rollback (vdcguid:String,backuplabel:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'rollback', rollback_ResultReceived, getError, vdcguid,backuplabel,jobguid,executionparams);

        }

        private function rollback_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ROLLBACK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESUME:String = 'resume_response';
        /**
        *         Resumes all machines in VDC
        *         @param vdcguid:          guid of the VDC to specified.
        *         @type vdcguid:           guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function resume (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'resume', resume_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function resume_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESUME, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CLONE:String = 'clone_response';
        /**
        *         Create a clone of a complete VDC.
        *         For the machines: cloning means the blocks on the disks are not copied, only the changes are remembered.
        *         @param sourcevdcguid:                 guid of the VDC rootobject
        *         @type sourcevdcguid:                  guid
        *         @param destinationcloudspaceguid:     guid of the VDC rootobject. If not specified, VDC will be cloned in the same space as the source VDC.
        *         @type destinationcloudspaceguid:      guid
        *         @note:                                if in same space:
        *         @note:                                -----------------
        *         @note:                                * all rootobject properties will be copied over apart from
        *         @note:                                ** new guid's
        *         @note:                                ** the machine.name = original + _clone_vX (x being incremental nr)
        *         @note:                                * For the network lan's, the machine's stay connected to the same LAN's but new ip addresses are looked for on those LAN's
        *         @note:                                if in different space
        *         @note:                                ---------------------
        *         @note:                                * all rootobject properties will be copied over
        *         @note:                                * new network LAN's are created with as name $originalLanName_clone_vX X being incremental nr
        *         @note:                                * the ip addresses are 100% the same as the original ip addresses
        *         @note:                                * for the private LAN's: the VLAN's are ALL NEW!!! There is always 100% separation between spaces for private LAN's
        *         @note:                                * for the public LAN's: the machine's stay connected to the same LAN's but new ip addresses are looked for on those LAN's
        *         @param copynetworkinfo:               Boolean value indicating if the network info should be copied. Default is True.
        *         @type copynetworkinfo:                boolean
        *         @param maintenancemode:               Boolean value indicating if cloned VDC should be put in maintenance mode. Default is False.
        *         @type maintenancemode:                boolean
        *         @note:                                 if maintenancemode==True
        *         @note:                                ------------------------
        *         @note:                                * then all LAN's will get a different vlan tag
        *         @note:                                * new network LAN's are created with as name $originalLanName_clone_vX X being incremental nr
        *         @note:                                * the ip addresses are 100% the same as the original ip addresses
        *         @param autostart:                     Boolean value indicating if the machine of the new VDC should start automatically. Default is True.
        *         @type autostart:                      boolean
        *         @param jobguid:                       guid of the job if avalailable else empty string
        *         @type jobguid:                        guid
        *         @param executionparams:               dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:                dictionary
        *         @return:                              dictionary with vdc guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                               dictionary
        *         
        */
        public function clone (sourcevdcguid:String,destinationcloudspaceguid:String="",copynetworkinfo:Boolean=true,maintenancemode:Boolean=false,autostart:Boolean=true,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'clone', clone_ResultReceived, getError, sourcevdcguid,destinationcloudspaceguid,copynetworkinfo,maintenancemode,autostart,jobguid,executionparams);

        }

        private function clone_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CLONE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_STOP:String = 'stop_response';
        /**
        *         Stops all machines in VDC
        *         Leaves storage connections & network bridges intact
        *         @param vdcguid:            guid of the VDC to specified.
        *         @type vdcguid:             guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function stop (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'stop', stop_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function stop_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_STOP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_INITIALIZE:String = 'initialize_response';
        /**
        *         Initializes a vdc based on the model (walk through all cloud services of that vdc and do an initialize).
        *         @param vdcguid:                    guid of the VDC to initialize.
        *         @type vdcguid:                     guid
        *         @param start:                      Start machines after initialize.
        *         @type start:                       boolean
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function initialize (vdcguid:String,start:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'initialize', initialize_ResultReceived, getError, vdcguid,start,jobguid,executionparams);

        }

        private function initialize_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_INITIALIZE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the VDC rootobject.
        *         @execution_method = sync
        *         
        *         @param vdcguid:            guid of the VDC rootobject
        *         @type vdcguid:             guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   XML representation of the VDC
        *         @rtype:                    string
        *         @raise e:                  In case an error occurred, exception is raised
        *         @todo:                     Will be implemented in phase2
        *         
        */
        public function getXML (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_IMPORTFROMURI:String = 'importFromURI_response';
        /**
        *         Imports a VDC from the source location specified.
        *         Export rootobject info
        *         @param vdcguid:                    guid of the VDC to specified.
        *         @type vdcguid:                     guid
        *         @param sourceuri:                  URI of the location holding an exported VDC. (e.g ftp://login:passwd@myhost.com/backups/myvdc/)
        *         @type sourceuri:                   string
        *         @param executormachineguid:        guid of the machine which should convert the disk to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:         guid
        *         @param cloudspaceguid:             guid of the cloudspace this machine is part of.
        *         @type  cloudspaceguid:             guid
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function importFromURI (vdcguid:String,sourceuri:String,executormachineguid:String="",jobguid:String="",cloudspaceguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'importFromURI', importFromURI_ResultReceived, getError, vdcguid,sourceuri,executormachineguid,jobguid,cloudspaceguid,executionparams);

        }

        private function importFromURI_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_IMPORTFROMURI, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_COPY:String = 'copy_response';
        /**
        *         See clone action but this case is copy instead of clone.
        *         
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        *         
        */
        public function copy (sourcevdcguid:Object,destinationcloudspaceguid:Object=null,copynetworkinfo:Object=null,maintenancemode:Object=null,autostart:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'copy', copy_ResultReceived, getError, sourcevdcguid,destinationcloudspaceguid,copynetworkinfo,maintenancemode,autostart,jobguid,executionparams);

        }

        private function copy_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_COPY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVELAN:String = 'removeLan_response';
        /**
        *         Removes a lan from to the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:          guid of the VDC specified
        *         @type vdcguid:           guid
        *         @param languid:          guid of the lan to add to the specified VDC
        *         @type languid:           guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function removeLan (vdcguid:String,languid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeLan', removeLan_ResultReceived, getError, vdcguid,languid,jobguid,executionparams);

        }

        private function removeLan_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVELAN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the VDC rootobject structure.
        *         @execution_method = sync
        *         
        *         @param vdcguid:            guid of the VDC rootobject
        *         @type vdcguid:             guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   XSD representation of the VDC structure.
        *         @rtype:                    string
        *         @raise e:                  In case an error occurred, exception is raised
        *         @todo:                     Will be implemented in phase2
        *         
        */
        public function getXMLSchema (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXPORTTOURI:String = 'exportToURI_response';
        /**
        *         Exports all macine of the VDC specified as vdi image on defined destination.
        *         Export rootobject info
        *         @param vdcguid:              guid of the VDC to specified.
        *         @type vdcguid:               guid
        *         @param destinationuri:       URI of the location where the VDI should be stored. (e.g ftp://login:passwd@myhost.com/backups/myvdc/)
        *         @type destinationuri:        string
        *         @param executormachineguid:  guid of the machine which should convert the disk to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:   guid
        *         @param compressed            Boolean value indicating if all exported machines should be compressed. Compression used is 7zip
        *         @type:                       boolean
        *         @param imagetype             Type of image format to use.
        *         @type imagetype:             string
        *         @note:                       Supported export formats are : "vdi", "parallels", "qcow2", "vvfat", "vpc", "bochs", "dmg", "cloop", "vmdk", "qcow", "cow", "host_device", "raw"
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function exportToURI (vdcguid:String,destinationuri:String,executormachineguid:Object=null,compressed:Object=null,imagetype:String="vdi",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exportToURI', exportToURI_ResultReceived, getError, vdcguid,destinationuri,executormachineguid,compressed,imagetype,jobguid,executionparams);

        }

        private function exportToURI_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXPORTTOURI, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of virtual datacenters (VDCs) for a given cloudspace/vdc.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:   guid of the cloudspace for which to retrieve the list of VDCs.
        *         @type cloudspaceguid:    guid
        *         @param vdcguid:          guid of the vdc
        *         @type vdcguid:           guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of dictionaries with guid, name and status for each VDC.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "vdc1", "status": "DEPLOYED"},
        *         @note:                                {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "name": "vdc2", "status": "DEPLOYING"}]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function list (cloudspaceguid:Object=null,vdcguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, cloudspaceguid,vdcguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the vdc rootobject.
        *         @execution_method = sync
        *         
        *         @param vdcguid:            guid of the vdc rootobject
        *         @type vdcguid:             guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   YAML representation of the vdc
        *         @rtype:                    string
        *         
        */
        public function getYAML (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVECONNECTION:String = 'removeConnection_response';
        /**
        *         Removes a connection between two cloud services in the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:                      guid of the VDC specified
        *         @type vdcguid:                       guid
        *         @param sourcecloudserviceguid:       guid of the cloud service to connect
        *         @type sourcecloudserviceguid:        guid
        *         @param destinationcloudserviceguid:  guid of the cloud service to connect
        *         @type destinationcloudserviceguid:   guid
        *         @param jobguid:                      guid of the job if avalailable else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function removeConnection (vdcguid:String,sourcecloudserviceguid:String,destinationcloudserviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeConnection', removeConnection_ResultReceived, getError, vdcguid,sourcecloudserviceguid,destinationcloudserviceguid,jobguid,executionparams);

        }

        private function removeConnection_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECONNECTION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSTATUSES:String = 'listStatuses_response';
        /**
        *         Returns a list of possible VDC statuses.
        *         @execution_method = sync
        *         
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of statuses.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '["DELETED","DEPLOYED","DEPLOYING","DISABLED","ERROR","MODIFIED"]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listStatuses (jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listStatuses', listStatuses_ResultReceived, getError, jobguid,executionparams);

        }

        private function listStatuses_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSTATUSES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEAPPLICATION:String = 'removeApplication_response';
        /**
        *         Removes an application from to the specified VDC.
        *         @execution_method = sync
        *         
        *         @param vdcguid:          guid of the VDC specified
        *         @type vdcguid:           guid
        *         @param applicationguid:  guid of the application to add to the specified VDC
        *         @type applicationguid:   guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function removeApplication (vdcguid:String,applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeApplication', removeApplication_ResultReceived, getError, vdcguid,applicationguid,jobguid,executionparams);

        }

        private function removeApplication_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEAPPLICATION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SNAPSHOT:String = 'snapshot_response';
        /**
        *         Creates snapshots of all machines in VDC
        *         @param vdcguid:          guid of the VDC to specified.
        *         @type vdcguid:           guid
        *         @param backuplabel:      Label which will be put on all snapshots of all machines of this VDC.
        *         @type backuplabel:       string
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function snapshot (vdcguid:String,backuplabel:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'snapshot', snapshot_ResultReceived, getError, vdcguid,backuplabel,jobguid,executionparams);

        }

        private function snapshot_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SNAPSHOT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCONFIGURATIONSTRING:String = 'getConfigurationString_response';
        /**
        *         Generate the configuration string for the given vdc 
        *         @param vdcguid:           guid of the vdc
        *         @type vdcguid:            guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  string containing configuration data
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function getConfigurationString (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getConfigurationString', getConfigurationString_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function getConfigurationString_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCONFIGURATIONSTRING, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_BACKUP:String = 'backup_response';
        /**
        *         backup all machines in VDC
        *         also backup all metadata to do with VDC (e.g. network info)
        *         
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function backup (vdcguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'backup', backup_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function backup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_BACKUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the VDC specified.
        *         @param vdcguid:            guid of the VDC to delete.
        *         @type vdcguid:             guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function deleteVdc (vdcguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteVdc', delete_ResultReceived, getError, vdcguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

