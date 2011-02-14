
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Policy extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_policy';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Policy()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the os rootobject structure.
        *         @execution_method = sync
        *         
        *         @param policyguid:                guid of the os rootobject
        *         @type policyguid:                 guid
        *  
        *         @param jobguid:                   guid of the job if avalailable else empty string
        *         @type jobguid:                    guid
        *         @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:            dictionary
        *         @return:                          XSD representation of the os structure.
        *         @rtype:                           string
        *         @raise e:                         In case an error occurred, exception is raised
        *         @todo:                            Will be implemented in phase2
        *         
        */
        public function getXMLSchema (policyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, policyguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new policy.
        *         @execution_method = sync
        *         
        *         @param name:                     Name for the new policy
        *         @type name:                      string
        *         @param rootobjecttype:           RootObject type for the new policy
        *         @type rootobjecttype:            string
        *         
        *         @param rootobjectaction:         Name of the action for the new policy
        *         @type rootobjectaction:          string
        *         
        *         @param rootobjectguid:           Guid of the rootobject for the new policy
        *         @type rootobjectguid:            string
        *         
        *         @param interval:                 Interval for the new policy
        *         @type interval:                  int
        *         
        *         @param runbetween:               List of tuples with timestamps when a policy can run
        *         @type runbetween:                list
        *         
        *         @param runnotbetween:            List of tuples with timestamps when a policy can not run
        *         @type runnotbetween:             string
        *         
        *         @param policyparams:             Params for the new policy
        *         @type policyparams:              string
        *         
        *         @param description:              Description for the new policy
        *         @type description:               string
        *         
        *         @param jobguid:                  Guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         Dictionary with policyguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,rootobjecttype:String,rootobjectaction:String,rootobjectguid:String,interval:Number,runbetween:Object=null,runnotbetween:String="None",policyparams:String="None",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,rootobjecttype,rootobjectaction,rootobjectguid,interval,runbetween,runnotbetween,policyparams,description,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of all policies depending on passed filters.
        *         @execution_method = sync
        *         
        *         @param policyguid:                   Guid of the cloudspace
        *         @type policyguid:                    guid
        *         
        *         @param name:                         Name of the policy
        *         @type name:                          string
        *         
        *         @param rootobjectaction:             Action on the rootobject
        *         @type rootobjectaction:              string         
        *         
        *         @param rootobjecttype:               Rootobject type e.g. sso
        *         @type rootobjecttype:                string
        *         
        *         @param status:                       Status of the policy
        *         @type status:                        string        
        *         @param jobguid:                      guid of the job if avalailable else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with array of operating system info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @note:                               {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                'result: [{ 'name': 'Daily backup DBServer'
        *         @note:                                            'description': 'Daily backup of our database server',
        *         @note:                                            'rootobjecttype': 'machine',
        *         @note:                                            'rootobjectaction': 'backup',
        *         @note:                                            'policyparams': {},
        *         @note:                                            'rootobjectguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                            'interval': 86400,
        *         @note:                                            'lastrun': '2009-05-23 11:25:33',
        *         @note:                                            'runbetween': [("00:00", "02.00"), ("04:00", "06:00")],
        *         @note:                                            'runnotbetween': [("08:00", "12:00"), ("14:00", "18:00")]}]}
        *         
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function list (policyguid:Object=null,name:Object=null,rootobjectaction:Object=null,rootobjecttype:Object=null,status:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, policyguid,name,rootobjectaction,rootobjecttype,status,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the policy rootobject.
        *         @execution_method = sync
        *         
        *         @param policyguid:              guid of the os rootobject
        *         @type policyguid:               guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @return:                        YAML representation of the os
        *         @rtype:                         string
        *         
        */
        public function getYAML (policyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, policyguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:     guid of the policy object
        *         @type rootobjectguid:      guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   rootobject
        *         @rtype:                    string
        *         @warning:                  Only usable using the python client.
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
        *         Returns a list of policy guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:               Name of the policy
        *         @type name:                string
        *         
        *         @param description:        description of the policy
        *         @type description:         string
        *         
        *         @param lastrun:            lastrun of the policy
        *         @type lastrun:             datetime
        *         
        *         @param status:             Status for the policy
        *         @type status:              string
        *         
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised        
        *         
        */
        public function updateModelProperties (policyguid:Object,name:String="",description:String="",lastrun:String="",status:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, policyguid,name,description,lastrun,status,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the os rootobject.
        *         @execution_method = sync
        *         
        *         @param policyguid:              guid of the os rootobject
        *         @type policyguid:               guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the os
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (policyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, policyguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of policy guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:               Name of the policy
        *         @type name:                string
        *         
        *         @param description:        description of the policy
        *         @type description:         string
        *         @param rootobjecttype:     Rootobject type.
        *         @type rootobjecttype:      string
        *         @param rootobjectaction:   Action to execute on the rootobject
        *         @type rootobjectaction:    string
        *         @param rootobjectguid:     Guid of the rootobject
        *         @type rootobjectguid:      string
        *         @param interval:           Interval in seconds
        *         @type interval:            int
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with an array of policy guids as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function find (name:String="",description:String="",rootobjecttype:String="",rootobjectaction:String="",rootobjectguid:String="",interval:Number=0,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,rootobjecttype,rootobjectaction,rootobjectguid,interval,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the given policy.
        *         @execution_method = sync
        *         
        *         @param policyguid:               Guid of the policy to delete.
        *         @type policyguid:                guid
        *         @param jobguid:                  Guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function deletePolicy (policyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deletePolicy', delete_ResultReceived, getError, policyguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

