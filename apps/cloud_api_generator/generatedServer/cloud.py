from pymonkey import q
from cloud_api_rootobjects import cloud_api_cloud
from cloud_api.BaseCloudAPI import BaseCloudAPI

class cloud(BaseCloudAPI):
    def __init__(self):
        self._rootobject = cloud_api_cloud.cloud()

    @q.manage.applicationserver.expose_authenticated
    def getXMLSchema (self, cloudguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the cloud rootobject structure.

        @execution_method = sync
        
        @param cloudguid:        Guid of the cloud rootobject
        @type cloudguid:         guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 XSD representation of the cloud structure.
        @rtype:                  string

        @raise e:                In case an error occurred, exception is raised

        @todo:                   Will be implemented in phase2
        
	"""
	return self._rootobject.getXMLSchema(cloudguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def addDatacenter (self, cloudguid, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        Add a datacenter to which the cloud belongs
        
        @execution_method = sync
        
        @param cloudguid:         Guid of the cloud rootobject
        @type cloudguid:          guid

        @param datacenterguid:    Guid of the datacenter to add
        @type datacenterguid:     guid
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
	return self._rootobject.addDatacenter(cloudguid,datacenterguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def create (self, name, description = "", datacenterguids = [], dns = "", smtp = "", smtplogin = "", smtppassword = "", jobguid = "", executionparams = {}):
        """
        
        Create a new cloud.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the cloud.
        @type name:                    string

        @param description:            Description for the cloud.
        @type description:             string

        @param datacenterguids:        guid of the datacenters to which this cloud belongs, can be a cloud spans multiple datacenters
        @type datacenterguids:         list(guid)

        @param dns:                    dns for this cloud environment.
        @type dns:                     ipaddress
        
        @param smtp:                   Host of the SMTP server to use in this cloud.
        @type smtp:                    string
        
        @param smtplogin:              Login of the SMTP server (if required).
        @type smtplogin:               string
        
        @param smtppassword:           Password of the SMTP server (if required).
        @type smtppassword:            string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with cloudguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
	return self._rootobject.create(name,description,datacenterguids,dns,smtp,smtplogin,smtppassword,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def list (self, cloudguid = "", jobguid = "", executionparams = {}):
        """
        
        List all clouds.

        @execution_method = sync
        
        @param cloudguid:                Guid of the cloud specified
        @type cloudguid:                 guid

        @security administrators
        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with array of cloud info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                          dictionary
        @note:                           {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                           'result: [{ 'cloudguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                       'name': 'cloud0001',
        @note:                                       'description': 'cloud 0001',
        @note:                                       'datacenterguids': '3351FF9F-D65A-4F65-A96B-AC4A6246C033','F353F79F-D65A-4F65-A96B-AC4A6246C033']}]}
        @note:                                     { 'cloudguid': '1351F79F-D65A-4F65-A96B-AC4A6246C033',
        @note:                                       'name': 'cloud0002',
        @note:                                       'description': 'cloud 0002',
        @note:                                       'datacenterguids': ['2351FF9F-D65A-4F65-A96B-AC4A6246C033','7353F79F-D65A-4F65-A96B-AC4A6246C033']}]}
        
        @raise e:                        In case an error occurred, exception is raised
        
	"""
	return self._rootobject.list(cloudguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getYAML (self, cloudguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the cloud rootobject.

        @param cloudguid:             Guid of the cloud rootobject
        @type cloudguid:              guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the cloud
        @rtype:                       string
        
	"""
	return self._rootobject.getYAML(cloudguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the cloud rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        
	"""
	return self._rootobject.getObject(rootobjectguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def deleteDatacenter (self, cloudguid, datacenterguid, jobguid = "", executionparams = {}):
        """
        
        Remove a datacenter to which the cloud belongs

        @execution_method = sync
        
        @param cloudguid:         Guid of the cloud rootobject
        @type cloudguid:          guid

        @param datacenterguid:    Guid of the datacenter to add
        @type datacenterguid:     guid
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary
        
	"""
	return self._rootobject.deleteDatacenter(cloudguid,datacenterguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def updateModelProperties (self, cloudguid, name = "", description = "", datacenterguids = [], dns = "", smtp = "", smtplogin = "", smtppassword = "", installtype = "", installoption = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @security administrators
        @param cloudguid:              Guid of the cloud specified
        @type cloudguid:               guid

        @param name:                   Name for the cloud.
        @type name:                    string

        @param description:            Description for the cloud.
        @type description:             string

        @param datacenterguids:        guid of the datacenters to which this cloud belongs, can be a cloud spans multiple datacenters
        @type datacenterguids:         list(guid)
        
        @param dns:                    IP of the DNS server to use in this cloud.
        @type dns:                     string
        
        @param smtp:                   Host of the SMTP server to use in this cloud.
        @type smtp:                    string
        
        @param smtplogin:              Login of the SMTP server (if required).
        @type smtplogin:               string
        
        @param smtppassword:           Password of the SMTP server (if required).
        @type smtppassword:            string
        
        @param installtype:            DEVELOPMENT / PRODUCTION
        @type installtype:             string
        
        @param installoption:          SSO / MIRRORCLOUD / DAAS
        @type installoption:           string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with cloud guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
	return self._rootobject.updateModelProperties(cloudguid,name,description,datacenterguids,dns,smtp,smtplogin,smtppassword,installtype,installoption,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def listDatacenters (self, cloudguid, jobguid = "", executionparams = {}):
        """
        
        List all related datacenters of the cloud.

        @execution_method = sync
        
        @param cloudguid:               Guid of the cloud rootobject
        @type cloudguid:                guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of cloud info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
	return self._rootobject.listDatacenters(cloudguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authenticated
    def getXML (self, cloudguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the cloud rootobject.

        @execution_method = sync
        
        @param cloudguid:           Guid of the cloud rootobject
        @type cloudguid:            guid

        @param jobguid:             Guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    XML representation of the cloud
        @rtype:                     string

        @raise e:                   In case an error occurred, exception is raised

        @todo:                      Will be implemented in phase2
        
	"""
	return self._rootobject.getXML(cloudguid,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def find (self, name = "", description = "", datacenterguids = "", dns = "", smtp = "", smtplogin = "", smtppassword = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud guids which met the find criteria.

        @security administrators

        @execution_method = sync
        
        @param name:                   Name for the cloud.
        @type name:                    string

        @param description:            Description for the cloud.
        @type description:             string

        @param datacenterguids:        guid of the datacenters to which this cloud belongs, can be a cloud spans multiple datacenters
        @type datacenterguids:         list(guid)

        @param dns:                    IP of the DNS server used in this cloud.
        @type dns:                     string
        
        @param smtp:                   Host of the SMTP server used in this cloud.
        @type smtp:                    string
        
        @param smtplogin:              Login of the SMTP server.
        @type smtplogin:               string
        
        @param smtppassword:           Password of the SMTP server.
        @type smtppassword:            string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Array of cloud guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        
	"""
	return self._rootobject.find(name,description,datacenterguids,dns,smtp,smtplogin,smtppassword,jobguid,executionparams)


    @q.manage.applicationserver.expose_authorized(groups=['administrators'])
    def delete (self, cloudguid, jobguid = "", executionparams = {}):
        """
        
        Delete a cloud.

        @execution_method = sync
        
        @security administrators
        @param cloudguid:             Guid of the cloud rootobject to delete.
        @type cloudguid:              guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
	return self._rootobject.delete(cloudguid,jobguid,executionparams)


