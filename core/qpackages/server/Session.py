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

class Session(BaseType):
    """
    Session object containing all basic data for a client's
    session on the server.
    """

    id             = q.basetype.guid(doc='The session\'s unique identifier.', allow_none=False, default=q.base.idgenerator.generateGUID())
    login          = q.basetype.string(doc='The login which is authenticated for this session.')
    ipAddress      = q.basetype.ipaddress(doc='The client\'s IP address', allow_none=True)
    created        = q.basetype.integer(doc='Epoch on which session was created.', allow_none=False, default=q.base.time.getTimeEpoch())
    updated        = q.basetype.integer(doc='Epoch on which session was last updated.', allow_none=False, default=q.base.time.getTimeEpoch())
    
    def __init__(self):
        self.id = q.base.idgenerator.generateGUID()
        self.created = q.base.time.getTimeEpoch()
        self.updated = q.base.time.getTimeEpoch()
        
    def __str__(self):
        return '%s - %s - %s'%(self.id, self.login, self.ipAddress)
    
    def __repr__(self):
        return str(self)
