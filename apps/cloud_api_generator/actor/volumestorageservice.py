from pymonkey import q

class volumestorageservice:
    def validateDisk (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Validates the disk specified.
        Disk can be a native volume or clone

        @param diskguid:                   Guid of the disk to validate.
        @type  diskguid:                   guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'validateDisk', params, jobguid=jobguid, executionparams=executionparams)

    def initStorageNode (self, cloudserviceguid, storagenodeguid, jobguid = "", executionparams = {}):
        """
        
        Add storagenode to the storagesystem.

        FLOW for dssstore
        #create in drp application(if not exist yet) (from template) dssstoragenode, connect to cloudservice
        # install required dss qpackages on pmachine
        #for each disk create a storagedaemon
        ##create storagedaemon apps in DRP and attach to relevant dssstoragenode application & relevant dssstoragenode pmachine
        ##register in drp that each storagedaemon delivers service to relevant disk
        #format required partition for each storage daemon (for first disk a small bootpartition cannot be used), take into consideration there can be existing partitions for DSS
        #make sure daemons are autostarting (copy tasklets into autostart scheduler)
        #start daemons
        #check daemons are really running, update DRP with status
        
        #

        @param storagenodeguid:            guid of pmachine which will become storage node
        @type  machineguid:                guid

        @param cloudserviceguid:           guid of application in drp but used as cloudservice
        @type  applicationguid:            guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['storagenodeguid'] = storagenodeguid
        params['cloudserviceguid'] = cloudserviceguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'initStorageNode', params, jobguid=jobguid, executionparams=executionparams)

    def deleteDisk (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Deletes the disk specified.
        Disk can be a native volume, snapshot or clone.

        @param diskguid:                   Guid of the disk to delete.
        @type  diskguid:                   guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'deleteDisk', params, jobguid=jobguid, executionparams=executionparams)

    def exportDisk (self, diskguid, destinationuri, executormachineguid = "", compressed = True, imagetype = "VDI", jobguid = "", executionparams = {}):
        """
        
        Export specified disk as an image on defined destination.

        FLOW
        # use q.system.cloudfs... functions

        @note: Based on the extension of the destination file, the VDI will be compressed or not. (e.g  when destination is .vdi.gz then image will be gzipped)

        @param diskguid:               Guid of the disk to export.
        @type diskguid:                guid

        @param destinationuri:         URI of the location where the VDI should be stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/10_20_2008_volImage_C_drive.vdi.gz)
        @type destinationuri:          string

        @param executormachineguid:    Guid of the machine which should convert the disk to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:     guid

        @param compressed:             Boolean indicating if the image should be compressed or not. Compression used is 7zip
        @type compressed:              boolean

        @param imagetype:              Type of the image format (VDI, RAW, VMDK, ...)
        @type imagetype:               string

        @param jobguid:                Guid of the job
        @type jobguid:                 guid

        @param executionParams:        dictionary with additional executionParams
        @type executionParams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['destinationuri'] = destinationuri
        params['imagetype'] = imagetype
        params['diskguid'] = diskguid
        params['compressed'] = compressed
        params['executormachineguid'] = executormachineguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'exportDisk', params, jobguid=jobguid, executionparams=executionparams)

    def cloneDisk (self, diskguid, destinationdiskguid, jobguid = "", executionparams = {}):
        """
        
        Clones specified disk of type snapshot to new existing disk
        Disk must be a be a disk of type snapshot, destination disk must be a disk of type clone

        @param diskguid:                   Guid of the snapshot disk to clone.
        @type  diskguid:                   guid

        @param destinationdiskguid:        Guid of the destination disk.
        @type  destinationdiskguid:        guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        params['destinationdiskguid'] = destinationdiskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'cloneDisk', params, jobguid=jobguid, executionparams=executionparams)

    def snapshotDisk (self, snapshots = [], machineagentguid = "", jobguid = "", executionparams = {}):
        """
        
        Snapshots specified disks
        Disk can be a nativevolume or clone

        @param snapshots:                  list of disks to snapshot {'snapshotguid': , 'volumeid': , 'disktype': , 'diskguid'}
        @type  snapshots:                  list

        @param machineagentguid:           Guid of the machine agent
        @type  machineagentguid:           guid
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineagentguid'] = machineagentguid
        params['snapshots'] = snapshots
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'snapshotDisk', params, jobguid=jobguid, executionparams=executionparams)

    def unexposeDisk (self, diskguid, protocol = "", jobguid = "", executionparams = {}):
        """
        
        Find iscsi (or alternative protocol) target and unexposes the disk specified, make changes in DRP

        @param diskguid:               Guid of the disk on which the VDI will be imported.
        @type diskguid:                guid

        @param jobguid:                Guid of the job
        @type jobguid:                 guid

        @param executionParams:        dictionary with additional executionParams
        @type executionParams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['protocol'] = protocol
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'unexposeDisk', params, jobguid=jobguid, executionparams=executionparams)

    def optimizeDisk (self, diskguid, scrubagentmachineguid, directorip = "", directorport = "", jobguid = "", executionparams = {}):
        """
        
        Removes unwanted data for the disk specified.
        Disk can be a native volume or clone.

        @param diskguid:                   Guid of the disk to validate.
        @type  diskguid:                   guid
        
        @param scrubagentmachineguid:      guid of the machine where scrubbing agent is running
        @type scrubagentmachineguid:       guid
        
        @param directorip:                 IP adress of the dss director
        @type directorip:                  string

        @param directorport:               Port of the dss director
        @type directorport:                string

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @todo:                             Will be implemented in phase2
        
	"""
        params =dict()
        params['scrubagentmachineguid'] = scrubagentmachineguid
        params['diskguid'] = diskguid
        params['directorport'] = directorport
        params['directorip'] = directorip
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'optimizeDisk', params, jobguid=jobguid, executionparams=executionparams)

    def createDisk (self, diskguid, disksafetytype = "", jobguid = "", executionparams = {}):
        """
        
        Creates a disk (volume) on the storage system and connects it to the volumestorageclient
        Disk is always a native volume.

        @param diskguid:                   Guid of the disk to create.
        @type  diskguid:                   guid
        
        @param disksafetytype:             Type of disk safety (SSO,MIRRORCLOUD...)
        @type disksafetytype:              string

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['disksafetytype'] = disksafetytype
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'createDisk', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, applicationguid = "", servicename = "", jobguid = "", executionparams = {}):
        """
        
        FLOW for dssstore
        #
        #configure dssdirector on mgmtcpunode, model dssdirector as application underneath cloudservice dssstore
        #for all known storagenodes of this specified storageservice cloudservice call actor volumestorageserver.initStorageNode()
        #for all known cpu nodes of this specified storageservice cloudservice call actor volumestorageclient.initialize()

        @param servicename:                name for service (there can be more storageservices)
        @type servicename:                 string

        @param applicationguid:            Guid of the application which needs to be initialized
        @type  applicationguid:            guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        params['servicename'] = servicename
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def exposeDisk (self, diskguid, protocol = "iscsi", ipaddress = "", machineguid = "", jobguid = "", executionparams = {}):
        """
        
        Exposes the specified disk over iscsi (or alternative protocol) on a cpu node which has capacity.

        FLOW for dss
        # check if already iscsitarget appliction in DRP which exposes this disk
        # if not: select random pmachine
        ## for that pmachine in drp create an application iscsitarget (from template)
        ## call actor iscsiTarget.init(...
        # if yes: fetch guid for iscsitargetapplicationguid
        # call actor iscsitarget.attachvolume(iscsitargetapplicationguid,diskguid)  #makes sure application iscsitarget delivers service to disk (is vmachinedisk)

        @param diskguid:               Guid of the disk on which the VDI will be imported.
        @type diskguid:                guid

        @param protocol:               Protocol only "iscsi" supported for now
        @type protocol:                string

        @param machineguid:            Guid of the machine which should expose the disk. If you want to overrule the location where it needs to be exposed, when not specified will be CPU node with most resource available (not for all storage systems relevant)
        @type machineguid:             guid

        @param ipaddress:               ip address allowed to connect to the iscsi target
        @type ipaddress:                string

        @param jobguid:                Guid of the job
        @type jobguid:                 guid

        @param executionParams:        dictionary with additional executionParams
        @type executionParams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['ipaddress'] = ipaddress
        params['protocol'] = protocol
        params['diskguid'] = diskguid
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'exposeDisk', params, jobguid=jobguid, executionparams=executionparams)

    def removeStorageNode (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        # flow for DSS
        # Put all storage daemon applications that were on this storage daemon in state ABANDONNED

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'removeStorageNode', params, jobguid=jobguid, executionparams=executionparams)

    def copyDisk (self, diskguid, destinationdiskguid, jobguid = "", executionparams = {}):
        """
        
        Copies specified disk to new existing disk
        Disk can be a snapshot or already a clone

        FLOW
        # use q.system.cloudfs... functions

        @param diskguid:                   Guid of the snapshot disk to clone.
        @type  diskguid:                   guid

        @param destinationdiskguid:        Guid of the destination disk.
        @type  destinationdiskguid:        guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
        @todo:                             Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        params['destinationdiskguid'] = destinationdiskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'copyDisk', params, jobguid=jobguid, executionparams=executionparams)

    def importDisk (self, sourceuri, diskguid, executormachineguid = "", compressed = True, type = "VDI", jobguid = "", executionparams = {}):
        """
        
        Import specified image on a disk.

        FLOW
        # use q.system.cloudfs... functions

        @warning: The data on the disk will be removed.

        @note: Based on the extension of the source file, the VDI will be decompressed or not. (e.g  when source is .vdi.gz then image will be unzipped)

        @param sourceuri:              URI of the location from where the VDI should be imported. (e.g ftp://login:passwd@myhost.com/backups/machinex/10_20_2008_volImage_C_drive.vdi.gz)
        @type sourceuri:               string

        @param diskguid:               Guid of the disk on which the VDI will be imported.
        @type diskguid:                guid

        @param executormachineguid:    Guid of the machine which should convert the VDI to the disk. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:     guid

        @param compressed:             Boolean indicating if the image should be compressed or not. Compression used is 7zip
        @type compressed:              boolean

        @param imagetype:              Type of the image format (VDI, RAW, VMDK, ...)
        @type imagetype:               string

        @param jobguid:                Guid of the job
        @type jobguid:                 guid

        @param executionParams:        dictionary with additional executionParams
        @type executionParams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['type'] = type
        params['diskguid'] = diskguid
        params['executormachineguid'] = executormachineguid
        params['sourceuri'] = sourceuri
        params['compressed'] = compressed
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'importDisk', params, jobguid=jobguid, executionparams=executionparams)

    def rollbackDisk (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Restores the snapshot specified on the parent disk of the snapshot, all more recent data of the parent disk is removed
        Result is native disk or clone

        @param diskguid:                   Guid of the snapshot disk to rollback.
        @type  diskguid:                   guid
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        return q.workflowengine.actionmanager.startActorAction('volumestorageservice', 'rollbackDisk', params, jobguid=jobguid, executionparams=executionparams)


