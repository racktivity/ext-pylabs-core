from pylabs import q

class volumestorageclient:
    def diskConnect (self, diskguid, restartlocal = False, ignorelock = False, usefailovercache = False, jobguid = "", executionparams = {}):
        """
        
        Connects disk specified on host.
        Can only be used after diskDisconnect


        FLOW for DSS VOLUME CLIENT
        # ...

        @param diskguid:                   Guid of the disk to connect.
        @type  diskguid:                   guid

        @param restartlocal:               Boolean indicating if the local cache should be used to restart the volume
        @type restartlocal:                boolean

        @param ignorelock:                 Boolean indicating if the lock on the backend should be ignored to restart the volume
        @type ignorelock:                  boolean

        @param usefailovercache:           Boolean indicating if the failover cache should be used to restart the volume
        @type usefailovercache:            boolean
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid
        
        @param executionparams:            dictionary with additional executionParams
        @type executionparams:             dictionary

        @return:                           dictionary with device name as result and jobguid: {'result': '/dev/...', 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['restartlocal'] = restartlocal
        params['diskguid'] = diskguid
        params['ignorelock'] = ignorelock
        params['usefailovercache'] = usefailovercache
        return q.workflowengine.actionmanager.startActorAction('volumestorageclient', 'diskConnect', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, applicationguid = "", jobguid = "", executionparams = {}):
        """
        
        Initializes client for storage system.

        FLOW for DSS VOLUME CLIENT
        # install qpackages for dssvolumeclient
        # in drp look for dsssttore cloudservice
        # find director app in hat cloudservice
        # configure dssclient (mgmtsal) to connect to that director
        # configure cache for dss: if no SSD use cache location on 2nd disk and make smaller, transaction logs on 3d disk  @todo check with Wim

        # install dssfailovercache qpackage
        # create path for the failovercache
        # start dssfailovercache on that path (add to auto start/stop)
        # add failovercache to model as dssfailovercache application (giving service to a disk (path), IP and port)
        
        @note Can be run as many times as required
        @note If this completes successful means we are connected to appropriate storage system

        @param applicationguid:            Guid of the application on which the storage system client should be initialized.
        @type  applicationguid:            guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with bool value as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageclient', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def diskResetFailover (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Reconfigures the failover cache for an attached disk.

        @param diskguid:                   Guid of the disk to disconnect.
        @type  diskguid:                   guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageclient', 'diskResetFailover', params, jobguid=jobguid, executionparams=executionparams)

    def getFailoverCacheMode (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Retrieves the failover cache mode for an attached disk.

        @param diskguid:                   Guid of the disk to get FOC Mode.
        @type  diskguid:                   guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': OK_SYNC, OK_STANDALONE, CATCHUP , DEGRADED or None, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageclient', 'getFailoverCacheMode', params, jobguid=jobguid, executionparams=executionparams)

    def diskDisconnect (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Disconnects disk specified on host.

        @param diskguid:                   Guid of the disk to disconnect.
        @type  diskguid:                   guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageclient', 'diskDisconnect', params, jobguid=jobguid, executionparams=executionparams)


