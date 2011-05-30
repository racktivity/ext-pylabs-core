from pylabs.config import ConfigManagementItem, ItemSingleClass, ItemGroupClass
from pylabs import q
import string

class MercurialConfigManagementItem(ConfigManagementItem):
    CONFIGTYPE = "mercurialconnection"
    DESCRIPTION = "MERCURIAL Connection"
    def ask(self):
        self.dialogAskString('url', 'Enter base URL of repository e.g. http://bitbucket.org/despiegk/%s' % self.itemname)
        self.dialogAskString('login', 'Username for mercurial connection')
        self.dialogAskPassword('passwd', 'Password for mercurial connection')
        hg_base = q.system.fs.joinPaths(q.dirs.varDir, 'mercurial')
        destination = self.params['url'].rstrip('/').split('/')[-1]
        target = q.system.fs.joinPaths(hg_base, destination)
        self.dialogAskString('destination', 'Destination folder to clone repository [%s]'% target)
        if not self.params['destination']:
            if not q.system.fs.exists(hg_base):
                q.system.fs.createDir(hg_base)
            self.params['destination'] = target

    def show(self):
        """
        Optional customization of show() method
        """
        # Here we do not want to show the password, so a customized show() method
        q.gui.dialog.message("\nMercurial Connection [%s]\n\n" % self.itemname +
                             "  URL:       %(url)s\n   Login:     %(login)s\n  Password:  *****" % self.params)
    def retrieve(self):
        """
        Optional implementation of retrieve() method, to be used by find()
        """
        import re
        rec = re.compile(r"(?P<protocol>http|https|file|ssh)://(?P<other>.*)")
        url = self.params['url']
        result = rec.search(url)
        if result.group('protocol') not in ["file"]:
            authstring = ""
            if self.params.get("login"):
                authstring = self.params.get("login")
                if self.params.get("passwd"):
                    authstring += ":%s" % self.params.get("passwd")
                authstring += "@"
            url = "%s://%s%s" % (result.group('protocol'), authstring, result.group("other"))
        return q.clients.mercurial.getclient(self.params.get('destination', ''), url)

MercurialConfigManagement = ItemGroupClass(MercurialConfigManagementItem)

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

MercurialConfigManagement.findByUrl = findByUrl
