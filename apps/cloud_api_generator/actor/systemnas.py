from pymonkey import q

class systemnas:
    def getDiskImageInfo (self, sourceuri, format = "VDI", jobguid = "", executionparams = {}):
        """
        
        get info of a specified disk image 

        @param sourceuri:                   URI of the location where the VDI is stored now
        @type sourceuri:                    string
       
        @param format:                      type of image e.g. VDI
        @type format:                       string
        
        @param jobguid:                     Guid of the job
        @type jobguid:                      guid

        @param executionparams:             dictionary with additional executionparams
        @type executionparams:              dictionary

        @return:                            dictionary with True as result and jobguid: {'result': qemu-info, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['sourceuri'] = sourceuri
        params['format'] = format
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'getDiskImageInfo', params, jobguid=jobguid, executionparams=executionparams)

    def listMachineTemplates (self, jobguid = "", executionparams = {}):
        """
        
        Gets a list of available machine templates
            
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary

        @return:                           dictionary with list of available templates
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'listMachineTemplates', params, jobguid=jobguid, executionparams=executionparams)

    def getConfigurationInfo (self, sourceuri, jobguid = "", executionparams = {}):
        """
        
        Get info about a specified image configuration 

        @param sourceuri:                   URI of the location where the cfg file is stored
        @type sourceuri:                    string
        
        @param jobguid:                     Guid of the job
        @type jobguid:                      guid

        @param executionparams:             dictionary with additional executionparams
        @type executionparams:              dictionary

        @return:                            dictionary with True as result and jobguid: {'result': cfg information, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['sourceuri'] = sourceuri
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'getConfigurationInfo', params, jobguid=jobguid, executionparams=executionparams)

    def listExportedDiskImages (self, jobguid = "", executionparams = {}):
        """
        
        Gets the list of exported disk images on the systemNAS 

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  list of exported images.
        @rtype:                   array

        @raise e:                 In case an error occurred, exception is raised              
        
	"""
        params =dict()
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'listExportedDiskImages', params, jobguid=jobguid, executionparams=executionparams)

    def listExportedVDCImages (self, jobguid = "", executionparams = {}):
        """
        
        Gets the list of exported vdc images on the systemNAS 

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  list of exported images.
        @rtype:                   array

        @raise e:                 In case an error occurred, exception is raised              
        
	"""
        params =dict()
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'listExportedVDCImages', params, jobguid=jobguid, executionparams=executionparams)

    def removeCredentials (self, username, jobguid = "", executionparams = {}):
        """
        
        removes credentials on systemnas for a user
        
        @param username:                   name of the user
        @type username:                    string
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary

        @return:                           dictionary 
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['username'] = username
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'removeCredentials', params, jobguid=jobguid, executionparams=executionparams)

    def listISOImages (self, jobguid = "", executionparams = {}):
        """
        
        Gets a list of available ISO images
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary

        @return:                           dictionary with list of available iso images
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'listISOImages', params, jobguid=jobguid, executionparams=executionparams)

    def importDirectory (self, sourceuri, destinationuri = "", jobguid = "", executionparams = {}):
        """
        
        import specified image(s) to defined destination.

        @param sourceuri:              URI of the location where the images are stored now
        @type sourceuri:               string
       
        @param destinationuri:         URI of the location where the images will be stored
        @type destinationuri:          string
        
        @param jobguid:                Guid of the job
        @type jobguid:                 guid

        @param executionparams:        dictionary with additional executionparams
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['destinationuri'] = destinationuri
        params['sourceuri'] = sourceuri
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'importDirectory', params, jobguid=jobguid, executionparams=executionparams)

    def listExportedMachineImages (self, machinetype = "", jobguid = "", executionparams = {}):
        """
        
        Gets the list of exported machine images on the systemNAS
        
        @param machinetype:       type of machine to filter
        @type machinetype:        string 

        @param jobguid:           guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  list of exported images.
        @rtype:                   array

        @raise e:                 In case an error occurred, exception is raised              
        
	"""
        params =dict()
        params['machinetype'] = machinetype
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'listExportedMachineImages', params, jobguid=jobguid, executionparams=executionparams)

    def initialize (self, applicationguid, jobguid = "", executionparams = {}):
        """
        
        Installs and configures the system NAS, makes sure that the system NAS is installed on right interfaces and is running

        @param applicationguid:            Guid of the application which needs to be initialized
        @type  applicationguid:            guid

        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary

        @return:                           dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['applicationguid'] = applicationguid
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'initialize', params, jobguid=jobguid, executionparams=executionparams)

    def setCredentials (self, username, password, jobguid = "", executionparams = {}):
        """
        
        sets credentials on systemnas for a user
        
        @param username:                   name of the user
        @type username:                    string
        
        @param password:                   password for the user
        @type password:                    string
        
        @param jobguid:                    Guid of the job
        @type jobguid:                     guid

        @param executionparams:            dictionary with additional executionparams
        @type executionparams:             dictionary

        @return:                           dictionary 
        @rtype:                            dictionary

        @raise e:                          In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['username'] = username
        params['password'] = password
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'setCredentials', params, jobguid=jobguid, executionparams=executionparams)

    def importImage (self, sourceuri, destinationuri = "", jobguid = "", executionparams = {}):
        """
        
        upload specified image as an image on defined destination.

        @param sourceuri:              URI of the location where the VDI is stored now
        @type sourceuri:               string
       
        @param destinationuri:         URI of the location where the VDI should be stored. (e.g ftp://login:passwd@myhost.com/backups/machinex/10_20_2008_volImage_C_drive.vdi.gz)
        @type destinationuri:          string
        
        @param jobguid:                Guid of the job
        @type jobguid:                 guid

        @param executionparams:        dictionary with additional executionparams
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        
	"""
        params =dict()
        params['destinationuri'] = destinationuri
        params['sourceuri'] = sourceuri
        return q.workflowengine.actionmanager.startActorAction('systemnas', 'importImage', params, jobguid=jobguid, executionparams=executionparams)


