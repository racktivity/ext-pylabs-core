class Floor():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """
    def create(self, name, floor, datacenterguid, alias=None, description=None, tags=None,  request=None, jobguid=None, executionparams=dict()):
        """
        Create a floor in a datacenter with a list of racks
        
        @params name: name of the floor
        @type name: string
        
        @params floor: floornumber
        @type floor: integer
        
        @params datacenterguid: in which the datacenter is located
        @type datacenterguid: guid
        
        @params alias: alias of the floor
        @type alias: string
        
        @params description: of the floor
        @type    description: string
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and guid, jobguid: {'result': {'returncode':True, guid:}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def delete(self, floorguid, request=None, jobguid=None, executionparams=dict()):
        """
        Deletes a floor
        
        @params floorguid: guid of the floor to delete
        @type version: guid
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def updateModelProperties(self, floorguid, name=None, floor=None, datacenterguid=None, alias=None, description=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update model properties for a floor with guid(floorguid)

        @params floorguid: guid of the floor
        @type floorguid: string
        
        @params name: name of the floor
        @type name: string
        
        @params floor: floornumber
        @type floor: integer
        
        @params datacenterguid: in which the datacenter is located
        @type datacenterguid: guid
        
        @params alias: alias name of the floor
        @type alias: string
        
        @params description: description of the floor
        @type description: string
        
        @params racks: list of rack guids located in the floor
        @type: list      
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
    def getAggregatedData(self, floorguid, meteringtypes,  request=None, jobguid='', executionparams={}):
        """
        Get aggregated data from all rooms in the floor
        Supported types are: Current, Power, Energy.
        Values are calculated from the latest monitoringinfo objects of the devices in the room.
        
        @param floorguid:         guid of the room
        @type floorguid:          guid
        
        @param meteringtypes:     list of meteringtypes e.g curret/power/energy
        @type meteringtypes:      list or string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  result is a dictionary with returncode True and requested values.e.g values:{current:, power:, energy:} and jobguid: {'result': {returncode:True, values:{current:,power:,energy:}, 'jobguid': guid}
        @rtype: dictionay
        """
        
    def getMeteringdevicesCount(self, floorguid, jobguid='', executionparams={}):
        """
        Get number of meteringdevices in this floor
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  result as a dictionary of the form {'returncode': True, 'count':{'configured':x, 'userd':x, 'identified':x}}
        @rtype:                   dictionary
        """
        
    def getViewData(self, floorguid, jobguid='', executionparams={}):
        """
        Returns view data as a list for this rootobject.
        
        @param floorguid: Floor guid
        @type floorguid:  guid
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return: [{viewdatatype:, viewdatavalue:, viewdataunit:},]
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
        
    def find(self, name=None,datacenterguid=None, floor=None, alias=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        @execution_method = sync
        
        @param name: name of the floors to find
        @type name: string
        
        @params datacenterguid: in which the datacenter is located
        @type datacenterguid: guid
        
        @params floor: floornumber
        @type floor: integer
        
        @param alias: alias name of the floor to find
        @type alias: string
        
        @param tags:             string of tags
        @type tags:              string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and floor guids  as result and jobguid: {'result': {'returncode':True,'guidlist':[]}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def list(self, floorguid=None, datacenterguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        @execution_method = sync
        
        List found floors and return floor information
        
        @param floorguid: guid of the floor to list
        @type floorguid: guid
        
        @param jobguid:           Guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and floor information  as result and jobguid: {'result': {'returncode':True,'floorinformation:{}}, 'jobguid': guid}
        a floor informatin contains the following info:
        {floorguid:{name:, alias, description:, datacenter: ,racks:, tags:,,}}
        @rtype:                   dictionary
        """
    
    def getTree(floorguid, depth=2, jobguid=None, executionparams=dict()):
        """
        Returns a json dict with a tree structure.
        
        @param floorguid: guid of the floor
        @type floorguid: guid
        
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
        
        @params guid: floor guid 
        @type timing: guid
        
        @params timing: timing intervals
        @type timing: list
        
        @return: a dictionary containing this information {'result': {returncode:'True', healthstatus:[],} jobguid:guid}
        @type: dict
        """
