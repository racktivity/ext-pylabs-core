from pylabs import q

class dssnamespace:
    def getSpreads (self, namespaceguid, jobguid = "", executionparams = {}):
        """
         
		Lists all spreads currently in use by that namespace. A spread is a list of storage daemon application GUID's
        
        @param namespaceguid:        the guid of the namespace you want to get the spreads for 
        @type namespaceguid:         guid
		
		@param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary
        
        @return:                     dictionary with [spreadid, [storagedaemonguid]] as result and jobguid: {'result': [spreadid, [storagedaemonguid]], 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
        params =dict()
        params['namespaceguid'] = namespaceguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'getSpreads', params, jobguid=jobguid, executionparams=executionparams)

    def getXMLSchema (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XSD format of the disk rootobject structure.

        @execution_method = sync
        
        @param diskguid:                guid of the disk rootobject
        @type diskguid:                 guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XSD representation of the disk structure.
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('dssnamespace', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, name, dsspolicyguid, jobguid = "", executionparams = {}):
        """
        
        Create a new namespace with the given policy

        @param name:               name of the namespace
        @type name:                string

        @param dsspolicyguid:      guid of the dss policy that should be applied for storing data in this namespace
        @type dsspolicyguid:       guid     

        @param jobguid:            guid of the job if avalailable else empty string
        @type jobguid:             guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with namespaceguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        params['dsspolicyguid'] = dsspolicyguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def getYAML (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in YAML format of the disk rootobject.

        @execution_method = sync
        
        @param diskguid:                guid of the disk rootobject
        @type diskguid:                 guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @return:                        YAML representation of the disk
        @rtype:                         string
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('dssnamespace', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def getnamespaceinfo (self, namespaceguid, jobguid = "", executionparams = {}):
        """
         
		returns status information about all objects and superblocks in the namespace. 
          
        @param namespaceguid:        the guid of namespace that contains the object 
        @type namespaceguid:         guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary
        
        @return:                     dictionary with [param, integer] as result and jobguid: {'result': [param, integer], 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
        params =dict()
        params['namespaceguid'] = namespaceguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'getnamespaceinfo', params, jobguid=jobguid, executionparams=executionparams)

    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the lan rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('dssnamespace', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def getnextobjectid (self, namespaceguid, jobguid = "", executionparams = {}):
        """
         
		Returns the next available objectid for that namespace. A dss client will use that id to store the object.
        
        @param namespaceguid:        the namespace you want to get the next object id for 
        @type namespaceguid:         guid
		
        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary
        
        @return:                     integer id to be used for next object id.
        @rtype:                      int

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
        params =dict()
        params['namespaceguid'] = namespaceguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'getnextobjectid', params, jobguid=jobguid, executionparams=executionparams)

    def updateSpreads (self, namespaceguid, jobguid = "", executionparams = {}):
        """
         
		Updates and returns all spreads in use by that namespace. Is used when balckisted storage daemons are detected in a spread. A spread is a list of storage daemon application GUID's
        
        @param namespaceguid:        the guid of the namespace you want to get the spreads for 
        @type namespaceguid:         guid
		
        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary
		 
        @return:                     dictionary with [spreadid, [storagedaemonguid]] as result and jobguid: {'result': [spreadid, [storagedaemonguid]], 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
        params =dict()
        params['namespaceguid'] = namespaceguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'updateSpreads', params, jobguid=jobguid, executionparams=executionparams)

    def verifyobject (self, namespaceguid, objectid, jobguid = "", executionparams = {}):
        """
         verifies if object is restorable from dss storage system, this checks the status of the data on the storage daemons for this object.
          
        @param namespaceguid:   the guid of namespace that contains the object 
        @type namespaceguid:    guid
        
        @param objectid :     	id of the object
        @type objectid:       	int      
        
        @return:                dictionary with object storage information as result and jobguid: {'result': dictionary, 'jobguid': guid}
        @rtype:                 dictionary

        @raise e:               In case an error occurred, exception is raised
        
        @todo:                  Will be implemented in phase2
        
	"""
        params =dict()
        params['namespaceguid'] = namespaceguid
        params['objectid'] = objectid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'verifyobject', params, jobguid=jobguid, executionparams=executionparams)

    def getobjectinfo (self, namespaceguid, objectid, jobguid = "", executionparams = {}):
        """
         returns storage information about an object in the store; list storage daemons per superblock and associated spread
          
        @param namespaceguid:        the guid of namespace that contains the object 
        @type namespaceguid:         guid
        
        @param objectid :     	     id of the object
        @type objectid:       	     int      

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary
        
        @return:                     dictionary with [superblockid, spreadid, [storagedaemonguid]] as result and jobguid: {'result': [superblockid, [spreadid, [storagedaemonguid]]], 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
        @todo:                       Will be implemented in phase2
        
	"""
        params =dict()
        params['namespaceguid'] = namespaceguid
        params['objectid'] = objectid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'getobjectinfo', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the disk rootobject.

        @execution_method = sync
        
        @param diskguid:                guid of the disk rootobject
        @type diskguid:                 guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        XML representation of the disk
        @rtype:                         string

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('dssnamespace', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, name = "", dsspolicyguid = "", jobguid = "", executionparams = {}):
        """
        
        Returns a list of namespace guids which met the find criteria.

        @execution_method = sync
        
        @param name:                       Name of the namespace to find.
        @type name:                        string

        @param dsspolicyguid:              guid of the dss policy that is used for the namespace to find
        @type dsspolicyguid:               guid    

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with an array of namespace guids as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['name'] = name
        params['dsspolicyguid'] = dsspolicyguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('dssnamespace', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, dssnamespaceguid, jobguid = "", executionparams = {}):
        """
        
        Delete a namespace.

        @param dssnamespaceguid: guid of the namespace rootobject
        @type dssnamespaceguid:  guid

        @param jobguid:          guid of the job if avalailable else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['dssnamespaceguid'] = dssnamespaceguid
        executionparams['rootobjectguid'] = dssnamespaceguid
        executionparams['rootobjecttype'] = 'dssnamespace'

        
        return q.workflowengine.actionmanager.startRootobjectAction('dssnamespace', 'delete', params, jobguid=jobguid, executionparams=executionparams)


