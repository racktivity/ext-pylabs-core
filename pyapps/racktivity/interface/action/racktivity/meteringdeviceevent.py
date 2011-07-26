class Meteringdeviceevent():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """
    def create(self, eventtype=None, timestamp=None, level=None, meteringdeviceguid=None, portsequence=None, sensorsequence=None, thresholdguid=None, tags=None, errmessagepublic=None, errmessageprivate=None,logs=None, request=None, jobguid=None, executionparams=dict()):
        """
        @param eventtype: custom type of the event
        @type eventtype: string
        
        @param timestamp: timestamp when the event has occured
        @type timestamp: string
        
        @param level: level of the meteringdeviceeventlevel
        @type level: meteringdeviceeventlevel
        
        @param meteringdeviceguid: guid of the meteringdeviceguid
        @type meteringdeviceguid: guid
        
        @param portsequence: sequence of the port on which the event has occured
        @type portsequence: integer
        
        @param sensorsequence: sequence of the sensor on which the event has occured
        @type sensorsequence: integer
        
        @param thresholdguid: guid of the related threshold
        @type thresholdguid: guid
        
        @param tags: string of tags
        @type tags: string
        
        @param errmsgpublic: public errormsg which can be showed to the user
        @type errmsgpublic: string
        
        @param  errmessagprivate: private message used for the internal system
        @type  errmessagprivate: string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and guid, jobguid: {'result': {'returncode':True, guid:}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def delete(self, meteringdeviceeventguid, request=None, jobguid=None, executionparams=dict()):
        """
        Deletes a racktivity meteringdeviceevent
        
        @params meteringdeviceeventguid: guid of the meteringdeviceevent to delete
        @type version: guid
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
    
    def find(self, meteringdeviceguid=None, portsequence=None, sensorsequence=None, eventtype=None, level=None, thresholdguid=None, latest=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Find and return a list of found meteringdeviceevent guids based on search parameters
        
        @param eventtype: custom type of the event
        @type eventtype: string
                    
        @param level: level of the meteringdeviceeventlevel
        @type level: meteringdeviceeventlevel
        
        @param meteringdeviceguid: guid of the meteringdeviceguid
        @type meteringdeviceguid: guid
        
        @param portsequence: sequence of the port on which the event has occured
        @type portsequence: integer
        
        @param sensorsequence: sequence of the sensor on which the event has occured
        @type sensorsequence: integer
        
        @param thresholdguid: guid of the related threshold
        @type thresholdguid: guid
        
        @param latest: return the latest x values according to the test parameters
        @type latest: integer
        
        @param tags:             string of tags
        @type tags:              string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and meteringdeviceevent guid  as result and jobguid: {'result': {'returncode':True,'guidlist':[]}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def list(self, meteringdeviceguid=None, portsequence=None, sensorsequence=None, eventtype=None, level=None, thresholdguid=None, latest=None,  request=None, jobguid=None, executionparams=dict()):
        """
        List found meteringdeviceevent information based on search parameters
        
        @param eventtype: custom type of the event
        @type eventtype: string
                    
        @param level: level of the meteringdeviceeventlevel
        @type level: meteringdeviceeventlevel
        
        @param meteringdeviceguid: guid of the meteringdeviceguid
        @type meteringdeviceguid: guid
        
        @param portsequence: sequence of the port on which the event has occured
        @type portsequence: integer
        
        @param sensorsequence: sequence of the sensor on which the event has occured
        @type sensorsequence: integer
        
        @param thresholdguid: guid of the related threshold
        @type thresholdguid: guid
        
        @param latest: return the latest x values according to the test parameters
        @type latest: integer
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and racktivitydeviceevent information  as result and jobguid: {'result': {'returncode':True,'racktivitydeviceeventinformation':{}}, 'jobguid': guid}
        a meteringdeviceevent informatin contains the following info:
        {meteringdeviceevenguid:{eventype:, level:, meteringdeviceguid:, portsequence, sensorsequence:, thresholdguid:,}}
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
        
    def listLatest(self, limit=10, datacenterguid=None, floorguid=None, roomguid=None, podguid=None, rowguid=None, rackguid=None, meteringdeviceguid=None, portsequence=None, sensorsequence=None, eventtype=None, level=None, thresholdguid=None, latest=None,  request=None, jobguid=None, executionparams=dict()):
       """
        List found latest specific number of meteringdeviceevent (in order) information based on search parameters

        @execution_method = sync

        @param limit: Number of last events to retrieve
        @type: integer
        
        @param datacenterguid: guid of the datacenter
        @type datacenterguid: guid
        
        @param floorguid: guid of the floor
        @type floorguid: guid
        
        @param roomguid: guid of the room
        @type roomguid: guid
        
        @param podguid: guid of the pod
        @type podguid: guid
        
        @param rowguid: guid of the row
        @type rowguid: guid
        
        @param rackguid: guid of the rack
        @type rackguid: guid

        @param meteringdeviceguid: guid of the meteringdevice
        @type meteringdeviceguid: guid
        
        @param portsequence: sequence of the port on which the event has occured
        @type portsequence: integer
           
        @param sensorsequence: sequence of the sensor on which the event has occured
        @type sensorsequence: integer     

        @param thresholdguid: guid of the related threshold
        @type thresholdguid: guid

        @param latest: return the latest x values according to the test parameters
        @type latest: integer

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and racktivitydeviceevent information  as result and jobguid: {'result': {'returncode':True,'racktivitydeviceeventinformation':{}}, 'jobguid': guid}
        a meteringdeviceevent informatin contains the following info: {meteringdeviceevenguid:{eventype:, level:, meteringdeviceguid:, portsequence, sensorsequence:, thresholdguid:,}}
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