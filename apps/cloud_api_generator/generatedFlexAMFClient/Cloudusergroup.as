
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Cloudusergroup extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_cloudusergroup';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Cloudusergroup()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTGROUPS:String = 'listGroups_response';
        /**
        *         Returns a list of cloud user groups which are member of the given cloud user group.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid: guid of the cloud user group specified
        *         @type cloudusergroupguid:  guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function listGroups (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listGroups', listGroups_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

        }

        private function listGroups_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTGROUPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the cloud user group rootobject structure.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:       guid of the cloud user group rootobject
        *         @type cloudusergroupguid:        guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         XSD representation of the cloud user group structure.
        *         @rtype:                          string
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function getXMLSchema (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDUSER:String = 'addUser_response';
        /**
        *         Add an existing cloud user to the cloud user group specified.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:   guid of the cloud user group specified
        *         @type cloudusergroupguid:    guid
        *         @param clouduserguid:        Gui of the cloud user to add to the cloud user group specified
        *         @type clouduserguid:         guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function addUser (cloudusergroupguid:String,clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addUser', addUser_ResultReceived, getError, cloudusergroupguid,clouduserguid,jobguid,executionparams);

        }

        private function addUser_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDUSER, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new cloud user group
        *         
        *         @execution_method = sync
        *         
        *         @param name:                Name for this new cloud user group
        *         @type name:                 string
        *         @param description:         Description for this new cloud user group
        *         @type description:          string
        *         @param jobguid:             guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with cloud user group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function create (name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, name,description,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEUSERROLE:String = 'removeUserRole_response';
        /**
        *         Remove an existing cloud user role from the cloud user group specified.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:           guid of the cloud user group specified
        *         @type cloudusergroupguid:            guid
        *         @param clouduserroleguid:            Guid of the cloud user role who should be removed from the cloud user group specified
        *         @type clouduserroleguid:             guid
        *         @param jobguid:                      guid of the job if avalailable else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function removeUserRole (cloudusergroupguid:String,clouduserroleguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeUserRole', removeUserRole_ResultReceived, getError, cloudusergroupguid,clouduserroleguid,jobguid,executionparams);

        }

        private function removeUserRole_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEUSERROLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of cloud user groups which are related to the customer specified.
        *         @execution_method = sync
        *         
        *         @param customerguid:         guid of the customer for which to retrieve the list of cloud user groups.
        *         @type customerguid:          guid
        *         @param cloudusergroupguid:   guid of the cloud user group specified
        *         @type cloudusergroupguid:    guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        *         @rtype:                      dictionary
        *         @note:                       Example return value:
        *         @note:                       {'result': '[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                     "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        *         @note:                                                  "name": "admins",
        *         @note:                                                  "description": "Cloud Administrators"},
        *         @note:                                                 {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                                  "name": "users",
        *         @note:                                                  "description": "cloud user groups"}]"}]',
        *         @note:                        'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function list (customerguid:Object=null,cloudusergroupguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, customerguid,cloudusergroupguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEGROUP:String = 'removeGroup_response';
        /**
        *         Remove an existing cloud user group from the cloud user group specified.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:           guid of the cloud user group specified
        *         @type cloudusergroupguid:            guid
        *         @param membercloudusergroupguid:     Guid of the cloud user group who should be removed from the cloud user group specified
        *         @type membercloudusergroupguid:      guid
        *         @param jobguid:                      guid of the job if avalailable else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function removeGroup (cloudusergroupguid:String,membercloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeGroup', removeGroup_ResultReceived, getError, cloudusergroupguid,membercloudusergroupguid,jobguid,executionparams);

        }

        private function removeGroup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEGROUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the cloud user group rootobject.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:       guid of the cloud user group rootobject
        *         @type cloudusergroupguid:        guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         YAML representation of the cloud user group
        *         @rtype:                          string
        *         
        */
        public function getYAML (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

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




        public const EVENTTYPE_LISTUSERS:String = 'listUsers_response';
        /**
        *         Returns a list of cloud users which are member of the given cloud user group.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:  guid of the cloud user group specified
        *         @type cloudusergroupguid:   guid
        *         @param jobguid:             guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function listUsers (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listUsers', listUsers_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

        }

        private function listUsers_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTUSERS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTROLES:String = 'listRoles_response';
        /**
        *         Returns a list of cloud user roles of the cloud user group
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid: guid of the cloud user group specified
        *         @type cloudusergroupguid:  guid
        *         @param jobguid:            guid of the job if avalailable else empty string
        *         @type jobguid:             guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   Dictionary of array of dictionaries with an array of cloud user roles with cloudusergroupguid
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function listRoles (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listRoles', listRoles_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

        }

        private function listRoles_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTROLES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEUSER:String = 'removeUser_response';
        /**
        *         Remove an existing cloud user from the cloud user group specified.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:   guid of the cloud user group specified
        *         @type cloudusergroupguid:    guid
        *         @param clouduserguid:        Gui of the cloud user to remove from the cloud user group specified
        *         @type clouduserguid:         guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function removeUser (cloudusergroupguid:String,clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeUser', removeUser_ResultReceived, getError, cloudusergroupguid,clouduserguid,jobguid,executionparams);

        }

        private function removeUser_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEUSER, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties, every parameter which is not passed or passed as empty string is not updated.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:   guid of the cloud user group specified
        *         @type cloudusergroupguid:    guid
        *         @param name:                 Name for this cloud user group
        *         @type name:                  string
        *         @param description:          Description for this cloud user group
        *         @type description:           string
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with cloud user group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (cloudusergroupguid:String,name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, cloudusergroupguid,name,description,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTCUSTOMERS:String = 'listCustomers_response';
        /**
        *         Returns a list of cloud users which are member of the given cloud user group.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:   guid of the cloud user group specified
        *         @type cloudusergroupguid:    guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        *         @todo:                       Will be implemented in phase2
        *         
        */
        public function listCustomers (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listCustomers', listCustomers_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

        }

        private function listCustomers_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCUSTOMERS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDGROUP:String = 'addGroup_response';
        /**
        *         Add an existing cloud user group to the cloud user group specified.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:           guid of the cloud user group specified
        *         @type cloudusergroupguid:            guid
        *         @param membercloudusergroupguid:     Guid of the cloud user group who should become a member of the cloud user group specified
        *         @type membercloudusergroupguid:      guid
        *         @param jobguid:                      guid of the job if avalailable else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function addGroup (cloudusergroupguid:String,membercloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addGroup', addGroup_ResultReceived, getError, cloudusergroupguid,membercloudusergroupguid,jobguid,executionparams);

        }

        private function addGroup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDGROUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the cloud user group rootobject.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:       guid of the cloud user group rootobject
        *         @type cloudusergroupguid:        guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         XML representation of the cloud user group
        *         @rtype:                          string
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function getXML (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDUSERROLE:String = 'addUserRole_response';
        /**
        *         Add an existing cloud user role to the cloud user group specified.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:           guid of the cloud user group specified
        *         @type cloudusergroupguid:            guid
        *         @param clouduserroleguid:            Guid of the cloud user role
        *         @type clouduserroleguid:             guid
        *         @param jobguid:                      guid of the job if avalailable else empty string
        *         @type jobguid:                       guid
        *         @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:               dictionary
        *         @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                              dictionary
        *         @raise e:                            In case an error occurred, exception is raised
        *         
        */
        public function addUserRole (cloudusergroupguid:String,clouduserroleguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addUserRole', addUserRole_ResultReceived, getError, cloudusergroupguid,clouduserroleguid,jobguid,executionparams);

        }

        private function addUserRole_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDUSERROLE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of cloud user groups guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:                    Name of the cloud user group to include in the search criteria.
        *         @type name:                     string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of cloud user group guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the cloud user group specified.
        *         @execution_method = sync
        *         
        *         @param cloudusergroupguid:       guid of the cloud user group to delete.
        *         @type cloudusergroupguid:        guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function deleteCloudusergroup (cloudusergroupguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteCloudusergroup', delete_ResultReceived, getError, cloudusergroupguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

