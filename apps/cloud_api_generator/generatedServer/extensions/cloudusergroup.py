from cloud_api_rootobjects import cloud_api_cloudusergroup

class cloudusergroup:

    def __init__(self):
        self._rootobject = cloud_api_cloudusergroup.cloudusergroup()

    def listGroups (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user groups which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid: guid of the cloud user group specified
        @type cloudusergroupguid:  guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listGroups(cloudusergroupguid,jobguid,executionparams)
        return result


    def getXMLSchema (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the cloud user group rootobject structure.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group rootobject
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XSD representation of the cloud user group structure.
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
        """
        result = self._rootobject.getXMLSchema(cloudusergroupguid,jobguid,executionparams)
        return result


    def addUser (self, cloudusergroupguid, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Add an existing cloud user to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param clouduserguid:        Gui of the cloud user to add to the cloud user group specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addUser(cloudusergroupguid,clouduserguid,jobguid,executionparams)
        return result


    def create (self, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new cloud user group
        
        @execution_method = sync
        
        @param name:                Name for this new cloud user group
        @type name:                 string

        @param description:         Description for this new cloud user group
        @type description:          string

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    dictionary with cloud user group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.create(name,description,jobguid,executionparams)
        return result


    def removeUserRole (self, cloudusergroupguid, clouduserroleguid, jobguid = "", executionparams = {}):
        """
        
        Remove an existing cloud user role from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param clouduserroleguid:            Guid of the cloud user role who should be removed from the cloud user group specified
        @type clouduserroleguid:             guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.removeUserRole(cloudusergroupguid,clouduserroleguid,jobguid,executionparams)
        return result


    def list (self, customerguid = "", cloudusergroupguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user groups which are related to the customer specified.

        @execution_method = sync
        
        @param customerguid:         guid of the customer for which to retrieve the list of cloud user groups.
        @type customerguid:          guid

        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                      dictionary
        @note:                       Example return value:
        @note:                       {'result': '[{"customerguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                     "groups": "[{"cloudusergroupguid": "C4395DA2-BE55-495A-A17E-6A25542CA398",
        @note:                                                  "name": "admins",
        @note:                                                  "description": "Cloud Administrators"},
        @note:                                                 {"cloudusergroupguid": "22544B07-4129-47B1-8690-B92C0DB21434",
        @note:                                                  "name": "users",
        @note:                                                  "description": "cloud user groups"}]"}]',
        @note:                        'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                    In case an error occurred, exception is raised
        
        """
        result = self._rootobject.list(customerguid,cloudusergroupguid,jobguid,executionparams)
        return result


    def removeGroup (self, cloudusergroupguid, membercloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Remove an existing cloud user group from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param membercloudusergroupguid:     Guid of the cloud user group who should be removed from the cloud user group specified
        @type membercloudusergroupguid:      guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.removeGroup(cloudusergroupguid,membercloudusergroupguid,jobguid,executionparams)
        return result


    def getYAML (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the cloud user group rootobject.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group rootobject
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         YAML representation of the cloud user group
        @rtype:                          string
        
        """
        result = self._rootobject.getYAML(cloudusergroupguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.getObject(rootobjectguid,jobguid,executionparams)

        from osis import ROOTOBJECT_TYPES
        import base64
        from osis.model.serializers import ThriftSerializer
        result = base64.decodestring(result['result'])
        result = ROOTOBJECT_TYPES['cloudusergroup'].deserialize(ThriftSerializer, result)
        return result


    def listUsers (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud users which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid:  guid of the cloud user group specified
        @type cloudusergroupguid:   guid

        @param jobguid:             guid of the job if avalailable else empty string
        @type jobguid:              guid

        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                     dictionary

        @raise e:                   In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listUsers(cloudusergroupguid,jobguid,executionparams)
        return result


    def listRoles (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user roles of the cloud user group

        @execution_method = sync
        
        @param cloudusergroupguid: guid of the cloud user group specified
        @type cloudusergroupguid:  guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   Dictionary of array of dictionaries with an array of cloud user roles with cloudusergroupguid
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
        """
        result = self._rootobject.listRoles(cloudusergroupguid,jobguid,executionparams)
        return result


    def removeUser (self, cloudusergroupguid, clouduserguid, jobguid = "", executionparams = {}):
        """
        
        Remove an existing cloud user from the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param clouduserguid:        Gui of the cloud user to remove from the cloud user group specified
        @type clouduserguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        result = self._rootobject.removeUser(cloudusergroupguid,clouduserguid,jobguid,executionparams)
        return result


    def updateModelProperties (self, cloudusergroupguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties, every parameter which is not passed or passed as empty string is not updated.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param name:                 Name for this cloud user group
        @type name:                  string

        @param description:          Description for this cloud user group
        @type description:           string

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with cloud user group guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        """
        result = self._rootobject.updateModelProperties(cloudusergroupguid,name,description,jobguid,executionparams)
        return result


    def listCustomers (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud users which are member of the given cloud user group.

        @execution_method = sync
        
        @param cloudusergroupguid:   guid of the cloud user group specified
        @type cloudusergroupguid:    guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     Dictionary of array of dictionaries with customerguid, and an array of cloud user groups with cloudusergroupguid, name, description.
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
        """
        result = self._rootobject.listCustomers(cloudusergroupguid,jobguid,executionparams)
        return result


    def addGroup (self, cloudusergroupguid, membercloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Add an existing cloud user group to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param membercloudusergroupguid:     Guid of the cloud user group who should become a member of the cloud user group specified
        @type membercloudusergroupguid:      guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addGroup(cloudusergroupguid,membercloudusergroupguid,jobguid,executionparams)
        return result


    def getXML (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the cloud user group rootobject.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group rootobject
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         XML representation of the cloud user group
        @rtype:                          string

        @raise e:                        In case an error occurred, exception is raised

        @todo:                           Will be implemented in phase2
        
        """
        result = self._rootobject.getXML(cloudusergroupguid,jobguid,executionparams)
        return result


    def addUserRole (self, cloudusergroupguid, clouduserroleguid, jobguid = "", executionparams = {}):
        """
        
        Add an existing cloud user role to the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:           guid of the cloud user group specified
        @type cloudusergroupguid:            guid

        @param clouduserroleguid:            Guid of the cloud user role
        @type clouduserroleguid:             guid

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        
        """
        result = self._rootobject.addUserRole(cloudusergroupguid,clouduserroleguid,jobguid,executionparams)
        return result


    def find (self, name = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of cloud user groups guids which met the find criteria.

        @execution_method = sync
        
        @param name:                    Name of the cloud user group to include in the search criteria.
        @type name:                     string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of cloud user group guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
        """
        result = self._rootobject.find(name,jobguid,executionparams)
        return result


    def delete (self, cloudusergroupguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the cloud user group specified.

        @execution_method = sync
        
        @param cloudusergroupguid:       guid of the cloud user group to delete.
        @type cloudusergroupguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        result = self._rootobject.delete(cloudusergroupguid,jobguid,executionparams)
        return result


