from pylabs.config import ConfigManagementItem, ItemSingleClass, ItemGroupClass
from pylabs import q

class MercurialConfigManagementItem(ConfigManagementItem):
    CONFIGTYPE = "mercurialconnection"
    DESCRIPTION = "MERCURIAL Connection"
    def ask(self):
        self.dialogAskString('url', 'Enter base URL of repository e.g. http://bitbucket.org/despiegk/ %s' % self.itemname)
        self.dialogAskString('login', 'Enter login')
        self.dialogAskPassword('passwd', 'Enter password for user "%s"' % self.params["login"])
        self.dialogAskString('codedir', 'default /opt/code/$nameOfConnection',"/opt/code/%s" % self.params["name"])

MercurialConfigManagement = ItemGroupClass(MercurialConfigManagementItem)

