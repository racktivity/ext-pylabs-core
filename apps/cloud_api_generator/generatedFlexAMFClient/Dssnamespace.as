
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Dssnamespace extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_dssnamespace';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Dssnamespace()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETSPREADS:String = 'getSpreads_response';
        /**
        *  
        * 		Lists all spreads currently in use by that namespace. A spread is a list of storage daemon application GUID's
        *         
        *         @param namespaceguid:        the guid of the namespace you want to get the spreads for 
        *         @type namespaceguid:         guid
        * 		
        * 		@param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         
        *         @return:                     dictionary with [spreadid, [storagedaemonguid]] as result and jobguid: {'result': [spreadid, [storagedaemonguid]], 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function getSpreads (namespaceguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getSpreads', getSpreads_ResultReceived, getError, namespaceguid,jobguid,executionparams);

        }

        private function getSpreads_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETSPREADS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the disk rootobject structure.
        *         @execution_method = sync
        *         
        *         @param diskguid:                guid of the disk rootobject
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the disk structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new namespace with the given policy
        *         @param name:               name of the namespace
        *         @type name:                string
        *         @param dsspolicyguid:      guid of the dss policy that should be applied for storing data in this namespace
        *         @type dsspolicyguid:       guid     
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with namespaceguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,dsspolicyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,dsspolicyguid,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the disk rootobject.
        *         @execution_method = sync
        *         
        *         @param diskguid:                guid of the disk rootobject
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @return:                        YAML representation of the disk
        *         @rtype:                         string
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getYAML (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETNAMESPACEINFO:String = 'getnamespaceinfo_response';
        /**
        *  
        * 		returns status information about all objects and superblocks in the namespace. 
        *           
        *         @param namespaceguid:        the guid of namespace that contains the object 
        *         @type namespaceguid:         guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         
        *         @return:                     dictionary with [param, integer] as result and jobguid: {'result': [param, integer], 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function getnamespaceinfo (namespaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getnamespaceinfo', getnamespaceinfo_ResultReceived, getError, namespaceguid,jobguid,executionparams);

        }

        private function getnamespaceinfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETNAMESPACEINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:    guid of the lan rootobject
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




        public const EVENTTYPE_GETNEXTOBJECTID:String = 'getnextobjectid_response';
        /**
        *  
        * 		Returns the next available objectid for that namespace. A dss client will use that id to store the object.
        *         
        *         @param namespaceguid:        the namespace you want to get the next object id for 
        *         @type namespaceguid:         guid
        * 		
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         
        *         @return:                     integer id to be used for next object id.
        *         @rtype:                      int
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function getnextobjectid (namespaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getnextobjectid', getnextobjectid_ResultReceived, getError, namespaceguid,jobguid,executionparams);

        }

        private function getnextobjectid_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETNEXTOBJECTID, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATESPREADS:String = 'updateSpreads_response';
        /**
        *  
        * 		Updates and returns all spreads in use by that namespace. Is used when balckisted storage daemons are detected in a spread. A spread is a list of storage daemon application GUID's
        *         
        *         @param namespaceguid:        the guid of the namespace you want to get the spreads for 
        *         @type namespaceguid:         guid
        * 		
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        * 		 
        *         @return:                     dictionary with [spreadid, [storagedaemonguid]] as result and jobguid: {'result': [spreadid, [storagedaemonguid]], 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function updateSpreads (namespaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateSpreads', updateSpreads_ResultReceived, getError, namespaceguid,jobguid,executionparams);

        }

        private function updateSpreads_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATESPREADS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_VERIFYOBJECT:String = 'verifyobject_response';
        /**
        *  verifies if object is restorable from dss storage system, this checks the status of the data on the storage daemons for this object.
        *           
        *         @param namespaceguid:   the guid of namespace that contains the object 
        *         @type namespaceguid:    guid
        *         
        *         @param objectid :     	id of the object
        *         @type objectid:       	int      
        *         
        *         @return:                dictionary with object storage information as result and jobguid: {'result': dictionary, 'jobguid': guid}
        *         @rtype:                 dictionary
        *         @raise e:               In case an error occurred, exception is raised
        *         
        *         @todo:                  Will be implemented in phase2
        *         
        */
        public function verifyobject (namespaceguid:String,objectid:Number,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'verifyobject', verifyobject_ResultReceived, getError, namespaceguid,objectid,jobguid,executionparams);

        }

        private function verifyobject_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_VERIFYOBJECT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECTINFO:String = 'getobjectinfo_response';
        /**
        *  returns storage information about an object in the store; list storage daemons per superblock and associated spread
        *           
        *         @param namespaceguid:        the guid of namespace that contains the object 
        *         @type namespaceguid:         guid
        *         
        *         @param objectid :     	     id of the object
        *         @type objectid:       	     int      
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         
        *         @return:                     dictionary with [superblockid, spreadid, [storagedaemonguid]] as result and jobguid: {'result': [superblockid, [spreadid, [storagedaemonguid]]], 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function getobjectinfo (namespaceguid:String,objectid:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getobjectinfo', getobjectinfo_ResultReceived, getError, namespaceguid,objectid,jobguid,executionparams);

        }

        private function getobjectinfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETOBJECTINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the disk rootobject.
        *         @execution_method = sync
        *         
        *         @param diskguid:                guid of the disk rootobject
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the disk
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of namespace guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:                       Name of the namespace to find.
        *         @type name:                        string
        *         @param dsspolicyguid:              guid of the dss policy that is used for the namespace to find
        *         @type dsspolicyguid:               guid    
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with an array of namespace guids as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function find (name:String="",dsspolicyguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,dsspolicyguid,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a namespace.
        *         @param dssnamespaceguid: guid of the namespace rootobject
        *         @type dssnamespaceguid:  guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function deleteDssnamespace (dssnamespaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteDssnamespace', delete_ResultReceived, getError, dssnamespaceguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

