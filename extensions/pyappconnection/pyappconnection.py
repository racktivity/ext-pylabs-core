from pylabs.config import ConfigManagementItem, ItemGroupClass
from pylabs import q, p

class PyAppConnection(object):
    """
    Pyapp API Connection object. Pass credentials through the constructor or set
    them using the setCredentials method to be able to use this connection.
    """
    def __init__(self, pyappname, server, login=None, passwd=None):
        """
        Create a Yapp API Connection

        @param pyappname: Name of the pyapp to make a connection to
        @type  pyappname: string
        @param server: IP or DNS name of the server the Pyapp API is running on
        @type server: string
        @param port: port the  API is running on
        @type port: number
        @param path: URL path the API is running on
        @type path: string
        @param login: login
        @type login: string
        @param passwd: password
        @type passwd: string
        """
        q.logger.log("Creating API Connection object", 5)
        self._pyappname = pyappname
        self._server = server
        self._login = login
        self._passwd = passwd
        self._transport = None


class PyappConnectionConfig(ConfigManagementItem):
    """
    Configuration of a API connection
    """
    # (MANDATORY) CONFIGTYPE and DESCRIPTION
    CONFIGTYPE = "pyappconnection"
    DESCRIPTION = "Pyapp API Connection"

    # MANDATORY IMPLEMENTATION OF ASK METHOD
    def ask(self):
        self.dialogAskString('pyappname', 'Enter the name of your pyapp', "sampleapp")
        self.dialogAskString('server', 'Enter (IP) address of the Application Server', "127.0.0.1")
        self.dialogAskString('login', 'Enter customer login (optional)')
        self.params['passwd'] = self.params['passwd'] if 'passwd' in self.params else ''
        if self.params['login']:
            self.dialogAskPassword('passwd', 'Enter customer password (optional)')

    # OPTIONAL CUSTOMIZATIONS OF SHOW METHOD
    def show(self):
        # Here we do not want to show the password, so a customized show() method
        params = dict(itemname=self.itemname, **self.params)
        params['passwd'] = '*' * len(params['passwd'])
        q.gui.dialog.message("API Client %(itemname)s "
            "(%(login)s:%(passwd)s@%(server)s:%(port)d%(path)s)" % params
        )

    # Optional implementation of retrieve() method, to be used by find()
    def retrieve(self):
        return p.application.getAPI(self.params['pyappname'], 
                    self.params['server'], username=self.params['login'],
                    password=self.params['passwd'])

PyappConnectionsConfig = ItemGroupClass(PyappConnectionConfig)
