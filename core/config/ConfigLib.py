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

from pylabs.config import ConfigManagementItem, GroupConfigManagement, SingleConfigManagement

def checkItemClass(itemclass):
    import inspect
    if not inspect.isclass(itemclass):
        raise TypeError("ItemGroupClass argument is not a class")
    if not issubclass(itemclass, ConfigManagementItem):
        raise ValueError("Itemclass [%s] is not a ConfigManagementItem" % itemclass.__name__)
    for attr in "CONFIGTYPE", "DESCRIPTION":
        if not hasattr(itemclass, attr):
            raise ValueError("Itemclass [%s] is invalid: no attribute [%s] found" % (itemclass.__name__, attr))


def ItemGroupClass(itemclass):
    checkItemClass(itemclass)

    class GroupClass(GroupConfigManagement):
        _ITEMCLASS = itemclass
        _CONFIGTYPE = itemclass.CONFIGTYPE
        _DESCRIPTION = itemclass.DESCRIPTION
        if hasattr(itemclass, 'SORT_PARAM'):
            _SORT_PARAM = itemclass.SORT_PARAM
        if hasattr(itemclass, 'KEYS'):
            _KEYS = itemclass.KEYS
        if hasattr(itemclass, 'SORT_METHOD'):
            _SORT_METHOD = itemclass.SORT_METHOD
        
    return GroupClass


def ItemSingleClass(itemclass):
    checkItemClass(itemclass)

    class SingleClass(SingleConfigManagement):
        _ITEMCLASS = itemclass
        _CONFIGTYPE = itemclass.CONFIGTYPE
        _DESCRIPTION = itemclass.DESCRIPTION

    return SingleClass