## XML-RPC Classes

### XMLRPC Server
Implementation of generic object/method exposed through XML-RPC

Classes and functions in this module allow you to expose a custom class instance and its methods through an XMLRPC service easily. It allows you to expose several classes in one server instance.

Here is a sample, the `service` module:
[[code]]
from pylabs.baseclasses.xmlrpc.server import ManagementClassXMLRPCServer
from pylabs.baseclasses.xmlrpc.server import xmlrpc_expose, xmlrpc_require_authentication

    class AuthHandler:
        def check(self, username, password):
            if username == 'user' and password == 'pass':
                return True
            return False

    class ServiceOne:
        @xmlrpc_expose
        def sum(self, a, b):
            return a + b

    class ServiceTwo:
        @xmlrpc_require_authentication
        @xmlrpc_expose
        def get_secret(self):
            return self._generate_secret()

        def _generate_secret(self):
            return 'secret'

ah = AuthHandler()
server = ManagementClassXMLRPCServer(port=8000, authentication_handler=ah)
s1 = ServiceOne()
s2 = ServiceTwo()
server.addManager(s1, 'one')
server.addManager(s2, 'two')
server.run()
[[/code]]

Once this service is running, you can access it using any XMLRPC client. See below for a more user-friendly approach.


### XMLRPC Client
The `ManagementClassXMLRPCClient` class implemented in this module allows you to auto-generate client classes (including tab-completion support in Q-Shell) for services exposed through XMLRPC as explained above.

Here is a sample, using the server as used above. We assume that `ServiceOne` and `ServiceTwo`) are the classes used in the server (see above), implemented in a `service` module.

[[code]]
from pylabs.baseclasses.xmlrpc.client import ManagementClassXMLRPCClient
from service import ServiceOne, ServiceTwo

    class ServiceOneClient(ManagementClassXMLRPCClient):
        MANAGER_CLASS = ServiceOne

    class ServiceTwoClient(ManagementClassXMLRPCClient):
        MANAGER_CLASS = ServiceTwo

c1 = ServiceOneClient('localhost', 8000, endpoint='one')
c2 = ServiceTwoClient('localhost', 8000, username='user', password='pass', endpoint='two')
[[/code]]
