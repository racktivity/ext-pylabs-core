class Racktivity():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    these actions do not call workflows which execute scripts in the reality on the agents
    """
    def create(self, sw_version=None, smtp=None, smtplogin=None, smtppassword=None, configured=False, tags=None,  request=None, jobguid=None, executionparams=dict()):
        """
        Create a racktivity object, if there is already a existing one, this action will fail
        This object keeps some configuration settings.
        
        @params sw_version: version of the racktivity software
        @type sw_version: string
        
        @params smtp: smtp server used in the software
        @type smtp: string
        
        @params smtplogin: smtplogin login account for the remote snmp server
        @type smtplogin: string
         
        @params smtppassword: password 
        @type smtpassword: string
        
        @params configured: if the environment is configured, this is set to True
        @type configure: boolean
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and guid, jobguid: {'result': {'returncode':True, guid:}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def delete(self, racktivityguid, request=None, jobguid=None, executionparams=dict()):
        """
        Deletes the racktivity object
        
        @params racktivityguid: guid of the racktivity object to delete
        @type version: guid
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def updateModelProperties(self, racktivityguid=None, sw_version=None, smtp=None,smtplogin=None, smtppassword=None, configured=None,  tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Update model properties, if racktivityguid is "", we search for the racktivityguid.

        @params racktivityguid: guid of the racktivity configuration object, if none, it is automatcly selected
        @type racktivityguid: string       
        
        @params sw_version: version of the racktivity software
        @type sw_version: string
        
        @params smtp: snmp server used in the software
        @type snmp: string
        
        @params smtplogin: smtplogin login account for the remote snmp server
        @type smtplogin: string
         
        @params smtppassword: password 
        @type smtpassword: string
        
        @params configured: if the environment is configured, this is set to True
        @type configure: boolean
        
        @param tags: string of tags
        @type tags: string
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def findObject(self, request=None, jobguid=None, executionparams=dict()):
        """
        Find and return guid of the racktivity config object
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and racktivity guid  as result and jobguid: {'result': {'returncode':True,'guid':}, 'jobguid': guid}
        @rtype:                   dictionary
        """
    
    def search(self, rootobjecttype='', tag='', request=None, jobguid=None, executionparams=dict()):
        """
        Find any rootobject that match the search critieria
        
        @param rootobjecttype:    The type of the rootobject you want to query, or all if rootobjecttype=''
        @type  rootobjecttype:    str
        
        @param tag:               Search object by tag.
        @type  tag:               str
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary
        
        @return:                  dictionary with the results as {'returncode': True, 'objects': [<object>, <object>, ...]} where an <object> is in the form of {'name': name, 'type': rootobjecttype, 'guid': guid}
        """
        
    def getObject(self, rootobjectguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:   guid of the job rootobject
        @type rootobjectguid:    guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 rootobject
        @rtype:                  rootobject

        @warning:                Only usable using the python client.
        """
    
    def listObject(self, request=None, jobguid=None, executionparams=dict()):
                """
        List the racktivity config object
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) and racktivity guid  as result and jobguid: {'result': {'returncode':True,'racktivityinfo':}, 'jobguid': guid}
        @rtype:                   dictionary
        """
        
    def sendMail(self, subject, body=None, sender =None, to =None, request=None, jobguid=None, executionparams=dict() ):
        """
        Send a mail using smtp
        
        @param subject:           Subject for the email 
        @type subject:            string

        @param body:              Body of the mail
        @type body:               string
        
        @param sender:            The email address of the sender
        @type sender:             string
        
        @param to:                The email address of the receiver
        @type to:                 string

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                   dictionary
        """
    
    def exportForConsole(self, rootobjectguid, returnformat="raw", request=None,  jobguid=None, executionparams=dict()):
        """
        This function returns a xml document with the latest device data specified as in the racktivity_export_console.xsd file.
        The extra rootobject parameter can limit the size to devices in a datacenter, rack, room, pod, ... and also a logical view.
        A string containing the link to the xml file on the energycloud webserver is returned as result.

        @param rootobjecguid:     Guid of the rootobject from which all devices should be added to the xml file, can be all main objects and the logical views.
        @type rootobjectguid:     guid

        @param returnformat:     return format, (raw or filename) in case of raw, the xml is returned as string, if filename a url is returned instead.
        @type returnformat:     str

        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True), and http link  as result and jobguid: {'result': {'returncode':True, 'export': http://energycloud/export.xml, 'jobguid': guid}
        @rtype:                   dictionary
        """

    def backup(self, destinationdir = "", request=None, jobguid=None, executionparams=dict()):
        """
        This function will backup all your qshell configurations to the provided destination dir
        If destination dir was not provided, backup is done in the configured destination dir
        @param destinationdir:    directory where the backup file should be stored
        @type destinationdir:     string
        @return:                  dictionary with returncode(True) and filename of the backup file as result and jobguid: {'result': {'returncode':True, 'filename':'/opt/backupfile.zip'}, 'jobguid': guid}
        @rtype:                   dictionary
        """

    def exportForHypervisor(self, rootobjectguid, returnformat="raw", request=None, jobguid=None, executionparams=dict()):
        """
        This function returns a xml document with the latest device data specified as in the racktivity_export_hypervisor.xsd file.
        The extra rootobject parameter can limit the size to devices in a datacenter, rack, room, pod, ... and also a logical view.
        A string containing the link to the xml file on the energycloud webserver is returned as result.

        @param rootobjecguid:     Guid of the rootobject from which all devices should be added to the xml file, can be all main objects and the logical views.
        @type rootobjectguid:     guid
        
        @param returnformat:      return format, (raw or filename) in case of raw, the xml is returned as string, if filename a url is returned instead.
        @type returnformat:       str
        
        @param jobguid:           Guid of the job if avalailable else empty string
        @type jobguid:            guid

        @param executionparams:   Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:    dictionary

        @return:                  dictionary with returncode(True), and http link  as result and jobguid: {'result': {'returncode':True, 'export': http://energycloud/export.xml, 'jobguid': guid}
        @rtype:                   dictionary
        """

    def findObjects (self, searchstring, maxresults=10, index=0, request=None, jobguid=None, executionparams=dict()):
        """
        Find a list of objects based on a logicalview search string.
        By default the max amount of results is 10, setting this to 0 will return the full result of the search.
        A index can also be specified, to get result 10 to 20 specify a index=10 and maxresults=10.
         
        The result is a list which contains the following data for every found object:
        {guid:, name:, type:,parent:}
        
        @param searchstring: logical view based search string
        @type searchstring: string
        
        @param maxresults: Max amount of results
        @type maxresults: integer
        
        @param index: where to start when returning the search result.
        @type index: integer
        
        
        @param jobguid: Guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams: Dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams: dictionary
        
        @return: dictionary with returncode(True) and searchresult as result and jobguid: {'result': {'returncode':True,'searchresult:[]}, 'jobguid': guid}
        @rtype: dictionary
        """
    def updateACL(self, rootobjectguid, cloudusergroupnames={}, request=None, jobguid=None, executionparams=dict()):
        """
        Update ACL in a rootobject.
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param cloudusergroupnames:          Dict with keys in the form of cloudusergroupguid_actionname and empty values for now.
        @type cloudusergroupnames:           dict

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """

    def addGroup(self, rootobjectguid, group, action=None, recursive=False, request=None, jobguid=None, executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to add to the specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group gets access to all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is added to all children objects
        @type recursive:                     Boolean 
        
        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def deleteGroup(self, rootobjectguid, group, action=None, recursive=False, request=None, jobguid=None, executionparams=dict()):
        """
        Delete a group in the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the rootobject for which this ACL applies.
        @type rootobjectguid:                guid

        @param group:                        name of the group or the group guid to delete for a specific action
        @type group:                         String 

        @param action:                       name of the required action. If no action specified, the group is deleted from all the actions configured on the object
        @type action:                        String

        @param recursive:                    If recursive is True, the group is deleted from all children objects
        @type recursive:                     Boolean         

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """


    def hasAccess(self, rootobjectguid, groups, action, request=None, jobguid=None, executionparams=dict()):
        """
        Add a group to the acl for a specific action
       
        @security administrators
        
        @param rootobjectguid:               Guid of the selected root object.
        @type rootobjectguid:                guid

        @param groups:                       list of groups to be checked
        @type groups:                        list 

        @param action:                       name of the required action.
        @type action:                        String

        @param jobguid:                      Guid of the job if available else empty string
        @type jobguid:                       guid

        @param executionparams:              dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:               dictionary

        @return:                             dictionary with returncode as result and jobguid: {'result':{returncode:'True'}, 'jobguid': guid}
        @rtype:                              dictionary

        @raise e:                            In case an error occurred, exception is raised
        """