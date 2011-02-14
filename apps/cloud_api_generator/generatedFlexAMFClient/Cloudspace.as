
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Cloudspace extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_cloudspace';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Cloudspace()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTVDCS:String = 'listVdcs_response';
        /**
        *         Returns a list of vdcs for the cloudspace.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:   Guid of the cloudspace specified
        *         @type cloudspaceguid:    guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of vdcs.
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function listVdcs (cloudspaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listVdcs', listVdcs_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function listVdcs_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTVDCS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTLANS:String = 'listLans_response';
        /**
        *         Returns a list of lans for the cloudspace.
        *         @param cloudspaceguid:   Guid of the cloudspace specified
        *         @type cloudspaceguid:    guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of lans.
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function listLans (cloudspaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listLans', listLans_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function listLans_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTLANS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTAPPLICATIONS:String = 'listApplications_response';
        /**
        *         Returns a list of applications for the cloudspace.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:   Guid of the cloudspace specified
        *         @type cloudspaceguid:    guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of apllications.
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function listApplications (cloudspaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listApplications', listApplications_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function listApplications_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTAPPLICATIONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the cloudspace rootobject structure.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:  Guid of the cloudspace rootobject
        *         @type cloudspaceguid:   guid
        *         @return:                XSD representation of the disk structure.
        *         @rtype:                 string
        *         @raise e:               In case an error occurred, exception is raised
        *         @todo:                  Will be implemented in phase2
        *         
        */
        public function getXMLSchema (cloudspaceguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new cloudspace for the given customer.
        *         @execution_method = sync
        *         
        *         @param customerguid:             Guid of the customer to which this cloudspace is assigned.
        *         @type customerguid:              guid
        *         @param name:                     Name for the new cloudspace
        *         @type name:                      string
        *         @param description:              Description for the new cloudspace
        *         @type description:               string
        *         @param parentcloudspaceguid:     Guid of the cloudspace of which this cloudspace is part of.
        *         @type parentcloudspaceguid:      guid
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         Dictionary with cloudspaceguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Define security for root spaces
        *         
        */
        public function create (customerguid:String,name:String,description:String="",parentcloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, customerguid,name,description,parentcloudspaceguid,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of cloudspaces for a given customer.
        *         @execution_method = sync
        *         
        *         @param customerguid:     Guid of  the customer for which to retrieve the list of cloudspaces.
        *         @type customerguid:      guid
        *         @param cloudspaceguid:   Guid of the cloudspace to delete.
        *         @type cloudspaceguid:    guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of dictionaries with guid, name and status for each cloudspace.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "cloudspace1", "status": "ACTIVE"},
        *         @note:                                {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "name": "cloudspace2", "status": "DISABLED"}]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function list (customerguid:Object=null,cloudspaceguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, customerguid,cloudspaceguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the cloudspace rootobject.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:  Guid of the cloudspace rootobject
        *         @type cloudspaceguid:   guid
        *         @return:                YAML representation of the cloudspace
        *         @rtype:                 string
        *         
        */
        public function getYAML (cloudspaceguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETSTATUS:String = 'setStatus_response';
        /**
        *         Updates the status of the cloudspace specified.
        *         @param cloudspaceguid:         Guid of the cloudspace specified
        *         @type cloudspaceguid:          guid
        *         @param status:                 Status for the cloudspace specified. See listStatuses() for the list of possible statuses.
        *         @type status:                  string
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setStatus (cloudspaceguid:String,status:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setStatus', setStatus_ResultReceived, getError, cloudspaceguid,status,jobguid,executionparams);

        }

        private function setStatus_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETSTATUS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:    Guid of the lan rootobject
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




        public const EVENTTYPE_LISTSTATUSES:String = 'listStatuses_response';
        /**
        *         Returns a list of possible cloudspace statuses.
        *         @execution_method = sync
        *         
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of statuses.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '["ACTIVE","DISABLED"]',
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




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the cloudspace rootobject.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:  Guid of the cloudspace rootobject
        *         @type cloudspaceguid:   guid
        *         @return:                XML representation of the cloudspace
        *         @rtype:                 string
        *         @raise e:               In case an error occurred, exception is raised
        *         @todo:                  Will be implemented in phase2
        *         
        */
        public function getXML (cloudspaceguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTDEVICES:String = 'listDevices_response';
        /**
        *         Returns a list of devices for the cloudspace.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:   Guid of the cloudspace specified
        *         @type cloudspaceguid:    guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of devices.
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function listDevices (cloudspaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listDevices', listDevices_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function listDevices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTDEVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of cloudspace guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param customerguid:     		Guid of  the customer to include in the search criteria.
        *         @type customerguid:      		guid
        *         @param parentcloudspaceguid:    Guid of the parent cloudspace to include in the search criteria.
        *         @type parentcloudspaceguid:     guid
        *         @param name:    				Name of the cloudspace to include in the search criteria.
        *         @type name:     				string
        *         @param status:    				Status of the cloudspace to include in the search criteria. See listStatuses().
        *         @type status:     				string
        *         @param jobguid:    	        	Guid of the job if avalailable else empty string
        *         @type jobguid:     	        	guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of cloudspaceguids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (customerguid:Object=null,parentcloudspaceguid:Object=null,name:Object=null,status:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, customerguid,parentcloudspaceguid,name,status,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the given cloudspace.
        *         @execution_method = sync
        *         
        *         @param cloudspaceguid:   Guid of the cloudspace to delete.
        *         @type cloudspaceguid:    guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function deleteCloudspace (cloudspaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteCloudspace', delete_ResultReceived, getError, cloudspaceguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

