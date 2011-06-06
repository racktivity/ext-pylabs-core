from gevent import pywsgi
import cgi
import os
import errno
from pylabs import q

class GServer(object):
    
    def __init__(self, handler=None):
        self.handler = handler
        self.sslEnabled = False

#    def setHandler(self, handler):
#        if not getattr(handler, 'handle', None):
#            raise ValueError('%s: not a valid handler'%handler)
#        self.server = pywsgi.WSGIServer((serverHost, serverPort), handler.handle)
#    
    def start(self, serverHost='127.0.0.1', serverPort=8080, keyfile=None, certfile=None, async=False):
        if keyfile and certfile:
            self.server = pywsgi.WSGIServer((serverHost, serverPort), self.handler.handle, keyfile=keyfile, certfile=certfile)
            print 'Serving on https://%(address)s:%(port)s'%{'address' : self.server.server_host, 'port' : self.server.server_port}
            self.sslEnabled = True            
        else:
            self.server = pywsgi.WSGIServer((serverHost, serverPort), self.handler.handle)
            print 'Serving on http://%(address)s:%(port)s'%{'address' : self.server.server_host, 'port' : self.server.server_port}                    
        if async:
            self.server.start()
        else:
            self.server.serve_forever()
    
    def stop(self, timeout=None):
        if self.sslEnabled:
            print 'Stopping Service on https://%(address)s:%(port)s'%{'address': self.server.server_host, 'port': self.server.server_port}
        else:
            print 'Stopping Service on http://%(address)s:%(port)s'%{'address': self.server.server_host, 'port': self.server.server_port}            
        self.server.stop(timeout)
