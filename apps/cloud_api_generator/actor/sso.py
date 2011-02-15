from pylabs import q

class sso:
    def sendMail (self, smtpserver, subject, body = "", sender = "", to = "", smtplogin = "", smtppassword = "", jobguid = "", executionparams = {}):
        """
        
        Sends a mail using smtp 

        @param smtpserver:        Smtp server for sending the email 
        @type smtpserver:         string

        @param subject:           Subject for the email 
        @type subject:            string

        @param body:              Body of the mail
        @type body:               string
        
        @param sender:            The email address of the sender
        @type sender:             string
        
        @param to:                The email address of the addressee (when None admin is the target)
        @type to:                 string

        @param smtplogin:         Login for the smtp server
        @type smtplogin:          string
        
        @param smtppassword:      Password for the smtp server
        @type smtppassword:       string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['body'] = body
        params['sender'] = sender
        params['smtppassword'] = smtppassword
        params['to'] = to
        params['smtpserver'] = smtpserver
        params['smtplogin'] = smtplogin
        params['subject'] = subject
        return q.workflowengine.actionmanager.startActorAction('sso', 'sendMail', params, jobguid=jobguid, executionparams=executionparams)

    def sendSNMPTrap (self, message, hostdestination = "127.0.0.1", port = 162, community = "aserver", jobguid = "", executionparams = {}):
        """
        
        Generate a notification (trap) to report an event to the SNMP manager with the specified message.

        @param message:           Message of notification 
        @type message:            string

        @param hostdestination:   Specifies to connect to the SNMP agent on the specified host. 
        @type hostdestination:    string
        
        @param port:              Port number on host
        @type port:               string
        
        @param community:         Specifies community name to use
        @type community:          string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['message'] = message
        params['hostdestination'] = hostdestination
        params['community'] = community
        params['port'] = port
        return q.workflowengine.actionmanager.startActorAction('sso', 'sendSNMPTrap', params, jobguid=jobguid, executionparams=executionparams)

    def validateDomain (self, url, macaddresses = [], domain = "", jobguid = "", executionparams = {}):
        """
        
        validates a domain for a customer

        @param url:               validation url
        @type url:                string

        @param macaddresses:      list of macaddresses to be validated
        @type macaddresses:       list

        @param domain:            Domain to validate
        @type domain:             string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['url'] = url
        params['domain'] = domain
        params['macaddresses'] = macaddresses
        return q.workflowengine.actionmanager.startActorAction('sso', 'validateDomain', params, jobguid=jobguid, executionparams=executionparams)

    def maintenance (self, duration = 3600, jobguid = "", executionparams = {}):
        """
        
        Execute maintenance tasks on SSO environment.
        
        @param duration:            duration of the maintenance tasks (seconds)
        @type duration:             int
        
        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary {'guid','name','pmachineguid','maintenancemode','VBoxProcessID','ipaddress','portnumber'}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['duration'] = duration
        return q.workflowengine.actionmanager.startActorAction('sso', 'maintenance', params, jobguid=jobguid, executionparams=executionparams)

    def sendMessageToNoc (self, loginname, username, password, domain, url, message, jobguid = "", executionparams = {}):
        """
        
        Sends a message to the NOC for a certain domain

        @param loginname          Login of the customer unregistering the domain
        @type loginname           string

        @param username           ITPS portal username
        @type username            string

        @param password           ITPS portal password
        @type password            string

        @param domain             Domain to unregister
        @type domain              string

        @param url                register url
        @type url                 string

        @param message            message to be sent
        @type message             string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['username'] = username
        params['domain'] = domain
        params['loginname'] = loginname
        params['url'] = url
        params['message'] = message
        params['password'] = password
        return q.workflowengine.actionmanager.startActorAction('sso', 'sendMessageToNoc', params, jobguid=jobguid, executionparams=executionparams)

    def registerDomain (self, loginname, username, password, domain, url, jobguid = "", executionparams = {}):
        """
        
        Registers a domain for a customer

        @param loginname          Login of the customer registering the domain
        @type loginname           string

        @param username           ITPS portal username
        @type username            string

        @param password           ITPS portal password
        @type password            string

        @param domain             Domain to register
        @type domain              string

        @param url                register url
        @type url                 string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['username'] = username
        params['url'] = url
        params['password'] = password
        params['loginname'] = loginname
        params['domain'] = domain
        return q.workflowengine.actionmanager.startActorAction('sso', 'registerDomain', params, jobguid=jobguid, executionparams=executionparams)

    def unregisterDomain (self, loginname, username, password, domain, url, jobguid = "", executionparams = {}):
        """
        
        Unregisters a domain for a customer

        @param loginname          Login of the customer unregistering the domain
        @type loginname           string

        @param username           ITPS portal username
        @type username            string

        @param password           ITPS portal password
        @type password            string

        @param domain             Domain to unregister
        @type domain              string

        @param url                register url
        @type url                 string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
        params =dict()
        params['username'] = username
        params['url'] = url
        params['password'] = password
        params['loginname'] = loginname
        params['domain'] = domain
        return q.workflowengine.actionmanager.startActorAction('sso', 'unregisterDomain', params, jobguid=jobguid, executionparams=executionparams)


