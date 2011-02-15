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
import ModelDataManager
import Page

class Space(BaseType, Keyable):

    key = q.basetype.string(doc = "Space key", allow_none = True)
    name = q.basetype.string(doc = "Space name", allow_none = True)
    description = q.basetype.string(doc = "Space description", allow_none = True)
    url = q.basetype.string(doc = "Space url", allow_none = True)
    homePage = q.basetype.string(doc = "Space homepage", allow_none = True)
    type = q.basetype.string(doc = "Space type", allow_none = True)
    pages = q.basetype.list(doc = "Space pages", allow_none = True)

    _modelManager = q.basetype.object(ModelDataManager.ModelDataManager, doc = "ModelDataManager responsible for object load, save, edit", allow_none = True)

    def __init__(self, key = None, name = None, description = ''):
        BaseType.__init__(self)
        self.key = key
        self.name = name
        self.description = description
        self.homePage = None
        self.pages = None
        self.url = None
        self.type = None

    def toDict(self):
        """Return a dictionary that represents current instance field values"""
        variables = ('key', 'name', 'type', 'url', 'homePage')
        return dict((key, getattr(self, key)) for key in variables if getattr(self, key) is not None)

    def __repr__(self):
        return str(self.toDict())

    def setKey(self, key):
        """Set key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, setting its key attribute(id, name ....etc)

        @param key: key attribute"""
        self.key = key


    def getKey(self):
        """Get key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, getting its key attribute(id, name ....etc)

        @return: key attribute"""
        return self.key

    ##########################
    ## Data access Behavior ##
    ##########################
    def save(self):
        """Save would save a new space if id = None, or edit an existing one if id is not None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.saveObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"

    def edit(self):
        """Edit an existing space, would throw an exception if id is None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.editObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    def load(self):
        """Load all attributes of Space using its id"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.loadObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    def remove(self):
        """Remove a Space

        @rtype: boolean
        @return: successfully removed"""
        return self._modelManager.confluenceProxy.removeSpace(self)

    ####################
    ## Smart Behavior ##
    ####################

    def addPage(self, title, parent = None, content = ''):
        """Create a Page

        @param title: page title
        @type parent: string, or Page object
        @param parent: the page id of the parent page, or Page object of the parent page(if not passed the page has no parent)
        @param content: page content written as wiki text
        @rtype: Page
        @return: newly created Page"""
        return Page.create(self._modelManager.confluenceProxy.addPage(self, title, parent, content).toDict(), self._modelManager)

    def listPages(self):
        """Return a list of available pages in this space

        @rtype: Page list
        @return: list of Pages contained in space"""
        return self._modelManager.confluenceProxy.listPages(self)

    def addBlogEntry(self, title, content = ''):
        """Create a BlogEntry on space parameter

        @param title: BlogEntry title
        @param content: BlogEntry content written as wiki text(default is empty content)
        @rtype: BlogEntry
        @return: newly created BlogEntry"""
        return self._modelManager.confluenceProxy.addBlogEntry(self, title, content)


    def listBlogEntries(self):
        """List all BlogEntries contained in Space parameter

        @rtype: BlogEntry list
        @return: list of BlogEntries published on space"""
        return self._modelManager.confluenceProxy.listBlogEntries(self)


    def  listLabels(self):
        """List all Labels available on this Space

        @rtype: list of Labels
        @return: Labels
        """
        return self._modelManager.confluenceProxy.listLabelsInSpace(self)


    def addLabel(self, name):
        """Add Label with name to Space

        @param name: Label name
        @return: successfully added
        """
        return self._modelManager.confluenceProxy.addLabelToSpace(name, self)


    def removeLabel(self, label):
        """Remove Label from Space

        @type label: String, or Label object
        @param label: label name, or Label object
        @return: successfully removed
        """
        return self._modelManager.confluenceProxy.removeLabelFromSpace(label, self)


def create(dictionary, modelManager = None):
    """Factory method, construct Space object from a confluence Space dictionary

    @param dictionary: confluence Space dictionary(returned by confluence from methods returning Space)
    @type modelManager: ModelDataManger instance
    @param modelManager: DataModelManager
    @rtype: Space
    @return: Space"""
    space = Space()

    space._modelManager = modelManager

    for key, value in dictionary.iteritems():
        setattr(space, key, value)

    return space
