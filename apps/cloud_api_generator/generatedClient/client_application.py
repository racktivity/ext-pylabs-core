from cloud_api_client.Exceptions import CloudApiException

class application:
    def __init__(self, proxy):
        self._proxy = proxy


    def listVdcs (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        List the vdcs the application is used in.

        @execution_method = sync

        @param applicationguid:   guid of the application to list the vdcs for.
        @type applicationguid:    guid

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary of array of dictionaries with guid, name, description, status, template, applicationtemplateguid, machineguid, machinename, cloudspaceguid, cloudspacename of the application.
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.listVdcs(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def restore (self, sourceapplicationguid, destinationapplicationguid = "", jobguid = "", executionparams = {}):
        """
        
        @param sourceapplicationguid is the application which is in backedup state in drp
        
        @param destinationapplicationguid is application where will be restored to if not specified will be the original application where the backup originated from
        
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @todo:                   Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.restore(sourceapplicationguid,destinationapplicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def removeNetworkService (self, applicationguid, servicename, jobguid = "", executionparams = {}):
        """
        
        Removes a network service for the application specified.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of network service .
        @type servicename:           string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.removeNetworkService(applicationguid,servicename,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def removeService (self, applicationguid, servicename, jobguid = "", executionparams = {}):
        """
        
        Removes a service for the application specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service .
        @type servicename:           string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.removeService(applicationguid,servicename,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def exists (self, templatename = "", machineguid = "", customer = "", jobguid = "", executionparams = {}):
        """
        
        Returns a dict with following key/value pairs: templateguid, applicationguid, machineguid
        which met the find criteria.

        @param templatename:          name of the parent template to include in the search criteria.
        @type templatename:           string

        @param machineguid:           guid of the machine to include in the search criteria.
        @type machineguid:            guid
        
        @param customer:              Flag whether the application is system or customer application
        @type customer:               boolean

        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      Dict of which met the find criteria specified.
        @rtype:                       array

        @raise e:                     In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.exists(templatename,machineguid,customer,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def revokeServiceToDevice (self, applicationguid, servicename, deviceguid, jobguid = "", executionparams = {}):
        """
        
        Revokes a service for the device specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param deviceguid:           guid of the device to which to revoke the service specified
        @type deviceguid:            guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.revokeServiceToDevice(applicationguid,servicename,deviceguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listAccountTypes (self, jobguid = "", executionparams = {}):
        """
        
        Returns a list of possible application account types.

        @execution_method = sync

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of application account types.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '["PUBLICACCOUNT", "SYSTEMACCOUNT"]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.listAccountTypes(jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listMonitoringInfo (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Retrieve application monitoring info used for the given machine

        @execution_method = sync

        @param machineguid:        guid of the machineguid running the application
        @type machineguid:         guid

        @param jobguid:            guid of the job if available else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with  application, port, ipaddress
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.listMonitoringInfo(machineguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getChildApplications (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Retrieve application template used to create the given application
        
        @execution_method = sync
        
        @param applicationguid:    guid of the parent application
        @type applicationguid:     guid

        @param jobguid:            guid of the job if available else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with applicationtemplate guid and applicationtemplate name as result and jobguid: {'result': {'guid':'58aef606-d30c-4ac4-b79c-f2ea955011f9', 'name':'dhcpserver'}, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.getChildApplications(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync

        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_application.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['application'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def initialize (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Performs initialization actions on the application specified. As a result the application will be ready to be used.
        @security administrators

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.initialize(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def revokeServiceToNetworkZone (self, applicationguid, servicename, networkzoneguid, jobguid = "", executionparams = {}):
        """
        
        Revokes a service for the network zone specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param networkzoneguid:      guid of the network zone to which to revoke the service specified
        @type networkzoneguid:       guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.revokeServiceToNetworkZone(applicationguid,servicename,networkzoneguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addCapacityProvided (self, applicationguid, amount, capacityunittype, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Adds provided capacity for the application specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param amount:               Amount of capacity units to add
        @type amount:                integer

        @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param name:                 Name of capacity units to add.
        @type name:                  string

        @param description:          Description of capacity units to add.
        @type type:                  string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.addCapacityProvided(applicationguid,amount,capacityunittype,name,description,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addAccount (self, applicationguid, login, password, accounttype, jobguid = "", executionparams = {}):
        """
        
        Adds an account for the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param login:                    Login for the new  account.
        @type login:                     string

        @param password:                 Password for the new account.
        @type password:                  string

        @param accounttype:              Type for the new account. See listAccountTypes().
        @type accounttype:               string

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.addAccount(applicationguid,login,password,accounttype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, cloudspaceguid = "", machineguid = "", name = "", status = "", istemplate = False, customer = "", mode = "", monitor = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of application guids which met the find criteria.

        @execution_method = sync

        @param cloudspaceguid:          Guid of the cloudspace to include in the search criteria.
        @type cloudspaceguid:           guid

        @param machineguid:             Guid of the machine to include in the search criteria.
        @type machineguid:              guid

        @param name:                    Name of the application to include in the search criteria.
        @type name:                     string

        @param status:                  Status of the  application to include in the search criteria. See listStatuses().
        @type status:                   string

        @param istemplate:              Indicate if the application is a template
        @type istemplate:               boolean

        @param customer:                Flag whether the application is system or customer application
        @type customer:                 boolean
        
        @param mode:                    Mode of the application (eg readonly...)
        @type mode:                     string
        
        @param monitor:                 Monitor flag
        @type monitor:                  boolean
        
        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of application guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.find(cloudspaceguid,machineguid,name,status,istemplate,customer,mode,monitor,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def offerServiceToApplication (self, applicationguid, servicename, destinationapplicationguid, remark = "", jobguid = "", executionparams = {}):
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

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.offerServiceToApplication(applicationguid,servicename,destinationapplicationguid,remark,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def createFromTemplate (self, cloudspaceguid, machineguid, applicationtemplateguid, name, description = "", customsettings = "", customer = False, jobguid = "", executionparams = {}):
        """
        
        Creates a new application, does not provision application yet

        @param cloudspaceguid:                   guid of the cloud space related to this application
        @type cloudspaceguid:                    guid

        @param machineguid:                      guid of the machine related to this application
        @type machineguid:                       guid

        @param applicationtemplateguid:          guid of the applicationtemplate to create this application from
        @type applicationtemplateguid:           guid

        @param name:                             Name for this new application. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                              string

        @param description:                      Description for this new application. This is free text describing the purpose of the application, if multi-line use back-slash + 

        @type description:                       string

        @param customsettings:                   Custom settings for this new application.
        @type customsettings:                    string
        
        @param customer:                         Flag whether the application is system or customer application
        @type customer:                          boolean

        @param jobguid:                          guid of the job if available else empty string
        @type jobguid:                           guid

        @param executionparams:                  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:                   dictionary

        @return:                                 dictionary with application guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                                  dictionary

        @raise e:                                In case an error occurred, exception is raised
        remark:                                  An application always lives on top of a machine, the machine also lives in a space, think is good to have both a reference to space
        
        """
        try:
            result = self._proxy.cloud_api_application.createFromTemplate(cloudspaceguid,machineguid,applicationtemplateguid,name,description,customsettings,customer,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def copy (self, sourceapplicationguid, destinationapplicationguid, jobguid = "", executionparams = {}):
        """
        
        Copies the application specified.

        @param sourceapplicationguid:            guid of the application to copy.
        @type sourceapplicationguid:             guid

        @param destinationapplicationguid:       guid of the target application.
        @type destinationapplicationguid:        guid

        @param jobguid:                          guid of the job if available else empty string
        @type jobguid:                           guid

        @param executionparams:                  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:                   dictionary

        @return:                                 dictionary with the guid of the new application as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                                  dictionary

        @raise e:                                In case an error occurred, exception is raised
        
        @todo:                                   Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.copy(sourceapplicationguid,destinationapplicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def offerServiceToDevice (self, applicationguid, servicename, deviceguid, remark = "", jobguid = "", executionparams = {}):
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

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.offerServiceToDevice(applicationguid,servicename,deviceguid,remark,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


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
        try:
            result = self._proxy.cloud_api_application.reload(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def removeCapacityProvided (self, applicationguid, capacityunittype, jobguid = "", executionparams = {}):
        """
        
        Removes provided capacity for the application specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.removeCapacityProvided(applicationguid,capacityunittype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, cloudspaceguid, name, machineguid = "", parentapplicactionguid = "", description = "", customsettings = "", customer = False, mode = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new application, does not provision application yet
        Application does not have to be linked to a machine.
        An application can group other applications, these are called cloudservices

        @param cloudspaceguid:         guid of the cloud space related to this application
        @type cloudspaceguid:          guid

        @param machineguid:            guid of the machine related to this application
        @type machineguid:             guid

        @param name:                   Name for this new application. The name is a freely chosen name, which has to be unique in SPACE.
        @type name:                    string

        @param description:            Description for this new application. This is free text describing the purpose of the application, if multi-line use back-slash + 

        @type description:             string

        @param customsettings:         Custom settings for this new application.
        @type customsettings:          string

        @param parentapplicactionguid: link to application which is cloudservice (modelled as parent application)
        @type parentapplicactionguid:  guid
        
        @param customer:               Flag whether the application is system or customer application
        @type customer:                boolean
        
        @param mode:                   configuration mode (READONLY,READWRITE...)
        @type mode:                    string

        @param jobguid:                guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with application guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        remark:                        An application always lives on top of a machine, the machine also lives in a space, think is good to have both a reference to space
        
        """
        try:
            result = self._proxy.cloud_api_application.create(cloudspaceguid,name,machineguid,parentapplicactionguid,description,customsettings,customer,mode,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getStatus (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Retrieve status of the given application
        
        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
        """
        try:
            result = self._proxy.cloud_api_application.getStatus(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def revokeServiceToCloudUser (self, applicationguid, servicename, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Revokes a service for the cloud user specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param clouduserguid:        guid of the cloud user to which to revoke the service specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.revokeServiceToCloudUser(applicationguid,servicename,clouduserguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def start (self, applicationguid, failifnotenoughresource = False, jobguid = "", executionparams = {}):
        """
        
        Starts the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param failifnotenoughresource:  Boolean value indicating if application should not start if not enough resources are available.
        @type failifnotenoughresource:   boolean

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.start(applicationguid,failifnotenoughresource,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, applicationguid, name = "", description = "", status = "", customsettings = "", customer = "", mode = "", monitor = "", jobguid = "", executionparams = {}):
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
        
        @param customer:             Flag whether the application is system or customer application
        @type customer:              boolean

        @param mode:                 Mode of the application (eg readonly...)
        @type mode:                  string
        
        @param monitor:              Monitor flag
        @type monitor:               boolean

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with application guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.updateModelProperties(applicationguid,name,description,status,customsettings,customer,mode,monitor,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def revokeServiceToDisk (self, applicationguid, servicename, diskguid, jobguid = "", executionparams = {}):
        """
        
        Revokes a service for the disk specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param diskguid:             guid of the disk to which to revoke the service specified
        @type diskguid:              guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.revokeServiceToDisk(applicationguid,servicename,diskguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getApplicationTemplate (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Retrieve application template used to create the given application

        @param applicationguid:      guid of the application
        @type applicationguid:       guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with applicationtemplate guid and applicationtemplate name as result and jobguid: {'result': {'guid':'58aef606-d30c-4ac4-b79c-f2ea955011f9', 'name':'dhcpserver'}, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.getApplicationTemplate(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def offerServiceToLan (self, applicationguid, servicename, languid, remark = "", jobguid = "", executionparams = {}):
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

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.offerServiceToLan(applicationguid,servicename,languid,remark,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def offerServiceToMachine (self, applicationguid, servicename, machineguid, remark = "", jobguid = "", executionparams = {}):
        """
        
        Offers a service for machine lan specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to add. Name must be unique!
        @type servicename:           string

        @param machineguid:          guid of the machine to which to offer the service specified
        @type machineguid:           guid

        @param remark:               Remark to add to this service offer.
        @type type:                  string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.offerServiceToMachine(applicationguid,servicename,machineguid,remark,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getNetworkServicePorts (self, applicationguid, networkservicename, jobguid = "", executionparams = {}):
        """
        
        Retrieve information about the networkserviceports for the given application
        
        @execution_method = sync

        @param applicationguid:       guid of the application
        @type applicationguid:        guid
        
        @param networkservicename:    name of the network service
        @type networkservicename:     string
        
        @param jobguid:               guid of the job if available else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.getNetworkServicePorts(applicationguid,networkservicename,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def moveToMachine (self, applicationguid, machineguid, jobguid = "", executionparams = {}):
        """
        
        Copies the application specified.

        @param applicationguid:                  guid of the application to move.
        @type applicationguid:                   guid

        @param machineguid:                      guid of the machine to which we want to move this application.
        @type machineguid:                       guid

        @param jobguid:                          guid of the job if available else empty string
        @type jobguid:                           guid

        @param executionparams:                  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:                   dictionary

        @return:                                 dictionary with the True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                                  dictionary

        @raise e:                                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.moveToMachine(applicationguid,machineguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def offerServiceToCloudUser (self, applicationguid, servicename, clouduserguid, remark = "", jobguid = "", executionparams = {}):
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

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.offerServiceToCloudUser(applicationguid,servicename,clouduserguid,remark,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addNetworkService (self, applicationguid, name, description = "", enabled = True, monitored = True, ipaddressguids = [], jobguid = "", executionparams = {}):
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

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.addNetworkService(applicationguid,name,description,enabled,monitored,ipaddressguids,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def stop (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Stops the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.stop(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def removeAccount (self, applicationguid, login, accounttype, jobguid = "", executionparams = {}):
        """
        
        Removes an account for the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param login:                    Login of the account to remove.
        @type login:                     string

        @param accouttype:               Type of the account to remove. See listAccountTypes().
        @type accouttype:                string

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.removeAccount(applicationguid,login,accounttype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def disable (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Disables the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.disable(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addService (self, applicationguid, name, description = "", jobguid = "", executionparams = {}):
        """
        
        Adds a new service for the application specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param name:                 Name of service to add. Name must be unique!
        @type name:                  string

        @param description:          Description of service to add.
        @type type:                  string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.addService(applicationguid,name,description,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the application rootobject.

        @execution_method = sync

        @param applicationguid:   guid of the lan rootobject
        @type applicationguid:    guid

        @return:                  XML representation of the lan
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised

        @todo:                    Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.getXML(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def importFromURI (self, applicationguid, sourceuri, executormachineguid = "", jobguid = "", executionparams = {}):
        """
        
        Imports an application from the source location specified.
        Export rootobject info

        @param applicationguid:            guid of the application to export.
        @type applicationguid:             guid

        @param sourceuri:                  URI of the location holding an exported application. (e.g ftp://login:passwd@myhost.com/backups/apache/)
        @type sourceuri:                   string

        @param executormachineguid:        guid of the machine which should convert the application to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:         guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.importFromURI(applicationguid,sourceuri,executormachineguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getAgentsForCloudService (self, cloudservicename, applicationtype = "", jobguid = "", executionparams = {}):
        """
        
        return guids of agents off applications of cloudservice (when applicatyupename is specified only one specific applicationtype part of cloudservice)
        e.g. getAgentsForCloudServiceApplication("dsssstore","storagedaemon") will return a list of all storagedaemonAgents
        
        @param applicationtype:       Specified application needs to be linked to a template with specified name (as string)
        
        @todo:                        Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.getAgentsForCloudService(cloudservicename,applicationtype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def revokeServiceToApplication (self, applicationguid, servicename, destinationapplicationguid, jobguid = "", executionparams = {}):
        """
        
        Revokes a service for the application specified.

        @param applicationguid:            guid of the application specified
        @type applicationguid:             guid

        @param servicename:                Name of service to revoke. Name must be unique!
        @type servicename:                 string

        @param destinationapplicationguid: guid of the application to which to revoke the service specified
        @type destinationapplicationguid:  guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.revokeServiceToApplication(applicationguid,servicename,destinationapplicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def restart (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Restart the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.restart(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listNetworkServices (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of network services for an application.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     Dictionary of array of network services.
        @rtype:                      dictionary
        @note:                       Example return value:
        @note:                       {'result': {'name': 'service1',
        @note:                                   'description': 'service one',
        @note:                                   'monitor': True,
        @note:                                   'enabled': True,
        @note:                                   'ipaddressguids': [],
        @note:                                   'ports':  {'portnr': 25,
        @note:                                              'monitor': True,
        @note:                                              'ipaddress': '192.168.90.1'
        @note:                                              'ipprotocoltype': 'TCP')
        @note:                                 },
        @note:                        'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.listNetworkServices(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def removeCapacityConsumed (self, applicationguid, capacityunittype, jobguid = "", executionparams = {}):
        """
        
        Removes consumed capacity for the customer specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.removeCapacityConsumed(applicationguid,capacityunittype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addCapacityConsumed (self, applicationguid, amount, capacityunittype, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Adds consumed capacity for the application specified.

        @param applicationguid:      guid of the customer specified
        @type applicationguid:       guid

        @param amount:               Amount of capacity units to add
        @type amount:                integer

        @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param name:                 Name of capacity units to add.
        @type name:                  string

        @param description:          Description of capacity units to add.
        @type type:                  string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.addCapacityConsumed(applicationguid,amount,capacityunittype,name,description,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


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
        try:
            result = self._proxy.cloud_api_application.uninstall(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def addNetworkServicePort (self, applicationguid, servicename, portnr, protocoltype = "", ipaddress = "", monitor = True, jobguid = "", executionparams = {}):
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

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.addNetworkServicePort(applicationguid,servicename,portnr,protocoltype,ipaddress,monitor,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getAgentForApplicationTypeService (self, machineguid, applicationtype, jobguid = "", executionparams = {}):
        """
        
        return guid of agent which serves specified applicationtype to this machine
        e.g. getAgentForService([machineguid of a machine],"dssdirector") will return the agent of the dssdirector
        
        @todo:                        Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.getAgentForApplicationTypeService(machineguid,applicationtype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def exportToURI (self, applicationguid, destinationuri, executormachineguid = "", compressed = True, imagetype = "vdi", jobguid = "", executionparams = {}):
        """
        
        Exports specified application (is a backup) to a remote destination.
        These are very application specific workflows
        Export rootobject info

        @param applicationguid:            guid of the application to export.
        @type applicationguid:             guid

        @param destinationuri:             URI of the location where the application should be stored. (e.g ftp://login:passwd@myhost.com/backups/apache/)
        @type destinationuri:              string

        @param executormachineguid:        guid of the machine which should convert the application to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:         guid

        @param compressed                  Boolean value indicating if the export should be compressed. Compression used is 7zip
        @type:                             boolean

        @param imagetype                   Type of image format to use.
        @type:                             string
        @note:                             Supported export formats are : "vdi", "parallels", "qcow2", "vvfat", "vpc", "bochs", "dmg", "cloop", "vmdk", "qcow", "cow", "host_device", "raw"

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @todo:                             Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.exportToURI(applicationguid,destinationuri,executormachineguid,compressed,imagetype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, cloudspaceguid = "", machineguid = "", applicationguid = "", status = "", customer = "", istemplate = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of applications.
        @question shouldn't there be at least some filter criteria, this is always going to be a useless result (too long) e.g. vmachineguid="",customerguid="", ... most common filter criteria, this should be main criteria for views, the filter criteria should be like find, but directly exposes views
        @SECURITY administrator only

        @execution_method = sync

        @param cloudspaceguid:    guid of the cloudspace if available else empty string
        @type cloudspaceguid:     guid

        @param machineguid:       guid of the application if available else empty string
        @type machineguid:        guid

        @param applicationguid:   guid of the application if available else empty string
        @type applicationguid:    guid

        @param status:            status of the application to include in the search criteria.
        @type status:             string
        
        @param customer:          Flag whether the application is system or customer application
        @type customer:           boolean

        @param istemplate:        Flag whether the application is template application
        @type istemplate:         boolean

        @param jobguid:           guid of the job if available else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  Dictionary of array of dictionaries with guid, name, description, status, template, applicationtemplateguid, machineguid, machinename, cloudspaceguid, cloudspacename of the application.
        @rtype:                   dictionary
        @note:                    Example return value:
        @note:                    {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "DSSDirector", "description": "DSS Director", "status": "ACTIVE", "template": "False", "applicationtemplateguid": "", "machineguid": "0D735CB9-8376-456C-827E-31CAC8815894", "machinename": "appliance1", "cloudspaceguid": "0D58B3BE-6C46-4450-954C-4BFFAF1E38C4", "cloudspacename": "Administrator space"},
        @note:                                {"guid": "D48CCFB4-207D-469F-8DA8-471304C3CCA7", "name": "DSSVolumeDriver", "description": "DSS Volumedriver", "status": "ACTIVE", "template": "False", "applicationtemplateguid": "", "machineguid": "0D735CB9-8376-456C-827E-31CAC8815894", "machinename": "appliance1", "cloudspaceguid": "0D58B3BE-6C46-4450-954C-4BFFAF1E38C4", "cloudspacename": "Administrator space"}]',
        @note:                     'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                 In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.list(cloudspaceguid,machineguid,applicationguid,status,customer,istemplate,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def offerServiceToNetworkZone (self, applicationguid, servicename, networkzoneguid, remark = "", jobguid = "", executionparams = {}):
        """
        
        Offers a service for the network zone specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to add. Name must be unique!
        @type servicename:           string

        @param networkzoneguid:      guid of the network zone to which to offer the service specified
        @type networkzoneguid:       guid

        @param remark:               Remark to add to this service offer.
        @type type:                  string

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.offerServiceToNetworkZone(applicationguid,servicename,networkzoneguid,remark,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the application rootobject.

        @execution_method = sync

        @param applicationguid:   guid of the lan rootobject
        @type applicationguid:    guid

        @return:                  YAML representation of the disk
        @rtype:                   string
        
        """
        try:
            result = self._proxy.cloud_api_application.getYAML(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def revokeServiceToMachine (self, applicationguid, servicename, machineguid, jobguid = "", executionparams = {}):
        """
        
        Revokes a service for the machine specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param machineguid:          guid of the machine to which to revoke the service specified
        @type machineguid:           guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.revokeServiceToMachine(applicationguid,servicename,machineguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXMLSchema (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the application rootobject structure.

        @execution_method = sync

        @param applicationguid:   guid of the lan rootobject
        @type applicationguid:    guid

        @return:                  XSD representation of the disk structure.
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised

        @todo:                    Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_application.getXMLSchema(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def listStatuses (self, jobguid = "", executionparams = {}):
        """
        
        Returns a list of possible application statuses.

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of statuses.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '["ACTIVE", "DISABLED", "MAINTENANCE"]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        
        @raise e:                In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.listStatuses(jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def revokeServiceToLan (self, applicationguid, servicename, languid, jobguid = "", executionparams = {}):
        """
        
        Revokes a service for the lan specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to revoke. Name must be unique!
        @type servicename:           string

        @param languid:              guid of the lan to which to revoke the service specified
        @type languid:               guid

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.revokeServiceToLan(applicationguid,servicename,languid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def offerServiceToDisk (self, applicationguid, servicename, diskguid, remark = "", partitionorder = "", jobguid = "", executionparams = {}):
        """
        
        Offers a service for the disk specified.

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of service to add. Name must be unique!
        @type servicename:           string

        @param diskguid:             guid of the disk to which to offer the service specified
        @type diskguid:              guid

        @param remark:               Remark to add to this service offer.
        @type remark:                string
    
        @param partitionorder:       number of partition serviced (eg mountpoints)
        @type partitionorder:        int

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.offerServiceToDisk(applicationguid,servicename,diskguid,remark,partitionorder,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getAgent (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        return guid of agent which serves the specified application (which is NOT part of cloudservice)
        
        """
        try:
            result = self._proxy.cloud_api_application.getAgent(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def backup (self, applicationguid, destinationuri = "", compressed = True, login = "", password = "", jobguid = "", executionparams = {}):
        """
        
        Creates a backup of the application (when needed a destination can be given)

        @param applicationguid:  Guid of the application
        @type applicationguid:   guid

        @param destinationuri:   URI of the location where the backup should be stored. (e.g ftp://login:passwd@myhost.com/backups/applicationx/).
                                 If no password and login are passed, default credentials will be used
        
        @type destinationuri:    string

        @param compressed:       If true backup will be zipped (compression = 7zip)
        @type compressed:        boolean

        @param login:            Login credential on the destination machine
        @type login:             string
        
        @param password:         Password on the destination machine
        @type password:          string
        
        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        
        """
        try:
            result = self._proxy.cloud_api_application.backup(applicationguid,destinationuri,compressed,login,password,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def removeNetworkServicePort (self, applicationguid, servicename, portnr, jobguid = "", executionparams = {}):
        """
        
        Removes a network service port from the application specified.

        @execution_method = sync

        @param applicationguid:      guid of the application specified
        @type applicationguid:       guid

        @param servicename:          Name of network service .
        @type servicename:           string

        @param portnr:               Port of network service .
        @type portnr:                int

        @param jobguid:              guid of the job if available else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.removeNetworkServicePort(applicationguid,servicename,portnr,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the application specified.

        @param applicationguid:          guid of the application to delete.
        @type applicationguid:           guid

        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_application.delete(applicationguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



