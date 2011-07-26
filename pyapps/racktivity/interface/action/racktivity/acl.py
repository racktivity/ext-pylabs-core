class ACL():
    """
    root object actions
    these actions do modify the DRP and call the actor actions to do the work in the reality
    """


    def create(self, rootobjecttype, rootobjectguid=None, cloudusergroupguidsread=[], cloudusergroupguidswrite=[], cloudusergroupguidsdelete=[], tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Create an ACL.
       
        @security administrators
        
        @param rootobjecttype:              Type of the rootobject. Can be one of the following values ACL, ASSET, DATACENTER, METERINGDEVICE, RACK, ROOM
        @type rootobjecttype:                string

        @param rootobjectguid:              Guid of the rootobject for which this ACL applies. If not specified, ACL applies to ALL rootobjects of type specified.
        @type rootobjectguid:                guid

        @param cloudusergroupguidsread      Array of cloud user group guids who have read access.
        @type cloudusergroupguidsread:      array

        @param cloudusergroupguidswrite     Array of cloud user group guids who have write access.
        @type cloudusergroupguidswrite:     array

        @param cloudusergroupguidsdelete    Array of cloud user group guids who have delete permissions.
        @type cloudusergroupguidsdelete:    array
        
        @param tags:  tags(strings)
        @type tags: String

        @param jobguid:                     Guid of the job if available else empty string
        @type jobguid:                      guid

        @param executionparams:             dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:              dictionary

        @return:                            dictionary with returncode and aclguid as result and jobguid: {'result':{returncode:'True', aclguid:guid}, 'jobguid': guid}
        @rtype:                             dictionary

        @raise e:                           In case an error occurred, exception is raised
        """

    def delete(self, aclguid, request=None, jobguid=None, executionparams=dict()):
        """
        Delete an ACL.
      
        @security administrators

        @param aclguid:                Guid of the acl to delete.
        @type aclguid:                 guid

        @param jobguid:                Guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, rootobjecttype, rootobjectguid=None, tags=None, request=None, jobguid=None, executionparams=dict()):
        """
        Returns a list of acl guids which met the find criteria.
        
        @security administrators
        
        @param rootobjecttype:         Type of the rootobject. Can be one of the following values ACL, ASSET, DATACENTER, POWERDEVICE, RACK, ROOM
        @type rootobjecttype:          string

        @param rootobjectguid:         Guid of the rootobject for which the ACL applies.
        @type rootobjectguid:          guid

        @param tags:                   string of tags
        @type tags:                    string

        @param jobguid:                Guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       Result with returncode and guidlist which met the find criteria specified.
        @rtype:                        array

        @note:                         Example return value:
        @note:                         {'result': {'returncode':True,'guidlist':["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]'},
        @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

        @raise e:                      In case an error occurred, exception is raised
        """

    def list(self, request=None, jobguid=None, executionparams=dict()):
        """
        List all acls.

        @security administrators

        @param jobguid:                 Guid of the job if available else empty string
        @type jobguid:                  guid

        @param executionparams:         dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:          dictionary

        @return:                        returncode and dictionary with array of acl info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {'returncode':'True', 'aclinfo': [{ 'aclguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'rootobjecttype': 'ASSET',
        @note:                                      'rootobjectguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803',
        @note:                                      'cloudusergroupguidsread': ['C4395DA2-BE55-495A-A17E-6A25542CA398', 'FAD805F7-1F4E-4DB1-8902-F440A59270E6'],
        @note:                                      'cloudusergroupguidswrite': ['2A0BA8AD-25BF-4BBA-8E07-1F1A4A15C25B', '4A3F2FD8-52FB-4560-9888-842A77376787'],
        @note:                                      'cloudusergroupguidsdelete': ['A1EE787E-8502-4283-A203-3A3255F34F2F', '75D8C11D-86CA-4A2E-9051-95A96548D5C6'],
        @note:                                      'actions': [{'name': 'STOP',
        @note:                                                   'cloudusergroupguids': ['46B7032F-57EA-4B33-BCD6-3CD57B1ECF54', 'EC1AD72C-5AD3-41D8-A060-CC07732A068C']},
        @note:                                                  {'name': 'START',
        @note:                                                   'cloudusergroupguids': ['46B7032F-57EA-4B33-BCD6-3CD57B1ECF54', 'EC1AD72C-5AD3-41D8-A060-CC07732A068C']}]
        @note:                          }        ]}}
        @raise e:                       In case an error occurred, exception is raised
        """

    def getObject(self, aclguid, request=None, jobguid=None,executionparams=dict()):
        """
        Gets the rootobject.
       
        @param aclguid:             Guid of the acl rootobject
        @type aclguid:              guid

        @return:                    rootobject
        @rtype:                     string

        @warning:                   Only usable using the python client.
        """

    

    def grantPermission(self, aclguid, permissiontype, cloudusergroupguids=[], request=None, jobguid=None, executionparams=dict()):
        """
        Grant permission for a list of cloud user group guids.
      
        @security administrators

        @param aclguid:                Guid of the acl to delete.
        @type aclguid:                 guid

        @param permissiontype          Type of permission to grant. Can be one of the following values READ, WRITE, DELETE
        @type permissiontype           string

        @param cloudusergroupguids     Array of cloud user group guids who are granted permission.
        @type cloudusergroupguids:     array
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def revokePermission(self, aclguid, permissiontype, cloudusergroupguids=[], request=None, jobguid=None, executionparams=dict()):
        """
        Revoke permission for a list of cloud user group guids.
      
        @security administrators

        @param aclguid:                Guid of the acl to delete.
        @type aclguid:                 guid

        @param permissiontype          Type of permission to revoke. Can be one of the following values READ, WRITE, DELETE
        @type permissiontype           string

        @param cloudusergroupguids     Array of cloud user group guids who are revoked permission.
        @type cloudusergroupguids:     array
        
        @param jobguid:                Guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def addAction(self, aclguid, name, cloudusergroupguids=[], request=None, jobguid=None, executionparams=dict()):
        """
        Add an action.(e.g switch on/off port ...)
      
        @security administrators

        @param aclguid:                Guid of the acl to delete.
        @type aclguid:                 guid

        @param name                    Name for the new action.
        @type name                     string

        @param cloudusergroupguids     Array of cloud user group guids who are allowed to execute the action.
        @type cloudusergroupguids:     array
        
        @param jobguid:                Guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def removeAction(self, aclguid, name, request=None, jobguid=None, executionparams=dict()):
        """
        Remove an action.
      
        @security administrators

        @param aclguid:                Guid of the acl to delete.
        @type aclguid:                 guid

        @param name                    Name for the action to delete.
        @type name                     string
        
        @param jobguid:                Guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def grantActionPermission(self, aclguid, name, cloudusergroupguids=[], request=None, jobguid=None, executionparams=dict()):
        """
        Grant permission for a list of cloud user group guids to execute the action specified.
      
        @security administrators

        @param aclguid:                Guid of the acl to delete.
        @type aclguid:                 guid

        @param name                    Name of the action.
        @type name                     string

        @param cloudusergroupguids     Array of cloud user group guids who are granted permission.
        @type cloudusergroupguids:     array
        
        @param jobguid:                Guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def revokeActionPermission(self, aclguid, name, cloudusergroupguids=[], request=None, jobguid=None, executionparams=dict()):
        """
        Revoke permission for a list of cloud user group guids to execute the action specified
      
        @security administrators

        @param aclguid:                Guid of the acl to delete.
        @type aclguid:                 guid

        @param name                    Name of the action.
        @type name                     string

        @param cloudusergroupguids     Array of cloud user group guids who are revoked permission.
        @type cloudusergroupguids:     array
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with returncode(True) as result and jobguid: {'result': {'returncode':True}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def listUserACL(self, clouduserguid, request=None, jobguid=None, executionparams=dict()):
        """
        List all ACL's which apply to the user specified
      
        @security administrators

        @param clouduserguid:          Guid of the cloud user.
        @type clouduserguid:           guid
        
        @param jobguid:                Guid of the job if available else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                        result is a dict with returncode(True) and array(useraclinfo) of acl info as result and jobguid: {'result': {returncode:True, useraclinfo:[]}, 'jobguid': guid}
        @rtype:                         dictionary
        @note:                          {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                          'result: {returcode:True, useraclinfo:[{ 'aclguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                      'rootobjecttype': 'ASSET',
        @note:                                      'rootobjectguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803',
        @note:                                      'canread': True,
        @note:                                      'canwrite': True,
        @note:                                      'candelete': False,
        @note:                                      'actions': ['STOP','START']
        @note:                          }        ]}}
        @raise e:                       In case an error occurred, exception is raised
        """

    def isOperationAllowed(self, rootobjecttype, permissiontype, clouduserguid, rootobjectguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        Check if the user specified is authorized for the operation specified
      
        @security administrators

        @param rootobjecttype:         Type of the rootobject. Can be one of the following values ACL, ASSET, DATACENTER, METERINGDEVICE, RACK, ROOM
        @type rootobjecttype:          string

        @param permissiontype          Type of permission to check. Can be one of the following values READ, WRITE, DELETE
        @type permissiontype           string

        @param clouduserguid           Guid of cloud user to check permission for.
        @type clouduserguid:           guid

        @param rootobjectguid:         Guid of the rootobject to check.
        @type rootobjectguid:          guid
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with boolean value as result and jobguid: {'result': {returncode:True, opallowed:True/False}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """
        
    def isActionAllowed(self, rootobjecttype, name, clouduserguid, rootobjectguid=None, request=None, jobguid=None, executionparams=dict()):
        """
        Check if the user specified is authorized for the operation specified
      
        @security administrators

        @param rootobjecttype:         Type of the rootobject. Can be one of the following values ACL, ASSET, DATACENTER, METERINGDEVICE, RACK, ROOM
        @type rootobjecttype:          string

        @param name                    Name of the action to check
        @type name                     string

        @param clouduserguid           Guid of cloud user to check permission for.
        @type clouduserguid:           guid

        @param rootobjectguid:         Guid of the rootobject to check.
        @type rootobjectguid:          guid
        
        @param jobguid:                Guid of the job if avalailable else empty string
        @type jobguid:                 guid

        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with boolean value as result and jobguid: {'result': {returncode:True, actionallowed:True/False}, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """
        
