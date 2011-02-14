from cloud_api_client.Exceptions import CloudApiException

class clouduser:
    def __init__(self, proxy):
        self._proxy = proxy


    def listJobs (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of jobs the cloud user executed.

        @execution_method = sync
                
        @param clouduserguid:    guid of the cloud user
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of machines for the cloud user.
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.listJobs(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listGroups (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Returns the list of groups to which a given clouduser belongs.
 
        @execution_method = sync
               
        @param clouduserguid:    guid of the cloud user for which to retrieve the list of groups to which this user belongs.
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of dictionaries with clouduserguid, login, email, firstname, lastname, cloudusergroupguid, name, description.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '[{"clouduserguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                 "login": "asmith", "email": "adam@smith.com",
        @note:                                 "firstname":"Adam", "lastname": "Smith",
        @note:                                 "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                              "name": "admins",
        @note:                                              "description": "Cloud Administrators"},
        @note:                                             {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                              "name": "users",
        @note:                                              "description": "Cloud Users"}]"}]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.listGroups(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXMLSchema (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the cloud user rootobject structure.

        @execution_method = sync
        
        @param clouduserguid:            guid of the cloud user rootobject
        @type clouduserguid:             guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XSD representation of the cloud user structure.
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.getXMLSchema(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def generateCertificate (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Generates a certificate for the cloud user specified.
        @SECURITY administrator only

        @execution_method = sync
        
        @param clouduserguid:        guid of the cloud user specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.generateCertificate(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, login, password, email = "", firstname = "", lastname = "", name = "", description = "", systemUser = False, jobguid = "", executionparams = {}):
        """
        
        Creates a new cloud user        
        
        @param login:               Login for this new cloud user
        @type login:                string

        @param password:            Password for this new cloud user
        @type password:             string

        @param email:               Email address for this new cloud user
        @type email:                string

        @param firstname:           Firstname for this new cloud user
        @type firstname:            string

        @param lastname:            Lastname for this new cloud user
        @type lastname:             string

        @param name:                Name for this new cloud user
        @type name:                 string

        @param description:         Description for this new cloud user
        @type description:          string

        @param systemUser:          Indicates if this user is system user
        @type systemUser:           boolean

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with cloud user guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.create(login,password,email,firstname,lastname,name,description,systemUser,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, clouduserguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud users.
        @SECURITY administrator only

        @execution_method = sync
        
        @param clouduserguid:     guid of the cloud user specified
        @type clouduserguid:      guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary of array of dictionaries with guid, login, name, description, firstname, lastname, address, city, country and status for cloud user.
        @rtype:                   dictionary
        @note:                    Example return value:
        @note:                    {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "login": "bgates", "name": "Bill Gates", "description": "CEO of Microsoft corp.", "firstname": "Bill", "lastname": "Gates", "address": "Main road", "city": "Bombai", "country":"India" , "status": "ACTIVE"},
        @note:                                 {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "login": "sjobs" , "name": "Steve Jobs", "description": "CEO of Apple corp.", "firstname": "Steve", "lastname": "Jobs", "address": "Antwerpsesteenweg", "city": "Lochristi", "country":"Belgium" , "status": "DISABLED"}]',
        @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                 In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.list(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listStatuses (self, jobguid = "", executionparams = {}):
        """
        
        Returns a list of possible cloud user statuses.

        @execution_method = sync
        
        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of statuses.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '["CONFIGURED","CREATED", "DISABLED"]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.listStatuses(jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the cloud user rootobject.

        @execution_method = sync
        
        @param clouduserguid:            guid of the cloud user rootobject
        @type clouduserguid:             guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         YAML representation of the cloud user
        @rtype:                          string
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.getYAML(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def setAdminFlag (self, clouduserguid, isAdmin = False, jobguid = "", executionparams = {}):
        """
        
        Updates the admin flag for the cloud user specified.
        @SECURITY administrator only
        
        @param clouduserguid:        guid of the cloud user specified
        @type clouduserguid:         guid

        @param isAdmin:              Admin flag value for this cloud user, default is False.
        @type isAdmin:               boolean

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.setAdminFlag(clouduserguid,isAdmin,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['clouduser'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listMachines (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of machines of the cloud user.

        @execution_method = sync
                
        @param clouduserguid:    guid of the cloud user
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of machines for the cloud user.
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.listMachines(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, clouduserguid, name = "", description = "", email = "", firstname = "", lastname = "", address = "", city = "", country = "", phonemobile = "", phonelandline = "", jobguid = "", executionparams = {}):
        """
        
        Update properties, every parameter which is not passed or passed as empty string is not updated.
        @SECURITY administrator only

        @execution_method = sync
        
        @param clouduserguid:        guid of the cloud user specified
        @type clouduserguid:         guid

        @param name:                 Name for this cloud user
        @type name:                  string

        @param description:          Description for this cloud user
        @type description:           string

        @param email:                Email for this cloud user
        @type email:                 string

        @param firstname:            Firstname for this cloud user
        @type firstname:             string

        @param lastname:             Lastname for this cloud user
        @type lastname:              string

        @param address:              Address for this cloud user
        @type address:               string

        @param city:                 City for this cloud user
        @type city:                  string

        @param country:              Country for this cloud user
        @type country:               string

        @param phonemobile:          Phonemobile for this cloud user
        @type phonemobile:           string

        @param phonelandline:        Phonelandline for this cloud user
        @type phonelandline:         string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with cloud user guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.updateModelProperties(clouduserguid,name,description,email,firstname,lastname,address,city,country,phonemobile,phonelandline,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listDatacenters (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of datacenters of the cloud user.

        @execution_method = sync
                
        @param clouduserguid:    guid of the cloud user
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of datacenters for the cloud user.
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.listDatacenters(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updatePassword (self, clouduserguid, currentpassword, newpassword, jobguid = "", executionparams = {}):
        """
        
        Update the password for the cloud user specified.
        
        @param clouduserguid:        guid of the cloud user specified
        @type clouduserguid:         guid

        @param currentpassword:      Current password for this cloud user
        @type currentpassword:       string

        @param newpassword:          New password for this cloud user
        @type newpassword:           string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.updatePassword(clouduserguid,currentpassword,newpassword,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the cloud user rootobject.

        @execution_method = sync
        
        @param clouduserguid:            guid of the cloud user rootobject
        @type clouduserguid:             guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XML representation of the cloud user
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.getXML(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def setStatus (self, clouduserguid, status, jobguid = "", executionparams = {}):
        """
        
        Updates the admin flag for the cloud user specified.
        @SECURITY administrator only

        @execution_method = sync
        
        @param clouduserguid:        guid of the cloud user specified
        @type clouduserguid:         guid

        @param status:               Status for the cloud user specified. See listStatuses() for the list of possible statuses.
        @type status:                string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.setStatus(clouduserguid,status,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, login = "", email = "", name = "", status = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user guids which met the find criteria.

        @execution_method = sync
        
        @param login:                   Login of  the cloud user to include in the search criteria.
        @type login:                    string

        @param email:                   Email of  the cloud user to include in the search criteria.
        @type email:                    string

        @param name:                    Name of the cloud user to include in the search criteria.
        @type name:                     string

        @param status:                  Status of the cloud user to include in the search criteria. See listStatuses().
        @type status:                   string        

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary
        
        @return:                        Array of cloud user guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.find(login,email,name,status,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the cloud user specified.

        @param clouduserguid:            guid of the cloud user to delete.
        @type clouduserguid:             guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        
        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_clouduser.delete(clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



