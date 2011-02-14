
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Networkzonerule extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_networkzonerule';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Networkzonerule()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the networkzonerule rootobject structure.
        *         @execution_method = sync
        *         
        *         @param networkzoneruleguid:     Guid of the networkzonerule rootobject
        *         @type networkzoneruleguid:      guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the networkzonerule structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (networkzoneruleguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, networkzoneruleguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new networkzonerule.
        *         @security administrators
        *         @param name:                      name of the networkzonerule
        *         @type name:                       string
        *         @param description:               description of the networkzonerule
        *         @type description:                string
        *         @param sourcenetworkzoneguid:     guid of the source network zone
        *         @type sourcenetworkzoneguid:      guid
        *         @param destnetworkzoneguid:       guid of the destination network zone
        *         @type destnetworkzoneguid:        guid
        *         @param nrhops:                    number of hops
        *         @type nrhops:                     int
        *         @param gatewayip:                 gateway
        *         @type gatewayip:                  ipaddress
        *         @param log:                       log of the networkzonerule
        *         @type log:                        string
        *         @param disabled:                  flag to indicate whether the rule is disable or not
        *         @type disabled:                   boolean
        *         @param freetransit:               freetransit of the networkzonerule
        *         @type freetransit:                int
        *         @param priority:                  priority of the networkzonerule
        *         @type priority:                   int
        *         @param ipzonerules:               ip zone rules
        *         @type ipzonerules:                array(ipzonerule)
        *         @param jobguid:                   Guid of the job if avalailable else empty string
        *         @type jobguid:                    guid
        *         @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:            dictionary
        *         @return:                          dictionary with networkzoneruleguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                           dictionary
        *         @raise e:                         In case an error occurred, exception is raised
        *         
        *         @todo:                            Will be implemented in phase2
        *         
        */
        public function create (name:String,description:String="",sourcenetworkzoneguid:String="",destnetworkzoneguid:String="",nrhops:Number=0,gatewayip:String="",log:String="",disabled:Boolean=true,freetransit:Number=0,priority:Number=0,ipzonerules:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,description,sourcenetworkzoneguid,destnetworkzoneguid,nrhops,gatewayip,log,disabled,freetransit,priority,ipzonerules,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all networkzonerules.
        *         @execution_method = sync
        *         
        *         @param networkzoneruleguid:     Guid of the networkzonerule specified
        *         @type networkzoneruleguid:      guid
        *         @security administrators
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of networkzonerule info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'networkzoneruleguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'networkzonerule0001',
        *         @note:                                      'description': 'networkzonerule 0001',
        *         @note:                                      'sourcenetworkzoneguid': '73444C07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'destnetworkzoneguid': '43554C07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'nrhops': 1,
        *         @note:                                      'gatewayip': '192.168.0.254',
        *         @note:                                      'log':"",
        *         @note:                                      'disabled' : True,
        *         @note:                                      'freetransit':"",
        *         @note:                                      'priority':"",
        *         @note:                                      'ipzonerules'=[]}]}
        *         
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function list (networkzoneruleguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, networkzoneruleguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the networkzonerule rootobject.
        *         @execution_method = sync
        *         
        *         @param networkzoneruleguid:   Guid of the networkzonerule rootobject
        *         @type networkzoneruleguid:    guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the networkzonerule
        *         @rtype:                       string
        *         
        */
        public function getYAML (networkzoneruleguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, networkzoneruleguid,jobguid,executionparams);

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
        *         @param rootobjectguid:      Guid of the networkzonerule rootobject
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
        *         @param networkzoneruleguid:           Guid of the networkzonerule specified
        *         @type networkzoneruleguid:            guid
        *         @param  name:                         name of the networkzonerule
        *         @type name:                           string
        *         @param  description:                  description of the networkzonerule
        *         @type description:                    string
        *         @param sourcenetworkzoneguid:         guid of the source network zone
        *         @type sourcenetworkzoneguid:          guid
        *         @param destnetworkzoneguid:           guid of the destination network zone
        *         @type destnetworkzoneguid:            guid
        *         @param nrhops:                        number of hops
        *         @type nrhops:                         int
        *         @param gatewayip:                     gateway
        *         @type gatewayip:                      ipaddress
        *         @param log:                           log of the networkzonerule
        *         @type log:                            string
        *         @param disabled:                      flag to indicate whether the rule is disable or not
        *         @type disabled:                       boolean
        *         @param freetransit:                   freetransit of the networkzonerule
        *         @type freetransit:                    int
        *         @param priority:                      priority of the networkzonerule
        *         @type priority:                       int
        *         @param ipzonerules:                   ip zone rules
        *         @type ipzonerules:                    array(ipzonerule)
        *         @param jobguid:                       Guid of the job if avalailable else empty string
        *         @type jobguid:                        guid
        *         @param executionparams:               dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:                dictionary
        *         @return:                              dictionary with networkzone rule guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                               dictionary
        *         @raise e:                             In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (networkzoneruleguid:String,name:String="",description:String="",sourcenetworkzoneguid:String="",destnetworkzoneguid:String="",nrhops:Number=0,gatewayip:String="",log:String="",disabled:Boolean=true,freetransit:Number=0,priority:Number=0,ipzonerules:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, networkzoneruleguid,name,description,sourcenetworkzoneguid,destnetworkzoneguid,nrhops,gatewayip,log,disabled,freetransit,priority,ipzonerules,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the networkzonerule rootobject.
        *         @execution_method = sync
        *         
        *         @param networkzoneruleguid:     Guid of the networkzonerule rootobject
        *         @type networkzoneruleguid:      guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the networkzonerule
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (networkzoneruleguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, networkzoneruleguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of networkzonerule guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param  name:                    name of the networkzonerule
        *         @type name:                      string
        *         @param  description:             description of the networkzonerule
        *         @type description:               string
        *         @param sourcenetworkzoneguid:    guid of the source network zone
        *         @type sourcenetworkzoneguid:     guid
        *         @param destnetworkzoneguid:      guid of the destination network zone
        *         @type destnetworkzoneguid:       guid
        *         @param nrhops:                   number of hops
        *         @type nrhops:                    int
        *         @param gatewayip:                gateway
        *         @type gatewayip:                 ipaddress
        *         @param log:                      log of the networkzonerule
        *         @type log:                       string
        *         @param disabled:                 flag to indicate whether the rule is disable or not
        *         @type disabled:                  boolean
        *         @param freetransit:              freetransit of the networkzonerule
        *         @type freetransit:               int
        *         @param priority:                 priority of the networkzonerule
        *         @type priority:                  int
        *         @param ipzonerules:              ip zone rules
        *         @type ipzonerules:               array(ipzonerule)
        *         
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         Array of networkzonerule guids which met the find criteria specified.
        *         @rtype:                          array
        *         @note:                           Example return value:
        *         @note:                           {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                            'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function find (name:Object=null,description:Object=null,sourcenetworkzoneguid:Object=null,destnetworkzoneguid:Object=null,nrhops:Object=null,gatewayip:Object=null,log:Object=null,disabled:Object=null,freetransit:Object=null,priority:Object=null,ipzonerules:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,sourcenetworkzoneguid,destnetworkzoneguid,nrhops,gatewayip,log,disabled,freetransit,priority,ipzonerules,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a networkzonerule.
        *         @security administrators
        *         @param networkzoneruleguid:   Guid of the networkzonerule rootobject to delete.
        *         @type networkzoneruleguid:    guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        *         @todo:                        Will be implemented in phase2
        *         
        */
        public function deleteNetworkzonerule (networkzoneruleguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteNetworkzonerule', delete_ResultReceived, getError, networkzoneruleguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

