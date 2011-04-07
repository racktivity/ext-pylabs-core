from pylabs import q

class Bitbucket(object):
    """
    Bitbucket tools PyLabs extension
    """

    def crowdGroupSync(self, crowdGroupName, crowdDirectoryName, crowdAccountName, bitbucketRepoName, bitbucketPermission, bitbucketAccountName):
        """
        Sync a Bitbucket group with a Crowd group and give the specified Bitbucket group some privileges on a Bitbucket repository

        @param crowdGroupName:              Crowd group name
        @type crowdGroupName:               string
        @param crowdDirectoryName:          Crowd directory name
        @type crowdDirectoryName:           string
        @param crowdAccountName:            Crowd account name
        @type crowdAccountName:             string
        @param bitbucketRepoName:           Bitbucket repository name
        @type bitbucketRepoName:            string
        @param bitbucketPermission:         Bitbucket access permission
        @type bitbucketPermission:          L{q.enumerators.BitbucketPermission}
        @param bitbucketAccountName:        Bitbucket account name
        @type bitbucketAccountNam:          string
        @return A dictionary of users added successfully, users deleted and users not added nor deleted to/from the Bitbucket group
        @rtype dict
        @raise Exception in case of errors
        """
        self._validateValues(crowdGroupName=crowdGroupName, crowdDirectoryName=crowdDirectoryName, crowdAccountName=crowdAccountName,
                             bitbucketRepoName=bitbucketRepoName, bitbucketPermission=bitbucketPermission,
                             bitbucketAccountName=bitbucketAccountName)

        if type(bitbucketPermission).__name__ != 'BitbucketPermission':
            q.errorconditionhandler.raiseError("Invalid Bitbucket permission type '%s'. Please use 'q.enumerators.BitbucketPermission'" %type(bitbucketPermission).__name__)

        if not q.clients.crowd.checkDirectory(crowdDirectoryName, crowdAccountName):
            q.errorconditionhandler.raiseError("No Crowd directory found with name '%s'." %crowdDirectoryName)

        if not q.clients.crowd.checkGroup(crowdGroupName, crowdDirectoryName, crowdAccountName):
            q.errorconditionhandler.raiseError("No Crowd group found with name '%s'." %crowdGroupName)

        if not q.clients.bitbucket.checkRepo(bitbucketRepoName, bitbucketAccountName):
            q.errorconditionhandler.raiseError("No Bitbucket repository found with name '%s'." %bitbucketRepoName)

        if not q.clients.bitbucket.checkGroup(crowdGroupName, bitbucketAccountName):
            q.gui.dialog.message("* Bitbucket group '%(groupName)s' not found. Creating Bitbucket group '%(groupName)s'..." %{'groupName': crowdGroupName})
            q.clients.bitbucket.addGroup(crowdGroupName, bitbucketAccountName)
            q.gui.dialog.message("*   Done creating Bitbucket group '%s'." %crowdGroupName)

        crowdMembers = q.clients.crowd.getGroupMembers(crowdGroupName, crowdDirectoryName, crowdAccountName)
        bitbucketMembers = q.clients.bitbucket.getGroupMembers(crowdGroupName, bitbucketAccountName)
        membersToAdd = [member for member in crowdMembers if member not in bitbucketMembers]
        membersWithNOP = [member for member in crowdMembers if member in bitbucketMembers]
        membersToDelete = [member for member in bitbucketMembers if member not in crowdMembers]

        for member in membersToAdd:
            q.gui.dialog.message("* Adding '%s' to '%s' Bitbucket group." %(member, crowdGroupName))
            q.clients.bitbucket.addGroupMember(member, crowdGroupName, bitbucketAccountName)

        for member in membersToDelete:
            q.gui.dialog.message("* Removing '%s' from '%s' Bitbucket group." %(member, crowdGroupName))
            q.clients.bitbucket.deleteGroupMember(member, crowdGroupName, bitbucketAccountName)

        q.clients.bitbucket.grantGroupPrivileges(crowdGroupName, bitbucketRepoName, bitbucketPermission, bitbucketAccountName)

        return {'addedMembers': membersToAdd, 'deletedMembers': membersToDelete, 'nopMembers': membersWithNOP}

    def _validateValues(self, **kwargs):
        """
        Validate values that they are not neither None nor empty valued

        @param kwargs:          Values to be validated
        @type kwargs:           dict
        @raise Exception in case one or more values do not satisfy the conditions specified above
        """
        invalidValues = dict()
        for key in kwargs:
            if not kwargs[key]:
                invalidValues[key] = kwargs[key]

        if invalidValues:
            q.errorconditionhandler.raiseError('Invalid values: %s' %invalidValues)
