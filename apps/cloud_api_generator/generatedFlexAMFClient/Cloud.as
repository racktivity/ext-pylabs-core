
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Cloud extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_cloud';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Cloud()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the cloud rootobject structure.
        *         @execution_method = sync
        *         
        *         @param cloudguid:        Guid of the cloud rootobject
        *         @type cloudguid:         guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 XSD representation of the cloud structure.
        *         @rtype:                  string
        *         @raise e:                In case an error occurred, exception is raised
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function getXMLSchema (cloudguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, cloudguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDDATACENTER:String = 'addDatacenter_response';
        /**
        *         Add a datacenter to which the cloud belongs
        *         
        *         @execution_method = sync
        *         
        *         @param cloudguid:         Guid of the cloud rootobject
        *         @type cloudguid:          guid
        *         @param datacenterguid:    Guid of the datacenter to add
        *         @type datacenterguid:     guid
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function addDatacenter (cloudguid:String,datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addDatacenter', addDatacenter_ResultReceived, getError, cloudguid,datacenterguid,jobguid,executionparams);

        }

        private function addDatacenter_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDDATACENTER, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new cloud.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   Name for the cloud.
        *         @type name:                    string
        *         @param description:            Description for the cloud.
        *         @type description:             string
        *         @param datacenterguids:        guid of the datacenters to which this cloud belongs, can be a cloud spans multiple datacenters
        *         @type datacenterguids:         list(guid)
        *         @param dns:                    dns for this cloud environment.
        *         @type dns:                     ipaddress
        *         
        *         @param smtp:                   Host of the SMTP server to use in this cloud.
        *         @type smtp:                    string
        *         
        *         @param smtplogin:              Login of the SMTP server (if required).
        *         @type smtplogin:               string
        *         
        *         @param smtppassword:           Password of the SMTP server (if required).
        *         @type smtppassword:            string
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with cloudguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,description:String="",datacenterguids:Object=null,dns:String="",smtp:String="",smtplogin:String="",smtppassword:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,description,datacenterguids,dns,smtp,smtplogin,smtppassword,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all clouds.
        *         @execution_method = sync
        *         
        *         @param cloudguid:                Guid of the cloud specified
        *         @type cloudguid:                 guid
        *         @security administrators
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with array of cloud info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @note:                           {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                           'result: [{ 'cloudguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                       'name': 'cloud0001',
        *         @note:                                       'description': 'cloud 0001',
        *         @note:                                       'datacenterguids': '3351FF9F-D65A-4F65-A96B-AC4A6246C033','F353F79F-D65A-4F65-A96B-AC4A6246C033']}]}
        *         @note:                                     { 'cloudguid': '1351F79F-D65A-4F65-A96B-AC4A6246C033',
        *         @note:                                       'name': 'cloud0002',
        *         @note:                                       'description': 'cloud 0002',
        *         @note:                                       'datacenterguids': ['2351FF9F-D65A-4F65-A96B-AC4A6246C033','7353F79F-D65A-4F65-A96B-AC4A6246C033']}]}
        *         
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function list (cloudguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, cloudguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the cloud rootobject.
        *         @param cloudguid:             Guid of the cloud rootobject
        *         @type cloudguid:              guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the cloud
        *         @rtype:                       string
        *         
        */
        public function getYAML (cloudguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, cloudguid,jobguid,executionparams);

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
        *         @param rootobjectguid:      Guid of the cloud rootobject
        *         @type rootobjectguid:       guid
        *         @return:                    rootobject
        *         @rtype:                     string
        *         @warning:                   Only usable using the python client.
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




        public const EVENTTYPE_DELETEDATACENTER:String = 'deleteDatacenter_response';
        /**
        *         Remove a datacenter to which the cloud belongs
        *         @execution_method = sync
        *         
        *         @param cloudguid:         Guid of the cloud rootobject
        *         @type cloudguid:          guid
        *         @param datacenterguid:    Guid of the datacenter to add
        *         @type datacenterguid:     guid
        *         
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function deleteDatacenter (cloudguid:String,datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteDatacenter', deleteDatacenter_ResultReceived, getError, cloudguid,datacenterguid,jobguid,executionparams);

        }

        private function deleteDatacenter_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETEDATACENTER, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param cloudguid:              Guid of the cloud specified
        *         @type cloudguid:               guid
        *         @param name:                   Name for the cloud.
        *         @type name:                    string
        *         @param description:            Description for the cloud.
        *         @type description:             string
        *         @param datacenterguids:        guid of the datacenters to which this cloud belongs, can be a cloud spans multiple datacenters
        *         @type datacenterguids:         list(guid)
        *         
        *         @param dns:                    IP of the DNS server to use in this cloud.
        *         @type dns:                     string
        *         
        *         @param smtp:                   Host of the SMTP server to use in this cloud.
        *         @type smtp:                    string
        *         
        *         @param smtplogin:              Login of the SMTP server (if required).
        *         @type smtplogin:               string
        *         
        *         @param smtppassword:           Password of the SMTP server (if required).
        *         @type smtppassword:            string
        *         
        *         @param installtype:            DEVELOPMENT / PRODUCTION
        *         @type installtype:             string
        *         
        *         @param installoption:          SSO / MIRRORCLOUD / DAAS
        *         @type installoption:           string
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with cloud guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (cloudguid:String,name:String="",description:String="",datacenterguids:Object=null,dns:String="",smtp:String="",smtplogin:String="",smtppassword:String="",installtype:String="",installoption:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, cloudguid,name,description,datacenterguids,dns,smtp,smtplogin,smtppassword,installtype,installoption,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTDATACENTERS:String = 'listDatacenters_response';
        /**
        *         List all related datacenters of the cloud.
        *         @execution_method = sync
        *         
        *         @param cloudguid:               Guid of the cloud rootobject
        *         @type cloudguid:                guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of cloud info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listDatacenters (cloudguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listDatacenters', listDatacenters_ResultReceived, getError, cloudguid,jobguid,executionparams);

        }

        private function listDatacenters_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTDATACENTERS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the cloud rootobject.
        *         @execution_method = sync
        *         
        *         @param cloudguid:           Guid of the cloud rootobject
        *         @type cloudguid:            guid
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    XML representation of the cloud
        *         @rtype:                     string
        *         @raise e:                   In case an error occurred, exception is raised
        *         @todo:                      Will be implemented in phase2
        *         
        */
        public function getXML (cloudguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, cloudguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of cloud guids which met the find criteria.
        *         @security administrators
        *         @execution_method = sync
        *         
        *         @param name:                   Name for the cloud.
        *         @type name:                    string
        *         @param description:            Description for the cloud.
        *         @type description:             string
        *         @param datacenterguids:        guid of the datacenters to which this cloud belongs, can be a cloud spans multiple datacenters
        *         @type datacenterguids:         list(guid)
        *         @param dns:                    IP of the DNS server used in this cloud.
        *         @type dns:                     string
        *         
        *         @param smtp:                   Host of the SMTP server used in this cloud.
        *         @type smtp:                    string
        *         
        *         @param smtplogin:              Login of the SMTP server.
        *         @type smtplogin:               string
        *         
        *         @param smtppassword:           Password of the SMTP server.
        *         @type smtppassword:            string
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Array of cloud guids which met the find criteria specified.
        *         @rtype:                        array
        *         @note:                         Example return value:
        *         @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,description:Object=null,datacenterguids:Object=null,dns:Object=null,smtp:Object=null,smtplogin:Object=null,smtppassword:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,datacenterguids,dns,smtp,smtplogin,smtppassword,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a cloud.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param cloudguid:             Guid of the cloud rootobject to delete.
        *         @type cloudguid:              guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function deleteCloud (cloudguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteCloud', delete_ResultReceived, getError, cloudguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

