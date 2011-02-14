
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Networkzone extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_networkzone';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Networkzone()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the networkzone rootobject structure.
        *         @execution_method = sync
        *         
        *         @param networkzoneguid:         Guid of the networkzone rootobject
        *         @type networkzoneguid:          guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the networkzone structure.
        *         @rtype:                          string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (networkzoneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, networkzoneguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new networkzone.
        *         @security administrators
        *         @param name:                   name of the networkzone
        *         @type name:                    string
        *         @param description:            description of the object
        *         @type description:             string
        *         @param public:                 is this network zone public to the internet
        *         @type public:                  bool
        *         @param datacenterguid:         guid of the datacenter
        *         @type datacenterguid:          guid
        *         @param parentnetworkzoneguid:  guid of the parantnetworkzoneguid
        *         @type parentnetworkzoneguid:   guid
        *         @param ranges:                 list of networkzoneranges
        *         @type ranges:                  array(networkzonerange)
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with networkzoneguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,description:String="",ispublic:Object=null,datacenterguid:String="",parentnetworkzoneguid:String="",ranges:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all networkzones.
        *         @execution_method = sync
        *         
        *         @param networkzoneguid:         Guid of the networkzone specified
        *         @type networkzoneguid:          guid
        *         @security administrators
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of networkzone info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'networkzoneguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'networkzone0001',
        *         @note:                                      'description': 'networkzone 0001',
        *         @note:                                      'public': False
        *         @note:                                      'datacenterguid': 'B2744B07-4129-47B1-8690-B92C0DB21434'
        *         @note:                                      'parentnetworkzoneguid': 'A2744B07-4129-47B1-8690-B92C0DB21434'
        *         @note:                                      'ranges': []}]}
        *         
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function list (networkzoneguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, networkzoneguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the networkzone rootobject.
        *         @execution_method = sync
        *         
        *         @param networkzoneguid:       Guid of the networkzone rootobject
        *         @type networkzoneguid:        guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the networkzone
        *         @rtype:                       string
        *         
        */
        public function getYAML (networkzoneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, networkzoneguid,jobguid,executionparams);

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
        *         @param rootobjectguid:      Guid of the networkzone rootobject
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




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @security administrators
        *         @param networkzoneguid:        Guid of the networkzone specified
        *         @type networkzoneguid:         guid
        *         @param name:                   name of the networkzone
        *         @type name:                    string
        *         @param description:            description of the object
        *         @type description:             string
        *         @param public:                 is this network zone public to the internet
        *         @type public:                  bool
        *         @param datacenterguid:         guid of the datacenter
        *         @type datacenterguid:          guid
        *         @param parentnetworkzoneguid:  guid of the parantnetworkzoneguid
        *         @type parentnetworkzoneguid:   guid
        *         @param ranges:                 list of networkzoneranges
        *         @type ranges:                  array(networkzonerange)
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with networkzone guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (networkzoneguid:String,name:String="",description:String="",ispublic:Object=null,datacenterguid:String="",parentnetworkzoneguid:String="",ranges:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, networkzoneguid,name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the networkzone rootobject.
        *         @execution_method = sync
        *         
        *         @param networkzoneguid:         Guid of the networkzone rootobject
        *         @type networkzoneguid:          guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the networkzone
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (networkzoneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, networkzoneguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of networkzone guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   name of the networkzone
        *         @type name:                    string
        *         @param description:            description of the object
        *         @type description:             string
        *         @param public:                 is this network zone public to the internet
        *         @type public:                  bool
        *         @param datacenterguid:         guid of the datacenter
        *         @type datacenterguid:          guid
        *         @param parentnetworkzoneguid:  guid of the parantnetworkzoneguid
        *         @type parentnetworkzoneguid:   guid
        *         @param ranges:                 list of networkzoneranges
        *         @type ranges:                  array(networkzonerange)
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Array of networkzone guids which met the find criteria specified.
        *         @rtype:                        array
        *         @note:                         Example return value:
        *         @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,description:Object=null,ispublic:Object=null,datacenterguid:Object=null,parentnetworkzoneguid:Object=null,ranges:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,public,datacenterguid,parentnetworkzoneguid,ranges,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a networkzone.
        *         @security administrators
        *         @param networkzoneguid:       Guid of the networkzone rootobject to delete.
        *         @type networkzoneguid:        guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function deleteNetworkzone (networkzoneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteNetworkzone', delete_ResultReceived, getError, networkzoneguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

