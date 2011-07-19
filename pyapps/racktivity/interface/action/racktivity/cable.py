class cable():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """


    def create(self, name, cabletype, description="",label="" ,tag="" ,request="", jobguid="", executionparams=dict()):
        """
        Create a new cable.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the cable.
        @type name:                    string

        @param description:            description of the cable
        @type description:             string

        @param cabletype:              cable type
        @type cabletype:               cabletype

        @param label:                  label attached to cable
        @type label:                   string(60)
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode and cableguid as result and jobguid: {'result':{returncode:'True', cableguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, cableguid, request="", jobguid="", executionparams=dict()):
        """
        Delete a cable.

        @execution_method = sync
        
        @security administrators
        @param cableguid:             Guid of the cable rootobject to delete.
        @type cableguid:              guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid


        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def updateModelProperties(self, cableguid, name="", cabletype="", description="",label="" ,tags="",  request="", jobguid="", executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @security administrators
        @param cableguid:              Guid of the cable specified
        @type cableguid:               guid

        @param name:                   Name for the cable.
        @type name:                    string

        @param description:            description of the cable
        @type description:             string

        @param cabletype:              cable type
        @type cabletype:               cabletype

        @param label:                  label attached to cable
        @type label:                   string(60)
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and cableguid as result and jobguid: {'result':{returncode:'True', cableguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name="", cabletype="", description="", label="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of cable guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the cable.
        @type name:                    string

        @param description:            description of the cable
        @type description:             string

        @param cabletype:              cable type
        @type cabletype:               cabletype

        @param label:                  label attached to cable
        @type label:                   string(60)

        @param tags:                   string of tags
        @type tags:                    string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Result is a dict containing, returncode(True) and Array(guidlist) of cable guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, cableguid="", request="", jobguid="", executionparams=dict()):
        """
        List all cables.

        @execution_method = sync
        
        @param cableguid:               Guid of the cable specified
        @type cableguid:                guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of cable info as result and jobguid: {'result': {returncode:True, cableinfo:[], 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True, cableinfo: [{ 'cableguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'cable0001',
        @note:                                      'description': 'cable 0001',
        @note:                                      'cabletype': 'USBCABLE'
        @note:                                      'label': ''}]}}
        
        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the cable rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
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