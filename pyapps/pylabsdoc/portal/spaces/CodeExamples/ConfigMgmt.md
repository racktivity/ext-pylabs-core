# Code Management Example

Below are two example Python files with their extension configuration.

## AppServerConfigManagement.py

[[code]]
from pylabs.config import *
from pylabs import q


class AppServerConfigManagementItem(ConfigManagementItem):
    """
    Configuration of an app server
    """


    # (MANDATORY) CONFIGTYPE and DESCRIPTION

    CONFIGTYPE = "appserver"
    DESCRIPTION = "Application Server"


    # MANDATORY IMPLEMENTATION OF ASK METHOD

    def ask(self):
        ip = self.dialogAskString("ip", "Enter ip address", "127.0.0.1")
        port = self.dialogAskInteger("port", "Enter port", 8901)



    #  OPTIONAL CUSTOMIZATIONS OF CONFIGURATION

    def show(self):
        """
        Optional customization of show() method
        """
        # Here we do not want to show the password, so a customized show() method
        q.gui.dialog.message("AppServer configuration:\n  ip = [%(ip)s], port = [%(port)d]" % self.params)

    def commit(self):
        """
        Optional customization of commit() method
        """
        q.gui.dialog.message("\n --> Modifying App Server Configuration\n")


# Create configuration object for group of AppServerConfigs,
# and register it as an extension on i tree (using extension.cfg)
AppServerConfig = ItemSingleClass(AppServerConfigManagementItem)
[[/code]]


## SvnConfigManagement.py

[[code]]
from pylabs.config import *
from pylabs import q


class SvnConnection(ConfigManagementItem):
    """
    Configuration of an svn connection.
    """


    # (MANDATORY) CONFIGTYPE and DESCRIPTION

    CONFIGTYPE = "svnconnection"
    DESCRIPTION = "Svn Connection"


    # MANDATORY IMPLEMENTATION OF ASK METHOD

    def ask(self):
        ip = self.dialogAskString('ip', 'SVN repository URL (e.g. http://trac.qlayer.com/svn/code/ )')
        branch = self.dialogAskString('branch', 'SVN branch', "trunk")
        login = self.dialogAskString('login', 'username')
        passwd = self.dialogAskPassword('password', 'password')

    #  OPTIONAL CUSTOMIZATIONS OF CONFIGURATION

    def show(self):
        """
        Optional customization of show() method
        """
        # Here we do not want to show the password, so a customized show() method
        q.gui.dialog.message("\nSvn Connection [%s]\n\n" % self.itemname +
                             "  Ip:        %(ip)s\n  Branch:    %(branch)s\n  Login:     %(login)s\n  Password:  *****" % self.params)

    def commit(self):
        """
        Optional customization of commit() method
        """
        q.gui.dialog.message("\n --> Modifying/Creating Svn Connection object\n")

    def remove(self):
        """
        Optional customization of remove() method
        """
        q.gui.dialog.message("\n --> Removing Svn Connection object from q tree\n")

    def retrieve(self):
        """
        Optional implementation of retrieve() method, to be used by find()
        """
        return "Svn Connection Object %s" % self.itemname

# Create configuration object for group of SvnConnections,
# and register it as an extension on i tree (using extension.cfg)
SvnConnections = ItemGroupClass(SvnConnection)

# If you do not want a group of configured items, but just a single configured item:
# SvnConnectionClass = ItemSingleClass(SvnConnection)
[[/code]]


## extension.cfg

    [hook1]
    qlocation=i.demo.svnconnection
    modulename=SvnConfigManagement
    classname=SvnConnections
    enabled=1
    
    [hook2]
    qlocation=i.demo.appserver
    modulename=AppServerConfigManagement
    classname=AppServerConfig
    enabled=1
