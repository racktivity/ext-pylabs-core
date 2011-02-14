
from pymonkey.config import *
from pymonkey import q


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