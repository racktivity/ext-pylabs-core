# Copyright (c) 2008, Q-layer NV
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the pylabs nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Q-LAYER ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Q-LAYER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import xmlrpclib

from pylabs import q
#from pylabs.log import Logger

from model.Group import Group
from model.User import User
from pylabs.baseclasses.BaseType import BaseType
import Utils


class UserManager(BaseType):
    """The handler of all user and groups related operations users of this class should set server and logger"""

    token = q.basetype.string(doc='session token', allow_none = True)
#    server = q.basetype.object(xmlrpclib.Server, doc='xml-rpc server proxy', allow_none = True) #xmlrpclib.Server is old style class
#    logger = q.basetype.object(Logger, doc='q logger', allow_none = True)

    def __init__(self, logger):
        self.server = None
        self.logger = logger

    def listUsers(self):
        """Return a list of current users

        @rtype: list
        @return: User fields"""
        return self.server.getActiveUsers(self.token, True)

    def addUser(self, name, fullName, password, email = None, url = None):
        """Create a User

        @param name: user's name
        @param fullName: user's full name
        @param password: user's password
        @param email: user's email (default value is set by Confluence)
        @param url: user's URL on Confluence (default value is set by Confluence)
        @return: User"""
        user = User(name, fullName)
        user.email = email
        user.url = url

        try:
            result = self.server.addUser(self.token, user.toDict(), password)
            return user.toDict()
        except Exception, ex:
            self.logger.log(str(ex))
            raise Exception( 'Unable to add user with the given name %(name)s, full name %(fullName)s, Reason %(errorMessage)s' %{'name' : name, 'fullName' : fullName, 'errorMessage' : Utils.extractDetails(ex)})

    def removeUser(self, name):
        """Remove a user

        @param name: user name
        @rtype: boolean
        @return: successfully removed"""
        try:
            result = self.server.removeUser(self.token, name)
        except Exception, ex:
             self.logger.log(str(ex))
             raise Exception( 'Unable to remove user with the given name %(name)s, Reason %(errorMessage)s' %{'name' : name, 'errorMessage' : Utils.extractDetails(ex)})
        if (result):
            return result
        else:
            raise Exception( 'Unable to remove user with the given name %(name)s' % {'name' : name})

    def getUser(self, name):
        """Return a User object

        @param name: user name
        @rtype: dictionary
        @return: User fields"""
        try:
            userDict = self.server.getUser(self.token, name)
        except Exception, ex:
             self.logger.log(str(ex))
             raise Exception( 'Unable to retrieve user with the given name %(name)s, Reason %(errorMessage)s' % {'name' : name, 'errorMessage' : Utils.extractDetails(ex)})
        return userDict

    def getGroup(self, name):
        """Return a Group object

        @param name: group name
        @rtype: dictionary
        @return: Group fields"""
        exists = self.server.hasGroup(self.token, name)
        group = None
        if not exists:
            raise Exception( 'Unable to retrieve group with the given name %(name)s, Reason no group with that name exists' % {'name' : name})
        return name


    def addGroup(self, name):
        """Create a Group

        @param name: group name
        @rtype: dictionary
        @return: newly created Group fields"""
        try:
            self.server.addGroup(self.token, name)
        except Exception, ex:
            self.logger.log(str(ex))
            raise Exception( 'Unable to add group with name %(name)s, Reason %(errorMessage)s' % {'name' : name, 'errorMessage' : Utils.extractDetails(ex)})
        return name


    def listGroups(self):
        """Return a list of available groups

        @rtype: dictionary
        @return: newly created Group fields"""
        return self.server.getGroups(self.token)


    def removeGroup(self, name, defaultGroupName = ''):
        """Remove a group, If defaultGroupName is specified, users belonging to group name will be added to defaultGroupName.

        @param name: group name
        @param defaultGroup: default group name (default value is empty strings)
        @return: boolean successfully removed"""
        # if no alternate group is provided the method must be invoked with empty strings to just remove the group
        try:
            return self.server.removeGroup(self.token, name, defaultGroupName)
        except Exception, ex:
            self.logger.log(str(ex))
            raise Exception( 'Unable to remove group with name %(name)s, Reason %(errorMessage)s' % {'name' : name, 'errorMessage' : Utils.extractDetails(ex)})


    def addUserToGroup(self, userName, groupName):
        """Join user to this group

        @param userName: user name
        @param groupName: group name"""
        try:
            self.server.addUserToGroup(self.token, userName, groupName)
        except Exception, ex:
            self.logger.log(str(ex))
            raise Exception( 'Unable to add user %(user)s to group %(group)s, Reason %(errorMessage)s' %{'user' : user, 'group' : groupName, 'errorMessage' : Utils.extractDetails(ex)})

    def removeUserFromGroup(self, user, groupName):
        """Removes user from group

         @param user: user name
         @param group: group name
         @rtype: boolean
         @return: successfully removed"""
        try:
            self.server.removeUserFromGroup(self.token, user, groupName)
        except Exception, ex:
            self.logger.log(str(ex))
            raise Exception( 'Unable to remove user %(user)s from group %(group)s, Reason %(errorMessage)s' %{'user' : user, 'group' : groupName, 'errorMessage' : Utils.extractDetails(ex)})

    def listUserGroups(self, name):
        """Return a list of current groups joined by this user
         @param user: user name
         @rtype: string list
         @return: Group names"""
        try:
            groupNames = self.server.getUserGroups(self.token, name)
        except Exception, ex:
            self.logger.log(str(ex))
            raise Exception( 'Unable to list user with name %(name)s groups, Reason %(errorMessage)s' % {'name' : name, 'errorMessage' : Utils.extractDetails(ex)})
        return groupNames

    def __getServer(self):
        return self.__server


    def __setServer(self, value):
        self.__server = value


    def __delServer(self):
        del self.__server

    server = property(__getServer, __setServer, __delServer, "Confluence server proxy")
