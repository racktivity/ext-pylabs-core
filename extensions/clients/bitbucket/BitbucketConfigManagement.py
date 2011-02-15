from pylabs.config import ConfigManagementItem, ItemSingleClass, ItemGroupClass
from pylabs import q

class BitbucketConfigManagementItem(ConfigManagementItem):
    CONFIGTYPE = "bitbucket"
    DESCRIPTION = "bitbucket account, key = accountname"
    def ask(self):
        self.dialogAskString('login', 'Enter login')
        self.dialogAskPassword('passwd', 'Enter password for user "%s"' % self.params["login"])

BitbucketConfigManagement = ItemGroupClass(BitbucketConfigManagementItem)

