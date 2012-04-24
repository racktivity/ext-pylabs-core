# Copyright (c) 2009, Nicolas Trangez
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
# 3. Neither the name of the author, nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''Adobe AMF transport for the pylabs Applicationserver'''

import operator

from twisted.plugin import IPlugin
from twisted.web.resource import Resource

from pyamf.remoting.gateway import ServiceWrapper, UnknownServiceMethodError, \
     UnknownServiceError, expose_request
from pyamf.remoting.gateway.twisted import TwistedGateway

from zope.interface import implements

from applicationserver.dispatcher import exposed_authenticated, NoSuchMethod, \
     NoSuchService
from applicationserver.iapplicationserverrequest import \
     IApplicationserverRequest
from applicationserver.itransport import ITransportFactory
from applicationserver.itransport import ServerTransportInfo, SiteTransport

# Some PyAMF glue
class AMFRequest(object):
   implements(IApplicationserverRequest)

   def __init__(self, request, username, password):
      self._request = request
      self._request_hostname = request.getRequestHostname()
      self._client_ip = request.getClientIP()
      self._username = username
      self._password = password

      self.user_authenticated = False

   request_hostname = property(operator.attrgetter('_request_hostname'))
   client_ip = property(operator.attrgetter('_client_ip'))
   username = property(operator.attrgetter('_username'))
   password = property(operator.attrgetter('_password'))


class FakeService(ServiceWrapper):
   '''A fake/proxy service wrapper'''
   expose_request = True

   def __init__(self, request, dispatcher, domain, servicename):
      ServiceWrapper.__init__(self, None)

      self.request = request
      self.dispatcher = dispatcher
      self.domain = domain
      self.servicename = servicename

   def _get_service_func(self, method, params):
      try:
         self.dispatcher.getServiceMethod(self.domain, self.servicename, method)
      except NoSuchService:
         raise UnknownServiceError('Unknown service %s' % self.servicename)
      except NoSuchMethod:
         raise UnknownServiceMethodError('Unknown method %s' % method)

      def fun(http_request, *args):
         try:
            return self.dispatcher.callServiceMethod(http_request._twistedrequest, self.domain,
                                                     self.servicename,
                                                     method, *args)
         except NoSuchService:
            raise UnknownServiceError('Unknown service %s' %
                                      self.servicename)
         except NoSuchMethod:
            raise UnknownServiceMethodError('Unknown method %s' % method)

      return fun

class ApplicationserverAMFGateway(TwistedGateway):
   def __init__(self, dispatcher, *args, **kwargs):
      TwistedGateway.__init__(self, *args, **kwargs)

      self.dispatcher = dispatcher

   def getServiceRequest(self, request, target):
      '''Translate a request into a handling FakeService'''
      parts = target.split('.')
      if len(parts) not in [2, 3]:
         raise UnknownServiceError('Unknown service %s' % target)
      
      
      if len(parts) == 2:
          parts.insert(0, None)
      domain, service, method = parts

      return self._request_class(request.envelope,
                                 FakeService(request, self.dispatcher, domain,
                                             service),
                                 method)

   def getAuthenticator(self, service_request):
      @expose_request
      def checkAuth(http_request, username, password):
         service, func = self.dispatcher.getServiceMethod(
            service_request.service.domain,
            service_request.service.servicename,
            service_request.method)

         request = AMFRequest(http_request, username, password)
         http_request._twistedrequest = request

         if not exposed_authenticated(func):
            return True


         if not self.dispatcher.checkAuthentication(service_request.service.domain, service, request, service_request.method, None, None):
            return False

         return True

      return checkAuth


# Applicationserver hooking comes next

class AMFTransport(Resource):
   def __init__(self, dispatcher):
      Resource.__init__(self)

      gateway = ApplicationserverAMFGateway(dispatcher)
      self.putChild('', gateway)

class AMFTransportFactory:
   implements(IPlugin, ITransportFactory)

   OPTIONS = None
   PROTOCOL = 'amf'

   def createTransport(self, dispatcher, configuration):
      amf_transport = AMFTransport(dispatcher, **configuration)
      site = AMFSite(amf_transport)

      return site

factory = AMFTransportFactory()

class AMFTransportInfo(ServerTransportInfo):
   PROTOCOL = AMFTransportFactory.PROTOCOL

class AMFSite(SiteTransport):
   TRANSPORT_INFO_CLASS = AMFTransportInfo
