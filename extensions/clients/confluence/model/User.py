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

class User(BaseType, Keyable):

    name = q.basetype.string(doc = "User name", allow_none = True)
    fullname = q.basetype.string(doc = "User fullname", allow_none = True)
    email = q.basetype.string(doc = "User email", allow_none = True)
    url = q.basetype.string(doc = "User url", allow_none = True)
    groups = q.basetype.dictionary(doc = "User groups", allow_none = True, default = dict())

    _modelManager = q.basetype.object(object, doc = "ModelDataManager responsible for object load, save, edit", allow_none = True)


    def __init__(self, name = None, fullname = None):
        BaseType.__init__(self)
        self.name = name
        self.fullname = fullname
        self.email = None
        self.url = None
        self.groups = None

    def toDict(self):
        """Return a dictionary that represents current instance field values"""
        variables = ('name', 'fullname', 'email', 'url', 'groups')
        return dict((key, getattr(self, key)) for key in variables if getattr(self, key) is not None)



    def __repr__(self):
        return str(self.toDict())


    def setKey(self, key):
        """Set key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, setting its key attribute(id, name ....etc)
        @param key: key attribute"""
        self.name = key


    def getKey(self):
        """Get key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, getting its key attribute(id, name ....etc)
        @return: key attribute"""
        return self.name

    ##########################
    ## Data access Behavior ##
    ##########################

    def save(self):
        """Save would save a new User if id = None, or edit an existing one if id is not None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.saveObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"

    def edit(self):
        """Edit an existing User, would throw an exception if id is None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.editObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    def load(self):
        """Load all attributes of a User using its id"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.loadObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"

    def removeUser(self):
        """Remove a user

        @rtype: boolean
        @return: successfully removed"""
        return self._modelManager.confluenceProxy.removeUser(self)

def create(dictionary, modelManager = None):
    """Factory method, construct User object from a confluence user dictionary

    @param dictionary: confluence user dictionary(returned by confluence from methods returning user)
    @type modelManager: ModelDataManger instance
    @param modelManager: DataModelManager
    @rtype: User
    @return: User"""
    user = User()
    if modelManager:
        user._modelManager = modelManager

    for key, value in dictionary.iteritems():
        setattr(user, key, value)

    return user