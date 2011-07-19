class clouduser():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, login, password, email="", firstname="", lastname="", name="", description="", tags="",  request="", jobguid="", executionparams=dict()):
        """
        Creates a new cloud user

        @execution_method = sync
        
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
        
        @param tags: Array of tags(strings)
        @type tags: array

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with returncode and clouduserguid as result and jobguid: {'result':{returncode:'True', clouduserguid:guid}, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        """

    def delete(self, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Deletes the cloud user specified.

        @execution_method = sync
        
        @param clouduserguid:            guid of the cloud user to delete.
        @type clouduserguid:             guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        
        @return:                         dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request="", jobguid="", executionparams=dict()):
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

 
    def updateModelProperties(self, clouduserguid, name="",description="", email="", firstname="", lastname="", address="", city="", country="", phonemobile="", phonelandline="", tags="",  request="", jobguid="", executionparams=dict()):
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
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                    dictionary with returncode and clouduserguid as result and jobguid: {'result':{returncode:'True', clouduserguid:guid}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """


    def updatePassword(self, clouduserguid, currentpassword, newpassword, request="", jobguid="", executionparams=dict()):
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

        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def setStatus(self, clouduserguid, status, request="", jobguid="", executionparams=dict()):
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

        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """


    def list(self, clouduserguid="", request="", jobguid="", executionparams=dict()):
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

        @return:                  result is a dict with a  returncode(True) and Dictionary(clouduserinfo) of array of dictionaries with guid, login, name, description, firstname, lastname, address, city, country and status for cloud user.
        @rtype:                   dictionary
        @note:                    Example return value:
        @note:                    {'result': {returncode:True, clouduserinfo:'[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "login": "bgates", "name": "Bill Gates", "description": "CEO of Microsoft corp.", "firstname": "Bill", "lastname": "Gates", "address": "Main road", "city": "Bombai", "country":"India" , "status": "ACTIVE"},
        @note:                                 {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "login": "jdoe" , "name": "John Doe", "description": "main user.", "firstname": "John", "lastname": "Due", "address": "Antwerpsesteenweg", "city": "Lochristi", "country":"Belgium" , "status": "DISABLED"}}]',
        @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                 In case an error occurred, exception is raised
        """

    def find(self, login="", email="", name="", status="", tags="", request="", jobguid="", executionparams=dict()):
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

        @param tags:                    string of tags
        @type tags:                     string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary
        
        @return:                        result is a dict with a returncode(True) and  Array(guidlist) of cloud user guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': {returncode:True, guidlist: '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        """

    def listStatuses(self, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of possible cloud user statuses.

        @execution_method = sync
        
        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

       @return:                 result is a dictionary of a returncode(True) and a array of statuses.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': {returncode:True, statuses:'["ACTIVE", "CONFIGURED", "DISABLED"]'},
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        """

    def listGroups(self, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Returns the list of groups to which a given clouduser belongs.
 
        @execution_method = sync
               
        @param clouduserguid:    guid of the cloud user for which to retrieve the list of groups to which this user belongs.
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 result is a dict with returncode(True) and Dictionary(groupinfo) of array of dictionaries with clouduserguid, login, email, firstname, lastname, cloudusergroupguid, name, description.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result':{returncode:True, groupinfo: '[{"clouduserguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                 "login": "asmith", "email": "adam@smith.com",
        @note:                                 "firstname":"Adam", "lastname": "Smith",
        @note:                                 "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                              "name": "admins",
        @note:                                              "description": "Cloud Administrators"},
        @note:                                             {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                              "name": "users",
        @note:                                              "description": "Cloud Users"}]"}]'},
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        """

    def listDatacenters(self, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of datacenters of the cloud user.

        @execution_method = sync
                
        @param clouduserguid:    guid of the cloud user
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 result is a dict with returncode(True) and Dictionary(guidlist) of array of datacenters for the cloud user.
        @note:                   {result:{returncode:True, guidlist:[],}, jobguid:}
        @note:
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """
        
    def listDevices(self, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of devices of the cloud user.

        @execution_method = sync
                
        @param clouduserguid:    guid of the cloud user
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 result is a dict with returncode(True) and Dictionary(guidlist) of array of datacenters for the cloud user.
        @note:                   {result:{returncode:True, guidlist:[],}, jobguid:}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """
        
    def listJobs(self, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of jobs the cloud user executed.

        @execution_method = sync
                
        @param clouduserguid:    guid of the cloud user
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 result is a dict with returncode(True) and Dictionary(guidlist) of array of datacenters for the cloud user.
        @note:                   {result:{returncode:True, guidlist:[],}, jobguid:}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def updateACL(self, rootobjectguid, cloudusergroupnames={}, request="", jobguid="", executionparams=dict()):
        """
        Update ACL in a rootobject.
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param cloudusergroupnames:          Dict with keys in the form of cloudusergroupguid_actionname and empty values for now.
        @type cloudusergroupnames:           dict

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """

    def addGroup(self, rootobjectguid, group, action="", recursive=False, request="", jobguid="", executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to add to the specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group gets access to all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is added to all children objects
        @type recursive:                     Boolean 
        
        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def deleteGroup(self, rootobjectguid, group, action="", recursive=False, request="", jobguid="", executionparams=dict()):
        """
        Delete a group in the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to delete for a specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group is deleted from all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is deleted from all children objects
        @type recursive:                     Boolean         

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def hasAccess(self, rootobjectguid, groups, action, request="", jobguid="", executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the selected root object.
        @type rootobjectguid:                guid

        @param groups:                       list of groups to be checked
        @type groups:                        list 

        @param action:                       name of the required action.
        @type action:                        String

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode as result and jobguid: {'result':{returncode:'True'}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """