
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Job extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_job';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Job()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:   guid of the job rootobject
        *         @type rootobjectguid:    guid
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 rootobject
        *         @rtype:                  rootobject
        *         @warning:                Only usable using the python client.
        *         
        */
        public function getObject (rootobjectguid:String,jobguid:String="",executionparams:Object=null):void
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




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new job.
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with backplaneguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function create (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the job rootobject structure.
        *         @execution_method = sync
        *         
        *         @param jobguid:          guid of the job rootobject
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 XSD representation of the job structure.
        *         @rtype:                  string
        *         @raise e:                In case an error occurred, exception is raised
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function getXMLSchema (jobguid:String,executionparams:Object=null):void
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




        public const EVENTTYPE_CLEAR:String = 'clear_response';
        /**
        *         Deletes all jobs.
        *         
        *         @execution_method = sync
        *         
        *         @security: administrator
        *         
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function clear (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'clear', clear_ResultReceived, getError, jobguid,executionparams);

        }

        private function clear_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CLEAR, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the job rootobject.
        *         @execution_method = sync
        *         
        *         @param yamljobguid:       guid of the job rootobject
        *         @type yamljobguid:        guid
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  YAML representation of the job
        *         @rtype:                   string
        *         
        */
        public function getYAML (yamljobguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, yamljobguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETLOGINFO:String = 'getLogInfo_response';
        /**
        *         return log info as string
        *         @todo define format
        *         
        *         @execution_method = sync
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param MaxLogLevel:      Specifies the highest log level
        *         @type MaxLogLevel:       integer
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        *         @return:                 job log info
        *         @rtype:                  string
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function getLogInfo (jobguid:String,MaxLogLevel:Number=5,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getLogInfo', getLogInfo_ResultReceived, getError, jobguid,MaxLogLevel,executionparams);

        }

        private function getLogInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETLOGINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FINDLATESTJOBS:String = 'findLatestJobs_response';
        /**
        *         Returns the latest jobs.
        *         @execution_method = sync
        *         
        *         @param maxrows:          specifies the number of jobs to return
        *         @type maxrows:           int
        *         @param errorsonly:       When True, only the latest <maxrows> ERROR jobs will be returned, otherwise the latest <maxrows> ERROR/RUNNING jobs will be returned
        *         @type errorsonly:        boolean
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 jobtree
        *         @rtype:                  array of dict [{...}]
        *         
        */
        public function findLatestJobs (maxrows:Number=5,errorsonly:Boolean=false,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'findLatestJobs', findLatestJobs_ResultReceived, getError, maxrows,errorsonly,jobguid,executionparams);

        }

        private function findLatestJobs_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FINDLATESTJOBS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the job rootobject.
        *         @execution_method = sync
        *         
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  XML representation of the job
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         @todo:                    Will be implemented in phase2
        *         
        */
        public function getXML (jobguid:String,executionparams:Object=null):void
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




        public const EVENTTYPE_GETJOBTREE:String = 'getJobTree_response';
        /**
        *         Gets the full tree of the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:   guid of the job rootobject
        *         @type rootobjectguid:    guid
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 jobtree
        *         @rtype:                  array of dict [{...}]
        *         
        */
        public function getJobTree (rootobjectguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getJobTree', getJobTree_ResultReceived, getError, rootobjectguid,jobguid,executionparams);

        }

        private function getJobTree_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETJOBTREE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         
        *         @execution_method = sync
        *         
        *         @param actionname:       actionname of the jobs to find
        *         @type actionname:        string
        *         @param agentguid:        agentguid of the jobs to find
        *         @type agentguid:         guid
        *         @param machineguid:      machineguid of the jobs to find
        *         @type machineguid:       guid
        *         @param applicationguid:  applicationguid of the jobs to find
        *         @type applicationguid:   guid
        *         @param datacenterguid:   datacenterguid of the jobs to find
        *         @type datacenterguid:    guid
        *         @param fromTime:         starttime of the jobs to find (equal or greater than)
        *         @type fromTime:          datetime
        *         @param toTime:           endtime of the jobs to find (equal or less than)
        *         @type toTime:            datetime
        *         
        *         @param clouduserguid:    guid of the job user executing the job
        *         @type clouduserguid:     guid
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        *         @returns array of array [[...]]
        *         
        */
        public function find (actionname:String="",agentguid:String="",machineguid:String="",applicationguid:String="",datacenterguid:String="",fromTime:String="",toTime:String="",clouduserguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, actionname,agentguid,machineguid,applicationguid,datacenterguid,fromTime,toTime,clouduserguid,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete all specified jobs and their children.
        *         
        *         @security: administrator
        *         
        *         @execution_method = sync
        *         
        *         @param jobguids:                 List of jobguids to delete           
        *         @type jobguids:                  array
        *         
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function deleteJob (jobguids:Array,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteJob', delete_ResultReceived, getError, jobguids,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

