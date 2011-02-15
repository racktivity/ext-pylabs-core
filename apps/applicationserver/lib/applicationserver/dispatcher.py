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

'''Service/method dispatching implementation'''

import inspect
import functools
import types

from pydispatch import dispatcher as pydispatcher

from twisted.internet import threads
from twisted.internet.defer import maybeDeferred
from twisted.python import log
from twisted.internet import reactor

from applicationserver.iapplicationserverrequest import \
        IApplicationserverRequest
from applicationserver.humanreadable import HumanReadable
from applicationserver.utils import attrchecker, service_method_caller
from applicationserver import signals

CHECK_AUTHENTICATION_METHOD = 'checkAuthentication'
CHECK_AUTHORIZATION_METHOD = 'checkAuthorization'
APPLICATIONSERVER_REQUEST_ARG = 'applicationserver_request'
APPLICATIONSERVER_HUMAN_READABLE_ARG = 'humanReadableResponse'

from pylabs import q

#TODO Find a better base exception type
#TODO Difference between authentication required and authentication failed
class AuthenticationError(RuntimeError):
    ERRNO = 9000
    MESSAGE = 'Authentication required'

    applicationserver_errno = ERRNO


class AuthorizationError(RuntimeError):
    ERRNO = 9001
    MESSAGE = 'Authorization Failed'

    applicationserver_errno = ERRNO

class NoSuchService(Exception):
    '''No such service exposed by the server'''
    ERRNO = 8000
    MESSAGE = 'Service not found'

    applicationserver_errno = ERRNO

class NoSuchMethod(Exception):
    '''No such method exposed by the server'''
    ERRNO = 8001
    MESSAGE = 'Method not found'

    applicationserver_errno = ERRNO


class Dispatcher:
    '''Service/method dispatcher'''

    def __init__(self):
        '''Initialize a new dispatcher'''
        # This will store all services we should host, using the service name
        # as mapping key to retrieve the service, and the service itself
        # as mapping key to retrieve the name
        log.msg('[DISPATCHER] Initializing')
        self.services = dict()
        
        ## Hack
        ## Prevent the application server to hang when 10  (default threadpoolsize) concurrent requests are being processed
        reactor.suggestThreadPoolSize(1000)
        ## REMOVE ME WHEN FIXED

    def addService(self, name, service):
        '''Register a service on the dispatcher

        @param name: Service name
        @type name: string
        @param service: Service object to expose
        @type service: object

        @raise RuntimeError: Duplicate service names
        '''
        if name in self.services:
            raise RuntimeError('Duplicate service name %s' % name)

        log.msg('[DISPATCHER] Adding service %s' % name)
        # Add the service to our container, using name and reference as key
        self.services[name] = service
        self.services[service] = name

    def removeService(self, name, service):
        '''Remove a service from the dispatcher

        @param name: Service name
        @type name: string
        @param service: Service object to expose
        @type service: object
        '''
        log.msg('[DISPATCHER] Removing service %s' % name)
        # Remove the service from our internal dict
        self.services.pop(name)
        self.services.pop(service)

    def callServiceMethod(self, request, service_name, method, *args,
            **kwargs):
        '''Call a method on service exposed by this dispatcher

        This should be used by C{transports} which get a reference to a
        dispatcher to call methods when requested to through their own channel.

        This method returns a deferred on which the transport should at least
        register a callback (and most likely also an errback) so returned data
        can be send to the client.

        Args and kwargs are relayed to the method callable.

        @return: Deferred to called method
        @rtype: L{twisted.internet.defer.Deferred}

        @param request: Original request
        @type request: IApplicationserverRequest
        @param service_name: Name of called service
        @type service_name: string
        @param method: Name of called method on the service
        @type method: string

        @raise NoSuchService: Service unknown
        @raise NoSuchMethod: Method unknown
        '''
        #log.msg('[DISPATCHER] Calling method %s on service %s' % \
        #        (method, service_name))
        
        # Cast request to an IApplicationserverRequest
        request = IApplicationserverRequest(request)

        #Fetch the actual service and method callable
        service, func = self.getServiceMethod(service_name, method)

        #Check authentication
        if exposed_authenticated(func):
            #log.msg('[DISPATCHER] Checking authentication')
            if not self.checkAuthentication(service, request, method, args,
                                            kwargs):
                raise AuthenticationError('Authentication failed')
            request.user_authenticated = True
        else:
            pass

        #Check authorization
        if exposed_authorized(func):
            #log.msg('[DISPATCHER] Checking authorization')
            if hasattr(func,'auth_categories'):
                auth_categories = getattr(func,'auth_categories')
            else:
                auth_categories = {}

            if not self.checkAuthorization(auth_categories,service,request,method,args,kwargs):
                raise AuthorizationError('Authorization failed')
        else:
            pass

        #Provide the original request as a parameter, if requested
        if want_request(func):
            kwargs[APPLICATIONSERVER_REQUEST_ARG] = request

        applicationserver_human_readable = \
                kwargs.pop('__applicationserver_human_readable', False)
        if want_human_readable(func):
            kwargs[APPLICATIONSERVER_HUMAN_READABLE_ARG] = \
                    applicationserver_human_readable
        returns_human_readable = bool(want_human_readable(func) and \
                                      applicationserver_human_readable)

        #Decorate the original func so log stuff can be set up correctly
        func = service_method_caller(service_name, func)

        if not want_not_threaded(func):
            #log.msg('[DISPATCHER] Running service method %s:%s in thread' % \
            #        (service_name, method))
            
            defer = threads.deferToThread(func, *args, **kwargs)
        else:
            # The service should not run in a thread
            #log.msg('[DISPATCHER] Running service method %s:%s in reactor' % \
            #        (service_name, method))
            
            defer = maybeDeferred(func, *args, **kwargs)

        def errback(failure):
            dispatchkwargs = {
                    'request': request,
                    'service': service_name,
                    'method': method,
                    'args': args,
                    'kwargs': kwargs,
                    'failure': failure,
            }

            log.err('[DISPATCHER] Service method call %s:%s failed: %s' % \
                    (service_name, method, failure))

            pydispatcher.send(signal=signals.SERVICE_METHOD_EXCEPTION,
                    sender=self, **dispatchkwargs)
            return failure

        if returns_human_readable:
            defer.addCallback(self.tupleToHumanReadable)
        defer.addErrback(errback)

        return defer

    def getServiceMethod(self, service_name, method):
        '''Resolve a function given a service and method name

        @param service_name: Name of the service to resolve
        @type service_name: string
        @param method: Name of method to retrieve
        @type method: string

        @return: Service and method to call
        @rtype: tuple(object, callable)

        @raise NoSuchService: Unknown service name
        @raise NoSuchMethod: Unknown method name or method not exposed
        '''
        #log.msg('[DISPATCHER] Looking up method %s on service %s' % \
        #        (method, service_name))

        try:
            service = self.services[service_name]
        except KeyError:
            raise NoSuchService(
                'No service called \'%s\' registered on this server' % \
                    service_name)

        try:
            func = getattr(service, method)
        except AttributeError:
            raise NoSuchMethod('Service %s exposes no method \'%s\'' % \
                    (service_name, method))

        if not exposed(func):
            raise NoSuchMethod('Method %s on %s is not exposed' % (method,
                service_name))

        return service, func

    def checkAuthentication(self, service, request, methodname, args, kwargs):
        '''Check authentication for a given service

        @param service: Service instance to check authentication for
        @type service: object
        @param request: Client request
        @type request: IApplicationserverRequest
        @param methodname: Name of the method being called
        @type methodname: string
        @param args: Arguments passed in request
        @type args: iterable
        @param kwargs: Keyword arguments passed in request
        @type kwargs: dict

        @return: Authentication success
        @rtype: bool

        @raise RuntimeError: Service got no L{CHECK_AUTHENTICATION_METHOD}
        '''
        if request.username is None or request.password is None:
            return False
        checker = getattr(service, CHECK_AUTHENTICATION_METHOD, None)
        if not checker:
            raise RuntimeError('Service %s got no %s method' % \
                    (service,CHECK_AUTHENTICATION_METHOD) )

        # Figure out whether the checkAuthentication method wants access to the
        # full request object.
        # If it takes 2 arguments, we pass username and password, which is the
        # original behavior
        # If it takes 4 arguments, we pass the request object, method name,
        # and args and kwargs provided during the method call
        checker_args, _, _, _ = inspect.getargspec(checker)
        if type(checker) is types.FunctionType:
            # It's a function (staticmethod), we want to count all args
            pass
        elif type(checker) is types.MethodType:
            # It's a method (or classmethod), we want to skip self/cls
            checker_args = checker_args[1:]
        else:
            raise TypeError('checkAuthentication is neither a function '
                            'or a method')

        if len(checker_args) == 2:
            # checkAuthentication(self, username, password)
            return checker(request.username, request.password)
        elif len(checker_args) == 4:
            # checkAuthentication(self, request, methodname, args, kwargs)
            return checker(request, methodname, args, kwargs)
        else:
            raise ValueError('checkAuthentication should take two or three '
                             'arguments')


    def checkAuthorization(self, auth_categories, service, request, methodname, args, kwargs):
        '''Check authorization for a given service

        @param auth_categories: Parameters; they are the keyword parameters to the decorator expose_authorized
        @type auth_categories: dict
        @param service: Service instance to check authentication for
        @type service: object
        @param request: Client request
        @type request: IApplicationserverRequest
        @param methodname: Name of the method being called
        @type methodname: string
        @param args: Arguments passed in request
        @type args: iterable
        @param kwargs: Keyword arguments passed in request
        @type kwargs: dict

        @return: Authorization success
        @rtype: bool

        @raise RuntimeError: Service got no L{CHECK_AUTHORIZATION_METHOD}

        '''
        checker = getattr(service, CHECK_AUTHORIZATION_METHOD, None)
        if not checker:
            raise RuntimeError('Service %s got no %s method' % \
                    (service,CHECK_AUTHORIZATION_METHOD) )

        # Figure out whether the checkAuthorization method wants access to the
        # full request object.
        # If it takes 2 arguments, we pass username and password, which is the
        # original behavior
        # If it takes 4 arguments, we pass the request object, method name,
        # and args and kwargs provided during the method call
        checker_args, _, _, _ = inspect.getargspec(checker)
        if type(checker) is types.FunctionType:
            # It's a function (staticmethod), we want to count all args
            pass
        elif type(checker) is types.MethodType:
            # It's a method (or classmethod), we want to skip self/cls
            checker_args = checker_args[1:]
        else:
            raise TypeError('%s is neither a function or a method' %(CHECK_AUTHORIZATION_METHOD,))

        if len(checker_args) == 2:
            return checker(auth_categories,request.username)
        else :
            return checker(auth_categories, request, methodname, args, kwargs)


    def tupleToHumanReadable(self, t):
        if isinstance(t, tuple) and len(t) == 2:
            # This should be human readable...
            return HumanReadable(*t)
        return t


'''Attribute set on exposed methods'''
EXPOSE_ATTRIBUTE = 'APPLICATIONSERVER_EXPOSE'
'''kwarg provided to methods containing the service name'''
EXPOSED_SERVICE_NAME_KWARG = '__pm_exposed_service_name'
'''Attribute set if the method wants a request parameter'''
APPLICATIONSERVER_REQUEST_ATTRIBUTE = 'APPLICATIONSERVER_WANT_REQUEST'
APPLICATIONSERVER_HUMAN_READABLE_ATTRIBUTE = \
        'APPLICATIONSERVER_WANT_HUMAN_READABLE'
APPLICATIONSERVER_NOT_THREADED_ATTRIBUTE = 'APPLICATIONSERVER_NOT_THREADED'

def tag_exposed(func):
    '''Tag a method as exposed'''
    setattr(func, EXPOSE_ATTRIBUTE, True)

    args, _, _, _ = inspect.getargspec(func)
    if APPLICATIONSERVER_REQUEST_ARG in args:
        setattr(func, APPLICATIONSERVER_REQUEST_ATTRIBUTE, True)
    if APPLICATIONSERVER_HUMAN_READABLE_ARG in args:
        setattr(func, APPLICATIONSERVER_HUMAN_READABLE_ATTRIBUTE, True)

    return func

def tag_expose_authenticated(func):
    '''Tag a method as exposed with authentication'''
    setattr(func, EXPOSE_AUTHENTICATED_ATTRIBUTE, True)
    return func

def tag_expose_authorized(func):
    '''Tag a method as exposed with authorization'''

    setattr(func,EXPOSE_AUTHORIZED_ATTRIBUTE, True)
    return func

def expose(func):
    '''Decorator to mark a method as exposed on a service instance'''
    func = tag_exposed(func)

    @functools.wraps(func)
    def exposed_func(*args, **kwargs):
        # We'll pop off the EXPOSED_SERVICE_NAME_KWARG since this should not be
        # handled to the called function. In this implementation we don't need
        # it altogether, but some code, eg the pylabs binding stuff, wants it
        # (and provides a different implementation of C{expose}), so it's
        # always used to call exposed functions.
        kwargs = kwargs.copy()
        try:
            kwargs.pop(EXPOSED_SERVICE_NAME_KWARG)
        except KeyError:
            pass

        return func(*args, **kwargs)

    return exposed_func

def not_threaded(func):
    '''Tag a method as Twisted-aware'''
    setattr(func, APPLICATIONSERVER_NOT_THREADED_ATTRIBUTE, True)
    return func

#Function to check whether a method is exposed
exposed = attrchecker(EXPOSE_ATTRIBUTE)
#Function to check whether a method wants a request argument
want_request =  attrchecker(APPLICATIONSERVER_REQUEST_ATTRIBUTE)
want_human_readable = attrchecker(APPLICATIONSERVER_HUMAN_READABLE_ATTRIBUTE)
# Function to check whether a method should not run in a thread
want_not_threaded = attrchecker(APPLICATIONSERVER_NOT_THREADED_ATTRIBUTE)

'''Attribute set on exposed methods who need authentication'''
EXPOSE_AUTHENTICATED_ATTRIBUTE = 'APPLICATIONSERVER_EXPOSE_AUTHENTICATED'
def expose_authenticated(func):
    '''Decorator to mark a method as exposed with authentication'''
    func = expose(func)
    func = tag_expose_authenticated(func)
    return func

#Function to check whether a method is exposed with authentication
exposed_authenticated = attrchecker(EXPOSE_AUTHENTICATED_ATTRIBUTE)

'''Attribute set on exposed methods who need authorization'''
EXPOSE_AUTHORIZED_ATTRIBUTE = 'APPLICATIONSERVER_EXPOSE_AUTHORIZED'
class expose_authorized:
    '''Decorator to mark a method as exposed with authorization'''
    def __init__(self,**kwargs):
        self.kwargs = kwargs
    def __call__(self,func):
        # We can't use the functools.partial since it for reasons further down in the function
        # we really must return a function here. A mere (whatever) callable would 've been nice
        def fake_partial(f, keywords):
            def newfunc(*fargs, **fkeywords):
                return f(*fargs, **fkeywords)
            newfunc.__dict__.update(f.__dict__)
            newfunc.func = func
            newfunc.auth_categories = keywords

            return newfunc

        if not 'force_authentication' in self.kwargs:
            fa = True
        else:
            try:
                fa = bool(self.kwargs['force_authentication'])
            except:
                fa = True

        if 'force_authentication' in self.kwargs:
            del(self.kwargs['force_authentication'])

        nf = fake_partial(func,self.kwargs)
        nf = expose(nf)
        nf = tag_expose_authorized(nf)

        if fa and not exposed_authenticated(nf):
            nf = expose_authenticated(nf)

        return nf


#Function to check whether a method is exposed with authorization
exposed_authorized = attrchecker(EXPOSE_AUTHORIZED_ATTRIBUTE)

