
package com.aserver.flex.lib.CloudApi
{
    import flash.events.EventDispatcher;
    import mx.rpc.events.FaultEvent;
    import mx.rpc.Fault;
    import mx.rpc.events.ResultEvent;
    import org.idmedia.as3commons.util.HashMap;
    import mx.rpc.remoting.mxml.RemoteObject;

    public class Disk extends EventDispatcher
    {
        private var srv:CloudApiAMFService = new CloudApiAMFService();
        private var service:String = 'cloud_api_disk';
        public const EVENTTYPE_ERROR:String = 'request_failed';

        public function Disk()
        {
        }
        private function getError(error:*):void
        {
            this.dispatchEvent(new FaultEvent(EVENTTYPE_ERROR,true, false, new Fault(error.code, error.level, error.description)));
            srv.disconnect();
        }


        public const EVENTTYPE_RESTORE:String = 'restore_response';
        /**
        *         Restores a backup from a disk to another disk.
        *         @warning: All data on the destination disk will be removed. All partitions and filesystems of the source disk will be copied to the destination disk.
        *         @param backupdiskguid:          guid of the backup to restore all data from.
        *         @type backupdiskguid:           guid
        *         @param diskguid:                guid of the disk to restore all data to.
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with array of disk info as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function restore (backupdiskguid:String,diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'restore', restore_ResultReceived, getError, backupdiskguid,diskguid,jobguid,executionparams);

        }

        private function restore_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_RESTORE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CANROLLBACK:String = 'canRollback_response';
        /**
        *         Checks whether snapshots that are more recent have clones. If so, rollback is disallowed
        *         @param diskguid:          guid of the snapshot to check.
        *         @type diskguid:           guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function canRollback (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'canRollback', canRollback_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function canRollback_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CANROLLBACK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETOBJECT:String = 'getObject_response';
        /**
        *         Gets the rootobject.
        *         @execution_method = sync
        *         
        *         @param rootobjectguid:    guid of the disk rootobject
        *         @type rootobjectguid:     guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  rootobject
        *         @rtype:                   string
        *         @warning:                 Only usable using the python client.
        *         
        */
        public function getObject (rootobjectguid:String,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getObject', getObject_ResultReceived, getError, rootobjectguid,jobguid,executionparams);

        }

        private function getObject_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETOBJECT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTEXPORTEDIMAGES:String = 'listExportedImages_response';
        /**
        *         Gets a the list of exported disk images on the systemNAS for a specific disk
        *         @param diskguid:          guid of the disk rootobject
        *         @type diskguid:           guid
        *         @param cloudspaceguid:    guid of the disk rootobject
        *         @type cloudspaceguid:     guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  list of exported images.
        *         @rtype:                   array
        *         @raise e:                 In case an error occurred, exception is raised              
        *         
        */
        public function listExportedImages (diskguid:String,cloudspaceguid:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listExportedImages', listExportedImages_ResultReceived, getError, diskguid,cloudspaceguid,jobguid,executionparams);

        }

        private function listExportedImages_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTEXPORTEDIMAGES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETLATESTSNAPSHOT:String = 'getLatestSnapshot_response';
        /**
        *         List the snapshots for a given disk.
        *         @execution_method = sync
        *         
        *         @param diskguid:             guid of the disk to list the snapshots from.
        *         @type  diskguid:             guid
        *         @param consistent:           boolean to specify snapshot consistency flag.
        *         @type  consistent:           boolean
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with snapshot disk info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function getLatestSnapshot (diskguid:String,consistent:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getLatestSnapshot', getLatestSnapshot_ResultReceived, getError, diskguid,consistent,jobguid,executionparams);

        }

        private function getLatestSnapshot_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETLATESTSNAPSHOT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CLONETONEWDISK:String = 'cloneToNewDisk_response';
        /**
        *         Clones a snaphot to a new disk.
        *         @param diskguid:          guid of the snapshot to clone.
        *         @type diskguid:           guid
        *         @param name: 		      name given to the new disk
        *         @type name:		          string
        *         @param description:   	  description given to the new disk
        *         @type description:	      string
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function cloneToNewDisk (diskguid:String,name:String="",description:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'cloneToNewDisk', cloneToNewDisk_ResultReceived, getError, diskguid,name,description,jobguid,executionparams);

        }

        private function cloneToNewDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CLONETONEWDISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTCLONES:String = 'listClones_response';
        /**
        *         List the clones for a given disk.
        *         @execution_method = sync
        *         
        *         @param diskguid:             guid of the disk to list the snapshots from.
        *         @type  diskguid:             guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of snapshot disks info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listClones (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listClones', listClones_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function listClones_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTCLONES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_FIND:String = 'find_response';
        /**
        *         Returns a list of disk guids which met the find criteria.
        *         @execution_method = sync
        *         
        *         @param name:                    Name of the disk.
        *         @type name:                     string
        *         @param machineguid:             guid of the machine the disk is part of.
        *         @type machineguid:              guid
        *         @param disktype:                Type of the disk. (DSSVOL, DSSVOLIMAGE, FILE, ...)
        *         @type disktype:                 string
        *         @param windowsdiskname:         Name of the windows disk.
        *         @type windowsdiskname:          string
        *         @param devicename:              Name of the disk's device
        *         @type devicename:               string
        *         @param sizefrommb:              Minimum size of the disk in MB.
        *         @type sizefrommb:               int
        *         @param sizetomb:                Maxinum size of the disk in MB.
        *         @type sizetomb:                 int
        *         @param compressiontype:         Compression type used on the disk. (NONE, GZIP, SEVENZIP, TARGZIP)
        *         @type compressiontype:          string
        *         @param disklifecycletype:       Dikslifecycletype of the disk. (ACTIVE, CLONE, SNAPSHOT, TEMPLATE, TODELETE)
        *         @type disklifecycletype:        string
        *         @param templatediskguid:        guid of the disk that was used to create the disk.
        *         @type templatediskguid:         guid
        *         @param iqn:                     IQN of the disk.
        *         @type iqn:                      string
        *         @param status:                  Status of the disk (ACTIVE, CONFIGURED, CREATED)
        *         @type status:                   string
        *         @param role:                    guid of the disk that was used to create the disk.
        *         @type role:                     guid
        *         @param backuplabel:             guid of the disk that was used to create the disk.
        *         @type backuplabel:              guid
        *         @param parentdiskguid:          guid of the disk's parent disk.
        *         @type parentdiskguid:           guid
        *         
        *         @param id:                      volume id of the disk.
        *         @type id:                       string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        Array of disk guids which met the find criteria specified.
        *         @rtype:                         array
        *         @note:                          Example return value:
        *         @note:                          {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        *         @note:                           'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function find (name:Object=null,machineguid:Object=null,disktype:Object=null,windowsdiskname:Object=null,devicename:Object=null,sizefrommb:Object=null,sizetomb:Object=null,compressiontype:Object=null,disklifecycletype:Object=null,templatediskguid:Object=null,iqn:Object=null,status:Object=null,role:Object=null,backuplabel:Object=null,parentdiskguid:Object=null,id:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'find', find_ResultReceived, getError, name,machineguid,disktype,windowsdiskname,devicename,sizefrommb,sizetomb,compressiontype,disklifecycletype,templatediskguid,iqn,status,role,backuplabel,parentdiskguid,id,jobguid,executionparams);

        }

        private function find_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_FIND, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ISCSIUNEXPOSE:String = 'iscsiUnExpose_response';
        /**
        *         Unexposes a disk which is exposed over ISCSI and deletes the ISCSI target.
        *         @param diskguid:                guid of the ISCSI exposed disk to unexpose.
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function iscsiUnExpose (diskguid:String,protocol:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'iscsiUnExpose', iscsiUnExpose_ResultReceived, getError, diskguid,protocol,jobguid,executionparams);

        }

        private function iscsiUnExpose_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ISCSIUNEXPOSE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTSNAPSHOTS:String = 'listSnapshots_response';
        /**
        *         List the snapshots for a given disk.
        *         @execution_method = sync
        *         
        *         @param diskguid:             guid of the disk to list the snapshots from.
        *         @type  diskguid:             guid
        *         
        *         @param timestampfrom:        Filter snapshots from given timestamp 
        *         @type timestampfrom:         datetime
        *         @param timestampuntil:       Filter snapshots until given timestamp
        *         @type timestampuntil:        datetime
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of snapshot disk info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listSnapshots (diskguid:String,timestampfrom:String="",timestampuntil:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listSnapshots', listSnapshots_ResultReceived, getError, diskguid,timestampfrom,timestampuntil,jobguid,executionparams);

        }

        private function listSnapshots_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTSNAPSHOTS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CLONETOEXISTINGDISK:String = 'cloneToExistingDisk_response';
        /**
        *         Clones a snapshot to an existing disk. The existing disk is deleted. Then the clone is created with the same guid as the existing disk.
        *         @param diskguid:           Guid of the disk to clone
        *         @type diskguid:            guid
        *         
        *         @param destinationdiskguid: Guid of the destination disk
        *         @type destinationdiskguid:  guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function cloneToExistingDisk (diskguid:String,destinationdiskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'cloneToExistingDisk', cloneToExistingDisk_ResultReceived, getError, diskguid,destinationdiskguid,jobguid,executionparams);

        }

        private function cloneToExistingDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CLONETOEXISTINGDISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ISCSIEXPOSE:String = 'iscsiExpose_response';
        /**
        *         Exposes a disk over iscsi on a cpu node which has capacity. Disks can only be exposed once at a time.
        *         @param diskguid:                guid of the disk to expose over ISCSI.
        *         @type diskguid:                 guid
        *         @param username:                Username that is allowed to connect
        *         @type username:                 string
        *         @param targetIQN:               iSCSI Qualified Name representing the iscsi target
        *         @type targetIQN:                string
        *         
        *         @param password:                Password of user that is allowed to connect
        *         @type password:                 string
        *         
        *         @param initiatorIQN:            iSCSI Qualified Name allowed to connect
        *         @type initiatorIQN:             string
        *         @param ipaddress:               ip address allowed to connect to the iscsi target
        *         @type ipaddress:                string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with a dictionary with ipaddress and iqn of the ISCSI exposed disk as result and jobguid: {'result': {'diskguid': guid, 'ipaddress': ip, 'iqn': iqn}, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function iscsiExpose (diskguid:String,targetIQN:String="",username:String="",password:String="",initiatorIQN:String="",ipaddress:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'iscsiExpose', iscsiExpose_ResultReceived, getError, diskguid,targetIQN,username,password,initiatorIQN,ipaddress,jobguid,executionparams);

        }

        private function iscsiExpose_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ISCSIEXPOSE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDPARTITIONFROMIMAGE:String = 'addPartitionFromImage_response';
        /**
        *         Adds a partition to a disk.
        *         @param diskguid:                guid of the disk rootobject.
        *         @type diskguid:                 guid
        *         @param imageuri:                URI of the image to use.
        *         @type imageuri:                 string
        *         @param filesystemtype:          Filesystem type used on partition. (EXT2, EXT3, FAT32, LINUX_SWAP, NTFS, REISERFS, XFS)
        *         @type filesystemtype:           string
        *         @param imagechecksum:           MD5 Hash of the image to check if the image is correct. No check executed if not specified.
        *         @type imagechecksum:            string
        *         @param size:                    Size of the partition in MB. Remaining size on the disk if not specified.
        *         @type size:                     int
        *         @param order:                   Partition number. Next available partition number if not specified.
        *         @type order:                    int
        *         @param boot:                    Indicate if this is the active partition.
        *         @type boot:                     boolean
        *         @param backup:                  Indicate if this is partition should be included in backups.
        *         @type backup:                   boolean
        *         
        *         @param filesystem:              Filesystem of the partition
        *         @type filesystem:               string
        *         @param label:                   Label of the partition
        *         @type label:                    String
        *         
        *         @param mountpoint:              Mountpoint of the partition
        *         @type mountpoint:               string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function addPartitionFromImage (diskguid:String,imageuri:String,filesystemtype:String,imagechecksum:String="",size:Number=0,order:Number=0,boot:Boolean=false,backup:Boolean=false,label:Object=null,mountpoint:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addPartitionFromImage', addPartitionFromImage_ResultReceived, getError, diskguid,imageuri,filesystemtype,imagechecksum,size,order,boot,backup,label,mountpoint,jobguid,executionparams);

        }

        private function addPartitionFromImage_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDPARTITIONFROMIMAGE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_COPYTOEXISTINGDISK:String = 'copyToExistingDisk_response';
        /**
        *         Copies all data from one disk to another.
        *         @warning: All data on the destination disk will be removed. All partitions and filesystems of the source disk will be copied to the destination disk.
        *         @param diskguidsource:          guid of the disk to copy all data from.
        *         @type diskguidsource:           guid
        *         @param diskguiddestination:     guid of the disk to copy all data to.
        *         @type diskguiddestination:      guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase 2.
        *         
        */
        public function copyToExistingDisk (diskguidsource:String,diskguiddestination:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'copyToExistingDisk', copyToExistingDisk_ResultReceived, getError, diskguidsource,diskguiddestination,jobguid,executionparams);

        }

        private function copyToExistingDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_COPYTOEXISTINGDISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTUNMANAGEDDISKS:String = 'listUnmanagedDisks_response';
        /**
        *         Lists the unmanaged disks (Disks not bound to a machine).
        *         @execution_method = sync
        *         
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of unmanaged disks as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listUnmanagedDisks (jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listUnmanagedDisks', listUnmanagedDisks_ResultReceived, getError, jobguid,executionparams);

        }

        private function listUnmanagedDisks_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTUNMANAGEDDISKS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_UPDATEMODELPROPERTIES:String = 'updateModelProperties_response';
        /**
        *         Update basic properties (every parameter which is not passed or passed as empty string is not updated)
        *         @param diskguid:               guid of the disk specified
        *         @type diskguid:                guid
        *         @param name:                   Name for this disk
        *         @type name:                    string
        *         @param description:            Description for this disk
        *         @type description:             string
        *         
        *         @param timestamp:              Timestamp of creation date in reality
        *         @type timestamp:               datetime
        *         @param id:                     id
        *         @type id:                      string
        *         @param iqn:                    iqn for this disk
        *         @type iqn:                     string
        *         @param devicename:             devicename for this disk
        *         @type devicename:              string
        *         
        *         @param status:                 status for this disk
        *         @type status:                  string
        *         
        *         @param disktype:               disktype for this disk
        *         @type disktype:                string
        *         
        *         @param diskorder:              Order of the disk
        *         @type diskorder:               int
        *         
        *         @param backendsize:            Backendsize of the disk (eg DSS volumes)
        *         @type backendsize:             int
        *         
        *         @param dsspolicyguid:          guid of the dss policy
        *         @type dsspolicyguid:           guid
        *         
        *         @param failovercachestatus     status of failover cache  (NONE,STANDALONE,DEGRADED or SYNCHRONISED)
        *         @type failovercachestatus      string
        *         
        *         @param jobguid:                guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with disk guid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function updateModelProperties (diskguid:String,name:String="",description:String="",timestamp:String="",id:String="",iqn:String="",devicename:String="",status:String="",disktype:String="",diskorder:Number=0,backendsize:Number=0,dsspolicyguid:Object=null,failovercachestatus:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'updateModelProperties', updateModelProperties_ResultReceived, getError, diskguid,name,description,timestamp,id,iqn,devicename,status,disktype,diskorder,backendsize,dsspolicyguid,failovercachestatus,jobguid,executionparams);

        }

        private function updateModelProperties_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_UPDATEMODELPROPERTIES, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEFILESYSTEM:String = 'removeFilesystem_response';
        /**
        *         Removes a filesystem from a partition.
        *         @param diskguid:                guid of the disk rootobject.
        *         @type diskguid:                 guid
        *         @param order:                   Partition number.
        *         @type order:                    int
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function removeFilesystem (diskguid:String,order:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removeFilesystem', removeFilesystem_ResultReceived, getError, diskguid,order,jobguid,executionparams);

        }

        private function removeFilesystem_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEFILESYSTEM, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVEFAILOVERCACHETOMACHINE:String = 'moveFailovercacheToMachine_response';
        /**
        *         Move failover cache for a disk from one machine to another.
        *         @param diskguid:                guid of the disk for which to move the failover cache.
        *         @type diskguid:                 guid
        *         @param machineguid:             guid of the machine to move the failover cache to.
        *         @type machineguid:              guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function moveFailovercacheToMachine (diskguid:String,machineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveFailovercacheToMachine', moveFailovercacheToMachine_ResultReceived, getError, diskguid,machineguid,jobguid,executionparams);

        }

        private function moveFailovercacheToMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVEFAILOVERCACHETOMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETWINDOWSDISKNAME:String = 'setWindowsDiskName_response';
        /**
        *         Set windows name for disk
        *         Can be used to query disks
        *         @param diskguid:                guid of the disk rootobject.
        *         @type diskguid:                 guid
        *         @param windowsdiskname:         Windows disk name  e.g. c:
        *         @type windowsdiskname:          string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function setWindowsDiskName (diskguid:String,windowsdiskname:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setWindowsDiskName', setWindowsDiskName_ResultReceived, getError, diskguid,windowsdiskname,jobguid,executionparams);

        }

        private function setWindowsDiskName_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETWINDOWSDISKNAME, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_IMPORTIMAGE:String = 'importImage_response';
        /**
        *         Import specified image on a disk.
        *         @warning: The data on the disk will be removed.
        *         @note: Based on the extension of the source file, the VDI will be decompressed or not. (e.g  when source is .vdi.gz then image will be unzipped)
        *         @param sourceuri:              URI of the location from where the VDI should be imported. (e.g ftp://login:passwd@myhost.com/backups/machinex/10_20_2008_volImage_C_drive.vdi.gz)
        *         @type sourceuri:               string
        *         @param diskguid:               guid of the disk on which the VDI will be imported.
        *         @type diskguid:                guid
        *         @param executormachineguid:    guid of the machine which should convert the VDI to the disk. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:     guid
        *         @param compressed:             Boolean indicating if the image should be compressed or not. Compression used is 7zip
        *         @type compressed:              boolean
        *         @param imagetype:              Type of the image format (VDI, RAW, VMDK, ...)
        *         @type imagetype:               string
        *         @param jobguid:                guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function importImage (sourceuri:String,diskguid:String="",executormachineguid:String="",compressed:Boolean=true,type:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'importImage', importImage_ResultReceived, getError, sourceuri,diskguid,executormachineguid,compressed,type,jobguid,executionparams);

        }

        private function importImage_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_IMPORTIMAGE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_REMOVEPARTITION:String = 'removePartition_response';
        /**
        *         Removes a partition from a disk.
        *         @param diskguid:                guid of the disk rootobject.
        *         @type diskguid:                 guid
        *         @param order:                   Partition number.
        *         @type order:                    int
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function removePartition (diskguid:String,order:Number,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'removePartition', removePartition_ResultReceived, getError, diskguid,order,jobguid,executionparams);

        }

        private function removePartition_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_REMOVEPARTITION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ROLLBACK:String = 'rollback_response';
        /**
        *         Rollback a disk to the given snapshot.
        *         @param snapshotguid:      guid of the snapshot.
        *         @type snapshotguid:       guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function rollback (snapshotguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'rollback', rollback_ResultReceived, getError, snapshotguid,jobguid,executionparams);

        }

        private function rollback_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ROLLBACK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATETEMPLATE:String = 'createTemplate_response';
        /**
        *         Creates a template from the disk.
        *         @param diskguid:                guid of the disk to mark as template.
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function createTemplate (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'createTemplate', createTemplate_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function createTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATETEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_MOVETOMACHINE:String = 'moveToMachine_response';
        /**
        *         Move a disk from one machine to another. When failovering the disk, the locking mechanism will be bypassed and failover cache be used when possible.
        *         @warning: The machines to which the disk is currently connected and will be connected to will be rebooted.
        *         @param diskguid:                guid of the disk to move.
        *         @type diskguid:                 guid
        *         @param machineguid:             guid of the machine to move the disk to.
        *         @type machineguid:              guid
        *         
        *         @param failover:                flags whether failover workflow needs to be followed
        *         @type  failover:                boolean
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function moveToMachine (diskguid:String,machineguid:String,failover:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'moveToMachine', moveToMachine_ResultReceived, getError, diskguid,machineguid,failover,jobguid,executionparams);

        }

        private function moveToMachine_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_MOVETOMACHINE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDPARTITION:String = 'addPartition_response';
        /**
        *         Adds a partition to a disk.
        *         @param diskguid:                guid of the disk rootobject.
        *         @type diskguid:                 guid
        *         @param size:                    Size of the partition in MB. Remaining size on the disk if not specified.
        *         @type size:                     int
        *         @param order:                   Partition number. Next available partition number if not specified.
        *         @type order:                    int
        *         @param boot:                    Indicate if this is the active partition.
        *         @type boot:                     boolean
        *         @param backup:                  Indicate if this is partition should be included in backups.
        *         @type backup:                   boolean
        *         
        *         @param info:                    extra information about the partition
        *         @type info:                     string
        *         
        *         @param filesystem:              Filesystem of the partition
        *         @type filesystem:               string
        *         @param label:                   Label of the partition
        *         @type label:                    String
        *         
        *         @param mountpoint:              Mountpoint of the partition
        *         @type mountpoint:               string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function addPartition (diskguid:String,size:Number=0,order:Number=0,boot:Boolean=false,backup:Boolean=false,info:String="",filesystem:String="",label:Object=null,mountpoint:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addPartition', addPartition_ResultReceived, getError, diskguid,size,order,boot,backup,info,filesystem,label,mountpoint,jobguid,executionparams);

        }

        private function addPartition_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDPARTITION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTBACKUPS:String = 'listBackups_response';
        /**
        *         List the snapshots for a given disk.
        *         @execution_method = sync
        *         
        *         @param diskguid:             guid of the disk to list the backups from.
        *         @type  diskguid:             guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with array of snapshot machine info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function listBackups (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listBackups', listBackups_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function listBackups_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTBACKUPS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_EXPORTIMAGE:String = 'exportImage_response';
        /**
        *         Export specified disk as vdi image on defined destination.
        *         @note: Based on the extension of the destination file, the VDI will be compressed or not. (e.g  when destination is .vdi.gz then image will be gzipped)
        *         @param diskguid:               guid of the disk to export.
        *         @type diskguid:                guid
        *         @param destinationuri:         URI of the location where the VDI should be stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/10_20_2008_volImage_C_drive.vdi.gz)
        *         @type destinationuri:          string
        *         @param executormachineguid:    guid of the machine which should convert the disk to a VDI. If the executormachineguid is empty, a machine will be selected automatically.
        *         @type executormachineguid:     guid
        *         @param compressed:             Boolean indicating if the image should be compressed or not. Compression used is 7zip
        *         @type compressed:              boolean
        *         @param imagetype:              Type of the image format (VDI, RAW, VMDK, ...)
        *         @type imagetype:               string
        *         @param jobguid:                guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function exportImage (diskguid:String,destinationuri:String,executormachineguid:String="",compressed:Boolean=true,imagetype:String="VDI",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'exportImage', exportImage_ResultReceived, getError, diskguid,destinationuri,executormachineguid,compressed,imagetype,jobguid,executionparams);

        }

        private function exportImage_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_EXPORTIMAGE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LISTPARTITIONS:String = 'listPartitions_response';
        /**
        *         Lists all partitions on the disk.
        *         @execution_method = sync
        *         
        *         @param diskguid:                guid of the disk to list partitions for.
        *         @type diskguid:                 guid
        *         
        *         @param label:                   label to filter
        *         @type label:                    string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with partitions info as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        *         @note:                           'result: [{ 'devicename': 'Disk 0',
        *         @note:                                      'mountpoint': 'C:',
        *         @note:                                      'type': 'NTFS',
        *         @note:                                      'backup': True,
        *         @note:                                      'boot': True,
        *         @note:                                      'order': 0,
        *         @note:                                      'size': 10240,
        *         @note:                                      'status': 'CREATED',
        *         @note:                                      'imagepath': '',
        *         @note:                                      'imagechecksum': ''},
        *         @note:                                      'label': ''},
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function listPartitions (diskguid:Object,label:Object=null,jobguid:Object=null,executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'listPartitions', listPartitions_ResultReceived, getError, diskguid,label,jobguid,executionparams);

        }

        private function listPartitions_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LISTPARTITIONS, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_APPLYTEMPLATE:String = 'applyTemplate_response';
        /**
        *         Applies a template on an existing disk.
        *         @warning: All data on the disk will be removed.
        *         @note: In case of a disk with disklifecycle CLONE, the disk will be removed and a new clone of the template disk will be created.
        *         @param diskguid:             guid of the disk on which the template will be applied.
        *         @type diskguid:              guid
        *         @param templateguid:         guid of the template to apply.
        *         @type templateguid:          guid
        *         @param jobguid:              guid of the job if avalailable else empty string
        *         @type jobguid:               guid
        *         @param executionparams:      dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:       dictionary
        *         @return:                     dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                      dictionary
        *         @raise e:                    In case an error occurred, exception is raised
        *         
        */
        public function applyTemplate (diskguid:String,templateguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'applyTemplate', applyTemplate_ResultReceived, getError, diskguid,templateguid,jobguid,executionparams);

        }

        private function applyTemplate_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_APPLYTEMPLATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXML:String = 'getXML_response';
        /**
        *         Gets a string representation in XML format of the disk rootobject.
        *         @param diskguid:                guid of the disk rootobject
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XML representation of the disk
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXML (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXML', getXML_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getXML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_OPTIMIZE:String = 'optimize_response';
        /**
        *         Optimizes a disk. E.g. defragments a Physical disk or scrubs a DSS disks
        *         @param diskguid:                guid of the disk to optimize.
        *         @type diskguid:                 guid
        *         @param scrubagentmachineguid:   guid of the machine where scrubbing agent is running
        *         @type scrubagentmachineguid:    guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function optimize (diskguid:String,scrubagentmachineguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'optimize', optimize_ResultReceived, getError, diskguid,scrubagentmachineguid,jobguid,executionparams);

        }

        private function optimize_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_OPTIMIZE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDFILESYSTEM:String = 'addFilesystem_response';
        /**
        *         Adds a filesystem on a partition of a disk.
        *         @param diskguid:                guid of the disk rootobject.
        *         @type diskguid:                 guid
        *         @param order:                   Partition number.
        *         @type order:                    int
        *         @param filesystemtype:          Filesystem type used on partition. (EXT2, EXT3,EXT4, FAT32, LINUX_SWAP, NTFS, REISERFS, XFS)
        *         @type filesystemtype:           string
        *         @param devicename:              Name of the device of the partition on the OS.
        *         @type devicename:               string
        *         @param mountpoint:              Name of the mountpoint of the partition on the OS.
        *         @type mountpoint:               string
        *         
        *         @param label:                   Label of filesystem 
        *         @type label:                    string
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                         dictionary
        *         @raise e:                       In case an error occurred, exception is raised
        *         
        */
        public function addFilesystem (diskguid:String,order:Number,filesystemtype:String,devicename:String="",mountpoint:String="",label:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addFilesystem', addFilesystem_ResultReceived, getError, diskguid,order,filesystemtype,devicename,mountpoint,label,jobguid,executionparams);

        }

        private function addFilesystem_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDFILESYSTEM, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETXMLSCHEMA:String = 'getXMLSchema_response';
        /**
        *         Gets a string representation in XSD format of the disk rootobject structure.
        *         @execution_method = sync
        *         
        *         @param diskguid:                guid of the disk rootobject
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:          dictionary
        *         @return:                        XSD representation of the disk structure.
        *         @rtype:                         string
        *         @raise e:                       In case an error occurred, exception is raised
        *         @todo:                          Will be implemented in phase2
        *         
        */
        public function getXMLSchema (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getXMLSchema', getXMLSchema_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getXMLSchema_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETXMLSCHEMA, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CANDELETE:String = 'canDelete_response';
        /**
        *         Checks whether there are clones. If so, deletion is disallowed
        *         @param diskguid:          guid of the disk to check.
        *         @type diskguid:           guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with boolean as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function canDelete (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'canDelete', canDelete_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function canDelete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CANDELETE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_COPYTONEWDISK:String = 'copyToNewDisk_response';
        /**
        *         Copies the content of the specified disk to a new disk with the given size and the role specified. All data is copied.
        *         @param diskguid:          guid of the disk to copy all data from.
        *         @type diskguid:           guid
        *         @param size:              Size of the new disk in MB. Same size as the source disk if no size specified.
        *         @type size:               int
        *         @param diskrole:          Role of the new disk ('BOOT', 'TEMP', 'DATA'). Same role as the source disk of no role specified.
        *         @type diskrole:           string
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         @todo:                    Will be implemented in phase 2
        *         
        */
        public function copyToNewDisk (diskguid:String,size:Number,diskrole:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'copyToNewDisk', copyToNewDisk_ResultReceived, getError, diskguid,size,diskrole,jobguid,executionparams);

        }

        private function copyToNewDisk_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_COPYTONEWDISK, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_LIST:String = 'list_response';
        /**
        *         Gets a the list of diks
        *         @execution_method = sync
        *         
        *         @param diskguid:          guid of the disk rootobject
        *         @type diskguid:           guid
        *         @param name:              name of the disk
        *         @type name:               string
        *         @param template:          disk is template
        *         @type template:           bool
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with array of disk info as result and jobguid: {'result': array, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised              
        *         
        */
        public function list (diskguid:String="",name:String="",template:Object=null,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'list', list_ResultReceived, getError, diskguid,name,template,jobguid,executionparams);

        }

        private function list_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_LIST, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SETSNAPSHOTRETENTIONPOLICY:String = 'setSnapshotRetentionPolicy_response';
        /**
        *         Sets the snapshot retention policy for disk
        *         @param diskguid:                   guid of the disk to set retention policy.
        *         @type diskguid:                    guid
        *         
        *         @param policyguid:                 guid of the retention policy to set
        *         @type policyguid:                  guid
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:                          In case an error occurred, exception is raised
        *         
        */
        public function setSnapshotRetentionPolicy (diskguid:String,policyguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'setSnapshotRetentionPolicy', setSnapshotRetentionPolicy_ResultReceived, getError, diskguid,policyguid,jobguid,executionparams);

        }

        private function setSnapshotRetentionPolicy_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SETSNAPSHOTRETENTIONPOLICY, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETYAML:String = 'getYAML_response';
        /**
        *         Gets a string representation in YAML format of the disk rootobject.
        *         @execution_method = sync
        *         
        *         @param diskguid:                guid of the disk rootobject
        *         @type diskguid:                 guid
        *         @param jobguid:                 guid of the job if avalailable else empty string
        *         @type jobguid:                  guid
        *         @return:                        YAML representation of the disk
        *         @rtype:                         string
        *         
        */
        public function getYAML (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getYAML', getYAML_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getYAML_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETYAML, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_ADDRAIDCONFIGURATIONTOPARTITION:String = 'addRaidConfigurationToPartition_response';
        /**
        *         Set raid configuration to partition
        *         
        *         @param diskguid:                   guid of the disk to set raid configuration on partition
        *         @type diskguid:                    guid
        *         
        *         @param partitionorder:             order of the partition
        *         @type partitionorder:              integer
        *         
        *         @param level:                      raid level
        *         @type level:                       string
        *         
        *         @param state:                      state of raid configuration
        *         @type state:                       string
        *         
        *         @param devices:                    devices of raid configuration
        *         @type devices:                     string
        *         
        *         @param activeDevices:              number of active devices
        *         @type activeDevices:               integer
        *         
        *         @param failedDevices:              number of failed devices
        *         @type failedDevices:               integer
        *         
        *         @param spareDevices:               number of spare devices
        *         @type spareDevices:                integer
        *         
        *         @param totalDevices:               number of total devices
        *         @type totalDevices:                integer
        *         
        *         @param raidDevices:                number of raid devices
        *         @type raidDevices:                 integer
        *         
        *         @param backendSize:                sum of all partition sizes the raid device is build on
        *         @type backendSize:                 integer
        *         
        *         @param jobguid:                    guid of the job if avalailable else empty string
        *         @type jobguid:                     guid
        *         @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:             dictionary
        *         @return:                           dictionary with machine True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                            dictionary
        *         @raise e:
        *         
        */
        public function addRaidConfigurationToPartition (diskguid:String,partitionorder:Number=0,level:String="",state:String="",devices:String="",activeDevices:Number=0,failedDevices:Number=0,spareDevices:Number=0,totalDevices:Number=0,raidDevices:Number=0,backendSize:Number=0,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'addRaidConfigurationToPartition', addRaidConfigurationToPartition_ResultReceived, getError, diskguid,partitionorder,level,state,devices,activeDevices,failedDevices,spareDevices,totalDevices,raidDevices,backendSize,jobguid,executionparams);

        }

        private function addRaidConfigurationToPartition_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_ADDRAIDCONFIGURATIONTOPARTITION, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_SNAPSHOT:String = 'snapshot_response';
        /**
        *         Create a snapshot with given name of the disk.
        *         @param diskguid:          guid of the disk rootobject
        *         @type diskguid:           guid
        *         @param snapshotname:      Name for the snapshot. If no name provided, a name will be generated based on the disk name and current date/time.
        *         @type snapshotname:       string
        *         @param label:             label for the snapshot
        *         @type label:              string
        *         
        *         @param async:             Flags whether the snapshot will be taken asynchronically afterwards (by calling the sso.snapshotmachine method)
        *         @type async:              boolean
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param automated:         Flag if snapshot was taken manually or scheduled
        *         @type automated:          boolean
        *         
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with snapshotguid as result and jobguid: {'result': snapshotguid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function snapshot (diskguid:String,snapshotname:String="",label:String="",automated:Boolean=false,async:Boolean=false,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'snapshot', snapshot_ResultReceived, getError, diskguid,snapshotname,label,automated,async,jobguid,executionparams);

        }

        private function snapshot_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_SNAPSHOT, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_GETCONFIGURATIONSTRING:String = 'getConfigurationString_response';
        /**
        *         Generate the configuration string for the given disk 
        *         @param diskguid:          guid of the disk
        *         @type diskguid:           guid
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  string containing configuration data
        *         @rtype:                   string
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        */
        public function getConfigurationString (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'getConfigurationString', getConfigurationString_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function getConfigurationString_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_GETCONFIGURATIONSTRING, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_BACKUP:String = 'backup_response';
        /**
        *         Create a backup with given name of the disk.
        *         @param diskguid:          guid of the disk rootobject
        *         @type diskguid:           guid
        *         @param backupname:        Name for the backup. If no name provided, a name will be generated based on the current date/time.
        *         @type backupname:         string
        *         @param jobguid:           guid of the job if avalailable else empty string
        *         @type jobguid:            guid
        *         @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:    dictionary
        *         @return:                  dictionary with diskguid as result and jobguid: {'result': diskguid, 'jobguid': guid}
        *         @rtype:                   dictionary
        *         @raise e:                 In case an error occurred, exception is raised
        *         
        *         @todo:                    Will be implemented in phase2
        *         
        */
        public function backup (diskguid:String,backupname:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'backup', backup_ResultReceived, getError, diskguid,backupname,jobguid,executionparams);

        }

        private function backup_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_BACKUP, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_CREATE:String = 'create_response';
        /**
        *         Create a new disk with the given name, size and the role specified.
        *         @param machineguid:            guid of the machine rootobject to which this disk belongs
        *         @type machineguid:             guid
        *         @param name:                   name given to the disk
        *         @type name:                    string
        *         
        *         @param size:                   Size of disk in MB
        *         @type size:                    int
        *         @param diskrole:               Role of the disk ('BOOT', 'TEMP','SSDTEMP', 'DATA')
        *         @type diskrole:                string
        *         
        *         @param diskorder:              Order of the disk
        *         @type diskorder:               int
        *         
        *         @param retentionpolicyguid:    Policy to be used for retention of snapshots
        *         @type retentionpolicyguid:     guid
        *         
        *         @param description:            Description for the disk
        *         @type description:             string
        *         
        *         @param disksafetytype:        Type of disk safety (SSO,MIRRORCLOUD...)
        *         @type disksafetytype:         string
        *         
        *         @param jobguid:                guid of the job if avalailable else empty string
        *         @type jobguid:                 guid
        *         @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:         dictionary
        *         @return:                       dictionary with diskguid as result and jobguid: {'result': guid, 'jobguid': guid}
        *         @rtype:                        dictionary
        *         @raise e:                      In case an error occurred, exception is raised
        *         
        */
        public function create (machineguid:String,name:String,size:Number,diskrole:String,diskorder:Number=0,retentionpolicyguid:String="",description:String="",disksafetytype:String="",jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'create', create_ResultReceived, getError, machineguid,name,size,diskrole,diskorder,retentionpolicyguid,description,disksafetytype,jobguid,executionparams);

        }

        private function create_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_CREATE, false, false, e.result));
            srv.disconnect();
        }




        public const EVENTTYPE_DELETE:String = 'delete_response';
        /**
        *         Delete a disk.
        *         @param diskguid:           guid of the disk rootobject
        *         @type diskguid:            guid
        *         @param jobguid:  	       guid of the job if avalailable else empty string
        *         @type jobguid:   	       guid
        *         @param executionparams:    dictionary of job specific params e.g. userErrormsg, maxduration ...
        *         @type executionparams:     dictionary
        *         @return:                   dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        *         @rtype:                    dictionary
        *         @raise e:                  In case an error occurred, exception is raised
        *         
        */
        public function deleteDisk (diskguid:String,jobguid:String="",executionparams:Object=null):void
        {
            var params:Object = new Object();

            if (executionparams == null){
                executionparams = new HashMap();
            }

            srv.callMethod(service, 'deleteDisk', delete_ResultReceived, getError, diskguid,jobguid,executionparams);

        }

        private function delete_ResultReceived (e:*):void
        {
            this.dispatchEvent(new ResultEvent(EVENTTYPE_DELETE, false, false, e.result));
            srv.disconnect();
        }


    }
}

