import pylabs
from pylabs.config import *
from pylabs import q
import string
class HgConnection(ConfigManagementItem):
    CONFIGTYPE = "hgconnection"
    DESCRIPTION = "Mercurial Connection"

    def ask(self):
        self.dialogAskString('url', 'Hg repository URL (e.g. http://bitbucket.org/aserver/drplib_dss)')
        self.dialogAskString('login', 'Username for Hg connection %s' % self.itemname)
        self.dialogAskPassword('passwd', 'Password for Hg connection %s' % self.itemname)
        self.dialogAskString('destination', 'Destination folder to clone repository %s'%self.itemname)

    #  OPTIONAL CUSTOMIZATIONS OF CONFIGURATION

    def show(self):
        """
        Optional customization of show() method
        """
        # Here we do not want to show the password, so a customized show() method
        q.gui.dialog.message("\nHg Connection [%s]\n\n" % self.itemname +
                             "  URL:       %(url)s\n   Login:     %(login)s\n  Password:  *****    \nDestination:       %(destination)s\n" % self.params)
    def retrieve(self):
        """
        Optional implementation of retrieve() method, to be used by find()
        """
#        return pylabs.q.clients.hg.clone(self.params['url'], self.params['login'], self.params['passwd'], self.params['destination'])

        from pylabs.clients.hg.HgTool import HgConnection as HgConn
        return HgConn(self.params['url'], self.params['login'], self.params['passwd'], self.params['destination'])

# Create configuration object for group of hgConnections,
# and register it as an extension on i tree (using extension.cfg)
HgConnections = ItemGroupClass(HgConnection)

def findByUrl(self, url):
    """
    Find hg connection based on url, by using an automatically generated name.
    If connection cannot be found, generate a new one.
    """
    def normalize_name(url):
        while url.endswith('/'):
            url = url[:-1]
        name = url  + '/'
        target = ""
        for character in name:
            if character in string.ascii_letters:
                target = target + character
            else:
                target = target + '_'
        return target
    connectionname = normalize_name(url)
    if connectionname not in self.list():
        self.add(itemname=connectionname, params={'url':url})
    return self.find(itemname=connectionname)

HgConnections.findByUrl = findByUrl

