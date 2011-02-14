from pymonkey import q

class drpdb:
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'drpdb'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('drpdb', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, name = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of drpdb guids which met the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the machine.
        @type name:                        string
        
        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of drpdb guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        executionparams['rootobjecttype'] = 'drpdb'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('drpdb', 'find', params, jobguid=jobguid, executionparams=executionparams)


