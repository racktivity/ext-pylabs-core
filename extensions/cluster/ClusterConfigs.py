import pylabs
from pylabs.config import *
from pylabs import q
import string
from pylabs.Shell import *

class ClusterConfig(ConfigManagementItem):
    CONFIGTYPE = "clusterconfig"
    DESCRIPTION = "Cluster Configuration"   
    KEYS = {}
 
    KEYS['domain'] ="Domain name for the cluster."
    KEYS['ip'] ="Ip addresses of clusternodes (comma separated)"
    KEYS['rootpasswd'] ="rootpassword for cluster"
    KEYS['master'] ="Which node is the master"
    
    def ask(self):
        self.dialogAskString('domain', 'Domain name for the cluster.')
        self.dialogAskString('ip', 'Ip addresses of clusternodes (comma separated)')        
        #self.dialogAskYesNo('local','Are we part of this cluster', False)
        self.dialogAskString('rootpasswd', 'rootpassword for cluster')        
        self.dialogAskChoice('master', 'Which node is the master',choices=[str(item.strip()) for item in self.params["ip"].split(",")])

    def show(self):
        """
        Optional customization of show() method
        """
        # Here we do not want to show the password, so a customized show() method
        items=["domain: %s"%self.params["domain"],"ipaddresses: %s"%self.params["ip"],"master: %s" %str(self.params["master"])]
        q.console.echo(self.itemname)
        q.console.echoListItems(items)
    
    #def retrieve(self):
        #"""
        #Optional implementation of retrieve() method, to be used by find()
        #"""
##        return pylabs.q.clients.hg.clone(self.params['url'], self.params['login'], self.params['passwd'], self.params['destination'])

        #from pylabs.clients.hg.HgTool import HgConnection as HgConn
        #return HgConn(self.params['url'], self.params['login'], self.params['passwd'], self.params['destination'])

# Create configuration object for group,
# and register it as an extension on i tree (using extension.cfg)
ClusterConfigs = ItemGroupClass(ClusterConfig)

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

def addClusterNode(self,clustername,ipaddress):
    """
    node with $ipaddress to add to cluster with name=$clustername
    """
    config=self.getConfig(clustername)
    if config["ip"].find(ipaddress)==-1:
        config["ip"]=config["ip"]+",%s"%ipaddress
        self.configure(clustername,config)

ClusterConfigs.addClusterNode = addClusterNode

