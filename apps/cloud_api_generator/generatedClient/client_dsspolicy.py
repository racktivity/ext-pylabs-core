from cloud_api_client.Exceptions import CloudApiException

class dsspolicy:
    def __init__(self, proxy):
        self._proxy = proxy


    def getXMLSchema (self, dsspolicyguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the dsspolicy rootobject structure.

        @execution_method = sync
        
        @param dsspolicyguid:           guid of the dsspolicyguid rootobject
        @type dsspolicyguid:            guid

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the dsspolicy structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.getXMLSchema(dsspolicyguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, name, storageNodes, storageSafety, minSbSize, maxSbSize, spreadLocations, resourceGroup, jobguid = "", executionparams = {}):
        """
         
        creates a new dss policy

        @execution_method = sync
        
        @param name:            policy name
        @type name:             string

        @param storageNodes:    defines the minimum number of storage daemons in the spread
        @type storageNodes:     int

        @param  storageSafety:  defines the number of storage daemons in that can be unavailable in a spread before data loss occurs
        @type storageSafety:    int
    
        @param minSbSize:       the minimum size of a superblock in bytes (needs to be power of 2)
        @type minSbSize:        int       
    
        @param maxSbSize:       the maximum size of a superblock in bytes (needs to be power of 2)
        @type maxSbSize:        int
        
        @param spreadLocations: specify a list of locations on which the data needs to be equally spread, array of datacenter guids
        @type spreadLocations:  array(guid)    
    
        @param resourceGroup:   a resourcegroup is an array of pmachineguids that represent storage nodes
        @type resourceGroup:    array(guid)        

        @param jobguid:         guid of the job if available else empty string
        @type jobguid:          guid

        @param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:  dictionary

        @return:                dictionary with policyguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                 dictionary

        @raise e:               In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.create(name,storageNodes,storageSafety,minSbSize,maxSbSize,spreadLocations,resourceGroup,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, name = "", status = "", disksafetytype = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of dsspolicy guids which met the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the dss policy
        @type name:                        string
        
        @param status:                     Status of the policy
        @type status:                      string
        
        @param disksafetytype:             Disksafety type of the policy
        @type disksafetytype:              string
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of policy guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.list(name,status,disksafetytype,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, dsspolicyguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the dsspolicy rootobject.

        @execution_method = sync
        
        @param dsspolicyguid:           guid of the dsspolicy rootobject
        @type dsspolicyguid:            guid

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @return:                        YAML representation of the dsspolicy
        @rtype:                         string
        
        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.getYAML(dsspolicyguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the dsspolicy rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['dsspolicy'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, dsspolicyguid, status = "", jobguid = "", executionparams = {}):
        """
        
        Updates the status of an dss policy
                                        
        @param dsspolicyguid:           Guid of the dsspolicyguid rootobject
        @type dsspolicyguid:            guid
        
        @param status:                  Change the status attribute
        @type status:                   string
        
        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with a boolean as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.updateModelProperties(dsspolicyguid,status,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, dsspolicyguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the dsspolicy rootobject.

        @execution_method = sync
        
        @param dsspolicyguid:           guid of the dsspolicyguid rootobject
        @type dsspolicyguid:            guid

        @param jobguid:                 guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the dsspolicy
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.getXML(dsspolicyguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, name = "", status = "", disksafetytype = "", storagesafety = "", storagewidth = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of dsspolicy guids which met the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the dsspolicy
        @type name:                        string
        
        @param status:                     Status of the policy
        @type status:                      string
        
        @param disksafetytype:             Disksafety type of the policy (eg SSO,MIRRORCLOUD)
        @type disksafetytype:              string

        @param storagesafety:              Storage safety of the policy (nr of disks that can be lost without data loss)
        @type storagesafety:               int

        @param storagewidth:               Storage width of the policy (nr of disks that data is spread amongst)
        @type storagewidth:                int
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of policy guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_dsspolicy.find(name,status,disksafetytype,storagesafety,storagewidth,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



