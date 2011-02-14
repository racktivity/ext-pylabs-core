
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Application extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_application';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Application()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTVDCS:String = 'listVdcs_response';
        /**
        *         List the vdcs the application is used in.
        *         @execution_method = sync
        *         @param applicationguid:   guid of the application to list the vdcs for.
        *         @type applicationguid:    guid
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary of array of dictionaries with guid, name, description, status, template, applicationtemplateguid, machineguid, machinename, cloudspaceguid, cloudspacename of the application.
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function listVdcs (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listVdcs', listVdcs_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function listVdcs_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTVDCS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESTORE:String = 'restore_response';
        /**
        *         @param sourceapplicationguid is the application which is in backedup state in drp
        *         
        *         @param destinationapplicationguid is application where will be restored to if not specified will be the original application where the backup originated from
        *         
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @todo:                   Will be implemented in phase2
        *         
        */
        public function restore (sourceapplicationguid:Object,destinationapplicationguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'restore', restore_ResultReceived, getError, sourceapplicationguid,destinationapplicationguid,jobguid,executionparams);

        }

        private function restore_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESTORE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVENETWORKSERVICE:String = 'removeNetworkService_response';
        /**
        *         Removes a network service for the application specified.
        *         @execution_method = sync
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of network service .
        *         @type servicename:           string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeNetworkService (applicationguid:String,servicename:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeNetworkService', removeNetworkService_ResultReceived, getError, applicationguid,servicename,jobguid,executionparams);

        }

        private function removeNetworkService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVENETWORKSERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVESERVICE:String = 'removeService_response';
        /**
        *         Removes a service for the application specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service .
        *         @type servicename:           string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeService (applicationguid:String,servicename:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeService', removeService_ResultReceived, getError, applicationguid,servicename,jobguid,executionparams);

        }

        private function removeService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVESERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXISTS:String = 'exists_response';
        /**
        *         Returns a dict with following key/value pairs: templateguid, applicationguid, machineguid
        *         which met the find criteria.
        *         @param templatename:          name of the parent template to include in the search criteria.
        *         @type templatename:           string
        *         @param machineguid:           guid of the machine to include in the search criteria.
        *         @type machineguid:            guid
        *         
        *         @param customer:              Flag whether the application is system or customer application
        *         @type customer:               boolean
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      Dict of which met the find criteria specified.
        *         @rtype:                       array
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function exists (templatename:String="",machineguid:String="",customer:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exists', exists_ResultReceived, getError, templatename,machineguid,customer,jobguid,executionparams);

        }

        private function exists_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXISTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REVOKESERVICETODEVICE:String = 'revokeServiceToDevice_response';
        /**
        *         Revokes a service for the device specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to revoke. Name must be unique!
        *         @type servicename:           string
        *         @param deviceguid:           guid of the device to which to revoke the service specified
        *         @type deviceguid:            guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function revokeServiceToDevice (applicationguid:String,servicename:String,deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'revokeServiceToDevice', revokeServiceToDevice_ResultReceived, getError, applicationguid,servicename,deviceguid,jobguid,executionparams);

        }

        private function revokeServiceToDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REVOKESERVICETODEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTACCOUNTTYPES:String = 'listAccountTypes_response';
        /**
        *         Returns a list of possible application account types.
        *         @execution_method = sync
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of application account types.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '["PUBLICACCOUNT", "SYSTEMACCOUNT"]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listAccountTypes (jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listAccountTypes', listAccountTypes_ResultReceived, getError, jobguid,executionparams);

        }

        private function listAccountTypes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTACCOUNTTYPES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTMONITORINGINFO:String = 'listMonitoringInfo_response';
        /**
        *         Retrieve application monitoring info used for the given machine
        *         @execution_method = sync
        *         @param machineguid:        guid of the machineguid running the application
        *         @type machineguid:         guid
        *         @param jobguid:            guid of the job if available else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with  application, port, ipaddress
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function listMonitoringInfo (machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listMonitoringInfo', listMonitoringInfo_ResultReceived, getError, machineguid,jobguid,executionparams);

        }

        private function listMonitoringInfo_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTMONITORINGINFO, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCHILDAPPLICATIONS:String = 'getChildApplications_response';
        /**
        *         Retrieve application template used to create the given application
        *         
        *         @execution_method = sync
        *         
        *         @param applicationguid:    guid of the parent application
        *         @type applicationguid:     guid
        *         @param jobguid:            guid of the job if available else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with applicationtemplate guid and applicationtemplate name as result and jobguid: {'result': {'guid':'58aef606-d30c-4ac4-b79c-f2ea955011f9', 'name':'dhcpserver'}, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function getChildApplications (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getChildApplications', getChildApplications_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function getChildApplications_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCHILDAPPLICATIONS, false, false, e.result));
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




        public const EVENTTYPE_INITIALIZE:String = 'initialize_response';
        /**
        *         Performs initialization actions on the application specified. As a result the application will be ready to be used.
        *         @security administrators
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function initialize (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'initialize', initialize_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function initialize_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_INITIALIZE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REVOKESERVICETONETWORKZONE:String = 'revokeServiceToNetworkZone_response';
        /**
        *         Revokes a service for the network zone specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to revoke. Name must be unique!
        *         @type servicename:           string
        *         @param networkzoneguid:      guid of the network zone to which to revoke the service specified
        *         @type networkzoneguid:       guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function revokeServiceToNetworkZone (applicationguid:String,servicename:String,networkzoneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'revokeServiceToNetworkZone', revokeServiceToNetworkZone_ResultReceived, getError, applicationguid,servicename,networkzoneguid,jobguid,executionparams);

        }

        private function revokeServiceToNetworkZone_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REVOKESERVICETONETWORKZONE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCAPACITYPROVIDED:String = 'addCapacityProvided_response';
        /**
        *         Adds provided capacity for the application specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param amount:               Amount of capacity units to add
        *         @type amount:                integer
        *         @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param name:                 Name of capacity units to add.
        *         @type name:                  string
        *         @param description:          Description of capacity units to add.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addCapacityProvided (applicationguid:String,amount:Number,capacityunittype:String,name:String="",description:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addCapacityProvided', addCapacityProvided_ResultReceived, getError, applicationguid,amount,capacityunittype,name,description,jobguid,executionparams);

        }

        private function addCapacityProvided_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCAPACITYPROVIDED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDACCOUNT:String = 'addAccount_response';
        /**
        *         Adds an account for the application specified.
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param login:                    Login for the new  account.
        *         @type login:                     string
        *         @param password:                 Password for the new account.
        *         @type password:                  string
        *         @param accounttype:              Type for the new account. See listAccountTypes().
        *         @type accounttype:               string
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function addAccount (applicationguid:String,login:String,password:String,accounttype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addAccount', addAccount_ResultReceived, getError, applicationguid,login,password,accounttype,jobguid,executionparams);

        }

        private function addAccount_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDACCOUNT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of application guids which met the find criteria.
        *         @execution_method = sync
        *         @param cloudspaceguid:          Guid of the cloudspace to include in the search criteria.
        *         @type cloudspaceguid:           guid
        *         @param machineguid:             Guid of the machine to include in the search criteria.
        *         @type machineguid:              guid
        *         @param name:                    Name of the application to include in the search criteria.
        *         @type name:                     string
        *         @param status:                  Status of the  application to include in the search criteria. See listStatuses().
        *         @type status:                   string
        *         @param istemplate:              Indicate if the application is a template
        *         @type istemplate:               boolean
        *         @param customer:                Flag whether the application is system or customer application
        *         @type customer:                 boolean
        *         
        *         @param mode:                    Mode of the application (eg readonly...)
        *         @type mode:                     string
        *         
        *         @param monitor:                 Monitor flag
        *         @type monitor:                  boolean
        *         
        *         @param jobguid:                 guid of the job if available else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of application guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (cloudspaceguid:Object=null,machineguid:Object=null,name:Object=null,status:Object=null,istemplate:Object=null,customer:Object=null,mode:Object=null,monitor:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, cloudspaceguid,machineguid,name,status,istemplate,customer,mode,monitor,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OFFERSERVICETOAPPLICATION:String = 'offerServiceToApplication_response';
        /**
        *         Offers a service for the application specified.
        *         @param applicationguid:            guid of the application specified
        *         @type applicationguid:             guid
        *         @param servicename:                Name of service to add. Name must be unique!
        *         @type servicename:                 string
        *         @param destinationapplicationguid: guid of the application to which to offer the service specified
        *         @type destinationapplicationguid:  guid
        *         @param remark:                     Remark to add to this service offer.
        *         @type type:                        string
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function offerServiceToApplication (applicationguid:String,servicename:String,destinationapplicationguid:String,remark:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'offerServiceToApplication', offerServiceToApplication_ResultReceived, getError, applicationguid,servicename,destinationapplicationguid,remark,jobguid,executionparams);

        }

        private function offerServiceToApplication_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OFFERSERVICETOAPPLICATION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATEFROMTEMPLATE:String = 'createFromTemplate_response';
        /**
        *         Creates a new application, does not provision application yet
        *         @param cloudspaceguid:                   guid of the cloud space related to this application
        *         @type cloudspaceguid:                    guid
        *         @param machineguid:                      guid of the machine related to this application
        *         @type machineguid:                       guid
        *         @param applicationtemplateguid:          guid of the applicationtemplate to create this application from
        *         @type applicationtemplateguid:           guid
        *         @param name:                             Name for this new application. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                              string
        *         @param description:                      Description for this new application. This is free text describing the purpose of the application, if multi-line use back-slash + 
        *         @type description:                       string
        *         @param customsettings:                   Custom settings for this new application.
        *         @type customsettings:                    string
        *         
        *         @param customer:                         Flag whether the application is system or customer application
        *         @type customer:                          boolean
        *         @param jobguid:                          guid of the job if available else empty string
        *         @type jobguid:                           guid
        *         @param executionparams:                  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:                   dictionary
        *         @return:                                 dictionary with application guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                                  dictionary
        *         @raise e:                                In case an error occurred, exception is raised
        *         remark:                                  An application always lives on top of a machine, the machine also lives in a space, think is good to have both a reference to space
        *         
        */
        public function createFromTemplate (cloudspaceguid:String,machineguid:String,applicationtemplateguid:String,name:String,description:String="",customsettings:String="",customer:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'createFromTemplate', createFromTemplate_ResultReceived, getError, cloudspaceguid,machineguid,applicationtemplateguid,name,description,customsettings,customer,jobguid,executionparams);

        }

        private function createFromTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATEFROMTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_COPY:String = 'copy_response';
        /**
        *         Copies the application specified.
        *         @param sourceapplicationguid:            guid of the application to copy.
        *         @type sourceapplicationguid:             guid
        *         @param destinationapplicationguid:       guid of the target application.
        *         @type destinationapplicationguid:        guid
        *         @param jobguid:                          guid of the job if available else empty string
        *         @type jobguid:                           guid
        *         @param executionparams:                  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:                   dictionary
        *         @return:                                 dictionary with the guid of the new application as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                                  dictionary
        *         @raise e:                                In case an error occurred, exception is raised
        *         
        *         @todo:                                   Will be implemented in phase2
        *         
        */
        public function copy (sourceapplicationguid:String,destinationapplicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'copy', copy_ResultReceived, getError, sourceapplicationguid,destinationapplicationguid,jobguid,executionparams);

        }

        private function copy_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_COPY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OFFERSERVICETODEVICE:String = 'offerServiceToDevice_response';
        /**
        *         Offers a service for the device specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to add. Name must be unique!
        *         @type servicename:           string
        *         @param deviceguid:           guid of the device to which to offer the service specified
        *         @type deviceguid:            guid
        *         @param remark:               Remark to add to this service offer.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function offerServiceToDevice (applicationguid:String,servicename:String,deviceguid:String,remark:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'offerServiceToDevice', offerServiceToDevice_ResultReceived, getError, applicationguid,servicename,deviceguid,remark,jobguid,executionparams);

        }

        private function offerServiceToDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OFFERSERVICETODEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RELOAD:String = 'reload_response';
        /**
        *         Reloads the specified application 
        *         @param applicationguid:  Guid of the application
        *         @type applicationguid:   guid
        *         @param jobguid:          Guid of the job
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        */
        public function reload (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'reload', reload_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function reload_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RELOAD, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVECAPACITYPROVIDED:String = 'removeCapacityProvided_response';
        /**
        *         Removes provided capacity for the application specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeCapacityProvided (applicationguid:String,capacityunittype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeCapacityProvided', removeCapacityProvided_ResultReceived, getError, applicationguid,capacityunittype,jobguid,executionparams);

        }

        private function removeCapacityProvided_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECAPACITYPROVIDED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new application, does not provision application yet
        *         Application does not have to be linked to a machine.
        *         An application can group other applications, these are called cloudservices
        *         @param cloudspaceguid:         guid of the cloud space related to this application
        *         @type cloudspaceguid:          guid
        *         @param machineguid:            guid of the machine related to this application
        *         @type machineguid:             guid
        *         @param name:                   Name for this new application. The name is a freely chosen name, which has to be unique in SPACE.
        *         @type name:                    string
        *         @param description:            Description for this new application. This is free text describing the purpose of the application, if multi-line use back-slash + 
        *         @type description:             string
        *         @param customsettings:         Custom settings for this new application.
        *         @type customsettings:          string
        *         @param parentapplicactionguid: link to application which is cloudservice (modelled as parent application)
        *         @type parentapplicactionguid:  guid
        *         
        *         @param customer:               Flag whether the application is system or customer application
        *         @type customer:                boolean
        *         
        *         @param mode:                   configuration mode (READONLY,READWRITE...)
        *         @type mode:                    string
        *         @param jobguid:                guid of the job if available else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with application guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         remark:                        An application always lives on top of a machine, the machine also lives in a space, think is good to have both a reference to space
        *         
        */
        public function create (cloudspaceguid:String,name:String,machineguid:String="",parentapplicactionguid:String="",description:String="",customsettings:String="",customer:Boolean=false,mode:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, cloudspaceguid,name,machineguid,parentapplicactionguid,description,customsettings,customer,mode,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETSTATUS:String = 'getStatus_response';
        /**
        *         Retrieve status of the given application
        *         
        *         @param applicationguid:  Guid of the application
        *         @type applicationguid:   guid
        *         @param jobguid:          Guid of the job
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        */
        public function getStatus (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getStatus', getStatus_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function getStatus_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETSTATUS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REVOKESERVICETOCLOUDUSER:String = 'revokeServiceToCloudUser_response';
        /**
        *         Revokes a service for the cloud user specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to revoke. Name must be unique!
        *         @type servicename:           string
        *         @param clouduserguid:        guid of the cloud user to which to revoke the service specified
        *         @type clouduserguid:         guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function revokeServiceToCloudUser (applicationguid:String,servicename:String,clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'revokeServiceToCloudUser', revokeServiceToCloudUser_ResultReceived, getError, applicationguid,servicename,clouduserguid,jobguid,executionparams);

        }

        private function revokeServiceToCloudUser_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REVOKESERVICETOCLOUDUSER, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_START:String = 'start_response';
        /**
        *         Starts the application specified.
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param failifnotenoughresource:  Boolean value indicating if application should not start if not enough resources are available.
        *         @type failifnotenoughresource:   boolean
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function start (applicationguid:String,failifnotenoughresource:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'start', start_ResultReceived, getError, applicationguid,failifnotenoughresource,jobguid,executionparams);

        }

        private function start_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_START, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update properties, every parameter which is not passed or passed as empty string is not updated.
        *         @SECURITY administrator only
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param name:                 Name for this application
        *         @type name:                  string
        *         @param description:          Description for this application
        *         @type description:           string
        *         @param status:               Status for this application
        *         @type status:                string
        *         @param customsettings:       Custom settings for this application
        *         @type customsettings:        string
        *         
        *         @param customer:             Flag whether the application is system or customer application
        *         @type customer:              boolean
        *         @param mode:                 Mode of the application (eg readonly...)
        *         @type mode:                  string
        *         
        *         @param monitor:              Monitor flag
        *         @type monitor:               boolean
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with application guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (applicationguid:String,name:String="",description:String="",status:String="",customsettings:String="",customer:Boolean=false,mode:String="",monitor:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, applicationguid,name,description,status,customsettings,customer,mode,monitor,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REVOKESERVICETODISK:String = 'revokeServiceToDisk_response';
        /**
        *         Revokes a service for the disk specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to revoke. Name must be unique!
        *         @type servicename:           string
        *         @param diskguid:             guid of the disk to which to revoke the service specified
        *         @type diskguid:              guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function revokeServiceToDisk (applicationguid:String,servicename:String,diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'revokeServiceToDisk', revokeServiceToDisk_ResultReceived, getError, applicationguid,servicename,diskguid,jobguid,executionparams);

        }

        private function revokeServiceToDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REVOKESERVICETODISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAPPLICATIONTEMPLATE:String = 'getApplicationTemplate_response';
        /**
        *         Retrieve application template used to create the given application
        *         @param applicationguid:      guid of the application
        *         @type applicationguid:       guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with applicationtemplate guid and applicationtemplate name as result and jobguid: {'result': {'guid':'58aef606-d30c-4ac4-b79c-f2ea955011f9', 'name':'dhcpserver'}, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function getApplicationTemplate (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getApplicationTemplate', getApplicationTemplate_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function getApplicationTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAPPLICATIONTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OFFERSERVICETOLAN:String = 'offerServiceToLan_response';
        /**
        *         Offers a service for the lan specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to add. Name must be unique!
        *         @type servicename:           string
        *         @param languid:              guid of the lan to which to offer the service specified
        *         @type languid:               guid
        *         @param remark:               Remark to add to this service offer.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function offerServiceToLan (applicationguid:String,servicename:String,languid:String,remark:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'offerServiceToLan', offerServiceToLan_ResultReceived, getError, applicationguid,servicename,languid,remark,jobguid,executionparams);

        }

        private function offerServiceToLan_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OFFERSERVICETOLAN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OFFERSERVICETOMACHINE:String = 'offerServiceToMachine_response';
        /**
        *         Offers a service for machine lan specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to add. Name must be unique!
        *         @type servicename:           string
        *         @param machineguid:          guid of the machine to which to offer the service specified
        *         @type machineguid:           guid
        *         @param remark:               Remark to add to this service offer.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function offerServiceToMachine (applicationguid:String,servicename:String,machineguid:String,remark:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'offerServiceToMachine', offerServiceToMachine_ResultReceived, getError, applicationguid,servicename,machineguid,remark,jobguid,executionparams);

        }

        private function offerServiceToMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OFFERSERVICETOMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETNETWORKSERVICEPORTS:String = 'getNetworkServicePorts_response';
        /**
        *         Retrieve information about the networkserviceports for the given application
        *         
        *         @execution_method = sync
        *         @param applicationguid:       guid of the application
        *         @type applicationguid:        guid
        *         
        *         @param networkservicename:    name of the network service
        *         @type networkservicename:     string
        *         
        *         @param jobguid:               guid of the job if available else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      dictionary 
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        */
        public function getNetworkServicePorts (applicationguid:String,networkservicename:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getNetworkServicePorts', getNetworkServicePorts_ResultReceived, getError, applicationguid,networkservicename,jobguid,executionparams);

        }

        private function getNetworkServicePorts_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETNETWORKSERVICEPORTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVETOMACHINE:String = 'moveToMachine_response';
        /**
        *         Copies the application specified.
        *         @param applicationguid:                  guid of the application to move.
        *         @type applicationguid:                   guid
        *         @param machineguid:                      guid of the machine to which we want to move this application.
        *         @type machineguid:                       guid
        *         @param jobguid:                          guid of the job if available else empty string
        *         @type jobguid:                           guid
        *         @param executionparams:                  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:                   dictionary
        *         @return:                                 dictionary with the True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                                  dictionary
        *         @raise e:                                In case an error occurred, exception is raised
        *         
        */
        public function moveToMachine (applicationguid:String,machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveToMachine', moveToMachine_ResultReceived, getError, applicationguid,machineguid,jobguid,executionparams);

        }

        private function moveToMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVETOMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OFFERSERVICETOCLOUDUSER:String = 'offerServiceToCloudUser_response';
        /**
        *         Offers a service for the cloud user specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to add. Name must be unique!
        *         @type servicename:           string
        *         @param clouduserguid:        guid of the disk to which to offer the service specified
        *         @type clouduserguid:         guid
        *         @param remark:               Remark to add to this service offer.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function offerServiceToCloudUser (applicationguid:String,servicename:String,clouduserguid:String,remark:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'offerServiceToCloudUser', offerServiceToCloudUser_ResultReceived, getError, applicationguid,servicename,clouduserguid,remark,jobguid,executionparams);

        }

        private function offerServiceToCloudUser_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OFFERSERVICETOCLOUDUSER, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDNETWORKSERVICE:String = 'addNetworkService_response';
        /**
        *         Adds a new service for the application specified.
        *         @execution_method = sync
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param name:                 Name of network service to add. Name must be unique!
        *         @type name:                  string
        *         @param description:          Description of network service to add.
        *         @type description:           string
        *         @param enabled:              Is this network service enabled.
        *         @type enabled:               bool
        *         @param monitored:            Should this network service be monitored.
        *         @type monitored:             bool
        *         @param ipaddressguids:       ip addresses linked to this service only, null if not specific to this service, link to guid of ip address as used in machine.
        *         @type ipaddressguids:        list
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addNetworkService (applicationguid:String,name:String,description:String="",enabled:Object=null,monitored:Object=null,ipaddressguids:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addNetworkService', addNetworkService_ResultReceived, getError, applicationguid,name,description,enabled,monitored,ipaddressguids,jobguid,executionparams);

        }

        private function addNetworkService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDNETWORKSERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_STOP:String = 'stop_response';
        /**
        *         Stops the application specified.
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function stop (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'stop', stop_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function stop_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_STOP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEACCOUNT:String = 'removeAccount_response';
        /**
        *         Removes an account for the application specified.
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param login:                    Login of the account to remove.
        *         @type login:                     string
        *         @param accouttype:               Type of the account to remove. See listAccountTypes().
        *         @type accouttype:                string
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function removeAccount (applicationguid:String,login:String,accounttype:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeAccount', removeAccount_ResultReceived, getError, applicationguid,login,accounttype,jobguid,executionparams);

        }

        private function removeAccount_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEACCOUNT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DISABLE:String = 'disable_response';
        /**
        *         Disables the application specified.
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function disable (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'disable', disable_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function disable_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DISABLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDSERVICE:String = 'addService_response';
        /**
        *         Adds a new service for the application specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param name:                 Name of service to add. Name must be unique!
        *         @type name:                  string
        *         @param description:          Description of service to add.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addService (applicationguid:String,name:String,description:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addService', addService_ResultReceived, getError, applicationguid,name,description,jobguid,executionparams);

        }

        private function addService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDSERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the application rootobject.
        *         @execution_method = sync
        *         @param applicationguid:   guid of the lan rootobject
        *         @type applicationguid:    guid
        *         @return:                  XML representation of the lan
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         @todo:                    Will be implemented in phase2
        *         
        */
        public function getXML (applicationguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_IMPORTFROMURI:String = 'importFromURI_response';
        /**
        *         Imports an application from the source location specified.
        *         Export rootobject info
        *         @param applicationguid:            guid of the application to export.
        *         @type applicationguid:             guid
        *         @param sourceuri:                  URI of the location holding an exported application. (e.g ftp://login:passwd@myhost.com/backups/apache/)
        *         @type sourceuri:                   string
        *         @param executormachineguid:        guid of the machine which should convert the application to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:         guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function importFromURI (applicationguid:String,sourceuri:String,executormachineguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'importFromURI', importFromURI_ResultReceived, getError, applicationguid,sourceuri,executormachineguid,jobguid,executionparams);

        }

        private function importFromURI_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_IMPORTFROMURI, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAGENTSFORCLOUDSERVICE:String = 'getAgentsForCloudService_response';
        /**
        *         return guids of agents off applications of cloudservice (when applicatyupename is specified only one specific applicationtype part of cloudservice)
        *         e.g. getAgentsForCloudServiceApplication("dsssstore","storagedaemon") will return a list of all storagedaemonAgents
        *         
        *         @param applicationtype:       Specified application needs to be linked to a template with specified name (as string)
        *         
        *         @todo:                        Will be implemented in phase2
        *         
        */
        public function getAgentsForCloudService (cloudservicename:Object,applicationtype:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAgentsForCloudService', getAgentsForCloudService_ResultReceived, getError, cloudservicename,applicationtype,jobguid,executionparams);

        }

        private function getAgentsForCloudService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAGENTSFORCLOUDSERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REVOKESERVICETOAPPLICATION:String = 'revokeServiceToApplication_response';
        /**
        *         Revokes a service for the application specified.
        *         @param applicationguid:            guid of the application specified
        *         @type applicationguid:             guid
        *         @param servicename:                Name of service to revoke. Name must be unique!
        *         @type servicename:                 string
        *         @param destinationapplicationguid: guid of the application to which to revoke the service specified
        *         @type destinationapplicationguid:  guid
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function revokeServiceToApplication (applicationguid:String,servicename:String,destinationapplicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'revokeServiceToApplication', revokeServiceToApplication_ResultReceived, getError, applicationguid,servicename,destinationapplicationguid,jobguid,executionparams);

        }

        private function revokeServiceToApplication_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REVOKESERVICETOAPPLICATION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_RESTART:String = 'restart_response';
        /**
        *         Restart the application specified.
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function restart (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'restart', restart_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function restart_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESTART, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTNETWORKSERVICES:String = 'listNetworkServices_response';
        /**
        *         Returns a list of network services for an application.
        *         @execution_method = sync
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     Dictionary of array of network services.
        *         @rtype:                      dictionary
        *         @note:                       Example return value:
        *         @note:                       {'result': {'name': 'service1',
        *         @note:                                   'description': 'service one',
        *         @note:                                   'monitor': True,
        *         @note:                                   'enabled': True,
        *         @note:                                   'ipaddressguids': [],
        *         @note:                                   'ports':  {'portnr': 25,
        *         @note:                                              'monitor': True,
        *         @note:                                              'ipaddress': '192.168.90.1'
        *         @note:                                              'ipprotocoltype': 'TCP')
        *         @note:                                 },
        *         @note:                        'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listNetworkServices (applicationguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listNetworkServices', listNetworkServices_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function listNetworkServices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTNETWORKSERVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVECAPACITYCONSUMED:String = 'removeCapacityConsumed_response';
        /**
        *         Removes consumed capacity for the customer specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeCapacityConsumed (applicationguid:String,capacityunittype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeCapacityConsumed', removeCapacityConsumed_ResultReceived, getError, applicationguid,capacityunittype,jobguid,executionparams);

        }

        private function removeCapacityConsumed_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECAPACITYCONSUMED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCAPACITYCONSUMED:String = 'addCapacityConsumed_response';
        /**
        *         Adds consumed capacity for the application specified.
        *         @param applicationguid:      guid of the customer specified
        *         @type applicationguid:       guid
        *         @param amount:               Amount of capacity units to add
        *         @type amount:                integer
        *         @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param name:                 Name of capacity units to add.
        *         @type name:                  string
        *         @param description:          Description of capacity units to add.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addCapacityConsumed (applicationguid:String,amount:Number,capacityunittype:String,name:String="",description:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addCapacityConsumed', addCapacityConsumed_ResultReceived, getError, applicationguid,amount,capacityunittype,name,description,jobguid,executionparams);

        }

        private function addCapacityConsumed_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCAPACITYCONSUMED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UNINSTALL:String = 'uninstall_response';
        /**
        *         Uninstalls the application specified
        *         @param applicationguid:  Guid of the application
        *         @type applicationguid:   guid
        *         @param jobguid:          Guid of the job
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                  dictionary
        *         
        */
        public function uninstall (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'uninstall', uninstall_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function uninstall_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UNINSTALL, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDNETWORKSERVICEPORT:String = 'addNetworkServicePort_response';
        /**
        *         Adds a network service port for the application specified.
        *         @execution_method = sync
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of network service .
        *         @type servicename:           string
        *         @param portnr:               Port of network service .
        *         @type portnr:                int
        *         @param protocoltype:         Protocol type (applicationipprotocoltype)
        *         @type protocoltype:          string
        *         @param ipaddress:            IP address to which port is bound to
        *         @type ipaddress:             string
        *         @param monitor:              Should this port be monitored
        *         @type monitor:               bool
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addNetworkServicePort (applicationguid:String,servicename:String,portnr:Number,protocoltype:String="",ipaddress:String="",monitor:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addNetworkServicePort', addNetworkServicePort_ResultReceived, getError, applicationguid,servicename,portnr,protocoltype,ipaddress,monitor,jobguid,executionparams);

        }

        private function addNetworkServicePort_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDNETWORKSERVICEPORT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAGENTFORAPPLICATIONTYPESERVICE:String = 'getAgentForApplicationTypeService_response';
        /**
        *         return guid of agent which serves specified applicationtype to this machine
        *         e.g. getAgentForService([machineguid of a machine],"dssdirector") will return the agent of the dssdirector
        *         
        *         @todo:                        Will be implemented in phase2
        *         
        */
        public function getAgentForApplicationTypeService (machineguid:Object,applicationtype:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAgentForApplicationTypeService', getAgentForApplicationTypeService_ResultReceived, getError, machineguid,applicationtype,jobguid,executionparams);

        }

        private function getAgentForApplicationTypeService_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAGENTFORAPPLICATIONTYPESERVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXPORTTOURI:String = 'exportToURI_response';
        /**
        *         Exports specified application (is a backup) to a remote destination.
        *         These are very application specific workflows
        *         Export rootobject info
        *         @param applicationguid:            guid of the application to export.
        *         @type applicationguid:             guid
        *         @param destinationuri:             URI of the location where the application should be stored. (e.g ftp://login:passwd@myhost.com/backups/apache/)
        *         @type destinationuri:              string
        *         @param executormachineguid:        guid of the machine which should convert the application to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:         guid
        *         @param compressed                  Boolean value indicating if the export should be compressed. Compression used is 7zip
        *         @type:                             boolean
        *         @param imagetype                   Type of image format to use.
        *         @type:                             string
        *         @note:                             Supported export formats are : "vdi", "parallels", "qcow2", "vvfat", "vpc", "bochs", "dmg", "cloop", "vmdk", "qcow", "cow", "host_device", "raw"
        *         @param jobguid:                    guid of the job if available else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         @todo:                             Will be implemented in phase2
        *         
        */
        public function exportToURI (applicationguid:String,destinationuri:String,executormachineguid:Object=null,compressed:Object=null,imagetype:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exportToURI', exportToURI_ResultReceived, getError, applicationguid,destinationuri,executormachineguid,compressed,imagetype,jobguid,executionparams);

        }

        private function exportToURI_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXPORTTOURI, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of applications.
        *         @question shouldn't there be at least some filter criteria, this is always going to be a useless result (too long) e.g. vmachineguid="",customerguid="", ... most common filter criteria, this should be main criteria for views, the filter criteria should be like find, but directly exposes views
        *         @SECURITY administrator only
        *         @execution_method = sync
        *         @param cloudspaceguid:    guid of the cloudspace if available else empty string
        *         @type cloudspaceguid:     guid
        *         @param machineguid:       guid of the application if available else empty string
        *         @type machineguid:        guid
        *         @param applicationguid:   guid of the application if available else empty string
        *         @type applicationguid:    guid
        *         @param status:            status of the application to include in the search criteria.
        *         @type status:             string
        *         
        *         @param customer:          Flag whether the application is system or customer application
        *         @type customer:           boolean
        *         @param istemplate:        Flag whether the application is template application
        *         @type istemplate:         boolean
        *         @param jobguid:           guid of the job if available else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary of array of dictionaries with guid, name, description, status, template, applicationtemplateguid, machineguid, machinename, cloudspaceguid, cloudspacename of the application.
        *         @rtype:                   dictionary
        *         @note:                    Example return value:
        *         @note:                    {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "DSSDirector", "description": "DSS Director", "status": "ACTIVE", "template": "False", "applicationtemplateguid": "", "machineguid": "0D735CB9-8376-456C-827E-31CAC8815894", "machinename": "appliance1", "cloudspaceguid": "0D58B3BE-6C46-4450-954C-4BFFAF1E38C4", "cloudspacename": "Administrator space"},
        *         @note:                                {"guid": "D48CCFB4-207D-469F-8DA8-471304C3CCA7", "name": "DSSVolumeDriver", "description": "DSS Volumedriver", "status": "ACTIVE", "template": "False", "applicationtemplateguid": "", "machineguid": "0D735CB9-8376-456C-827E-31CAC8815894", "machinename": "appliance1", "cloudspaceguid": "0D58B3BE-6C46-4450-954C-4BFFAF1E38C4", "cloudspacename": "Administrator space"}]',
        *         @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function list (cloudspaceguid:Object=null,machineguid:Object=null,applicationguid:Object=null,status:Object=null,customer:Object=null,istemplate:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, cloudspaceguid,machineguid,applicationguid,status,customer,istemplate,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OFFERSERVICETONETWORKZONE:String = 'offerServiceToNetworkZone_response';
        /**
        *         Offers a service for the network zone specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to add. Name must be unique!
        *         @type servicename:           string
        *         @param networkzoneguid:      guid of the network zone to which to offer the service specified
        *         @type networkzoneguid:       guid
        *         @param remark:               Remark to add to this service offer.
        *         @type type:                  string
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function offerServiceToNetworkZone (applicationguid:String,servicename:String,networkzoneguid:String,remark:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'offerServiceToNetworkZone', offerServiceToNetworkZone_ResultReceived, getError, applicationguid,servicename,networkzoneguid,remark,jobguid,executionparams);

        }

        private function offerServiceToNetworkZone_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OFFERSERVICETONETWORKZONE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the application rootobject.
        *         @execution_method = sync
        *         @param applicationguid:   guid of the lan rootobject
        *         @type applicationguid:    guid
        *         @return:                  YAML representation of the disk
        *         @rtype:                   string
        *         
        */
        public function getYAML (applicationguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REVOKESERVICETOMACHINE:String = 'revokeServiceToMachine_response';
        /**
        *         Revokes a service for the machine specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to revoke. Name must be unique!
        *         @type servicename:           string
        *         @param machineguid:          guid of the machine to which to revoke the service specified
        *         @type machineguid:           guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function revokeServiceToMachine (applicationguid:String,servicename:String,machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'revokeServiceToMachine', revokeServiceToMachine_ResultReceived, getError, applicationguid,servicename,machineguid,jobguid,executionparams);

        }

        private function revokeServiceToMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REVOKESERVICETOMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the application rootobject structure.
        *         @execution_method = sync
        *         @param applicationguid:   guid of the lan rootobject
        *         @type applicationguid:    guid
        *         @return:                  XSD representation of the disk structure.
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         @todo:                    Will be implemented in phase2
        *         
        */
        public function getXMLSchema (applicationguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSTATUSES:String = 'listStatuses_response';
        /**
        *         Returns a list of possible application statuses.
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of statuses.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '["ACTIVE", "DISABLED", "MAINTENANCE"]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listStatuses (jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listStatuses', listStatuses_ResultReceived, getError, jobguid,executionparams);

        }

        private function listStatuses_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSTATUSES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REVOKESERVICETOLAN:String = 'revokeServiceToLan_response';
        /**
        *         Revokes a service for the lan specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to revoke. Name must be unique!
        *         @type servicename:           string
        *         @param languid:              guid of the lan to which to revoke the service specified
        *         @type languid:               guid
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function revokeServiceToLan (applicationguid:String,servicename:String,languid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'revokeServiceToLan', revokeServiceToLan_ResultReceived, getError, applicationguid,servicename,languid,jobguid,executionparams);

        }

        private function revokeServiceToLan_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REVOKESERVICETOLAN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OFFERSERVICETODISK:String = 'offerServiceToDisk_response';
        /**
        *         Offers a service for the disk specified.
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of service to add. Name must be unique!
        *         @type servicename:           string
        *         @param diskguid:             guid of the disk to which to offer the service specified
        *         @type diskguid:              guid
        *         @param remark:               Remark to add to this service offer.
        *         @type remark:                string
        *     
        *         @param partitionorder:       number of partition serviced (eg mountpoints)
        *         @type partitionorder:        int
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function offerServiceToDisk (applicationguid:String,servicename:String,diskguid:String,remark:String="",partitionorder:Number=0,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'offerServiceToDisk', offerServiceToDisk_ResultReceived, getError, applicationguid,servicename,diskguid,remark,partitionorder,jobguid,executionparams);

        }

        private function offerServiceToDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OFFERSERVICETODISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETAGENT:String = 'getAgent_response';
        /**
        *         return guid of agent which serves the specified application (which is NOT part of cloudservice)
        *         
        */
        public function getAgent (applicationguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getAgent', getAgent_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function getAgent_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETAGENT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_BACKUP:String = 'backup_response';
        /**
        *         Creates a backup of the application (when needed a destination can be given)
        *         @param applicationguid:  Guid of the application
        *         @type applicationguid:   guid
        *         @param destinationuri:   URI of the location where the backup should be stored. (e.g ftp://login:passwd@myhost.com/backups/applicationx/).
        *                                  If no password and login are passed, default credentials will be used
        *         
        *         @type destinationuri:    string
        *         @param compressed:       If true backup will be zipped (compression = 7zip)
        *         @type compressed:        boolean
        *         @param login:            Login credential on the destination machine
        *         @type login:             string
        *         
        *         @param password:         Password on the destination machine
        *         @type password:          string
        *         
        *         @param jobguid:          guid of the job if available else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         
        */
        public function backup (applicationguid:String,destinationuri:String="",compressed:Boolean=true,login:String="",password:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'backup', backup_ResultReceived, getError, applicationguid,destinationuri,compressed,login,password,jobguid,executionparams);

        }

        private function backup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_BACKUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVENETWORKSERVICEPORT:String = 'removeNetworkServicePort_response';
        /**
        *         Removes a network service port from the application specified.
        *         @execution_method = sync
        *         @param applicationguid:      guid of the application specified
        *         @type applicationguid:       guid
        *         @param servicename:          Name of network service .
        *         @type servicename:           string
        *         @param portnr:               Port of network service .
        *         @type portnr:                int
        *         @param jobguid:              guid of the job if available else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeNetworkServicePort (applicationguid:String,servicename:String,portnr:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeNetworkServicePort', removeNetworkServicePort_ResultReceived, getError, applicationguid,servicename,portnr,jobguid,executionparams);

        }

        private function removeNetworkServicePort_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVENETWORKSERVICEPORT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the application specified.
        *         @param applicationguid:          guid of the application to delete.
        *         @type applicationguid:           guid
        *         @param jobguid:                  guid of the job if available else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function deleteApplication (applicationguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteApplication', delete_ResultReceived, getError, applicationguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

