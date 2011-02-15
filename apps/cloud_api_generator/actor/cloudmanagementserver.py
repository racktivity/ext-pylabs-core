from pylabs import q

class cloudmanagementserver:
    def importRootObjects (self, jobguid = "", executionparams = {}):
        """
        
        PHASE2
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
	"""
        params =dict()
        return q.workflowengine.actionmanager.startActorAction('cloudmanagementserver', 'importRootObjects', params, jobguid=jobguid, executionparams=executionparams)

    def exportRootObjects (self, exports, destinationpath, jobguid = "", executionparams = {}):
        """
        
        the export is in YAML format and 7zip compressed
        PHASE2

        e.g. ["machine","sdsd-2323232-fsfd","machine_kds1",]
        the names of the filenames will be $destUncPath/$the3eArrayElement.rootobject.7z
            e.g. dss://login:passwd@backup_machinex/myroot/backups/rootobjects/10-10-2009/machine_kds1.rootobject.7z

        @param destinationpath:  e.g. ftp://login:passwd@10.10.1.1/myroot/backups/rootobjects/10-10-2009/, cifs://login:passwd@10.10.1.1/myroot/backups/rootobjects/10-10-2009/, dss://login:passwd@backup_machinex/myroot/backups/rootobjects/10-10-2009/z
        @param exports is array of array  [[$rootobjectType,$rootobjectguid,$exportNameForRootobject]]

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
	"""
        params =dict()
        params['exports'] = exports
        params['destinationpath'] = destinationpath
        return q.workflowengine.actionmanager.startActorAction('cloudmanagementserver', 'exportRootObjects', params, jobguid=jobguid, executionparams=executionparams)

    def importAllRootObjects (self, jobguid = "", executionparams = {}):
        """
        
        PHASE2
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
	"""
        params =dict()
        return q.workflowengine.actionmanager.startActorAction('cloudmanagementserver', 'importAllRootObjects', params, jobguid=jobguid, executionparams=executionparams)

    def exportAllRootObjects (self, types, destinationpath, jobguid = "", executionparams = {}):
        """
        
        PHASE2
        walk over all rootobjects of defined types, if not types specified then all types
        all these rootobjects will be exported to destUncPath
        @param destinationpath:  e.g. ftp://login:passwd@10.10.1.1/myroot/backups/rootobjects/10-10-2009/, cifs://login:passwd@10.10.1.1/myroot/backups/rootobjects/10-10-2009/, dss://login:passwd@backup_machinex/myroot/backups/rootobjects/10-10-2009/z
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
	"""
        params =dict()
        params['destinationpath'] = destinationpath
        params['types'] = types
        return q.workflowengine.actionmanager.startActorAction('cloudmanagementserver', 'exportAllRootObjects', params, jobguid=jobguid, executionparams=executionparams)


