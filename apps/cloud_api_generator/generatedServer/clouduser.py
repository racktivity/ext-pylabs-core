from pylabs import q
from cloud_api_rootobjects import cloud_api_clouduser
from cloud_api.BaseCloudAPI import BaseCloudAPI

class clouduser(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_clouduser.clouduser()

    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listJobs(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listGroups(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getXMLSchema(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.generateCertificate(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.create(login,password,email,firstname,lastname,name,description,systemUser,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.list(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listStatuses(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getYAML(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.setAdminFlag(clouduserguid,isAdmin,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listMachines(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.updateModelProperties(clouduserguid,name,description,email,firstname,lastname,address,city,country,phonemobile,phonelandline,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.listDatacenters(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.updatePassword(clouduserguid,currentpassword,newpassword,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.getXML(clouduserguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.setStatus(clouduserguid,status,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.find(login,email,name,status,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
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
	return self._rootobject.delete(clouduserguid,jobguid,executionparams)


