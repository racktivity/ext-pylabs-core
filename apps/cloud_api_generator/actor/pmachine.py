from pylabs import q

class pmachine:
    def applyPartitionTemplate (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Applies new partion template to a pmachine 
       
        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary list of installed packages
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'applyPartitionTemplate', params, jobguid=jobguid, executionparams=executionparams)

    def initializeNetwork (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Configures the machine's network so that it can be used in cloud

        @param machineguid:       Guid of the machine
        @type machineguid:        guid

        @param jobguid:           Guid of the job
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'initializeNetwork', params, jobguid=jobguid, executionparams=executionparams)

    def reconfigureUser (self, machineguid, clouduserguid, newpassword, jobguid = "", executionparams = {}):
        """
        
        Updates configfiles and user credentials for clouduser
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param clouduserguid:         guid of the clouduser
        @type clouduserguid:          string
        
        @param newpassword:           newpassword for the user
        @type newpassword:            string 
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['clouduserguid'] = clouduserguid
        params['newpassword'] = newpassword
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'reconfigureUser', params, jobguid=jobguid, executionparams=executionparams)

    def changePassword (self, machineguid, username, newpassword, jobguid = "", executionparams = {}):
        """
        
        Changes the password on a pmachine using new password
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param username               username
        @type username                string
        
        @param newpassword            new password of the user
        @type newpassword             string

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['username'] = username
        params['newpassword'] = newpassword
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'changePassword', params, jobguid=jobguid, executionparams=executionparams)

    def shutdown (self, machineguid, multiple = False, jobguid = "", executionparams = {}):
        """
        
        Shutdown a pmachine and related vmachines
       
        @param machineguid:         Guid of the machine
        @type machineguid:          guid
        
        @param multiple:            Boolean that indicates if pmachine shutdown is part of completed environment shutdown
        @type multiple:             boolean
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary 
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['multiple'] = multiple
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'shutdown', params, jobguid=jobguid, executionparams=executionparams)

    def setTimeZone (self, machineguid, timezone, jobguid = "", executionparams = {}):
        """
        
        set timezone for a pmachine
        
        @param machineguid:         machineguid of the pmachine
        @type machineguid:          machineguid
       
        @param timezone:            name of the timezone
        @type timezone:             string
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary 
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['timezone'] = timezone
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'setTimeZone', params, jobguid=jobguid, executionparams=executionparams)

    def listSnapshots (self, machineguid, volumeid = "", jobguid = "", executionparams = {}):
        """
        
        lists snapshots on a node 
        
        @param machineguid:           guid of pmachine
        @type machineguid:            guid
        
        @param volumeid:              Volume id to list snapshots from
        @type volumeid:               string
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with result a dict of machineguid,volume ids and its snapshot ids
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['volumeid'] = volumeid
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'listSnapshots', params, jobguid=jobguid, executionparams=executionparams)

    def writeCfgFile (self, machineguid, filename, settings = [], jobguid = "", executionparams = {}):
        """
        
        Retrieves installed packages on a physical machine 
       
        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param filename:            name of the config file
        @type filename:             string
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param settings:            list of dict { 'section':, 'key':, 'value': }
        @type settings              list
        
        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary list of installed packages
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['filename'] = filename
        params['settings'] = settings
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'writeCfgFile', params, jobguid=jobguid, executionparams=executionparams)

    def reconnectVolumes (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Restarts volumes on a physical machine

        @param machineguid:           guid of the pmachine rootobject
        @type machineguid:            guid
        
        @param jobguid:               Guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. maxduration ...
        @type executionparams:        dictionary

        @return:                      True
        @rtype:                       boolean       
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'reconnectVolumes', params, jobguid=jobguid, executionparams=executionparams)

    def deleteSnapshots (self, listofsnapshots = [], jobguid = "", executionparams = {}):
        """
        
        Deletes snapshots on a physical machine 

        @param listofsnapshots:       list of snapshots to delete
        @type listofsnapshots:        list

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['listofsnapshots'] = listofsnapshots
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'deleteSnapshots', params, jobguid=jobguid, executionparams=executionparams)

    def prepareShutdown (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Prepares a shutdown of a pmachine and related vmachines
       
        @param machineguid:         Guid of the machine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary 
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'prepareShutdown', params, jobguid=jobguid, executionparams=executionparams)

    def reboot (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Reboots a pmachine 
       
        @param machineguid:         Guid of the machine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary 
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'reboot', params, jobguid=jobguid, executionparams=executionparams)

    def executeQshellScript (self, machineguid, qshellscriptcontent, jobguid = "", executionparams = {}):
        """
        
        Execute a Q-Shell script on a pmachine.

        @param machineguid:                guid of the pmachine to execute the script on
        @type  machineguid:                guid

        @param qshellscriptcontent:        Content of the script to execute.
        @type  qshellscriptcontent:        string

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['qshellscriptcontent'] = qshellscriptcontent
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'executeQshellScript', params, jobguid=jobguid, executionparams=executionparams)

    def listVolumes (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Lists volumes on specified node 
        
        @param machineguid:           guid of pmachine
        @type machineguid:            guid
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      list with volume ids
        @rtype:                       list

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'listVolumes', params, jobguid=jobguid, executionparams=executionparams)

    def inventoryScan (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Scans a pmachine to make an inventory of its disk(sizes),memory,cpu,nics... 
       
        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with True if inventory scan succeeded
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'inventoryScan', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Configures the machine so that it can be used in cloud

        @param machineguid:       Guid of the machine
        @type machineguid:        guid

        @param jobguid:           Guid of the job
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def deleteVolumes (self, volumes, jobguid = "", executionparams = {}):
        """
        
        Volumes that needs to be deleted
        
        @param volumes:               dict of volumes. Format: {pmachineguid:[volumes]}
        @type volumes:                dictionary
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with result a boolean
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['volumes'] = volumes
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'deleteVolumes', params, jobguid=jobguid, executionparams=executionparams)

    def addUser (self, machineguid, username, password, shell, jobguid = "", executionparams = {}):
        """
        
        add user on pmachine
        
        @param machineguid:                guid of pmachine
        @type machineguid:                 guid
        
        @param username:                   name of the user
        @type username:                    string
        
        @param password:                   password for the user
        @type password:                    string
        
        @param shell:                      default shell for the user
        @type shell:                       string
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary

        @return:                           dictionary 
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['username'] = username
        params['shell'] = shell
        params['password'] = password
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'addUser', params, jobguid=jobguid, executionparams=executionparams)

    def disconnectVolumes (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Disconnects volumes on a physical machine

        @param machineguid:           guid of the pmachine rootobject
        @type machineguid:            guid
        
        @param jobguid:               Guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. maxduration ...
        @type executionparams:        dictionary

        @return:                      True
        @rtype:                       boolean       
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'disconnectVolumes', params, jobguid=jobguid, executionparams=executionparams)

    def generateRRDGraph (self, machineguid, rrdParams = {}, jobguid = "", executionparams = {}):
        """
        
        Generates RRD Graph and returns the uri of generated graph
       
        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param rrdParams:           Dictionary of all parameters needed to generate the RRD graph
        @type rrdParams:            dictionary
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with uri of RRD 
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['rrdParams'] = rrdParams
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'generateRRDGraph', params, jobguid=jobguid, executionparams=executionparams)

    def removeUser (self, machineguid, username, jobguid = "", executionparams = {}):
        """
        
        remove user on pmachine
        
        @param machineguid:                guid of pmachine
        @type machineguid:                 guid

        @param username:                   name of the user
        @type username:                    string
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary

        @return:                           dictionary 
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['username'] = username
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'removeUser', params, jobguid=jobguid, executionparams=executionparams)

    def getInstalledPackages (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Retrieves installed packages on a physical machine 
       
        @param machineguid:         Guid of the pmachine
        @type machineguid:          guid
        
        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary list of installed packages
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'getInstalledPackages', params, jobguid=jobguid, executionparams=executionparams)

    def isServiceRunning (self, ip, portnr, protocol, jobguid = "", executionparams = {}):
        """
        
        Checks whether a service is listing on ip:portnr using defined protocol
        
        @param ip:                    ip address of pmachine
        @type ip:                     string
        
        @param portnr:                portnr
        @type portnr:                 int
        
        @param protocol:              protocol
        @type protocol:               string
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with result a boolean
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        
	"""
        params =dict()
        params['ip'] = ip
        params['portnr'] = portnr
        params['protocol'] = protocol
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'isServiceRunning', params, jobguid=jobguid, executionparams=executionparams)

    def refreshStatus (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Gets the status of the physical machine

        @param machineguid:           guid of the machine rootobject
        @type machineguid:            guid
        
        @param jobguid:               Guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. maxduration ...
        @type executionparams:        dictionary

        @return:                      True or False
        @rtype:                       boolean
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('pmachine', 'refreshStatus', params, jobguid=jobguid, executionparams=executionparams)


