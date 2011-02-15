from pylabs import q

class machine:
    def exportMachine (self, machineGuid, destinationUri, executerMachineGuid = "", jobguid = "", executionparams = {}):
        """
        
        exports machine info to destinationURI
        
        @param machineguid:              Guid of the machine
        @type machineguid:               guid
        
        @param destinationuri:           destination of export
        @type destinationuri:            string
        
        @param executerMachineGuid:      Guid of the export executing machine
        @type executerMachineGuid:       guid

        @param jobguid:                  Guid of the job
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary
        
	"""
        params =dict()
        params['destinationUri'] = destinationUri
        params['executerMachineGuid'] = executerMachineGuid
        params['machineGuid'] = machineGuid
        return q.workflowengine.actionmanager.startActorAction('machine', 'exportMachine', params, jobguid=jobguid, executionparams=executionparams)

    def importMachine (self, sourceUri, machineGuid = "", executerMachineGuid = "", jobguid = "", executionparams = {}):
        """
        
        exports machine info to destinationURI       
        
        @param destinationuri:           destination of export
        @type destinationuri:            string
        
        @param machineguid:              Guid of the machine
        @type machineguid:               guid
        
        @param executerMachineGuid:      Guid of the export executing machine
        @type executerMachineGuid:       guid

        @param jobguid:                  Guid of the job
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary
        
	"""
        params =dict()
        params['executerMachineGuid'] = executerMachineGuid
        params['sourceUri'] = sourceUri
        params['machineGuid'] = machineGuid
        return q.workflowengine.actionmanager.startActorAction('machine', 'importMachine', params, jobguid=jobguid, executionparams=executionparams)


