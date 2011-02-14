# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>
 
NOT_CONNECTED_MESSAGE = """You are currently not connected to Confluence server, use q.clients.confluence.connect(<serverURL>, <userName>, <password>)"""


class Confluence(object):
    """Confluence serves as a proxy, when initialized self._impl is initialized to None, thus a call to any method will raise an exception,
    self._impl will be set by ConfluenceProxy when connect() method is called."""


    def __init__(self):
        self._impl = None #reference to a concrete implementation of the xmlrpc client


    def logout(self):
        """Logout from current session, calling this method changes the state of confluence extension to unconnected state

        @rtype: boolean
        @return: successful log out"""
        self._validateConnected()

        return self._impl.logout()


    def serverInfo(self):
        """Get confluence XMLRPC server info

        @rtype: dictionary
        @return: confluence portal info"""
        self._validateConnected()

        return self._impl.serverInfo()


    def listSpaces(self):
        """Return a list of Spaces Objects available to the current user

        @rtype: Space list
        @return: list of available Spaces"""
        self._validateConnected()

        return self._impl.listSpaces()


    def addSpace(self, key, name, description = ''):
        """Create a Space

        @param key: the key for the new space (must be unique)
        @param name: the space name
        @param description: the space description (default value is empty string)
        @rtype: Space
        @return: newly added Space"""
        self._validateConnected()

        return self._impl.addSpace(key, name, description)


    def getUser(self, name):
        """Return a User object

        @type name: string, or User Object
        @param name: user name, or User object
        @rtype: User object"""
        self._validateConnected()

        return self._impl.getUser(name)


    def removeSpace(self, space):
        """Remove Space, deleting it from confluence portal

        @type space: string, or Space object
        @param space: space key, or Space object
        @rtype: boolean
        @return: successfully removed"""
        self._validateConnected()

        return self._impl.removeSpace(space)


    def getGroup(self, name):
        """Return a Group object

        @param name: group name
        @rtype: Group"""
        self._validateConnected()

        return self._impl.getGroup(name)


    def addUser(self, name, fullName, password, email = None, url = None):
        """Create a User

        @param name: user's name
        @param fullName: user's full name
        @param password: user's password
        @param email: user's email (default value is set by Confluence)
        @param url: user's URL on Confluence (default value is set by Confluence)
        @rtype: User object
        @return: newly created User"""
        self._validateConnected()

        return self._impl.addUser(name, fullName, password, email, url)


    def listUsers(self):
        """Return a list of current users

        @rtype: User List
        @return: list of available Users"""
        self._validateConnected()

        return self._impl.listUsers()


    def listPages(self, space):
        """Return a list of available pages in this space

        @type space: string, or Space Object
        @param space: space key, or Space object
        @rtype: Page list
        @return: list of Pages contained in space"""
        self._validateConnected()

        return self._impl.listPages(space)


    def removeUser(self, user):
        """Remove a user

        @type user:  string, or User object
        @param user: user name, or User object
        @rtype: boolean
        @return: successfully removed"""
        self._validateConnected()

        return self._impl.removeUser(user)


    def listGroups(self):
        """Return a list of available groups

        @rtype: Group List
        @return: list of available Groups"""
        self._validateConnected()

        return self._impl.listGroups()


    def removeGroup(self, group, defaultGroup=''):
        """Remove a group, if defaultGroupName parameter is specified, users belonging to group will be added to defaultGroup

        @type group: string, or Group object
        @param group: group name, or Group object
        @type defaultGroup: string, or Group object
        @param defaultGroup: default group name, or defaultGroup object (default value is empty string)
        @rtype: boolean
        @return: successfully removed"""
        self._validateConnected()

        return self._impl.removeGroup(group, defaultGroup)


    def addGroup(self, name):
        """Create a Group

        @param name: group name
        @rtype: Group
        @return: newly created Group"""
        self._validateConnected()

        return self._impl.addGroup(name)


    def addUserToGroup(self, user, group):
        """Join user to this group

        @type user:  string, or User object
        @param user: user name, or User object
        @type group:  string, or Group object
        @param group: group name, or Group object"""
        self._validateConnected()

        return self._impl.addUserToGroup(user, group)


    def listUserGroups(self, user):
        """Return a list of current groups joined by this user

        @param user: user name, or User object
        @rtype: Group list
        @return: list of Groups user belongs to"""
        self._validateConnected()

        return self._impl.listUserGroups(user)


    def removeUserFromGroup(self, user, group):
        """Remove user from group

        @type user:  string, or User object
        @param user: user name, or User object
        @type group:  string, or Group object
        @param group: group name, or Group object
        @rtype: boolean
        @return: successfully removed"""
        self._validateConnected()

        return self._impl.removeUserFromGroup(user, group)


    def getSpace(self, key):
        """Return a Space object

        @param key: space key
        @rtype: Space"""
        self._validateConnected()

        return self._impl.getSpace(key)


    def addPage(self, space, title, parent = None, content = ''):
        """Create a Page

        @type space: string, or Space object
        @param space: space key, or Space object
        @param title: page title
        @type parent: string, or Page object
        @param parent: the page id of the parent page, or Page object of the parent page(if not passed the page has no parent)
        @param content: page content written as wiki text
        @rtype: Page
        @return: newly created Page"""
        self._validateConnected()

        return self._impl.addPage(space, title, parent, content)


    def addAttachment(self, page, fileName, localPath, fileType, comment = ''):
        """Add attachment to page

        @type page: string, or Page object
        @param page: page id, or Page object of the page that attachment should be added in
        @param fileName: attachment name
        @param localPath: path to the local file to be uploaded as attachment
        @param fileType: type of the attachment (for example 'txt', 'gif'... etc)
        @param comment: user comment (default value is empty string)
        @rtype: Attachment
        @return: newly created Attachment"""
        self._validateConnected()

        return self._impl.addAttachment(page, fileName, localPath, fileType, comment)


    def addAttachmentFolder(self, page, localPath, fileType = None, comment = None):
        """Add all files at given directory as attachment to the given page

        @type page: string, or Page object
        @param page: page id, or Page object of the page that attachment should be added in
        @param localPath: the path of the directory on local machine
        @param fileType: type of the attachment (the default value is the file extension (the part of the file name following a dot), if there is no extension the default value is 'unknown-type'
        @param comment: user comment (default value is empty string)"""
        self._validateConnected()

        return self._impl.addAttachmentFolder(page, localPath, fileType, comment)


    def getPage(self, id):
        """Return a Page object

        @type id: string, or Page object
        @param id: page id, or Page object
        @rtype: Page"""
        self._validateConnected()

        return self._impl.getPage(id)


    def findPage(self, space, title):
        """Return a Page object

        @type space: string, or Space object
        @param space: space key, or Space object
        @param title: the title of the page
        @rtype: Page"""
        self._validateConnected()

        return self._impl.findPage(space, title)


    def removeAttachment(self, page, name):
        """Remove an attachment from this page

        @type page: string, or Page object
        @param page: page id, or Page object of the page containing this attachment
        @param name: attachment name
        @rtype: boolean
        @return: successfully removed"""
        self._validateConnected()

        return self._impl.removeAttachment(page, name)


    def moveAttachment(self, originalPage, originalName, newPage = None, newName = None):
        """Move an attachment to a different content entity object and/or give it a new name
        at most one parameter can take the default value (either newPage parameter, or newName parameter)

        @type originalPage: string, or Page object
        @param originalPage: page id, or Page object of the original page containing the attachment
        @param originalName: original name of the attachment
        @type newPage: string, or Page object
        @param newPage: page id, or Page object of the page the attachment will be moved at (if not mentioned the attachment will not be moved to another page)
        @param newName: attachment new name (default value is attachment current name)
        @rtype: boolean
        @return: successfully moved"""
        self._validateConnected()

        return self._impl.moveAttachment(originalPage, originalName, newPage, newName)


    def listAttachments(self, page):
        """Returns all the Attachments on this page

        @type page: string , or Page object
        @param page: page id, or Page object
        @rtype: Attachment list
        @return: list of Attachment on page"""
        self._validateConnected()

        return self._impl.listAttachments(page)


    def getAttachment(self, page, name, version = None):
        """Return information about an attachment, if version is not specified latest version is returned

        @type page: string , or Page object
        @param page: page id, or Page object
        @param name: attachment name
        @param version: attachment version(if default value, latest version is returned)
        @rtype: Attachment"""
        self._validateConnected()

        return self._impl.getAttachment(page, name, version)


    def downloadAttachment(self, page, name, localPath, version = None):
        """Download attachment file and save it in localPath parameter

        @type page: string , or Page object
        @param page: page id, or Page object
        @param name: attachment name
        @param localPath: path of the local directory the attachment will be downloaded at
        @param version: attachment version(if not specified the latest version is downloaded)"""
        self._validateConnected()

        return self._impl.downloadAttachment(page, name, localPath, version)


    def downloadAttachments(self, page,localPath):
        """Download all attachment files of a given page and save them in localPath parameter

        @type page: string , or Page object
        @param page: page id, or Page object
        @param localPath: path of the local directory the attachment will be downloaded at"""
        self._validateConnected()

        return self._impl.downloadAttachments(page, localPath)


    def removePage(self,page):
        """Remove a page deleting it from confluence server

        @type page: string, or Page object
        @param page: page id, or Page object"""
        self._validateConnected()

        return self._impl.removePage(page)


    def search(self, query, space = None, typeFilter = None, lastModifiedFilter = None, maxResults = 50):
        """Return a list of SearchResults that match given search query parameter (including pages and other content types),
        limit your search by adding space parameter, typeFilter parameter, and lastModifiedFilter parameter
        If you do not include a parameter, the default is used instead

        @param query: text line to search for
        @type space: string , or Space object
        @param space: space key, or Space object(if default value, the search includes all spaces)
        @param typeFilter: one of the values listed by calling: q.enumerators.ConfluenceTypeFilter, for example q.enumerators.ConfluenceTypeFilter.all, q.enumerators.ConfluenceTypeFilter.page, etc ...(if default value, the search includes all types except mail)
        @param lastModifiedFilter: one of the values listed by calling: q.enumerators.ConfluenceLastModifiedFilter, for example q.enumerators.ConfluenceLastModifiedFilter.TODAY, q.enumerators.ConfluenceLastModifiedFilter.LASTWEEK, etc ...(if default value, the search puts no time restriction on result)
        @param maxResults: search max result(default value is 50)
        @rtype: dictionary list
        @return: search results that match query respecting filters"""
        self._validateConnected()

        return self._impl.search(query, space, typeFilter, lastModifiedFilter, maxResults)


    def addPersonalSpace(self, user ,title, description = ''):
        """Create a personal space to user

        @type user: string, or User object
        @param user: user name, or User object
        @param title: space title
        @param description: the space description (default value is empty string)
        @rtype: Space
        @return: newly created Space"""
        self._validateConnected()

        return self._impl.addPersonalSpace(user ,title, description)


    def createPageFromFile(self, localFilePath, space, title = None, parentId = None, addFileAsAttachment = False):
        """Create a page and add the localFilePath path content as the page content

        @param localPath: the path of the file on local machine containing the wiki text to be used as new page content
        @type space: string , or Space object
        @param space: space key, or Space object
        @param title: page title(if default value, the file name will be used as a title)
        @param parentId: the page id of the parent page (if default value, the page has no parent)
        @param addFileAsAttachment: if True, the file specified is added as attachment to the page(if default value, no attachment is created)
        @rtype: Page
        @return: newly created Page"""
        self._validateConnected()

        return self._impl.createPageFromFile(localFilePath, space, title, parentId, addFileAsAttachment)


    def addComment(self, page, content):
        """Add comment to page

        @type page: string, or Page object
        @param page: page id, or Page object
        @param content: comment content
        @rtype: dictionary
        @return: newly created Comment"""
        self._validateConnected()

        return self._impl.addComment(page, content)


    def editPage(self, page):
        """Update content of page

        @type page: Page object
        @param page: Page object having the updated content
        @rtype: Page
        @return: updated Page"""
        self._validateConnected()

        return self._impl.editPage(page)

    def editSpace(self, space):
        """Update content of space

        @type space: Space object
        @param space: Space object having the updated content
        @rtype: Space
        @return: updated Space"""
        self._validateConnected()

        return self._impl.editSpace(space)

    def addBlogEntry(self, space, title, content = ''):
        """Create a BlogEntry on space parameter

        @type space: string, or Space object
        @param space: space key, or Space object
        @param title: BlogEntry title
        @param content: BlogEntry content written as wiki text(default is empty content)
        @rtype: BlogEntry
        @return: newly created BlogEntry"""
        self._validateConnected()

        return self._impl.addBlogEntry(space, title, content)
        
    def installPlugin(self, localPath):
        """Install plugin

        @param localPath: path to the local file to be uploaded as plugin
        @return: boolean"""
        self._validateConnected()

        return self._impl.installPlugin(localPath)

    def isPluginEnabled(self, pluginKey):
        """Check if plugin is enabled

        @param pluginKey: name of the plugin
        @return: boolean"""
        self._validateConnected()

        return self._impl.isPluginEnabled(pluginKey)

    def listBlogEntries(self, space):
        """List all BlogEntries contained in Space parameter

        @type space: string, or Space object
        @param space: space key, or Space object
        @rtype: BlogEntry list
        @return: list of BlogEntries published on space"""
        self._validateConnected()

        return self._impl.listBlogEntries(space)


    def getBlogEntry(self, id):
        """Get BlogEntry having the given id

        @type id: string, or BlogEntry object
        @param id: BlogEntry id, or BlogEntry object
        @return: BlogEntry"""
        self._validateConnected()

        return self._impl.getBlogEntry(id)
        
        
    def linkPages(self, sourceSpaceKey, sourcePage, destSpaceKey, destPage = None):
        """Duplicates a page hierarchy on another space. The structure and page titles will be copied, The contents of the original spaces are included in the new pages. (with an {include:KEY:pagetitle} macro)

        @type sourceSpaceKey: string
        @param sourceSpaceKey: The key of the space of the original pages
        @type sourcePage: string
        @param sourcePage: The ID or the title of the root page for the link-operation. All children of the this page will be linked.
        @type destSpaceKey: string
        @param destSpaceKey: The key of the space where the pages should be duplicated. Should be different from the sourceSpaceKey parameter, otherwise the link operation will fail because pages in the same space cannot have the same name.
        @type destPage: string
        @param destPage: The ID or key of the root page on the target space. If the page already exists, all children of the sourcePage will be copied (recursively) as children of destPage. If the destSpace does not yet contain a page with the title specified, a new (orphaned) page will be created. If this parameter is omitted, a new page with the same title as sourcePage will be created.
        """
        self._validateConnected()

        return self._impl.linkPages(sourceSpaceKey, sourcePage, destSpaceKey, destPage)


    def listLabelsInPage(self, page):
        """List all Labels available for a given page (can be also used to list Labels for any ContentEntityObject ID)

        @type page: string, or Page object
        @param page: page id, or Page object
        @rtype: list of Labels
        @return: Labels
        """
        self._validateConnected()

        return self._impl.listLabelsInPage(page)


    def listLabelsInSpace(self, space,  maxLabelsToReturn = 20):
        """List all Labels available for a given Space

        @type space: string, or Space object
        @param space: space key, or Space object
        @param maxLabelsToReturn: maximum number of labels to return
        @rtype: list of Labels
        @return: Labels
        """
        self._validateConnected()

        return self._impl.listLabelsInSpace(space)


    def addLabelToPage(self, name, page):
        """Add Label with name to given page

        @param name: Label name
        @type page: string, or Page object
        @param page: page id, or Page object
        @return: successfully added
        """
        self._validateConnected()

        return self._impl.addLabelToPage(name, page)


    def addLabelToSpace(self, name, space):
        """Add Label with name to given space

        @param name: Label name
        @type space: string, or Space object
        @param space: space key, or Space object
        @return: successfully added
        """
        self._validateConnected()

        return self._impl.addLabelToSpace(name, space)


    def removeLabelFromPage(self, label, page):
        """
        Remove Label from given Page

        @type label: String, or Label object
        @param label: label name, or Label object
        @type page: string, or Page object
        @param page: page id, or Page object
        @return: successfully removed
        """
        self._validateConnected()

        return self._impl.removeLabelFromPage(label, page)


    def removeLabelFromSpace(self, label, space):
        """
        Remove Label from given space

        @type label: String, or Label object
        @param label: label name, or Label object
        @type space: string, or Space object
        @param space: space key, or Space object
        @return: successfully removed
        """
        self._validateConnected()

        return self._impl.removeLabelFromSpace(label, space)


    def _validateConnected(self):
        """Validate that Confluence is in connected state, if not raise Exception"""
        if not self._impl:
            raise Exception( NOT_CONNECTED_MESSAGE)


    def pm_setImpl(self,value):
        """Sets self._impl to value, and by doing so becoming in connected state"""
        self._impl = value
