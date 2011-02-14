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
 
'''Applicationserver request object interface'''

from twisted.python import components
from twisted.web.http import Request
from zope.interface import Interface, Attribute, implements

class IApplicationserverRequest(Interface):
    '''Request information transfered from a transport to the dispatcher'''
    request_hostname = Attribute('''
        Request hostname
        
        @type: string''')
    client_ip = Attribute('''
        Client IP
        
        @type: string''')

    user_authenticated = Attribute('''
        Denotes whether the request is authenticated
        
        @type: bool''')
    username = Attribute('''
        Authentication username
        
        @type: string''')
    password = Attribute('''
        Authentication password
        
        @type: string''')


class ApplicationserverRequestFromTwistedWebHTTPRequest:
    '''Adapter from twisted.web request objects to L{IApplicationserverRequest}
    
    This adapter can transform a L{twisted.web.http.Request} into an
    L{IApplicationserverRequest}'''
    implements(IApplicationserverRequest)

    def __init__(self, request):
        '''Initialize a new adapter

        @param request: Twisted request to adapt
        @type request: L{twisted.web.http.Request}
        '''
        self._request = request
        self.user_authenticated = False

    @property
    def request_hostname(self):
        '''Request hostname'''
        return self._request.getRequestHostname()

    @property
    def client_ip(self):
        '''Request client IP'''
        return self._request.getClientIP()

    @property
    def username(self):
        '''Request username'''
        return self._request.getUser()

    @property
    def password(self):
        '''Request password'''
        return self._request.getPassword()


#Register our adapter
components.registerAdapter(ApplicationserverRequestFromTwistedWebHTTPRequest,
                           Request, IApplicationserverRequest)