class resourcegroup():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name, description="", request="", jobguid="", executionparams=dict()):
        """
        Creates a new resource group

        @execution_method = sync

        @param name:                Name for this new resource group
        @type name:                 string

        @param description:         Description for this new resource group
        @type description:          string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                       dictionary with returncode and resourcegroupguid as result and jobguid: {'result':{returncode:'True', resourcegroupguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                   In case an error occurred, exception is raised
        """
        
    def delete(self, resourcegroupguid, request="", jobguid="", executionparams=dict()):
        """
        Deletes the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:       Guid of the resource group to delete.
        @type resourcegroupguid:        guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request="", jobguid="", executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    Guid of the resourcegroup rootobject
        @type rootobjectguid:     guid

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        """

    

    def updateModelProperties(self, resourcegroupguid, name="",description="", request="", jobguid="", executionparams=dict()):
        """
        Update basic properties, every parameter which is not passed or passed as empty string is not updated.

        @execution_method = sync
        
        @param resourcegroupguid:   Guid of the resource group specified
        @type resourcegroupguid:    guid

        @param name:                Name for this resource group
        @type name:                 string

        @param description:         Description for this resource group
        @type description:          string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                       dictionary with returncode and resourcegroupguid as result and jobguid: {'result':{returncode:'True', resourcegroupguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary
        
        @raise e:                   In case an error occurred, exception is raised
        """


    def addDevice(self, resourcegroupguid, deviceguid, request="", jobguid="", executionparams=dict()):
        """
        Adds an existing device to the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:           Guid of the resource group specified
        @type resourcegroupguid:            guid

        @param deviceguid:                  Guid of the device to add to the resource group specified
        @type deviceguid:                   guid

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                           In case an error occurred, exception is raised
        """

    def removeDevice(self, resourcegroupguid, deviceguid, request="", jobguid="", executionparams=dict()):
        """
        Removes an existing device from the resource group specified.

        @execution_method = sync
        
        @param resourcegroupguid:           Guid of the resource group specified
        @type resourcegroupguid:            guid

        @param deviceguid:                  Guid of the device to remove from the resource group specified
        @type deviceguid:                   guid

        @param jobguid:                     Guid of the job if avalailable else empty string
        @type jobguid:                      guid

        @param executionparams:             dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                           In case an error occurred, exception is raised
        """

    def list(self, resourcegroupguid="",  customerguid="", deviceguid="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of resource groups which are related to the customer and or specified.

        @execution_method = sync
        
        @param resourcegroupguid:   Guid of the resourcegroup from which we wan't to list the data
        @type resourcegroup

        @param customerguid:        Guid of the customer specified
        @type customerguid:         guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary of array of dictionaries with customerguid, and an array of resource groups with resourcegroupguid, customerguid, deviceguids, name, description.
        @rtype:                     dictionary
        @note:                      Example return value:
        @note:                      result: {'returncode':'True', 'meteringdeviceinfo':[{"resourcegroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                               "customerguid": "D51AD737-D29E-4505-989C-8D4E18BCAAE0",
        @note                                                "deviceguids":[D51AD737-D29E-4505-989C-8D4E18BCAAE0, D51AD737-D29E-4505-989C-8D4E18BCAAE0]'
        @note:                                               "name": "RESGROUPCUSTX",
        @note:                                               "description": "Resource group of customer x"]},
        @note:                       'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                   In case an error occurred, exception is raised
        """

    def listDevices(self, resourcegroupguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of devices which are related to the resourcegroup specified.

        @execution_method = sync
        
        @param resourcegroupguid:      Guid of the resource group specified
        @type resourcegroupguid:       guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                        Result is a dict with returncode(True) and Array(guidlist) of device guids which are related to this resourcegroups.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]}',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}


        @raise e:                      In case an error occurred, exception is raised
         """

   
    def find(self, name="", customerguid="", description="", deviceguid="",request="", jobguid="", executionparams=dict()):
        """
        Returns a list of resource groups guids which met the find criteria.

        @execution_method = sync
        
        @param name:                    Name of the resource group to include in the search criteria.
        @type name:                     string
        
        @param customerguid:            guid of the customer, e.g show only resourcegroups related to this customer
        @type: guid
    
        @param description:             Description for this new resource group
        @type description:              string

        @param deviceguid:          Guid of the device to which this resource group is related
        @type deviceguid:           guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Result is a dict with returncode(True) and Array(guidlist) of resourcegroups guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]}',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
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