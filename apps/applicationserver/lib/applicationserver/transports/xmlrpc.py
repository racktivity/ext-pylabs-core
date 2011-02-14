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

import xmlrpclib
import functools
import operator

from twisted.plugin import IPlugin
from twisted.web import xmlrpc, server
from twisted.web.xmlrpc import Fault, NoSuchFunction
from twisted.python import log
from twisted.internet import defer

from zope.interface import implements

from applicationserver.itransport import ITransportFactory, IServerTransport
from applicationserver.itransport import ServerTransportInfo, SiteTransport
from applicationserver.utils import auth_func_attrchecker
from applicationserver.dispatcher import NoSuchService, NoSuchMethod
from applicationserver.dispatcher import AuthenticationError

class XMLRPCTransport(xmlrpc.XMLRPC):
    def __init__(self, dispatcher,allowNone=False):
        xmlrpc.XMLRPC.__init__(self,allowNone)
        self.dispatcher = dispatcher

    def _getFunction(self, functionPath, request):
        # Overridden from C{xmlrpc.XMLRPC}
        try:
            #putSubHandle gets preference
            func = xmlrpc.XMLRPC._getFunction(self, functionPath)

            if not auth_func_attrchecker(func, request):
                raise AuthenticationError("Not authorized")

            return func

        except Exception:
            pass

        if functionPath.count(self.separator) != 1:
            raise NoSuchFunction(self.NOT_FOUND, 'No such function')

        service, method = functionPath.split(self.separator, 1)

        self.dispatcher.getServiceMethod(service, method)

        return functools.partial(self.dispatcher.callServiceMethod, request, service, method)

    def render_POST(self, request):
        # Find out the user agent. User agent 'applicationserver-client' gets
        # a special treatment (pickled Fault)
        userAgent = request.getHeader("user-agent")
        isApplicationserverClient = bool(userAgent == "applicationserver-client")

        request.content.seek(0, 0)
        request.setHeader("content-type", "text/xml")
        try:
            args, functionPath = xmlrpclib.loads(request.content.read())
        except Exception, e:
            f = Fault(self.FAILURE, "Can't deserialize input: %s" % (e,))
            self._cbRender(f, request)
        else:
            try:
                function = self._getFunction(functionPath, request)
            except (NoSuchService, NoSuchMethod), e:
                self._cbRender(Fault(e.ERRNO, e.MESSAGE), request)
            except Fault, f:
                self._cbRender(f, request)
            else:
                defer.maybeDeferred(function, *args).addErrback(
                    self._ebRender, isApplicationserverClient
                ).addCallback(
                    self._cbRender, request
                )
        return server.NOT_DONE_YET

    #Hack to work on old Twisted versions
    if not hasattr(xmlrpc.XMLRPC, 'render_POST'):
        render = render_POST

    def _ebRender(self, failure, isApplicationserverClient=False):
        '''Custom error render method'''
        if isinstance(failure.value, xmlrpclib.Fault):
            return failure.value

        log.err(failure)

        value = getattr(failure.value, 'MESSAGE', None)
        if not value:
            value = getattr(failure, 'getErrorMessage', lambda: 'error')()

        #Use exception.applicationserver_errno if available by default, as
        #spec'ed. Default to 8002, ie self.FAILURE
        errno = getattr(failure.value, 'applicationserver_errno', self.FAILURE)

        if isApplicationserverClient:
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
                failurePickle = None
            else:
                failurePickle = pickle.dumps(failure)

            fault =  xmlrpclib.Fault(errno, [value, failurePickle])
            return fault
        else:
            return xmlrpclib.Fault(errno, value)

class XMLRPCTransportFactory:
    implements(IPlugin, ITransportFactory)

    OPTIONS = None
    PROTOCOL = 'xmlrpc'

    def createTransport(self, dispatcher, configuration):
        allowNone = configuration['allow_none'] if configuration and 'allow_none' in configuration else False

        xmlrpc_transport = XMLRPCTransport(dispatcher, allowNone)
        site = XMLRPCSite(xmlrpc_transport)
        #TODO This is kinda hackish (it's used to be able to hook controller on
        #the XMLRPC transport). Somehow this should be enhanced.
        site._xmlrpc_transport = xmlrpc_transport

        return site


factory = XMLRPCTransportFactory()


class XMLRPCTransportInfo(ServerTransportInfo):
    '''TransportInfo for the XMLRPC transport'''
    PROTOCOL = XMLRPCTransportFactory.PROTOCOL


class XMLRPCSite(SiteTransport):
    TRANSPORT_INFO_CLASS = XMLRPCTransportInfo
