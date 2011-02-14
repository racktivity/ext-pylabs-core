
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Lan extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_lan';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Lan()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTVDCS:String = 'listVdcs_response';
        /**
        *         List the vdcs the lan is used in.
        *         @execution_method = sync
        *         @param languid:                    guid of the lan to list the vdcs for.
        *         @type languid:                     guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function listVdcs (languid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listVdcs', listVdcs_ResultReceived, getError, languid,jobguid,executionparams);

        }

        private function listVdcs_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTVDCS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         @param rootobjectguid:    guid of the lan rootobject
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




        public const EVENTTYPE_SETFROMIPTOIP:String = 'setFromIpToIp_response';
        /**
        *         Configures the network for the specified LAN.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param fromip:                 Network address for the LAN
        *         @type fromip:                  string
        *         @param toip:                   Defines if the LAN is used as a management LAN
        *         @type toip:                    string
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setFromIpToIp (languid:String,fromip:String,toip:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setFromIpToIp', setFromIpToIp_ResultReceived, getError, languid,fromip,toip,jobguid,executionparams);

        }

        private function setFromIpToIp_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETFROMIPTOIP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETFLAGS:String = 'setFlags_response';
        /**
        *         Sets the role flags for the specified LAN.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param publicflag:             Defines if the LAN is used as a public LAN. Not modified if empty.
        *         @type publicflag:              boolean
        *         @param managementflag:         Defines if the LAN is used as a management LAN. Not modified if empty.
        *         @type managementflag:          boolean
        *         @param storageflag:            Defines if the LAN is used as a storage LAN. Not modified if empty.
        *         @type storageflag:             boolean
        *         
        *         @param internetpublicflag:     Defines if the LAN is used as a internet public LAN. e.g a public lan with extra security constraints.
        *         @type internetpublicflag:      boolean
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setFlags (languid:String,publicflag:Boolean=false,managementflag:Boolean=false,storageflag:Boolean=false,internetpublicflag:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setFlags', setFlags_ResultReceived, getError, languid,publicflag,managementflag,storageflag,internetpublicflag,jobguid,executionparams);

        }

        private function setFlags_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETFLAGS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of LAN guids which met the find criteria.
        *         @execution_method = sync
        *         @param backplaneguid:           guid of the backplane to include in the search criteria.
        *         @type backplaneguid:            guid
        *         @param cloudspaceguid:          guid of the cloudspace to include in the search criteria.
        *         @type cloudspaceguid:           guid
        *         @param parentlanguid:           guid of the parent lan to include in the search criteria.
        *         @type parentlanguid:            guid
        *         @param name:                    Name of the lans to include in the search criteria.
        *         @type name:                     string
        *         @param dns:                     DNS of the lans to include in the search criteria.
        *         @type dns:                      string
        *         @param status:                  Status of the lans to include in the search criteria. See listStatuses().
        *         @type status:                   string
        *         @param startip:                 startip of the lans to include in the search criteria.
        *         @type startip:                  string
        *         @param endip:                   endip of the lans to include in the search criteria.
        *         @type endip:                    string
        *         @param gateway:                 gateway of the lans to include in the search criteria.
        *         @type gateway:                  string
        *         @param managementflag:          managementflag of the lans to include in the search criteria.
        *         @type managementflag:           boolean
        *         @param publicflag:              publicflag of the lans to include in the search criteria.
        *         @type publicflag:               boolean
        *         @param storageflag:             storageflag of the lans to include in the search criteria.
        *         @type storageflag:              boolean
        *         @param network:                 network of the lans to include in the search criteria.
        *         @type network:                  string
        *         @param netmask:                 netmask of the lans to include in the search criteria.
        *         @type netmask:                  string
        *         @param vlantag:                 vlan tag of the lans to include in the search criteria.
        *         @type vlantag:                  int
        *         @param lantype:                 Type the lan (static of dynamic)
        *         @type lantype:                  string
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of lan guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (backplaneguid:Object=null,cloudspaceguid:Object=null,name:Object=null,dns:Object=null,status:Object=null,startip:Object=null,endip:Object=null,gateway:Object=null,managementflag:Object=null,publicflag:Object=null,storageflag:Object=null,network:Object=null,netmask:Object=null,parentlanguid:Object=null,vlantag:Object=null,lantype:Object=null,dhcpflag:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, backplaneguid,cloudspaceguid,name,dns,status,startip,endip,gateway,managementflag,publicflag,storageflag,network,netmask,parentlanguid,vlantag,lantype,dhcpflag,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTMACRANGES:String = 'listMacRanges_response';
        /**
        *         Returns the macranges define on lans
        *         @execution_method = sync
        *         @param publicflag:                 Filter on public flag on lan
        *         @type publicflag:                  boolean
        *         
        *         @param managementflag:             Filter on management flag on lan
        *         @type managementflag:              boolean
        *                 
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           list of dictionary {'guid','name','macrange','publicflag','managementflag'}
        *         @rtype:                            list
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function listMacRanges (publicflag:Boolean=false,managementflag:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listMacRanges', listMacRanges_ResultReceived, getError, publicflag,managementflag,jobguid,executionparams);

        }

        private function listMacRanges_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTMACRANGES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVETOCLOUDSPACE:String = 'moveToCloudspace_response';
        /**
        *         Moves the specified LAN to the another space.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param spaceguid:              guid of the space to move the LAN to
        *         @type spaceguid:               guid
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function moveToCloudspace (languid:String,spaceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveToCloudspace', moveToCloudspace_ResultReceived, getError, languid,spaceguid,jobguid,executionparams);

        }

        private function moveToCloudspace_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVETOCLOUDSPACE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new lan
        *         @param cloudspaceguid:         guid of the space this lan is part of
        *         @type cloudspaceguid:          guid
        *         @param backplaneguid:          guid of the backplane this lan is part of
        *         @type backplaneguid:           guid
        *         @param name:                   Name the lan
        *         @type name:                    string
        *         @param lantype:                Type the lan (static of dynamic)
        *         @type lantype:                 string
        *         
        *         @param parentlanguid:          guid of the lan's parent lan
        *         @type parentlanguid:           guid
        *         
        *         @param network:                Network address for the LAN
        *         @type network:                 string
        *         @param netmask:                Netmask for the LAN
        *         @type netmask:                 string
        *         
        *         @param fromip:                 Network address for the LAN
        *         @type fromip:                  string
        *         @param toip:                   Defines if the LAN is used as a management LAN
        *         @type toip:                    string
        *         
        *         @param gateway:                Address of the default gateway.
        *         @type gateway:                 string
        *         
        *         @param dns:                    Address of the DNS server.
        *         @type dns:                     string
        *         
        *         @param publicflag:             Defines if the LAN is used as a public LAN. Not modified if empty.
        *         @type publicflag:              boolean
        *         
        *         @param internetpublicflag:     Defines if the LAN is used as a internet public LAN. Not modified if empty.
        *         @type internetpublicflag:      boolean
        *         
        *         @param managementflag:         Defines if the LAN is used as a management LAN. Not modified if empty.
        *         @type managementflag:          boolean
        *         
        *         @param storageflag:            Defines if the LAN is used as a storage LAN. Not modified if empty.
        *         @type storageflag:             boolean
        *          
        *         @param description:            Description of the LAN
        *         @type description:             string
        *         
        *         @param integratedflag:         True if the lan is a integrated network or not, default false, because only used for public networks
        *         @type integratedflag:          boolean
        *         
        *         @param nrreservedip:           Number of reserved ip addresses for the sso nodes
        *         @type  nrreservedip:           integer
        *         
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with languid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         @note:                         Administrators only
        *         
        */
        public function create (cloudspaceguid:String,backplaneguid:String,name:String,lantype:String,parentlanguid:String="",network:String="",netmask:String="",fromip:String="",toip:String="",gateway:String="",dns:String="",publicflag:Boolean=false,internetpublicflag:Boolean=false,managementflag:Boolean=false,storageflag:Boolean=false,description:String="",integratedflag:Boolean=false,nrreservedip:Number=-1,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, cloudspaceguid,backplaneguid,name,lantype,parentlanguid,network,netmask,fromip,toip,gateway,dns,publicflag,internetpublicflag,managementflag,storageflag,description,integratedflag,nrreservedip,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETSTATUS:String = 'setStatus_response';
        /**
        *         Configures the status for the specified LAN.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param status:                 Status of the LAN ("BROKEN", "ACTIVE", "DISABLED", "NOTCONNECTED)
        *         @type status:                  string
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setStatus (languid:String,status:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setStatus', setStatus_ResultReceived, getError, languid,status,jobguid,executionparams);

        }

        private function setStatus_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETSTATUS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties
        *         @param languid:                 Guid of the LAN to update.
        *         @type languid:                  guid
        *         @param name:                    Name of the lan.
        *         @type name:                     string
        *         @param description:             Description of the lan.
        *         @type description:              string
        *         @param gateway:                 Gateway of the lan.
        *         @type gateway:                  string
        *         @param network:                 Network of the lan.
        *         @type network:                  string
        *         @param netmask:                 Netmask of the lan.
        *         @type netmask:                  string
        *         @param startip:                 Startip of the lans to include in the search criteria.
        *         @type startip:                  string
        *         @param endip:                   Endip of the lans to include in the search criteria.
        *         @type endip:                    string
        *         @param jobguid:                 Guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Dictionary with lan guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (languid:String,name:String="",description:String="",gateway:String="",network:String="",netmask:String="",startip:String="",endip:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, languid,name,description,gateway,network,netmask,startip,endip,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETNEXTMACRANGE:String = 'getNextMacRange_response';
        /**
        *         Get the next mac range for a qlan
        *         @execution_method = sync
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function getNextMacRange (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getNextMacRange', getNextMacRange_ResultReceived, getError, jobguid,executionparams);

        }

        private function getNextMacRange_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETNEXTMACRANGE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CHECKIPRANGEINUSE:String = 'checkIPRangeInUse_response';
        /**
        *         Check if this ip range conflicts with any existing ip range, return true if it conflicts, false otherwise
        *         
        *         @param startip:                    Start ip of the range
        *         @type startip:                     string
        *         
        *         @param endip:                      End ip of the range
        *         @type endip:                       string
        *                 
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           array of the existing lans that conflict with this range ({'result': array, 'jobguid': guid})
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function checkIPRangeInUse (startip:String,endip:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'checkIPRangeInUse', checkIPRangeInUse_ResultReceived, getError, startip,endip,jobguid,executionparams);

        }

        private function checkIPRangeInUse_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CHECKIPRANGEINUSE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETLANTYPE:String = 'setLanType_response';
        /**
        *         Configures the LAN type for the specified LAN.
        *         @param languid:                guid of the lan
        *         @type languid:                 guid
        *         @param lantype:                Type of LAN
        *         @type lantype:                 integer
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setLanType (languid:String,lantype:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setLanType', setLanType_ResultReceived, getError, languid,lantype,jobguid,executionparams);

        }

        private function setLanType_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETLANTYPE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETNETWORKNETMASK:String = 'setNetworkNetmask_response';
        /**
        *         Configures the network for the specified LAN.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param network:                Network address for the LAN
        *         @type network:                 string
        *         @param netmask:                Netmask for the LAN
        *         @type netmask:                 string
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setNetworkNetmask (languid:String,network:String,netmask:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setNetworkNetmask', setNetworkNetmask_ResultReceived, getError, languid,network,netmask,jobguid,executionparams);

        }

        private function setNetworkNetmask_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETNETWORKNETMASK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTIPADDRESSES:String = 'listIPAddresses_response';
        /**
        *         List all IP addresses for a lan.
        *         @execution_method = sync
        *         @param languid:                    guid of the lan to list the ips for.
        *         @type languid:                     guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'ipaddress': '10.100.0.1',
        *         @note:                                          'netmask': '255.255.0.0',
        *         @note:                                          'guid': '789544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'ispublic': False},
        *         @note:                                        { 'ipaddress': '10.100.0.5',
        *         @note:                                          'netmask': '255.255.0.0',
        *         @note:                                          'guid': '888544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'ispublic': False}]}
        *         
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function listIPAddresses (languid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listIPAddresses', listIPAddresses_ResultReceived, getError, languid,jobguid,executionparams);

        }

        private function listIPAddresses_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTIPADDRESSES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETDNS:String = 'setDNS_response';
        /**
        *         Configures the domain name server for the specified LAN.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param dns:                    Address of the DNS server.
        *         @type dns:                     string
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setDNS (languid:String,dns:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setDNS', setDNS_ResultReceived, getError, languid,dns,jobguid,executionparams);

        }

        private function setDNS_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETDNS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the lan rootobject.
        *         @execution_method = sync
        *         @param languid:                guid of the lan rootobject
        *         @type languid:                 guid
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       XML representation of the lan
        *         @rtype:                        string
        *         @raise e:                      In case an error occurred, exception is raised
        *         @todo:                         Will be implemented in phase2
        *         
        */
        public function getXML (languid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, languid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETDEFAULTGATEWAY:String = 'setDefaultGateway_response';
        /**
        *         Configures the default gateway for the specified LAN.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param gateway:                Address of the default gateway.
        *         @type gateway:                 string
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setDefaultGateway (languid:String,gateway:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setDefaultGateway', setDefaultGateway_ResultReceived, getError, languid,gateway,jobguid,executionparams);

        }

        private function setDefaultGateway_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETDEFAULTGATEWAY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the lan rootobject structure.
        *         @execution_method = sync
        *         @param languid:                guid of the lan rootobject
        *         @type languid:                 guid
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       XSD representation of the disk structure.
        *         @rtype:                        string
        *         @raise e:                      In case an error occurred, exception is raised
        *         @todo:                         Will be implemented in phase2
        *         
        */
        public function getXMLSchema (languid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, languid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVETOBACKPLANE:String = 'moveToBackplane_response';
        /**
        *         Moves the specified LAN to the another backplane.
        *         @param languid:                guid of the LAN
        *         @type languid:                 guid
        *         @param backplaneguid:          guid of the backplane to move the LAN to
        *         @type backplaneguid:           guid
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         @note: Administrator only
        *         
        */
        public function moveToBackplane (languid:String,backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveToBackplane', moveToBackplane_ResultReceived, getError, languid,backplaneguid,jobguid,executionparams);

        }

        private function moveToBackplane_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVETOBACKPLANE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         List all lans.
        *         @returns array of array [[$lanName,"public" or "private",$nrOfIpAddresses,$nrOfFreeIPAddresses,$description]]
        *         @execution_method = sync
        *         @param cloudspaceguid:             guid of the cloud space to list the lans for. If not specified, return all lans you have access to.
        *         @type cloudspaceguid:              guid
        *         @param backplaneguid:              guid of the backplane to list the lans for. If not specified, return all lans you have access to.
        *         @type backplaneguid:               guid
        *         @param languid:                    guid of the LAN
        *         @type languid:                     guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of lan info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'cloudspaceguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'backplaneguid': '55544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'languid': '75544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'parentlanguid': '45544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'Office Lan',
        *         @note:                                          'description': 'Our Office Lan',
        *         @note:                                          'lantype': 'STATIC',
        *         @note:                                          'public': False,
        *         @note:                                          'storage': False,
        *         @note:                                          'management': False},
        *         @note:                                        { 'cloudspaceguid': '789544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'backplaneguid': '78644B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'languid': '78644B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'parentlanguid': '74844B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'name': 'Internet Feed',
        *         @note:                                          'description': 'Our Public Lan',
        *         @note:                                          'lantype': 'DYNAMIC',
        *         @note:                                          'public': True,
        *         @note:                                          'storage': False,
        *         @note:                                          'management': False}]}
        *         
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function list (cloudspaceguid:Object=null,backplaneguid:Object=null,languid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, cloudspaceguid,backplaneguid,languid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the lan rootobject.
        *         @execution_method = sync
        *         @param languid:                guid of the lan rootobject
        *         @type languid:                 guid
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       YAML representation of the disk
        *         @rtype:                        string
        *         
        */
        public function getYAML (languid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, languid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTFREEIPADDRESSES:String = 'listFreeIPAddresses_response';
        /**
        *         List the free ip addresses for a lan.
        *         @execution_method = sync
        *         @param languid:                    guid of the lan to list the ips for.
        *         @type languid:                     guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                              'result: [{ 'ipaddress': '10.100.0.1',
        *         @note:                                          'netmask': '255.255.0.0',
        *         @note:                                          'guid': '789544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'ispublic': False},
        *         @note:                                        { 'ipaddress': '10.100.0.5',
        *         @note:                                          'netmask': '255.255.0.0',
        *         @note:                                          'guid': '888544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                                          'ispublic': False}]}
        *         
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function listFreeIPAddresses (languid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listFreeIPAddresses', listFreeIPAddresses_ResultReceived, getError, languid,jobguid,executionparams);

        }

        private function listFreeIPAddresses_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTFREEIPADDRESSES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETVLANTAG:String = 'setVlanTag_response';
        /**
        *         Configures the VLAN tag for the specified LAN.
        *         @param languid:                guid of the lan
        *         @type languid:                 guid
        *         @param vlantag:                VLAN tag
        *         @type vlantag:                 integer
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function setVlanTag (languid:String,vlantag:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setVlanTag', setVlanTag_ResultReceived, getError, languid,vlantag,jobguid,executionparams);

        }

        private function setVlanTag_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETVLANTAG, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes s lan.
        *         @param languid:                guid of the lan to delete
        *         @type languid:                 guid
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function deleteLan (languid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteLan', delete_ResultReceived, getError, languid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

