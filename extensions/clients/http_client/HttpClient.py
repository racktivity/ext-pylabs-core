import urllib2, urllib
import base64
import mimetypes
import mimetools

HTTP_CREATED = 201 #from practical examples, authorization created returns 201
HTTP_OK = 200
HTTP_NO_CONTENT = 204 #An authorization token was created and provided to the client in the Location header.
HTTP_AUTH_REQUIRED = 401 # Authorization required.
HTTP_FORBIDDEN = 403  #Authentication failed.
HTTP_NOT_FOUND = 404

STATUS_OK = set([HTTP_CREATED, HTTP_OK, HTTP_NO_CONTENT])
STATUS_AUTH_REQ = set([HTTP_AUTH_REQUIRED, HTTP_FORBIDDEN])

AUTHORIZATION_HEADER = 'Authorization'

class Connection(object):
    
    def __init__(self):
        pass
    
    def addAuthentication(self, url, username, password):
        passManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passManager.add_password(None, url, username, password)
        authenticationHandler = urllib2.HTTPBasicAuthHandler(passManager)
        opener = urllib2.build_opener(authenticationHandler)
        urllib2.install_opener(opener)
        
    def get(self, url, data=None, headers=None, **params):
        response = self._http_request(url, data=data, headers=headers, method='GET', **params)
        return response#.read()
    
    def post(self, url, data=None, headers=None, **params):
        response = self._http_request(url, data=data, headers=headers, method='POST', **params)
        return response#.read()
    
    def put(self, url, data=None, headers=None, **params):
        response = self._http_request(url, data=data, headers=headers, method='PUT', **params)
        return response#.read()
        
    def delete(self, url, data=None, headers=None, **params):
        response = self._http_request(url, data=data, headers=headers, method='DELETE', **params)
        return response#.read()
    
    def download(self, fileUrl, downloadPath, customHeaders=None):
        '''
        Download a file from server to a local path
        
        @param fileUrl: url of an existing file that has its data available on server (sent earlier)
        @param downloadPath: local directory to download into
        @param customHeaders: allows this method to be used to retrieve edited copies of an image
        @return: True
        '''
        
        _urlopener = urllib.FancyURLopener()
        if customHeaders:
            for k, v in customHeaders.items():
                _urlopener.addheader(k, v)
        _urlopener.retrieve(fileUrl, downloadPath, None, None)
        return True
    
    def _updateUrlParams(self, url, **kwargs):
        _scheme, _netloc, _url, _params, _query, _fragment = urllib2.urlparse.urlparse(url)
        params = urllib2.urlparse.parse_qs(_query)
        for k, v in params.items():#parse_qs puts the values in a list which corrupts the url later on
            params[k] = v.pop() if isinstance(v, list) else v
            
        for k, v in kwargs.items():
            if v is not None: params[k] = v
        _query = urllib.urlencode(params)
        return urllib2.urlparse.urlunparse((_scheme, _netloc, _url, _params, _query, _fragment))
    
    
    def _http_request(self, url, data=None, headers=None, method=None, **kwargs):
        url = self._updateUrlParams(url, **kwargs)
        request = urllib2.Request(url, data=data)
        if headers:
            for key, value in headers.iteritems():
                request.add_header(key, value)
        if not method:
            method = 'POST' if data else 'GET'
        request.get_method = lambda: method
        resp = urllib2.urlopen(request)
        #if resp.code in STATUS_AUTH_REQ: raise AuthorizationError('Not logged in or token expired')
        if resp.code not in (STATUS_OK):
            raise Exception('unexpected HTTP response status %s: %s'%resp.code, resp)
        return resp
    
class HttpClient(object):
    def getConnection(self):
        connection = Connection()
        return connection