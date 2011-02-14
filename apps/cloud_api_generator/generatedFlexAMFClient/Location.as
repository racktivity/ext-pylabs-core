
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Location extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_location';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Location()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the location rootobject structure.
        *         @execution_method = sync
        *         
        *         @param locationguid:            Guid of the location rootobject
        *         @type locationguid:             guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the location structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (locationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, locationguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new location.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   Name for the location.
        *         @type name:                    string
        *         @param description:            Description for the location.
        *         @type description:             string
        *         @param alias:                  Alias for the location.
        *         @type alias:                   string
        *         @param address:                Address for the location.
        *         @type address:                 string
        *         @param city:                   City for the location.
        *         @type city:                    string
        *         @param country:                Country for the location.
        *         @type country:                 string
        *         @param public:                 Indicates if the location is a public location.
        *         @type public:                  boolean
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with locationguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,description:String="",alias:String="",address:String="",city:String="",country:String="",ispublic:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,description,alias,address,city,country,public,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all locations.
        *         @execution_method = sync
        *         
        *         @param locationguid:            Guid of the location specified
        *         @type locationguid:             guid
        *         @security administrators
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of location info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                          'result: [{ 'locationguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                      'name': 'LOCATION0001',
        *         @note:                                      'description': 'Location 0001',
        *         @note:                                      'alias': 'LOC-0001',
        *         @note:                                      'address': 'Antwerpsesteenweg 19',
        *         @note:                                      'city': 'Lochristi'
        *         @note:                                      'country': 'Belgium'
        *         @note:                                      'public': False},
        *         @note:                                    { 'locationguid': '1351F79F-D65A-4F65-A96B-AC4A6246C033',
        *         @note:                                      'name': 'LOCATION0001',
        *         @note:                                      'description': 'Location 0001',
        *         @note:                                      'alias': 'LOC-0001',
        *         @note:                                      'address': 'Antwerpsesteenweg 19',
        *         @note:                                      'city': 'Lochristi'
        *         @note:                                      'country': 'Belgium'
        *         @note:                                      'public': False}]}
        *         
        */
        public function list (locationguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, locationguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the location rootobject.
        *         @execution_method = sync
        *         
        *         @param locationguid:          Guid of the location rootobject
        *         @type locationguid:           guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      YAML representation of the location
        *         @rtype:                       string
        *         
        */
        public function getYAML (locationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, locationguid,jobguid,executionparams);

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
        *         @param rootobjectguid:        Guid of the location rootobject
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
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param locationguid:           Guid of the location specified
        *         @type locationguid:            guid
        *         @param name:                   Name for the location.
        *         @type name:                    string
        *         @param description:            Description for the location.
        *         @type description:             string
        *         @param alias:                  Alias for the location.
        *         @type alias:                   string
        *         @param address:                Address for the location.
        *         @type address:                 string
        *         @param city:                   City for the location.
        *         @type city:                    string
        *         @param country:                Country for the location.
        *         @type country:                 string
        *         @param public:                 Indicates if the location is a public location.
        *         @type public:                  boolean
        *         @param timezonename:           name of timeZone for the location.
        *         @type timezonename:            string
        *         @param timezonedelta:          delta of timeZone for the location.
        *         @type timezonedelta:           float
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with location guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (locationguid:String,name:String="",description:String="",alias:String="",address:String="",city:String="",country:String="",ispublic:Boolean=false,timezonename:String="",timezonedelta:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, locationguid,name,description,alias,address,city,country,public,timezonename,timezonedelta,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTDATACENTERS:String = 'listDatacenters_response';
        /**
        *         List all datacenters of the location.
        *         
        *         @execution_method = sync
        *         
        *         @param locationguid:            Guid of the location rootobject
        *         @type locationguid:             guid
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of datacenters
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listDatacenters (locationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listDatacenters', listDatacenters_ResultReceived, getError, locationguid,jobguid,executionparams);

        }

        private function listDatacenters_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTDATACENTERS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the location rootobject.
        *         @execution_method = sync
        *         
        *         @param locationguid:            Guid of the location rootobject
        *         @type locationguid:             guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the location
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (locationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, locationguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETTIMEZONE:String = 'setTimeZone_response';
        /**
        *         Changes the time zone for a certain location
        *         
        *         @security administrators
        *         
        *         @param locationguid:            Guid of the location rootobject
        *         @type locationguid:             guid
        *         
        *         @param timezonename:            name of timeZone for the location.
        *         @type timezonename:             string
        *         @param timezonedelta:           delta of timeZone for the location.
        *         @type timezonedelta:            float
        *         
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         
        *         @return:                        dictionary with True as a result when succeeded
        *         @rtype:                         dictionary
        *         
        *         @raise e:                       In case an error occurred, exception is raised        
        *         
        */
        public function setTimeZone (locationguid:String,timezonename:String,timezonedelta:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setTimeZone', setTimeZone_ResultReceived, getError, locationguid,timezonename,timezonedelta,jobguid,executionparams);

        }

        private function setTimeZone_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETTIMEZONE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of location guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param name:                   Name for the location.
        *         @type name:                    string
        *         @param description:            Description for the location.
        *         @type description:             string
        *         @param alias:                  Alias for the location.
        *         @type alias:                   string
        *         @param address:                Address for the location.
        *         @type address:                 string
        *         @param city:                   City for the location.
        *         @type city:                    string
        *         @param country:                Country for the location.
        *         @type country:                 string
        *         @param public:                 Indicates if the location is a public location.
        *         @type public:                  boolean
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Array of location guids which met the find criteria specified.
        *         @rtype:                        array
        *         @note:                         Example return value:
        *         @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,description:Object=null,alias:Object=null,address:Object=null,city:Object=null,country:Object=null,ispublic:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,alias,address,city,country,public,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a location.
        *         @execution_method = sync
        *         
        *         @security administrators
        *         @param locationguid:          Guid of the location rootobject to delete.
        *         @type locationguid:           guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function deleteLocation (locationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteLocation', delete_ResultReceived, getError, locationguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

