from pymonkey import q

class agent:
    def unregisterFromNOC (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Unregisters agents and removes keep alive job 
        
        @param machineguid:               Guid of the pmachine
        @type machineguid:                guid
        
        @param jobguid:                   Guid of the job
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                           dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('agent', 'unregisterFromNOC', params, jobguid=jobguid, executionparams=executionparams)

    def register (self, macaddress, jobguid = "", executionparams = {}):
        """
        
        Register agent for machine with given macaddress
        generate login and password for agent
        register agent in ejabberd
      
        @param macaddress:                macaddress of the machine to register an agent for
        @type macaddress:                 string

        @param jobguid:                   Guid of the job
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          dictionary with agentconfig as result 
                                          and jobguid {'result':{'agentcontrollerguid': '00000000-a8ad-46a1-966f-39565101d763',
                                                                 'agentguid': 'd7ef38bb-660d-4f72-a60e-9d4c589ff6c2',
                                                                 'password': '6ab8f121-27bc-4458-902b-33f75bbacac7',
                                                                 'xmppserver': 'dmachine.office.aserver.com'}, 
                                                       'jobguid':guid}
        @rtype:                           dictionary
        
	"""
        params =dict()
        params['macaddress'] = macaddress
        return q.workflowengine.actionmanager.startActorAction('agent', 'register', params, jobguid=jobguid, executionparams=executionparams)

    def test (self, agentguid, jobguid = "", executionparams = {}):
        """
        
        Tests the agent specified
        
        @param agentguid:                 Guid of the agent
        @type agentguid:                  guid

        @param jobguid:                   Guid of the job
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                           dictionary
        
	"""
        params =dict()
        params['agentguid'] = agentguid
        return q.workflowengine.actionmanager.startActorAction('agent', 'test', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, machineguid = "", jobguid = "", executionparams = {}):
        """
        
        Initializes the agent specified
        e.g. installing the agent on the related machine
        
        @param machineguid:               Guid of the machine
        @type machineguid:                guid

        @param jobguid:                   Guid of the job
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                           dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('agent', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def registerToNOC (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Registers agents and configures keep alive job 
        
        @param machineguid:                Guid of the pmachine
        @type machineguid:                 guid
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('agent', 'registerToNOC', params, jobguid=jobguid, executionparams=executionparams)

    def restart (self, agentguid, ipaddress, jobguid = "", executionparams = {}):
        """
        
        Restarts the agent 
        
        @param agentguid:                 Guid of the agent
        @type agentguid:                  guid
        
        @param ipaddress:                 The ipaddress where agent is running
        @type ipaddress:                  string

        @param jobguid:                   Guid of the job
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                           dictionary
        
	"""
        params =dict()
        params['agentguid'] = agentguid
        params['ipaddress'] = ipaddress
        return q.workflowengine.actionmanager.startActorAction('agent', 'restart', params, jobguid=jobguid, executionparams=executionparams)

    def modifyPassword (self, machineguid, newPassword, jobguid = "", executionparams = {}):
        """
        
        Modifies the password of agentv4 running on given machine

        @param machineguid:               Guid of the pmachine
        @type machineguid:                guid

        @param newPassword:               new password to set
        @type newPassword:                string

        @param jobguid:                   Guid of the job
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                           dictionary
        
	"""
        params =dict()
        params['newPassword'] = newPassword
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('agent', 'modifyPassword', params, jobguid=jobguid, executionparams=executionparams)


