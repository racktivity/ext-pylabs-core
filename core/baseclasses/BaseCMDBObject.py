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

import pymonkey

from pymonkey.baseclasses.BaseType import BaseType
from pymonkey.pmtypes.PrimitiveTypes import String, Integer, Boolean
from pymonkey.baseclasses.dirtyflaggingmixin import DirtyFlaggingMixin

class BaseCMDBObject(BaseType, DirtyFlaggingMixin):
    """
    Base for all types of CMDB objects.
    
    This class contains basic properties which are available on all CMDB objects.
    A BaseCMDBObject is an abstract class which should only be used to create new types
    of CMDB objects.
    """
    
    def __init__(self):
        
        # call parent
        BaseType.__init__(self)
       
        # Initialize fake data if requested        
        if pymonkey.q.vars.getVar('fakeData') or 'fakeData' in os.environ.keys() :
            pymonkey.q.logger.log('fakeData variable set - loading fake data', 5)
            self.__fake_data__()
    
    #rootcmdbtypename = ""  ##string, name like q.servers.apache , identifies uniquely the CMDB entry of the root object (CMDBObject)
    #creationdate = 0       
    #changed=False                ##boolean   #when object or subobject was changed this property will be set on True, allows mgmt class to re-configure application
    #changedtime=0                ##epoch #time change happened
    
    # @TODO: how can we integrate DirtyFlaggingMixin into this object 
    # @TODO: create timestamp/epoch pmtypes 
    timestampcreated = Integer(doc = 'Epoch time when this object was created')
    timestampmodified = Integer(doc = 'Epoch time when this object was last modified')
    
    def __fake_data__(self):
        pass