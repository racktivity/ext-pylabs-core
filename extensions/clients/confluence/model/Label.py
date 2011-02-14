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

class Label(BaseType, Keyable):

    name = q.basetype.string(doc = "Name of the label", allow_none = True)
    owner = q.basetype.string(doc = "Username of the owner", allow_none = True)
    namespace = q.basetype.string(doc = "Namespace of the label", allow_none = True)
    id = q.basetype.integer(doc = "ID of the label", allow_none = True)

    _modelManager = q.basetype.object(object, doc = "ModelDataManager responsible for object load, save, edit", allow_none = True)


    def __init__(self, name = None):
        BaseType.__init__(self)
        self.name = name
        self.owner = None
        self.namespace = None
        self.id = None


    def toDict(self):
        """Return a dictionary that represents current instance field values"""
        variables = ('name', 'owner', 'namespace', 'id')
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


    #TO-DO add smart behavior to Label object


def create(dictionary, modelManager = None):
    """Factory method, construct Label object from a confluence Label dictionary

    @param dictionary: confluence Label dictionary(returned by confluence from methods returning Label)
    @type modelManager: ModelDataManger instance
    @param modelManager: DataModelManager
    @rtype: Label
    @return: Label"""
    label = Label()
    if modelManager:
        label._modelManager = modelManager

    for key, value in dictionary.iteritems():
        try:
            setattr(label, key, value)
        except ValueError:
            setattr(label, key, int(value))

    return label