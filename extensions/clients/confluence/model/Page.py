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
 
from pylabs import q
from pylabs.baseclasses import BaseType

from Keyable import Keyable
import Space
import ModelDataManager


class BasePage(object):
    """Marker base class, to reach a composite pattern effect with Page and Parent Pages, along with type checking"""
    pass

class Page(BaseType, BasePage, Keyable):

    space = q.basetype.object(BaseType, doc = "Page space", allow_none = True)
    title = q.basetype.string(doc = "Page title", allow_none = True)
    content = q.basetype.string(doc = "Page content", allow_none = False)
    parent = q.basetype.object(BasePage, doc = "Page parent", allow_none = True)
    version = q.basetype.string(doc = "Page version", allow_none = True)
    id = q.basetype.string(doc = "Page id", allow_none = True)
    url = q.basetype.string(doc = "Page url", allow_none = True)
    locks = q.basetype.string(doc = "Page locks", allow_none = True)
    created = q.basetype.string(doc = "Page created", allow_none = True)
    creator = q.basetype.string(doc = "Page creator", allow_none = True)
    modified = q.basetype.string(doc = "Page modified", allow_none = True)
    modifier = q.basetype.string(doc = "Page modifier", allow_none = True)
    homePage = q.basetype.string(doc = "Page homePage", allow_none = True)
    contentStatus = q.basetype.string(doc = "Page contentStatus", allow_none = True)
    current = q.basetype.string(doc = "Page current", allow_none = True)
    attachements = q.basetype.string(doc = "Page attachments", allow_none = True)
    subPages = q.basetype.list(doc = "Page subPages", allow_none = True)
    comments = q.basetype.string(doc = "Page comments", allow_none = True)

    _modelManager = q.basetype.object(object, doc = "ModelDataManager responsible for object load, save, edit", allow_none = True)

    def __init__(self, space = None, title = None, content = '', parent = None):
        BaseType.__init__(self)
        self.space = space
        self.title = title
        self.content = content
        self.parent = parent
        self.version = None
        self.id = None
        self.url = None
        self.locks = None
        self.created = None
        self.creator = None
        self.modified = None
        self.modifier = None
        self.homePage = None
        self.contentStatus = None
        self.current = None
        self.attachements = None
        self.subPages = None
        self.comments = None



    def toDict(self):
        """Return a dictionary that represents current instance field values"""
        variables = ('id', 'title', 'url', 'locks', 'version', 'content', 'created', 'creator', 'modified', 'modifier', 'homePage', 'contentStatus', 'current', 'attachements', 'subPages', 'comments')
        pageDict = dict((key, getattr(self, key)) for key in variables if getattr(self, key) is not None)
        #add Page instances of other object one by one
        try:
            pageDict['parentId'] = self.parent.id
        except AttributeError:
            pass #if self.parent does not exist do not add it to dict

        try:
            pageDict['space'] = self.space.key
        except AttributeError:
            pass #if self.space does not exist do not add it to dict
        return pageDict


    def __repr__(self):
        pageDict = self.toDict()
        try:
            del pageDict['content']
        except KeyError:
            pass
        return str(pageDict)


    def setKey(self, key):
        """Set key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, setting its key attribute(id, name ....etc)

        @param key: key attribute"""
        self.id = key


    def getKey(self):
        """Get key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, getting its key attribute(id, name ....etc)

        @return: key attribute"""
        return self.id

    ##########################
    ## Data access Behavior ##
    ##########################

    def save(self):
        """Save would save a new page if id = None, or edit an existing one if id is not None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.saveObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"

    def edit(self):
        """Edit an existing page, would throw an exception if id is None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.editObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    def load(self):
        """Load all attributes of a page using its id"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.loadObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    ####################
    ## Smart Behavior ##
    ####################

    def addAttachment(self, fileName, localPath, fileType, comment = ''):
        """Add attachment to page

        @param fileName: attachment name
        @param localPath: path to the local file to be uploaded as attachment
        @param fileType: type of the attachment (for example 'txt', 'gif'... etc)
        @param comment: user comment (default value is empty string)
        @rtype: Attachment
        @return: newly created Attachment"""

        return self._modelManager.confluenceProxy.addAttachment(self, fileName, localPath, fileType, comment)


    def addAttachmentFolder(self, localPath, fileType = None, comment = None):
        """Add all files at given directory as attachment to the given page

        @param localPath: the path of the directory on local machine
        @param fileType: type of the attachment (the default value is the file extension (the part of the file name following a dot), if there is no extension the default value is 'unknown-type'
        @param comment: user comment (default value is empty string)"""

        return self._modelManager.confluenceProxy.addAttachmentFolder(self, localPath, fileType, comment)


    def listAttachments(self):
        """Returns all the Attachments on this page

        @rtype: Attachment list
        @return: list of Attachment on page"""
        return self._modelManager.confluenceProxy.listAttachments(self)


    def getAttachment(self, name, version = None):
        """Return information about an attachment, if version is not specified latest version is returned

        @param name: attachment name
        @param version: attachment version(if default value, latest version is returned)
        @rtype: Attachment"""
        return self._modelManager.confluenceProxy.getAttachment(self, name, version)


    def downloadAttachment(self, name, localPath, version = None):
        """Download attachment file and save it in localPath parameter

        @param name: attachment name
        @param localPath: path of the local directory the attachment will be downloaded at
        @param version: attachment version(if not specified the latest version is downloaded)"""
        return self._modelManager.confluenceProxy.downloadAttachment(self, name, localPath, version)


    def downloadAttachments(self,localPath):
        """Download all attachment files of a given page and save them in localPath parameter

        @param localPath: path of the local directory the attachment will be downloaded at"""
        return self._modelManager.confluenceProxy.downloadAttachments(self, localPath)


    def remove(self):
        """Remove a page deleting it from confluence server"""
        return self._modelManager.confluenceProxy.removePage(self)


    def addComment(self, content):
        """Add comment to page

        @param content: comment content"""
        return self._modelManager.confluenceProxy.addComment(self, content)


    def  listLabels(self):
        """List all Labels available on this page

        @rtype: list of Labels
        @return: Labels
        """
        return self._modelManager.confluenceProxy.listLabelsInPage(self)


    def addLabel(self, name):
        """Add Label with name to page

        @param name: Label name
        @return: successfully added
        """
        return self._modelManager.confluenceProxy.addLabelToPage(name, self)


    def removeLabel(self, label):
        """Remove Label from Page

        @type label: String, or Label object
        @param label: label name, or Label object
        @return: successfully removed
        """
        return self._modelManager.confluenceProxy.removeLabelFromPage(label, self)


def create(dictionary, modelManager = None):
    """Factory method, construct Page object from a confluence page dictionary

    @param dictionary: confluence page dictionary(returned by confluence from methods returning page)
    @type modelManager: ModelDataManger instance
    @param modelManager: DataModelManager
    @rtype: Page
    @return: Page"""
    page = Page()
    page._modelManager = modelManager

    #the following keys will have a special handling so we must overwrite the values by the following conditions

    if 'space' in dictionary:
        page.space = Space.Space()
        page.space.key = dictionary['space']
        del dictionary['space']
    if 'parentId' in dictionary:
        page.parent = Page()
        page.parent.id = dictionary['parentId']
        del dictionary['parentId']
    for key, value in dictionary.iteritems():
        setattr(page, key, str(value))

    return page