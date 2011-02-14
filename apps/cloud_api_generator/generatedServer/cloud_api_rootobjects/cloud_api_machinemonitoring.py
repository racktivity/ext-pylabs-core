from pymonkey import q

class machinemonitoring:
    def getDSSDirectorInfo (self, jobguid = "", executionparams = {}):
        """
        
        Return information about DSS Director monitoring

        @execution_method = sync
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': dict(), 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getDSSDirectorInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getDSSStorageDaemonInfo (self, applicationguid = "", jobguid = "", executionparams = {}):
        """
        
        Return information about DSS Storage daemon monitoring

        @execution_method = sync
        
        @param applicationguid:            guid of the application representing the dss storage daemon in drp
        @type applicationguid:             guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': dict(), 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getDSSStorageDaemonInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getVMachineStorageInfo (self, vmachineguid, diskguid = "", jobguid = "", executionparams = {}):
        """
        
        return info about sso storage information (dispersed storage info mainly)

        @execution_method = sync

        @param vmachineguid:               guid of the guest machine for which to retrieve the storage info for
        @type vmachineguid:                guid

        @param diskguid:                   guid of the disk for which to retrieve the storage info for, or all disks when not specified
        @type diskguid:                    guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @note: {'jobguid': '301ce80a-b0cf-4a31-8be9-d89bd92efbe9',
        @note:  'result': {'machineguid': '2388d3d3-4de4-45fe-b17f-4f1ca05ff062',
        @note:             'volumes'    : [{'capacityGB': 500.0,
        @note:                              'usedGB'    :  10.0,
        @note:                              'guid': 'd1fd8dc4-65b7-4fa7-b55e-02cecd0d2a8b',
        @note:                              'volumetype': DSSVOL,
        @note:                              'dssinfo': {'SCOCount'                  : 0,
        @note:                                          'SCOCounter'                : 0,
        @note:                                          'backendSize'   : 0,
        @note:                                          'cacheHitCounter'             : 0,
        @note:                                          'cacheHitCounterLastHour'            : 0,
        @note:                                          'cacheMissCounter'        : 0,
        @note:                                          'cacheMissCounterLastHour'     : 0,
        @note:                                          'dataStoreReadUsed' : 0,
        @note:                                          'dataStoreWriteUsed'  : 0,
        @note:                                          'queueCount'  : 0,
        @note:                                          'queueSize'  : 0,
        @note:                                          'sourceDataCounter'  : 0,
        @note:                                          'sourceDataCounterIncreaseLastDay'  : 0,
        @note:                                          'tLogUsed'  : 0,
        @note:                                          'writeTime'  : 0,
        @note:                                          'metaDataStoreCacheSize'  : 0},
        @note:                             }

        @raise e:                          In case an error occurred, exception is raised

        @todo:                             Define result
        
	"""
        params =dict()
        params['diskguid'] = diskguid
        params['vmachineguid'] = vmachineguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getVMachineStorageInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getPMachineStorageInfo (self, pmachineguid, diskguid = "", jobguid = "", executionparams = {}):
        """
        
        returns sso storage information of physical volumes on storage nodes

        @execution_method = sync

        @param pmachineguid:               guid of physical storage node to retrieve info from
        @type pmachineguid:                guid

        @param diskguid:                   guid of the disk for which to retrieve the storage info for, or all disks when not specified
        @type diskguid:                    guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @note: {'jobguid': '301ce80a-b0cf-4a31-8be9-d89bd92efbe9',
        @note:  'result': {'machineguid': '2388d3d3-4de4-45fe-b17f-4f1ca05ff062',
        @note:             'disks'      : [{'capacityGB': 500.0,
        @note:                              'guid': 'd1fd8dc4-65b7-4fa7-b55e-02cecd0d2a8b',
        @note:                              'description': ' ATA Disk',
        @note:                              'version': '3b9fc25b-ef69-455e-a50e-b9e002614f8f',
        @note:                              'disktype': IDE,
        @note:                              'smartinfo': {'RawReadErrorRate'          : 0,
        @note:                                            'SpinUpTime'                : 0,
        @note:                                            'ReallocatedSectorsCount'   : 0,
        @note:                                            'SeekErrorRate'             : 0,
        @note:                                            'SpinRetryCount'            : 0,
        @note:                                            'TemperatureCelcius'        : 0,
        @note:                                            'ReallocatedEventCount'     : 0,
        @note:                                            'CurrentPendingSectorCount' : 0,
        @note:                                            'UncorrectableSectorCount'  : 0,
        @note:                                            'OverallStatus'             : 'UNKNOWN'},
        @note:                              'creationdate': None,
        @note:                              'deviceId': '/dev/sda'}],
        @note:             'partitions' : [{'capacityGB'      : 209.66202163696289,
        @note:                              'diskLogicalName' : '/dev/sda',
        @note:                              'fileSystemType'  : EXT3,
        @note:                              'logicalname'     : '/dev/sda4',
        @note:                              'usedGB'          : 10.654228210449219,
        @note:                              'version'         : '0671e77d-4b3e-4ba8-a551-a1828ebd8156',
        @note:                              'guid'            : '36869c23-1011-4432-b253-1d0705e0aa01',
        @note:                              'mountpoint'      : '/mnt/dss/disk1',
        @note:                              'creationdate'    : None,
        @note:                              'partitionType'   : None}]}

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        params['diskguid'] = diskguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getPMachineStorageInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getDSSVolumeInfo (self, volumeguid = "", jobguid = "", executionparams = {}):
        """
        
        Return information about a(ll) volume(s)

        @execution_method = sync
        
        @param volumeguid:                 guid of the volume to get information of
        @type volumeguid:                  guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': dict ( key = volumeGuid, 
                                                                                                                 value = dict ( key = 'diskSafety' , 
                                                                                                                                value = worst case value
                                                                                                                                key = 'backendSize', 
                                                                                                                                value = actual backendSize), 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['volumeguid'] = volumeguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getDSSVolumeInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getPMachineProcesses (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        Returns array of processes running on pmachine and details of that process like cpu & memory used.

        @execution_method = sync

        If fake output fake values, can be handy for demo purposes
        - returns a realistic overview of processes running on a typical pmachine
        - support the 3 types: cpunode, stornode, mgmtappliance

        @param pmachineguid:               guid of the host machine for which to retieve  the virtual machines' load info for
        @type pmachineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'result':
        @note:                                   {'machineguid': '7D763680-ED8A-463F-AA25-EBF3EA7A1894',
        @note:                                    'processes':
        @note:                                       [{'name': 'apache',
        @nota:                                         'pid': 5190,
        @note:                                         'parentpid': 1,
        @note:                                         'cpu': 63.1,
        @note:                                         'cpuavg': 49.6,
        @note:                                         'memory': 6.3,
        @note:                                         'memoryavg': 5.0,
        @note:                                         'memorypeak': 300,
        @note:                                         'memorypeakavg': 100}],
                                            'jobguid': "8D763680-ED8A-463F-AA25-EBF3EA7A1894"}
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getPMachineProcesses', params, jobguid=jobguid, executionparams=executionparams)

    def getPMachineNetworkInfo (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        return info about networking per interface (device) for a given physical machine

        @execution_method = sync

        @param pmachineguid:               guid of the host machine for which to retrieve the network info for
        @type pmachineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised

        @note:                             {'result':
        @note:                                   {'machineguid': '7D763680-ED8A-463F-AA25-EBF3EA7A1894',
        @note:                                    'nics':
        @note:                                       [{'name': 'eth1',
        @nota:                                         'mac': 'aa:54:b8:3c:f7:ff',
        @note:                                         'ipaddresses': ['192.168.11.13', '85.255.23.45'],
        @note:                                         'status': 'ACTIVE',
        @note:                                         'mbsent': 49.6,
        @note:                                         'mbsentavg': 6.3,
        @note:                                         'mbreceived': 5.0,
        @note:                                         'mbreceivedavg': 300,
        @note:                                         'packetsreceived': 49.6,
        @note:                                         'packetsreceivedavg': 6.3,
        @note:                                         'packetssent': 5.0,
        @note:                                         'packetssentavg': 300,}],}
                                            'jobguid': "8D763680-ED8A-463F-AA25-EBF3EA7A1894"}

        @todo:                            Update comparing to OSIS monitoring
        @note:                            dictionary : {deviceid:{"macaddr":...,ipaddr:[ipaddr1,ipaddr2],status,mbSent,mbSentPerSecAvg,mbRec,mbRecPerSecAvg,noPacketsRecPerSec,noPacketsRecPerSecAvg,noPacketsSentPerSec,noPacketsSentPerSecAvg,errors...},...}
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getPMachineNetworkInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getVMachinesLoad (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        Returns load information for each virtual machine running on the specified host machine.

        @execution_method = sync

        memory, cpu & bandwidth usage per vmachine
        - memory in MB & percentage of total MB capacity of host
        - cpu in percentage of total capacity of host for last measurement
        - cpu in percentage of total capacity of host avg over last hour
        - bandwidth in mbit/sec for last measurement
        - bandwidth in mbit/sec avg over last hour

        information comes from monitoring database (in principle only 1 monitoring object per vmachine needs to be captured, all info is in)

        If fake output fake values, can be handy for demo purposes
        - cpu: hash the guid, use first letter as gradation between 0 & 15, then do a 20% variation (random), this to make sure machine always comes back in same range
           e.g. cpu guid hash = 8B3D8B3D  , cpuusage=((guid[0]+1)/15*10)+rand(0,4)-0,2    , cpuusageAvg=((guid[0]+1)/15*10)
        -  memusage=vmachine.memory
        -  bwusage=((guid[0]+1)/15*10) * (1.4-rand(0,8)) * 1             mbit
        -  bwusageLastHour=((guid[0]+1)/15*10) * 1             mbit


        @param pmachineguid:               guid of the host machine for which to retieve  the virtual machines' load info for
        @type pmachineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'result':
        @note:                                  [{'machineguid': '7D763680-ED8A-463F-AA25-EBF3EA7A1894',
        @note:                                    'name': 'MyVMachine',
        @note:                                    'memory': 1024,
        @note:                                    'memorypercent': 15,
        @note:                                    'cpupercent': 40,
        @note:                                    'cpupercentavg': 12,
        @note:                                    'bandwidth': 800,
        @note:                                    'bandwidthavg': 600},
        @note:                                   {'machineguid': '9D763680-ED8A-463F-AA25-EBF3EA7A1894',
        @note:                                    'name': 'MyVMachine',
        @note:                                    'memory': 2048,
        @note:                                    'memorypercent': 30,
        @note:                                    'cpupercent': 12,
        @note:                                    'cpupercentavg': 4,
        @note:                                    'bandwidth': 300,
        @note:                                    'bandwidthavg': 100}],
        @note:                                   'jobguid': "8D763680-ED8A-463F-AA25-EBF3EA7A1894"}
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getVMachinesLoad', params, jobguid=jobguid, executionparams=executionparams)

    def getPMachinePowerInfo (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        Return pmachine power monitoring information from PDU

          * Voltage
          * Current
          * CPU usage
          * Max current
          * Power
          * Power Factor
          * Consumption

        @execution_method = sync

        @param pmachineguid:               guid of the host machine for which to retrieve  the power info for
        @type pmachineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @note: {'jobguid': '301ce80a-b0cf-4a31-8be9-d89bd92efbe7',
        @note:  'result': {'voltage': '231',
        @note:             'current': '63',
        @note:             'cpuusage': '80',
        @note:             'maxcurrent': '53',
        @note:             'power': '5300',
        @note:             'powerfactor': '36',
        @note:             'consumption': '3600'}

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getPMachinePowerInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getDSSStoragePoolInfo (self, jobguid = "", executionparams = {}):
        """
        
        Return information about DSS Storage pool monitoring

        @execution_method = sync
        
        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': dict(), 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getDSSStoragePoolInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getPMachineLoad (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        Returns load information for a given physical machine.

        @execution_method = sync

        returns monitoring statistics for pmachine
        cpu & bandwidth usage per pmachine
        - CPUIOWait
        - CPUIOWaitAvg
        - CPUIdle
        - CPUIdleAvg
        - CPUSystem
        - CPUSystemAvg
        - bandwidth in mbit/sec for last measurement  (over all nics)
        - bandwidth in mbit/sec avg over last hour (over all nics)
        - nr of packets sent per sec for last measurement  (over all nics)
        - nr of packets sent per sec avg over last hour (over all nics)


        information comes from monitoring database (in principle only 1 monitoring object fetch required for the pmachine)

        If fake output fake values, can be handy for demo purposes
        - cpu: hash the guid, use first letter as gradation between 0 & 15, then do a 20% variation (random), this to make sure machine always comes back in same range
           e.g. cpu guid hash = 8B3D8B3D  , cpuusage=((guid[0]+1)/15*10)+rand(0,4)-0,2    , cpuusageAvg=((guid[0]+1)/15*10)
        -  bwusage=((guid[0]+1)/15*10) * (1.4-rand(0,8)) * 10             mbit
        -  bwusageLastHour=((guid[0]+1)/15*10) * 10             mbit
        - @todo invent similar formula's for the other params (make sure it add's up e,g, all CPU stats in total =100%)

        @param pmachineguid:               guid of the host machine for which to retieve  the virtual machines' load info for
        @type pmachineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'result':
        @note:                                   {'machineguid': '7D763680-ED8A-463F-AA25-EBF3EA7A1894',
        @note:                                    'cpuiowait': 0.2,
        @note:                                    'cpuiowaitavg': 0.1,
        @note:                                    'cpuidle': 63.1,
        @note:                                    'cpuidleavg': 49.6,
        @note:                                    'cpusystem': 6.3,
        @note:                                    'cpusystemavg': 5.0,
        @note:                                    'cpuuser': 6.3,
        @note:                                    'cpuuseravg': 5.0,
        @note:                                    'bandwidth': 300,
        @note:                                    'bandwidthavg': 100,
        @note:                                    'packetssent': 300,
        @note:                                    'packetssentavg': 100
        @note:                                    'packetsreceived': 300,
        @note:                                    'packetsreceivedavg': 100},
                                            'jobguid': "8D763680-ED8A-463F-AA25-EBF3EA7A1894"}
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getPMachineLoad', params, jobguid=jobguid, executionparams=executionparams)

    def getVMachineLoad (self, vmachineguid, jobguid = "", executionparams = {}):
        """
        
        Returns load information for a specified (virtual) machine.

        @execution_method = sync

        memory, cpu & bandwidth usage for 1 vmachine
        - memory in MB & percentage of total MB capacity of host
        - cpu in mhz for last measurement  (calculated as % of host e.g. if host 4core 2 Ghz = 8000mhz, if machine uses 10% of capacity, his cpu load = 800 Mhz)
        - cpu in mhz avg over last hour
        - bandwidth in mbit/sec for last measurement (all vnics per vmachine)
        - bandwidth in mbit/sec avg over last hour (all vnics per vmachine)

        information comes from monitoring database (in principle only 1 monitoring object per vmachine needs to be captured, all info is in)

        If fake output fake values, can be handy for demo purposes
        - cpu: hash the guid, use first letter as gradation between 0 & 15, then do a 20% variation (random), this to make sure machine always comes back in same range
           e.g. cpu guid hash = 8B3D8B3D  , cpuusage=((guid[0]+1)/15*10)+rand(0,4)-0,2    , cpuusageAvg=((guid[0]+1)/15*10)
        -  memusage=vmachine.memory
        -  bwusage=((guid[0]+1)/15*10) * (1.4-rand(0,8)) * 1             mbit
        -  bwusageLastHour=((guid[0]+1)/15*10) * 1             mbit

        @param vmachineguid:               guid of the virtual machine for which to get load info for
        @type vmachineguid:                guid

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary
        @note:                             {'result':
        @note:                                  {'machineguid': '7D763680-ED8A-463F-AA25-EBF3EA7A1894',
        @note:                                   'name': 'MyVMachine',
        @note:                                   'memory': 1024,
        @note:                                   'memorypercent': 15,
        @note:                                   'cpu': 1200,
        @note:                                   'cpuavg': 800,
        @note:                                   'bandwidth': 800,
        @note:                                   'bandwidthavg': 600},
                                            'jobguid': "8D763680-ED8A-463F-AA25-EBF3EA7A1894"}

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['vmachineguid'] = vmachineguid
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getVMachineLoad', params, jobguid=jobguid, executionparams=executionparams)

    def getEnvironmentPowerInfo (self, jobguid = "", executionparams = {}):
        """
        
        Return environment monitoring information of PDU

          * Voltage
          * Total current
          * Total Power
          * Total consumption
          * Temperature
          * Humidity

        @execution_method = sync

        @param jobguid:                    guid of the job if available else empty string
        @type jobguid:                     guid

        @param executionparams:            dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:             dictionary

        @return:                           dictionary with a dictionary as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                            dictionary

        @note:                             {'jobguid': '301ce80a-b0cf-4a31-8be9-d89bd92efbe7',
        @note:                              'result': {'voltage': '231',
        @note:                                         'totalcurrent': '63',
        @note:                                         'totalpower': '14553',
        @note:                                         'totalconsumption': '5300',
        @note:                                         'temperature': '23',
        @note:                                         'humidity': '36'}

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        executionparams['rootobjecttype'] = 'machinemonitoring'

        
        return q.workflowengine.actionmanager.startRootobjectActionSynchronous('machinemonitoring', 'getEnvironmentPowerInfo', params, jobguid=jobguid, executionparams=executionparams)


