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

import json

from twisted.plugin import IPlugin
from twisted.web import http, server
from twisted.web.resource import Resource
from twisted.python import log

from zope.interface import implements

from applicationserver.itransport import ITransportFactory
from applicationserver.itransport import ServerTransportInfo, SiteTransport
from applicationserver.dispatcher import AuthenticationError, AuthorizationError, NoSuchService
from applicationserver.dispatcher import NoSuchMethod

FAILURE_CODE = 8002
JSON_MIME = 'application/json'
SCRIPT_MIME = 'text/javascript'


class JSONException:
    def __init__(self, message, exception):
        self.message = message
        self.exception = exception

    def dumps(self):
        data = {
            'error': True,
            'code': getattr(self.exception, 'applicationserver_errno',
                            FAILURE_CODE),
            'message': self.message,
        }

        try:
            jsonexc = json.dumps(self.exception)
        except:
            jsonexc = str(self.exception)

        data['exception'] = jsonexc

        try:
            ret = json.dumps(data)
            return ret
        except:
            try:
                ret = json.dumps({
                    'error': True,
                    'code': FAILURE_CODE,
                    'message': 'Unable to serialize original exception',
                    'exception': None,
                })
                return ret
            except:
                ret = '''
{"message": "A critical error happened, I don\'t know how to handle this",
"code": %(failure_code)d,
"exception": null,
"error": true}'
''' % {'failure_code': FAILURE_CODE}
                return ' '.join(ret.strip().splitlines())


class RESTTransport(Resource):
    '''Main REST transport

    This handles requests to '/'.
    '''
    def __init__(self, dispatcher, noerrors=False):
        Resource.__init__(self)
        self.dispatcher = dispatcher
        self.noerrors = noerrors

    def getChild(self, name, request):
        if not name:
            return Resource.getChild(self, name, request)
        if len(request.postpath) > 1:
            return RESTDomain(self.dispatcher, name, self.noerrors)
        return RESTService(self.dispatcher, None, name, self.noerrors)


class RESTDomain(Resource):
    def __init__(self, dispatcher, domain, noerrors=False):
        Resource.__init__(self)
        self.dispatcher = dispatcher
        self.domain = domain
        self.noerrors = noerrors

    def getChild(self, name, request):
        if not name:
            return Resource.getChild(self, name, request)
        if not self.isServiceName(str(request.URLPath())):
            return RESTDomain(self.dispatcher, name, self.noerrors)
        return RESTService(self.dispatcher, self.domain, name, self.noerrors)

    def isServiceName(self, url):
        # URL is http://url[:port]/appname/appserver/rest/domain/servicename/method
        urlParts = url.split('/')
        if len(urlParts) < 8:
            return False
        return True


class RESTService(Resource):
    '''REST service handler

    This handles requests to '/myservice/'.
    '''

    isLeaf = True  # Disable calling getChild

    def __init__(self, dispatcher, domain, service, noerrors=False):
        Resource.__init__(self)
        self.dispatcher = dispatcher
        self.service = service
        self.domain = domain
        self.noerrors = noerrors

    def render_call(self, request):
        #TODO Defer this
        def parse_args():
            args = dict()
            for name, value in request.args.iteritems():
                if isinstance(value, list) and len(value) == 1:
                    value = value[0]
                else:
                    #We only support single-item arguments
                    raise ValueError('Multi-item arguments not supported')

                #Unpack input data. Default to JSON, if the input string is not
                #parsable as a JSON string, just pass it through (as a string)
                try:
                    value = json.loads(value)
                except ValueError:
                    value = value

                args[name] = value

            return args

        try:
            args = parse_args()
        except ValueError, e:
            request.setResponseCode(http.INTERNAL_SERVER_ERROR)
            request.setHeader('Content-Type', JSON_MIME)
            return JSONException(
                'The server was unable to parse your request parameters: %s' % str(e), e).dumps()
        callback = None
        contenttype = JSON_MIME
        if 'jsonp_callback' in args:
            callback = args.pop('jsonp_callback')
            contenttype = SCRIPT_MIME

        try:
            originalContentType = str(request.responseHeaders.getRawHeaders("Content-Type"))
            request.setHeader('Content-Type', contenttype)
            d = self.dispatcher.callServiceMethod(request, self.domain, self.service, request.postpath[-1], **args)
        except (NoSuchService, NoSuchMethod), e:
            request.setResponseCode(http.NOT_FOUND)
            request.setHeader('Content-Type', contenttype)
            return JSONException(e.MESSAGE, e).dumps()

        def write(data):
            if callback:
                data = "%s(%s)" % (callback, data)
            request.write(data)

        def finish_render(data):
            try:
                newContentType = str(request.responseHeaders.getRawHeaders("Content-Type"))
                # we JSONify the data only if the content-type was not changed inside the call or
                # if it was set to application/json
                if newContentType == originalContentType or JSON_MIME in newContentType:
                    jsondata = json.dumps(data, indent=2)
                else:
                    jsondata = data
            except Exception, e:
                #Auch, unable to serialize data
                log.msg("Unable to serialize data to JSON: %s" % e)
                request.setResponseCode(http.INTERNAL_SERVER_ERROR)
                request.setHeader('Content-Type', contenttype)
                write(JSONException(
                    'The server was unable to serialize the method result',
                    e).dumps())
            else:
                write(jsondata)

            request.finish()

        def error_render(failure):
            if failure.check(AuthenticationError, AuthorizationError):
                if request.code == http.OK:
                    request.setResponseCode(http.UNAUTHORIZED)
            else:
                log.msg("An error occurred in the service method: %s" % failure)
                request.setResponseCode(http.INTERNAL_SERVER_ERROR)
            request.setHeader('Content-Type', contenttype)
            if self.noerrors:
                write(JSONException('Internal server error', 'Please, contact administrator.').dumps())
            else:
                write(JSONException('Internal server error', getattr(failure, 'value', None)).dumps())

            request.finish()

        d.addCallback(finish_render)
        d.addErrback(error_render)

        return server.NOT_DONE_YET

    def render_GET(self, request):
        if request.uri == "/crossdomain.xml":
            # may needs to-ports="8888,8889"
            request.setHeader("content-type", "text/xml")
            return """<?xml version="1.0"?><!DOCTYPE cross-domain-policy SYSTEM """ \
                """"http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">""" \
                """<cross-domain-policy><allow-access-from domain="*" /></cross-domain-policy>"""
        else:
            return self.render_call(request)

    # POST is just a normal render
    render_POST = render_call

    # Both DELETE and PUT need to have their body parsed first because twisted only does this for POST
    def render_DELETE(self, request):
        request.args = http.parse_qs(request.content.read(), 1)
        return self.render_call(request)

    render_PUT = render_DELETE


class RESTTransportFactory(object):
    implements(IPlugin, ITransportFactory)

    OPTIONS = None
    PROTOCOL = 'rest'

    def createTransport(self, dispatcher, configuration):
        rest_transport = RESTTransport(dispatcher, **configuration)
        site = RESTSite(rest_transport)

        return site


rest_factory = RESTTransportFactory()


class RESTTransportInfo(ServerTransportInfo):
    '''TransportInfo for the REST transport'''
    PROTOCOL = RESTTransportFactory.PROTOCOL


class RESTSite(SiteTransport):
    TRANSPORT_INFO_CLASS = RESTTransportInfo
