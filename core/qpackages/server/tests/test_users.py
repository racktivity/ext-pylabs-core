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
from pylabs import pylabsTestCase
from pylabs import q

class Users(pylabsTestCase):
    ''' Test Suite for the Users.py in servers '''

    def init(self):
        from pylabs.qpackages.server.Users import Users
        u = Users()
        u.addUser('test_user', 'test_password')
        u.addUser('test_user1', 'test_password1')

    def test_add_user(self):
        ''' Testing whether we can add users'''
        self.init()
        from pylabs.qpackages.server.Users import Users
        u = Users()
        self.assert_(u)
        u.addUser('test_user2', 'test_password')
        userList = u.list()
        self.assert_('test_user2' in userList)

    def test_exists(self):
        self.init()
        from pylabs.qpackages.server.Users import Users
        u = Users()
        self.assert_(u.exists('test_user'))
        self.assert_(not u.exists('test_shouldnotexist'))

    def test_validate(self):
        self.init()
        from pylabs.qpackages.server.Users import Users
        u = Users()
        self.assert_(u.validate('test_user', 'test_password'))
        self.assert_(not u.validate('test_user', 'testweq_password'))

    def test_delete_user(self):
        self.init()
        from pylabs.qpackages.server.Users import Users
        u = Users()
        u.removeUser('test_user1')
        userList = u.list()
        self.assert_('test_user1' not in userList)