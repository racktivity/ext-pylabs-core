class autodiscoverysnmpmap():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, manufacturer, sysobjectid, oidmapping, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Create a new autodiscovery snmp map
        
        @param manufacturer:           manufacturer for this mapping
        @type manufacturer:            string
        
        @param sysobjectid:           the value returned when calling oid "1.3.6.1.2.1.1.2" 
        @type sysobjectidr:           string
        
        @param oidmapping:        mapping from certain types to oids
        @type dict:               oidmapping
          
        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode and cableguid as result and jobguid: {'result':{returncode:'True', autodiscoverysnmpmapguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def delete(self, autodiscoverysnmpmapguid, request="", jobguid="", executionparams=dict()):
        """
        Delete a autodiscoverysnmpmap
        
        @security administrators
        @param autodiscoverysnmpmapguid:             Guid of the autodiscoverysnmpmap rootobject to delete.
        @type autodiscoverysnmpmapguid:              guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
        
    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
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
        
    def updateModelProperties(self, autodiscoverysnmpmapguid, manufacturer=None, sysobjectid=None, oidmapping=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)
   
        @param autodiscoverymapguid:              Guid of the autodiscovery map specified
        @type autodiscoverymapguid:               guid

        @param manufacturer:           manufacturer for this mapping
        @type manufacturer:            string
        
        @param sysobjectid:           the value returned when calling oid "1.3.6.1.2.1.1.2" 
        @type sysobjectidr:           string
        
        @param oidmapping:        mapping from certain types to oids
        @type oidmapping:               dict

        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and autodiscoverymapguids as result and jobguid: {'result':{returncode:'True', autodiscoverymapguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, manufacturer=None, sysobjectid=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of autodiscoverymapguids  which met the find criteria.
        
        @param manufacturer:                   Name for the autodiscoverymapguid.
        @type manufacturer:                    string

        @param sysobjectid:           the value returned when calling oid "1.3.6.1.2.1.1.2" 
        @type sysobjectidr:           string

        @param tags:                   string of tags
        @type tags:                    string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Result is a dict containing, returncode(True) and Array(guidlist) of cable guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, autodiscoverysnmpmapguid=None, manufacturer=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all cables.

        @param autodiscoverymapguid:              Guid of the autodiscovery map specified
        @type autodiscoverymapguid:               guid

        @param manufacturer:                   Name for the autodiscoverymapguid
        @type manufacturer:                    string

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of autodiscoverymap info as result and jobguid: {'result': {returncode:True, autodiscoverymapinfo:[], 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True, autodiscoverymapinfo: [{ 'autodisoverymapguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'manufacturer': 'avocent',
        @note:                                      'oidmapping': {} ]}}
        
        @raise e:                       In case an error occurred, exception is raised
        """
