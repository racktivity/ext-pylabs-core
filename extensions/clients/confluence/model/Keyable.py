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
 
class Keyable(object):
    """Interface for model object containing key parameter

    classes extending <<Keyable>> can be used with auto boxing and unboxing mechanism
    By boxing and unboxing we mean automatically transforming primitive key string to the corresponding full blown object and vice versa.
    A mechanism similar to method overloading is possible for such family of object, you can pass in an instance of the object, or
    simply its key string to interact with the entity at hand. For example  you can call an rpc method like addUserToGroup can be called using (User, Group) instances, or corresponding keys ("userName", "groupName").
    Specifying which field is the key field for a certain entity is the job of the subclasses, by overriding setKey() and getKey()"""

    _ERROR_MESSAGE = "not yet implemented"

    def __init__(self):
        if self.__class__ == Keyable:
            raise TypeError( 'can\'t instantiate an interface')


    def setKey(self, key):
        """Set key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, setting its key attribute(id, name ....etc)
        @param key: key attribute"""
        raise Exception( Keyable._ERROR_MESSAGE)


    def getKey(self):
        """Get key attribute used by confluence as an identifier for the corresponding model object, each class will override this method, getting its key attribute(id, name ....etc)
        @return: key attribute"""
        raise Exception( Keyable._ERROR_MESSAGE)