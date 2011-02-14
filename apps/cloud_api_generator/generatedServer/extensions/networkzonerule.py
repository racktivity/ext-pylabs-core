from cloud_api_rootobjects import cloud_api_networkzonerule

class networkzonerule:

    def __init__(self):
        self._rootobject = cloud_api_networkzonerule.networkzonerule()

    def getXMLSchema (self, networkzoneruleguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the networkzonerule rootobject structure.

        @execution_method = sync
        
        @param networkzoneruleguid:     Guid of the networkzonerule rootobject
        @type networkzoneruleguid:      guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the networkzonerule structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        result = self._rootobject.getXMLSchema(networkzoneruleguid,jobguid,executionparams)
        return result


    def create (self, name, description = "", sourcenetworkzoneguid = "", destnetworkzoneguid = "", nrhops = 0, gatewayip = "", log = "", disabled = True, freetransit = 0, priority = 0, ipzonerules = [], jobguid = "", executionparams = {}):
        """
        
        Create a new networkzonerule.

        @security administrators
        @param name:                      name of the networkzonerule
        @type name:                       string

        @param description:               description of the networkzonerule
        @type description:                string

        @param sourcenetworkzoneguid:     guid of the source network zone
        @type sourcenetworkzoneguid:      guid

        @param destnetworkzoneguid:       guid of the destination network zone
        @type destnetworkzoneguid:        guid

        @param nrhops:                    number of hops
        @type nrhops:                     int

        @param gatewayip:                 gateway
        @type gatewayip:                  ipaddress

        @param log:                       log of the networkzonerule
        @type log:                        string

        @param disabled:                  flag to indicate whether the rule is disable or not
        @type disabled:                   boolean

        @param freetransit:               freetransit of the networkzonerule
        @type freetransit:                int

        @param priority:                  priority of the networkzonerule
        @type priority:                   int

        @param ipzonerules:               ip zone rules
        @type ipzonerules:                array(ipzonerule)

        @param jobguid:                   Guid of the job if avalailable else empty string
        @type jobguid:                    guid

        @param executionparams:           dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:            dictionary

        @return:                          dictionary with networkzoneruleguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                           dictionary

        @raise e:                         In case an error occurred, exception is raised
        
        @todo:                            Will be implemented in phase2
        
        """
        result = self._rootobject.create(name,description,sourcenetworkzoneguid,destnetworkzoneguid,nrhops,gatewayip,log,disabled,freetransit,priority,ipzonerules,jobguid,executionparams)
        return result


    def list (self, networkzoneruleguid = "", jobguid = "", executionparams = {}):
        """
        
        List all networkzonerules.

        @execution_method = sync
        
        @param networkzoneruleguid:     Guid of the networkzonerule specified
        @type networkzoneruleguid:      guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of networkzonerule info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'networkzoneruleguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'networkzonerule0001',
        @note:                                      'description': 'networkzonerule 0001',
        @note:                                      'sourcenetworkzoneguid': '73444C07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'destnetworkzoneguid': '43554C07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'nrhops': 1,
        @note:                                      'gatewayip': '192.168.0.254',
        @note:                                      'log':"",
        @note:                                      'disabled' : True,
        @note:                                      'freetransit':"",
        @note:                                      'priority':"",
        @note:                                      'ipzonerules'=[]}]}
        
        @raise e:                       In case an error occurred, exception is raised
        
        """
        result = self._rootobject.list(networkzoneruleguid,jobguid,executionparams)
        return result


    def getYAML (self, networkzoneruleguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the networkzonerule rootobject.

        @execution_method = sync
        
        @param networkzoneruleguid:   Guid of the networkzonerule rootobject
        @type networkzoneruleguid:    guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the networkzonerule
        @rtype:                       string
        
        """
        result = self._rootobject.getYAML(networkzoneruleguid,jobguid,executionparams)
        return result


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the networkzonerule rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        
        """
        result = self._rootobject.getObject(rootobjectguid,jobguid,executionparams)

        from osis import ROOTOBJECT_TYPES
        import base64
        from osis.model.serializers import ThriftSerializer
        result = base64.decodestring(result['result'])
        result = ROOTOBJECT_TYPES['networkzonerule'].deserialize(ThriftSerializer, result)
        return result


    def updateModelProperties (self, networkzoneruleguid, name = "", description = "", sourcenetworkzoneguid = "", destnetworkzoneguid = "", nrhops = 0, gatewayip = "", log = "", disabled = True, freetransit = 0, priority = 0, ipzonerules = [], jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @security administrators
        @param networkzoneruleguid:           Guid of the networkzonerule specified
        @type networkzoneruleguid:            guid

        @param  name:                         name of the networkzonerule
        @type name:                           string

        @param  description:                  description of the networkzonerule
        @type description:                    string

        @param sourcenetworkzoneguid:         guid of the source network zone
        @type sourcenetworkzoneguid:          guid

        @param destnetworkzoneguid:           guid of the destination network zone
        @type destnetworkzoneguid:            guid

        @param nrhops:                        number of hops
        @type nrhops:                         int

        @param gatewayip:                     gateway
        @type gatewayip:                      ipaddress

        @param log:                           log of the networkzonerule
        @type log:                            string

        @param disabled:                      flag to indicate whether the rule is disable or not
        @type disabled:                       boolean

        @param freetransit:                   freetransit of the networkzonerule
        @type freetransit:                    int

        @param priority:                      priority of the networkzonerule
        @type priority:                       int

        @param ipzonerules:                   ip zone rules
        @type ipzonerules:                    array(ipzonerule)

        @param jobguid:                       Guid of the job if avalailable else empty string
        @type jobguid:                        guid

        @param executionparams:               dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:                dictionary

        @return:                              dictionary with networkzone rule guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                               dictionary

        @raise e:                             In case an error occurred, exception is raised
        
        """
        result = self._rootobject.updateModelProperties(networkzoneruleguid,name,description,sourcenetworkzoneguid,destnetworkzoneguid,nrhops,gatewayip,log,disabled,freetransit,priority,ipzonerules,jobguid,executionparams)
        return result


    def getXML (self, networkzoneruleguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the networkzonerule rootobject.

        @execution_method = sync
        
        @param networkzoneruleguid:     Guid of the networkzonerule rootobject
        @type networkzoneruleguid:      guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the networkzonerule
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
        """
        result = self._rootobject.getXML(networkzoneruleguid,jobguid,executionparams)
        return result


    def find (self, name = "", description = "", sourcenetworkzoneguid = "", destnetworkzoneguid = "", nrhops = "", gatewayip = "", log = "", disabled = True, freetransit = "", priority = "", ipzonerules = [], jobguid = "", executionparams = {}):
        """
        
        Returns a list of networkzonerule guids which met the find criteria.

        @execution_method = sync
        
        @security administrators
        @param  name:                    name of the networkzonerule
        @type name:                      string

        @param  description:             description of the networkzonerule
        @type description:               string

        @param sourcenetworkzoneguid:    guid of the source network zone
        @type sourcenetworkzoneguid:     guid

        @param destnetworkzoneguid:      guid of the destination network zone
        @type destnetworkzoneguid:       guid

        @param nrhops:                   number of hops
        @type nrhops:                    int

        @param gatewayip:                gateway
        @type gatewayip:                 ipaddress

        @param log:                      log of the networkzonerule
        @type log:                       string

        @param disabled:                 flag to indicate whether the rule is disable or not
        @type disabled:                  boolean

        @param freetransit:              freetransit of the networkzonerule
        @type freetransit:               int

        @param priority:                 priority of the networkzonerule
        @type priority:                  int

        @param ipzonerules:              ip zone rules
        @type ipzonerules:               array(ipzonerule)
        
        @param jobguid:                  Guid of the job if avalailable else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary

        @return:                         Array of networkzonerule guids which met the find criteria specified.
        @rtype:                          array

        @note:                           Example return value:
        @note:                           {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                            'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                        In case an error occurred, exception is raised
        
        @todo:                           Will be implemented in phase2
        
        """
        result = self._rootobject.find(name,description,sourcenetworkzoneguid,destnetworkzoneguid,nrhops,gatewayip,log,disabled,freetransit,priority,ipzonerules,jobguid,executionparams)
        return result


    def delete (self, networkzoneruleguid, jobguid = "", executionparams = {}):
        """
        
        Delete a networkzonerule.

        @security administrators
        @param networkzoneruleguid:   Guid of the networkzonerule rootobject to delete.
        @type networkzoneruleguid:    guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
        @todo:                        Will be implemented in phase2
        
        """
        result = self._rootobject.delete(networkzoneruleguid,jobguid,executionparams)
        return result


