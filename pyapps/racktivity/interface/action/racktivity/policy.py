class policy:
    
    def create(self, name, rootobjecttype, rootobjectaction, rootobjectguid, interval, runbetween=None, runnotbetween=None, policyparams=None,  description=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Creates a new policy.

        @execution_method = sync
        
        @param name:                     Name for the new policy
        @type name:                      string

        @param rootobjecttype:           RootObject type for the new policy
        @type rootobjecttype:            string
        
        @param rootobjectaction:         Name of the action for the new policy
        @type rootobjectaction:          string
        
        @param rootobjectguid:           Guid of the rootobject for the new policy
        @type rootobjectguid:            string
        
        @param interval:                 Interval for the new policy
        @type interval:                  int
        
        @param runbetween:               List of tuples with timestamps when a policy can run
        @type runbetween:                list
        
        @param runnotbetween:            List of tuples with timestamps when a policy can not run
        @type runnotbetween:             string
        
        @param policyparams:             Params for the new policy
        @type policyparams:              string
        
        @param description:              Description for the new policy
        @type description:               string
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:                  Guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with returncode and policyguid as result and jobguid: {'result':{returncode:'True', policyguid:guid}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def delete(self, policyguid, request=None, jobguid=None, executionparams=dict()):
        """
        Deletes the given policy.

        @execution_method = sync
        
        @param policyguid:               Guid of the policy to delete.
        @type policyguid:                guid

        @param jobguid:                  Guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """
        # make sure all ip addresses are disconnected from the required hosts before the lan can be disconnec
    
    def list(self, policyguid=None,name=None, rootobjectaction=None, rootobjecttype=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of all policies depending on passed filters.

        @execution_method = sync
        
        @param policyguid:                   Guid of the cloudspace
        @type policyguid:                    guid
        
        @param name:                         Name of the policy
        @type name:                          string
        
        @param rootobjectaction:             Action on the rootobject
        @type rootobjectaction:              string         
        
        @param rootobjecttype:               Rootobject type e.g. sso
        @type rootobjecttype:                string

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode(True) and array of policy info as result and jobguid: {'result':{returncode:True, policyinfo:[]}, 'jobguid': guid}
        @rtype:                              dictionary
        @note:                               {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                'result:{returncode:True, policyinfo: [{ 'name': 'Daily backup DBServer'
        @note:                                            'description': 'Daily backup of our database server',
        @note:                                            'rootobjecttype': 'machine',
        @note:                                            'rootobjectaction': 'backup',
        @note:                                            'policyparams': {},
        @note:                                            'rootobjectguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                            'interval': 86400,
        @note:                                            'lastrun': '2009-05-23 11:25:33',
        @note:                                            'runbetween': [("00:00", "02.00"), ("04:00", "06:00")],
        @note:                                            'runnotbetween': [("08:00", "12:00"), ("14:00", "18:00")]}]}}
        
        @raise e:                            In case an error occurred, exception is raised
        """
        
    def listToRun(self, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of all policies that needs to be exectued

        @execution_method = sync
        
        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode(True) and array of policy info as result and jobguid: {'result':{returncode:True, policyinfo:[]}, 'jobguid': guid}
        @rtype:                              dictionary
        @note:                               {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                'result:{returncode:True, policyinfo: [{ 'name': 'Daily backup DBServer'
        @note:                                            'description': 'Daily backup of our database server',
        @note:                                            'rootobjecttype': 'machine',
        @note:                                            'rootobjectaction': 'backup',
        @note:                                            'policyparams': {},
        @note:                                            'rootobjectguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                            'interval': 86400,
        @note:                                            'lastrun': '2009-05-23 11:25:33',
        @note:                                            'runbetween': [("00:00", "02.00"), ("04:00", "06:00")],
        @note:                                            'runnotbetween': [("08:00", "12:00"), ("14:00", "18:00")]}]}}
        
        @raise e:                            In case an error occurred, exception is raised
        """
    
    def find(self, name=None, description=None, rootobjecttype=None, rootobjectaction=None, rootobjectguid=None, interval=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of policy guids which met the find criteria.

        @execution_method = sync
        
        @param name:               Name of the policy
        @type name:                string
        
        @param description:        description of the policy
        @type description:         string

        @param rootobjecttype:     Rootobject type.
        @type rootobjecttype:      string

        @param rootobjectaction:   Action to execute on the rootobject
        @type rootobjectaction:    string

        @param rootobjectguid:     Guid of the rootobject
        @type rootobjectguid:      string

        @param interval:           Interval in seconds
        @type interval:            int

        @param tags:               string of tags
        @type tags:                string

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with returncode(True) and array of policy guids as result and jobguid: {'result': {returncode:True, guidlist:guids}, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        """

    def updateModelProperties(self, policyguid, name=None,description=None, lastrun=None, policyparams=None, interval=None, runbetween=None, runnotbetween=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of policy guids which met the find criteria.

        @execution_method = sync
        
        @param name:               Name of the policy
        @type name:                string
        
        @param description:        description of the policy
        @type description:         string
        
        @param lastrun:            lastrun of the policy
        @type lastrun:             datetime
        
        @param tags: Array of tags(strings)
        @type tags: array
        
        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid
        
        @param policyparams:       Policy parameters
        @type policyparams:        string
        
        @param interval:           Policy interval in minutes
        @type interval:            float
        
        @param runbetween:         List of tuples with timestamps when a policy can run
        @type runbetween:          list
        
        @param runnotbetween:      List of tuples with timestamps when a policy can not run
        @type runnotbetween:       string
        
        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with returncode and policyguid as result and jobguid: {'result':{returncode:'True', policyguid:guid}, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised        
        """
        
        
    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:     guid of the policy object
        @type rootobjectguid:      guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   rootobject
        @rtype:                    string

        @warning:                  Only usable using the python client.
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