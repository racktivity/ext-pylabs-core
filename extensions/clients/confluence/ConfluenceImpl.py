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
 
import xmlrpclib

from pylabs import q
from pylabs.baseclasses.BaseType import BaseType

from Confluence import Confluence
from UserManager import UserManager
from SpaceManager import SpaceManager
from model import AttachmentProxy
from model import BlogEntry
from model import Group
from model import ModelDataManager
from model import Page
from model import Space
from model import User
from model import Label
import Utils

class ConfluenceImpl(BaseType, Confluence):
    """ConfluenceImpl is used to represent the connected state Confluence extension, it has a _proxy (ConfluenceProxy) instance to set/reset _proxy._Impl, switching between connected/unconnected state
    also serves as a thin layer to convert from Confluence Objects (Page, Space, User... etc) to primitive data types(String, maps, lists... etc) from user (using  _unbox()), or the opposite conversion from xml-rpc server dictionaries boxing them into model objects. The lower layer, which is SpaceManager and UserManager are strictly handling primitive objects and collections and is not aware of the model objects (ideally speaking). Following the strict design practices would avoid circular import problems as much as possible"""

    _modelDataManager = q.basetype.object(ModelDataManager.ModelDataManager, doc='manager to handle model object saving, editing... etc', allow_none = True)

    def __init__(self, serverAddress, login, password):
        """@param serverAddress: server Url,or Ip adress; for example, 'http://confluence.aserver.com', or '172.17.1.6'
        @param login: user login
        @param password: user password"""
        BaseType.__init__(self)
        self._serverAddress = serverAddress+'/rpc/xmlrpc' #the address of the confluence server
        self._server = xmlrpclib.Server(self._serverAddress) #xmlrpclib.Server object representing Confluence xml rpc proxy
        self._server = getattr(self._server,'confluence1')
        self._login = login #users login
        self._password = password #user password
        self._token = self._server.login(self._login,self._password) #session token
        self._userManager = None
        self._spaceManager = None
        self._proxy = None #set by proxy when connect() is called
        self._modelDataManager = None


    def logout(self):
        """Logout from current session, calling this method changes the state of confluence extension to unconnected state

        @rtype: boolean
        @return: successful log out"""
        self._proxy._impl = None #nullify the reference to the concrete impl, reverting to the initial unconnected state
        return self._server.logout(self._token)


    def serverInfo(self):
        """Get confluence XMLRPC server info

        @rtype: dictionary
        @return: server info"""
        return self._server.getServerInfo(self._token)


    def listSpaces(self):
        """Return a list of Spaces Objects available to the current user

        @rtype: Space list
        @return: list of available Spaces"""
        return tuple(Space.create(space,self._modelDataManager) for space in self.pm_getSpaceManager().listSpaces())


    def addSpace(self, key, name, description = ''):
        """Create a Space

        @param key: the key for the new space (must be unique)
        @param name: the space name
        @param description: the space description (default value is empty string)
        @rtype: Space
        @return: newly added Space"""
        return Space.create(self.pm_getSpaceManager().addSpace(key, name, description),self._modelDataManager)


    def removeSpace(self, space):
        """Remove a Space, deleting it from confluence portal

        @type space: string, or Space object
        @param space: space
        @rtype: boolean
        @return: successfully removed"""
        return self.pm_getSpaceManager().removeSpace(self._unbox(space))


    def getUser(self, name):
        """Return a User object

        @type name: string, or User Object
        @param name: user name, or User object
        @rtype: User object"""
        return User.create(self.pm_getUserManager().getUser(self._unbox(name)),self._modelDataManager)


    def getGroup(self, name):
        """Return a Group object

        @param name: group name
        @rtype: Group"""
        return Group.create(self.pm_getUserManager().getGroup(self._unbox(name)), self._modelDataManager)

    def installPlugin(self, localFilePath):
        pluginFile = None
        try:
            pluginFile = open(localFilePath, 'rb')#reads file as binary
        except IOError, ex:
            q.logger.log(ex, 3)
            raise IOError( 'No file found at given file path %s' % localFilePath)
        fileData = pluginFile.read()
        fileBinData = xmlrpclib.Binary(fileData)
        try:
            result = self._server.installPlugin(self._token, q.system.fs.getBaseName(localFilePath), fileBinData)
        except Exception, ex:
            raise
            q.logger.log(str(ex), 3)
            raise Exception( 'Unable to install plugin at %s' % localFilePath + '. Reason %s' % Utils.extractDetails(ex))
        return result
        
    
    def isPluginEnabled(self, pluginKey):
        try:
            result = self._server.isPluginEnabled(self._token, pluginKey)
        except Exception, ex:
            q.logger.log(str(ex), 3)
            raise Exception( 'Unable to check plugin %s' % pluginKey + '. Reason %s' % Utils.extractDetails(ex))
        return result


    def addUser(self, name, fullName, password, email = None, url = None):
        """Create a User

        @param name: user's name
        @param fullName: user's full name
        @param password: user's password
        @param email: user's email (default value is set by Confluence)
        @param url: user's URL on Confluence (default value is set by Confluence)
        @rtype: User object
        @return: newly created User"""
        return User.create(self.pm_getUserManager().addUser(name, fullName, password, email, url),self._modelDataManager)


    def listUsers(self):
        """Return a list of current users

        @rtype: User List
        @return: list of available Users"""
        return tuple(User.create({'name':name},self._modelDataManager) for name in self.pm_getUserManager().listUsers())


    def listPages(self, space):
        """Return a list of available pages in this space

        @type space: string, or Space Object
        @param space: space key, or Space object
        @rtype: Page list
        @return: list of Pages contained in space"""
        return tuple(Page.create(page, self._modelDataManager) for page in self.pm_getSpaceManager().listPages(self._unbox(space)))


    def removeUser(self, user):
        """Remove a user

        @type user:  string, or User object
        @param user: user name, or User object
        @rtype: boolean
        @return: successfully removed"""
        return self.pm_getUserManager().removeUser(self._unbox(user))


    def listGroups(self):
        """Return a list of available groups

        @rtype: Group List
        @return: list of available Groups"""
        return tuple(Group.create(groupName, self._modelDataManager) for groupName in self.pm_getUserManager().listGroups())


    def removeGroup(self, group, defaultGroup=''):
        """Remove a group, if defaultGroupName parameter is specified, users belonging to group will be added to defaultGroup

        @type group: string, or Group object
        @param group: group name, or Group object
        @type defaultGroup: string, or Group object
        @param defaultGroup: default group name, or defaultGroup object (default value is empty string)
        @rtype: boolean
        @return: successfully removed"""
        return self.pm_getUserManager().removeGroup(self._unbox(group), self._unbox(defaultGroup))


    def addGroup(self, name):
        """Create a Group

        @param name: group name
        @rtype: Group
        @return: newly created Group"""
        return Group.create(self.pm_getUserManager().addGroup(name), self._modelDataManager)


    def addUserToGroup(self, user, group):
        """Join user to this group

        @type user:  string, or User object
        @param user: user name, or User object
        @type group:  string, or Group object
        @param group: group name, or Group object"""
        return self.pm_getUserManager().addUserToGroup(self._unbox(user), self._unbox(group))


    def listUserGroups(self, user):
        """Return a list of current groups joined by this user

        @param user: user name, or User object
        @rtype: Group list
        @return: list of Groups user belongs to"""
        return tuple(Group.create(name, self._modelDataManager) for name in self.pm_getUserManager().listUserGroups(self._unbox(user)))


    def removeUserFromGroup(self, user, group):
        """Remove user from group

        @type user:  string, or User object
        @param user: user name, or User object
        @type group:  string, or Group object
        @param group: group name, or Group object
        @rtype: boolean
        @return: successfully removed"""
        return self.pm_getUserManager().removeUserFromGroup(self._unbox(user), self._unbox(group))


    def getSpace(self, key):
        """Return a Space object

        @param key: space key
        @rtype: Space"""
        return Space.create(self.pm_getSpaceManager().getSpace(key),self._modelDataManager)


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
        return Page.create(self.pm_getSpaceManager().addPage(self._unbox(space), title, self._unbox(parent), content), self._modelDataManager)


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

        return AttachmentProxy.AttachmentProxy(self.pm_getSpaceManager().addAttachment(self._unbox(page), fileName, localPath, fileType, comment))

    def addAttachmentFolder(self, page, localPath, fileType = None, comment = None):
        """Add all files at given directory as attachment to the given page

        @type page: string, or Page object
        @param page: page id, or Page object of the page that attachment should be added in
        @param localPath: the path of the directory on local machine
        @param fileType: type of the attachment (the default value is the file extension (the part of the file name following a dot), if there is no extension the default value is 'unknown-type'
        @param comment: user comment (default value is empty string)"""

        return self.pm_getSpaceManager().addAttachmentFolder(self._unbox(page), localPath, fileType, comment)


    def getPage(self, id):
        """Return a Page object

        @type id: string, or Page object
        @param id: page id, or Page object
        @rtype: Page"""
        return Page.create(self.pm_getSpaceManager().getPage(self._unbox(id)), self._modelDataManager)

    def findPage(self, space, title):
        """Return a Page object

        @type space: string, or Space object
        @param space: space key, or Space object
        @param title: the title of the page
        @rtype: Page"""
        return Page.create(self.pm_getSpaceManager().findPage(self._unbox(space), title), self._modelDataManager)


    def removeAttachment(self, page, name):
        """Remove an attachment from this page

        @type page: string, or Page object
        @param page: page id, or Page object of the page containing this attachment
        @param name: attachment name
        @rtype: boolean
        @return: successfully removed"""
        return self.pm_getSpaceManager().removeAttachment(self._unbox(page), name)


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
        return self.pm_getSpaceManager().moveAttachment(self._unbox(originalPage), originalName, self._unbox(newPage), newName)


    def listAttachments(self, page):
        """Returns all the Attachments on this page

        @type page: string , or Page object
        @param page: page id, or Page object
        @rtype: Attachment list
        @return: list of Attachment on page"""
        return tuple(AttachmentProxy.AttachmentProxy(attachmentDict) for attachmentDict in self.pm_getSpaceManager().listAttachments(self._unbox(page)))


    def getAttachment(self, page, name, version = None):
        """Return information about an attachment, if version is not specified latest version is returned

        @type page: string , or Page object
        @param page: page id, or Page object
        @param name: attachment name
        @param version: attachment version(if default value, latest version is returned)
        @rtype: Attachment"""
        return AttachmentProxy.AttachmentProxy(self.pm_getSpaceManager().getAttachment(self._unbox(page), name, version))


    def downloadAttachment(self, page, name, localPath, version = None):
        """Download attachment file and save it in localPath parameter

        @type page: string , or Page object
        @param page: page id, or Page object
        @param name: attachment name
        @param localPath: path of the local directory the attachment will be downloaded at
        @param version: attachment version(if not specified the latest version is downloaded)"""
        return self.pm_getSpaceManager().downloadAttachment(self._unbox(page), name, localPath, version)

    def downloadAttachments(self, page,localPath):
        """Download all attachment files of a given page and save them in localPath parameter

        @type page: string , or Page object
        @param page: page id, or Page object
        @param localPath: path of the local directory the attachment will be downloaded at"""
        return self.pm_getSpaceManager().downloadAttachments(self._unbox(page), localPath)


    def removePage(self,page):
        """Remove a page deleting it from confluence server

        @type page: string , or Page object
        @param page: page id, or Page object"""
        return self.pm_getSpaceManager().removePage(self._unbox(page))


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
        return self.pm_getSpaceManager().search(query, self._unbox(space), typeFilter, lastModifiedFilter, maxResults)


    def addPersonalSpace(self, user ,title, description = ''):
        """Create a personal space to user

        @type user: string, or User object
        @param user: user name, or User object
        @param title: space title
        @param description: the space description (default value is empty string)
        @rtype: Space
        @return: newly created Space"""
        return Space.create(self.pm_getSpaceManager().addPersonalSpace(self._unbox(user) ,title, description),self._modelDataManager)


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
        return Page.create(self.pm_getSpaceManager().createPageFromFile(localFilePath, self._unbox(space), title, parentId, addFileAsAttachment), self._modelDataManager)


    def addComment(self, page, content):
        """Add comment to page

        @type page: string, or Page object
        @param page: page id, or Page object
        @param content: comment content
        @rtype: dictionary
        @return: newly created Comment"""
        return self.pm_getSpaceManager().addComment(self._unbox(page), content)


    def editPage(self, page):
        """Update content of page

        @type page: Page object
        @param page: Page object having the updated content
        @rtype: Page
        @return: updated Page"""
        return Page.create(self.pm_getSpaceManager().editPage(page.toDict()), self._modelDataManager)
        
    def editSpace(self, space):
        """Update modified changes to space
        
        @type space: Space object
        @param space: space
        @rtype: object
        @return: Space object"""
        return Space.create(self.pm_getSpaceManager().editSpace(space.toDict()),self._modelDataManager)


    def addBlogEntry(self, space, title, content = ''):
        """Create a BlogEntry on space parameter

        @type space: string, or Space object
        @param space: space key, or Space object
        @param title: BlogEntry title
        @param content: BlogEntry content written as wiki text(default is empty content)
        @rtype: BlogEntry
        @return: newly created BlogEntry"""
        return BlogEntry.create(self.pm_getSpaceManager().addBlogEntry(self._unbox(space), title, content), self._modelDataManager)


    def listBlogEntries(self, space):
        """List all BlogEntries contained in Space parameter

        @type space: string, or Space object
        @param space: space key, or Space object
        @rtype: BlogEntry list
        @return: list of BlogEntries published on space"""
        return tuple(BlogEntry.create(blogDict, self._modelDataManager) for blogDict in self.pm_getSpaceManager().listBlogEntries(self._unbox(space)))


    def getBlogEntry(self, id):
        """Get BlogEntry having the given id

        @type id: string, or BlogEntry object
        @param id: BlogEntry id, or BlogEntry object
        @return: BlogEntry"""
        return BlogEntry.create(self.pm_getSpaceManager().getBlogEntry(self._unbox(id)),self._modelDataManager)
        
        
    def linkPages(self, sourceSpaceKey, sourcePage, destSpaceKey, destPage = ""):
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
        
        pagesInSourceSpace = self.listPages(sourceSpaceKey)
        
        # Build  -pagesDict:   (page-id, page-object) pairs
        #        -childIdDict: (page-id, list of child-page id's) pairs
        pagesDict = dict([(page.id, page) for page in pagesInSourceSpace])
        childIdDict = dict([(id, []) for id in pagesDict.keys()])
        for id, page in pagesDict.iteritems():
            if page.parent.id and page.parent.id != '0':
                childIdDict[page.parent.id].append(id)
        
        # find sourcePageId
        if sourcePage.isdigit(): # parameter passed is the ID of the page
            sourcePageID = sourcePage
        else:
            sourcePageID = self.findPage(sourceSpaceKey, sourcePage).id
        
        # find destPageID, or create destination page
        if destPage and destPage.isdigit():
            destPageId = destPage
        else:
            try:
                destPageID = self.findPage(destSpaceKey, destPage).id
            except Exception, e:
                res = self.addPage( space   = destSpaceKey, 
                                    title   = destPage if destPage else pagesDict[sourcePageID].title,  # If the destPage param is defined, this will be the title of the page. Otherwise, use the same title as the source page.
                                    parent  = '0', # Orphaned page
                                    content = "{include:%s:%s}" % (sourceSpaceKey, pagesDict[sourcePageID].title) )
                destPageID = res.id
        
        def createChildPagesRecursively(parentSourceID, parentDestID):
            for childSourceID in childIdDict[parentSourceID]:
                res = self.addPage( space   = destSpaceKey, 
                                    title   = pagesDict[childSourceID].title,
                                    parent  = parentDestID,
                                    content = "{include:%s:%s}" % (sourceSpaceKey, pagesDict[childSourceID].title) )
                createChildPagesRecursively(childSourceID, res.id)
        
        createChildPagesRecursively(sourcePageID, destPageID)


    def listLabelsInPage(self, page):
        """List all Labels available for a given pageId (can be also used to list Labels for any ContentEntityObject ID)

        @type page: string, or Page object
        @param page: page id, or Page object
        @rtype: list of Labels
        @return: Labels
        """
        return tuple(Label.create(labelDict, self._modelDataManager) for labelDict in self.pm_getSpaceManager().getLabelsById(self._unbox(page)))


    def listLabelsInSpace(self, space, maxLabelsToReturn = 20):
        """List all Labels available for a given Space

        @type space: string, or Space object
        @param space: space key, or Space object
        @param maxLabelsToReturn: maximum number of labels to return
        @rtype: list of Labels
        @return: Labels
        """
        return tuple(Label.create(labelDict, self._modelDataManager) for labelDict in self.pm_getSpaceManager().getLabelsInSpace(self._unbox(space), maxLabelsToReturn))


    def addLabelToPage(self, name, page):
        """Add Label with name to given page

        @param name: Label name
        @type page: string, or Page object
        @param page: page id, or Page object
        @return: successfully added
        """
        return self.pm_getSpaceManager().addLabelToPage(name, self._unbox(page))


    def addLabelToSpace(self, name, space):
        """Add Label with name to given space

        @param name: Label name
        @type space: string, or Space object
        @param space: space key, or Space object
        @return: successfully added
        """
        return self.pm_getSpaceManager().addLabelToSpace(name, self._unbox(space))


    def removeLabelFromPage(self, label, page):
        """Remove Label from given Page

        @type label: String, or Label object
        @param label: label name, or Label object
        @type page: string, or Page object
        @param page: page id, or Page object
        @return: successfully removed
        """
        return self.pm_getSpaceManager().removeLabelFromPage(self._unbox(label), self._unbox(page))


    def removeLabelFromSpace(self, label, space):
        """
        Remove Label from given space

        @type label: String, or Label object
        @param label: label name, or Label object
        @type space: string, or Space object
        @param space: space key, or Space object
        @return: successfully removed
        """
        return self.pm_getSpaceManager().removeLabelFromSpace(self._unbox(label), self._unbox(space))

#################################### properties, setter and getters ################################

    def _unbox(self, value):
        """return the key of the given object if it implements Keyable interface, else return object"""
        try:
            return value.getKey()
        except AttributeError:
            return value

    #TODO: the special getter is used to avoid AttributeError(s)and mainly to highlight dependency injection. A basetype Bean or Popo (as in Pojo) which does this check would enable removing this getter
    def pm_getUserManager(self):
        if self._userManager == None:
            raise Exception( 'UserManager not configured properly')
        return self._userManager

    #TODO: the special getter is used to avoid AttributeError(s)and mainly to highlight dependency injection. A basetype Bean or Popo (as in Pojo) which does this check would enable removing this getter
    def pm_getSpaceManager(self):
        if self._spaceManager == None:
            raise Exception( 'SpaceManager not configured properly')
        return self._spaceManager

    #TODO: the special setter is unavoidable now, since it is used to copy in mutli attributes or otherwise maintain the two way association between the parent and child objects. a very special type TwoWayAssociationBean can replace this by a special setter. but such a type won't come around soon
    def pm_setUserManager(self, value):
        self._userManager = value
        self._userManager.server = self._server
        self._userManager.token = self._token

    #TODO: the special setter is unavoidable now, since it is used to copy in mutli attributes or otherwise maintain the two way association between the parent and child objects. a very special type TwoWayAssociationBean can replace this by a special setter. but such a type won't come around soon
    def pm_setSpaceManager(self, value):
        self._spaceManager = value
        self._spaceManager.server = self._server
        self._spaceManager.token = self._token

    def pm_setProxy(self, value):
        self._proxy = value
        self._modelDataManager = ModelDataManager.ModelDataManager(self._proxy)

    def pm_getProxy(self):
        return self._proxy
