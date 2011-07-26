class Lan():

    def create(self, backplaneguid, name, lantype, network, netmask, parentlanguid=None, fromip=None, toip=None, gateway=None, dns=[], description=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Creates a new lan

        @param backplaneguid:          guid of the backplane this lan is part of
        @type backplaneguid:           guid

        @param name:                   Name the lan
        @type name:                    string

        @param lantype:                Type the lan (static of dynamic)
        @type lantype:                 string
        
        @param network:                Network address for the LAN
        @type network:                 string

        @param netmask:                Netmask for the LAN
        @type netmask:                 string
        
        @param parentlanguid:          guid of the lan's parent lan
        @type parentlanguid:           guid
              
        @param fromip:                 Network address for the LAN
        @type fromip:                  string

        @param toip:                   Defines if the LAN is used as a management LAN
        @type toip:                    string
        
        @param gateway:                Address of the default gateway.
        @type gateway:                 string
        
        @param dns:                    list of DNS server addresses.
        @type dns:                     list
         
        @param description:            Description of the LAN
        @type description:             string

        @param tags: string of tags
        @type tags: string

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode and languid as result and jobguid: {'result':{returncode:'True', languid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised

        @note:                         Administrators only
        """
#        ...
#        q.actions.rootobject.
#        ...
    def delete(self, languid, request=None, jobguid=None, executionparams=dict()):
        """
        Deletes s lan.

        @param languid:                guid of the lan to delete
        @type languid:                 guid

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setVlanTag(self, languid, vlantag, request=None, jobguid=None, executionparams=dict()):
        """
        Configures the VLAN tag for the specified LAN.

        @param languid:                guid of the lan
        @type languid:                 guid

        @param vlantag:                VLAN tag
        @type vlantag:                 integer

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setLanType(self, languid, lantype, request=None, jobguid=None, executionparams=dict()):
        """
        Configures the LAN type for the specified LAN.

        @param languid:                guid of the lan
        @type languid:                 guid

        @param lantype:                Type of LAN
        @type lantype:                 integer

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setFlags(self, languid, publicflag=False, managementflag=False, storageflag=False, request=None, jobguid=None, executionparams=dict()):
        """
        Sets the role flags for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param publicflag:             Defines if the LAN is used as a public LAN. Not modified if empty.
        @type publicflag:              boolean

        @param publicflag:             Defines if the LAN is used as a public LAN. Not modified if empty.
        @type publicflag:              boolean

        @param managementflag:         Defines if the LAN is used as a management LAN. Not modified if empty.
        @type managementflag:          boolean

        @param storageflag:            Defines if the LAN is used as a storage LAN. Not modified if empty.
        @type storageflag:             boolean

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setNetworkNetmask(self, languid, network, netmask, request=None, jobguid=None, executionparams=dict()):
        """
        Configures the network for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param network:                Network address for the LAN
        @type network:                 string

        @param netmask:                Netmask for the LAN
        @type netmask:                 string

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setFromIpToIp(self, languid, fromip, toip, request=None, jobguid=None, executionparams=dict()):
        """
        Configures the network for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param fromip:                 Network address for the LAN
        @type fromip:                  string

        @param toip:                   Defines if the LAN is used as a management LAN
        @type toip:                    string

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setStatus(self, languid, status, request=None, jobguid=None, executionparams=dict()):
        """
        Configures the status for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param status:                 Status of the LAN ("BROKEN", "ACTIVE", "DISABLED", "NOTCONNECTED)
        @type status:                  string

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setDefaultGateway(self, languid, gateway, request=None, jobguid=None, executionparams=dict()):
        """
        Configures the default gateway for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param gateway:                Address of the default gateway.
        @type gateway:                 string

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def setDNS(self, languid, dns, request=None, jobguid=None, executionparams=dict()):
        """
        Configures the domain name server for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param dns:                    List of the DNS server addresses.
        @type dns:                     list

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def moveToBackplane(self, languid, backplaneguid, request=None, jobguid=None, executionparams=dict()):
        """
        Moves the specified LAN to the another backplane.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param backplaneguid:          guid of the backplane to move the LAN to
        @type backplaneguid:           guid

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                      dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised

        @note: Administrator only
        """

    

    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync

        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        """

   
    def updateModelProperties(self, languid, name=None, description=None, gateway=None, network=None, netmask=None, startip=None, endip=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update basic properties

        @param languid:                 Guid of the LAN to update.
        @type languid:                  guid

        @param name:                    Name of the lan.
        @type name:                     string

        @param description:             Description of the lan.
        @type description:              string

        @param gateway:                 Gateway of the lan.
        @type gateway:                  string

        @param network:                 Network of the lan.
        @type network:                  string

        @param netmask:                 Netmask of the lan.
        @type netmask:                  string

        @param startip:                 Startip of the lans to include in the search criteria.
        @type startip:                  string

        @param endip:                   Endip of the lans to include in the search criteria.
        @type endip:                    string

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with returncode and languid as result and jobguid: {'result':{returncode:'True', languid:guid}, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        """

    def find(self, backplaneguid=None, name=None, dns=None, status=None, startip=None, endip=None, gateway=None, managementflag=None, publicflag=None, storageflag=None, \
             network=None, netmask=None, parentlanguid=None, vlantag=None, lantype=None, dhcpflag=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of LAN guids which met the find criteria.

        @execution_method = sync

        @param backplaneguid:           guid of the backplane to include in the search criteria.
        @type backplaneguid:            guid

        @param parentlanguid:           guid of the parent lan to include in the search criteria.
        @type parentlanguid:            guid

        @param name:                    Name of the lans to include in the search criteria.
        @type name:                     string

        @param dns:                     DNS of the lans to include in the search criteria.
        @type dns:                      string

        @param status:                  Status of the lans to include in the search criteria. See listStatuses().
        @type status:                   string

        @param startip:                 startip of the lans to include in the search criteria.
        @type startip:                  string

        @param endip:                   endip of the lans to include in the search criteria.
        @type endip:                    string

        @param gateway:                 gateway of the lans to include in the search criteria.
        @type gateway:                  string

        @param managementflag:          managementflag of the lans to include in the search criteria.
        @type managementflag:           boolean

        @param publicflag:              publicflag of the lans to include in the search criteria.
        @type publicflag:               boolean

        @param storageflag:             storageflag of the lans to include in the search criteria.
        @type storageflag:              boolean

        @param network:                 network of the lans to include in the search criteria.
        @type network:                  string

        @param netmask:                 netmask of the lans to include in the search criteria.
        @type netmask:                  string

        @param vlantag:                 vlan tag of the lans to include in the search criteria.
        @type vlantag:                  int

        @param lantype:                 Type the lan (static of dynamic)
        @type lantype:                  string

        @param tags:                    string of tags
        @type tags:                     string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        returncode (True) and Array of lan guids(guidlist) which met the find criteria specified.
        @rtype:                         array

        @note:                          Example return value:
        @note:                          {'result': {returncode:True, guidlist:'["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        """

    def list(self, backplaneguid=None, languid=None, request=None, jobguid=None, executionparams=dict()):
        """
        List all lans.

        @returns array of array [[$lanName,"public" or "private",$nrOfIpAddresses,$nrOfFreeIPAddresses,$description]]


        @execution_method = sync

        @param backplaneguid:              guid of the backplane to list the lans for. If not specified, return all lans you have access to.
        @type backplaneguid:               guid

        @param languid:                    guid of the LAN
        @type languid:                     guid

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with returncode(True) and array of lan info(laninfo) as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: {returncode:True, laninfo:[{ 'cloudspaceguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'backplaneguid': '55544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'languid': '75544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'parentlanguid': '45544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'Office Lan',
        @note:                                          'description': 'Our Office Lan',
        @note:                                          'lantype': 'STATIC',
        @note:                                          'public': False,
        @note:                                          'storage': False,
        @note:                                          'management': False},
        @note:                                        { 'cloudspaceguid': '789544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'backplaneguid': '78644B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'languid': '78644B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'parentlanguid': '74844B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'name': 'Internet Feed',
        @note:                                          'description': 'Our Public Lan',
        @note:                                          'lantype': 'DYNAMIC',
        @note:                                          'public': True,
        @note:                                          'storage': False,
        @note:                                          'management': False}]}}
        
        @raise e:                          In case an error occurred, exception is raised
        """

    def listIPAddresses(self, languid, request=None, jobguid=None, executionparams=dict()):
        """
        List all IP addresses for a lan.

        @execution_method = sync

        @param languid:                    guid of the lan to list the ips for.
        @type languid:                     guid

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with returncode and array of ip info(ipinfo) as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: {returncode:True, ipinfo:[{ 'ipaddress': '10.100.0.1',
        @note:                                          'netmask': '255.255.0.0',
        @note:                                          'guid': '789544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'ispublic': False},
        @note:                                        { 'ipaddress': '10.100.0.5',
        @note:                                          'netmask': '255.255.0.0',
        @note:                                          'guid': '888544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'ispublic': False}]}}
        
        @raise e:                          In case an error occurred, exception is raised
        """

    
    def getNextMacRange(self, request=None, jobguid=None,executionparams=dict()):
        """
        Get the next mac range for a qlan

        @execution_method = sync

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with retruncode and macrange as result and jobguid: {'result': {returncode:True, macrange:}, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
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