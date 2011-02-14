
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Customer extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_customer';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Customer()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
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




        public const EVENTTYPE_REMOVECAPACITYAVAILABLE:String = 'removeCapacityAvailable_response';
        /**
        *         Removes available capacity for the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Guid of the customer specified
        *         @type customerguid:          guid
        *         @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeCapacityAvailable (customerguid:String,capacityunittype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeCapacityAvailable', removeCapacityAvailable_ResultReceived, getError, customerguid,capacityunittype,jobguid,executionparams);

        }

        private function removeCapacityAvailable_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECAPACITYAVAILABLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTCAPACITY:String = 'listCapacity_response';
        /**
        *         Returns a list of capacity units available and consumed for the given customer.
        *         
        *         @execution_method = sync
        *         
        *         @param customerguid:     Guid of the customer for which to retrieve the list of capacity units
        *         @type customerguid:      guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of dictionaries with customerguid, login, email, firstname, lastname, array of available capacity, array of consumed capacity.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                 "capacityavailable": "[{"amount": "1000",
        *         @note:                                                         "capacityunittype": "CU",
        *         @note:                                                         "name": "CPU"
        *         @note:                                                         "description": "CPU units"},
        *         @note:                                                        {"amount": "2000",
        *         @note:                                                         "capacityunittype": "MU",
        *         @note:                                                         "name": "Memory"
        *         @note:                                                         "description": "Memory units"}]"}]',
        *         @note:                                 "capacityconsumed": "[{"amount": "100",
        *         @note:                                                         "capacityunittype": "CU",
        *         @note:                                                         "name": "CPU"
        *         @note:                                                         "description": "CPU units"},
        *         @note:                                                        {"amount": "200",
        *         @note:                                                         "capacityunittype": "MU",
        *         @note:                                                         "name": "Memory"
        *         @note:                                                         "description": "Memory units"}]"}]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listCapacity (customerguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listCapacity', listCapacity_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function listCapacity_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCAPACITY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of customer guids which meet the search criteria.
        *         @execution_method = sync
        *         
        *         @param name:                    Name of the customer to include in the search criteria.
        *         @type name:                     string
        *         @param status:                  Status of the customer to include in the search criteria. See listStatuses().
        *         @type status:                   string
        *         
        *         @param resourcegroupguid:       Guid of the resourcegroup of the customer
        *         @type resourcegroupguid:        guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of customer guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,status:Object=null,resourcegroupguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,status,resourcegroupguid,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UNREGISTERDOMAIN:String = 'unregisterDomain_response';
        /**
        *         Unregisters a domain for a customer
        *         
        *         @param customerguid       Guid of the customer unregistering the domain
        *         @type customerguid        guid
        *         
        *         @param username           ITPS portal username
        *         @type username            string
        *         
        *         @param password           ITPS portal password
        *         @type password            string
        *         
        *         @param domain             Domain to unregister
        *         @type domain              string
        *         
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function unregisterDomain (customerguid:Object,username:Object,password:Object,domain:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'unregisterDomain', unregisterDomain_ResultReceived, getError, customerguid,username,password,domain,jobguid,executionparams);

        }

        private function unregisterDomain_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UNREGISTERDOMAIN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new customer
        *         @execution_method = sync
        *         
        *         @param name:                Name for this new customer
        *         @type name:                 string
        *         @param resourcegroupguid:   Guid of the resource group related to this customer
        *         @type resourcegroupguid:    guid
        *         @param description:         Description for this new customer
        *         @type description:          string
        *         @param address:             Address for this new customer
        *         @type address:              string
        *         @param city:                City for this new customer
        *         @type city:                 string
        *         @param country:             Country for this new customer
        *         @type country:              string
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with customer guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function create (name:String,resourcegroupguid:String="",description:String="",address:String="",city:String="",country:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,resourcegroupguid,description,address,city,country,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETSTATUS:String = 'setStatus_response';
        /**
        *         Updates the status of the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Guid of the customer specified
        *         @type customerguid:          guid
        *         @param status:               Status for the customer specified. See listStatuses() for the list of possible statuses.
        *         @type status:                string
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function setStatus (customerguid:String,status:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setStatus', setStatus_ResultReceived, getError, customerguid,status,jobguid,executionparams);

        }

        private function setStatus_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETSTATUS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update properties, every parameter which is not passed or passed as empty string is not updated.
        *         @SECURITY administrator only
        *         @execution_method = sync
        *         
        *         @param customerguid:         Guid of the customer specified
        *         @type customerguid:          guid
        *         @param name:                 Name for this customer
        *         @type name:                  string
        *         @param description:          Description for this customer
        *         @type description:           string
        *         @param address:              Address for this customer
        *         @type address:               string
        *         @param city:                 City for this customer
        *         @type city:                  string
        *         @param country:              Country for this customer
        *         @type country:               string
        *         
        *         @param retentionpolicyguid:  Guid of the retention policy for snapshots
        *         @type retentionpolicyguid:   guid
        *         
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with customer guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (customerguid:String,name:String="",description:String="",address:String="",city:String="",country:String="",retentionpolicyguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, customerguid,name,description,address,city,country,retentionpolicyguid,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTCLOUDSPACES:String = 'listCloudSpaces_response';
        /**
        *         Returns a list of cloudspaces for the customer.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Guid of the customer specified
        *         @type customerguid:          guid
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     Dictionary of array of cloudspaces.
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function listCloudSpaces (customerguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listCloudSpaces', listCloudSpaces_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function listCloudSpaces_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCLOUDSPACES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCLOUDUSERGROUP:String = 'addCloudUserGroup_response';
        /**
        *         Adds a cloud user group to the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Gui of the customer specified
        *         @type customerguid:          guid
        *         @param cloudusergroupguid:   Guid of the cloud user group specified
        *         @type cloudusergroupguid:    guid
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addCloudUserGroup (customerguid:String,cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addCloudUserGroup', addCloudUserGroup_ResultReceived, getError, customerguid,cloudusergroupguid,jobguid,executionparams);

        }

        private function addCloudUserGroup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCLOUDUSERGROUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REGISTERDOMAIN:String = 'registerDomain_response';
        /**
        *         Registers a domain for a customer
        *         
        *         @param customerguid       Guid of the customer registering the domain
        *         @type customerguid        guid
        *         
        *         @param username           ITPS portal username
        *         @type username            string
        *         
        *         @param password           ITPS portal password
        *         @type password            string
        *         
        *         @param domain             Domain to register
        *         @type domain              string
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         
        *         @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         
        */
        public function registerDomain (customerguid:Object,username:Object,password:Object,domain:Object,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'registerDomain', registerDomain_ResultReceived, getError, customerguid,username,password,domain,jobguid,executionparams);

        }

        private function registerDomain_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REGISTERDOMAIN, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTGROUPS:String = 'listGroups_response';
        /**
        *         Returns a list of cloud user groups for a given customer.
        *         
        *         @execution_method = sync
        *         
        *         @param customerguid:     Guid of the customer for which to retrieve the list of groups to which this user belongs.
        *         @type customerguid:      guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of dictionaries with customerguid, login, email, firstname, lastname, cloudusergroupguid, name, description.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                 "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        *         @note:                                              "name": "admins",
        *         @note:                                              "description": "Cloud Administrators"},
        *         @note:                                             {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                              "name": "users",
        *         @note:                                              "description": "customers"}]"}]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listGroups (customerguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listGroups', listGroups_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function listGroups_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTGROUPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVECLOUDUSERGROUP:String = 'removeCloudUserGroup_response';
        /**
        *         Removes a cloud user group for the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Gui of the customer specified
        *         @type customerguid:          guid
        *         @param cloudusergroupguid:   Guid of the cloud user group specified
        *         @type cloudusergroupguid:    guid
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeCloudUserGroup (customerguid:String,cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeCloudUserGroup', removeCloudUserGroup_ResultReceived, getError, customerguid,cloudusergroupguid,jobguid,executionparams);

        }

        private function removeCloudUserGroup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECLOUDUSERGROUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the customer rootobject.
        *         @execution_method = sync
        *         
        *         @param customerguid:            Guid of the customer rootobject
        *         @type customerguid:             guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the customer
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (customerguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVECAPACITYCONSUMED:String = 'removeCapacityConsumed_response';
        /**
        *         Removes consumed capacity for the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Guid of the customer specified
        *         @type customerguid:          guid
        *         @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeCapacityConsumed (customerguid:String,capacityunittype:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeCapacityConsumed', removeCapacityConsumed_ResultReceived, getError, customerguid,capacityunittype,jobguid,executionparams);

        }

        private function removeCapacityConsumed_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVECAPACITYCONSUMED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCAPACITYCONSUMED:String = 'addCapacityConsumed_response';
        /**
        *         Adds consumed capacity for the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Guid of the customer specified
        *         @type customerguid:          guid
        *         @param amount:               Amount of capacity units to add
        *         @type amount:                integer
        *         @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param name:                 Name of capacity units to add.
        *         @type name:                  string
        *         @param description:          Description of capacity units to add.
        *         @type type:                  string
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addCapacityConsumed (customerguid:String,amount:Number,capacityunittype:String,name:String="",description:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addCapacityConsumed', addCapacityConsumed_ResultReceived, getError, customerguid,amount,capacityunittype,name,description,jobguid,executionparams);

        }

        private function addCapacityConsumed_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCAPACITYCONSUMED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDCAPACITYAVAILABLE:String = 'addCapacityAvailable_response';
        /**
        *         Adds available capacity for the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         Gui of the customer specified
        *         @type customerguid:          guid
        *         @param amount:               Amount of capacity units to add
        *         @type amount:                integer
        *         @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        *         @type capacityunittype:      string
        *         @param name:                 Name of capacity units to add.
        *         @type name:                  string
        *         @param description:          Description of capacity units to add.
        *         @type type:                  string
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addCapacityAvailable (customerguid:String,amount:Number,capacityunittype:String,name:String="",description:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addCapacityAvailable', addCapacityAvailable_ResultReceived, getError, customerguid,amount,capacityunittype,name,description,jobguid,executionparams);

        }

        private function addCapacityAvailable_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDCAPACITYAVAILABLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the customer rootobject structure.
        *         @execution_method = sync
        *         
        *         @param customerguid:             Guid of the customer rootobject
        *         @type customerguid:              guid
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         XSD representation of the customer structure.
        *         @rtype:                          string
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function getXMLSchema (customerguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of customers.
        *         @SECURITY administrator only
        *         @execution_method = sync
        *         
        *         @param customerguid:     Guid of the customer specified
        *         @type customerguid:      guid
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of dictionaries with guid, name, description, address, city, country and status for customer.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "Customer1", "description": "My first customer", "address": "Main road", "city": "Bombai", "country":"India" , "status": "ACTIVE"},
        *         @note:                                {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "name": "Customer2", "description": "My second customer", "address": "Antwerpsesteenweg", "city": "Lochristi", "country":"Belgium" , "status": "DISABLED"}]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function list (customerguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the customer rootobject.
        *         @execution_method = sync
        *         
        *         @param customerguid:             Guid of the customer rootobject
        *         @type customerguid:              guid
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         YAML representation of the customer
        *         @rtype:                          string
        *         
        */
        public function getYAML (customerguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSTATUSES:String = 'listStatuses_response';
        /**
        *         Returns a list of possible customer statuses.
        *         @execution_method = sync
        *         
        *         @param jobguid:          Guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of statuses.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '["ACTIVE", "CONFIGURED", "DISABLED"]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
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




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:             Guid of the customer to delete.
        *         @type customerguid:              guid
        *         @param jobguid:                  Guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function deleteCustomer (customerguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteCustomer', delete_ResultReceived, getError, customerguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

