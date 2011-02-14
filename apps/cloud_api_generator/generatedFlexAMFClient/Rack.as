
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Rack extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_rack';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Rack()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the rack rootobject structure.
        *         @execution_method = sync
        *         
        *         @param rackguid:           Guid of the rack rootobject
        *         @type rackguid:            guid
        *         @param jobguid:            Guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   XSD representation of the rack structure.
        *         @rtype:                    string
        *         @raise e:                  In case an error occurred, exception is raised
        *         @todo:                     Will be implemented in phase2
        *         
        */
        public function getXMLSchema (rackguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, rackguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new rack.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   Name for the rack.
        *         @type name:                    string
        *         @param racktype:               type of the rack
        *         @type racktype:                string
        *         @param description:            Description for the rack.
        *         @type description:             string
        *         @param datacenterguid:         datacenter to which the rack belongs
        *         @type datacenterguid:          guid
        *         @param  floor:                 floor location of the rack in the datacenter
        *         @type floor:                   string(100)
        *         @param  corridor:              corridor location of the rack on the floor
        *         @type corridor:                string(100)
        *         @param  position:              position of the rack in the corridor or datacenter
        *         @type position:                string(100)
        *         @param  height:                rack height
        *         @type height:                  int
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with rackguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,racktype:String,description:String="",datacenterguid:String="",floor:Object=null,corridor:Object=null,position:Object=null,height:Number=42,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,racktype,description,datacenterguid,floor,corridor,position,height,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all racks.
        *         @execution_method = sync
        *         
        *         @param rackguid:                Guid of the rack specified
        *         @type rackguid:                 guid
        *         @security administrators
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of rack info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'rackguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'rack001',
        *         @note:                                      'description': 'rack 0001',
        *         @note:                                      'racktype' :   "OPEN",
        *         @note:                                      'floor':"",
        *         @note:                                      'datacenterguid': '3351FF9F-D65A-4F65-A96B-AC4A6246C033',
        *                                                     'corridor': "",
        *                                                     'position':"",
        *                                                     'height':42}]}
        *                                                     
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function list (rackguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, rackguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the rack rootobject.
        *         @execution_method = sync
        *         
        *         @param rackguid:              Guid of the rack rootobject
        *         @type rackguid:               guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the rack
        *         @rtype:                       string
        *         
        */
        public function getYAML (rackguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, rackguid,jobguid,executionparams);

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
        *         @param rootobjectguid:      Guid of the rack rootobject
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
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param rackguid:               Guid of the rack specified
        *         @type rackguid:                guid
        *         @param name:                   Name for the rack.
        *         @type name:                    string
        *         @param racktype:               type of the rack
        *         @type racktype:                string
        *         @param description:            Description for the rack.
        *         @type description:             string
        *         @param datacenterguid:         datacenter to which the rack belongs
        *         @type datacenterguid:          guid
        *         @param  floor:                 floor location of the rack in the datacenter
        *         @type floor:                   string(100)
        *         @param  corridor:              corridor location of the rack on the floor
        *         @type corridor:                string(100)
        *         @param  position:              position of the rack in the corridor or datacenter
        *         @type position:                string(100)
        *         @param  height:                rack height
        *         @type height:                  int
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with rack guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (rackguid:String,name:String="",racktype:String="",description:String="",datacenterguid:String="",floor:Object=null,corridor:Object=null,position:Object=null,height:Number=42,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, rackguid,name,racktype,description,datacenterguid,floor,corridor,position,height,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the rack rootobject.
        *         @execution_method = sync
        *         
        *         @param rackguid:           Guid of the rack rootobject
        *         @type rackguid:            guid
        *         @param jobguid:            Guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   XML representation of the rack
        *         @rtype:                    string
        *         @raise e:                  In case an error occurred, exception is raised
        *         @todo:                     Will be implemented in phase2
        *         
        */
        public function getXML (rackguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, rackguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTDEVICES:String = 'listDevices_response';
        /**
        *         List all devices of the rack.
        *   
        *         @execution_method = sync
        *               
        *         @param rackguid:                Guid of the rack specified
        *         @type rackguid:                 guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of devices
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listDevices (rackguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listDevices', listDevices_ResultReceived, getError, rackguid,jobguid,executionparams);

        }

        private function listDevices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTDEVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of rack guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   Name for the rack.
        *         @type name:                    string
        *         @param racktype:               type of the rack
        *         @type racktype:                string
        *         @param description:            Description for the rack.
        *         @type description:             string
        *         @param datacenterguid:         datacenter to which the rack belongs
        *         @type datacenterguid:          guid
        *         @param  floor:                 floor location of the rack in the datacenter
        *         @type floor:                   string(100)
        *         @param  corridor:              corridor location of the rack on the floor
        *         @type corridor:                string(100)
        *         @param  position:              position of the rack in the corridor or datacenter
        *         @type position:                string(100)
        *         @param  height:                rack height
        *         @type height:                  int
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Array of rack guids which met the find criteria specified.
        *         @rtype:                        array
        *         @note:                         Example return value:
        *         @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,racktype:Object=null,description:Object=null,datacenterguid:Object=null,floor:Object=null,corridor:Object=null,position:Object=null,height:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,racktype,description,datacenterguid,floor,corridor,position,height,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a rack.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param rackguid:              Guid of the rack rootobject to delete.
        *         @type rackguid:               guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function deleteRack (rackguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteRack', delete_ResultReceived, getError, rackguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

