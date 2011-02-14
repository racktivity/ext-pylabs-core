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

'''Mixin and helpers to access 'dirty flagging' information set by pmtypes'''

DIRTY_PROPERTIES_ATTRIBUTE = '_pm__dirty_properties'
DIRTY_AFTER_LAST_SAVE_ATTRIBUTE = '_pm__dirty_after_last_save'

class DirtyFlaggingMixin:
    """
    Mixin class that will add 2 attributes on the a class containing data about changes to the properties
    """
    def _get_dirty_properties(self):
        '''Return all dirty properties in this instance

        @returns: Dirty property names
        @rtype: set
        '''
        dirty = getattr(self, DIRTY_PROPERTIES_ATTRIBUTE, None)
        if dirty is None: #No if not dirty: not set() == True
            dirty = set()
            setattr(self, DIRTY_PROPERTIES_ATTRIBUTE, dirty)
        return dirty

    '''Check whether a given object got dirty properties

    @type: bool'''
    isDirty = property(fget=lambda s: len(s.dirtyProperties) > 0)

    '''Get a set of all dirtied properties

    @type: set'''
    dirtyProperties = property(fget=_get_dirty_properties)

    '''Check whether a given object was dirtied after last save

    @type: bool'''
    isDirtiedAfterSave = property(fget=lambda s: getattr(s, DIRTY_AFTER_LAST_SAVE_ATTRIBUTE, False))

    def reset_dirtied_after_save(self):
        '''Reset dirtied after save state

        Call this from the function which saves to object to CMDB.
        '''
        setattr(self, DIRTY_AFTER_LAST_SAVE_ATTRIBUTE, False)