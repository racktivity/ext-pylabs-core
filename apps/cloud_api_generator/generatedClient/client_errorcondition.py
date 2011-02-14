from cloud_api_client.Exceptions import CloudApiException

class errorcondition:
    def __init__(self, proxy):
        self._proxy = proxy


    def getXMLSchema (self, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the errorcondition rootobject structure.

        @execution_method = sync

        @param jobguid:          guid of the errorcondition rootobject
        @type jobguid:           guid

        @param executionparams:  dictionary of errorcondition specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 XSD representation of the errorcondition structure.
        @rtype:                  string

        @raise e:                In case an error occurred, exception is raised

        @todo:                   Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.getXMLSchema(jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def create (self, errorconditiontype = "", timestamp = "", level = "", agent = "", tags = "", errormessagepublic = "", errormessageprivate = "", application = "", backtrace = "", logs = "", transactioninfo = "", jobguid = "", executionparams = {}):
        """
        
        Create a new errorcondition

        @execution_method = sync

        @param errorconditiontype:       type of errorcondition
        @type errorconditiontype:        int

        @param timestamp:                timestamp of errorcondition
        @type timestamp:                 int

        @param level:                    level of errorcondition
        @type level:                     string

        @param agent:                    unique id of agent
        @type agent:                     string

        @param tags:                     series of tags format
        @type tags:                      string

        @params errormessagepublic:      public error message
        @type errormessagepublic         string

        @params errormessageprivate:     private error message
        @type errormessageprivate        string

        @param application:              name of the application
        @type application:               string

        @param backtrace:                backtrace message
        @type backtrace:                 string

        @param logs:                     log message
        @type logs:                      string

        @param transactioninfo:          info of the transaction
        @type transactioninfo:           string

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with backplaneguid as result and errorconditionguid: {'result': guid, 'errorconditionguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.create(errorconditiontype,timestamp,level,agent,tags,errormessagepublic,errormessageprivate,application,backtrace,logs,transactioninfo,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def list (self, errorconditionguid = "", jobguid = "", executionparams = {}):
        """
        
        List all errorconditions or only specified errorcondition

        @execution_method = sync

        @param errorconditionguid:       guid of the errorcondition
        @type errorconditionguid:        guid

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid


        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with array of errorcondition info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.list(errorconditionguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getYAML (self, errorconditionguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the errorcondition rootobject.

        @execution_method = sync

        @param errorconditionguid: guid of the errorcondition rootobject
        @type errorconditionguid:  guid

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   YAML representation of the errorcondition
        @rtype:                    string
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.getYAML(errorconditionguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getObject (self, errorconditionguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync

        @param errorconditionguid:   guid of the job rootobject
        @type errorconditionguid:    guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     rootobject
        @rtype:                      rootobject

        @warning:                    Only usable using the python client.
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.getObject(errorconditionguid,jobguid,executionparams)

            from osis import ROOTOBJECT_TYPES
            import base64
            from osis.model.serializers import ThriftSerializer
            result = base64.decodestring(result['result'])
            result = ROOTOBJECT_TYPES['errorcondition'].deserialize(ThriftSerializer, result)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def raiseErrorCondition (self, level = "", typeid = "", errormessagepublic = "", errormessageprivate = "", tags = "", jobguid = "", executionparams = {}):
        """
        
        Create a new errorcondition and escalate it

        @execution_method = sync

        @param level:                    level of errorcondition ('CRITICAL','ERROR','INFO','UNKNOWN','URGENT','WARNING')
        @type level:                     string
        
        @param typeid:                   predefined type id (ex. SSO-MON-NETWORK-0001)
        @type typeid:                    string

        @params errormessagepublic:      public error message
        @type errormessagepublic         string

        @params errormessageprivate:     private error message
        @type errormessageprivate        string

        @param tags:                     series of tags format
        @type tags:                      string

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with backplaneguid as result and errorconditionguid: {'result': guid, 'errorconditionguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.raiseErrorCondition(level,typeid,errormessagepublic,errormessageprivate,tags,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def getXML (self, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the errorcondition rootobject.

        @execution_method = sync

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  XML representation of the errorcondition
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised

        @todo:                    Will be implemented in phase2
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.getXML(jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def find (self, errorconditiontype = "", timestamp = "", level = "", agent = "", tags = "", application = "", jobguid = "", executionparams = {}):
        """
        
        @execution_method = sync

        @param errorconditiontype:       type of errorcondition
        @type errorconditiontype:        string

        @param timestamp:                timestamp of errorcondition
        @type timestamp:                 int

        @param level:                    level of errorcondition
        @type level:                     int

        @param agent:                    unique id of agent
        @type agent:                     string

        @param tags:                     series of tags format
        @type tags:                      string

        @param application:              name of the application
        @type application:               string

        @param jobguid:                  guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        @returns array of array [[...]]
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.find(errorconditiontype,timestamp,level,agent,tags,application,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)


    def delete (self, errorconditionguid, jobguid = "", executionparams = {}):
        """
        
        Delete the specified errorcondition

        @security: administrator

        @execution_method = sync

        @param errorconditionguid:       guid of the errorcondition
        @type errorconditionguid:        guid

        @param jobguid:                  guid of the errorcondition if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of errorcondition specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         dictionary with True as result and errorcondition: {'result': True, 'errorconditionguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        
        """
        try:
            result = self._proxy.cloud_api_errorcondition.delete(errorconditionguid,jobguid,executionparams)
            return result
        except Exception, ex:
            raise CloudApiException(ex)



