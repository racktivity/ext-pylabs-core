
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Capacityplanning extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_capacityplanning';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Capacityplanning()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTCAPACITYUNITTYPES:String = 'listCapacityUnitTypes_response';
        /**
        *         Returns a list of possible capacity unit types.
        *         @execution_method = sync
        *         
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         e.g. ["machine","sdsd-2323232-fsfd","machine_kds1",]
        *         the names of the filenames will be $destUncPath/$the3eArrayElement.rootobject.7z
        *             e.g. dss://login:passwd@backup_machinex/myroot/backups/rootobjects/10-10-2009/machine_kds1.rootobject.7z
        *         @return:                  Dictionary of array of capacity types.
        *         @rtype:                   dictionary
        *         @note:                    Example return value:
        *         @note:                    {'result': '["CU", "LV", "MU", "NBU", "NUIPPORTS", "NUM", "SUA", "SUP", "WV"]',
        *         @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function listCapacityUnitTypes (jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listCapacityUnitTypes', listCapacityUnitTypes_ResultReceived, getError, jobguid,executionparams);

        }

        private function listCapacityUnitTypes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCAPACITYUNITTYPES, false, false, e.result));
            srv.disconnect();
        }


    }
}

