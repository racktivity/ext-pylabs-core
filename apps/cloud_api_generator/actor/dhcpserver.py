from pylabs import q

class dhcpserver:
    def addHost (self, machineguid, tftpserveripaddress = "", bootimagename = "", bootparameters = "", jobguid = "", executionparams = {}):
        """
        
        Adds a host to the DHCP server (every configuration to do with host is being configured).

        @param machineguid:                 Guid of the machine to add.
        @type  machineguid:                 guid

        @param tftpserveripaddress          IP address of the TFTP server, only relevant for booting over PXE
        @type  tftpserveripaddress          type_ipaddress

        @param bootimagename                Name of image which needs to be booted over linux pxelinux.0
        @type  bootimagename                string

        @param bootparameters               Additional boot parameters (as string) for PXE boot
        @param bootparameters               string

        @param jobguid:                     Guid of the job
        @type jobguid:                      guid

        @param executionparams:             dictionary with additional executionparams
        @type executionparams:              dictionary

        @return:                            dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['bootimagename'] = bootimagename
        params['tftpserveripaddress'] = tftpserveripaddress
        params['bootparameters'] = bootparameters
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('dhcpserver', 'addHost', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, applicationguid, previousmachineguid = "", jobguid = "", executionparams = {}):
        """
        
        Installs and configures the DHCP server is installed on right interfaces and is running

        @param applicationguid:            Guid of the application which needs to be initialized
        @type  applicationguid:            guid

        @param previousmachineguid:        Guid of the machine which was previously running the dhcpserver
+       @type  previousmachineguid:        guid


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
        params['previousmachineguid'] = previousmachineguid
        return q.workflowengine.actionmanager.startActorAction('dhcpserver', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def removeNetworkRange (self, languid, jobguid = "", executionparams = {}):
        """
        
        Removes a network range from the DHCP server.

        @param languid:                    Guid of the lan to remove as a shared network
        @type languid:                     guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional parameters
        @type executionparams:             dictionary

        @return:                           dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['languid'] = languid
        return q.workflowengine.actionmanager.startActorAction('dhcpserver', 'removeNetworkRange', params, jobguid=jobguid, executionparams=executionparams)

    def removeHost (self, machineguid, jobguid = "", executionparams = {}):
        """
        
        Removes a host from the DHCP server.

        @param machineguid:                Guid of the machine to remove.
        @type machineguid:                 guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional parameters
        @type executionparams:             dictionary

        @return:                           dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['machineguid'] = machineguid
        return q.workflowengine.actionmanager.startActorAction('dhcpserver', 'removeHost', params, jobguid=jobguid, executionparams=executionparams)

    def addNetworkRange (self, languid, tftpserveripaddress = "", bootimagename = "", bootparameters = "", jobguid = "", executionparams = {}):
        """
        
        Adds a network range to the DHCP server.

        @param languid:                     Guid of the lan to add as a shared network
        @type languid:                      guid

        @param tftpserveripaddress          IP address of the TFTP server, only relevant for booting over PXE
        @type  tftpserveripaddress          type_ipaddress

        @param bootimagename                Name of image which needs to be booted over linux pxelinux.0
        @type  bootimagename                string

        @param bootparameters               Additional boot parameters (as string) for PXE boot
        @param bootparameters               string

        @param jobguid:                     Guid of the job
        @type jobguid:                      guid

        @param executionparams:             dictionary with additional parameters
        @type executionparams:              dictionary

        @return:                            dictionary with boolean as result and jobguid: {'result': boolean, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['bootparameters'] = bootparameters
        params['bootimagename'] = bootimagename
        params['languid'] = languid
        params['tftpserveripaddress'] = tftpserveripaddress
        return q.workflowengine.actionmanager.startActorAction('dhcpserver', 'addNetworkRange', params, jobguid=jobguid, executionparams=executionparams)


