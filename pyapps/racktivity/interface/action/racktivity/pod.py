class Pod():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """
    def create(self, name,  alias=None, description=None, roomguid=None, tags=None,  request=None, jobguid=None, executionparams=dict()):
        """
        Create a pod in a room with a list of racks
        
        @params name: name of the pod
        @type name: string
        
        @params alias: alias of the pod
        @type alias: string
        
        @params: description of the pod
        @type description: string
        
        @params: roomguid in which the pod is located
        @type roomguid: guid
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and guid, jobguid: {'result': {'returncode':True, guid:}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def delete(self, podguid, request=None, jobguid=None, executionparams=dict()):
        """
        Deletes a pod
        
        @params podguid: guid of the pod to delete
        @type version: guid
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def updateModelProperties(self, podguid, name=None, alias=None, description=None, roomguid=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update model properties for a pod with guid(podguid)

        @params enterpriseguid: guid of the pod
        @type enterpriseguid: string
        
        @params name: name of the pod
        @type name: string
        
        @params alias: alias name of the pod
        @type alias: string
        
        @params description: description of the pod
        @type description: string
        
        @params roomguid: room guid in which the pod is located
        @type: roomguid: string
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    
    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:   guid of the job rootobject
        @type rootobjectguid:    guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 rootobject
        @rtype:                  rootobject

        @warning:                Only usable using the python client.
        """
        
    def find(self, name=None,  alias=None, roomguid=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        
        @execution_method = sync
        
        @param name: name of the pods to find
        @type name: string
        
        @param alias: alias name of the pod to find
        @type alias: string
        
        @param roomguid: list pods located in the room
        @type roomguid: guid
        
        @param tags:             string of tags
        @type tags:              string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and pod guids  as result and jobguid: {'result': {'returncode':True,'guidlist':[]}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def list(self, podguid=None, name=None,  alias=None, roomguid=None, tags=None,  request=None, jobguid=None, executionparams=dict()):
        """
        List found pods and return pod information
        
        @execution_method = sync
        
        @param podguid: guid of the pod
        @type podguid: guid
        
        @param name: name of the pods to find
        @type name: string
        
        @param alias: alias name of the pod to find
        @type alias: string
        
        @param roomguid: list pods located in the roomguid
        @type roomguid: guid
        
        @param tags:             string of tags
        @type tags:              string
        
        @param jobguid:           Guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and pod information  as result and jobguid: {'result': {'returncode':True,'podinformation:{}}, 'jobguid': guid}
        a pod informatin contains the following info:
        {podguid:{name:, alias, description:, roomguid: ,racks:, tags:,,}}
        @rtype:                   dictionary
        """
        
    def getAggregatedData(self, podguid, meteringtypes, request=None, jobguid='', executionparams={}):
        """
        Get aggregated data from all racks in the pod
        Supported types are: Current, Power, Energy.
        Values are calculated from the latest monitoringinfo objects of the devices in the room.
        
        @param podguid:         guid of the pod
        @type podguid:          guid
        
        @param meteringtypes:     list of meteringtypes e.g curret/power/energy
        @type meteringtypes:      list or string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  result is a dictionary with returncode True and requested values.e.g values:{current:, power:, energy:} and jobguid: {'result': {returncode:True, values:{current:,power:,energy:}, 'jobguid': guid}
        @rtype: dictionay
        """
     
    def getMeteringdevicesCount(self, podguid, jobguid='', executionparams={}):
        """
        Get number of meteringdevices in this pod
        
        @param podguid: Pod guid
        @type podguid: guid
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  result as a dictionary of the form {'returncode': True, 'count':{'configured':x, 'userd':x, 'identified':x}}
        @rtype:                   dictionary
        """
    
    def getTree(podguid, depth=2, jobguid=None, executionparams=dict()):
        """
        Returns a json dict with a tree structure.
        
        @param podguid: guid of the pod
        @type podguid: guid
        
        @param depth: depth to return, default 2. 0 means unlimited depth
        @type depth: integer
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and 'result': {'name','type',children = []}
        @rtype:                   dictionary
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


    def getPduHealthStatus(self, guid, timing = [3600, 86400], request=None, jobguid=None, executionparams=dict()):
        """
        getPduHealtStatus, returns a list of 3 values, the first list contains the amount of pdus  which monitoring data is more recent then currenttime-timing[0], the second the  # of pdus  which are last monitored between currenttime - timing[0] and currenttime - timing[1] and the last list contains the amount of pdus which are monitored later then currenttime - timing[1]
        
        E.g:  [200, 5, 2]
        
        Timing contains the time intervals in seconds.(defaults are set on one hour and 1 day)
        
        @params guid: pod guid 
        @type timing: guid
        
        @params timing: timing intervals
        @type timing: list
        
        @return: a dictionary containing this information {'result': {returncode:'True', healthstatus:[],} jobguid:guid}
        @type: dict
        """
