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

try:
    from twisted.trial import unittest
    from twisted.web import xmlrpc
    from twisted.internet import defer
except ImportError:
    import nose
    raise nose.SkipTest('No Twisted Trial support')

from pylabs.baseclasses.xmlrpc.server import ManagementClassXMLRPCServer
from pylabs.baseclasses.xmlrpc.server import xmlrpc_expose, \
        xmlrpc_require_authentication

TEST_PORT = 8123

class ExportedClass:
    @xmlrpc_expose
    def test_abc(self):
        return 'abc'

    @xmlrpc_expose
    def test_123(self):
        return 123

    @xmlrpc_require_authentication
    @xmlrpc_expose
    def test_auth(self):
        return True

class XMLRPCServerTestCase:
    AUTHENTICATION_HANDLER = None
    def setUp(self):
        server = ManagementClassXMLRPCServer(port=TEST_PORT,
                authentication_handler=self.AUTHENTICATION_HANDLER)
        server.addManager(ExportedClass(), endpoint='test')
        _, self.service = server._register_server()
        self.port = self.service.getHost().port
        self.factories = list()

    def tearDown(self):
        self.factories = list()
        return self.service.stopListening()

    def queryFactory(self, *args, **kwargs):
        factory = xmlrpc._QueryFactory(*args, **kwargs)
        self.factories.append(factory)
        return factory

    def proxy(self, username=None, password=None):
        if username:
            uri = 'http://%s:%s@localhost:%d/' % (username, password,
                    self.port)
        else:
            uri = 'http://localhost:%d/' % self.port

        p = xmlrpc.Proxy(uri)
        p.queryFactory = self.queryFactory

        return p

class TestBasicServer(XMLRPCServerTestCase, unittest.TestCase):
    def test_calls(self):
        tests = (
                    ('test.test_abc', 'abc'),
                    ('test.test_123', 123),
                )
        deferreds = list()

        for method, result in tests:
            deferred = self.proxy().callRemote(method)
            deferred.addCallback(self.assertEquals, result)
            deferreds.append(deferred)

        return defer.DeferredList(deferreds, fireOnOneErrback=True)

class SimpleHandler:
    def check(self, username, password):
        return username == password == 'test'

class TestAuthentication(XMLRPCServerTestCase, unittest.TestCase):
    AUTHENTICATION_HANDLER = SimpleHandler()

    def _run_test(self, username, password, should_fail=False):
        deferred = self.proxy(username, password).callRemote('test.test_auth')
        deferred.addCallback(lambda v: self.assert_(not should_fail))
        deferred.addErrback(lambda v: self.assertEqual(
            str(v.getErrorMessage()), '(\'401\', \'Unauthorized\')'))
        return deferred

    def test_auth_required(self):
        return self._run_test(None, None, True)

    def test_wrong_credentials(self):
        return self._run_test('test', 'wrong', True)

    def test_success(self):
        return self._run_test('test', 'test', False)