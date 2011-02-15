from pylabs import q

class application:
    def restore (self, applicationguid, sourceuri, compressed = True, jobguid = "", executionparams = {}):
        """
        
        Restores an application from the specified backup
        PHASE 2

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param sourceuri:        URI of the location where the backup is stored
        @type sourceuri:         string

        @param compressed:       Boolean value which indicates if backup is zipped (compression = 7zip)
        @type compressed:        boolean

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        params['compressed'] = compressed
        params['sourceuri'] = sourceuri
        return q.workflowengine.actionmanager.startActorAction('application', 'restore', params, jobguid=jobguid, executionparams=executionparams)

    def start (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Starts the application specified

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('application', 'start', params, jobguid=jobguid, executionparams=executionparams)

    def getstatus (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Gets the realtime status of the application specified

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with status as result and jobguid: {'result': 'running', 'jobguid': guid}
        @rtype:                  dictionary

        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('application', 'getstatus', params, jobguid=jobguid, executionparams=executionparams)

    def stop (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Stops the application specified

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('application', 'stop', params, jobguid=jobguid, executionparams=executionparams)

    def reload (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Reloads the specified application 

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('application', 'reload', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, applicationguid = "", uninstallfirst = False, jobguid = "", executionparams = {}):
        """
        
        Initializes the application specified
        e.g. install the appropriate qpackages
        e.g. configure the application

        @param applicationguid:      Guid of the application
        @type applicationguid:       guid

        @param uninstallfirst:       Boolean value indicating if the application must be uninstalled before initializing it.
        @type uninstallfirst:        boolean

        @param jobguid:              Guid of the job
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        params['uninstallfirst'] = uninstallfirst
        return q.workflowengine.actionmanager.startActorAction('application', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def uninstall (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Uninstalls the application specified

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('application', 'uninstall', params, jobguid=jobguid, executionparams=executionparams)

    def backup (self, applicationguid, destinationuri, compressed = True, jobguid = "", executionparams = {}):
        """
        
        Exports the application specified as a backup to a remote destination specified

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param destinationuri:   URI of the location where the backup should be stored. (e.g ftp://login:passwd@myhost.com/backups/applicationx/)
        @type destinationuri:    string

        @param compressed:       if true backup will be zipped (compression = 7zip)
        @type compressed:        boolean

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        @security administrators
        
	"""
        params =dict()
        params['destinationuri'] = destinationuri
        params['applicationguid'] = applicationguid
        params['compressed'] = compressed
        return q.workflowengine.actionmanager.startActorAction('application', 'backup', params, jobguid=jobguid, executionparams=executionparams)

    def restart (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Restarts the application specified

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('application', 'restart', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the specified application 

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('application', 'delete', params, jobguid=jobguid, executionparams=executionparams)


