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

from pymonkey import q
from pymonkey.baseclasses.BaseType import BaseType

from model.BlogEntry import BlogEntry
import model.Space as Space
from model.AttachmentProxy import AttachmentProxy
import Utils



class SpaceManager(BaseType):
    """The handler of all space and page related operation users of this class should set server and logger

    This layer in the application always accept parameters as primitive types, either passes in as primitive values or unboxed by the upper layer ConfluenceImpl from model object, extracting primitive key values from them
    all the return types from the methods that do return a value are primitive dictionaries as well, the boxing into model object is done as well by the upper layer, ConfluenceImpl"""

    token = q.basetype.string(doc='session token')

    def __init__(self, logger):
        self._server = None
        self._logger = logger


    def listSpaces(self):
        """Return a list of Spaces Objects available to the current user

        @rtype: dictionary list
        @return: Spaces"""
        return self.server.getSpaces(self.token)

    def addSpace(self, key , name , description = ''):
        """Create a Space

        @param key: the key for the new space (must be unique)
        @param name: the space name
        @param description: the space description (default value is empty string)
        @rtype: dictionary
        @return: newly created Space"""
        missingMandatoryArgs = list()
        if not key:
            missingMandatoryArgs.append('key')

        if not name:
            missingMandatoryArgs.append('name')

        if missingMandatoryArgs:
            raise ValueError('missing mandatory argument %(args)s' % {'args': str(missingMandatoryArgs)} )

        space = Space.Space(key, name, description)
        try:
            spaceDict = self.server.addSpace(self.token, space.toDict())
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to add space with key %s' % (space.key) + '. Reason %s' % Utils.extractDetails(ex))
        #populate space summary
        return spaceDict

    def getSpace(self, key):
        """Return a Space object

        @param key: space key
        @rtype: dictionary
        @return: Space"""
        try:
            spaceDict = self.server.getSpace(self.token, key)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to get space with key %s' % key + '. Reason %s' % Utils.extractDetails(ex))

        return spaceDict


    def getPage(self, id):
        """Return a Page object

        @param id: page id
        @rtype: dictionary
        @return: Page"""
        try:
            pageDict = self.server.getPage(self.token, id)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to find page %s' % id + '. Reason %s' % Utils.extractDetails(ex))
        return pageDict


    def findPage(self, spaceKey, title):
        """Return a Page object

        @param spaceKey: key of the space to search for page in
        @param title: the title of the page
        @rtype: dictionary
        @return: page"""
        try:
            pageDict = self._getServer().getPage(self.token, spaceKey, title)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to find page %s in space %s' % (title,spaceKey) + '. Reason %s' % Utils.extractDetails(ex))
        return pageDict


    def removeSpace(self, key):
        """Remove a Space

        @param key: space key
        @return: boolean successfully removed"""
        try:
            result = self.server.removeSpace(self.token, key)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to remove space with key %s' % key + '. Reason %s' % Utils.extractDetails(ex))

        if result:
            return result
        else:
            raise Exception( 'Unable to remove space with key %s' % key + '. Reason %s' % Utils.extractDetails(ex))


    def listPages(self, spaceKey):
        """Return a list of available pages in this space

        @param spaceKey: space key of space to list pages of
        @rtype: dictionary list
        @return: page fields"""
        try:
            spacePages = self.server.getPages(self.token, spaceKey)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to list pages in space with key %s' % spaceKey + '. Reason %s' % Utils.extractDetails(ex))
        #TODO construct a list of Page objects and return it, don't just return the dictionary
        return spacePages


    def addPage(self, spaceKey, title, parentId = None, content = ''):
        """Create a Page

        @param spaceKey: space key for the page to be added in
        @param title: page title
        @param parentId: the page id of the parent page (if not passed the page has no parent)
        @param content: page content written as wiki text
        @rtype: dictionary
        @return: newly created page values"""
        #construct a page dictionary this step should be replace by a creation of a Page object
        missingMandatoryArgs = list()
        if not spaceKey:
            missingMandatoryArgs.append('spaceKey')

        if not title:
            missingMandatoryArgs.append('title')

        if missingMandatoryArgs:
            raise ValueError('Missing mandatory argument %(args)s' % {'args': str(missingMandatoryArgs)} )

        pageDict = {}
        pageDict['space'] = spaceKey
        pageDict['title'] = title
        pageDict['content'] = content
        if parentId:
            pageDict['parentId'] = parentId
        pageDict = self.editPage(pageDict)
        return pageDict


    def addAttachment(self, pageId, fileName, localFilePath, fileType, comment = None):
        """Add a single attachment to a given page

        @param pageId: page id of the page that attachment should be added in
        @param fileName: attachment name
        @param localPath: path to the local file to be uploaded as attachment
        @param fileType: type of the attachment
        @param comment: user comment (default value is empty string)
        @rtype: dictionary
        @return: attachment values"""
        attachmentFile = None
        try:
            attachmentFile = open(localFilePath, 'rb')#reads file as binary
        except IOError, ex:
            self._logger.log(ex, 3)
            raise IOError( 'No file found at given file path %s' % localFilePath)
        fileData = attachmentFile.read()
        fileBinData = xmlrpclib.Binary(fileData)
        #construct an Attachment object this step should be done by initializing an Attachment object, and it is done so only as a first iteration
        attachmentDict = {}
        attachmentDict['fileName'] = fileName
        if not fileType == None:
            attachmentDict['contentType'] = fileType
        if not comment == None:
            attachmentDict['comment'] = comment
        try:
            attachmentDict = self.server.addAttachment(self.token, pageId, attachmentDict, fileBinData)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to save attachment with name %s' % fileName + '. Reason %s' % Utils.extractDetails(ex))
        return attachmentDict


    def addAttachmentFolder(self, pageId, localPath, fileType = None, comment = None):
        """Add all files at given directory as attachment to the given page

        @param pageId: page id to add attachment in
        @param localPath: the path of the directory on local machine
        @param fileType: type of the attachment (if Directory equals True, the default value is the file extension(the part of the file name following a dot), if there is no extension the default value is 'unknown-type'
        @param comment: user comment (default value is empty string)"""

        defaultType = 'unknown-type'
        if not q.system.fs.isDir(localPath):
            raise Exception( 'given path is not a directory %s' % localPath)
        filePaths = q.system.fs.listFilesInDir(localPath)
        for path in filePaths:
            name = q.system.fs.getBaseName(path) #get the file name
            #get the file type if there is not a default value is stored
            if fileType == None:
                fileNameSplitted = name.rsplit('.',1)
                fileNameSplittedLength = len(fileNameSplitted)
                if fileNameSplittedLength > 0: #there is a '.' in the file name
                    fileType = fileNameSplitted[fileNameSplittedLength-1]
                else: fileType = defaultType #there is no '.' in file name, so the default value is used
            #call _addAttachment except Exception and collect result or exception in resultList
            self.addAttachment(pageId, name, path, fileType, comment)


    def removeAttachment(self, pageId, name):
        """Remove an attachment from this page

        @param pageId: id of the page containing this attachment
        @param name: attachment name
        @rtype: boolean
        @return: successfully removed"""
        try:
            return self.server.removeAttachment(self.token, pageId, name)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to remove attachment: %s in page: %s' % (pageId,name) + '. Reason %s' % Utils.extractDetails(ex))


    def moveAttachment(self, originalPageId, originalName, newPageId = None, newName = None):
        """Move an attachment to a different content entity object and/or give it a new name.
        at most one parameter can take the default value (either newPageId parameter, or newName parameter.

        @param originalPageId: the page id of the original page containing the attachment.
        @param originalName: the original name of the attachment.
        @param newPageId: page id of the page the attachment will be moved at (if not mentioned the attachment will not be moved to another page).
        @param newName: the attachment new name (if not mentioned the attachment will keep his current name).
        @rtype: boolean
        @return: successfully moved"""
        if (newName == None and newPageId == None):
            raise Exception( 'newPage and newName parameters cannot both be empty')
        if (newName == None or newName == ''):
            newName = originalName
        if newPageId == None:
            newPageId = originalPageId
        try:
             return self.server.moveAttachment(self.token, originalPageId, originalName, newPageId, newName)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to move attachment %s in page %s' % (originalName, originalPageId) + '. Reason %s' % Utils.extractDetails(ex))


    def listAttachments(self, pageId):
        """Return all the Attachments for this page

        @param pageId: page id of the page to list attachment in
        @rtype: dictionary list
        @return: attachment fields"""
        try:
            attachmentDictList = self.server.getAttachments(self.token, pageId)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to list attachments in page %s' % pageId + '. Reason %s' % Utils.extractDetails(ex))

        return attachmentDictList


    def getAttachment(self, pageId, name, version = None):
        """Return information about an attachment
        if version is not specified latest version is returned

        @param pageId: page id of the page containing the attachment
        @param name: attachment name
        @param version: attachment version(if not specified the latest version is returned)"""
        if version:
            try:
                attachmentDict = self.server.getAttachment(self.token, pageId, name, str(version))
                return attachmentDict
            except Exception, ex:
                self.logger.log(str(ex), 3)
                raise Exception( 'Unable to get attachment %s in page %s' % (name, pageId) + '. Reason %s' % Utils.extractDetails(ex))
        else:
            #version is not specified, so list all attachment in page as there is no direct way to get latest attachment version
            attachmentList = self.listAttachments(pageId)
            attachment = None
            #search for attachment with the given name
            for attachment in attachmentList:
                if attachment['fileName'] == name:
                    return attachment
            if attachment == None:
                raise Exception( 'Unable to get attachment %s in page %s' % (name, pageId) + '. Reason %s' % Utils.extractDetails(ex))


    def downloadAttachment(self, pageId, name, localDirPath, version = None):
        """Download an attachment file and save it on local machine

        @param pageId: page id of the page containing the attachment
        @param name: attachment name
        @param localDirPath: path of the local directory the attachment will be downloaded at
        @param version: attachment version(if not specified the latest version is returned)"""
        if not q.system.fs.isDir(localDirPath):
            raise Exception( 'No directory found with path %s' % localDirPath)
        localFilePath =  q.system.fs.joinPaths(localDirPath,name)
        if q.system.fs.exists(localFilePath):
            raise Exception( 'File allready exists with path %s' %localFilePath)
        if not version:
            #user did not specify version, getting latest file version
            #need to create object Attachment to be able to get version as it is not a key in attachment dictionary, but is extracted from url
            attachment = AttachmentProxy(self.getAttachment(pageId, name))
            try:
                attachmentData = self.server.getAttachmentData(self.token, pageId, name, attachment.version)
            except Exception, ex:
                self.logger.log(str(ex), 3)
                raise Exception( 'Unable to download attachment %s in page %s' % (name, pageId) + '. Reason %s' % Utils.extractDetails(ex))
        else:
            try:
                attachmentData = self.server.getAttachmentData(self.token, pageId, name, str(version))
            except Exception, ex:
                self.logger.log(str(ex), 3)
                raise Exception( 'Unable to download attachment %s in page %s version %s' % (name, pageId,version) + '. Reason %s' % Utils.extractDetails(ex))
        #checking if file exists,if it does not create the file and any necessary directory in the path
        q.system.fs.writeFile(localFilePath, attachmentData.data)


    def downloadAttachments(self, pageId, localDirPath):
        """Download all attachment files of a given page and save them on local machine

        @param pageId: page id of the page containing the attachment
        @param localDirPath: path of the local directory the attachment will be downloaded at"""
        if not q.system.fs.isDir(localDirPath):
            raise Exception( 'No directory found with path %s' % localDirPath)
        attachmentList = self.listAttachments(pageId)
        for attachmentDict in attachmentList:
            #need to create object Attachment to be able to get version as it is not a key in attachment dictionary, but is extracted from url
            attachment = AttachmentProxy(attachmentDict)
            self.downloadAttachment(pageId, attachment.fileName, localDirPath, attachment.version)


    def removePage(self, id):
        """Remove a page deleting it from confluence server

        @param id: page id"""
        try:
            self._server.removePage(self.token, id)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to remove page %s' % id)


    def search(self, query, spaceKey = None, typeFilter = None, lastModifiedFilter = None, maxResults = 50):
        """Return a list of SearchResults which match a given search query parameter (including pages and other content types),
        limit your search by adding space parameter, typeFilter parameter, and lastModifiedFilter parameter.
        If you do not include a parameter, the default is used instead

        @param query: text line to search for
        @param spaceKey: space key(if not mentioned the search includes all spaces)
        @param typeFilter: one of the values listed by calling: q.enumerators.ConfluenceTypeFilter, for example q.enumerators.ConfluenceTypeFilter.all, q.enumerators.ConfluenceTypeFilter.page, etc ...(if not mentioned the search includes all types except mail)
        @param lastModifiedFilter: one of the values listed by calling: q.enumerators.ConfluenceLastModifiedFilter, for example q.enumerators.ConfluenceLastModifiedFilter.TODAY, q.enumerators.ConfluenceLastModifiedFilter.LASTWEEK, etc ...(if not mentioned the search puts no time restriction on result)
        @param maxResults: search max result(default value is 50)
        @rtype: dictionary list
        @return: search result"""
        parameters = {}
        if spaceKey != None:
            parameters['spaceKey'] = spaceKey
        if typeFilter != None:
            parameters['type'] = str(typeFilter)
        if lastModifiedFilter != None:
            parameters['lastModified'] = str(lastModifiedFilter)
        try:
            return self._server.search(self.token, query, parameters, maxResults)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to search for line %s' % query + '. Reason %s' % Utils.extractDetails(ex))


    def addPersonalSpace(self,userName ,title, description = ''):
        """Create a personal space to user

        @param userName: user name to create personal space for
        @param title: the space name
        @param description: the space description (default value is empty string)
        @rtype: dictionary
        @return: Space"""
        key = ''
        #the key is neglected and generated by confluence in this method,
        #the creation of Space object needs a key, so an empty string is used,
        #the space returned from confluence must have a key,
        # so this exceptional space object( space with empty string key) existance is limited to
        #this method namespace and is hidden from client code
        space = Space.Space(key, title, description)
        try:
            spaceDict = self._server.addPersonalSpace(self.token, space.toDict(), userName)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to add personal space %s to user %s' %(title, userName) + '. Reason %s' % Utils.extractDetails(ex))

        return spaceDict


    def createPageFromFile(self, localFilePath, spaceKey, title = None, parentId = None, addFileAsAttachment = False):
        """Create a page and add the localFilePath path content as the page content

        @param localPath: the path of the file on local machine containing the wiki text to be used as new page content
        @param spaceKey: space key
        @param title: page title(if not mentioned the file name will be used as a title)
        @param parentId: the page id of the parent page (if not passed the page has no parent)
        @param addFileAsAttachment: if True, the file specified is added as attachment to the page(if not mentioned no attachment is created)
        @rtype: dictionary
        @return: Page"""
        attachmentFile = None
        try:
            attachmentFile = open(localFilePath)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'No file found at given file path %s' % localFilePath)
        fileData = attachmentFile.read()
        if title == None:
            title = q.system.fs.getBaseName(localFilePath) #get the file name
        page = self.addPage(spaceKey, title, parentId, fileData)
        if addFileAsAttachment:
            self.addAttachment(page['id'], title, localFilePath, 'txt')
        return page


    def addComment(self, pageId, content = ''):
        """Add comment to page

        @param pageId: page id
        @param content: comment content
        @rtype: dictionary
        @return: newly added comment fields"""
        comment = {}
        comment = {
                   'pageId': pageId,
                    'content': content}
        try:
            return self._server.addComment(self.token, comment)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception( 'Unable to add comment in page %s' % (pageId) + '. Reason %s' % Utils.extractDetails(ex))

    def editPage(self, page):
        """update content of page

        @type page: dictionary
        @param page: dictionary of Page having the updated content
        @rtype: dictionary
        @return: updated Page Object"""
        try:
            return self.server.storePage(self.token, page)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to add page with title %s' % page['title'] + '. Reason %s' % Utils.extractDetails(ex))

    def editSpace(self, space):
        """update content of space

        @type page: dictionary
        @param page: dictionary of Space having the updated content
        @rtype: dictionary
        @return: updated Space Object"""
        try:
            return self.server.storeSpace(self.token, space)
        except Exception, ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to store space with name %s' % space['name'] + '. Reason %s' % Utils.extractDetails(ex))

    def addBlogEntry(self, space, title, content):
        """Create a BlogEntry on Confluence portal

        @param space: space key to add BlogRntry in
        @param title: BlogEntry title
        @param content: BlogEntry content written as wiki text(default is empty content)
        @rtype: dictionary
        @return: BlogEntry fields"""
        try:
            blogEntryDict = {'space':space, 'title':title, 'content':content}
            return self.server.storeBlogEntry(self.token, blogEntryDict)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to add blogEntry with title %s' % title + '. Reason %s' % Utils.extractDetails(ex))


    def listBlogEntries(self, space):
        """List all BlogEntries contained in Space

        @param space: space key to list BlogRntries in
        @rtype: list of dictionaries
        @return: BlogEntry fields"""
        try:
            return self.server.getBlogEntries(self.token, space)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to list blogEntries in space %s' % space + '. Reason %s' % Utils.extractDetails(ex))


    def getBlogEntry(self, id):
        """Get BlogEntry having the given id

        @param id: BlogEntry id
        @rtype: dictionary
        @return: BlogEntry fields"""
        try:
            return self.server.getBlogEntry(self.token, id)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to get blogEntry with id %s' % id + '. Reason %s' % Utils.extractDetails(ex))


    def getLabelsById(self, pageId):
        """List Labels for given page

        @param pageId: page id
        @rtype: list of dictionaries
        @return: Labels
        """
        try:
            return self.server.getLabelsById(self.token, pageId)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to list Labels for page with id %s' % pageId + '. Reason %s' % Utils.extractDetails(ex))


    def getLabelsInSpace(self, spaceKey, maxLabelsToReturn = 20):
        """List Labels in Space

        @param spaceKey: space key
        @param maxLabelsToReturn: maximum number of labels to return
        @rtype: list of dictionaries
        @return: Labels
        """
        try:
            return self.server.getMostPopularLabelsInSpace(self.token, spaceKey, maxLabelsToReturn)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to list Labels for space with key %s' % spaceKey + '. Reason %s' % Utils.extractDetails(ex))


    def addLabelToPage(self, name, pageId):
        """Add Label to given page

        @param name: Label name
        @param pageId: page id
        @return: successfully added
        """
        try:
            return self.server.addLabelByName(self.token, name, pageId)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to add Label with name %(labelName)s for page with id %(page)s' %{'labelName':name, 'page':pageId} + '. Reason %s' % Utils.extractDetails(ex))


    def addLabelToSpace(self, name, spaceKey):
        """Add Label to given page

        @param name: Label name
        @param spaceKey: space key
        @return: successfully added
        """
        try:
            return self.server.addLabelByNameToSpace(self.token, name, spaceKey)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to add Label with name %(labelName)s for space with key %(space)s' %{'labelName':name, 'space':spaceKey} + '. Reason %s' % Utils.extractDetails(ex))


    def removeLabelFromPage(self, labelName, pageId):
        """
        Remove Label from given Page

        @param labelName: label name
        @param pageId: page id
        @return: successfully removed
        """
        try:
            return self.server.removeLabelByName(self.token, labelName, pageId)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to remove Label with name %(labelName)s from page with id %(page)s' %{'labelName':labelName, 'page':pageId} + '. Reason %s' % Utils.extractDetails(ex))


    def removeLabelFromSpace(self, labelName, spaceKey):
        """
        Remove Label from given space

        @param labelName: label name
        @param spaceKey: space key
        @return: successfully removed
        """
        try:
            return self.server.removeLabelByNameFromSpace(self.token, labelName, spaceKey)
        except Exception,ex:
            self.logger.log(str(ex), 3)
            raise Exception('Unable to remove Label with name %(labelName)s from space with key %(space)s' %{'labelName':labelName, 'space':spaceKey} + '. Reason %s' % Utils.extractDetails(ex))


################################################ properties, setters and getters #########################################
    #TODO find out the correct types to supply to q.basetype.object init method for Logger and xmlrpc server, and remove properties
    def _getLogger(self):
        return self._logger


    def _setLogger(self, value):
        self._logger = value


    def _delLogger(self):
        del self._logger

    logger = property(_getLogger, _setLogger, _delLogger, "q.logger")

    def _getServer(self):
        return self._server


    def _setServer(self, value):
        self._server = value

    def _delServer(self):
        del self._server

    server = property(_getServer, _setServer, _delServer, "Confluence server proxy")
