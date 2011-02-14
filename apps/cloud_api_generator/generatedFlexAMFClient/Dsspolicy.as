
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Dsspolicy extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_dsspolicy';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Dsspolicy()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the dsspolicy rootobject structure.
        *         @execution_method = sync
        *         
        *         @param dsspolicyguid:           guid of the dsspolicyguid rootobject
        *         @type dsspolicyguid:            guid
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the dsspolicy structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (dsspolicyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, dsspolicyguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *  
        *         creates a new dss policy
        *         @execution_method = sync
        *         
        *         @param name:            policy name
        *         @type name:             string
        *         @param storageNodes:    defines the minimum number of storage daemons in the spread
        *         @type storageNodes:     int
        *         @param  storageSafety:  defines the number of storage daemons in that can be unavailable in a spread before data loss occurs
        *         @type storageSafety:    int
        *     
        *         @param minSbSize:       the minimum size of a superblock in bytes (needs to be power of 2)
        *         @type minSbSize:        int       
        *     
        *         @param maxSbSize:       the maximum size of a superblock in bytes (needs to be power of 2)
        *         @type maxSbSize:        int
        *         
        *         @param spreadLocations: specify a list of locations on which the data needs to be equally spread, array of datacenter guids
        *         @type spreadLocations:  array(guid)    
        *     
        *         @param resourceGroup:   a resourcegroup is an array of pmachineguids that represent storage nodes
        *         @type resourceGroup:    array(guid)        
        *         @param jobguid:         guid of the job if available else empty string
        *         @type jobguid:          guid
        *         @param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:  dictionary
        *         @return:                dictionary with policyguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                 dictionary
        *         @raise e:               In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,storageNodes:Number,storageSafety:Number,minSbSize:Number,maxSbSize:Number,spreadLocations:Object,resourceGroup:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,storageNodes,storageSafety,minSbSize,maxSbSize,spreadLocations,resourceGroup,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of dsspolicy guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:                       Name of the dss policy
        *         @type name:                        string
        *         
        *         @param status:                     Status of the policy
        *         @type status:                      string
        *         
        *         @param disksafetytype:             Disksafety type of the policy
        *         @type disksafetytype:              string
        *         
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with an array of policy guids as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function list (name:String="",status:String="",disksafetytype:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, name,status,disksafetytype,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the dsspolicy rootobject.
        *         @execution_method = sync
        *         
        *         @param dsspolicyguid:           guid of the dsspolicy rootobject
        *         @type dsspolicyguid:            guid
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @return:                        YAML representation of the dsspolicy
        *         @rtype:                         string
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getYAML (dsspolicyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, dsspolicyguid,jobguid,executionparams);

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
        *         @param rootobjectguid:    guid of the dsspolicy rootobject
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




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Updates the status of an dss policy
        *                                         
        *         @param dsspolicyguid:           Guid of the dsspolicyguid rootobject
        *         @type dsspolicyguid:            guid
        *         
        *         @param status:                  Change the status attribute
        *         @type status:                   string
        *         
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with a boolean as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         
        */
        public function updateModelProperties (dsspolicyguid:String,status:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, dsspolicyguid,status,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the dsspolicy rootobject.
        *         @execution_method = sync
        *         
        *         @param dsspolicyguid:           guid of the dsspolicyguid rootobject
        *         @type dsspolicyguid:            guid
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the dsspolicy
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (dsspolicyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, dsspolicyguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of dsspolicy guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:                       Name of the dsspolicy
        *         @type name:                        string
        *         
        *         @param status:                     Status of the policy
        *         @type status:                      string
        *         
        *         @param disksafetytype:             Disksafety type of the policy (eg SSO,MIRRORCLOUD)
        *         @type disksafetytype:              string
        *         @param storagesafety:              Storage safety of the policy (nr of disks that can be lost without data loss)
        *         @type storagesafety:               int
        *         @param storagewidth:               Storage width of the policy (nr of disks that data is spread amongst)
        *         @type storagewidth:                int
        *         
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with an array of policy guids as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function find (name:String="",status:String="",disksafetytype:String="",storagesafety:Number=0,storagewidth:Number=0,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,status,disksafetytype,storagesafety,storagewidth,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }


    }
}

