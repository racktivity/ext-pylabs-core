class ipaddress():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """

    def create(self, name, address, description="", netmask = "",block = False,iptype="", ipversion = "", languid = "" ,virtual = False, tags="", request = "", jobguid = "", executionparams=dict()):
    
        """
        Create a new ipaddress.

        @security administrators

        @param name:              name of the ipaddress
        @type name:               string
        
        @param  address:          IP address of the IP
        @type address:            type_ipaddress

        @param  description:      description of the object
        @type description:        string

        @param  netmask:          netmask of the IP object
        @type netmask:            type_netmaskaddress

        @param  block:            flag indicating if the IP is blocked
        @type block:              boolean

        @param  iptype:           type of the IP object, STATIC or DHCP
        @type iptype:             string

        @param ipversion:         version of the IP object, IPV4 or IPV6
        @type ipversion:          string
        @param languid:           lan to which the ip is connected
        @type languid:            guid

        @param virtual            flag is if ip is a VIPA
        @type virtual             boolean 
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode and ipaddressguid as result and jobguid: {'result':{returncode:'True', ipaddressguid:guid}, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        """

    def delete(self, ipaddressguid, request="", jobguid="", executionparams=dict()):
        """
        Delete a ipaddress.

        @security administrators

        @param ipaddressguid:         Guid of the ipaddress rootobject to delete.
        @type ipaddressguid:          guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """

    def updateModelProperties(self, ipaddressguid, name="",description="",address="",netmask="",block = False,iptype="",ipversion="", virtual=None, languid="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @security administrators

        @param ipaddressguid:          Guid of the ipaddress specified
        @type ipaddressguid:           guid

        @param name:                   name of the ipaddress
        @type name:                    string

        @param  description:           description of the object
        @type description:             string

        @param  address:               IP address of the IP
        @type address:                 type_ipaddress

        @param  netmask:               netmask of the IP object
        @type netmask:                 type_netmaskaddress

        @param  block:                 flag indicating if the IP is blocked
        @type block:                   boolean

        @param  iptype:                type of the IP object, STATIC or DHCP
        @type iptype:                  string

        @param ipversion:              version of the IP object, IPV4 or IPV6
        @type ipversion:               string

        @param languid:                lan to which the ip is connected
        @type languid:                 guid
        
        @param virtual                 flags whether ipaddress is a VIPA
        @type virtual                  boolean 

        @param tags: string of tags
        @type tags: string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and ipaddressguid as result and jobguid: {'result':{returncode:'True', ipaddressguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name="", description="", address="", netmask="",block = False, iptype="", ipversion="", languid="", cloudspaceguid="", virtual=None, tags="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of ipaddress guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        
        @param name:                    name of the ipaddress
        @type name:                     string

        @param description:             description of the object
        @type description:              string

        @param address:                 IP address of the IP object
        @type address:                  type_ipaddress

        @param netmask:                 netmask of the IP object
        @type netmask:                  type_netmaskaddress

        @param block:                   flag indicating if the IP is blocked
        @type block:                    boolean

        @param iptype:                  type of the IP object, STATIC or DHCP
        @type iptype:                   string

        @param ipversion:               version of the IP object, IPV4 or IPV6
        @type ipversion:                string

        @param languid:                 lan to which the ip is connected
        @type languid:                  guid

        @param cloudspaceguid:          cloudspaceguid to which the ip is connected
        @type cloudspaceguid:           guid
        
        @param virtual                  flag whether to include VIPA
        @type virtual                   boolean 

        @param tags:                    string of tags
        @type tags:                     string

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        result is a dict of a returntype(True) and a Array of ipaddress guids(guidlist) which met the find criteria specified.
        @rtype:                         array

        @note:                          Example return value:
        @note:                          {'result':{returntype:True, guidlist: '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]}',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        """

    def list(self, ipaddressguid="", request="", jobguid="", executionparams=dict()):
        """
        List all ipaddresss.

        @execution_method = sync
        
        @param ipaddressguid:           Guid of the ipaddress rootobject
        @type ipaddressguid:            guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        result is dict with returncode(true) and dictionary with array of ipaddress info(ipaddressinfo) as result and jobguid
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised

        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returncode:True, ipaddressinfo: [{ 'ipaddressguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'ipaddress0001',
        @note:                                      'description': 'ipaddress 0001',
        @note:                                      'address': '192.148.0.1',
        @note:                                      'netmask': '255.255.255.255',
        @note:                                      'block': '',
        @note:                                      'iptype': 'STATIC',
        @note:                                      'ipversion':'IPV4',
        @note:                                      'languid': '77544B07-4129-47B1-8690-B92C0DB2143'}]}}
        """
        
    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:        Guid of the ipaddress rootobject
        @type rootobjectguid:         guid

        @return:                      rootobject
        @rtype:                       string

        @warning:                     Only usable using the python client.
        """

  

    def setState(self, ipaddressguid, status, request="", jobguid="", executionparams=dict()):
        """
        Sets the state of the ip address
        
        @param ipaddressguid:           Guid of the ipaddress rootobject
        @type ipaddressguid:            guid
        
        @param status:                  status of the ipaddress
        @type status:                   string

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised        
        
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