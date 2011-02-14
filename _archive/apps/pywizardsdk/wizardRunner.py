from pyamf.remoting.gateway.wsgi import WSGIGateway
from pymonkey.InitBase import *
import traceback
import sys
from wizard import ApplicationserverWizardService

class ApplicationServerRequest:
    def __init__(self, username, password):
        self.username = username
	self.password = password

class WizardEngine:
    def __init__(self):
        self.wizard_engine = ApplicationserverWizardService()
	self.applicationserver_request = ApplicationServerRequest(None, None)

    def setApplicationserverRequest(self, applicationserver_request):
	self.applicationserver_request = applicationserver_request

    def start(self, customerGuid, wizardName, extra=None):
	try:
            return self.wizard_engine.start(customerGuid, wizardName, extra, self.applicationserver_request)
	except Exception, e:
	    print 'Exception occurred while executing start(customerGuid=%s, wizardName=%s, extra=%s)\n'%(customerGuid, wizardName, extra)
	    print '\n'.join(traceback.format_exception(*tuple(sys.exc_info())))

    def callback(self, wizardName='', methodName='', formData='', extra=None, SessionId=None):
        try:
	    return self.wizard_engine.callback(wizardName, methodName, formData, extra, SessionId, self.applicationserver_request)
        except Exception, e:
	    print 'Exception occurred while executing callback(wizardName=%s, methodName=%s, formData=%s, extra=%s, SessionId=%s)\n'%(wizardName, methodName, formData, extra, SessionId)
   	    print '\n'.join(traceback.format_exception(*tuple(sys.exc_info())))

    def stop(self, sessionId):
	try:
	    return self.wizard_engine.stop(sessionId)
        except Exception, e:
	    print 'Exception occurred while executing stop(sessionId=%s)\n'%(sessionId)
	    print '\n'.join(traceback.format_exception(*tuple(sys.exc_info())))

    def result(self, sessionId, result):
	try:
    	    return self.wizard_engine.result(sessionId, result)
        except Exception, e:
	    print 'Exception occurred while executing result(sessionId=%s, result=%s)\n'%(sessionId, result)
	    print '\n'.join(traceback.format_exception(*tuple(sys.exc_info())))

wizard_engine = WizardEngine()

def authenticator(username, password):
    applicationserver_request = ApplicationServerRequest(username, password)
    wizard_engine.setApplicationserverRequest(applicationserver_request)
    return True


class MyGateway(WSGIGateway):
  
    def __call__(self, environ, start_response):
        print environ

        if environ.get('PATH_INFO', None) ==  '/crossdomain.xml':
            response = """
            <!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd"> 
            <cross-domain-policy> 
                <allow-access-from domain="*" /> 
            </cross-domain-policy> 
            """            

            start_response('200 OK', [
                ('Content-Type', 'text/xml'),
                ('Content-Length', str(len(response))),
                ('Server', environ.get('REMOTE_HOST','')),
            ])
            return [response]

	else:
            return  WSGIGateway.__call__(self, environ, start_response)

                



#gateway = WSGIGateway({'wizard_engine': wizard_engine}, authenticator=authenticator)
gateway = MyGateway({'wizard_engine': wizard_engine}, authenticator=authenticator)


if __name__ == '__main__':
    from optparse import OptionParser
    from wsgiref import simple_server

    parser = OptionParser()
    parser.add_option("-p", "--port", default=8899,
        dest="port", help="port number [default: %default]")
    parser.add_option("--host", default="localhost",
        dest="host", help="host address [default: %default]")
    (options, args) = parser.parse_args()

    host = options.host
    port = int(options.port)

    httpd = simple_server.WSGIServer((host, port), simple_server.WSGIRequestHandler)
    httpd.set_app(gateway)

    print "Running Wizard Engine on http://%s:%d" % (host, port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

