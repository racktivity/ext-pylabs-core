class errorcondition:
    """
    errorcondition class
    """

    def create(self, errorconditiontype=None, timestamp=None, level=None, agent=None, errormessagepublic=None, errormessageprivate=None,
               application=None, backtrace=None, logs=None, transactioninfo=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Create a new errorcondition

        @execution_method = sync

        @param errorconditiontype:       type of errorcondition
        @type errorconditiontype:        int

        @param timestamp:                timestamp of errorcondition
        @type timestamp:                 int

        @param level:                    level of errorcondition
        @type level:                     string

        @param agent:                    unique id of agent
        @type agent:                     string

        @param tags:                     series of tags format
        @type tags:                      string

        @params errormessagepublic:      public error message
        @type errormessagepublic         string

        @params errormessageprivate:     private error message
        @type errormessageprivate        string

        @param application:              name of the application
        @type application:               string

        @param backtrace:                backtrace message
        @type backtrace:                 string

        @param logs:                     log message
        @type logs:                      string

        @param transactioninfo:          info of the transaction
        @type transactioninfo:           string
        
        @param tags: Array of tags(strings)
        @type tags: array

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with returncode and errorconditionguid as result and jobguid: {'result':{returncode:'True', errorconditionguid:guid}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def find(self, errorconditiontype=None, timestamp=None, level=None, agent=None, tags=None, application=None, request=None, jobguid=None,executionparams=dict()):
        """
        @execution_method = sync

        @param errorconditiontype:       type of errorcondition
        @type errorconditiontype:        string

        @param timestamp:                timestamp of errorcondition
        @type timestamp:                 int

        @param level:                    level of errorcondition
        @type level:                     int

        @param agent:                    unique id of agent
        @type agent:                     string

        @param tags:                     series of tags format
        @type tags:                      string

        @param application:              name of the application
        @type application:               string

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        
        @returns result is a dict with returncode(True) and list of guids(guidlist) 
        Example: {result:{returncode:True, guidlist:[]}, jobguid:guid}
        @rtype dictionary
        
        """

    def getObject(self, errorconditionguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync

        @param errorconditionguid:   guid of the job rootobject
        @type errorconditionguid:    guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     rootobject
        @rtype:                      rootobject

        @warning:                    Only usable using the python client.
        """


    def delete(self, errorconditionguid, request=None, jobguid=None,executionparams=dict()):
        """
        Delete the specified errorcondition

        @security: administrator

        @execution_method = sync

        @param errorconditionguid:       guid of the errorcondition
        @type errorconditionguid:        guid

        @param jobguid:                  guid of the errorcondition if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of errorcondition specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and errorcondition: {'result': True, 'errorconditionguid': guid}
        @rtype:                          dictionary

        @raise e:                         dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        """

    def list(self, errorconditionguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all errorconditions or only specified errorcondition

        @execution_method = sync

        @param errorconditionguid:       guid of the errorcondition
        @type errorconditionguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid


        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         return is a dict with returncode(True) and dictionary with array of errorcondition info(errorconditioninfo) as result and jobguid: {'result': {returncode:true, errorconditioninfo:array}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def raiseErrorCondition(self, level=None, typeid=None, errormessagepublic=None, errormessageprivate=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Create a new errorcondition and escalate it

        @execution_method = sync

        @param level:                    level of errorcondition ('CRITICAL','ERROR','INFO','UNKNOWN','URGENT','WARNING')
        @type level:                     string
        
        @param typeid:                   predefined type id (ex. SSO-MON-NETWORK-0001)
        @type typeid:                    string

        @params errormessagepublic:      public error message
        @type errormessagepublic         string

        @params errormessageprivate:     private error message
        @type errormessageprivate        string

        @param tags:                     series of tags format
        @type tags:                      string

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with returncode and errorconditionguid as result and jobguid: {'result':{returncode:'True', errorconditionguid:guid}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
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
