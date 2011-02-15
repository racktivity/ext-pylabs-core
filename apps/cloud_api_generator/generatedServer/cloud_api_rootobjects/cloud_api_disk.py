from pylabs import q

class disk:
    def restore (self, backupdiskguid, diskguid, jobguid = "", executionparams = {}):
        """
        
        Restores a backup from a disk to another disk.

        @warning: All data on the destination disk will be removed. All partitions and filesystems of the source disk will be copied to the destination disk.

        @param backupdiskguid:          guid of the backup to restore all data from.
        @type backupdiskguid:           guid

        @param diskguid:                guid of the disk to restore all data to.
        @type diskguid:                 guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with array of disk info as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['backupdiskguid'] = backupdiskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'restore', params, jobguid=jobguid, executionparams=executionparams)

    def canRollback (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Checks whether snapshots that are more recent have clones. If so, rollback is disallowed

        @param diskguid:          guid of the snapshot to check.
        @type diskguid:           guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'canRollback', params, jobguid=jobguid, executionparams=executionparams)

    def getObject (self, rootobjectguid, jobguid = "", executionparams = {}):
        """
        
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:    guid of the disk rootobject
        @type rootobjectguid:     guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  rootobject
        @rtype:                   string

        @warning:                 Only usable using the python client.
        
	"""
        params =dict()
        params['rootobjectguid'] = rootobjectguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'getObject', params, jobguid=jobguid, executionparams=executionparams)

    def listExportedImages (self, diskguid, cloudspaceguid = "", jobguid = "", executionparams = {}):
        """
        
        Gets a the list of exported disk images on the systemNAS for a specific disk

        @param diskguid:          guid of the disk rootobject
        @type diskguid:           guid

        @param cloudspaceguid:    guid of the disk rootobject
        @type cloudspaceguid:     guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  list of exported images.
        @rtype:                   array

        @raise e:                 In case an error occurred, exception is raised              
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['cloudspaceguid'] = cloudspaceguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'listExportedImages', params, jobguid=jobguid, executionparams=executionparams)

    def getLatestSnapshot (self, diskguid, consistent = False, jobguid = "", executionparams = {}):
        """
        
        List the snapshots for a given disk.

        @execution_method = sync
        
        @param diskguid:             guid of the disk to list the snapshots from.
        @type  diskguid:             guid

        @param consistent:           boolean to specify snapshot consistency flag.
        @type  consistent:           boolean

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with snapshot disk info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['consistent'] = consistent
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'getLatestSnapshot', params, jobguid=jobguid, executionparams=executionparams)

    def cloneToNewDisk (self, diskguid, name = "", description = "", jobguid = "", executionparams = {}):
        """
        
        Clones a snaphot to a new disk.

        @param diskguid:          guid of the snapshot to clone.
        @type diskguid:           guid

        @param name: 		      name given to the new disk
        @type name:		          string

        @param description:   	  description given to the new disk
        @type description:	      string

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['name'] = name
        params['description'] = description
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'cloneToNewDisk', params, jobguid=jobguid, executionparams=executionparams)

    def listClones (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        List the clones for a given disk.

        @execution_method = sync
        
        @param diskguid:             guid of the disk to list the snapshots from.
        @type  diskguid:             guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of snapshot disks info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'listClones', params, jobguid=jobguid, executionparams=executionparams)

    def find (self, name = None, machineguid = None, disktype = None, windowsdiskname = None, devicename = None, sizefrommb = None, sizetomb = None, compressiontype = None, disklifecycletype = None, templatediskguid = None, iqn = None, status = None, role = None, backuplabel = None, parentdiskguid = None, id = None, jobguid = "", executionparams = {}):
        """
        
        Returns a list of disk guids which met the find criteria.

        @execution_method = sync
        
        @param name:                    Name of the disk.
        @type name:                     string

        @param machineguid:             guid of the machine the disk is part of.
        @type machineguid:              guid

        @param disktype:                Type of the disk. (DSSVOL, DSSVOLIMAGE, FILE, ...)
        @type disktype:                 string

        @param windowsdiskname:         Name of the windows disk.
        @type windowsdiskname:          string

        @param devicename:              Name of the disk's device
        @type devicename:               string

        @param sizefrommb:              Minimum size of the disk in MB.
        @type sizefrommb:               int

        @param sizetomb:                Maxinum size of the disk in MB.
        @type sizetomb:                 int

        @param compressiontype:         Compression type used on the disk. (NONE, GZIP, SEVENZIP, TARGZIP)
        @type compressiontype:          string

        @param disklifecycletype:       Dikslifecycletype of the disk. (ACTIVE, CLONE, SNAPSHOT, TEMPLATE, TODELETE)
        @type disklifecycletype:        string

        @param templatediskguid:        guid of the disk that was used to create the disk.
        @type templatediskguid:         guid

        @param iqn:                     IQN of the disk.
        @type iqn:                      string

        @param status:                  Status of the disk (ACTIVE, CONFIGURED, CREATED)
        @type status:                   string

        @param role:                    guid of the disk that was used to create the disk.
        @type role:                     guid

        @param backuplabel:             guid of the disk that was used to create the disk.
        @type backuplabel:              guid

        @param parentdiskguid:          guid of the disk's parent disk.
        @type parentdiskguid:           guid
        
        @param id:                      volume id of the disk.
        @type id:                       string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        Array of disk guids which met the find criteria specified.
        @rtype:                         array
        @note:                          Example return value:
        @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['status'] = status
        params['devicename'] = devicename
        params['windowsdiskname'] = windowsdiskname
        params['name'] = name
        params['compressiontype'] = compressiontype
        params['backuplabel'] = backuplabel
        params['parentdiskguid'] = parentdiskguid
        params['sizetomb'] = sizetomb
        params['templatediskguid'] = templatediskguid
        params['disktype'] = disktype
        params['iqn'] = iqn
        params['sizefrommb'] = sizefrommb
        params['disklifecycletype'] = disklifecycletype
        params['role'] = role
        params['id'] = id
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'find', params, jobguid=jobguid, executionparams=executionparams)

    def iscsiUnExpose (self, diskguid, protocol = "iscsi", jobguid = "", executionparams = {}):
        """
        
        Unexposes a disk which is exposed over ISCSI and deletes the ISCSI target.

        @param diskguid:                guid of the ISCSI exposed disk to unexpose.
        @type diskguid:                 guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['protocol'] = protocol
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'iscsiUnExpose', params, jobguid=jobguid, executionparams=executionparams)

    def listSnapshots (self, diskguid, timestampfrom = "", timestampuntil = "", jobguid = "", executionparams = {}):
        """
        
        List the snapshots for a given disk.

        @execution_method = sync
        
        @param diskguid:             guid of the disk to list the snapshots from.
        @type  diskguid:             guid
        
        @param timestampfrom:        Filter snapshots from given timestamp 
        @type timestampfrom:         datetime

        @param timestampuntil:       Filter snapshots until given timestamp
        @type timestampuntil:        datetime

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of snapshot disk info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['timestampfrom'] = timestampfrom
        params['timestampuntil'] = timestampuntil
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'listSnapshots', params, jobguid=jobguid, executionparams=executionparams)

    def cloneToExistingDisk (self, diskguid, destinationdiskguid, jobguid = "", executionparams = {}):
        """
        
        Clones a snapshot to an existing disk. The existing disk is deleted. Then the clone is created with the same guid as the existing disk.

        @param diskguid:           Guid of the disk to clone
        @type diskguid:            guid
        
        @param destinationdiskguid: Guid of the destination disk
        @type destinationdiskguid:  guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['destinationdiskguid'] = destinationdiskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'cloneToExistingDisk', params, jobguid=jobguid, executionparams=executionparams)

    def iscsiExpose (self, diskguid, targetIQN = "", username = "", password = "", initiatorIQN = "", ipaddress = "", jobguid = "", executionparams = {}):
        """
        
        Exposes a disk over iscsi on a cpu node which has capacity. Disks can only be exposed once at a time.

        @param diskguid:                guid of the disk to expose over ISCSI.
        @type diskguid:                 guid

        @param username:                Username that is allowed to connect
        @type username:                 string

        @param targetIQN:               iSCSI Qualified Name representing the iscsi target
        @type targetIQN:                string
        
        @param password:                Password of user that is allowed to connect
        @type password:                 string
        
        @param initiatorIQN:            iSCSI Qualified Name allowed to connect
        @type initiatorIQN:             string

        @param ipaddress:               ip address allowed to connect to the iscsi target
        @type ipaddress:                string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with a dictionary with ipaddress and iqn of the ISCSI exposed disk as result and jobguid: {'result': {'diskguid': guid, 'ipaddress': ip, 'iqn': iqn}, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['username'] = username
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['targetIQN'] = targetIQN
        params['initiatorIQN'] = initiatorIQN
        params['password'] = password
        params['ipaddress'] = ipaddress
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'iscsiExpose', params, jobguid=jobguid, executionparams=executionparams)

    def addPartitionFromImage (self, diskguid, imageuri, filesystemtype, imagechecksum = "", size = 0, order = 0, boot = False, backup = False, label = "", mountpoint = "", jobguid = "", executionparams = {}):
        """
        
        Adds a partition to a disk.

        @param diskguid:                guid of the disk rootobject.
        @type diskguid:                 guid

        @param imageuri:                URI of the image to use.
        @type imageuri:                 string

        @param filesystemtype:          Filesystem type used on partition. (EXT2, EXT3, FAT32, LINUX_SWAP, NTFS, REISERFS, XFS)
        @type filesystemtype:           string

        @param imagechecksum:           MD5 Hash of the image to check if the image is correct. No check executed if not specified.
        @type imagechecksum:            string

        @param size:                    Size of the partition in MB. Remaining size on the disk if not specified.
        @type size:                     int

        @param order:                   Partition number. Next available partition number if not specified.
        @type order:                    int

        @param boot:                    Indicate if this is the active partition.
        @type boot:                     boolean

        @param backup:                  Indicate if this is partition should be included in backups.
        @type backup:                   boolean
        
        @param filesystem:              Filesystem of the partition
        @type filesystem:               string

        @param label:                   Label of the partition
        @type label:                    String
        
        @param mountpoint:              Mountpoint of the partition
        @type mountpoint:               string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['filesystemtype'] = filesystemtype
        params['boot'] = boot
        params['imageuri'] = imageuri
        params['imagechecksum'] = imagechecksum
        params['mountpoint'] = mountpoint
        params['label'] = label
        params['backup'] = backup
        params['order'] = order
        params['size'] = size
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'addPartitionFromImage', params, jobguid=jobguid, executionparams=executionparams)

    def copyToExistingDisk (self, diskguidsource, diskguiddestination, jobguid = "", executionparams = {}):
        """
        
        Copies all data from one disk to another.

        @warning: All data on the destination disk will be removed. All partitions and filesystems of the source disk will be copied to the destination disk.

        @param diskguidsource:          guid of the disk to copy all data from.
        @type diskguidsource:           guid

        @param diskguiddestination:     guid of the disk to copy all data to.
        @type diskguiddestination:      guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised

        @todo:                          Will be implemented in phase 2.
        
	"""
        params =dict()
        params['diskguidsource'] = diskguidsource
        params['diskguiddestination'] = diskguiddestination
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'copyToExistingDisk', params, jobguid=jobguid, executionparams=executionparams)

    def listUnmanagedDisks (self, jobguid = "", executionparams = {}):
        """
        
        Lists the unmanaged disks (Disks not bound to a machine).

        @execution_method = sync
        
        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of unmanaged disks as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised

        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'listUnmanagedDisks', params, jobguid=jobguid, executionparams=executionparams)

    def updateModelProperties (self, diskguid, name = "", description = "", timestamp = "", id = "", iqn = "", devicename = "", status = "", disktype = "", diskorder = "", backendsize = "", dsspolicyguid = "", failovercachestatus = "", jobguid = "", executionparams = {}):
        """
        
        Update basic properties (every parameter which is not passed or passed as empty string is not updated)

        @param diskguid:               guid of the disk specified
        @type diskguid:                guid

        @param name:                   Name for this disk
        @type name:                    string

        @param description:            Description for this disk
        @type description:             string
        
        @param timestamp:              Timestamp of creation date in reality
        @type timestamp:               datetime

        @param id:                     id
        @type id:                      string

        @param iqn:                    iqn for this disk
        @type iqn:                     string

        @param devicename:             devicename for this disk
        @type devicename:              string
        
        @param status:                 status for this disk
        @type status:                  string
        
        @param disktype:               disktype for this disk
        @type disktype:                string
        
        @param diskorder:              Order of the disk
        @type diskorder:               int
        
        @param backendsize:            Backendsize of the disk (eg DSS volumes)
        @type backendsize:             int
        
        @param dsspolicyguid:          guid of the dss policy
        @type dsspolicyguid:           guid
        
        @param failovercachestatus     status of failover cache  (NONE,STANDALONE,DEGRADED or SYNCHRONISED)
        @type failovercachestatus      string
        
        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with disk guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['status'] = status
        params['devicename'] = devicename
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['name'] = name
        params['dsspolicyguid'] = dsspolicyguid
        params['timestamp'] = timestamp
        params['diskorder'] = diskorder
        params['disktype'] = disktype
        params['iqn'] = iqn
        params['failovercachestatus'] = failovercachestatus
        params['backendsize'] = backendsize
        params['id'] = id
        params['description'] = description
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'updateModelProperties', params, jobguid=jobguid, executionparams=executionparams)

    def removeFilesystem (self, diskguid, order, jobguid = "", executionparams = {}):
        """
        
        Removes a filesystem from a partition.

        @param diskguid:                guid of the disk rootobject.
        @type diskguid:                 guid

        @param order:                   Partition number.
        @type order:                    int

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['order'] = order
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'removeFilesystem', params, jobguid=jobguid, executionparams=executionparams)

    def moveFailovercacheToMachine (self, diskguid, machineguid, jobguid = "", executionparams = {}):
        """
        
        Move failover cache for a disk from one machine to another.

        @param diskguid:                guid of the disk for which to move the failover cache.
        @type diskguid:                 guid

        @param machineguid:             guid of the machine to move the failover cache to.
        @type machineguid:              guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'moveFailovercacheToMachine', params, jobguid=jobguid, executionparams=executionparams)

    def setWindowsDiskName (self, diskguid, windowsdiskname, jobguid = "", executionparams = {}):
        """
        
        Set windows name for disk
        Can be used to query disks

        @param diskguid:                guid of the disk rootobject.
        @type diskguid:                 guid

        @param windowsdiskname:         Windows disk name  e.g. c:
        @type windowsdiskname:          string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['windowsdiskname'] = windowsdiskname
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'setWindowsDiskName', params, jobguid=jobguid, executionparams=executionparams)

    def importImage (self, sourceuri, diskguid = "", executormachineguid = "", compressed = True, type = "VDI", jobguid = "", executionparams = {}):
        """
        
        Import specified image on a disk.

        @warning: The data on the disk will be removed.

        @note: Based on the extension of the source file, the VDI will be decompressed or not. (e.g  when source is .vdi.gz then image will be unzipped)

        @param sourceuri:              URI of the location from where the VDI should be imported. (e.g ftp://login:passwd@myhost.com/backups/machinex/10_20_2008_volImage_C_drive.vdi.gz)
        @type sourceuri:               string

        @param diskguid:               guid of the disk on which the VDI will be imported.
        @type diskguid:                guid

        @param executormachineguid:    guid of the machine which should convert the VDI to the disk. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:     guid

        @param compressed:             Boolean indicating if the image should be compressed or not. Compression used is 7zip
        @type compressed:              boolean

        @param imagetype:              Type of the image format (VDI, RAW, VMDK, ...)
        @type imagetype:               string

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['type'] = type
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['executormachineguid'] = executormachineguid
        params['sourceuri'] = sourceuri
        params['compressed'] = compressed
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'importImage', params, jobguid=jobguid, executionparams=executionparams)

    def removePartition (self, diskguid, order, jobguid = "", executionparams = {}):
        """
        
        Removes a partition from a disk.

        @param diskguid:                guid of the disk rootobject.
        @type diskguid:                 guid

        @param order:                   Partition number.
        @type order:                    int

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['order'] = order
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'removePartition', params, jobguid=jobguid, executionparams=executionparams)

    def rollback (self, snapshotguid, jobguid = "", executionparams = {}):
        """
        
        Rollback a disk to the given snapshot.

        @param snapshotguid:      guid of the snapshot.
        @type snapshotguid:       guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['snapshotguid'] = snapshotguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'rollback', params, jobguid=jobguid, executionparams=executionparams)

    def createTemplate (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Creates a template from the disk.

        @param diskguid:                guid of the disk to mark as template.
        @type diskguid:                 guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'createTemplate', params, jobguid=jobguid, executionparams=executionparams)

    def moveToMachine (self, diskguid, machineguid, failover = False, jobguid = "", executionparams = {}):
        """
        
        Move a disk from one machine to another. When failovering the disk, the locking mechanism will be bypassed and failover cache be used when possible.

        @warning: The machines to which the disk is currently connected and will be connected to will be rebooted.

        @param diskguid:                guid of the disk to move.
        @type diskguid:                 guid

        @param machineguid:             guid of the machine to move the disk to.
        @type machineguid:              guid
        
        @param failover:                flags whether failover workflow needs to be followed
        @type  failover:                boolean

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['failover'] = failover
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['machineguid'] = machineguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'moveToMachine', params, jobguid=jobguid, executionparams=executionparams)

    def addPartition (self, diskguid, size = 0, order = 0, boot = False, backup = False, info = "", filesystem = "", label = "", mountpoint = "", jobguid = "", executionparams = {}):
        """
        
        Adds a partition to a disk.

        @param diskguid:                guid of the disk rootobject.
        @type diskguid:                 guid

        @param size:                    Size of the partition in MB. Remaining size on the disk if not specified.
        @type size:                     int

        @param order:                   Partition number. Next available partition number if not specified.
        @type order:                    int

        @param boot:                    Indicate if this is the active partition.
        @type boot:                     boolean

        @param backup:                  Indicate if this is partition should be included in backups.
        @type backup:                   boolean
        
        @param info:                    extra information about the partition
        @type info:                     string
        
        @param filesystem:              Filesystem of the partition
        @type filesystem:               string

        @param label:                   Label of the partition
        @type label:                    String
        
        @param mountpoint:              Mountpoint of the partition
        @type mountpoint:               string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['info'] = info
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['boot'] = boot
        params['label'] = label
        params['filesystem'] = filesystem
        params['mountpoint'] = mountpoint
        params['backup'] = backup
        params['order'] = order
        params['size'] = size
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'addPartition', params, jobguid=jobguid, executionparams=executionparams)

    def listBackups (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        List the snapshots for a given disk.

        @execution_method = sync
        
        @param diskguid:             guid of the disk to list the backups from.
        @type  diskguid:             guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'listBackups', params, jobguid=jobguid, executionparams=executionparams)

    def exportImage (self, diskguid, destinationuri, executormachineguid = "", compressed = True, imagetype = "VDI", jobguid = "", executionparams = {}):
        """
        
        Export specified disk as vdi image on defined destination.

        @note: Based on the extension of the destination file, the VDI will be compressed or not. (e.g  when destination is .vdi.gz then image will be gzipped)

        @param diskguid:               guid of the disk to export.
        @type diskguid:                guid

        @param destinationuri:         URI of the location where the VDI should be stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/10_20_2008_volImage_C_drive.vdi.gz)
        @type destinationuri:          string

        @param executormachineguid:    guid of the machine which should convert the disk to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        @type executormachineguid:     guid

        @param compressed:             Boolean indicating if the image should be compressed or not. Compression used is 7zip
        @type compressed:              boolean

        @param imagetype:              Type of the image format (VDI, RAW, VMDK, ...)
        @type imagetype:               string

        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['destinationuri'] = destinationuri
        params['imagetype'] = imagetype
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['compressed'] = compressed
        params['executormachineguid'] = executormachineguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'exportImage', params, jobguid=jobguid, executionparams=executionparams)

    def listPartitions (self, diskguid, label = "", jobguid = "", executionparams = {}):
        """
        
        Lists all partitions on the disk.

        @execution_method = sync
        
        @param diskguid:                guid of the disk to list partitions for.
        @type diskguid:                 guid
        
        @param label:                   label to filter
        @type label:                    string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with partitions info as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                           'result: [{ 'devicename': 'Disk 0',
        @note:                                      'mountpoint': 'C:',
        @note:                                      'type': 'NTFS',
        @note:                                      'backup': True,
        @note:                                      'boot': True,
        @note:                                      'order': 0,
        @note:                                      'size': 10240,
        @note:                                      'status': 'CREATED',
        @note:                                      'imagepath': '',
        @note:                                      'imagechecksum': ''},
        @note:                                      'label': ''},

        @raise e:                       In case an error occurred, exception is raised
        
        @todo:                          Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['label'] = label
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'listPartitions', params, jobguid=jobguid, executionparams=executionparams)

    def applyTemplate (self, diskguid, templateguid, jobguid = "", executionparams = {}):
        """
        
        Applies a template on an existing disk.

        @warning: All data on the disk will be removed.

        @note: In case of a disk with disklifecycle CLONE, the disk will be removed and a new clone of the template disk will be created.

        @param diskguid:             guid of the disk on which the template will be applied.
        @type diskguid:              guid

        @param templateguid:         guid of the template to apply.
        @type templateguid:          guid

        @param jobguid:              guid of the job if avalailable else empty string
        @type jobguid:               guid

        @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:       dictionary

        @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                      dictionary

        @raise e:                    In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['templateguid'] = templateguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'applyTemplate', params, jobguid=jobguid, executionparams=executionparams)

    def getXML (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Gets a string representation in XML format of the disk rootobject.

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
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'getXML', params, jobguid=jobguid, executionparams=executionparams)

    def optimize (self, diskguid, scrubagentmachineguid, jobguid = "", executionparams = {}):
        """
        
        Optimizes a disk. E.g. defragments a Physical disk or scrubs a DSS disks

        @param diskguid:                guid of the disk to optimize.
        @type diskguid:                 guid

        @param scrubagentmachineguid:   guid of the machine where scrubbing agent is running
        @type scrubagentmachineguid:    guid

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['scrubagentmachineguid'] = scrubagentmachineguid
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'optimize', params, jobguid=jobguid, executionparams=executionparams)

    def addFilesystem (self, diskguid, order, filesystemtype, devicename = "", mountpoint = "", label = "", jobguid = "", executionparams = {}):
        """
        
        Adds a filesystem on a partition of a disk.

        @param diskguid:                guid of the disk rootobject.
        @type diskguid:                 guid

        @param order:                   Partition number.
        @type order:                    int

        @param filesystemtype:          Filesystem type used on partition. (EXT2, EXT3,EXT4, FAT32, LINUX_SWAP, NTFS, REISERFS, XFS)
        @type filesystemtype:           string

        @param devicename:              Name of the device of the partition on the OS.
        @type devicename:               string

        @param mountpoint:              Name of the mountpoint of the partition on the OS.
        @type mountpoint:               string
        
        @param label:                   Label of filesystem 
        @type label:                    string

        @param jobguid:                 guid of the job if avalailable else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                         dictionary

        @raise e:                       In case an error occurred, exception is raised

        
	"""
        params =dict()
        params['devicename'] = devicename
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['filesystemtype'] = filesystemtype
        params['label'] = label
        params['mountpoint'] = mountpoint
        params['order'] = order
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'addFilesystem', params, jobguid=jobguid, executionparams=executionparams)

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
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'getXMLSchema', params, jobguid=jobguid, executionparams=executionparams)

    def canDelete (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Checks whether there are clones. If so, deletion is disallowed

        @param diskguid:          guid of the disk to check.
        @type diskguid:           guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with boolean as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'canDelete', params, jobguid=jobguid, executionparams=executionparams)

    def copyToNewDisk (self, diskguid, size, diskrole = "", jobguid = "", executionparams = {}):
        """
        
        Copies the content of the specified disk to a new disk with the given size and the role specified. All data is copied.

        @param diskguid:          guid of the disk to copy all data from.
        @type diskguid:           guid

        @param size:              Size of the new disk in MB. Same size as the source disk if no size specified.
        @type size:               int

        @param diskrole:          Role of the new disk ('BOOT', 'TEMP', 'DATA'). Same role as the source disk of no role specified.
        @type diskrole:           string

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised

        @todo:                    Will be implemented in phase 2
        
	"""
        params =dict()
        params['diskrole'] = diskrole
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['size'] = size
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'copyToNewDisk', params, jobguid=jobguid, executionparams=executionparams)

    def list (self, diskguid = "", name = "", template = "", jobguid = "", executionparams = {}):
        """
        
        Gets a the list of diks

        @execution_method = sync
        
        @param diskguid:          guid of the disk rootobject
        @type diskguid:           guid

        @param name:              name of the disk
        @type name:               string

        @param template:          disk is template
        @type template:           bool

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with array of disk info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised              
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['name'] = name
        params['template'] = template
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'list', params, jobguid=jobguid, executionparams=executionparams)

    def setSnapshotRetentionPolicy (self, diskguid, policyguid, jobguid = "", executionparams = {}):
        """
        
        Sets the snapshot retention policy for disk

        @param diskguid:                   guid of the disk to set retention policy.
        @type diskguid:                    guid
        
        @param policyguid:                 guid of the retention policy to set
        @type policyguid:                  guid

        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['policyguid'] = policyguid
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'setSnapshotRetentionPolicy', params, jobguid=jobguid, executionparams=executionparams)

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
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('disk', 'getYAML', params, jobguid=jobguid, executionparams=executionparams)

    def addRaidConfigurationToPartition (self, diskguid, partitionorder = "", level = "", state = "", devices = "", activeDevices = "", failedDevices = "", spareDevices = "", totalDevices = "", raidDevices = "", backendSize = "", jobguid = "", executionparams = {}):
        """
        
        Set raid configuration to partition
        
        @param diskguid:                   guid of the disk to set raid configuration on partition
        @type diskguid:                    guid
        
        @param partitionorder:             order of the partition
        @type partitionorder:              integer
        
        @param level:                      raid level
        @type level:                       string
        
        @param state:                      state of raid configuration
        @type state:                       string
        
        @param devices:                    devices of raid configuration
        @type devices:                     string
        
        @param activeDevices:              number of active devices
        @type activeDevices:               integer
        
        @param failedDevices:              number of failed devices
        @type failedDevices:               integer
        
        @param spareDevices:               number of spare devices
        @type spareDevices:                integer
        
        @param totalDevices:               number of total devices
        @type totalDevices:                integer
        
        @param raidDevices:                number of raid devices
        @type raidDevices:                 integer
        
        @param backendSize:                sum of all partition sizes the raid device is build on
        @type backendSize:                 integer
        
        @param jobguid:                    guid of the job if avalailable else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:
        
	"""
        params =dict()
        params['activeDevices'] = activeDevices
        params['totalDevices'] = totalDevices
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['level'] = level
        params['raidDevices'] = raidDevices
        params['devices'] = devices
        params['state'] = state
        params['partitionorder'] = partitionorder
        params['spareDevices'] = spareDevices
        params['backendSize'] = backendSize
        params['failedDevices'] = failedDevices
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'addRaidConfigurationToPartition', params, jobguid=jobguid, executionparams=executionparams)

    def snapshot (self, diskguid, snapshotname = "", label = "", automated = False, async = False, jobguid = "", executionparams = {}):
        """
        
        Create a snapshot with given name of the disk.

        @param diskguid:          guid of the disk rootobject
        @type diskguid:           guid

        @param snapshotname:      Name for the snapshot. If no name provided, a name will be generated based on the disk name and current date/time.
        @type snapshotname:       string

        @param label:             label for the snapshot
        @type label:              string
        
        @param async:             Flags whether the snapshot will be taken asynchronically afterwards (by calling the sso.snapshotmachine method)
        @type async:              boolean

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param automated:         Flag if snapshot was taken manually or scheduled
        @type automated:          boolean
        
        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with snapshotguid as result and jobguid: {'result': snapshotguid, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['snapshotname'] = snapshotname
        params['automated'] = automated
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['async'] = async
        params['label'] = label
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'snapshot', params, jobguid=jobguid, executionparams=executionparams)

    def getConfigurationString (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Generate the configuration string for the given disk 

        @param diskguid:          guid of the disk
        @type diskguid:           guid

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  string containing configuration data
        @rtype:                   string

        @raise e:                 In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'getConfigurationString', params, jobguid=jobguid, executionparams=executionparams)

    def backup (self, diskguid, backupname = "", jobguid = "", executionparams = {}):
        """
        
        Create a backup with given name of the disk.

        @param diskguid:          guid of the disk rootobject
        @type diskguid:           guid

        @param backupname:        Name for the backup. If no name provided, a name will be generated based on the current date/time.
        @type backupname:         string

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        @rtype:                   dictionary

        @raise e:                 In case an error occurred, exception is raised
        
        @todo:                    Will be implemented in phase2
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        params['backupname'] = backupname
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'backup', params, jobguid=jobguid, executionparams=executionparams)

    def create (self, machineguid, name, size, diskrole, diskorder = "", retentionpolicyguid = "", description = "", disksafetytype = "", jobguid = "", executionparams = {}):
        """
        
        Create a new disk with the given name, size and the role specified.

        @param machineguid:            guid of the machine rootobject to which this disk belongs
        @type machineguid:             guid

        @param name:                   name given to the disk
        @type name:                    string
        
        @param size:                   Size of disk in MB
        @type size:                    int

        @param diskrole:               Role of the disk ('BOOT', 'TEMP','SSDTEMP', 'DATA')
        @type diskrole:                string
        
        @param diskorder:              Order of the disk
        @type diskorder:               int
        
        @param retentionpolicyguid:    Policy to be used for retention of snapshots
        @type retentionpolicyguid:     guid
        
        @param description:            Description for the disk
        @type description:             string
        
        @param disksafetytype:        Type of disk safety (SSO,MIRRORCLOUD...)
        @type disksafetytype:         string
        
        @param jobguid:                guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with diskguid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['disksafetytype'] = disksafetytype
        params['name'] = name
        params['description'] = description
        params['diskorder'] = diskorder
        params['retentionpolicyguid'] = retentionpolicyguid
        params['diskrole'] = diskrole
        params['machineguid'] = machineguid
        params['size'] = size
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'create', params, jobguid=jobguid, executionparams=executionparams)

    def delete (self, diskguid, jobguid = "", executionparams = {}):
        """
        
        Delete a disk.

        @param diskguid:           guid of the disk rootobject
        @type diskguid:            guid

        @param jobguid:  	       guid of the job if avalailable else empty string
        @type jobguid:   	       guid

        @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:     dictionary

        @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                    dictionary

        @raise e:                  In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        executionparams['rootobjectguid'] = diskguid
        executionparams['rootobjecttype'] = 'disk'

        
        return q.workflowengine.actionmanager.startRootobjectAction('disk', 'delete', params, jobguid=jobguid, executionparams=executionparams)


