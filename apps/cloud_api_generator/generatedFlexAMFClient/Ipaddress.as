
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Ipaddress extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_ipaddress';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Ipaddress()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the ipaddress rootobject structure.
        *         @execution_method = sync
        *         
        *         @param ipaddressguid:           Guid of the ipaddress rootobject
        *         @type ipaddressguid:            guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the ipaddress structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (ipaddressguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, ipaddressguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new ipaddress.
        *         @security administrators
        *         @param name:              name of the ipaddress
        *         @type name:               string
        *         @param  description:      description of the object
        *         @type description:        string
        *         @param  address:          IP address of the IP
        *         @type address:            type_ipaddress
        *         @param  netmask:          netmask of the IP object
        *         @type netmask:            type_netmaskaddress
        *         @param  block:            flag indicating if the IP is blocked
        *         @type block:              boolean
        *         @param  iptype:           type of the IP object, STATIC or DHCP
        *         @type iptype:             string
        *         @param ipversion:         version of the IP object, IPV4 or IPV6
        *         @type ipversion:          string
        *         @param languid:           lan to which the ip is connected
        *         @type languid:            guid
        *         @param virtual            flag is if ip is a VIPA
        *         @type virtual             boolean 
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with ipaddressguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,description:String="",address:Object=null,netmask:Object=null,block:Boolean=false,iptype:String="",ipversion:String="",languid:Object=null,virtual:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,description,address,netmask,block,iptype,ipversion,languid,virtual,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all ipaddresss.
        *         @execution_method = sync
        *         
        *         @param ipaddressguid:           Guid of the ipaddress rootobject
        *         @type ipaddressguid:            guid
        *         @security administrators
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of ipaddress info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'ipaddressguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'ipaddress0001',
        *         @note:                                      'description': 'ipaddress 0001',
        *         @note:                                      'address': '192.148.0.1',
        *         @note:                                      'netmask': '255.255.255.255',
        *         @note:                                      'block': '',
        *         @note:                                      'iptype': 'STATIC',
        *         @note:                                      'ipversion':'IPV4',
        *         @note:                                      'languid': '77544B07-4129-47B1-8690-B92C0DB2143'}]}
        *         
        */
        public function list (ipaddressguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, ipaddressguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the ipaddress rootobject.
        *         @execution_method = sync
        *         
        *         @param ipaddressguid:         Guid of the ipaddress rootobject
        *         @type ipaddressguid:          guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the ipaddress
        *         @rtype:                       string
        *         
        */
        public function getYAML (ipaddressguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, ipaddressguid,jobguid,executionparams);

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
        *         @param rootobjectguid:        Guid of the ipaddress rootobject
        *         @type rootobjectguid:         guid
        *         @return:                      rootobject
        *         @rtype:                       string
        *         @warning:                     Only usable using the python client.
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
        *         @param ipaddressguid:          Guid of the ipaddress specified
        *         @type ipaddressguid:           guid
        *         @param name:                   name of the ipaddress
        *         @type name:                    string
        *         @param  description:           description of the object
        *         @type description:             string
        *         @param  address:               IP address of the IP
        *         @type address:                 type_ipaddress
        *         @param  netmask:               netmask of the IP object
        *         @type netmask:                 type_netmaskaddress
        *         @param  block:                 flag indicating if the IP is blocked
        *         @type block:                   boolean
        *         @param  iptype:                type of the IP object, STATIC or DHCP
        *         @type iptype:                  string
        *         @param ipversion:              version of the IP object, IPV4 or IPV6
        *         @type ipversion:               string
        *         @param languid:                lan to which the ip is connected
        *         @type languid:                 guid
        *         
        *         @param virtual                 flags whether ipaddress is a VIPA
        *         @type virtual                  boolean 
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with ipaddress guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (ipaddressguid:String,name:String="",description:String="",address:Object=null,netmask:Object=null,block:Boolean=false,iptype:String="",ipversion:String="",virtual:Object=null,languid:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, ipaddressguid,name,description,address,netmask,block,iptype,ipversion,virtual,languid,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the ipaddress rootobject.
        *         @param ipaddressguid:           Guid of the ipaddress rootobject
        *         @type ipaddressguid:            guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the ipaddress
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (ipaddressguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, ipaddressguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETSTATE:String = 'setState_response';
        /**
        *         Sets the state of the ip address
        *         
        *         @param ipaddressguid:           Guid of the ipaddress rootobject
        *         @type ipaddressguid:            guid
        *         
        *         @param status:                  status of the ipaddress
        *         @type status:                   string
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with boolean as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised        
        *         
        *         
        */
        public function setState (ipaddressguid:String,status:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setState', setState_ResultReceived, getError, ipaddressguid,status,jobguid,executionparams);

        }

        private function setState_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETSTATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of ipaddress guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         
        *         @param name:                    name of the ipaddress
        *         @type name:                     string
        *         @param description:             description of the object
        *         @type description:              string
        *         @param address:                 IP address of the IP object
        *         @type address:                  type_ipaddress
        *         @param netmask:                 netmask of the IP object
        *         @type netmask:                  type_netmaskaddress
        *         @param block:                   flag indicating if the IP is blocked
        *         @type block:                    boolean
        *         @param iptype:                  type of the IP object, STATIC or DHCP
        *         @type iptype:                   string
        *         @param ipversion:               version of the IP object, IPV4 or IPV6
        *         @type ipversion:                string
        *         @param languid:                 lan to which the ip is connected
        *         @type languid:                  guid
        *         @param cloudspaceguid:          cloudspaceguid to which the ip is connected
        *         @type cloudspaceguid:           guid
        *         
        *         @param virtual                  flag whether to include VIPA
        *         @type virtual                   boolean 
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of ipaddress guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,description:Object=null,address:Object=null,netmask:Object=null,block:Object=null,iptype:Object=null,ipversion:Object=null,languid:Object=null,cloudspaceguid:Object=null,virtual:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,address,netmask,block,iptype,ipversion,languid,cloudspaceguid,virtual,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a ipaddress.
        *         @security administrators
        *         @param ipaddressguid:         Guid of the ipaddress rootobject to delete.
        *         @type ipaddressguid:          guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function deleteIpaddress (ipaddressguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteIpaddress', delete_ResultReceived, getError, ipaddressguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

