from pylabs.config import ConfigManagementItem, ItemSingleClass, ItemGroupClass
from pylabs import q

class CrowdConfigManagementItem(ConfigManagementItem):
    CONFIGTYPE = "crowd"
    DESCRIPTION = "crowd account, key = accountname"
    def ask(self):
        self.dialogAskString('login', 'Enter login')
        self.dialogAskPassword('passwd', 'Enter password for user "%s"' % self.params["login"])

CrowdConfigManagement = ItemGroupClass(CrowdConfigManagementItem)
