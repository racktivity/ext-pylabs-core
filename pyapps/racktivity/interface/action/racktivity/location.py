class location():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name, description=None, alias=None, address=None, city=None, country=None, public=False, coordinatesinfo=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Create a new location.
        
        @security administrators
        @param name:                   Name for the location.
        @type name:                    string

        @param description:            Description for the location.
        @type description:             string

        @param alias:                  Alias for the location.
        @type alias:                   string

        @param address:                Address for the location.
        @type address:                 string

        @param city:                   City for the location.
        @type city:                    string

        @param country:                Country for the location.
        @type country:                 string

        @param public:                 Indicates if the location is a public location.
        @type public:                  boolean
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and locationguid as result and jobguid: {'result':{returncode:'True', rackguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, locationguid, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a location.
        
        @security administrators
        @param locationguid:          Guid of the location rootobject to delete.
        @type locationguid:           guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def updateModelProperties(self, locationguid, name=None, description=None, alias=None, address=None, city=None, country=None, coordinatesinfo=None, tags=None, public=False, timezonename=None, timezonedelta=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        
        @security administrators
        @param locationguid:           Guid of the location specified
        @type locationguid:            guid

        @param name:                   Name for the location.
        @type name:                    string

        @param description:            Description for the location.
        @type description:             string

        @param alias:                  Alias for the location.
        @type alias:                   string

        @param address:                Address for the location.
        @type address:                 string

        @param city:                   City for the location.
        @type city:                    string

        @param country:                Country for the location.
        @type country:                 string

        @param public:                 Indicates if the location is a public location.
        @type public:                  boolean

        @param timezonename:           name of timeZone for the location.
        @type timezonename:            string

        @param timezonedelta:          delta of timeZone for the location.
        @type timezonedelta:           float
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and locationguid as result and jobguid: {'result':{returncode:'True', rackguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name=None, description=None, alias=None, address=None, city=None, country=None, public=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of location guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the location.
        @type name:                    string

        @param description:            Description for the location.
        @type description:             string

        @param alias:                  Alias for the location.
        @type alias:                   string

        @param address:                Address for the location.
        @type address:                 string

        @param city:                   City for the location.
        @type city:                    string

        @param country:                Country for the location.
        @type country:                 string

        @param public:                 Indicates if the location is a public location.
        @type public:                  boolean

        @param tags:                   string of tags
        @type tags:                    string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       returncode and Array of location guids(guidlist) which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result':{returncode:True, guidlist: '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, locationguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all locations.

        @execution_method = sync
        
        @param locationguid:            Guid of the location specified
        @type locationguid:             guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with returncode(True) and array of location info(locationinfo) as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised

        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True, locationinfo: [{ 'locationguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'LOCATION0001',
        @note:                                      'description': 'Location 0001',
        @note:                                      'alias': 'LOC-0001',
        @note:                                      'address': 'Antwerpsesteenweg 19',
        @note:                                      'city': 'Lochristi'
        @note:                                      'country': 'Belgium'
        @note:                                      'public': False},
        @note:                                    { 'locationguid': '1351F79F-D65A-4F65-A96B-AC4A6246C033',
        @note:                                      'name': 'LOCATION0001',
        @note:                                      'description': 'Location 0001',
        @note:                                      'alias': 'LOC-0001',
        @note:                                      'address': 'Antwerpsesteenweg 19',
        @note:                                      'city': 'Lochristi'
        @note:                                      'country': 'Belgium'
        @note:                                      'public': False}]}}
        """

    def listDatacenters(self, locationguid, request=None, jobguid=None, executionparams=dict()):
        """
        List all datacenters of the location.
        
        @execution_method = sync
        
        @param locationguid:            Guid of the location rootobject
        @type locationguid:             guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        result is a dictionary of returncode(True) and guidlist of datacenters {return:{returncode:True,guidlist:[]}, jobguid:}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        """
       
    
    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:        Guid of the location rootobject
        @type rootobjectguid:         guid

        @return:                      rootobject
        @rtype:                       string

        @warning:                     Only usable using the python client.
        """
        
    def getAggregatedData(self, locationguid,  meteringtypes, request=None, jobguid=None, executionparams=dict()):
        """
        Get aggregated data from all meteringdevices in the location
        Supported types are: Current, Power, Energy.
        Values are calculated from the latest monitoringinfo objects of the devices in the rack.
        
        @param locationguid: Guid of the location
        @type locationguid: guid
        
        @param meteringtypes: list of meteringtypes e.g curret/power/energy
        @type meteringtypes: list 
        
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
        
        @return:                       result is a dictionary with returncode True and requested values.e.g values:{current:, power:, energy:} and jobguid: {'result': {returncode:True, values:{current:,power:,energy:}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
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
        
        @params guid: location guid 
        @type timing: guid
        
        @params timing: timing intervals
        @type timing: list
        
        @return: a dictionary containing this information {'result': {returncode:'True', healthstatus:[],} jobguid:guid}
        @type: dict
        """
