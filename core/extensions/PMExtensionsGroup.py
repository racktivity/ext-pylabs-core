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

import os
import imp

import pymonkey
import pymonkey.extensions.PMExtensions
from pymonkey.extensions.PMExtension import BasePMExtension

class _ModulePlaceholder: pass
ModulePlaceholder = _ModulePlaceholder

class PMExtensionsGroup(object):
    """
    Dummy class to hold extension instances
    is middle class e.g. if q.servers.rsyncserver and servers does not exist
    """
    def __init_properties__(self):    
        self.pm_pmExtensions=None    #link to parent pm_pmExtensions object
        self.pm_parentPMExtensionsGroup=None   #group can be part of other group, in that case pm_pmExtensions=None
        self.pm_extensionsRootPath="" #rootdir of extensions
        self.pm_groupPMExtensions={}
        
    def __init__(self,pm_pmExtensionsOrPMExtensionsGroup=None):
        self.__init_properties__()
        if isinstance(pm_pmExtensionsOrPMExtensionsGroup, pymonkey.extensions.PMExtensions.PMExtensions):
            self.pm_pmExtensions=pm_pmExtensionsOrPMExtensionsGroup
        if isinstance(pm_pmExtensionsOrPMExtensionsGroup,PMExtensionsGroup):
            self.pm_parentPMExtensionsGroup=pm_pmExtensionsOrPMExtensionsGroup

    def __getattribute__(self, name):
        """
        overloaded method from python itself, getattribute gets called when anyone asks for an attribute
        """
        #call getattribute from python, goal get to your _exts without getting in loop (otherwise this method would be called again)
        if name in ('__init_properties__', 'pm_groupPMExtensions', 'addExtension'):
            return object.__getattribute__(self, name)

        try:
            tmp = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if tmp is not ModulePlaceholder:
                return tmp

        _extensions = object.__getattribute__(self, 'pm_groupPMExtensions')

        #check if attribute (which would be extension of PMExtensionsGroup) exists, if not should not return method or attribute
        if name not in _extensions:
            raise AttributeError("cannot get method or attribute which is not an extension from a extension group object")

        extension = _extensions[name]
        #we can now load the extension because someone asked for it
        extension.activate()            
        return extension.instance

    def pm_addExtension(self, extension):
        '''
        Register an extension as child attribute of this object
        '''
        if isinstance(extension, BasePMExtension)==False:
            raise TypeError("Parameter = BasePMExtension to addExtension")
        self.pm_groupPMExtensions[extension.pmExtensionName] = extension
        setattr(self, extension.pmExtensionName, ModulePlaceholder)