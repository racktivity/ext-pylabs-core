from pymonkey import q

class ras:
    def initialize (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Configures the ras service to be ready to use in the cloud.
        
        @param applicationguid:            Guid of the application of which to initialize the RAS service 
        @type applicationguid:             guid
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid
        
        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary
        
        @return:                           dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                            dictionary
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('ras', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def removeTunnel (self, sourcemachineguid, sourceport, destinationmachineguid, destinationport, jobguid = "", executionparams = {}):
        """
        
        Removes a tunnel on the RAS server
        
        @param sourcemachineguid:          Guid of the machine on which to remove the tunnel 
        @type sourcemachineguid:           guid
        
        @param sourceport:                 Source port of the  tunnel 
        @type sourceport:                  int
        
        @param destinationmachineguid:     Guid of the destination machine of the tunnel 
        @type destinationmachineguid:      guid
        
        @param destinationport:            Port number of the destination of the tunnel
        @type destinationport:             int
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid
        
        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary
        
        @return:                           dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                            dictionary
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['sourceport'] = sourceport
        params['destinationmachineguid'] = destinationmachineguid
        params['sourcemachineguid'] = sourcemachineguid
        params['destinationport'] = destinationport
        return q.workflowengine.actionmanager.startActorAction('ras', 'removeTunnel', params, jobguid=jobguid, executionparams=executionparams)

    def connectAgentToTunnel (self, clientagentguid, sessionguid, destinationip, destinationport, protocol = "", jobguid = "", executionparams = {}):
        """
        
        Sends an rscript to the specified agent (or cloud_helper) to setup the tunnel and launch the appropriate client if protocol provided.
        
        @param clientagentguid:            Guid of the agent which want to connect to the tunnel
        @type clientagentguid:             guid
        
        @param sessionguid:                Guid of the tunnel session
        @type sessionguid:                 guid
        
        @param destinationip:              IP address to connect to
        @type destinationip:               string
        
        @param destinationport:            Port number to connect to
        @type destinationport:             int
        
        @param protocol:                   Protocol to use 
        @type protocol:                    string
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid
        
        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary
        
        @return:                           dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                            dictionary
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['sessionguid'] = sessionguid
        params['protocol'] = protocol
        params['clientagentguid'] = clientagentguid
        params['destinationport'] = destinationport
        params['destinationip'] = destinationip
        return q.workflowengine.actionmanager.startActorAction('ras', 'connectAgentToTunnel', params, jobguid=jobguid, executionparams=executionparams)

    def addTunnel (self, sourcemachineguid, sourceport, destinationmachineguid, destinationport, jobguid = "", executionparams = {}):
        """
        
        Confgures a tunnel on the RAS server
        
        @param sourcemachineguid:          Guid of the machine on which to initialize the tunnel 
        @type sourcemachineguid:           guid
        
        @param sourceport:                 Source port of the  tunnel 
        @type sourceport:                  int
        
        @param destinationmachineguid:     Guid of the destination machine of the tunnel 
        @type destinationmachineguid:      guid
        
        @param destinationport:            Port number of the destination of the tunnel
        @type destinationport:             int
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid
        
        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary
        
        @return:                           dictionary with dictionary as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                            dictionary
        
        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['sourceport'] = sourceport
        params['destinationmachineguid'] = destinationmachineguid
        params['sourcemachineguid'] = sourcemachineguid
        params['destinationport'] = destinationport
        return q.workflowengine.actionmanager.startActorAction('ras', 'addTunnel', params, jobguid=jobguid, executionparams=executionparams)


