
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Resourcegroup extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_resourcegroup';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Resourcegroup()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_REMOVEDEVICE:String = 'removeDevice_response';
        /**
        *         Removes an existing device from the resource group specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:           Guid of the resource group specified
        *         @type resourcegroupguid:            guid
        *         @param deviceguid:                  Guid of the device to remove from the resource group specified
        *         @type deviceguid:                   guid
        *         @param jobguid:                     Guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @param executionparams:             dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:              dictionary
        *         @return:                            dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                           In case an error occurred, exception is raised
        *         
        */
        public function removeDevice (resourcegroupguid:String,deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeDevice', removeDevice_ResultReceived, getError, resourcegroupguid,deviceguid,jobguid,executionparams);

        }

        private function removeDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEDEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the resource group rootobject structure.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:       Guid of the resource group rootobject
        *         @type resourcegroupguid:        guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the resource group structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDBACKPLANE:String = 'addBackplane_response';
        /**
        *         Add an existing backplane to the resource group specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:   Guid of the resource group specified
        *         @type resourcegroupguid:    guid
        *         @param backplaneguid:       Guid of the backplane to add to the resource group specified
        *         @type backplaneguid:        guid
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function addBackplane (resourcegroupguid:String,backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addBackplane', addBackplane_ResultReceived, getError, resourcegroupguid,backplaneguid,jobguid,executionparams);

        }

        private function addBackplane_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDBACKPLANE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDDEVICE:String = 'addDevice_response';
        /**
        *         Adds an existing device to the resource group specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:           Guid of the resource group specified
        *         @type resourcegroupguid:            guid
        *         @param deviceguid:                  Guid of the device to add to the resource group specified
        *         @type deviceguid:                   guid
        *         @param jobguid:                     Guid of the job if avalailable else empty string
        *         @type jobguid:                      guid
        *         @param executionparams:             dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:              dictionary
        *         @return:                            dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                             dictionary
        *         @raise e:                           In case an error occurred, exception is raised
        *         
        */
        public function addDevice (resourcegroupguid:String,deviceguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addDevice', addDevice_ResultReceived, getError, resourcegroupguid,deviceguid,jobguid,executionparams);

        }

        private function addDevice_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDDEVICE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of resource groups which are related to the customer specified.
        *         @execution_method = sync
        *         
        *         @param datacenterguid:      Guid of the datacenter to which this resource group is related
        *         @type datacenterguid:       guid
        *         @param resourcegroupguid:   Guid of the resource group specified
        *         @type resourcegroupguid:    guid
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary of array of dictionaries with customerguid, and an array of resource groups with resourcegroupguid, datacenterguid, name, description.
        *         @rtype:                     dictionary
        *         @note:                      Example return value:
        *         @note:                      {'result': {"datacenterguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                  "groups": "[{"resourcegroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        *         @note:                                               "datacenterguid": "D51AD737-D29E-4505-989C-8D4E18BCAAE0",
        *         @note:                                               "name": "RESGROUPCUSTX",
        *         @note:                                               "description": "Resource group of customer x"},
        *         @note:                                              {"resourcegroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                               "datacenterguid": "D51AD737-D29E-4505-989C-8D4E18BCAAE0",
        *         @note:                                               "name": "RESGROUPCUSTX",
        *         @note:                                               "description": "Resource group of customer y"}]"},
        *         @note:                       'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function list (datacenterguid:Object=null,resourcegroupguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, datacenterguid,resourcegroupguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIESADVANCED:String = 'updateModelPropertiesAdvanced_response';
        /**
        *         Update basic properties, every parameter which is not passed or passed as empty string is not updated.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:   Guid of the resource group specified
        *         @type resourcegroupguid:    guid
        *         @param datacenterguid:      Guid of the datacenter to which this resource group is related
        *         @type datacenterguid:       guid
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with resource group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function updateModelPropertiesAdvanced (resourcegroupguid:String,datacenterguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelPropertiesAdvanced', updateModelPropertiesAdvanced_ResultReceived, getError, resourcegroupguid,datacenterguid,jobguid,executionparams);

        }

        private function updateModelPropertiesAdvanced_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIESADVANCED, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the resource group rootobject.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:  Guid of the resource group rootobject
        *         @type resourcegroupguid:   guid
        *         @param jobguid:            Guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @return:                   YAML representation of the resource group
        *         @rtype:                    string
        *         
        */
        public function getYAML (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

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
        *         @param jobguid:           Guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  rootobject
        *         @rtype:                   string
        *         @warning:                 Only usable using the python client.
        *         
        */
        public function getObject (rootobjectguid:String,jobguid:String="",executionparams:Object=null):void
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




        public const EVENTTYPE_LISTMACHINES:String = 'listMachines_response';
        /**
        *         Returns a list of machines which are related to the resourcegroup specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:     Guid of the resource group specified
        *         @type resourcegroupguid:      guid
        *         @param jobguid:               Guid of the job if avalailable else empty string
        *         @type jobguid:                guid
        *         @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:        dictionary
        *         @return:                      Dictionary of array of machines
        *         @rtype:                       dictionary
        *         @raise e:                     In case an error occurred, exception is raised
        *         
        *         @todo:                        Will be implemented in phase2
        *         
        */
        public function listMachines (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listMachines', listMachines_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

        }

        private function listMachines_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTMACHINES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties, every parameter which is not passed or passed as empty string is not updated.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:   Guid of the resource group specified
        *         @type resourcegroupguid:    guid
        *         @param name:                Name for this resource group
        *         @type name:                 string
        *         @param description:         Description for this resource group
        *         @type description:          string
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with resource group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (resourcegroupguid:String,name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, resourcegroupguid,name,description,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTCUSTOMERS:String = 'listCustomers_response';
        /**
        *         Returns a list of customers which are related to the resourcegroup specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:    Guid of the resource group specified
        *         @type resourcegroupguid:     guid
        *         @param jobguid:              Guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     Dictionary of array of customers
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function listCustomers (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listCustomers', listCustomers_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

        }

        private function listCustomers_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCUSTOMERS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTBACKPLANES:String = 'listBackplanes_response';
        /**
        *         Returns a list of backplanes which are related to the resourcegroup specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:      Guid of the resource group specified
        *         @type resourcegroupguid:       guid
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary of array of backplanes
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        *         @todo:                         Will be implemented in phase2
        *         
        */
        public function listBackplanes (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listBackplanes', listBackplanes_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

        }

        private function listBackplanes_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTBACKPLANES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEBACKPLANE:String = 'removeBackplane_response';
        /**
        *         Removes an existing backplane from the resource group specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:   Guid of the resource group specified
        *         @type resourcegroupguid:    guid
        *         @param backplaneguid:       Guid of the backplane to remove from the resource group specified
        *         @type backplaneguid:        guid
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function removeBackplane (resourcegroupguid:String,backplaneguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeBackplane', removeBackplane_ResultReceived, getError, resourcegroupguid,backplaneguid,jobguid,executionparams);

        }

        private function removeBackplane_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEBACKPLANE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the resource group rootobject.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:       Guid of the resource group rootobject
        *         @type resourcegroupguid:        guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the resource group
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTDEVICES:String = 'listDevices_response';
        /**
        *         Returns a list of devices which are related to the resourcegroup specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:      Guid of the resource group specified
        *         @type resourcegroupguid:       guid
        *         @param jobguid:                Guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       Dictionary of array of dictionaries of .
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        *         @todo:                         Will be implemented in phase2
        *         
        */
        public function listDevices (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listDevices', listDevices_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

        }

        private function listDevices_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTDEVICES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new resource group
        *         @execution_method = sync
        *         
        *         @param datacenterguid:      Guid of the datacenter to which this resource group is related
        *         @type datacenterguid:       guid
        *         @param name:                Name for this new resource group
        *         @type name:                 string
        *         @param description:         Description for this new resource group
        *         @type description:          string
        *         @param jobguid:             Guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with resource group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function create (datacenterguid:String,name:String,description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, datacenterguid,name,description,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of resource groups guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:                    Name of the resource group to include in the search criteria.
        *         @type name:                     string
        *         @param description:             Description for this new resource group
        *         @type description:              string
        *         @param datacenterguid:          Guid of the datacenter to which this resource group is related
        *         @type datacenterguid:           guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of resource group guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,description:Object=null,datacenterguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,description,datacenterguid,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the resource group specified.
        *         @execution_method = sync
        *         
        *         @param resourcegroupguid:       Guid of the resource group to delete.
        *         @type resourcegroupguid:        guid
        *         @param jobguid:                 Guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function deleteResourcegroup (resourcegroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteResourcegroup', delete_ResultReceived, getError, resourcegroupguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

