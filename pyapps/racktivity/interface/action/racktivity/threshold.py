class threshold():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, thresholdtype,  minimum, maximum,  thresholdimpacttype, clouduserguid="", tags="",  request="", jobguid="", executionparams=dict()):
        """
        Create a new threshold.

        @execution_method = sync
        
        @security administrators
        
        @param thresholdtype:                 Type of the threshold.
        @type thresholdtype:                    thresholdtype

        @param minimum:         Integer
        @type minimum:             Integer

        @param maximum:       Integer
        @type maximum:          Integer

        @param thresholdimpacttype:      Impact  when maximum/minimum of the threshold is reached
        @type thresholdimpacttype:         thresholdimpacttype
        
        @param clouduserguid:                guid of the user who set this threshold
        @type alias:                   guid
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and rackguid as result and jobguid: {'result':{returncode:'True', thresholdguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, thresholdguid, request="", jobguid="", executionparams=dict()):
        """
        Delete a threshold.

        @execution_method = sync
        
        @security administrators
        @param thresholdguid:              Guid of the room to delete.
        @type thresholdguid:               guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}                              
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def updateModelProperties(self, thresholdguid, thresholdtype,  minimum, maximum,  thresholdimpacttype, clouduserguid="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @security administrators
        
        @param thresholdtype:                 Type of the threshold.
        @type thresholdtype:                    thresholdtype

        @param minimum:          Minimum value of the threshold, if maximum is 0, only minimum is used
        @type minimum:             Integer

        @param maximum:       Maximum value of the threshold, if minimum is 0, only maximum is used
        @type maximum:          Integer

        @param thresholdimpacttype:      Impact  when maximum/minimum of the threshold is reached
        @type thresholdimpacttype:         thresholdimpacttype
        
        @param clouduserguid:                guid of the user who updated this threshold
        @type alias:                   guid
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with return code and rack guid as result and jobguid: {'result': {returncode:True, thresholdguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self,  thresholdtype="", thresholdimpacttype="" ,request="", jobguid="", executionparams=dict()):
        """
        Returns a list of room guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        
        @param thresholdtype:     Type of the threshold 
        @type thresholdtype:    thresholdtype
        
        @param thresholdimpacttype: Type of impacttype 
        @type thresholdimpacttype:  thresholdimpacttype

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       returncode (True) and Array of thresholdguids guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result':{ retruncode:'True, guidlist:["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, thresholdguid="", thresholdtype="",  thresholdimpacttype="",  request="", jobguid="", executionparams=dict()):
        """
        List all thresholds.

        @execution_method = sync
        
        @param thresholdguid:         Guid of the threshold specified
        @type thresholdguid:                 guid
        
        @param thresholdtype:     Type of the threshold 
        @type thresholdtype:    thresholdtype
        
        @param thresholdimpacttype: Type of impacttype 
        @type thresholdimpacttype:  thresholdimpacttype

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with returncode and array of room info as result and jobguid: {'result':{returncode:True, thresholdinfo:{}}, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True, thresholdinfo:[{ 'thresholdguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'thresholdtype': VOLTAGE,
        @note:                                      'minimum': 0,
        @note:                                      'maximum': 250,
        @note:                                      'thresholdimpacttype': WARNING,
                                                    }]'
                                                    
        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the threshold rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
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