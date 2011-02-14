from pymonkey import q

class job:
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:   guid of the job rootobject
        @type rootobjectguid:    guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 rootobject
        @rtype:                  rootobject

        @warning:                Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, jobguid = "", executionparams = {}):
        """
        
        Create a new job.

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with backplaneguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectAction('job', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def getXMLSchema (self, jobguid, executionparams = {}):
        """
        
        Gets a string representation in XSD format of the job rootobject structure.

        @execution_method = sync
        
        @param jobguid:          guid of the job rootobject
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 XSD representation of the job structure.
        @rtype:                  string

        @raise e:                In case an error occurred, exception is raised

        @todo:                   Will be implemented in phase2
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def clear (self, jobguid = "", executionparams = {}):
        """
        
        Deletes all jobs.
        
        @execution_method = sync
        
        @security: administrator
        
        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        
        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'clear', params, jobguid=jobguid, executionparams=executionparams)

    def getYAML (self, yamljobguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the job rootobject.

        @execution_method = sync
        
        @param yamljobguid:       guid of the job rootobject
        @type yamljobguid:        guid

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  YAML representation of the job
        @rtype:                   string
        
	"""
        params =dict()
        params['yamljobguid'] = yamljobguid
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def getLogInfo (self, jobguid, MaxLogLevel = 5, executionparams = {}):
        """
        
        return log info as string
        @todo define format
        
        @execution_method = sync

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param MaxLogLevel:      Specifies the highest log level
        @type MaxLogLevel:       integer

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 job log info
        @rtype:                  string
        
        @todo:                   Will be implemented in phase2
        
	"""
        params =dict()
        params['MaxLogLevel'] = MaxLogLevel
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'getLogInfo', params, jobguid=jobguid, executionparams=executionparams)

    def findLatestJobs (self, maxrows = 5, errorsonly = False, jobguid = "", executionparams = {}):
        """
        
        Returns the latest jobs.

        @execution_method = sync
        
        @param maxrows:          specifies the number of jobs to return
        @type maxrows:           int

        @param errorsonly:       When True, only the latest <maxrows> ERROR jobs will be returned, otherwise the latest <maxrows> ERROR/RUNNING jobs will be returned
        @type errorsonly:        boolean

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 jobtree
        @rtype:                  array of dict [{...}]
        
	"""
        params =dict()
        params['errorsonly'] = errorsonly
        params['maxrows'] = maxrows
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'findLatestJobs', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, jobguid, executionparams = {}):
        """
        
        Gets a string representation in XML format of the job rootobject.

        @execution_method = sync
        
        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  XML representation of the job
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised

        @todo:                    Will be implemented in phase2
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def getJobTree (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the full tree of the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:   guid of the job rootobject
        @type rootobjectguid:    guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 jobtree
        @rtype:                  array of dict [{...}]
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'getJobTree', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, actionname = "", agentguid = "", machineguid = "", applicationguid = "", datacenterguid = "", fromTime = "", toTime = "", clouduserguid = "", jobguid = "", executionparams = {}):
        """
                
        @execution_method = sync
        
        @param actionname:       actionname of the jobs to find
        @type actionname:        string

        @param agentguid:        agentguid of the jobs to find
        @type agentguid:         guid

        @param machineguid:      machineguid of the jobs to find
        @type machineguid:       guid

        @param applicationguid:  applicationguid of the jobs to find
        @type applicationguid:   guid

        @param datacenterguid:   datacenterguid of the jobs to find
        @type datacenterguid:    guid

        @param fromTime:         starttime of the jobs to find (equal or greater than)
        @type fromTime:          datetime

        @param toTime:           endtime of the jobs to find (equal or less than)
        @type toTime:            datetime
        
        @param clouduserguid:    guid of the job user executing the job
        @type clouduserguid:     guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @returns array of array [[...]]
        
	"""
        params =dict()
        params['clouduserguid'] = clouduserguid
        params['actionname'] = actionname
        params['applicationguid'] = applicationguid
        params['toTime'] = toTime
        params['agentguid'] = agentguid
        params['fromTime'] = fromTime
        params['datacenterguid'] = datacenterguid
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, jobguids, jobguid = "", executionparams = {}):
        """
        
        Delete all specified jobs and their children.
        
        @security: administrator
        
        @execution_method = sync
        
        @param jobguids:                 List of jobguids to delete           
        @type jobguids:                  array
        
        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        
        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['jobguids'] = jobguids
        executionparams['rootobjecttype'] = 'job'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('job', 'delete', params, jobguid=jobguid, executionparams=executionparams)


