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

'''Implementation of generic object/method exposal through XML-RPC

Classes and functions in this module allow you to expose a custom class
instance and its methods through an XMLRPC service easily. It allows you to
expose several classes in one server instance.

Here's a sample service:

>>> from pymonkey.baseclasses.xmlrpc.server import ManagementClassXMLRPCServer
>>> from pymonkey.baseclasses.xmlrpc.server import xmlrpc_expose, xmlrpc_require_authentication
>>>
>>> class AuthHandler:
...     def check(self, username, password):
...         if username == 'user' and password == 'pass':
...             return True
...         return False
...
>>> class ServiceOne:
...     @xmlrpc_expose
...     def sum(self, a, b):
...         return a + b
...
>>> class ServiceTwo:
...     @xmlrpc_require_authentication
...     @xmlrpc_expose
...     def get_secret(self):
...         return self._generate_secret()
...
...     def _generate_secret(self):
...         return 'secret'
...
>>> def main():
...     ah = AuthHandler()
...     server = ManagementClassXMLRPCServer(port=8000, authentication_handler=ah)
...     s1 = ServiceOne()
...     s2 = ServiceTwo()
...     server.addManager(s1, 'one')
...     server.addManager(s2, 'two')
...     server.run()
...
>>> if __name__ == '__main__':
...     main()

Once this service is running, you can access it using any XMLRPC client. See
L{pymonkey.baseclasses.xmlrpc.client} for a more user-friendly approach.

Here's a sample using plain xmlrpclib:

>>> import xmlrpclib
>>> client = xmlrpclib.Server('http://localhost:8000')
>>> client.one.sum(1, 2)
3
>>> client.two.get_secret()

*** Error: <ProtocolError for localhost:8000/RPC2: 401 Unauthorized> (type ProtocolError)

>>> client = xmlrpclib.Server('http://user:wrongpass@localhost:8000')
>>> client.two.get_secret()

*** Error: <ProtocolError for user:wrongpass@localhost:8000/RPC2: 401 Unauthorized> (type ProtocolError)

>>> client = xmlrpclib.Server('http://user:pass@localhost:8000')
>>> client.two.get_secret()
'secret'

@todo Document xmlrpc_request functionality
'''
import new
import inspect
import xmlrpclib

from twisted.internet import reactor
from twisted.web import xmlrpc, server
from twisted.python import log

import pymonkey

#TODO Introspection
#TODO Document xmlrpc_request functionality

XMLRPC_EXPOSE = 'XMLRPC_EXPOSE'
XMLRPC_REQUIRE_AUTHENTICATION = 'XMLRPC_REQUIRE_AUTHENTICATION'
XMLRPC_REQUEST_ARG = 'xmlrpc_request'

FAILURE_PICKLE_DELIMITER = '||FAILURE_PICKLE_DELIMITER||'

def xmlrpc_expose(func):
    '''Decorator to mark a method to be exposed through XMLRPC'''
    setattr(func, XMLRPC_EXPOSE, True)
    return func

def xmlrpc_require_authentication(func):
    '''Decorator to mark methods exposed through XMLRPC who require
    authenticated calls'''
    setattr(func, XMLRPC_REQUIRE_AUTHENTICATION, True)
    return func

def ebRender(self, failure):
    '''Custom error render method (used by our XMLRPC objects)'''
    if isinstance(failure.value, xmlrpclib.Fault):
        return failure.value

    log.err(failure)

    if hasattr(failure, 'getErrorMessage'):
        value = failure.getErrorMessage()
    else:
        value = 'error'

    try:
        import cPickle as pickle
    except ImportError:
        try:
            import pickle
        except ImportError:
            pass

    try:
        pickle
    except NameError:
        pass
    else:
        value = '%s%s%s' % (value, FAILURE_PICKLE_DELIMITER,
                pickle.dumps(failure))

    return xmlrpclib.Fault(self.FAILURE, value)

def generate_wrapped_method(method, method_name):
    '''Create a wrapped clone of an original class method to be used as XMLRPC
    callback'''
    def wrapped(self, *args, **kwargs):
        return method(*args, **kwargs)

    wrapped.__doc__ = method.__doc__
    wrapped.__name__ = 'xmlrpc_%s' % method_name
    wrapped.help = wrapped.__doc__

    argspec = inspect.getargspec(method)
    if XMLRPC_REQUEST_ARG in argspec[0]:
        setattr(wrapped, XMLRPC_REQUEST_ARG, True)

    return wrapped

def generate_manager_server(manager):
    '''Generate a wrapping XMLRPC server class for a given type'''
    class ManagerXMLRPCServer(xmlrpc.XMLRPC):
        _ebRender = ebRender

    ManagerXMLRPCServer.__name__ = '%sXMLRPCServer' % \
            manager.__class__.__name__
    ManagerXMLRPCServer.__doc__ = 'XMLRPC Server wrapper for %s' % \
            manager.__class__.__name__

    manager_server = ManagerXMLRPCServer()
    
    #Now add instancemethods for all exposed methods
    for attrname in dir(manager):
        attr = getattr(manager, attrname)
        if getattr(attr, XMLRPC_EXPOSE, False):
            wrapped = generate_wrapped_method(attr, attrname)

            if getattr(attr, XMLRPC_REQUIRE_AUTHENTICATION, False):
                setattr(wrapped, XMLRPC_REQUIRE_AUTHENTICATION, True)

            wrapped_name = wrapped.__name__
            wrapped = new.instancemethod(wrapped, manager_server, manager_server.__class__)

            setattr(manager_server, wrapped_name, wrapped)

    xmlrpc.addIntrospection(manager_server)

    return manager_server


class AuthenticationRequired(Exception):
    '''Exception raised when a request without authentication is performed to
    a method requiring authentication'''
    pass

class AuthenticationFailed(Exception):
    '''Exception raised when a request with invalid authentication is
    performed to a method requiring authentication'''
    pass


class Request(object):
    '''Read-only wrapper around a twisted.web.server.Request object

    Instances of this class are passed as request parameter to XMLRPC methods
    accepting a request argument (see L{xmlrpc_expose}).
    '''
    def __init__(self, twisted_request):
        '''Generate a new wrapper

        @param twisted_request: Request object to wrap
        @type twisted_request: twisted.web.server.Request
        '''
        self._twisted_request = twisted_request

    headers = property(fget=lambda s: s._twisted_request.getAllHeaders())
    request_hostname = property(fget=lambda s: \
            s._twisted_request.getRequestHostname())
    request_host = property(fget=lambda s: s._twisted_request.getHost())
    client_ip = property(fget=lambda s: s._twisted_request.getClientIP())
    secure = property(fget=lambda s: s._twisted_request.isSecure())
    user = property(fget=lambda s: s._twisted_request.getUser())
    password = property(fget=lambda s: s._twisted_request.getPassword())

    def __str__(self):
        return 'Request from %s' % self.client_ip


#This is from twisted.web.xmlrpc
from twisted.web import resource, http
from twisted.internet import defer
Fault = xmlrpclib.Fault

class RootServer(xmlrpc.XMLRPC):
    '''Root XMLRPC server object used to host any exposed managers

    A RootServer instance is used as the exposed object on the root of the
    object tree of the XMLRPC server, ie calls without any namespacing would
    be handled by this object.'''

    #Use our custom error renderer
    _ebRender = ebRender

    def __init__(self, allowNone=False, authenticationHandler=None):
        '''Initialize a new root server

        The authenticationHandler is used to validate authentication data
        provided with calls requiring authentication (see
        L{xmlrpc_authentication_required}). It should implement one method,
        'check', which takes 2 arguments: username and password. The check
        method should return a boolean denoting credential validity.

        @param allowNone: See L{twisted.web.xmlrpc.XMLRPC.__init__}
        @type allowNone: bool
        @param authenticationHandler: Object providing an authentication check method
        @type authenticationHandler: object
        '''
        xmlrpc.XMLRPC.__init__(self, allowNone)
        self.authenticationHandler = authenticationHandler

    def _check_authentication(self, request):
        '''Validate provided authentication data in request'''
        user = request.getUser()
        password = request.getPassword()

        if not user or not password:
            raise AuthenticationRequired

        if not self.authenticationHandler:
            msg = 'XMLRPC method requires athentication, but no authentication handler registered'
            pymonkey.q.logger.log(msg)
            raise RuntimeError(msg)

        if not self.authenticationHandler.check(user, password):
            raise AuthenticationFailed

    def render(self, request):
        #Need this trick to overcome some API changes between
        #Twisted.web 8.0.0 and prior versions
        if not hasattr(xmlrpc.XMLRPC, 'render_POST') and \
                request.method == 'POST':
            return self.render_POST(request)
        else:
            return xmlrpc.XMLRPC.render(self, request)

    def render_POST(self, request):
        #This is based on twisted.web.xmlrpc.XMLRPC.render_POST of
        #twisted.web 8.0.0
        request.content.seek(0, 0)
        request.setHeader("content-type", "text/xml")
        try:
            args, functionPath = xmlrpclib.loads(request.content.read())
        except Exception, e:
            f = Fault(self.FAILURE, "Can't deserialize input: %s" % (e,))
            self._cbRender(f, request)
        else:
            try:
                function = self._getFunction(functionPath)
            except Fault, f:
                self._cbRender(f, request)
            else:
                #MOD START
                if getattr(function, XMLRPC_REQUIRE_AUTHENTICATION, False):
                    try:
                        self._check_authentication(request)
                    except AuthenticationRequired:
                        request.setResponseCode(http.UNAUTHORIZED)
                        return 'Authorisation required'
                    except AuthenticationFailed:
                        request.setResponseCode(http.UNAUTHORIZED)
                        return 'Unauthorized'

                kwargs = dict()
                if getattr(function, XMLRPC_REQUEST_ARG, False):
                    kwargs[XMLRPC_REQUEST_ARG] = Request(request)

                defer.maybeDeferred(function, *args, **kwargs).addErrback(
                #MOD END
                    self._ebRender
                ).addCallback(
                    self._cbRender, request
                )
        return server.NOT_DONE_YET


class ManagementClassXMLRPCServer(object):
    '''Server object to expose one or more service objects over XMLRPC

    See the module documentation of L{pymonkey.baseclasses.xmlrpc.server} for
    an extensive example.
    '''
    def __init__(self, port=8000, authentication_handler=None, interface=''):
        '''Initialize a new ManagementClassXMLRPCServer

        @param port: Port to run the server on
        @type port: number
        @param authentication_handler: Authentication handler to use, see L{RootServer.__init__}
        @type authentication_handler: instance
        @param interface: Interface (hostname/IP address) to listen on. Empty string is all addresses.
        @type interface: string
        '''
        self._port = port
        self._managers = dict()
        self._authentication_handler = authentication_handler
        self._interface = interface

    def _register_server(self):
        '''Register the server on the Twisted reactor

        This method is split-up for unit testing sake.
        '''
        root_server = RootServer(
                authenticationHandler=self._authentication_handler)
        xmlrpc.addIntrospection(root_server)

        #Create all endpoints
        for endpoint, manager_server in self._managers.itervalues():
            root_server.putSubHandler(endpoint, manager_server)
            
        #Run reactor
        port = reactor.listenTCP(self._port, server.Site(root_server),
                interface=self._interface)
        return self._interface, port

    def run(self):
        '''Run the server

        This method does not return unless the Twisted reactor is stopped.
        '''
        self._register_server()
        reactor.run()
    
    def addManager(self, manager, endpoint):
        '''Add a manager instance to the server

        Any exposed method on the manager added at endpoint marked with
        xmlrpc_expose will be available as C{endpoint.methodname} on the
        XMLRPC server. See the module documentation of
        L{pymonkey.baseclasses.xmlrpc.server} for an extensive example.
        '''
        manager_server = generate_manager_server(manager)
        self._managers[manager] = (endpoint, manager_server)