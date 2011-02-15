from pylabs import q
from cloud_api_rootobjects import cloud_api_customer
from cloud_api.BaseCloudAPI import BaseCloudAPI

class customer(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_customer.customer()

    @q.manage.applicationserver.expose_authenticated
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    Guid of the lan rootobject
        @type rootobjectguid:     guid

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def removeCapacityAvailable (self, customerguid, capacityunittype, jobguid = "", executionparams = {}):
        """
        
        Removes available capacity for the customer specified.

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.removeCapacityAvailable(customerguid,capacityunittype,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listCapacity (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of capacity units available and consumed for the given customer.
        
        @execution_method = sync
        
        @param customerguid:     Guid of the customer for which to retrieve the list of capacity units
        @type customerguid:      guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of dictionaries with customerguid, login, email, firstname, lastname, array of available capacity, array of consumed capacity.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                 "capacityavailable": "[{"amount": "1000",
        @note:                                                         "capacityunittype": "CU",
        @note:                                                         "name": "CPU"
        @note:                                                         "description": "CPU units"},
        @note:                                                        {"amount": "2000",
        @note:                                                         "capacityunittype": "MU",
        @note:                                                         "name": "Memory"
        @note:                                                         "description": "Memory units"}]"}]',
        @note:                                 "capacityconsumed": "[{"amount": "100",
        @note:                                                         "capacityunittype": "CU",
        @note:                                                         "name": "CPU"
        @note:                                                         "description": "CPU units"},
        @note:                                                        {"amount": "200",
        @note:                                                         "capacityunittype": "MU",
        @note:                                                         "name": "Memory"
        @note:                                                         "description": "Memory units"}]"}]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.listCapacity(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def find (self, name = "", status = "", resourcegroupguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of customer guids which meet the search criteria.

        @execution_method = sync
        
        @param name:                    Name of the customer to include in the search criteria.
        @type name:                     string

        @param status:                  Status of the customer to include in the search criteria. See listStatuses().
        @type status:                   string
        
        @param resourcegroupguid:       Guid of the resourcegroup of the customer
        @type resourcegroupguid:        guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of customer guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
	return self._rootobject.find(name,status,resourcegroupguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def unregisterDomain (self, customerguid, username, password, domain, jobguid = "", executionparams = {}):
        """
        
        Unregisters a domain for a customer
        
        @param customerguid       Guid of the customer unregistering the domain
        @type customerguid        guid
        
        @param username           ITPS portal username
        @type username            string
        
        @param password           ITPS portal password
        @type password            string
        
        @param domain             Domain to unregister
        @type domain              string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
	return self._rootobject.unregisterDomain(customerguid,username,password,domain,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def create (self, name, resourcegroupguid = "", description = "", address = "", city = "", country = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new customer

        @execution_method = sync
        
        @param name:                Name for this new customer
        @type name:                 string

        @param resourcegroupguid:   Guid of the resource group related to this customer
        @type resourcegroupguid:    guid

        @param description:         Description for this new customer
        @type description:          string

        @param address:             Address for this new customer
        @type address:              string

        @param city:                City for this new customer
        @type city:                 string

        @param country:             Country for this new customer
        @type country:              string

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with customer guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
	"""
	return self._rootobject.create(name,resourcegroupguid,description,address,city,country,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def setStatus (self, customerguid, status, jobguid = "", executionparams = {}):
        """
        
        Updates the status of the customer specified.

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param status:               Status for the customer specified. See listStatuses() for the list of possible statuses.
        @type status:                string

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.setStatus(customerguid,status,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def updateModelProperties (self, customerguid, name = "", description = "", address = "", city = "", country = "", retentionpolicyguid = "", jobguid = "", executionparams = {}):
        """
        
        Update properties, every parameter which is not passed or passed as empty string is not updated.
        @SECURITY administrator only

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param name:                 Name for this customer
        @type name:                  string

        @param description:          Description for this customer
        @type description:           string

        @param address:              Address for this customer
        @type address:               string

        @param city:                 City for this customer
        @type city:                  string

        @param country:              Country for this customer
        @type country:               string
        
        @param retentionpolicyguid:  Guid of the retention policy for snapshots
        @type retentionpolicyguid:   guid
        
        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with customer guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.updateModelProperties(customerguid,name,description,address,city,country,retentionpolicyguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listCloudSpaces (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloudspaces for the customer.

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     Dictionary of array of cloudspaces.
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
	return self._rootobject.listCloudSpaces(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addCloudUserGroup (self, customerguid, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Adds a cloud user group to the customer specified.

        @execution_method = sync
        
        @param customerguid:         Gui of the customer specified
        @type customerguid:          guid

        @param cloudusergroupguid:   Guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.addCloudUserGroup(customerguid,cloudusergroupguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def registerDomain (self, customerguid, username, password, domain, jobguid = "", executionparams = {}):
        """
        
        Registers a domain for a customer
        
        @param customerguid       Guid of the customer registering the domain
        @type customerguid        guid
        
        @param username           ITPS portal username
        @type username            string
        
        @param password           ITPS portal password
        @type password            string
        
        @param domain             Domain to register
        @type domain              string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
	return self._rootobject.registerDomain(customerguid,username,password,domain,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listGroups (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user groups for a given customer.
        
        @execution_method = sync
        
        @param customerguid:     Guid of the customer for which to retrieve the list of groups to which this user belongs.
        @type customerguid:      guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of dictionaries with customerguid, login, email, firstname, lastname, cloudusergroupguid, name, description.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                 "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                              "name": "admins",
        @note:                                              "description": "Cloud Administrators"},
        @note:                                             {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                              "name": "users",
        @note:                                              "description": "customers"}]"}]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.listGroups(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def removeCloudUserGroup (self, customerguid, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Removes a cloud user group for the customer specified.

        @execution_method = sync
        
        @param customerguid:         Gui of the customer specified
        @type customerguid:          guid

        @param cloudusergroupguid:   Guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.removeCloudUserGroup(customerguid,cloudusergroupguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXML (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the customer rootobject.

        @execution_method = sync
        
        @param customerguid:            Guid of the customer rootobject
        @type customerguid:             guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid


        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the customer
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
	return self._rootobject.getXML(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def removeCapacityConsumed (self, customerguid, capacityunittype, jobguid = "", executionparams = {}):
        """
        
        Removes consumed capacity for the customer specified.

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param capacityunittype:     Type of capacity units to remove. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.removeCapacityConsumed(customerguid,capacityunittype,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addCapacityConsumed (self, customerguid, amount, capacityunittype, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Adds consumed capacity for the customer specified.

        @execution_method = sync
        
        @param customerguid:         Guid of the customer specified
        @type customerguid:          guid

        @param amount:               Amount of capacity units to add
        @type amount:                integer

        @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param name:                 Name of capacity units to add.
        @type name:                  string

        @param description:          Description of capacity units to add.
        @type type:                  string

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.addCapacityConsumed(customerguid,amount,capacityunittype,name,description,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addCapacityAvailable (self, customerguid, amount, capacityunittype, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Adds available capacity for the customer specified.

        @execution_method = sync
        
        @param customerguid:         Gui of the customer specified
        @type customerguid:          guid

        @param amount:               Amount of capacity units to add
        @type amount:                integer

        @param capacityunittype:     Type of capacity units to add. See capacityplanning.listCapacityUnitTypes()
        @type capacityunittype:      string

        @param name:                 Name of capacity units to add.
        @type name:                  string

        @param description:          Description of capacity units to add.
        @type type:                  string

        @param jobguid:              Guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
	return self._rootobject.addCapacityAvailable(customerguid,amount,capacityunittype,name,description,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXMLSchema (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the customer rootobject structure.

        @execution_method = sync
        
        @param customerguid:             Guid of the customer rootobject
        @type customerguid:              guid

        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XSD representation of the customer structure.
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
	"""
	return self._rootobject.getXMLSchema(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def list (self, customerguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of customers.
        @SECURITY administrator only

        @execution_method = sync
        
        @param customerguid:     Guid of the customer specified
        @type customerguid:      guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of dictionaries with guid, name, description, address, city, country and status for customer.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "Customer1", "description": "My first customer", "address": "Main road", "city": "Bombai", "country":"India" , "status": "ACTIVE"},
        @note:                                {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "name": "Customer2", "description": "My second customer", "address": "Antwerpsesteenweg", "city": "Lochristi", "country":"Belgium" , "status": "DISABLED"}]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.list(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getYAML (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the customer rootobject.

        @execution_method = sync
        
        @param customerguid:             Guid of the customer rootobject
        @type customerguid:              guid

        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         YAML representation of the customer
        @rtype:                          string
        
	"""
	return self._rootobject.getYAML(customerguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listStatuses (self, jobguid = "", executionparams = {}):
        """
        
        Returns a list of possible customer statuses.

        @execution_method = sync
        
        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of statuses.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '["ACTIVE", "CONFIGURED", "DISABLED"]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.listStatuses(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def delete (self, customerguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the customer specified.

        @execution_method = sync
        
        @param customerguid:             Guid of the customer to delete.
        @type customerguid:              guid

        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
	"""
	return self._rootobject.delete(customerguid,jobguid,executionparams)


