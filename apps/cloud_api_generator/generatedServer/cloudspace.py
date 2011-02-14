from pymonkey import q
from cloud_api_rootobjects import cloud_api_cloudspace
from cloud_api.BaseCloudAPI import BaseCloudAPI

class cloudspace(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_cloudspace.cloudspace()

    @q.manage.applicationserver.expose_authenticated
    def listVdcs (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of vdcs for the cloudspace.

        @execution_method = sync
        
        @param cloudspaceguid:   Guid of the cloudspace specified
        @type cloudspaceguid:    guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of vdcs.
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.listVdcs(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listLans (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of lans for the cloudspace.

        @param cloudspaceguid:   Guid of the cloudspace specified
        @type cloudspaceguid:    guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of lans.
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.listLans(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listApplications (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of applications for the cloudspace.

        @execution_method = sync
        
        @param cloudspaceguid:   Guid of the cloudspace specified
        @type cloudspaceguid:    guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of apllications.
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.listApplications(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXMLSchema (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the cloudspace rootobject structure.

        @execution_method = sync
        
        @param cloudspaceguid:  Guid of the cloudspace rootobject
        @type cloudspaceguid:   guid

        @return:                XSD representation of the disk structure.
        @rtype:                 string

        @raise e:               In case an error occurred, exception is raised

        @todo:                  Will be implemented in phase2
        
	"""
	return self._rootobject.getXMLSchema(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def create (self, customerguid, name, description = "", parentcloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new cloudspace for the given customer.

        @execution_method = sync
        
        @param customerguid:             Guid of the customer to which this cloudspace is assigned.
        @type customerguid:              guid

        @param name:                     Name for the new cloudspace
        @type name:                      string

        @param description:              Description for the new cloudspace
        @type description:               string

        @param parentcloudspaceguid:     Guid of the cloudspace of which this cloudspace is part of.
        @type parentcloudspaceguid:      guid

        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         Dictionary with cloudspaceguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Define security for root spaces
        
	"""
	return self._rootobject.create(customerguid,name,description,parentcloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def list (self, customerguid = "", cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloudspaces for a given customer.

        @execution_method = sync
        
        @param customerguid:     Guid of  the customer for which to retrieve the list of cloudspaces.
        @type customerguid:      guid

        @param cloudspaceguid:   Guid of the cloudspace to delete.
        @type cloudspaceguid:    guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of dictionaries with guid, name and status for each cloudspace.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '[{"guid": "FAD805F7-1F4E-4DB1-8902-F440A59270E6", "name": "cloudspace1", "status": "ACTIVE"},
        @note:                                {"guid": "C4395DA2-BE55-495A-A17E-6A25542CA398", "name": "cloudspace2", "status": "DISABLED"}]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.list(customerguid,cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getYAML (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the cloudspace rootobject.

        @execution_method = sync
        
        @param cloudspaceguid:  Guid of the cloudspace rootobject
        @type cloudspaceguid:   guid

        @return:                YAML representation of the cloudspace
        @rtype:                 string
        
	"""
	return self._rootobject.getYAML(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def setStatus (self, cloudspaceguid, status, jobguid = "", executionparams = {}):
        """
        
        Updates the status of the cloudspace specified.

        @param cloudspaceguid:         Guid of the cloudspace specified
        @type cloudspaceguid:          guid

        @param status:                 Status for the cloudspace specified. See listStatuses() for the list of possible statuses.
        @type status:                  string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
	return self._rootobject.setStatus(cloudspaceguid,status,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    Guid of the lan rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listStatuses (self, jobguid = "", executionparams = {}):
        """
        
        Returns a list of possible cloudspace statuses.

        @execution_method = sync
        
        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of statuses.
        @rtype:                  dictionary
        @note:                   Example return value:
        @note:                   {'result': '["ACTIVE","DISABLED"]',
        @note:                    'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.listStatuses(jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXML (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the cloudspace rootobject.

        @execution_method = sync
        
        @param cloudspaceguid:  Guid of the cloudspace rootobject
        @type cloudspaceguid:   guid

        @return:                XML representation of the cloudspace
        @rtype:                 string

        @raise e:               In case an error occurred, exception is raised

        @todo:                  Will be implemented in phase2
        
	"""
	return self._rootobject.getXML(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listDevices (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of devices for the cloudspace.

        @execution_method = sync
        
        @param cloudspaceguid:   Guid of the cloudspace specified
        @type cloudspaceguid:    guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary of array of devices.
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.listDevices(cloudspaceguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def find (self, customerguid = "", parentcloudspaceguid = "", name = "", status = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloudspace guids which met the find criteria.

        @execution_method = sync
        
        @param customerguid:     		Guid of  the customer to include in the search criteria.
        @type customerguid:      		guid

        @param parentcloudspaceguid:    Guid of the parent cloudspace to include in the search criteria.
        @type parentcloudspaceguid:     guid

        @param name:    				Name of the cloudspace to include in the search criteria.
        @type name:     				string

        @param status:    				Status of the cloudspace to include in the search criteria. See listStatuses().
        @type status:     				string

        @param jobguid:    	        	Guid of the job if avalailable else empty string
        @type jobguid:     	        	guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of cloudspaceguids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
	return self._rootobject.find(customerguid,parentcloudspaceguid,name,status,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def delete (self, cloudspaceguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the given cloudspace.

        @execution_method = sync
        
        @param cloudspaceguid:   Guid of the cloudspace to delete.
        @type cloudspaceguid:    guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
	"""
	return self._rootobject.delete(cloudspaceguid,jobguid,executionparams)


