
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Errorcondition extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_errorcondition';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Errorcondition()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the errorcondition rootobject structure.
        *         @execution_method = sync
        *         @param jobguid:          guid of the errorcondition rootobject
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of errorcondition specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 XSD representation of the errorcondition structure.
        *         @rtype:                  string
        *         @raise e:                In case an error occurred, exception is raised
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function getXMLSchema (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new errorcondition
        *         @execution_method = sync
        *         @param errorconditiontype:       type of errorcondition
        *         @type errorconditiontype:        int
        *         @param timestamp:                timestamp of errorcondition
        *         @type timestamp:                 int
        *         @param level:                    level of errorcondition
        *         @type level:                     string
        *         @param agent:                    unique id of agent
        *         @type agent:                     string
        *         @param tags:                     series of tags format
        *         @type tags:                      string
        *         @params errormessagepublic:      public error message
        *         @type errormessagepublic         string
        *         @params errormessageprivate:     private error message
        *         @type errormessageprivate        string
        *         @param application:              name of the application
        *         @type application:               string
        *         @param backtrace:                backtrace message
        *         @type backtrace:                 string
        *         @param logs:                     log message
        *         @type logs:                      string
        *         @param transactioninfo:          info of the transaction
        *         @type transactioninfo:           string
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with backplaneguid as result and errorconditionguid: {'result': guid, 'errorconditionguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function create (errorconditiontype:Number=0,timestamp:Number=0,level:String="",agent:String="",tags:String="",errormessagepublic:Object=null,errormessageprivate:Object=null,application:String="",backtrace:String="",logs:String="",transactioninfo:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, errorconditiontype,timestamp,level,agent,tags,errormessagepublic,errormessageprivate,application,backtrace,logs,transactioninfo,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all errorconditions or only specified errorcondition
        *         @execution_method = sync
        *         @param errorconditionguid:       guid of the errorcondition
        *         @type errorconditionguid:        guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with array of errorcondition info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function list (errorconditionguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, errorconditionguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the errorcondition rootobject.
        *         @execution_method = sync
        *         @param errorconditionguid: guid of the errorcondition rootobject
        *         @type errorconditionguid:  guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   YAML representation of the errorcondition
        *         @rtype:                    string
        *         
        */
        public function getYAML (errorconditionguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, errorconditionguid,jobguid,executionparams);

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
        *         @param errorconditionguid:   guid of the job rootobject
        *         @type errorconditionguid:    guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     rootobject
        *         @rtype:                      rootobject
        *         @warning:                    Only usable using the python client.
        *         
        */
        public function getObject (errorconditionguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getObject', getObject_ResultReceived, getError, errorconditionguid,jobguid,executionparams);

        }

        private function getObject_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETOBJECT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RAISEERRORCONDITION:String = 'raiseErrorCondition_response';
        /**
        *         Create a new errorcondition and escalate it
        *         @execution_method = sync
        *         @param level:                    level of errorcondition ('CRITICAL','ERROR','INFO','UNKNOWN','URGENT','WARNING')
        *         @type level:                     string
        *         
        *         @param typeid:                   predefined type id (ex. SSO-MON-NETWORK-0001)
        *         @type typeid:                    string
        *         @params errormessagepublic:      public error message
        *         @type errormessagepublic         string
        *         @params errormessageprivate:     private error message
        *         @type errormessageprivate        string
        *         @param tags:                     series of tags format
        *         @type tags:                      string
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with backplaneguid as result and errorconditionguid: {'result': guid, 'errorconditionguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function raiseErrorCondition (level:String="",typeid:String="",errormessagepublic:Object=null,errormessageprivate:Object=null,tags:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'raiseErrorCondition', raiseErrorCondition_ResultReceived, getError, level,typeid,errormessagepublic,errormessageprivate,tags,jobguid,executionparams);

        }

        private function raiseErrorCondition_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RAISEERRORCONDITION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the errorcondition rootobject.
        *         @execution_method = sync
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  XML representation of the errorcondition
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         @todo:                    Will be implemented in phase2
        *         
        */
        public function getXML (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         @execution_method = sync
        *         @param errorconditiontype:       type of errorcondition
        *         @type errorconditiontype:        string
        *         @param timestamp:                timestamp of errorcondition
        *         @type timestamp:                 int
        *         @param level:                    level of errorcondition
        *         @type level:                     int
        *         @param agent:                    unique id of agent
        *         @type agent:                     string
        *         @param tags:                     series of tags format
        *         @type tags:                      string
        *         @param application:              name of the application
        *         @type application:               string
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @returns array of array [[...]]
        *         
        */
        public function find (errorconditiontype:String="",timestamp:Number=0,level:Number=0,agent:String="",tags:String="",application:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, errorconditiontype,timestamp,level,agent,tags,application,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete the specified errorcondition
        *         @security: administrator
        *         @execution_method = sync
        *         @param errorconditionguid:       guid of the errorcondition
        *         @type errorconditionguid:        guid
        *         @param jobguid:                  guid of the errorcondition if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of errorcondition specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and errorcondition: {'result': True, 'errorconditionguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function deleteErrorcondition (errorconditionguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteErrorcondition', delete_ResultReceived, getError, errorconditionguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

