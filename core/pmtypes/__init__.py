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

__all__ = ['IPv4Address', 'IPv4Range']

from pylabs.pmtypes.IPAddress import IPv4Address, IPv4Range

__all__ += ['Boolean', 'Integer', 'Float', 'String']
from pylabs.pmtypes.PrimitiveTypes import Boolean, Integer, Float, String

__all__ += ['List', 'Set', 'Dictionary']
from pylabs.pmtypes.CollectionTypes import List, Set, Dictionary

__all__ += ['Guid', 'Path', 'DirPath', 'FilePath', 'UnixDirPath',
            'UnixFilePath', 'WindowsDirPath', 'WindowsFilePath', ]
from pylabs.pmtypes.CustomTypes import Guid, Path, DirPath, FilePath, \
        UnixDirPath, UnixFilePath, WindowsDirPath, WindowsFilePath

__all__ += ['Object', 'Enumeration']
from pylabs.pmtypes.GenericTypes import Object, Enumeration

# Type registration starts here

def register_types():
    '''Register all known types on some container

    @return: Container with all types as attributes
    @rtype: object
    '''

    #All modules we want to load types from
    #This is inline not to clutter package namespace
    from pylabs.pmtypes import PrimitiveTypes, CollectionTypes, CustomTypes
    TYPEMODS = (PrimitiveTypes, CollectionTypes, CustomTypes, )

    class TypeContainer: pass
    base = TypeContainer()

    def _register_types_from_module(mod, base):
        '''Hook all classes found in mod on base

        This is an inner-function so we don't pollute package namespace.

        @param mod: Module containing types to hook
        @type mod: module
        @param base: Hook point for types
        @type base: object

        @raises RuntimeError: Multiple types with the same name are found
        '''
        #Import inspect here so we don't pollute package namespace
        import inspect

        #Go through all names defined in the module (classes, imported modules,
        #functions,...)
        #Using names 'classname' and 'class_', although not all discovered
        #attributes are classes... This will be a first discriminator though
        for class_ in mod.__dict__.itervalues():
            #Check whether it's a class defined in our module (not imported)
            if inspect.isclass(class_) and inspect.getmodule(class_) is mod:
                #Fail on duplicate names
                if hasattr(base, class_.NAME):
                    raise RuntimeError('Type %s is already registred on type base' % class_.NAME)
                #Hook the class
                setattr(base, class_.NAME, class_)

    for mod in TYPEMODS:
        _register_types_from_module(mod, base)


    #This is similar to _register_types_from_module
    def _register_generic_types_from_module(mod, base):
        import inspect
        for function in mod.__dict__.itervalues():
            if inspect.isfunction(function) and inspect.getmodule(function) is mod:
                if hasattr(function, 'qtypename'):
                    if hasattr(base, function.qtypename):
                        raise RuntimeError('Type %s is already registered on type base' % function.qtypename)
                    setattr(base, function.qtypename, function)

    from pylabs.pmtypes import GenericTypes
    GENERICMODS = (GenericTypes, )
    for mod in GENERICMODS:
        _register_generic_types_from_module(mod, base)

    return base
