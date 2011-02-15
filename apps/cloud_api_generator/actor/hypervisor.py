from pylabs import q

class hypervisor:
    def startVMachine (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        start vmachine by instructing the hypervisor

        FLOW for VB
        # in drp: check vmachine is configured or stopped or started  (means it has been provisioned once before)
        # start the vmachine

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'startVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def deleteVMachine (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        delete vmachine by instructing the hypervisor

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'deleteVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def snapshotVMachine (self, snapshotmachineguid, jobguid = "", executionparams = {}):
        """
        
        snapshot vmachine by instructing the hypervisor
        only works for local vdi based machines (images is on local filesystem)
        PHASE2

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid} ##snapshotGuid??
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['snapshotmachineguid'] = snapshotmachineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'snapshotVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def pauseVMachine (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        pause vmachine by instructing the hypervisor

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'pauseVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def setVMachineVideoMode (self, machineguid, order, xres, yres, bpp, jobguid = "", executionparams = {}):
        """
        
        Gets the video mode for a machine controlled by its hypervisor.
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param order:                 Number of the monitor [0-7]
        @type order:                  integer
        
        @param xres:                  horizontal resolution
        @type xres:                   int
        
        @param yres:                  vertical resolution
        @type yres:                   int
        
        @param bpp:                   bits per pixel
        @type bpp:                    int

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with jobguid and result True/False
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['bpp'] = bpp
        params['yres'] = yres
        params['order'] = order
        params['xres'] = xres
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'setVMachineVideoMode', params, jobguid=jobguid, executionparams=executionparams)

    def stopVMachine (self, machineguid, clean = True, timeout = 900, jobguid = "", executionparams = {}):
        """
        
        stop vmachine by instructing the hypervisor
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param clean:            soft shutdown if true else power off
        @type clean:             boolean

        @param timeout:          time (in seconds) to wait for the machine to stop 
        @type timeout:           int

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['timeout'] = timeout
        params['clean'] = clean
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'stopVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def getVMachineInfo (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        gets information about vmachine by instructing the hypervisor
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with hypervisor information
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'getVMachineInfo', params, jobguid=jobguid, executionparams=executionparams)

    def getVMachineVideoMode (self, machineguid, order, jobguid = "", executionparams = {}):
        """
        
        Gets the video mode for a machine controlled by its hypervisor
        
        @param machineguid:           guid of the physical machine
        @type machineguid:            guid
        
        @param order:                 Number of the monitor [0-7]
        @type order:                  integer

        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        
        @return:                      dictionary with jobguid and result a dict = { xres : , yres: , bpp : } 
        @rtype:                       dictionary

        @raise e:                     In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['order'] = order
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'getVMachineVideoMode', params, jobguid=jobguid, executionparams=executionparams)

    def getVMachineDiskInfo (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        gets information about vmachine disk information by instructing the hypervisor
        
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with hypervisor information
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'getVMachineDiskInfo', params, jobguid=jobguid, executionparams=executionparams)

    def rollbackVMachine (self, snapshotmachineguid, jobguid = "", executionparams = {}):
        """
        
        only works for local vdi based machines (images is on local filesystem)
        PHASE2
        @param snapshotmachineguid:          Guid of the snapshotmachine
        @type snapshotmachineguid:           guid

        @param jobguid:                      Guid of the jobguid
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                              dictionary
        
	"""
        params =dict()
        params['snapshotmachineguid'] = snapshotmachineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'rollbackVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        Add node to hypervisor cloud (pmachine is installed & accessible)

        FLOW for virtualbox
        #install qpackages (virtualbox)
        #check if storage, if yes fail (hypervisor needs to be initialized before storagenode)
        #adjust kernel
        #call volumestorageclient.init for this node (will create caches,....)

        @param pmachineguid:               guid of pmachine which will host the hypervisor
        @type  pmachineguid:               guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def provisionVMachine (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        configure hypervisor to know about vmachine (use api of hypervisor to configure the vmachine)
        requirements
        * the storage devices/images are already available
        * if using networking outside of hypervisor, is already available
        * dhcp for the vmachine already configured

        FLOW for VB
        # in drp: check vmachine is connected to pmachine
        # go to pmachine
        # call Volumestorageclient.diskConnect... for each disk
        # configure vmachine (mac addr, disks, ...)
        # remark: vnics (bridges do not need to be configured)
        # start vmachine

        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid
  
        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'provisionVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def resumeVMachine (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        resume vmachine by instructing the hypervisor
        @param jobguid:          Guid of the job
        @type jobguid:           guid

        @param machineguid:      Guid of the machine
        @type machineguid:       guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                  dictionary
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'resumeVMachine', params, jobguid=jobguid, executionparams=executionparams)

    def uninstall (self, pmachineguid, jobguid = "", executionparams = {}):
        """
        
        Remove hypervisor soft from cpunode
        PHASE2

        FLOW for virtualbox
        #remove virtualbox & qpackages
        #remove drp app from appropriate pmachine

        @param pmachineguid:               guid of pmachine which will host the hypervisor
        @type  pmachineguid:               guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionParams:            dictionary with additional executionParams
        @type executionParams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['pmachineguid'] = pmachineguid
        return q.workflowengine.actionmanager.startActorAction('hypervisor', 'uninstall', params, jobguid=jobguid, executionparams=executionparams)


