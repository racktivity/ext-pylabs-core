class cloudusergroup():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name="", description="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Creates a new cloud user group
        
        @execution_method = sync
        
        @param name:                Name for this new cloud user group
        @type name:                 string

        @param description:         Description for this new cloud user group
        @type description:          string
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with returncode and cloudusergroupguid as result and jobguid: {'result':{returncode:'True', cloudusergroupguid:guid}, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        """
        
    def delete(self, cloudusergroupguid, request="", jobguid="", executionparams=dict()):
        """
        Deletes the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group to delete.
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
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
        
        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        """

    def updateModelProperties(self, cloudusergroupguid, name="",description="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Update basic properties, every parameter which is not passed or passed as empty string is not updated.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param name:                 Name for this cloud user group
        @type name:                  string

        @param description:          Description for this cloud user group
        @type description:           string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param tags: string of tags
        @type tags: string

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with returncode and cloudusergroupguid as result and jobguid: {'result':{returncode:'True', cloudusergroupguid:guid}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def addUser(self, cloudusergroupguid, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Add an existing cloud user to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param clouduserguid:        Gui of the cloud user to add to the cloud user group specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def removeUser(self, cloudusergroupguid, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Remove an existing cloud user from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param clouduserguid:        Gui of the cloud user to remove from the cloud user group specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def addGroup(self, cloudusergroupguid, membercloudusergroupguid, request="", jobguid="", executionparams=dict()):
        """
        Add an existing cloud user group to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param membercloudusergroupguid:     Gui of the cloud user group who should become a member of the cloud user group specified
        @type membercloudusergroupguid:      guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """

    def removeGroup(self, cloudusergroupguid, membercloudusergroupguid, request="", jobguid="", executionparams=dict()):
        """
        Remove an existing cloud user group from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param membercloudusergroupguid:     Gui of the cloud user group who should be removed from the cloud user group specified
        @type membercloudusergroupguid:      guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """

    def list(self, customerguid="", cloudusergroupguid="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of cloud user groups which are related to the customer specified.

        @execution_method = sync
        
        @param customerguid:         guid of the customer for which to retrieve the list of cloud user groups.
        @type customerguid:          guid

        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     result is dict with returncode(True) and Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description(cloudusergroupinfo).
        @rtype:                      dictionary
        @note:                       Example return value:
        @note:                       {'result': {returncode:True, cloudusergroupinfo:'[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                     "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                                  "name": "admins",
        @note:                                                  "description": "Cloud Administrators"},
        @note:                                                 {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                                  "name": "users",
        @note:                                                  "description": "cloud user groups"}]"}]',
        @note:                        'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                    In case an error occurred, exception is raised
        """

    def find(self, name="", request="", jobguid="", tags="", executionparams=dict()):
        """
        Returns a list of cloud user groups guids which met the find criteria.

        @execution_method = sync
        
        @param name:                    Name of the cloud user group to include in the search criteria.
        @type name:                     string

        @param tags:                    string of tags
        @type tags:                     string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        return is a dict with returncode(True) and guidlist, Array of cloud user group guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': {returncode:True, guildlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        """

    def listUsers(self, cloudusergroupguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of cloud users which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid:  guid of the cloud user group specified
        @type cloudusergroupguid:   guid

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    result is a dict with returncode and Dictionary (userlist)of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        {'result':{returncode:True, userlist:{}}, jobguid:}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        """
        
    def listGroups(self, cloudusergroupguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of cloud user groups which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid: guid of the cloud user group specified
        @type cloudusergroupguid:  guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                    result is a dict with returncode and Dictionary(grouplist) of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        {'result':{returncode:True, grouplist:{}}, jobguid:}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
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



