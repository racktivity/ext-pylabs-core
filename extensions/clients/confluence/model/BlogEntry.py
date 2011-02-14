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
 
from pymonkey import q
from pymonkey.baseclasses import BaseType

from Keyable import Keyable
import Space
import ModelDataManager



class BlogEntry(BaseType, Keyable):
    """Model Object to encapsulate BlogEntry fields returned by Confluence portal"""

    id = q.basetype.string(doc = "The id of the blog entry", allow_none = True, default = None)
    space = q.basetype.object(Space.Space, doc = "The space of the blog entry", allow_none = True, default = None)
    title = q.basetype.string(doc = "The title of the blog entry", allow_none = True, default = None)
    url = q.basetype.string(doc = "The url to view this blog entry online", allow_none = True, default = None)
    version = q.basetype.integer(doc = "The version number of this blog entry", allow_none = True)
    content = q.basetype.string(doc = "The blog entry content", allow_none = True, default = None)
    locks = q.basetype.integer(doc = "The number of locks current on this blog entry", allow_none = True)
    publishDate = q.basetype.string(doc = "The date the blog post was published", allow_none = True, default = None)

    _modelManager = q.basetype.object(ModelDataManager.ModelDataManager, doc = "ModelDataManager responsible for object load, save, edit", allow_none = True)


    def __init__(self, id = None, space = None, title =None, content = ''):
        BaseType.__init__(self)
        self.id = id
        self.space = space
        self.title = title
        self.content = content


    def toDict(self):
        """Return a dictionary that represents current instance field values"""

        variables = ('id', 'title', 'url', 'version', 'content', 'locks', 'publishDate')
        blogEntryDict = (dict((key, getattr(self, key)) for key in variables if getattr(self, key) is not None))

        try:
            blogEntryDict['space'] = self.space.key
        except AttributeError:
            pass #if self.space does not exist do not add it to dict

        return blogEntryDict


    def __repr__(self):
        return str(self.toDict())


    def setKey(self, key):
        """Set key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, setting its key attribute(id, name ....etc)

        @param key: key attribute"""
        self.id = key


    def getKey(self):
        """Get key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, getting its key attribute(id, name ....etc)

        @return: key attribute"""
        return self.id


    def save(self):
        """Save would save a new BlogEntry if id = None, or edit an existing one if id is not None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.saveObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    def edit(self):
        """Edit an existing BlogEntry, would throw an exception if id is None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.editObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    def load(self):
        """Load all attributes of BlogEntry using its id"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.loadObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"



def create(dictionary, modelManager = None):
    """Factory method, construct BlogEntry object from a confluence BlogEntry dictionary

    @param dictionary: confluence BlogEntry dictionary(returned by confluence from methods returning BlogEntry).
    @type modelManager: ModelDataManger
    @param modelManager: DataModelManager instance
    @rtype: BlogEntry
    @return: BlogEntry"""
    blogEntry = BlogEntry()

    blogEntry._modelManager = modelManager

    #the following keys will have a special handling so we must overwrite the values by the following conditions
    try:
        blogEntry.space = Space.Space()
        blogEntry.space.key = dictionary['space']
        del dictionary['space']
    except KeyError:
        pass #no-op

    #list containing all numeric fields expected to be returned by confluence portal
    integerFieldslist = ['version', 'locks']

    #convert numeric fields to integer, set them in blogEntry, before setting blogEntry string fields
    for field in integerFieldslist:
        try:
            setattr(blogEntry, field, int(dictionary[field]))
            del dictionary[field]
        except KeyError:
            pass #no-op


    for key, value in dictionary.iteritems():
        setattr(blogEntry, key, str(value))

    return blogEntry