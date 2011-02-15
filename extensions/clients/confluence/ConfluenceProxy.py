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

from pylabs import q

from Confluence import Confluence
from ConfluenceImpl import ConfluenceImpl
from UserManager import UserManager
from SpaceManager import SpaceManager
import model.ConfluenceEnums
import Utils

class ConfluenceProxy(Confluence):
    """Represent a not connected state of Confluence showing only method 'connect', since all other methods require a connection"""

    def __init__(self):
        self._impl = None
        self._serverAddress = None
        self._login = None

    def connect(self, serverUrl, login, password):
        """Connect to confluence server
        for example, connect('http://172.17.1.26', 'testAccount', 'testPassword'), or
        connect('172.17.1.26', 'testAccount', 'testPassword')
        @param serverUrl: confluence server url starting with 'http://<domain name, or ip address>', or ip address
        @param login: user login
        @param password: user password"""
        if self._impl:
            raise ValueError('Already connected to %(host)s as %(user)s'%{'host': self._serverAddress, 'user': self._login})

        if not serverUrl.startswith('http://'):
            serverUrl = 'http://' + serverUrl

        try:
            _confluence = ConfluenceImpl(serverUrl, login, password)
            userManager = UserManager(q.logger)
            spaceManager = SpaceManager(q.logger)

            _confluence.pm_setProxy(self)
            _confluence.pm_setUserManager(userManager)
            _confluence.pm_setSpaceManager(spaceManager)

            self._impl = _confluence #set the reference of the concrete implementation to the newly created object

            #keep server url and login for use by status messages
            self._serverAddress = serverUrl
            self._login = login

        except Exception, ex:
            q.logger.log(str(ex), 3)
            raise ValueError( 'Not able to connect to server %(serverUrl)s with user %(login)s, Reason %(errorMessage)s'%{'serverUrl' : serverUrl, 'login' : login, 'errorMessage' : Utils.extractDetails(ex)})