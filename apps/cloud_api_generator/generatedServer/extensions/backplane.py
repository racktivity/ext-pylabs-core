from cloud_api_rootobjects import cloud_api_backplane

class backplane:

    def __init__(self):
        self._rootobject = cloud_api_backplane.backplane()

    def listLans (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        List of all related lans to the backplane.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane rootobject
        @type backplaneguid:            guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of lans info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
        """
        result = self._rootobject.listLans(backplaneguid,jobguid,executionparams)
        return result


    def getXMLSchema (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the backplane rootobject structure.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane rootobject
        @type backplaneguid:            guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the backplane structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        result = self._rootobject.getXMLSchema(backplaneguid,jobguid,executionparams)
        return result


    def create (self, name, backplanetype, description = "", publicflag = False, managementflag = False, storageflag = False, jobguid = "", executionparams = {}):
        """
        
        Create a new backplane.

        @param name:                   Name for the backplane.
        @type name:                    string

        @param backplanetype:          Type of the backplane (ETHERNET, INFINIBAND)
        @type backplanetype:           string

        @param description:            Description for the backplane.
        @type description:             string

        @param publicflag:             Indicates if the backplane is a public backplane.
        @type publicflag:              boolean

        @param storageflag:            Indicates if the backplane is a storage backplane.
        @type storageflag:             boolean

        @param managementflag:         Indicates if the backplane is a management backplane.
        @type managementflag:          boolean

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with backplaneguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        result = self._rootobject.create(name,backplanetype,description,publicflag,managementflag,storageflag,jobguid,executionparams)
        return result


    def list (self, backplaneguid = "", jobguid = "", executionparams = {}):
        """
        
        List all backplanes.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane
        @type backplaneguid:            guid
 
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of backplane info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'backplaneguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'Storage Backplane',
        @note:                                      'backplanetype': 'INFINIBAND',
        @note:                                      'public': False,
        @note:                                      'storage': True,
        @note:                                      'management': False},
        @note:                                    { 'backplaneguid': '789544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'Management Backplane',
        @note:                                      'backplanetype': 'ETHERNET',
        @note:                                      'public': False,
        @note:                                      'storage': False,
        @note:                                      'management': False}]}
        
        @raise e:                       In case an error occurred, exception is raised
        
        """
        result = self._rootobject.list(backplaneguid,jobguid,executionparams)
        return result


    def getYAML (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the backplane rootobject.

        @execution_method = sync
        
        @param backplaneguid:    Guid of the backplane rootobject
        @type backplaneguid:     guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 YAML representation of the backplane
        @rtype:                  string
        
        """
        result = self._rootobject.getYAML(backplaneguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.getObject(rootobjectguid,jobguid,executionparams)

        from osis import ROOTOBJECT_TYPES
        import base64
        from osis.model.serializers import ThriftSerializer
        result = base64.decodestring(result['result'])
        result = ROOTOBJECT_TYPES['backplane'].deserialize(ThriftSerializer, result)
        return result


    def updateModelProperties (self, backplaneguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @param backplaneguid:          Guid of the backplane specified
        @type backplaneguid:           guid

        @param name:                   Name for this backplane
        @type name:                    string

        @param description:            Description for this backplane
        @type description:             string

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with backplane guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        result = self._rootobject.updateModelProperties(backplaneguid,name,description,jobguid,executionparams)
        return result


    def setFlags (self, backplaneguid, publicflag = False, managementflag = False, storageflag = False, jobguid = "", executionparams = {}):
        """
        
        Sets the role flags for the specified backplane.

        @param backplaneguid:          Guid of the backplane
        @type backplaneguid:           guid

        @param publicflag:             Defines if the backplane is used as a public backplane. Not modified if empty.
        @type publicflag:              boolean

        @param managementflag:         Defines if the backplane is used as a management backplane. Not modified if empty.
        @type managementflag:          boolean

        @param storageflag:            Defines if the backplane is used as a storage backplane. Not modified if empty.
        @type storageflag:             boolean

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        result = self._rootobject.setFlags(backplaneguid,publicflag,managementflag,storageflag,jobguid,executionparams)
        return result


    def getXML (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the backplane rootobject.
        
        @execution_method = sync

        @param backplaneguid:    Guid of the backplane rootobject
        @type backplaneguid:     guid

        @param jobguid:          Guid of the job if avalailable else empty string
        @type jobguid:           guid


        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 XML representation of the backplane
        @rtype:                  string

        @raise e:                In case an error occurred, exception is raised

        @todo:                   Will be implemented in phase2
        
        """
        result = self._rootobject.getXML(backplaneguid,jobguid,executionparams)
        return result


    def find (self, name = "", managementflag = "", publicflag = "", storageflag = "", backplanetype = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of backplane guids which met the find criteria.
        
        @execution_method = sync

        @param name:                    Name of the backplanes to include in the search criteria.
        @type name:                     string

        @param managementflag:          managementflag of the backplanes to include in the search criteria.
        @type managementflag:           boolean

        @param publicflag:              publicflag of the backplanes to include in the search criteria.
        @type publicflag:               boolean

        @param storageflag:             storageflag of the backplanes to include in the search criteria.
        @type storageflag:              boolean

        @param backplanetype:           Type of the backplanes to include in the search criteria.
        @type backplanetype:            int

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of backplane guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
        """
        result = self._rootobject.find(name,managementflag,publicflag,storageflag,backplanetype,jobguid,executionparams)
        return result


    def listResourcegroups (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        List of all related resourcegroups to the backplane.

        @execution_method = sync
        
        @param backplaneguid:           Guid of the backplane rootobject
        @type backplaneguid:            guid
        
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of resourcegroups info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
        """
        result = self._rootobject.listResourcegroups(backplaneguid,jobguid,executionparams)
        return result


    def delete (self, backplaneguid, jobguid = "", executionparams = {}):
        """
        
        Delete a backplane.

        @param backplaneguid:          Guid of the backplane rootobject to delete.
        @type backplaneguid:           guid

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
        """
        result = self._rootobject.delete(backplaneguid,jobguid,executionparams)
        return result


