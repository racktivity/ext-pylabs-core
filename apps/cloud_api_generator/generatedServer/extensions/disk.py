from cloud_api_rootobjects import cloud_api_disk

class disk:

    def __init__(self):
        self._rootobject = cloud_api_disk.disk()

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
        result = self._rootobject.restore(backupdiskguid,diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.canRollback(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.getObject(rootobjectguid,jobguid,executionparams)

        from osis import ROOTOBJECT_TYPES
        import base64
        from osis.model.serializers import ThriftSerializer
        result = base64.decodestring(result['result'])
        result = ROOTOBJECT_TYPES['disk'].deserialize(ThriftSerializer, result)
        return result


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
        result = self._rootobject.listExportedImages(diskguid,cloudspaceguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.getLatestSnapshot(diskguid,consistent,jobguid,executionparams)
        return result


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
        result = self._rootobject.cloneToNewDisk(diskguid,name,description,jobguid,executionparams)
        return result


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
        result = self._rootobject.listClones(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.find(name,machineguid,disktype,windowsdiskname,devicename,sizefrommb,sizetomb,compressiontype,disklifecycletype,templatediskguid,iqn,status,role,backuplabel,parentdiskguid,id,jobguid,executionparams)
        return result


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
        result = self._rootobject.iscsiUnExpose(diskguid,protocol,jobguid,executionparams)
        return result


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
        result = self._rootobject.listSnapshots(diskguid,timestampfrom,timestampuntil,jobguid,executionparams)
        return result


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
        result = self._rootobject.cloneToExistingDisk(diskguid,destinationdiskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.iscsiExpose(diskguid,targetIQN,username,password,initiatorIQN,ipaddress,jobguid,executionparams)
        return result


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
        result = self._rootobject.addPartitionFromImage(diskguid,imageuri,filesystemtype,imagechecksum,size,order,boot,backup,label,mountpoint,jobguid,executionparams)
        return result


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
        result = self._rootobject.copyToExistingDisk(diskguidsource,diskguiddestination,jobguid,executionparams)
        return result


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
        result = self._rootobject.listUnmanagedDisks(jobguid,executionparams)
        return result


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
        result = self._rootobject.updateModelProperties(diskguid,name,description,timestamp,id,iqn,devicename,status,disktype,diskorder,backendsize,dsspolicyguid,failovercachestatus,jobguid,executionparams)
        return result


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
        result = self._rootobject.removeFilesystem(diskguid,order,jobguid,executionparams)
        return result


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
        result = self._rootobject.moveFailovercacheToMachine(diskguid,machineguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.setWindowsDiskName(diskguid,windowsdiskname,jobguid,executionparams)
        return result


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
        result = self._rootobject.importImage(sourceuri,diskguid,executormachineguid,compressed,type,jobguid,executionparams)
        return result


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
        result = self._rootobject.removePartition(diskguid,order,jobguid,executionparams)
        return result


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
        result = self._rootobject.rollback(snapshotguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.createTemplate(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.moveToMachine(diskguid,machineguid,failover,jobguid,executionparams)
        return result


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
        result = self._rootobject.addPartition(diskguid,size,order,boot,backup,info,filesystem,label,mountpoint,jobguid,executionparams)
        return result


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
        result = self._rootobject.listBackups(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.exportImage(diskguid,destinationuri,executormachineguid,compressed,imagetype,jobguid,executionparams)
        return result


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
        result = self._rootobject.listPartitions(diskguid,label,jobguid,executionparams)
        return result


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
        result = self._rootobject.applyTemplate(diskguid,templateguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.getXML(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.optimize(diskguid,scrubagentmachineguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.addFilesystem(diskguid,order,filesystemtype,devicename,mountpoint,label,jobguid,executionparams)
        return result


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
        result = self._rootobject.getXMLSchema(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.canDelete(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.copyToNewDisk(diskguid,size,diskrole,jobguid,executionparams)
        return result


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
        result = self._rootobject.list(diskguid,name,template,jobguid,executionparams)
        return result


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
        result = self._rootobject.setSnapshotRetentionPolicy(diskguid,policyguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.getYAML(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.addRaidConfigurationToPartition(diskguid,partitionorder,level,state,devices,activeDevices,failedDevices,spareDevices,totalDevices,raidDevices,backendSize,jobguid,executionparams)
        return result


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
        result = self._rootobject.snapshot(diskguid,snapshotname,label,automated,async,jobguid,executionparams)
        return result


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
        result = self._rootobject.getConfigurationString(diskguid,jobguid,executionparams)
        return result


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
        result = self._rootobject.backup(diskguid,backupname,jobguid,executionparams)
        return result


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
        result = self._rootobject.create(machineguid,name,size,diskrole,diskorder,retentionpolicyguid,description,disksafetytype,jobguid,executionparams)
        return result


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
        result = self._rootobject.delete(diskguid,jobguid,executionparams)
        return result


