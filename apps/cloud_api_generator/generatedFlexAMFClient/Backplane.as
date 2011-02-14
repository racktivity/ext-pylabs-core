
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Backplane extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_backplane';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Backplane()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTLANS:String = 'listLans_response';
        /**
        *         List of all related lans to the backplane.
        *         @execution_method = sync
        *         
        *         @param backplaneguid:           Guid of the backplane rootobject
        *         @type backplaneguid:            guid
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of lans info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listLans (backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listLans', listLans_ResultReceived, getError, backplaneguid,jobguid,executionparams);

        }

        private function listLans_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTLANS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the backplane rootobject structure.
        *         @execution_method = sync
        *         
        *         @param backplaneguid:           Guid of the backplane rootobject
        *         @type backplaneguid:            guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the backplane structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, backplaneguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new backplane.
        *         @param name:                   Name for the backplane.
        *         @type name:                    string
        *         @param backplanetype:          Type of the backplane (ETHERNET, INFINIBAND)
        *         @type backplanetype:           string
        *         @param description:            Description for the backplane.
        *         @type description:             string
        *         @param publicflag:             Indicates if the backplane is a public backplane.
        *         @type publicflag:              boolean
        *         @param storageflag:            Indicates if the backplane is a storage backplane.
        *         @type storageflag:             boolean
        *         @param managementflag:         Indicates if the backplane is a management backplane.
        *         @type managementflag:          boolean
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with backplaneguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,backplanetype:String,description:String="",publicflag:Boolean=false,managementflag:Boolean=false,storageflag:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,backplanetype,description,publicflag,managementflag,storageflag,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all backplanes.
        *         @execution_method = sync
        *         
        *         @param backplaneguid:           Guid of the backplane
        *         @type backplaneguid:            guid
        *  
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of backplane info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'backplaneguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'Storage Backplane',
        *         @note:                                      'backplanetype': 'INFINIBAND',
        *         @note:                                      'public': False,
        *         @note:                                      'storage': True,
        *         @note:                                      'management': False},
        *         @note:                                    { 'backplaneguid': '789544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'Management Backplane',
        *         @note:                                      'backplanetype': 'ETHERNET',
        *         @note:                                      'public': False,
        *         @note:                                      'storage': False,
        *         @note:                                      'management': False}]}
        *         
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function list (backplaneguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, backplaneguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the backplane rootobject.
        *         @execution_method = sync
        *         
        *         @param backplaneguid:    Guid of the backplane rootobject
        *         @type backplaneguid:     guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 YAML representation of the backplane
        *         @rtype:                  string
        *         
        */
        public function getYAML (backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, backplaneguid,jobguid,executionparams);

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
        *         @param rootobjectguid:    Guid of the lan rootobject
        *         @type rootobjectguid:     guid
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
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @param backplaneguid:          Guid of the backplane specified
        *         @type backplaneguid:           guid
        *         @param name:                   Name for this backplane
        *         @type name:                    string
        *         @param description:            Description for this backplane
        *         @type description:             string
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with backplane guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (backplaneguid:String,name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, backplaneguid,name,description,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETFLAGS:String = 'setFlags_response';
        /**
        *         Sets the role flags for the specified backplane.
        *         @param backplaneguid:          Guid of the backplane
        *         @type backplaneguid:           guid
        *         @param publicflag:             Defines if the backplane is used as a public backplane. Not modified if empty.
        *         @type publicflag:              boolean
        *         @param managementflag:         Defines if the backplane is used as a management backplane. Not modified if empty.
        *         @type managementflag:          boolean
        *         @param storageflag:            Defines if the backplane is used as a storage backplane. Not modified if empty.
        *         @type storageflag:             boolean
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setFlags (backplaneguid:String,publicflag:Boolean=false,managementflag:Boolean=false,storageflag:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setFlags', setFlags_ResultReceived, getError, backplaneguid,publicflag,managementflag,storageflag,jobguid,executionparams);

        }

        private function setFlags_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETFLAGS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the backplane rootobject.
        *         
        *         @execution_method = sync
        *         @param backplaneguid:    Guid of the backplane rootobject
        *         @type backplaneguid:     guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 XML representation of the backplane
        *         @rtype:                  string
        *         @raise e:                In case an error occurred, exception is raised
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function getXML (backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, backplaneguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of backplane guids which met the find criteria.
        *         
        *         @execution_method = sync
        *         @param name:                    Name of the backplanes to include in the search criteria.
        *         @type name:                     string
        *         @param managementflag:          managementflag of the backplanes to include in the search criteria.
        *         @type managementflag:           boolean
        *         @param publicflag:              publicflag of the backplanes to include in the search criteria.
        *         @type publicflag:               boolean
        *         @param storageflag:             storageflag of the backplanes to include in the search criteria.
        *         @type storageflag:              boolean
        *         @param backplanetype:           Type of the backplanes to include in the search criteria.
        *         @type backplanetype:            int
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of backplane guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,managementflag:Object=null,publicflag:Object=null,storageflag:Object=null,backplanetype:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,managementflag,publicflag,storageflag,backplanetype,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTRESOURCEGROUPS:String = 'listResourcegroups_response';
        /**
        *         List of all related resourcegroups to the backplane.
        *         @execution_method = sync
        *         
        *         @param backplaneguid:           Guid of the backplane rootobject
        *         @type backplaneguid:            guid
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of resourcegroups info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listResourcegroups (backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listResourcegroups', listResourcegroups_ResultReceived, getError, backplaneguid,jobguid,executionparams);

        }

        private function listResourcegroups_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTRESOURCEGROUPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a backplane.
        *         @param backplaneguid:          Guid of the backplane rootobject to delete.
        *         @type backplaneguid:           guid
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function deleteBackplane (backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteBackplane', delete_ResultReceived, getError, backplaneguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

