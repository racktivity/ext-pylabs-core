from cloud_api_rootobjects import cloud_api_os

class os:

    def __init__(self):
        self._rootobject = cloud_api_os.os()

    def getXMLSchema (self, osguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the os rootobject structure.

        @execution_method = sync
        
        @param osguid:                guid of the os rootobject
        @type osguid:                 guid

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      XSD representation of the os structure.
        @rtype:                       string

        @raise e:                     In case an error occurred, exception is raised

        @todo:                        Will be implemented in phase2
        
        """
        result = self._rootobject.getXMLSchema(osguid,jobguid,executionparams)
        return result


    def list (self, osguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of all known operating systems.

        @execution_method = sync
        
        @param osguid:               guid of the os rootobject
        @type osguid:                guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of operating system info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised

        @note:                       {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                        'result: [{ 'osguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                    'name': 'Windows XP',
        @note:                                    'description': 'Microsoft Windows XP',
        @note:                                    'iconname': 'WinXP.png',
        @note:                                    'osversion': 'Service Pack 2',
        @note:                                    'patchlevel': '',
        @note:                                    'type': 'WINDOWS'}]}
        
        """
        result = self._rootobject.list(osguid,jobguid,executionparams)
        return result


    def getYAML (self, osguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the os rootobject.

        @execution_method = sync
        
        @param diskguid:                guid of the os rootobject
        @type diskguid:                 guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @return:                        YAML representation of the os
        @rtype:                         string
        
        """
        result = self._rootobject.getYAML(osguid,jobguid,executionparams)
        return result


    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the os object
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
        """
        result = self._rootobject.getObject(rootobjectguid,jobguid,executionparams)

        from osis import ROOTOBJECT_TYPES
        import base64
        from osis.model.serializers import ThriftSerializer
        result = base64.decodestring(result['result'])
        result = ROOTOBJECT_TYPES['os'].deserialize(ThriftSerializer, result)
        return result


    def getXML (self, osguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the os rootobject.

        @execution_method = sync
        
        @param osguid:                guid of the os rootobject
        @type osguid:                 guid

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid
        
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      XML representation of the os
        @rtype:                       string

        @raise e:                     In case an error occurred, exception is raised

        @todo:                        Will be implemented in phase2
        
        """
        result = self._rootobject.getXML(osguid,jobguid,executionparams)
        return result


    def find (self, name = "", ostype = "", iconname = "", osversion = "", patchlevel = "", description = "", osbitversion = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of os guids which met the find criteria.

        @execution_method = sync
        
        @param name:               Name of the os.
        @type name:                string

        @param ostype:             Os type.
        @type ostype:              string

        @param iconname:           filename of icon representing os in various clouduser interfaces
        @type iconname:            string

        @param osversion:          version of the operating system
        @type osversion:           string

        @param patchlevel:         patch level of operating system
        @type patchlevel:          string

        @param description:        description of the operating system
        @type description:         string
        
        @param osbitversion:          bit version of the operating system e.g. 32-bit , 64-bit
        @type osbitversion:           string

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with an array of os guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
        """
        result = self._rootobject.find(name,ostype,iconname,osversion,patchlevel,description,osbitversion,jobguid,executionparams)
        return result


