
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Clouduser extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_clouduser';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Clouduser()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_LISTJOBS:String = 'listJobs_response';
        /**
        *         Returns a list of jobs the cloud user executed.
        *         @execution_method = sync
        *                 
        *         @param clouduserguid:    guid of the cloud user
        *         @type clouduserguid:     guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of machines for the cloud user.
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listJobs (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listJobs', listJobs_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function listJobs_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTJOBS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTGROUPS:String = 'listGroups_response';
        /**
        *         Returns the list of groups to which a given clouduser belongs.
        *  
        *         @execution_method = sync
        *                
        *         @param clouduserguid:    guid of the cloud user for which to retrieve the list of groups to which this user belongs.
        *         @type clouduserguid:     guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of dictionaries with clouduserguid, login, email, firstname, lastname, cloudusergroupguid, name, description.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '[{"clouduserguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                 "login": "asmith", "email": "adam@smith.com",
        *         @note:                                 "firstname":"Adam", "lastname": "Smith",
        *         @note:                                 "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        *         @note:                                              "name": "admins",
        *         @note:                                              "description": "Cloud Administrators"},
        *         @note:                                             {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        *         @note:                                              "name": "users",
        *         @note:                                              "description": "Cloud Users"}]"}]',
        *         @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listGroups (clouduserguid:Object,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listGroups', listGroups_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function listGroups_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTGROUPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the cloud user rootobject structure.
        *         @execution_method = sync
        *         
        *         @param clouduserguid:            guid of the cloud user rootobject
        *         @type clouduserguid:             guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         XSD representation of the cloud user structure.
        *         @rtype:                          string
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function getXMLSchema (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GENERATECERTIFICATE:String = 'generateCertificate_response';
        /**
        *         Generates a certificate for the cloud user specified.
        *         @SECURITY administrator only
        *         @execution_method = sync
        *         
        *         @param clouduserguid:        guid of the cloud user specified
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
        public function generateCertificate (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'generateCertificate', generateCertificate_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function generateCertificate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GENERATECERTIFICATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Creates a new cloud user        
        *         
        *         @param login:               Login for this new cloud user
        *         @type login:                string
        *         @param password:            Password for this new cloud user
        *         @type password:             string
        *         @param email:               Email address for this new cloud user
        *         @type email:                string
        *         @param firstname:           Firstname for this new cloud user
        *         @type firstname:            string
        *         @param lastname:            Lastname for this new cloud user
        *         @type lastname:             string
        *         @param name:                Name for this new cloud user
        *         @type name:                 string
        *         @param description:         Description for this new cloud user
        *         @type description:          string
        *         @param systemUser:          Indicates if this user is system user
        *         @type systemUser:           boolean
        *         @param jobguid:             guid of the job if avalailable else empty string
        *         @type jobguid:              guid
        *         @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:      dictionary
        *         @return:                    dictionary with cloud user guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                     dictionary
        *         @raise e:                   In case an error occurred, exception is raised
        *         
        */
        public function create (login:String,password:String,email:String="",firstname:String="",lastname:String="",name:String="",description:String="",systemUser:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, login,password,email,firstname,lastname,name,description,systemUser,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Returns a list of cloud users.
        *         @SECURITY administrator only
        *         @execution_method = sync
        *         
        *         @param clouduserguid:     guid of the cloud user specified
        *         @type clouduserguid:      guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  Dictionary of array of dictionaries with guid, login, name, description, firstname, lastname, address, city, country and status for cloud user.
        *         @rtype:                   dictionary
        *         @note:                    Example return value:
        *         @note:                    {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "login": "bgates", "name": "Bill Gates", "description": "CEO of Microsoft corp.", "firstname": "Bill", "lastname": "Gates", "address": "Main road", "city": "Bombai", "country":"India" , "status": "ACTIVE"},
        *         @note:                                 {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "login": "sjobs" , "name": "Steve Jobs", "description": "CEO of Apple corp.", "firstname": "Steve", "lastname": "Jobs", "address": "Antwerpsesteenweg", "city": "Lochristi", "country":"Belgium" , "status": "DISABLED"}]',
        *         @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function list (clouduserguid:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSTATUSES:String = 'listStatuses_response';
        /**
        *         Returns a list of possible cloud user statuses.
        *         @execution_method = sync
        *         
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of statuses.
        *         @rtype:                  dictionary
        *         @note:                   Example return value:
        *         @note:                   {'result': '["CONFIGURED","CREATED", "DISABLED"]',
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




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the cloud user rootobject.
        *         @execution_method = sync
        *         
        *         @param clouduserguid:            guid of the cloud user rootobject
        *         @type clouduserguid:             guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         YAML representation of the cloud user
        *         @rtype:                          string
        *         
        */
        public function getYAML (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETADMINFLAG:String = 'setAdminFlag_response';
        /**
        *         Updates the admin flag for the cloud user specified.
        *         @SECURITY administrator only
        *         
        *         @param clouduserguid:        guid of the cloud user specified
        *         @type clouduserguid:         guid
        *         @param isAdmin:              Admin flag value for this cloud user, default is False.
        *         @type isAdmin:               boolean
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function setAdminFlag (clouduserguid:String,isAdmin:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setAdminFlag', setAdminFlag_ResultReceived, getError, clouduserguid,isAdmin,jobguid,executionparams);

        }

        private function setAdminFlag_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETADMINFLAG, false, false, e.result));
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




        public const EVENTTYPE_LISTMACHINES:String = 'listMachines_response';
        /**
        *         Returns a list of machines of the cloud user.
        *         @execution_method = sync
        *                 
        *         @param clouduserguid:    guid of the cloud user
        *         @type clouduserguid:     guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of machines for the cloud user.
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listMachines (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listMachines', listMachines_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function listMachines_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTMACHINES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update properties, every parameter which is not passed or passed as empty string is not updated.
        *         @SECURITY administrator only
        *         @execution_method = sync
        *         
        *         @param clouduserguid:        guid of the cloud user specified
        *         @type clouduserguid:         guid
        *         @param name:                 Name for this cloud user
        *         @type name:                  string
        *         @param description:          Description for this cloud user
        *         @type description:           string
        *         @param email:                Email for this cloud user
        *         @type email:                 string
        *         @param firstname:            Firstname for this cloud user
        *         @type firstname:             string
        *         @param lastname:             Lastname for this cloud user
        *         @type lastname:              string
        *         @param address:              Address for this cloud user
        *         @type address:               string
        *         @param city:                 City for this cloud user
        *         @type city:                  string
        *         @param country:              Country for this cloud user
        *         @type country:               string
        *         @param phonemobile:          Phonemobile for this cloud user
        *         @type phonemobile:           string
        *         @param phonelandline:        Phonelandline for this cloud user
        *         @type phonelandline:         string
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with cloud user guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (clouduserguid:String,name:String="",description:String="",email:String="",firstname:String="",lastname:String="",address:String="",city:String="",country:String="",phonemobile:String="",phonelandline:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, clouduserguid,name,description,email,firstname,lastname,address,city,country,phonemobile,phonelandline,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTDATACENTERS:String = 'listDatacenters_response';
        /**
        *         Returns a list of datacenters of the cloud user.
        *         @execution_method = sync
        *                 
        *         @param clouduserguid:    guid of the cloud user
        *         @type clouduserguid:     guid
        *         @param jobguid:          guid of the job if avalailable else empty string
        *         @type jobguid:           guid
        *         @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:   dictionary
        *         @return:                 Dictionary of array of datacenters for the cloud user.
        *         @rtype:                  dictionary
        *         @raise e:                In case an error occurred, exception is raised
        *         
        */
        public function listDatacenters (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listDatacenters', listDatacenters_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function listDatacenters_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTDATACENTERS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEPASSWORD:String = 'updatePassword_response';
        /**
        *         Update the password for the cloud user specified.
        *         
        *         @param clouduserguid:        guid of the cloud user specified
        *         @type clouduserguid:         guid
        *         @param currentpassword:      Current password for this cloud user
        *         @type currentpassword:       string
        *         @param newpassword:          New password for this cloud user
        *         @type newpassword:           string
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function updatePassword (clouduserguid:String,currentpassword:String,newpassword:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updatePassword', updatePassword_ResultReceived, getError, clouduserguid,currentpassword,newpassword,jobguid,executionparams);

        }

        private function updatePassword_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEPASSWORD, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the cloud user rootobject.
        *         @execution_method = sync
        *         
        *         @param clouduserguid:            guid of the cloud user rootobject
        *         @type clouduserguid:             guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         @return:                         XML representation of the cloud user
        *         @rtype:                          string
        *         @raise e:                        In case an error occurred, exception is raised
        *         @todo:                           Will be implemented in phase2
        *         
        */
        public function getXML (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETSTATUS:String = 'setStatus_response';
        /**
        *         Updates the admin flag for the cloud user specified.
        *         @SECURITY administrator only
        *         @execution_method = sync
        *         
        *         @param clouduserguid:        guid of the cloud user specified
        *         @type clouduserguid:         guid
        *         @param status:               Status for the cloud user specified. See listStatuses() for the list of possible statuses.
        *         @type status:                string
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function setStatus (clouduserguid:String,status:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setStatus', setStatus_ResultReceived, getError, clouduserguid,status,jobguid,executionparams);

        }

        private function setStatus_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETSTATUS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of cloud user guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param login:                   Login of  the cloud user to include in the search criteria.
        *         @type login:                    string
        *         @param email:                   Email of  the cloud user to include in the search criteria.
        *         @type email:                    string
        *         @param name:                    Name of the cloud user to include in the search criteria.
        *         @type name:                     string
        *         @param status:                  Status of the cloud user to include in the search criteria. See listStatuses().
        *         @type status:                   string        
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         
        *         @return:                        Array of cloud user guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (login:Object=null,email:Object=null,name:Object=null,status:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, login,email,name,status,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Deletes the cloud user specified.
        *         @param clouduserguid:            guid of the cloud user to delete.
        *         @type clouduserguid:             guid
        *         @param jobguid:                  guid of the job if avalailable else empty string
        *         @type jobguid:                   guid
        *         @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:           dictionary
        *         
        *         @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                          dictionary
        *         @raise e:                        In case an error occurred, exception is raised
        *         
        */
        public function deleteClouduser (clouduserguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteClouduser', delete_ResultReceived, getError, clouduserguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

