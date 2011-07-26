class feed():
    def create(self, name, feedproductiontype, datacenterguid=None, co2emission=None, feedconnectors=list(), description=None,tags=None ,request=None, jobguid=None, executionparams=dict()):
        """
        Create a new feed.

        @param name:                   Name for the feed.
        @type name:                    string
        
        @param feedproductiontype:     type of production for the feed 
        @type feedproductiontype:      feedProductionType

        @param datacenterguid:         guid of the datacenter to which the feed is linked
        @type datacenterguid:          guid
        
        @param co2emission:            The co2 emission of the feed, None to use the default for this feed production type.
        @type co2emission:             float
        
        @param feedconnectors:         list of feedconnector information
        @type  feedconnectors:         list

        @param description:            description of the feed
        @type description:             string
      
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode and feedguid as result and jobguid: {'result':{returncode:'True', feed:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, feedguid, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a feed.
        
        @security administrators
        @param feedguid:             Guid of the feed rootobject to delete.
        @type feedguid:              guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid


        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
    def addConnector(self, feedguid, name, sequence, status, request=None, jobguid=None, executionparams=dict()):
        """
        Add a feed connector to the feed
        
        @param feedguid:         The feed guid
        @type feedguid:          The GUID of the feed
        
        @param name:             Name of the connector
        @type  name:             str
        
        @param sequence:         Sequence of the connector
        @type  sequence:         int
        
        @param status:           Status of the connector
        @type  status:           feedConnectorStatustType
        
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
    
    def deleteConnector(self, feedguid, name, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a feed connector from the feed
        
        @param feedguid:         The feed guid
        @type feedguid:          The GUID of the feed
        
        
        @param name:             Name of the connector to delete
        @type  name:             str
        
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
    
    def connectConnector(self, feedguid, name, cableguid, request=None, jobguid=None, executionparams=dict()):
        """
        Connect a feed connector to a cable
        
        @param feedguid:         The feed guid
        @type feedguid:          The GUID of the feed
        
        
        @param name:             Name of the connector to delete
        @type  name:             str
        
        @param cableguid:        GUID of the cable to connect to
        @type  cableguid:             GUID
        
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
    
    def updateModelProperties(self, feedguid, name=None, datacenterguid=None, co2emission=None, feedproductiontype=None, description=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        
        @param feedguid:               Guid of the feed to change
        @type feedguid:                Type of the feed

        @param name:                   Name for the feed.
        @type name:                    string

        @param datacenterguid:         guid of the datacenter to which the feed is linked
        @type datacenterguid:          guid
        
        @param co2emission:            The co2 emission of the feed
        @type co2emission:             float
        
        @param feedproductiontype:     type of production for the feed 
        @type feedproductiontype:      feedProductionType

        @param feedconnectors:         list of feedconnector information
        @type  feedconnectors:         list

        @param description:            description of the feed
        @type description:             string
      
        @param tags:                   string of tags
        @type tags:                    string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and feedguid as result and jobguid: {'result':{returncode:'True', feedguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name=None, datacenterguid=None, feedproductiontype=None, cableguid=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of feed guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the feed.
        @type name:                    string

        @param datacenterguid:         find on datacenterguid
        @type description:             string

        @param feedproductiontype:     find on productiontype
        @type feedproductiontype:       feedProductiontype
        
        @param cableguid:             A cable guid 
        @type cableguid:              GUID

        @param tags:                  tags attached to feed
        @type tags:                   string(60)

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Result is a dict containing, returncode(True) and Array(guidlist) of feed guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, feedguid=None, datacenterguid=None, feedproductiontype=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all feeds.

        @execution_method = sync

        @param feedguid:               
        
        @param name:                   Name for the feed.
        @type name:                    string

        @param datacenterguid:         find on datacenterguid
        @type description:             string

        @param feedproductiontype:     find on productiontype
        @type feedproductiontype:       feedProductiontype

        @param tags:                  tags attached to feed
        @type tags:                   string(60)

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of feed info as result and jobguid: {'result': {returncode:True, feedinfo:[], 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True, feedinfo: [{ 'feedguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'feed0001',
        @note:                                      'description': 'feed 0001',
        @note:                                      'feedproductiontype': 'GAS'
        @note:                                      'datacenterguid': '22544B07-4129-47B1-8690-B92C0DB21434'
        @note:                                      'tags': 'gas, producer:electrabel'}]}}
        
        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the feed rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
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