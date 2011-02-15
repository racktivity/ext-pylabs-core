from pylabs import q

class test:
    def testTimeout (self, jobguid = "", executionparams = {}):
        """
        
        test if job gets killed after maxduration specified in execution params
        
	"""
        params =dict()
        return q.workflowengine.actionmanager.startActorAction('test', 'testTimeout', params, jobguid=jobguid, executionparams=executionparams)


