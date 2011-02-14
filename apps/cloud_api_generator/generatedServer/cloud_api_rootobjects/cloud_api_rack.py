from pymonkey import q

class rack:
    def getXMLSchema (self, rackguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the rack rootobject structure.

        @execution_method = sync
        
        @param rackguid:           Guid of the rack rootobject
        @type rackguid:            guid

        @param jobguid:            Guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   XSD representation of the rack structure.
        @rtype:                    string

        @raise e:                  In case an error occurred, exception is raised

        @todo:                     Will be implemented in phase2
        
	"""
        params =dict()
        params['rackguid'] = rackguid
        executionparams['rootobjectguid'] = rackguid
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, name, racktype, description = "", datacenterguid = "", floor = "", corridor = "", position = "", height = 42, jobguid = "", executionparams = {}):
        """
        
        Create a new rack.

        @execution_method = sync
        
        @security administrators
        @param name:                   Name for the rack.
        @type name:                    string

        @param racktype:               type of the rack
        @type racktype:                string

        @param description:            Description for the rack.
        @type description:             string

        @param datacenterguid:         datacenter to which the rack belongs
        @type datacenterguid:          guid

        @param  floor:                 floor location of the rack in the datacenter
        @type floor:                   string(100)

        @param  corridor:              corridor location of the rack on the floor
        @type corridor:                string(100)

        @param  position:              position of the rack in the corridor or datacenter
        @type position:                string(100)

        @param  height:                rack height
        @type height:                  int

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with rackguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        params['floor'] = floor
        params['height'] = height
        params['corridor'] = corridor
        params['position'] = position
        params['racktype'] = racktype
        params['datacenterguid'] = datacenterguid
        params['description'] = description
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def list (self, rackguid = "", jobguid = "", executionparams = {}):
        """
        
        List all racks.

        @execution_method = sync
        
        @param rackguid:                Guid of the rack specified
        @type rackguid:                 guid

        @security administrators
        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of rack info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: [{ 'rackguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'name': 'rack001',
        @note:                                      'description': 'rack 0001',
        @note:                                      'racktype' :   "OPEN",
        @note:                                      'floor':"",
        @note:                                      'datacenterguid': '3351FF9F-D65A-4F65-A96B-AC4A6246C033',
                                                    'corridor': "",
                                                    'position':"",
                                                    'height':42}]}
                                                    
        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['rackguid'] = rackguid
        executionparams['rootobjectguid'] = rackguid
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'list', params, jobguid=jobguid, executionparams=executionparams)

    def getYAML (self, rackguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the rack rootobject.

        @execution_method = sync
        
        @param rackguid:              Guid of the rack rootobject
        @type rackguid:               guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the rack
        @rtype:                       string
        
	"""
        params =dict()
        params['rackguid'] = rackguid
        executionparams['rootobjectguid'] = rackguid
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the rack rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def updateModelProperties (self, rackguid, name = "", racktype = "", description = "", datacenterguid = "", floor = "", corridor = "", position = "", height = 42, jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @execution_method = sync
        
        @security administrators
        @param rackguid:               Guid of the rack specified
        @type rackguid:                guid

        @param name:                   Name for the rack.
        @type name:                    string

        @param racktype:               type of the rack
        @type racktype:                string

        @param description:            Description for the rack.
        @type description:             string

        @param datacenterguid:         datacenter to which the rack belongs
        @type datacenterguid:          guid

        @param  floor:                 floor location of the rack in the datacenter
        @type floor:                   string(100)

        @param  corridor:              corridor location of the rack on the floor
        @type corridor:                string(100)

        @param  position:              position of the rack in the corridor or datacenter
        @type position:                string(100)

        @param  height:                rack height
        @type height:                  int

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with rack guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['rackguid'] = rackguid
        executionparams['rootobjectguid'] = rackguid
        params['name'] = name
        params['floor'] = floor
        params['height'] = height
        params['corridor'] = corridor
        params['position'] = position
        params['racktype'] = racktype
        params['datacenterguid'] = datacenterguid
        params['description'] = description
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'updateModelProperties', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, rackguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the rack rootobject.

        @execution_method = sync
        
        @param rackguid:           Guid of the rack rootobject
        @type rackguid:            guid

        @param jobguid:            Guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   XML representation of the rack
        @rtype:                    string

        @raise e:                  In case an error occurred, exception is raised

        @todo:                     Will be implemented in phase2
        
	"""
        params =dict()
        params['rackguid'] = rackguid
        executionparams['rootobjectguid'] = rackguid
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def listDevices (self, rackguid, jobguid = "", executionparams = {}):
        """
        
        List all devices of the rack.
  
        @execution_method = sync
              
        @param rackguid:                Guid of the rack specified
        @type rackguid:                 guid

        @param jobguid:                 Guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of devices
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['rackguid'] = rackguid
        executionparams['rootobjectguid'] = rackguid
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'listDevices', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, name = "", racktype = "", description = "", datacenterguid = "", floor = "", corridor = "", position = "", height = 42, jobguid = "", executionparams = {}):
        """
        
        Returns a list of rack guids which met the find criteria.

        @execution_method = sync
        
        @security administrators

        @param name:                   Name for the rack.
        @type name:                    string

        @param racktype:               type of the rack
        @type racktype:                string

        @param description:            Description for the rack.
        @type description:             string

        @param datacenterguid:         datacenter to which the rack belongs
        @type datacenterguid:          guid

        @param  floor:                 floor location of the rack in the datacenter
        @type floor:                   string(100)

        @param  corridor:              corridor location of the rack on the floor
        @type corridor:                string(100)

        @param  position:              position of the rack in the corridor or datacenter
        @type position:                string(100)

        @param  height:                rack height
        @type height:                  int

        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Array of rack guids which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        params['floor'] = floor
        params['height'] = height
        params['corridor'] = corridor
        params['position'] = position
        params['racktype'] = racktype
        params['datacenterguid'] = datacenterguid
        params['description'] = description
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, rackguid, jobguid = "", executionparams = {}):
        """
        
        Delete a rack.

        @execution_method = sync
        
        @security administrators
        @param rackguid:              Guid of the rack rootobject to delete.
        @type rackguid:               guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['rackguid'] = rackguid
        executionparams['rootobjectguid'] = rackguid
        executionparams['rootobjecttype'] = 'rack'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('rack', 'delete', params, jobguid=jobguid, executionparams=executionparams)


