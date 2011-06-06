from pylabs import q
from pylabs.baseclasses import BaseType
from pylabs.config import *
from pylabs.inifile import IniFile

def _commit():
    serverIniFile = IniFile(q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'logservermain.cfg'))
    configStr = list()
    for key, value in serverIniFile.getSectionAsDict('main').items():
            configStr.append('%s=%s'%(key,value))
    configStr.append('<store>')
    storeIniFile = IniFile(q.system.fs.joinPaths(q.dirs.cfgDir, 'qconfig', 'logserverstore.cfg'))
    for section in storeIniFile.getSections():
        storeDef = storeIniFile.getValue(section, 'store_def')
        _getConfigStr(eval(storeDef), configStr)
    configStr.append('</store>')
    configFilePath = q.system.fs.joinPaths(q.dirs.cfgDir, 'scribe_logserver.conf')
    fd = open(configFilePath, 'w')
    fd.write('\n'.join(configStr))
    fd.close()

class ScribeServerConfigManagementItem(ConfigManagementItem):
    """
    ScribeConfigurator class
    """

    CONFIGTYPE = "logservermain"
    DESCRIPTION = "Scribe sever config for logserver"
    KEYS = {}
    KEYS['port'] ="port(Port on which the server will listen to"
    KEYS['max_msg_per_second'] ="x_msg_per_second(Max Messages per second)"
    KEYS['max_queue_size'] ="max_queue_size(Max queue size)"
    
   
    def ask(self):
        #the order of the ask questions will define the order of the parameters for review
        self.dialogMessage("Scribe Server configuration for logserver")
        self.dialogAskInteger('port', 'port(Port on which the server will listen to)', default = 9991)
        self.dialogAskInteger('max_msg_per_second', 'max_msg_per_second(Max Messages per second)', default=100000)
        self.dialogAskInteger('max_queue_size', 'max_queue_size(Max queue size)', default = 500000)

   
    def show(self):
        q.gui.dialog.message("\nScribe Server Configuration for logserver [%s]\n\n" % self.itemname +
                             "Port: %(port)s\nMax messages per second: %(max_msg_per_second)s\nMax queue size: %(max_queue_size)s\n " % self.params)
    
    def commit(self):
        _commit()

scribeServerConfig = ItemSingleClass(ScribeServerConfigManagementItem)

def _getConfigStr(storeDict, configStr = None):
    if configStr == None:
        configStr = list()
    for key, value in storeDict.items():
        if isinstance(value, dict):
            configStr.append('<%s>'%key)
            configStr.extend(_getConfigStr(value))
            configStr.append('</%s>'%key)
            continue
        configStr.append('%s=%s'%(key, value))
    return configStr


class ScribeStoreConfigManagementItem(ConfigManagementItem):
    """
    Scribe store configurator
    """
    CONFIGTYPE = "logserverstore"
    DESCRIPTION = "Scribe Store Configuration for logserver"
    KEYS = {}
    KEYS['store_def'] ="Store Definition as dictionary"
    KEYS['max_msg_per_second'] ="x_msg_per_second(Max Messages per second)"
    KEYS['max_queue_size'] ="max_queue_size(Max queue size)"
    def ask(self):
        #the order of the ask questions will define the order of the parameters for review
        self.dialogMessage("Scribe Store configuration for logserver")
        self.dialogAskString('store_def', 'Store Definition as dictionary')

    def show(self):
        q.gui.dialog.message("\nScribe Store Configuration for logserver [%s]\n\n"% self.itemname +
                             "Store Def: %(store_def)s\n"%self.params)
    def commit(self):
        _commit()


scribeStoreConfig = ItemGroupClass(ScribeStoreConfigManagementItem)

