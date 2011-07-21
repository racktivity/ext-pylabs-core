class events():
    def raiseCritical(self, agentguid, message, messageprivate='', typeid='', tags='', escalate=False, request="", jobguid="", executionparams=dict()):
        """
        Raise Critical
        
        @param agentguid: guid of the agent which will execute the action
        @type agentguid: guid 
        
        @param message: Message
        @type message: str 
        
        @param messageprivate: Private Message
        @type messageprivate: str
        
        @param typeid: Type ID
        @type typeid: str
        
        @param tags: Tags
        @type tags: tag string
        
        @param escalate: If true, event handlers tasklets will be fired with the given parameters, tags and typeid
        @type escalate: boolean
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 dictionary with True as result and jobguid: {'result': {'returncode': True}, 'jobguid': guid}
        @rtype:                  dictionary
        """
        
    def raiseError(self, agentguid, message, messageprivate='', typeid='', tags='', escalate=False, request="", jobguid="", executionparams=dict()):
        """
        Raise Error
        
        @param agentguid: guid of the agent which will execute the action
        @type agentguid: guid 
        
        @param message: Message
        @type message: str 
        
        @param messageprivate: Private Message
        @type messageprivate: str
        
        @param typeid: Type ID
        @type typeid: str
        
        @param tags: Tags
        @type tags: tag string
        
        @param escalate: If true, event handlers tasklets will be fired with the given parameters, tags and typeid
        @type escalate: boolean
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 dictionary with True as result and jobguid: {'result': {'returncode': True}, 'jobguid': guid}
        @rtype:                  dictionary
        """
    
    def raiseUrgent(self, agentguid, message, messageprivate='', typeid='', tags='', escalate=False, request="", jobguid="", executionparams=dict()):
        """
        Raise Urgent
        
        @param agentguid: guid of the agent which will execute the action
        @type agentguid: guid 
        
        @param message: Message
        @type message: str 
        
        @param messageprivate: Private Message
        @type messageprivate: str
        
        @param typeid: Type ID
        @type typeid: str
        
        @param tags: Tags
        @type tags: tag string
        
        @param escalate: If true, event handlers tasklets will be fired with the given parameters, tags and typeid
        @type escalate: boolean
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 dictionary with True as result and jobguid: {'result': {'returncode': True}, 'jobguid': guid}
        @rtype:                  dictionary
        """
    
    def raiseInfo(self, agentguid, message, messageprivate='', typeid='', tags='', escalate=False, request="", jobguid="", executionparams=dict()):
        """
        Raise Info
        
        @param agentguid: guid of the agent which will execute the action
        @type agentguid: guid 
        
        @param message: Message
        @type message: str 
        
        @param messageprivate: Private Message
        @type messageprivate: str
        
        @param typeid: Type ID
        @type typeid: str
        
        @param tags: Tags
        @type tags: tag string
        
        @param escalate: If true, event handlers tasklets will be fired with the given parameters, tags and typeid
        @type escalate: boolean
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 dictionary with True as result and jobguid: {'result': {'returncode': True}, 'jobguid': guid}
        @rtype:                  dictionary
        """
    
    def raiseWarning(self, agentguid, message, messageprivate='', typeid='', tags='', escalate=False, request="", jobguid="", executionparams=dict()):
        """
        Raise Warning
        
        @param agentguid: guid of the agent which will execute the action
        @type agentguid: guid 
        
        @param message: Message
        @type message: str 
        
        @param messageprivate: Private Message
        @type messageprivate: str
        
        @param typeid: Type ID
        @type typeid: str
        
        @param tags: Tags
        @type tags: tag string
        
        @param escalate: If true, event handlers tasklets will be fired with the given parameters, tags and typeid
        @type escalate: boolean
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 dictionary with True as result and jobguid: {'result': {'returncode': True}, 'jobguid': guid}
        @rtype:                  dictionary
        """