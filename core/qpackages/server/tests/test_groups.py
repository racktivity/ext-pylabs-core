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
from pymonkey import PymonkeyTestCase
from pymonkey import q

class TestGroups(PymonkeyTestCase):
    ''' Test Suite for the Groups.py in servers '''

    def init(self):
        from pymonkey.qpackages.server.Groups import Groups
        from pymonkey.qpackages.server.Users import Users
        u = Users()
        u.addUser('test_user', 'test_password')
        u.addUser('test_user1', 'test_password1')
        u.addUser('test_user2', 'test_password2')
        u.addUser('test_user3', 'test_password3')
        g = Groups()
        g.addGroup('test_group')
        g.addGroup('test_group1')
        g.addGroup('test_group2')
        g.addUserToGroup('test_group1', 'test_user')
        g.addUserToGroup('test_group1', 'test_user1')
        g.addUserToGroup('test_group1', 'test_user2')
        g.addUserToGroup('test_group2', 'test_user')
        g.addUserToGroup('test_group2', 'test_user2')
        g.addUserToGroup('test_group2', 'test_user3')

    def test_add_group(self):
        ''' Testing whether we can add groups'''
        self.init()
        from pymonkey.qpackages.server.Groups import Groups
        g = Groups()
        self.assert_(g)
        g.addGroup('test_group5')
        self.assert_('test_group5' in g.list())

    def test_remove_group(self):
        ''' Testing whether we can remove a group '''
        self.init()
        from pymonkey.qpackages.server.Groups import Groups
        g = Groups()
        self.assertRaises(RuntimeError, g.removeGroup, 'bleh')
        g.removeGroup('test_group2')
        self.assert_( not 'test_group2:' in g.list())

    def test_exists(self):
        self.init()
        from pymonkey.qpackages.server.Groups import Groups
        g = Groups()
        self.assert_(g.exists('test_group'))
        self.assert_(not g.exists('test_shouldnotexist'))

    def test_add_user_to_group(self):
        self.init()
        from pymonkey.qpackages.server.Groups import Groups
        g = Groups()
        g.addUserToGroup('test_group1', 'test_user3')
        self.assert_(g.checkUserInGroup('test_group1', 'test_user3'))
        self.assertRaises(RuntimeError,g.addUserToGroup, 'test_group1', 'test_user')

    def test_delete_user_from_group(self):
        self.init()
        from pymonkey.qpackages.server.Groups import Groups
        g = Groups()
        g.removeUserFromGroup('test_group1', 'test_user1')
        self.assert_(not g.checkUserInGroup('test_group1', 'test_user1'))

    def test_listUsersInGroup(self):
        self.init()
        from pymonkey.qpackages.server.Groups import Groups
        g = Groups()
        uList = g.listUsersInGroup('test_group1')
        self.assertEquals(set(uList), set(('test_user', 'test_user1', 'test_user2',)))