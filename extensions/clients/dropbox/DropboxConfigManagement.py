
from pylabs.config import ConfigManagementItem, ItemSingleClass, ItemGroupClass, GroupConfigManagement
from pylabs import q


from dropbox import client, rest, auth

class DropboxConfigManagementItem(ConfigManagementItem):
    CONFIGTYPE = "dropboxusers"
    DESCRIPTION = "Dropbox login Name "

    def ask(self):
        self.dialogAskPassword('passwd', 'Enter password for user "%s"' % self.itemname)
        
        if self.state== 1:
            config = q.config.getConfig('dropbox')
            if not config:
                q.errorconditionhandler.raiseError("dropbox.cfg does not exists  ")
            if 'auth' not in config:
                q.errorconditionhandler.raiseError("dropbox.cfg does not include auth section  ")
            config = config['auth']
            config = q.config.getConfig('dropbox')['auth']
            dba = auth.Authenticator(config)
            access_token = dba.obtain_trusted_access_token( self.itemname, self.params["passwd"])
            self.params["key"] = access_token.key
            self.params["secret"] = access_token.secret
            
            
            
    def save(self):
        errors = []

        file = q.config.getInifile(self.configtype)
        if not file.checkSection(self.itemname):
            file.addSection(self.itemname)
        for k, v in self.params.iteritems():
            file.setParam(self.itemname, k, v)
        file.write()

  
DropboxConfigManagement = ItemGroupClass(DropboxConfigManagementItem)
#we have no problem in allowing items like @ so we are monkey patching this method
def _itemnameAsk(self):
    # Ask itemname to user.
    # If self._itemdescription has been defined, use it to make a useful question
    # Check that the name is compatible with the persistency technology (e.g. inifile sectionname)
    name = q.gui.dialog.askString("Please enter a name for the %s" % self._DESCRIPTION)
    return name

DropboxConfigManagement._itemnameAsk = _itemnameAsk

