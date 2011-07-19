class customer:
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name, description="", address="", city="", country="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Creates a new customer
        @execution_method = sync
        
        @param name:                Name for this new customer
        @type name:                 string

        @param description:         Description for this new customer
        @type description:          string

        @param address:             Address for this new customer
        @type address:              string

        @param city:                City for this new customer
        @type city:                 string

        @param country:             Country for this new customer
        @type country:              string

        @param tags: string of tags
        @type tags: string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with returncode and customerguid as result and jobguid: {'result':{returncode:'True', customerguid:guid}, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        """
        
    def delete(self, customerguid, request="", jobguid="", executionparams=dict()):
        """
        Deletes the customer specified.

        @execution_method = sync
        
        @param customerguid:             Guid of the customer to delete.
        @type customerguid:              guid

        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    Guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        """


    def updateModelProperties(self, customerguid, name="",description="", address="", city="", country="", tags="", request="", jobguid="",  executionparams=dict()):
        """
        Update properties, every parameter which is not passed or passed as empty string is not updated.
        @SECURITY administrator only

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param name:                 Name for this customer
        @type name:                  string

        @param description:          Description for this customer
        @type description:           string

        @param address:              Address for this customer
        @type address:               string

        @param city:                 City for this customer
        @type city:                  string

        @param country:              Country for this customer
        @type country:               string
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with returncode and customerguid as result and jobguid: {'result':{returncode:'True', customerguid:guid}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """


    def setStatus(self, customerguid, status, request="", jobguid="", executionparams=dict()):
        """
        Updates the status of the customer specified.

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param status:               Status for the customer specified. See listStatuses() for the list of possible statuses.
        @type status:                string

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def addCloudUserGroup(self, customerguid, cloudusergroupguid, request="", jobguid="", executionparams=dict()):
        """
        Adds a cloud user group to the customer specified.

        @execution_method = sync
        
        @param customerguid:         Gui of the customer specified
        @type customerguid:          guid

        @param cloudusergroupguid:   Guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def removeCloudUserGroup(self, customerguid, cloudusergroupguid, request="", jobguid="", executionparams=dict()):
        """
        Removes a cloud user group for the customer specified.

        @execution_method = sync
        
        @param customerguid:         Gui of the customer specified
        @type customerguid:          guid

        @param cloudusergroupguid:   Guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

   

    def list(self, customerguid="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of customers.
        @SECURITY administrator only

        @execution_method = sync
        
        @param customerguid:     Guid of the customer specified
        @type customerguid:      guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Result is returncode(True) and Dictionary of array of dictionaries with guid, name, description, address, city, country and status for customer(customerinfo).
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': {returncode:True, customerinfo:'[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "Customer1", "description": "My first customer", "address": "Main road", "city": "Bombai", "country":"India" , "status": "ACTIVE"},
        @note:                                {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "name": "Customer2", "description": "My second customer", "address": "Antwerpsesteenweg", "city": "Lochristi", "country":"Belgium" , "status": "DISABLED"}]}',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        """

    def listStatuses(self, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of possible customer statuses.

        @execution_method = sync
        
        @param jobguid:          Guid of the job if avalailable else empty string
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
    
    def listGroups(self, customerguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of cloud user groups for a given customer.
        
        @execution_method = sync
        
        @param customerguid:     Guid of the customer for which to retrieve the list of groups to which this user belongs.
        @type customerguid:      guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 result is dict with a returncode(True) and Dictionary of array of dictionaries with customerguid, login, email, firstname, lastname, cloudusergroupguid, name, description(groupinfo).
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': {returncode:True, groupinfo:'[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                 "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                              "name": "admins",
        @note:                                              "description": "Cloud Administrators"},
        @note:                                             {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                              "name": "users",
        @note:                                              "description": "customers"}]"}]}',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self, name="", status="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of customer guids which meet the search criteria.

        @execution_method = sync
        
        @param name:                    Name of the customer to include in the search criteria.
        @type name:                     string

        @param status:                  Status of the customer to include in the search criteria. See listStatuses().
        @type status:                   string

        @param tags:                    string of tags
        @type tags:                     string

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        result is a dict with returncode(True) and Array of customer guids which met the find criteria specified(guidlist).
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        """
        
    def getAggregatedData(self, customerguid,  meteringtypes, request="", jobguid="", executionparams=dict()):
        """
        Get aggregated data from all meteringdevices owned by this customer
        Supported types are: Current, Power, Energy.
        Values are calculated from the latest monitoringinfo objects of the devices
        
        @param customerguid
        @type guid
        
        @param meteringtypes: list of meteringtypes e.g curret/power/energy
        @type meteringtypes: list 
        
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       result is a dictionary with returncode True and requested values.e.g values:{current:, power:, energy:} and jobguid: {'result': {returncode:True, values:{current:,power:,energy:}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
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
