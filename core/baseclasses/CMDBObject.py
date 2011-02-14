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

import pymonkey

from pymonkey.cmdb import cmdb
from pymonkey.baseclasses.BaseCMDBObject import BaseCMDBObject
from pymonkey.pmtypes.PrimitiveTypes import String, Integer, Boolean
from pymonkey.pmtypes.CustomTypes import Guid

class CMDBObject(BaseCMDBObject):
    """
    Base class for all CMDB classes which are registered directly in the CMDB
    
    CMDB objects represent data and contain logic to manipulate data structures.
    CMDB objects do not contain any management logic and never perform operations on the system
    
    Serialization and deserialization of objects is done using the q.cmdb namespace.
    """
 
    cmdbtypename = String(doc = 'identifies uniquely the CMDB entry')
    cmdbid       = Integer(doc = 'Unique id for the cmdb object')
    cmdbguid     = Guid(doc = 'Unique guid for the cmdb object')    
    cmdbinsync   = Boolean(doc = 'Flag that indicates if the system is in sync with CMDB', default = True)

    def __init__(self):
        """
        Initialize CMDB Object
        """
        
        BaseCMDBObject.__init__(self)

        # Initialize properties if not already initialized
        if self.cmdbid is None:
            self.cmdbid=pymonkey.q.base.idgenerator.generateRandomInt(1,10000000)        
            self.cmdbguid=pymonkey.q.base.idgenerator.generateGUID()
        
       
    
    def __new__(cls):
        """
        The CMDB can only contain 1 instance per CMDBObject derived type.
        
        Retrieve object from cmdb if available, otherwise, register new object
        in cmdb.
        """
        
        pymonkey.q.logger.log('Checking if we already have an instance for class %s' % cls.__name__, 5)
        
        #pymonkey.q.logger.log('_instance is %s' % str(hasattr(cls, '_instance')), 5)
        
        if hasattr(cls, '_instance'):
            pymonkey.q.logger.log('returning existing instance', 5)
            return cls._instance
        
        o = None
        
        pymonkey.q.logger.log('Checking if we already have a saved %s object in the cmdb' % cls.cmdbtypename, 5)
        if pymonkey.q.cmdb.existsObject(cls.cmdbtypename):
            pymonkey.q.logger.log('object found, retrieving it from the cmdb', 5)
            o = pymonkey.q.cmdb.getObject(cls.cmdbtypename)
        
        if o == None:
            o = BaseCMDBObject.__new__(cls)
            
        cls._instance = o
        
        return cls._instance
    
        
   
    
    def save(self):
        """
        Save configuration to the database
        """
                              
        pymonkey.q.cmdb.saveObject(self.cmdbtypename, self)
        
 
    def __str__(self):
        # @TODO: implement nicely
        #raise NotImplementedError("%s.__str__()" % self.__class__.__name__)
        return self.__class__.__name__

    def __repr__(self):
        return str(self)