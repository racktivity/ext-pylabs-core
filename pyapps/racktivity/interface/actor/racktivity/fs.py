class FS():
    def writeFile(self, agentguid, filename, contents, append=False, request="", jobguid="", executionparams=dict()):
        """
        Writes file content to path
        
        @param agentguid: guid of the agent which will execute the action
        @type agentguid: guid 
      
        @param filename: The file path
        @type filename:  path
        
        @param contents: The file contents to write
        @type contents:  string
        
        @param append:  If file exists, append the contents to the file
        @type append:  boolean
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
    
        @return:                 dictionary with True as result and jobguid: {'result': {'returncode': True}, 'jobguid': guid}
        @rtype:                  dictionary
        """