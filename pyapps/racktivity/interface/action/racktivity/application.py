class Application():

    def create(self, name, deviceguid="",  parentapplicactionguid="",description="", customsettings="", template=False, tags="",  request="", jobguid="", executionparams=dict()):
        """
        Creates a new application, does not provision application yet
        Application does not have to be linked to a machine.
        An application can group other applications, these are called cloudservices


        @param deviceguid:            guid of the device related to this application
        @type deviceguid:             guid
        
        @param name:                   Name for this new application. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                    string

        @param description:            Description for this new application. This is free text describing the purpose of the application, if multi-line use back-slash + \n
        @type description:             string

        @param customsettings:         Custom settings for this new application.
        @type customsettings:          string
        
        @param template:              indicate if the application is a template
        @type template:               boolean
        
        @param tags: string of tags
        @type tags: string

        @param parentapplicactionguid: link to application which is cloudservice (modelled as parent application)
        @type parentapplicactionguid:  guid

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                        dictionary with returncode and applicationguid as result and jobguid: {'result':{returncode:'True', applicationguid:guid}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def createFromTemplate(self, deviceguid, applicationtemplateguid, name, description="", customsettings="", tags="",  request="", jobguid="", executionparams=dict()):
        """
        Creates a new application, does not provision application yet

        @param deviceguid:                      guid of the device related to this application
        @type deviceguid:                       guid
        
        @param applicationtemplateguid:          guid of the applicationtemplate to create this application from
        @type applicationtemplateguid:           guid

        @param name:                             Name for this new application. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                              string

        @param description:                      Description for this new application. This is free text describing the purpose of the application, if multi-line use back-slash + \n
        @type description:                       string

        @param customsettings:                   Custom settings for this new application.
        @type customsettings:                    string
        
        @param tags: string of tags
        @type tags: string

        @param jobguid:                          guid of the job if avalailable else empty string
        @type jobguid:                           guid

        @param executionparams:                  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:                   dictionary

        @return                                  dictionary with returncode and applicationguid as result and jobguid: {'result':{returncode:'True', applicationguid:guid}, 'jobguid': guid}
        @rtype:                                  dictionary

        @raise e:                                In case an error occurred, exception is raised
      
        """
        
    def delete(self, applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Deletes the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def updateModelProperties(self, applicationguid, name="", description="", status="", customsettings="", template="", tags="", request="", jobguid="", executionparams=dict()):
        """
        Update properties, every parameter which is not passed or passed as empty string is not updated.
        @SECURITY administrator only

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param name:                 Name for this application
        @type name:                  string

        @param description:          Description for this application
        @type description:           string

        @param status:               Status for this application
        @type status:                string

        @param customsettings:       Custom settings for this application
        @type customsettings:        string
        
        @param template:              indicate if the application is a template
        @type template:               boolean
        
        @param tags: tags(strings)
        @type tags: string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                      dictionary with returncode and applicationguid as result and jobguid: {'result':{returncode:'True', applicationguid:guid}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """
  

    def start(self, applicationguid, failifnotenoughresource=False, request="", jobguid="", executionparams=dict()):
        """
        Starts the application specified.

        @param applicationguid:          guid of the application to start.
        @type applicationguid:           guid

        @param failifnotenoughresource:  Boolean value indicating if application should not start if not enough resources are available.
        @type failifnotenoughresource:   boolean

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def stop(self, applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Stops the application specified.

        @param applicationguid:          guid of the application to stop.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def restart(self, applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Restart the application specified.

        @param applicationguid:          guid of the application to restart.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def disable(self, applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Disables the application specified.

        @param applicationguid:          guid of the application to disable.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def initialize(self,applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Performs initialization actions on the application specified. As a result the application will be ready to be used.
        @security administrators

        @param applicationguid:          guid of the application to initialize.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def getObject(self, rootobjectguid, request="", jobguid="",executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync

        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        """
        
        
    def list(self, deviceguid="",  applicationguid="", name="",status="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of applications.
        @SECURITY administrator only

        @execution_method = sync

        @param deviceguid:       guid of the device on which the application is running if avalailable else empty string
        @type deviceguid:        guid
        
        @param applicationguid:   guid of the application if avalailable else empty string
        @type applicationguid:    guid
        
        @param name:   name of the application
        @type name:   string

        @param status:            status of the application to include in the search criteria.
        @type status:             string

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  returncode(True) and Dictionary(applicationinfo) of array of dictionaries with guid, name, description, status, template, applicationtemplateguid, deviceguid, devicename of the application.
        @rtype:                   dictionary
        @note:                    Example return value:
        @note:                    {'result': 'returncode':'True', 'applicationinfo':[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "RackcontrollerAPI", "description": "Rackcontroller api service", "status": "ACTIVE", "template": "False", "applicationtemplateguid": "", "deviceguid": "0D735CB9-8376-456C-827E-31CAC8815894", "devicename": "rackcontroller1 }],
        @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}}

        @raise e:                 In case an error occurred, exception is raised
        """

    def listStatuses(self, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of possible application statuses.

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 returncode(True) and Dictionary(statusinfo) of array of statuses.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': {'returncode':'True', 'statustypes':["ACTIVE", "DISABLED", "MAINTENANCE"]'},
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        
        @raise e:                In case an error occurred, exception is raised
        """

    def listAccountTypes(self, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of possible application account types.

        @execution_method = sync

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 returncode(True) and Dictionary(accounttypes) of array of application account types.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': {'returncode':'True', 'accounttypes': '["PUBLICACCOUNT", "SYSTEMACCOUNT"]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}}

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self,  deviceguid="", meteringdeviceguid="",  status="", name="", istemplate=False, tags="", request="", jobguid="", executionparams=dict()):
        """
        Returns a list of application guids which met the find criteria.

        @execution_method = sync

        @param deviceguid:             guid of the device to include in the search criteria.
        @type deviceguid:              guid
        
        @param meteringdeviceguid: guid of the meteringdevice to include in the search criteria
        @type meteringdeviceguid: guid

        @param status:                  Status of the  VDC to include in the search criteria. See listStatuses().
        @type status:                   string
        
        @param name:   name of the application
        @type name:   string

        @param istemplate:              indicate if the application is a template
        @type istemplate:               boolean

        @param tags:                    string of tags
        @type tags:                     string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        returntype(True) and Array(guidlist) of application guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': {'returncode:True', 'guidlist':["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}}

        @raise e:                       In case an error occurred, exception is raised
        """

    
    def addAccount(self, applicationguid, login, password, accounttype, request="", jobguid="", executionparams=dict()):
        """
        Adds an account for the application specified.

        @param applicationguid:          guid of the application to add a account to
        @type applicationguid:           guid

        @param login:                    Login for the new  account.
        @type login:                     string

        @param password:                 Password for the new account.
        @type password:                  string

        @param accounttype:              Type for the new account. See listAccountTypes().
        @type accounttype:               string

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    def removeAccount(self, applicationguid, login, accounttype, request="", jobguid="", executionparams=dict()):
        """
        Removes an account for the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param login:                    Login of the account to remove.
        @type login:                     string

        @param accouttype:               Type of the account to remove. See listAccountTypes().
        @type accouttype:                string

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """

    
    def addService(self, applicationguid, name, description="", request="", jobguid="", executionparams=dict()):
        """
        Adds a new service for the application specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param name:                 Name of service to add. Name must be unique!
        @type name:                  string

        @param description:          Description of service to add.d
        @type type:                  string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) and serviceguid as result and jobguid: {'result': {'returncode':True, 'serviceguid:}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def removeService(self, applicationguid, servicename, request="", jobguid="", executionparams=dict()):
        """
        Removes a service for the application specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service .
        @type servicename:           string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def offerServiceToDevice(self, applicationguid, servicename, deviceguid, remark="", request="", jobguid="", executionparams=dict()):
        """
        Offers a service for the device specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to add. Name must be unique!
        @type servicename:           string

        @param deviceguid:           guid of the device to which to offer the service specified
        @type deviceguid:            guid

        @param remark:               Remark to add to this service offer.
        @type type:                  string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """
    def revokeServiceToDevice(self, applicationguid, servicename, deviceguid, request="", jobguid="", executionparams=dict()):
        """
        Revokes a service for the device specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param deviceguid:           guid of the device to which to revoke the service specified
        @type deviceguid:            guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def offerServiceToApplication(self, applicationguid, servicename, destinationapplicationguid, remark="", request="", jobguid="", executionparams=dict()):
        """
        Offers a service for the application specified.

        @param applicationguid:            guid of the application specified
        @type applicationguid:             guid

        @param servicename:                Name of service to add. Name must be unique!
        @type servicename:                 string

        @param destinationapplicationguid: guid of the application to which to offer the service specified
        @type destinationapplicationguid:  guid

        @param remark:                     Remark to add to this service offer.
        @type type:                        string

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        """
    def revokeServiceToApplication(self, applicationguid, servicename, destinationapplicationguid, request="", jobguid="", executionparams=dict()):
        """
        Revokes a service for the application specified.

        @param applicationguid:            guid of the application specified
        @type applicationguid:             guid

        @param servicename:                Name of service to revoke. Name must be unique!
        @type servicename:                 string

        @param destinationapplicationguid: guid of the application to which to revoke the service specified
        @type destinationapplicationguid:  guid

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        """

    def offerServiceToLan(self, applicationguid, servicename, languid, remark="", request="", jobguid="", executionparams=dict()):
        """
        Offers a service for the lan specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to add. Name must be unique!
        @type servicename:           string

        @param languid:              guid of the lan to which to offer the service specified
        @type languid:               guid

        @param remark:               Remark to add to this service offer.
        @type type:                  string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """
    def revokeServiceToLan(self, applicationguid, servicename, languid, request="", jobguid="", executionparams=dict()):
        """
        Revokes a service for the lan specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param languid:              guid of the lan to which to revoke the service specified
        @type languid:               guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """


    def offerServiceToCloudUser(self, applicationguid, servicename, clouduserguid, remark="", request="", jobguid="", executionparams=dict()):
        """
        Offers a service for the cloud user specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to add. Name must be unique!
        @type servicename:           string

        @param clouduserguid:        guid of the disk to which to offer the service specified
        @type clouduserguid:         guid

        @param remark:               Remark to add to this service offer.
        @type type:                  string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def revokeServiceToCloudUser(self, applicationguid, servicename, clouduserguid, request="", jobguid="", executionparams=dict()):
        """
        Revokes a service for the cloud user specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param clouduserguid:        guid of the cloud user to which to revoke the service specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def getChildApplications(self, applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Retrieve application template used to create the given application
        
        @execution_method = sync
        
        @param applicationguid:    guid of the parent application
        @type applicationguid:     guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   returncode(True) and dictionary(childinfo) with applicationtemplate guid and applicationtemplate name as result and jobguid: {'result': {'returncode':True, 'childinfo':{'guid':'58aef606-d30c-4ac4-b79c-f2ea955011f9', 'name':'dhcpserver'}, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        """

    
    def addNetworkService(self, applicationguid, name, description="", enabled=True, monitored=True, ipaddressguids=[], request="", jobguid="", executionparams=dict()):
        """
        Adds a new service for the application specified.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param name:                 Name of network service to add. Name must be unique!
        @type name:                  string

        @param description:          Description of network service to add.
        @type description:           string

        @param enabled:              Is this network service enabled.
        @type enabled:               bool

        @param monitored:            Should this network service be monitored.
        @type monitored:             bool

        @param ipaddressguids:       ip addresses linked to this service only, null if not specific to this service, link to guid of ip address as used in machine.
        @type ipaddressguids:        list

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def removeNetworkService(self, applicationguid, servicename, request="", jobguid="", executionparams=dict()):
        """
        Removes a network service for the application specified.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of network service .
        @type servicename:           string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def addNetworkServicePort(self, applicationguid, servicename, portnr, protocoltype="", ipaddress="",  monitor=True, request="", jobguid="", executionparams=dict()):
        """
        Adds a network service port for the application specified.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of network service .
        @type servicename:           string

        @param portnr:               Port of network service .
        @type portnr:                int

        @param protocoltype:         Protocol type (applicationipprotocoltype)
        @type protocoltype:          string

        @param ipaddress:            IP address to which port is bound to
        @type ipaddress:             string

        @param monitor:              Should this port be monitored
        @type monitor:               bool

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def removeNetworkServicePort(self, applicationguid, servicename, portnr, request="", jobguid="", executionparams=dict()):
        """
        Removes a network service port from the application specified.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of network service .
        @type servicename:           string

        @param portnr:               Port of network service .
        @type portnr:                int

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        """

    def listNetworkServices(self,applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Returns a list of network services for an application.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     returncode(True) and Dictionary(networkserviceinfo) of array of network services.
        @rtype:                      dictionary
        @note:                       Example return value:
        @note:                       {'result':{'returncode'=True, 'networkserviceinfo':{'name': 'service1',
        @note:                                   'description': 'service one',
        @note:                                   'monitor': True,
        @note:                                   'enabled': True,
        @note:                                   'ipaddressguids': [],
        @note:                                   'ports':  {'portnr': 25,
        @note:                                              'monitor': True,
        @note:                                              'ipaddress': '192.168.90.1'
        @note:                                              'ipprotocoltype': 'TCP')
        @note:                                 }},
        @note:                        'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                    In case an error occurred, exception is raised
        """


    def getNetworkServicePorts(self, applicationguid, networkservicename, request="", jobguid="", executionparams=dict() ):
        """
        Retrieve information about the networkserviceports for the given application
        
        @execution_method = sync

        @param applicationguid:       guid of the application
        @type applicationguid:        guid
        
        @param networkservicename:    name of the network service
        @type networkservicename:     string
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      returncode(True) and  dictionary(networkserviceports) 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        """
        
    def reload(self, applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Reloads the specified application 

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                  dictionary
        """
    
    def getStatus(self, applicationguid, request="", jobguid="", executionparams=dict()):
        """
        Retrieve status of the given application
        
        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as and status as result and jobguid: {'result': {'returncode':True, 'status':, 'jobguid': guid}
        @rtype:                  dictionary
        """

    def updateACL(self, rootobjectguid, cloudusergroupnames={}, request="", jobguid="", executionparams=dict()):
        """
        Update ACL in a rootobject.
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param cloudusergroupnames:          Dict with keys in the form of cloudusergroupguid_actionname and empty values for now.
        @type cloudusergroupnames:           dict

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """

    def addGroup(self, rootobjectguid, group, action="", recursive=False, request="", jobguid="", executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to add to the specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group gets access to all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is added to all children objects
        @type recursive:                     Boolean 
        
        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def deleteGroup(self, rootobjectguid, group, action="", recursive=False, request="", jobguid="", executionparams=dict()):
        """
        Delete a group in the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to delete for a specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group is deleted from all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is deleted from all children objects
        @type recursive:                     Boolean         

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def hasAccess(self, rootobjectguid, groups, action, request="", jobguid="", executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the selected root object.
        @type rootobjectguid:                guid

        @param groups:                       list of groups to be checked
        @type groups:                        list 

        @param action:                       name of the required action.
        @type action:                        String

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode as result and jobguid: {'result':{returncode:'True'}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """