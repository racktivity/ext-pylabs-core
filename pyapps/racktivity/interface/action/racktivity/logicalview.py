class logicalview():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """
    def create(self, name,  viewstring, description="",  clouduserguid="", share=False,  tags="",  request="", jobguid="", executionparams=dict()):
        """
        Create a new logical view

        @params name: name of the logical view
        @type name: string

        @params viewstring: definition of the view
        @type viewstring: string

        @params: description of the logical view
        @type description: string

        @params: clouduserguid which created this view
        @type clouduserguid: guid

        @params share: if shared, it appears in all logical vies
        @type share: boolean

        @param tags: string of tags
        @type tags: string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and guid, jobguid: {'result': {'returncode':True, guid:}, 'jobguid': guid}
        @rtype:                   dictionary
        """

    def delete(self, logicalviewguid, request="", jobguid="", executionparams=dict()):
        """
        Deletes a pod

        @params logicalviewguid: guid of the logical_view to delete
        @type version: guid

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """

    def updateModelProperties(self, logicalviewguid, name="",  viewstring="", description="",  clouduserguid="", share=False,  tags="", request="", jobguid="", executionparams=dict()):
        """
        Update model properties for a logical view with guid(logicalviewguid)

        @param logicalviewguid: guid of the logical view to update
        @type: string

        @params name: name of the logical view
        @type name: string

        @params viewstring: definition of the view
        @type viewstring: string

        @params: description of the logical view
        @type description: string

        @params: clouduserguid which created this view
        @type clouduserguid: guid

        @params share: if shared, it appears in all logical vies
        @type share: boolean

        @param tags: string of tags
        @type tags: string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """


    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync

        @param rootobjectguid:   guid of the logical view object
        @type rootobjectguid:    guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 rootobject
        @rtype:                  rootobject

        @warning:                Only usable using the python client.
        """

    def find(self, name="", clouduserguid="", share="", tags="", request="", jobguid="", executionparams=dict()):
        """
        @param name: name of the logical view to find
        @type name: string

        @param clouduserguid: clouduser guid
        @type clouduserguid: guid

        @param share: show all shared logical views.
        @type share: boolean

        @param tags:             string of tags
        @type tags:              string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and logical guids  as result and jobguid: {'result': {'returncode':True,'guidlist':[]}, 'jobguid': guid}
        @rtype:                   dictionary
        """

    def list(self, name="", clouduserguid="", share="", tags="",  request="", jobguid="", executionparams=dict()):
        """
        List found logical views and return logical view information

        @param name: name of the logical view to find
        @type name: string

        @param clouduserguid: clouduser guid
        @type clouduserguid: guid

        @param share: show all shared logical views.
        @type share: boolean

        @param tags:             string of tags
        @type tags:              string

        @param jobguid:           Guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and logical_view information  as result and jobguid: {'result': {'returncode':True,'logicalview_information:{}}, 'jobguid': guid}
        a logical_view informatin contains the following info:
        {logicalviewguid:{name:, clouduser, description:, tags:}}
        @rtype:                   dictionary
        """

    def getViewResult (self, logicalviewguid, request="", jobguid="", executionparams=dict()):
        """
        Get the result of a specific view


        @param jobguid:           Guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and logical_view_result as result and jobguid: {'result': {'returncode':True,'logicalview_result:{}}, 'jobguid': guid}
        a  logical view informatin contains the following info:
        @rtype:                   dictionary
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


    def getPduHealthStatus(self, guid, timing = [3600, 86400], request="", jobguid="", executionparams=dict()):
        """
        getHealtStatus, returns a list of 3 values, the first list contains the amount of pdus  which monitoring data is more recent then currenttime-timing[0], the second the  # of pdus  which are last monitored between currenttime - timing[0] and currenttime - timing[1] and the last list contains the amount of pdus which are monitored later then currenttime - timing[1]
        
        E.g:  [200, 5, 2]
        
        Timing contains the time intervals in seconds.(defaults are set on one hour and 1 day)
        
        @params guid: logicalview guid 
        @type timing: guid
        
        @params timing: timing intervals
        @type timing: list
        
        @return: a dictionary containing this information {'result': {returncode:'True', healthstatus:[],} jobguid:guid}
        @type: dict
        """
