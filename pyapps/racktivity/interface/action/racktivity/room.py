class room():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name, datacenterguid, floorguid, description=None, alias=None,  tags=None,  request=None, jobguid=None, executionparams=dict()):
        """
        Create a new room.

        
        @security administrators
        @param name:                 Name for the room.
        @type name:                    string
        
        @param datacenterguid:       datacenter to which the room belongs
        @type datacenterguid:        guid

        @param floorguid:            floor guid where the room in located
        @type floorguid:             guid

        @param description:          Description of the room
        @type description:             string

        @param alias:                alias of the room 
        @type alias:                   string
        
        @param tags: string containing a list of tags
        @type tags: tags

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and roomguid as result and jobguid: {'result':{returncode:'True', roomguid:guid}, 'jobguid': guid}}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, roomguid, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a room.

        
        @security administrators
        @param roomguid:              Guid of the room to delete.
        @type roomguid:               guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def updateModelProperties(self, roomguid,name=None, description=None, datacenterguid=None, floorguid=None, alias=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        
        @security administrators
        @param roomguid:               Guid of the room specified
        @type roomguid:                guid

        @param name:                   Name for the room.
        @type name:                    string

        @param description:            Description for the room
        @type description:             string

        @param datacenterguid:         datacenter to which the room belongs
        @type datacenterguid:          guid

        @param  floorguid:             floor location of the room in the datacenter
        @type floorguid:               guid

        @param alias:               alias of the room in the datacenter
        @type alias:                 string
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and roomguid as result and jobguid: {'result':{returncode:'True', roomguid:guid}, 'jobguid': guid}}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name=None,  description=None, datacenterguid=None, floorguid=None, alias=None,  tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of room guids which met the find criteria.

        @execution_method = sync
        
        @security administrators

        @param name:                   Name for the room.
        @type name:                    string

        @param description:            Description for the room.
        @type description:             string

        @param datacenterguid:         datacenter to which the roombelongs
        @type datacenterguid:          guid

        @param  floorguid:             floor location of the room in the datacenter
        @type floorguid:               guid
        
        @param alias:                  alias of the room in the datacenter
        @type alias:                   string
        
        @param tags:                   string of tags
        @type tags:                    string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       returncode (True) and Array of room guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result':{ retruncode:'True, guidlist:["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}


        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, roomguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all rooms.

        @execution_method = sync
        
        @param roomguid:                Guid of the room specified
        @type roomguid:                 guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with returncode and array of room info as result and jobguid: {'result':{returncode:True, roominfo:{}}, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True,roominfo:[{ 'roomguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'room001',
        @note:                                      'description': 'room 0001',,
        @note:                                      'floorguid':"D151F09F-A65A-AF65-A96B-AC4A6F46C033",
        @note:                                      'datacenterguid': '3351FF9F-D65A-4F65-A96B-AC4A6246C033',
                                                    'alias': 'vivaldi'}]}
                                                    
        @raise e:                       In case an error occurred, exception is raised
        """
        
    def getAggregatedData(self, roomguid,  meteringtypes, request=None, jobguid=None, executionparams=dict()):
        """
        Get aggregated data from all meteringdevices in the room
        Supported types are: Current, Power, Energy.
        Values are calculated from the latest monitoringinfo objects of the devices in the rack.
        
        @param roomguid: guid of the room
        @type roomguid: guid
        
        @param meteringtypes: list of meteringtypes e.g curret/power/energy
        @type meteringtypes: list 
        
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       result is a dictionary with returncode True and requested values.e.g values:{current:, power:, energy:} and jobguid: {'result': {returncode:True, values:{current:,power:,energy:}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the room rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        """
        
    def getMeteringdevicesCount(self, roomguid, request=None, jobguid=None,executionparams=dict()):
        """
        Get number of meteringdevices in this room
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       result as a dictionary of the form {'returncode': True, 'count':{'configured':x, 'userd':x, 'identified':x}}
        """
        
    def getViewData(self, rootobjectguid, request=None, jobguid=None, executionparams=dict()):
        """
        Returns view data as a list for this rootobject.
        
        @return: [{viewdatatype:, viewdatavalue:, viewdataunit:},]
        """
    
    def getTree(roomguid, depth=2, jobguid=None, executionparams=dict()):
        """
        Returns a json dict with a tree structure.
        
        @param roomguid: guid of the room
        @type roomguid: guid
        
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
        
        @params guid: room guid 
        @type timing: guid
        
        @params timing: timing intervals
        @type timing: list
        
        @return: a dictionary containing this information {'result': {returncode:'True', healthstatus:[],} jobguid:guid}
        @type: dict
        """
