class backplane():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name, backplanetype, description=None, publicflag=False, managementflag=False, storageflag=False, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Create a new backplane.

        @param name:                   Name for the backplane.
        @type name:                    string

        @param backplanetype:          Type of the backplane (ETHERNET, INFINIBAND)
        @type backplanetype:           string

        @param description:            Description for the backplane.
        @type description:             string

        @param publicflag:             Indicates if the backplane is a public backplane.
        @type publicflag:              boolean

        @param storageflag:            Indicates if the backplane is a storage backplane.
        @type storageflag:             boolean

        @param managementflag:         Indicates if the backplane is a management backplane.
        @type managementflag:          boolean
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and backplaneguid as result and jobguid: {'result':{returncode:'True', backplaneguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, backplaneguid, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a backplane.

        @param backplaneguid:          Guid of the backplane rootobject to delete.
        @type backplaneguid:           guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def updateModelProperties(self, backplaneguid,  name=None,  backplanetype=None, description=None, tags=[], request=None, jobguid=None, executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @param backplaneguid:          Guid of the backplane specified
        @type backplaneguid:           guid

        @param name:                   Name for this backplane
        @type name:                    string
        
        @param backplanetype:          Type of the backplane (ETHERNET, INFINIBAND)
        @type backplanetype:           string

        @param description:            Description for this backplane
        @type description:             string
        
        @param tags: Array of tags(strings)
        @type tags: array

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and backplaneguid as result and jobguid: {'result':{returncode:'True', backplaneguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setFlags(self, backplaneguid, publicflag=False, managementflag=False, storageflag=False, request=None, jobguid=None, executionparams=dict()):
        """
        Sets the role flags for the specified backplane.

        @param backplaneguid:          Guid of the backplane
        @type backplaneguid:           guid

        @param publicflag:             Defines if the backplane is used as a public backplane. Not modified if empty.
        @type publicflag:              boolean

        @param managementflag:         Defines if the backplane is used as a management backplane. Not modified if empty.
        @type managementflag:          boolean

        @param storageflag:            Defines if the backplane is used as a storage backplane. Not modified if empty.
        @type storageflag:             boolean

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name=None, managementflag=None, publicflag=None, storageflag=None, backplanetype=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of backplane guids which met the find criteria.
        
        @execution_method = sync

        @param name:                    Name of the backplanes to include in the search criteria.
        @type name:                     string

        @param managementflag:          managementflag of the backplanes to include in the search criteria.
        @type managementflag:           boolean

        @param publicflag:              publicflag of the backplanes to include in the search criteria.
        @type publicflag:               boolean

        @param storageflag:             storageflag of the backplanes to include in the search criteria.
        @type storageflag:              boolean

        @param backplanetype:           Type of the backplanes to include in the search criteria.
        @type backplanetype:            int

        @param tags:                    string of tags
        @type tags:                     string

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Result is a dict with returncode(True) and Array(guidlist) of backplane guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]}',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        """

    def list(self, backplaneguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all backplanes.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane
        @type backplaneguid:            guid
 
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        result is a dict with returncode(True) and array(backplaneinfo) of backplane info as result and jobguid: {'result':{returncode:True, backplaneinfo: array}, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True, backplaneinfo:[{ 'backplaneguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'Storage Backplane',
        @note:                                      'backplanetype': 'INFINIBAND',
        @note:                                      'public': False,
        @note:                                      'storage': True,
        @note:                                      'management': False},
        @note:                                    { 'backplaneguid': '789544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'Management Backplane',
        @note:                                      'backplanetype': 'ETHERNET',
        @note:                                      'public': False,
        @note:                                      'storage': False,
        @note:                                      'management': False}]}}
        
        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    Guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        """

    def updateACL(self, rootobjectguid, cloudusergroupnames={}, request=None, jobguid=None, executionparams=dict()):
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

    def addGroup(self, rootobjectguid, group, action=None, recursive=False, request=None, jobguid=None, executionparams=dict()):
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


    def deleteGroup(self, rootobjectguid, group, action=None, recursive=False, request=None, jobguid=None, executionparams=dict()):
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


    def hasAccess(self, rootobjectguid, groups, action, request=None, jobguid=None, executionparams=dict()):
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