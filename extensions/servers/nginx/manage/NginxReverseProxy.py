from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

class NginxReverseProxy(CMDBSubObject):
    
    url = q.basetype.string(doc="source url to proxy")
    path = q.basetype.string(doc="destination path of the proxy")

    def __init__(self, url, path):
        """
        Initialize
        @param url: url to proxy e.g. http://localhost:8888
        @param path: path to map the proxied url /appserver/xmlrpc/
        """
        self.url = url
        self.path = path