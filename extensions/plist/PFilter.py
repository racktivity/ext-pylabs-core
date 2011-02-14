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
from pymonkey.Shell import *

class PFilter(pymonkey.baseclasses.BaseType):
    """
    Defines a set of rules used by PFind to create a PList
    Only PFiles matching the criteria will be added to the PList  
  
    @TODO: Can a PFilter be used to filter an existing PList? -> yes
    """    
    #rootPath                        = q.basetype.dirpath(doc = 'Base path for the pfiles in this plist. The pfile\'s paths in the plist will be relative to this path', allow_none = True, default = None)
    
    #?#fieldsToCapture                 = q.basetype.list(doc = 'List of PFileFields to capture for each file. The fields will also be save in this order')
    #?#fieldsSortOrder                 = q.basetype.list(doc = 'List of PFileFields to determine sort order. None for no sorting (default)')
    
    includePathRegex                = q.basetype.string(doc = 'Regular expression to which directory paths should match to be inluded in the list', allow_none = True, default = None)
    includeMaxFileSize              = q.basetype.integer(doc = 'Maximum file size to be inluded in the list', allow_none = True, default = None)
    includeFromModificationDate     = q.basetype.integer(doc = '', allow_none = True, default = None)
    includeToModificationDate       = q.basetype.integer(doc = '', allow_none = True, default = None)
    includeFromCreationDate         = q.basetype.integer(doc = '', allow_none = True, default = None)
    includeToCreationDate           = q.basetype.integer(doc = '', allow_none = True, default = None)
    
    excludePathRegex                = q.basetype.string(doc = 'Regular expression to which directory paths should match to be explicitly exclude from the list', allow_none = True, default = None)
    excludeMaxFileSize              = q.basetype.integer(doc = 'Maximum file size to be inluded in the list', allow_none = True, default = None)
    excludeFromModificationDate     = q.basetype.integer(doc = '', allow_none = True, default = None)
    excludeToModificationDate       = q.basetype.integer(doc = '', allow_none = True, default = None)
    excludeFromCreationDate         = q.basetype.integer(doc = '', allow_none = True, default = None)
    excludeToCreationDate           = q.basetype.integer(doc = '', allow_none = True, default = None)
    
    def validate(self, pfile):
        """
        Validates if the given path is valid for this filter
        
        @param path: PFile instance to check
        @return:     Boolean indicating if the pfile is valid for this filter
        """
        
        return True