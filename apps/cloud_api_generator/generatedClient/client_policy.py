from cloud_api_client.Exceptions import CloudApiException

class policy:
    def __init__(self, proxy):
        self._proxy = proxy


    def getXMLSchema (self, policyguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the os rootobject structure.

        @execution_method = sync
        
        @param policyguid:                guid of the os rootobject
        @type policyguid:                 guid
 
        @param jobguid:                   guid of the job if avalailable else empty string
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          XSD representation of the os structure.
        @rtype:                           string

        @raise e:                         In case an error occurred, exception is raised

        @todo:                            Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_policy.getXMLSchema(policyguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, name, rootobjecttype, rootobjectaction, rootobjectguid, interval, runbetween = None, runnotbetween = None, policyparams = None, description = "", jobguid = "", executionparams = {}):
        """
        
        Creates a new policy.

        @execution_method = sync
        
        @param name:                     Name for the new policy
        @type name:                      string

        @param rootobjecttype:           RootObject type for the new policy
        @type rootobjecttype:            string
        
        @param rootobjectaction:         Name of the action for the new policy
        @type rootobjectaction:          string
        
        @param rootobjectguid:           Guid of the rootobject for the new policy
        @type rootobjectguid:            string
        
        @param interval:                 Interval for the new policy
        @type interval:                  int
        
        @param runbetween:               List of tuples with timestamps when a policy can run
        @type runbetween:                list
        
        @param runnotbetween:            List of tuples with timestamps when a policy can not run
        @type runnotbetween:             string
        
        @param policyparams:             Params for the new policy
        @type policyparams:              string
        
        @param description:              Description for the new policy
        @type description:               string
        
        @param jobguid:                  Guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         Dictionary with policyguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_policy.create(name,rootobjecttype,rootobjectaction,rootobjectguid,interval,runbetween,runnotbetween,policyparams,description,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, policyguid = "", name = "", rootobjectaction = "", rootobjecttype = "", status = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of all policies depending on passed filters.

        @execution_method = sync
        
        @param policyguid:                   Guid of the cloudspace
        @type policyguid:                    guid
        
        @param name:                         Name of the policy
        @type name:                          string
        
        @param rootobjectaction:             Action on the rootobject
        @type rootobjectaction:              string         
        
        @param rootobjecttype:               Rootobject type e.g. sso
        @type rootobjecttype:                string
        
        @param status:                       Status of the policy
        @type status:                        string        

        @param jobguid:                      guid of the job if avalailable else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with array of operating system info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                              dictionary
        @note:                               {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                'result: [{ 'name': 'Daily backup DBServer'
        @note:                                            'description': 'Daily backup of our database server',
        @note:                                            'rootobjecttype': 'machine',
        @note:                                            'rootobjectaction': 'backup',
        @note:                                            'policyparams': {},
        @note:                                            'rootobjectguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                            'interval': 86400,
        @note:                                            'lastrun': '2009-05-23 11:25:33',
        @note:                                            'runbetween': [("00:00", "02.00"), ("04:00", "06:00")],
        @note:                                            'runnotbetween': [("08:00", "12:00"), ("14:00", "18:00")]}]}
        
        @raise e:                            In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_policy.list(policyguid,name,rootobjectaction,rootobjecttype,status,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, policyguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the policy rootobject.

        @execution_method = sync
        
        @param policyguid:              guid of the os rootobject
        @type policyguid:               guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @return:                        YAML representation of the os
        @rtype:                         string
        
        """
        try:
            result = self._proxy.cloud_api_policy.getYAML(policyguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:     guid of the policy object
        @type rootobjectguid:      guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   rootobject
        @rtype:                    string

        @warning:                  Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_policy.getObject(rootobjectguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['policy'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def updateModelProperties (self, policyguid, name = "", description = "", lastrun = "", status = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of policy guids which met the find criteria.

        @execution_method = sync
        
        @param name:               Name of the policy
        @type name:                string
        
        @param description:        description of the policy
        @type description:         string
        
        @param lastrun:            lastrun of the policy
        @type lastrun:             datetime
        
        @param status:             Status for the policy
        @type status:              string
        
        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised        
        
        """
        try:
            result = self._proxy.cloud_api_policy.updateModelProperties(policyguid,name,description,lastrun,status,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, policyguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the os rootobject.

        @execution_method = sync
        
        @param policyguid:              guid of the os rootobject
        @type policyguid:               guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid
        
        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the os
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_policy.getXML(policyguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, name = "", description = "", rootobjecttype = "", rootobjectaction = "", rootobjectguid = "", interval = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of policy guids which met the find criteria.

        @execution_method = sync
        
        @param name:               Name of the policy
        @type name:                string
        
        @param description:        description of the policy
        @type description:         string

        @param rootobjecttype:     Rootobject type.
        @type rootobjecttype:      string

        @param rootobjectaction:   Action to execute on the rootobject
        @type rootobjectaction:    string

        @param rootobjectguid:     Guid of the rootobject
        @type rootobjectguid:      string

        @param interval:           Interval in seconds
        @type interval:            int

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with an array of policy guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_policy.find(name,description,rootobjecttype,rootobjectaction,rootobjectguid,interval,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, policyguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the given policy.

        @execution_method = sync
        
        @param policyguid:               Guid of the policy to delete.
        @type policyguid:                guid

        @param jobguid:                  Guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         Dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_policy.delete(policyguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



