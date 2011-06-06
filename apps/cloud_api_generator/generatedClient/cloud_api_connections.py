import inspect
import xmlrpclib

from pylabs.config import ConfigManagementItem, ItemGroupClass
from pylabs import q
import cloud_api_clients
SSL_PORT = 443

class CloudApiConnection(object):
    """
    Cloud API Connection object. Pass credentials through the constructor or set
    them using the setCredentials method to be able to use this connection.
    """
    def __init__(self, server, port, path, login=None, passwd=None):
        """
        Create a Cloud API Connection

        @param server: IP or DNS name of the server the Cloud API is running on
        @type server: string
        @param port: port the Cloud API is running on
        @type port: number
        @param path: URL path the Cloud API is running on
        @type path: string
        @param login: login
        @type login: string
        @param passwd: password
        @type passwd: string
        """
        q.logger.log("Creating Cloud API Connection object", 5)
        self._server = server
        self._port = port
        self._path = path
        self._login = login
        self._passwd = passwd
        self._transport = None
        self._url = None
        self._proxy = None
        if self._login and self._passwd:
            self.setCredentials(self._login, self._passwd)

	self._reset()
        q.logger.log("Created Cloud API Connection object %s" % (self, ))

    def setCredentials(self, login, passwd):
        """
        Set login and password for this connection. This also triggers the
        reset method.

        @param login: login
        @type login: string
        @param password: password
        @type password: string
        """
        self._login = login
        self._passwd = passwd
        self._reset()

    def _reset(self):
        """
        Create the ServerProxy object and hook all clients to this object
        """
        q.logger.log("Resetting Cloud API Connection object", 5)
        self._url = self._getUrl()
        self._proxy = xmlrpclib.ServerProxy(self._url, transport=self._transport,allow_none=True)
        clientsDir = q.system.fs.getDirName(inspect.getabsfile(cloud_api_clients))
        import sys
        try:
            sys.path.append(clientsDir)
            modules = q.system.fs.listPyScriptsInDir(clientsDir)            
            modules = q.system.fs.listPyScriptsInDir(clientsDir)
            modules.remove('cloud_api_connections')
            for moduleName in modules:
                try:
                    if moduleName.startswith('client'): 
                        module = __import__(moduleName)
                        for memberName, member in inspect.getmembers(module):
                            if inspect.isclass(member):
                                self._hook(memberName.lower(), member)
                except ImportError, ex:
                    q.logger.log('Failed to import module "%s"'%moduleName, 1)
                    raise ex
        finally:
            sys.path.remove(clientsDir)

    def _getUrl(self,forceCredentials=True):
        """
        Return the XML-RPC url for this connection. If forceCredentials is True
        an exception will be raised if self.login or self.passwd are not set.

        The returned url will contain credentials only if login and password
        are set.

        @param forceCredentials: force credentials to be set
        @type forceCredentials: boolean
        @return: url with credentials if they have been set, else without credentials
        @rtype: string
        """
        if forceCredentials:
            if not self._login:
                raise ValueError("No Cloud API login set")
            if not self._passwd:
                raise ValueError("No Cloud API password set")

        if not self._login or not self._passwd:
            credString = ""
        else:
            credString = "%s:%s@" % (self._login, self._passwd)

        return "%s://%s%s:%s%s" % (
            "https" if self._port == SSL_PORT else "http",
            credString,
            self._server,
            self._port,
            self._path,
        )

    def _hook(self, clientName, clientClass):
        """
        Hook a Cloud API client into this object

        @param clientClass: class of the Cloud API Client
        @type clientClass: class
        """
        client = clientClass(self._proxy)
        setattr(self, clientName, client)

    def __str__(self):
        return "Cloud API Connection (%s)" % (self._getUrl(forceCredentials=False), )


class CloudApiConnectionConfig(ConfigManagementItem):
    """
    Configuration of a Cloud API connection
    """
    # (MANDATORY) CONFIGTYPE and DESCRIPTION
    CONFIGTYPE = "cloudapiconnection"
    DESCRIPTION = "Cloud API Connection"
    KEYS = {}
    KEYS['server'] =" (IP) address of the Application Server', 127.0.0.1"
    KEYS['port'] =" port of the Application Server', 80"
    KEYS['path'] =" URL path of the XML-RPC transport of the Application Server', '/appserver/xmlrpc/'"
    KEYS['login'] =" customer login (optional)"
    KEYS['passwd'] =" customer password (optional)"

    # MANDATORY IMPLEMENTATION OF ASK METHOD
    def ask(self):
        self.dialogAskString('server', 'Enter (IP) address of the Application Server', "127.0.0.1")
        self.dialogAskInteger('port', 'Enter port of the Application Server', 80)
        self.dialogAskString('path', 'Enter URL path of the XML-RPC transport of the Application Server', '/appserver/xmlrpc/')
        self.dialogAskString('login', 'Enter customer login (optional)')
        self.params['passwd'] = self.params['passwd'] if 'passwd' in self.params else ''
        if self.params['login']:
            self.dialogAskPassword('passwd', 'Enter customer password (optional)')

    # OPTIONAL CUSTOMIZATIONS OF SHOW METHOD
    def show(self):
        # Here we do not want to show the password, so a customized show() method
        params = dict(itemname=self.itemname, **self.params)
        params['passwd'] = '*' * len(params['passwd'])
        q.gui.dialog.message("Cloud API Client %(itemname)s "
            "(%(login)s:%(passwd)s@%(server)s:%(port)d%(path)s)" % params
        )

    # Optional implementation of retrieve() method, to be used by find()
    def retrieve(self):
        con = CloudApiConnection(
            server=self.params['server'],
            port=self.params['port'],
            path=self.params['path'],
            login=self.params['login'],
            passwd=self.params['passwd'],
        )
        return con

CloudApiConnectionsConfig = ItemGroupClass(CloudApiConnectionConfig)
