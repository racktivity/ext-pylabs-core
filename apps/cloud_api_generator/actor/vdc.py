from pylabs import q

class vdc:
    def importVdc (self, sourceUri, vdcGuid = "", executerMachineGuid = "", jobguid = "", executionparams = {}):
        """
        
        exports vdc info to destinationURI
        
        @param destinationuri:        destination of export
        @type destinationuri:         string
        
        @param vdcGuid:               Guid of the vdc
        @type vdcGuid:                guid
        
        @param executerMachineGuid:   Guid of the export executing machine
        @type executerMachineGuid:    guid

        @param jobguid:               Guid of the job
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                       dictionary
        
	"""
        params =dict()
        params['executerMachineGuid'] = executerMachineGuid
        params['vdcGuid'] = vdcGuid
        params['sourceUri'] = sourceUri
        return q.workflowengine.actionmanager.startActorAction('vdc', 'importVdc', params, jobguid=jobguid, executionparams=executionparams)

    def exportVdc (self, vdcGuid, destinationUri, executerMachineGuid = "", jobguid = "", executionparams = {}):
        """
        
        exports machine info to destinationURI
        
        @param vdcGuid:             Guid of the vdc
        @type vdcGuid:              guid
        
        @param destinationuri:      destination of export
        @type destinationuri:       string
        
        @param executerMachineGuid: Guid of the export executing machine
        @type executerMachineGuid:  guid

        @param jobguid:             Guid of the job
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                     dictionary
        
	"""
        params =dict()
        params['destinationUri'] = destinationUri
        params['executerMachineGuid'] = executerMachineGuid
        params['vdcGuid'] = vdcGuid
        return q.workflowengine.actionmanager.startActorAction('vdc', 'exportVdc', params, jobguid=jobguid, executionparams=executionparams)


