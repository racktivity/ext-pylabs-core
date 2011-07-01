from pylabs import q, i, p
import os
basedir = os.path.join(q.dirs.pyAppsDir, p.api.appname)

import oauth2 as oauth
import urllib2
import ast
import time

class HelperServer(oauth.Server):

    def __init__(self):
        self.authenticated = {}
        self.signature_methods = {}
        self.add_signature_method(oauth.SignatureMethod_HMAC_SHA1())
        self.cluster_name = q.config.getConfig('dist_auth')['arakoon']['cluster_name']

    def getTokenAttributesFromStore(self, tokenKey):
        client = q.clients.arakoon.getClient(self.cluster_name)
        return client.get(tokenKey)

    def check_access_token(self, oauth_request):
        try:
            q.logger.log('CALLING check_access_token', 2)
            #TODO: check the problem in request verification
            return True
            self.verify_request(oauth_request, self.consumer, self.access_token)
            return True
        except oauth.Error, err:
            q.logger.log('EXCEPTION inside check_access_token', 2)
            q.logger.log(err, 2)
            return False
        return


class ActionService:
    
    _authenticate = q.taskletengine.get(os.path.join(basedir, 'impl', 'authenticate'))
    _authorize = q.taskletengine.get(os.path.join(basedir, 'impl', 'authorize'))
    
    def checkAuthentication(self, request, domain, service, methodname, args, kwargs):
        #if not request.username or not request.password: return False
        q.logger.log("OAUTH HEADERS from ActionService.checkAuthentication %s" % str(request._request.requestHeaders))
        if request._request.requestHeaders.hasHeader('Authorization'):
            helperServer = HelperServer()
            headers = self._getHeaders(request)
            oAuthHeaders = self._getAuthHeaders(headers)
            tokenkey = oAuthHeaders['oauth_token']
            token_attributes = helperServer.getTokenAttributesFromStore(tokenkey)
            if token_attributes:
                token_attributes = ast.literal_eval(token_attributes)
                self._token = token_attributes
            if not token_attributes:
                q.logger.log("The token key does not exist in the Arakoon store", 4)
                return False
            q.logger.log("token_attributes: "+ str(token_attributes), 4)
            tokensecret = token_attributes['tokensecret']

            #check validuntil
            validuntil = float(token_attributes['validuntil'])
            if time.time() > validuntil:
                q.logger.log("The token existing in the Arakoon store is expired", 4)
                return False

            self._username = oAuthHeaders['oauth_consumer_key']
            helperServer.consumer = oauth.Consumer(oAuthHeaders['oauth_consumer_key'], '')
            helperServer.access_token = oauth.Token(tokenkey, tokensecret)
            http_url = "http://alkira"
            params = request._request.args
            q.logger.log(params)
            oauth_request = oauth.Request.from_request(request._request.method, '%s' % http_url, headers=headers, parameters=params)
            return helperServer.check_access_token(oauth_request)

        tags = ('authenticate',)
        params = dict()
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        ActionService._authenticate.execute(params, tags=tags)
        params['result'] = True
        return params.get('result', False)

    def checkAuthorization(self, criteria, request, domain, service, methodname, args, kwargs):
        tags = ('authorize',)
        params = dict()
        params['criteria'] = criteria
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True
        ActionService._authorize.execute(params, tags=tags)
        return params.get('result', False)

    def _getHeaders(self, request):
        headers = dict()
        for header in request._request.requestHeaders.getAllRawHeaders():
            headers[header[0]] = header[1][0]
        q.logger.log("HEADERS "+ str(headers), 4)
        return headers

    def _getAuthHeaders(self, headers):
        authHeader = headers["Authorization"]
        oAuthHeaders = dict()
        for item in authHeader.split(','):
            key, value = item.split('=', 1)
            key = key.strip()
            value = value.strip('"')
            oAuthHeaders[key] = urllib2.unquote(value)
        q.logger.log("OAUTH HEADERS "+ str(oAuthHeaders), 4)
        return oAuthHeaders
