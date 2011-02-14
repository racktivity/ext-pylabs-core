import httplib2, urllib

class Connection(object):
    def __init__(self):
        self.h = httplib2.Http(".cache")
        
    def addAuthentication(self, name, password):
        '''
        Add credentials to the HTTP request (Basic HTTP authentication)
        
        @param name:       Username
        @type name:        string
        
        @param name:       Password
        @type name:        string
        '''
        self.h.add_credentials(name, password)
        
    def get(self, url):
        '''
        Do a HTTP POST request
        
        @param url:        HTTP URL
        @type url:         string
        
        @return:           Content of the HTTP response body 
        @rtype:            string
        '''
        res, content = self.h.request(url)
        return content
    
    def post(self, url, params=None, headers=None):
        '''
        Do a HTTP POST request
        
        @param url:        HTTP URL
        @type url:         string
        
        @param params:     Dictionary with parameters to POST to the URL
        @type params:      dict
        
        @param headers:    Dictionary with additional HTTP headers to add to the request
        @type headers:     dict
        
        @return:           Content of the HTTP response body 
        @rtype:            string
        '''
        res, content = self.h.request(url, 'POST', urllib.urlencode(params) if params else params, headers)
        return content

class HttpClient(object):
    def getconnection(self):
        connection = Connection()
        return connection
