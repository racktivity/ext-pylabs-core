from pymonkey import q

class lan:
    def listVdcs (self, languid, jobguid = "", executionparams = {}):
        """
        
        List the vdcs the lan is used in.

        @execution_method = sync

        @param languid:                    guid of the lan to list the vdcs for.
        @type languid:                     guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'listVdcs', params, jobguid=jobguid, executionparams=executionparams)

    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync

        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def setFromIpToIp (self, languid, fromip, toip, jobguid = "", executionparams = {}):
        """
        
        Configures the network for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param fromip:                 Network address for the LAN
        @type fromip:                  string

        @param toip:                   Defines if the LAN is used as a management LAN
        @type toip:                    string

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['toip'] = toip
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['fromip'] = fromip
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setFromIpToIp', params, jobguid=jobguid, executionparams=executionparams)

    def setFlags (self, languid, publicflag = False, managementflag = False, storageflag = False, internetpublicflag = False, jobguid = "", executionparams = {}):
        """
        
        Sets the role flags for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param publicflag:             Defines if the LAN is used as a public LAN. Not modified if empty.
        @type publicflag:              boolean

        @param managementflag:         Defines if the LAN is used as a management LAN. Not modified if empty.
        @type managementflag:          boolean

        @param storageflag:            Defines if the LAN is used as a storage LAN. Not modified if empty.
        @type storageflag:             boolean
        
        @param internetpublicflag:     Defines if the LAN is used as a internet public LAN. e.g a public lan with extra security constraints.
        @type internetpublicflag:      boolean

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['managementflag'] = managementflag
        params['storageflag'] = storageflag
        params['publicflag'] = publicflag
        params['internetpublicflag'] = internetpublicflag
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setFlags', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, backplaneguid = "", cloudspaceguid = "", name = "", dns = "", status = "", startip = "", endip = "", gateway = "", managementflag = "", publicflag = "", storageflag = "", network = "", netmask = "", parentlanguid = "", vlantag = "", lantype = "", dhcpflag = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of LAN guids which met the find criteria.

        @execution_method = sync

        @param backplaneguid:           guid of the backplane to include in the search criteria.
        @type backplaneguid:            guid

        @param cloudspaceguid:          guid of the cloudspace to include in the search criteria.
        @type cloudspaceguid:           guid

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

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of lan guids which met the find criteria specified.
        @rtype:                         array

        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['status'] = status
        params['endip'] = endip
        params['publicflag'] = publicflag
        params['name'] = name
        params['startip'] = startip
        params['netmask'] = netmask
        params['cloudspaceguid'] = cloudspaceguid
        params['parentlanguid'] = parentlanguid
        params['network'] = network
        params['storageflag'] = storageflag
        params['lantype'] = lantype
        params['dns'] = dns
        params['managementflag'] = managementflag
        params['dhcpflag'] = dhcpflag
        params['gateway'] = gateway
        params['vlantag'] = vlantag
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def listMacRanges (self, publicflag = "", managementflag = "", jobguid = "", executionparams = {}):
        """
        
        Returns the macranges define on lans

        @execution_method = sync

        @param publicflag:                 Filter on public flag on lan
        @type publicflag:                  boolean
        
        @param managementflag:             Filter on management flag on lan
        @type managementflag:              boolean
                
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           list of dictionary {'guid','name','macrange','publicflag','managementflag'}
        @rtype:                            list

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['managementflag'] = managementflag
        params['publicflag'] = publicflag
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'listMacRanges', params, jobguid=jobguid, executionparams=executionparams)

    def moveToCloudspace (self, languid, spaceguid, jobguid = "", executionparams = {}):
        """
        
        Moves the specified LAN to the another space.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param spaceguid:              guid of the space to move the LAN to
        @type spaceguid:               guid

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['spaceguid'] = spaceguid
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'moveToCloudspace', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, cloudspaceguid, backplaneguid, name, lantype, parentlanguid = "", network = "", netmask = "", fromip = "", toip = "", gateway = "", dns = "", publicflag = False, internetpublicflag = False, managementflag = False, storageflag = False, description = "", integratedflag = False, nrreservedip = -1, jobguid = "", executionparams = {}):
        """
        
        Creates a new lan

        @param cloudspaceguid:         guid of the space this lan is part of
        @type cloudspaceguid:          guid

        @param backplaneguid:          guid of the backplane this lan is part of
        @type backplaneguid:           guid

        @param name:                   Name the lan
        @type name:                    string

        @param lantype:                Type the lan (static of dynamic)
        @type lantype:                 string
        
        @param parentlanguid:          guid of the lan's parent lan
        @type parentlanguid:           guid
        
        @param network:                Network address for the LAN
        @type network:                 string

        @param netmask:                Netmask for the LAN
        @type netmask:                 string
        
        @param fromip:                 Network address for the LAN
        @type fromip:                  string

        @param toip:                   Defines if the LAN is used as a management LAN
        @type toip:                    string
        
        @param gateway:                Address of the default gateway.
        @type gateway:                 string
        
        @param dns:                    Address of the DNS server.
        @type dns:                     string
        
        @param publicflag:             Defines if the LAN is used as a public LAN. Not modified if empty.
        @type publicflag:              boolean
        
        @param internetpublicflag:     Defines if the LAN is used as a internet public LAN. Not modified if empty.
        @type internetpublicflag:      boolean
        
        @param managementflag:         Defines if the LAN is used as a management LAN. Not modified if empty.
        @type managementflag:          boolean
        
        @param storageflag:            Defines if the LAN is used as a storage LAN. Not modified if empty.
        @type storageflag:             boolean
         
        @param description:            Description of the LAN
        @type description:             string
        
        @param integratedflag:         True if the lan is a integrated network or not, default false, because only used for public networks
        @type integratedflag:          boolean
        
        @param nrreservedip:           Number of reserved ip addresses for the sso nodes
        @type  nrreservedip:           integer
        
        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with languid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised

        @note:                         Administrators only
        
	"""
        params =dict()
        params['storageflag'] = storageflag
        params['publicflag'] = publicflag
        params['toip'] = toip
        params['network'] = network
        params['nrreservedip'] = nrreservedip
        params['description'] = description
        params['fromip'] = fromip
        params['lantype'] = lantype
        params['parentlanguid'] = parentlanguid
        params['netmask'] = netmask
        params['integratedflag'] = integratedflag
        params['cloudspaceguid'] = cloudspaceguid
        params['dns'] = dns
        params['managementflag'] = managementflag
        params['backplaneguid'] = backplaneguid
        params['internetpublicflag'] = internetpublicflag
        params['gateway'] = gateway
        params['name'] = name
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def setStatus (self, languid, status, jobguid = "", executionparams = {}):
        """
        
        Configures the status for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param status:                 Status of the LAN ("BROKEN", "ACTIVE", "DISABLED", "NOTCONNECTED)
        @type status:                  string

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['status'] = status
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setStatus', params, jobguid=jobguid, executionparams=executionparams)

    def updateModelProperties (self, languid, name = "", description = "", gateway = "", network = "", netmask = "", startip = "", endip = "", jobguid = "", executionparams = {}):
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

        @param jobguid:                 Guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Dictionary with lan guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['endip'] = endip
        params['network'] = network
        params['startip'] = startip
        params['name'] = name
        params['netmask'] = netmask
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['gateway'] = gateway
        params['description'] = description
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'updateModelProperties', params, jobguid=jobguid, executionparams=executionparams)

    def getNextMacRange (self, jobguid = "", executionparams = {}):
        """
        
        Get the next mac range for a qlan

        @execution_method = sync

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'getNextMacRange', params, jobguid=jobguid, executionparams=executionparams)

    def checkIPRangeInUse (self, startip, endip, jobguid = "", executionparams = {}):
        """
        
        Check if this ip range conflicts with any existing ip range, return true if it conflicts, false otherwise
        
        @param startip:                    Start ip of the range
        @type startip:                     string
        
        @param endip:                      End ip of the range
        @type endip:                       string
                
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           array of the existing lans that conflict with this range ({'result': array, 'jobguid': guid})
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['startip'] = startip
        params['endip'] = endip
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'checkIPRangeInUse', params, jobguid=jobguid, executionparams=executionparams)

    def setLanType (self, languid, lantype, jobguid = "", executionparams = {}):
        """
        
        Configures the LAN type for the specified LAN.

        @param languid:                guid of the lan
        @type languid:                 guid

        @param lantype:                Type of LAN
        @type lantype:                 integer

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['lantype'] = lantype
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setLanType', params, jobguid=jobguid, executionparams=executionparams)

    def setNetworkNetmask (self, languid, network, netmask, jobguid = "", executionparams = {}):
        """
        
        Configures the network for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param network:                Network address for the LAN
        @type network:                 string

        @param netmask:                Netmask for the LAN
        @type netmask:                 string

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['netmask'] = netmask
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['network'] = network
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setNetworkNetmask', params, jobguid=jobguid, executionparams=executionparams)

    def listIPAddresses (self, languid, jobguid = "", executionparams = {}):
        """
        
        List all IP addresses for a lan.

        @execution_method = sync

        @param languid:                    guid of the lan to list the ips for.
        @type languid:                     guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'ipaddress': '10.100.0.1',
        @note:                                          'netmask': '255.255.0.0',
        @note:                                          'guid': '789544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'ispublic': False},
        @note:                                        { 'ipaddress': '10.100.0.5',
        @note:                                          'netmask': '255.255.0.0',
        @note:                                          'guid': '888544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'ispublic': False}]}
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'listIPAddresses', params, jobguid=jobguid, executionparams=executionparams)

    def setDNS (self, languid, dns, jobguid = "", executionparams = {}):
        """
        
        Configures the domain name server for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param dns:                    Address of the DNS server.
        @type dns:                     string

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['dns'] = dns
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setDNS', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, languid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the lan rootobject.

        @execution_method = sync

        @param languid:                guid of the lan rootobject
        @type languid:                 guid

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       XML representation of the lan
        @rtype:                        string

        @raise e:                      In case an error occurred, exception is raised

        @todo:                         Will be implemented in phase2
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def setDefaultGateway (self, languid, gateway, jobguid = "", executionparams = {}):
        """
        
        Configures the default gateway for the specified LAN.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param gateway:                Address of the default gateway.
        @type gateway:                 string

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['gateway'] = gateway
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setDefaultGateway', params, jobguid=jobguid, executionparams=executionparams)

    def getXMLSchema (self, languid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the lan rootobject structure.

        @execution_method = sync

        @param languid:                guid of the lan rootobject
        @type languid:                 guid

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       XSD representation of the disk structure.
        @rtype:                        string

        @raise e:                      In case an error occurred, exception is raised

        @todo:                         Will be implemented in phase2
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def moveToBackplane (self, languid, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Moves the specified LAN to the another backplane.

        @param languid:                guid of the LAN
        @type languid:                 guid

        @param backplaneguid:          guid of the backplane to move the LAN to
        @type backplaneguid:           guid

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised

        @note: Administrator only
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'moveToBackplane', params, jobguid=jobguid, executionparams=executionparams)

    def list (self, cloudspaceguid = "", backplaneguid = "", languid = "", jobguid = "", executionparams = {}):
        """
        
        List all lans.

        @returns array of array [[$lanName,"public" or "private",$nrOfIpAddresses,$nrOfFreeIPAddresses,$description]]


        @execution_method = sync

        @param cloudspaceguid:             guid of the cloud space to list the lans for. If not specified, return all lans you have access to.
        @type cloudspaceguid:              guid

        @param backplaneguid:              guid of the backplane to list the lans for. If not specified, return all lans you have access to.
        @type backplaneguid:               guid

        @param languid:                    guid of the LAN
        @type languid:                     guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of lan info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'cloudspaceguid': '22544B07-4129-47B1-8690-B92C0DB21434',
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
        @note:                                          'management': False}]}
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['cloudspaceguid'] = cloudspaceguid
        params['backplaneguid'] = backplaneguid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'list', params, jobguid=jobguid, executionparams=executionparams)

    def getYAML (self, languid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the lan rootobject.

        @execution_method = sync

        @param languid:                guid of the lan rootobject
        @type languid:                 guid

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       YAML representation of the disk
        @rtype:                        string
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def listFreeIPAddresses (self, languid, jobguid = "", executionparams = {}):
        """
        
        List the free ip addresses for a lan.

        @execution_method = sync

        @param languid:                    guid of the lan to list the ips for.
        @type languid:                     guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with array of ip info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                              'result: [{ 'ipaddress': '10.100.0.1',
        @note:                                          'netmask': '255.255.0.0',
        @note:                                          'guid': '789544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'ispublic': False},
        @note:                                        { 'ipaddress': '10.100.0.5',
        @note:                                          'netmask': '255.255.0.0',
        @note:                                          'guid': '888544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                          'ispublic': False}]}
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('lan', 'listFreeIPAddresses', params, jobguid=jobguid, executionparams=executionparams)

    def setVlanTag (self, languid, vlantag, jobguid = "", executionparams = {}):
        """
        
        Configures the VLAN tag for the specified LAN.

        @param languid:                guid of the lan
        @type languid:                 guid

        @param vlantag:                VLAN tag
        @type vlantag:                 integer

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        params['vlantag'] = vlantag
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'setVlanTag', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, languid, jobguid = "", executionparams = {}):
        """
        
        Deletes s lan.

        @param languid:                guid of the lan to delete
        @type languid:                 guid

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        executionparams['rootobjectguid'] = languid
        executionparams['rootobjecttype'] = 'lan'

        
        return q.workflowengine.actionmanager.startRootobjectAction('lan', 'delete', params, jobguid=jobguid, executionparams=executionparams)


