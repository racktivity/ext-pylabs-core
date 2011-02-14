from pymonkey import q

class smartclientbootservice:
    def initialize (self, applicationguid = "", jobguid = "", executionparams = {}):
        """
        
        initialize the smartclientbootservice, can do this as many times as required
        
        FLOW
        #if applicationguid=="": in drp create cloudservice "smartclientbootservice" from template 
        #check if there is already DHCP server
        ##if no dhcpserver yet: create application rootobject dhcpserver in DRP (from template dhcpserver) and attach to pmachine on which ssomanagement vmachine runs
        #change drp: dhdcpserver application object in drp needs smartclientbootservice in DRP as parent
        #call actor dhcpserver.init()
        #create application rootobject apache in DRP (from template apacheserver) and attach to pmachine on which ssomanagement vmachine runs
        #instal/update required qpackages on pmachine underneath mgmt vmachine
        
        @param applicationguid:            Guid of the application which needs to be initialized
        @type  applicationguid:            guid  
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid
        
        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary
        
        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('smartclientbootservice', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def addSmartClient (self, smartclientguid, jobguid = "", executionparams = {}):
        """
        
        Adds a host to the DHCP server (every configuration to do with host is being configured).
        
        FLOW
        # call actor dhcpserver.addHost(... with imagename for pxe boot of smartclient)

        @param smartclientguid:            Guid of the machine to add.
        @type  machineguid:                guid  
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid
        
        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary
        
        @return:                           dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                            dictionary
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['smartclientguid'] = smartclientguid
        return q.workflowengine.actionmanager.startActorAction('smartclientbootservice', 'addSmartClient', params, jobguid=jobguid, executionparams=executionparams)


