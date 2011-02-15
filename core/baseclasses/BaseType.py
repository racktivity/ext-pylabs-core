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

import pylabs
from pylabs.pmtypes.base import BaseType as TypeBaseType

def generate_init_properties(cls, attrs):
    '''Generate a class __init_properties__ method

    @param cls: Type to generate method for
    @type cls: type
    @param attrs: Class construction attributes
    @type attrs: dict

    @returns: __init_properties__ method
    @rtype: method
    '''
    def __init_properties__(self):
        '''Initialize all properties with their default value'''

        pylabs.q.logger.log('Initialize all properties with their default '
                              'value for instance of %s' % \
                              self.__class__.__name__, 7)

        # Call superclass __init_properties__, if any. No-op otherwise
        base = super(cls, self)
        if hasattr(base, '__init_properties__'):
            base.__init_properties__()

        for name, attr in (p for p in attrs.iteritems() \
                            if isinstance(p[1], TypeBaseType)):
            value = attr.get_default(self)
            setattr(self, attr.attribute_name, value)
            pylabs.q.logger.log('Set attr %s to %r' % \
                                  (attr.attribute_name, value), 9)

    return __init_properties__


class BaseTypeMeta(type):
    '''Meta class for all BaseTypes, makes sure we know the name of descriptor attributes'''

    def __new__(cls, name, bases, attrs):
        t = type.__new__(cls, name, bases, attrs)

        try:
            #If this *is* 'BaseObject' we don't want to do anything special with it
            #This raises a NameError if BaseObject is not 'known' yet
            BaseType
        except NameError:
            return t

        # Store attribute name on BaseType attributes
        for name, value in (p for p in attrs.iteritems() \
                            if isinstance(p[1], TypeBaseType)):
            value._PM_NAME = name

        #Generate __init_properties__
        ip = generate_init_properties(t, attrs)
        setattr(t, '__init_properties__', ip)

        property_metadata = dict()
        for base in bases:
            property_metadata.update(
                getattr(base, 'pm_property_metadata', dict()))
        for name, value in (p for p in attrs.iteritems() \
                            if isinstance(p[1], TypeBaseType)):
            property_metadata[name] = value.constructor_args

        setattr(t, 'pm_property_metadata', property_metadata)

        return t


class BaseType(object):

    __metaclass__ = BaseTypeMeta

    def __init__(self):
        """
        Initialize basetype
        
        During initialization all pmtype properties are set to their default
        values. This is only done when an object is created for the first time,
        otherwise the property values would be overwritten when e.g. restoring
        an object from the cmdb.        
        """

        pylabs.q.logger.log('Checking if properties need to be initialized '
                              'for %s instance' % self.__class__.__name__, 7)
        
        if not hasattr(self, '_pm__initialized'):
            self.__init_properties__()
        self._pm__initialized = True