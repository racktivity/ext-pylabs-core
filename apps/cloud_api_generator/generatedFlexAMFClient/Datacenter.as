
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Datacenter extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_datacenter';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Datacenter()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTCLOUDS:String = 'listClouds_response';
        /**
        *         List all clouds of the datacenter.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:          Guid of the datacenter specified
        *         @type datacenterguid:           guid
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of clouds
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listClouds (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listClouds', listClouds_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function listClouds_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCLOUDS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the datacenter rootobject structure.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:           Guid of the datacenter rootobject
        *         @type datacenterguid:            guid
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         XSD representation of the datacenter structure.
        *         @rtype:                          string
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function getXMLSchema (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTRACKS:String = 'listRacks_response';
        /**
        *         List all racks of the datacenter.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:           Guid of the datacenter specified
        *         @type datacenterguid:            guid
        *         
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with array of racks
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function listRacks (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listRacks', listRacks_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function listRacks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTRACKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new datacenter.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   Name for the datacenter.
        *         @type name:                    string
        *         @param description:            Description for the datacenter.
        *         @type description:             string
        *         @param locationguid:           guid of the location of the datacenter
        *         @type locationguid:            guid
        *         @param clouduserguid:          guid of the clouduser owning the datacenter
        *         @type clouduserguid:           guid
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with datacenterguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,description:String="",locationguid:String="",clouduserguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,description,locationguid,clouduserguid,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all datacenters.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:          Guid of the datacenter specified
        *         @type datacenterguid:           guid
        *         @security administrators
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of datacenter info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'datacenterguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'datacenter0001',
        *         @note:                                      'description': 'datacenter 0001',
        *         @note:                                      'locationguid': '3351FF9F-D65A-4F65-A96B-AC4A6246C033',
        *         @note:                                      'clouduserguid': 'F353F79F-D65A-4F65-A96B-AC4A6246C033'}]}
        *         @note:                                    { 'datacenterguid': '1351F79F-D65A-4F65-A96B-AC4A6246C033',
        *         @note:                                      'name': 'datacenter0001',
        *         @note:                                      'description': 'datacenter 0001',
        *         @note:                                      'locationguid': '2351FF9F-D65A-4F65-A96B-AC4A6246C033',
        *         @note:                                      'clouduserguid': '7353F79F-D65A-4F65-A96B-AC4A6246C033'}]}
        *         
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function list (datacenterguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the datacenter rootobject.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:        Guid of the datacenter rootobject
        *         @type datacenterguid:         guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the datacenter
        *         @rtype:                       string
        *         
        */
        public function getYAML (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, datacenterguid,jobguid,executionparams);

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
        *         @param rootobjectguid:      Guid of the datacenter rootobject
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




        public const EVENTTYPE_LISTNETWORKZONES:String = 'listNetworkzones_response';
        /**
        *         List all network zones of the datacenter.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:          Guid of the datacenter specified
        *         @type datacenterguid:           guid
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of network zones
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listNetworkzones (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listNetworkzones', listNetworkzones_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function listNetworkzones_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTNETWORKZONES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param datacenterguid:         Guid of the datacenter specified
        *         @type datacenterguid:          guid
        *         @param name:                   Name for the datacenter.
        *         @type name:                    string
        *         @param description:            Description for the datacenter.
        *         @type description:             string
        *         @param locationguid:           guid of the location of the datacenter
        *         @type locationguid:            guid
        *         @param clouduserguid:          guid of the clouduser owning the datacenter
        *         @type clouduserguid:           guid
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with datacenter guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (datacenterguid:String,name:String="",description:String="",locationguid:String="",clouduserguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, datacenterguid,name,description,locationguid,clouduserguid,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the datacenter rootobject.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:           Guid of the datacenter rootobject
        *         @type datacenterguid:            guid
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         XML representation of the datacenter
        *         @rtype:                          string
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function getXML (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of datacenter guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   Name for the datacenter.
        *         @type name:                    string
        *         @param description:            Description for the datacenter.
        *         @type description:             string
        *         @param locationguid:           guid of the location of the datacenter
        *         @type locationguid:            guid
        *         @param clouduserguid:          guid of the clouduser owning the datacenter
        *         @type clouduserguid:           guid
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Array of datacenter guids which met the find criteria specified.
        *         @rtype:                        array
        *         @note:                         Example return value:
        *         @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,description:Object=null,locationguid:Object=null,clouduserguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,locationguid,clouduserguid,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTRESOURCEGROUPS:String = 'listResourceGroups_response';
        /**
        *         List all resource groups of the datacenter.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:           Guid of the datacenter specified
        *         @type datacenterguid:            guid
        *         
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with array of clouds
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function listResourceGroups (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listResourceGroups', listResourceGroups_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function listResourceGroups_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTRESOURCEGROUPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a datacenter.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param datacenterguid:        Guid of the datacenter rootobject to delete.
        *         @type datacenterguid:         guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function deleteDatacenter (datacenterguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteDatacenter', delete_ResultReceived, getError, datacenterguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

