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
from User import User

class Group(BaseType, Keyable):

    name = q.basetype.string(doc = "Group name", allow_none = True)

    _modelManager = q.basetype.object(object, doc = "ModelDataManager responsible for object load, save, edit", allow_none = True)

    def __init__(self, name = None):
        BaseType.__init__(self)
        self.name = name

    def toDict(self):
        return {'name': self.name}

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


    def save(self):
        """Save would save a new Group if id = None, or edit an existing one if id is not None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.saveObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"

    def edit(self):
        """Edit an existing Group, would throw an exception if id is None"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.editObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


    def load(self):
        """Load all attributes of a Group using its id"""
        if self._modelManager:
            self.__dict__.update( self._modelManager.loadObject(self).__dict__) #update Confluence portal
            return self #can be void, but returning self would support method chaining
        else:
            raise ValueError, "ModelManager is not set properly"


def create(groupName, modelManager = None):
    """Factory method, construct Group object from a confluence Group dictionary

    @param dictionary: confluence Group dictionary(returned by confluence from methods returning Group)
    @type modelManager: ModelDataManger
    @param modelManager: DataModelManager instance
    @rtype: Group
    @return: Group"""
    group = Group()
    if modelManager:
        group._modelManager = modelManager
    group.name = groupName
    return group