
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Os extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_os';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Os()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the os rootobject structure.
        *         @execution_method = sync
        *         
        *         @param osguid:                guid of the os rootobject
        *         @type osguid:                 guid
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      XSD representation of the os structure.
        *         @rtype:                       string
        *         @raise e:                     In case an error occurred, exception is raised
        *         @todo:                        Will be implemented in phase2
        *         
        */
        public function getXMLSchema (osguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, osguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of all known operating systems.
        *         @execution_method = sync
        *         
        *         @param osguid:               guid of the os rootobject
        *         @type osguid:                guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of operating system info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         @note:                       {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                        'result: [{ 'osguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                    'name': 'Windows XP',
        *         @note:                                    'description': 'Microsoft Windows XP',
        *         @note:                                    'iconname': 'WinXP.png',
        *         @note:                                    'osversion': 'Service Pack 2',
        *         @note:                                    'patchlevel': '',
        *         @note:                                    'type': 'WINDOWS'}]}
        *         
        */
        public function list (osguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, osguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the os rootobject.
        *         @execution_method = sync
        *         
        *         @param diskguid:                guid of the os rootobject
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @return:                        YAML representation of the os
        *         @rtype:                         string
        *         
        */
        public function getYAML (osguid:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, osguid,jobguid,executionparams);

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
        *         @param rootobjectguid:    guid of the os object
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




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the os rootobject.
        *         @execution_method = sync
        *         
        *         @param osguid:                guid of the os rootobject
        *         @type osguid:                 guid
        *         @param jobguid:               guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      XML representation of the os
        *         @rtype:                       string
        *         @raise e:                     In case an error occurred, exception is raised
        *         @todo:                        Will be implemented in phase2
        *         
        */
        public function getXML (osguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, osguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of os guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:               Name of the os.
        *         @type name:                string
        *         @param ostype:             Os type.
        *         @type ostype:              string
        *         @param iconname:           filename of icon representing os in various clouduser interfaces
        *         @type iconname:            string
        *         @param osversion:          version of the operating system
        *         @type osversion:           string
        *         @param patchlevel:         patch level of operating system
        *         @type patchlevel:          string
        *         @param description:        description of the operating system
        *         @type description:         string
        *         
        *         @param osbitversion:          bit version of the operating system e.g. 32-bit , 64-bit
        *         @type osbitversion:           string
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with an array of os guids as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function find (name:String="",ostype:String="",iconname:String="",osversion:String="",patchlevel:String="",description:String="",osbitversion:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,ostype,iconname,osversion,patchlevel,description,osbitversion,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }


    }
}

