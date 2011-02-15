from pylabs import q

class cloudinstallservice:
    def initialize (self, applicationguid = "", jobguid = "", executionparams = {}):
        """
        
        Installs and configures the cloud install service.

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
        return q.workflowengine.actionmanager.startActorAction('cloudinstallservice', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def bootInRecoveryMode (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Configures the cloud install service so that a machine gets booted in recovery mode

        @param machineguid:                Guid of the machine to boot in recovery mode.
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
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('cloudinstallservice', 'bootInRecoveryMode', params, jobguid=jobguid, executionparams=executionparams)

    def installDCOS (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Installs DC-OS for the machine specified.
        As a result DC-OS is installed along with an agent and the machine is registered with the management machine.

        @param machineguid:                Guid of the machine to add.
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
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('cloudinstallservice', 'installDCOS', params, jobguid=jobguid, executionparams=executionparams)

    def bootFromLocalDisk (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Configures the cloud install service so that a machine boots from its local disk

        @param machineguid:                Guid of the machine to add.
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
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('cloudinstallservice', 'bootFromLocalDisk', params, jobguid=jobguid, executionparams=executionparams)


