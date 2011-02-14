
from pymonkey.InitBase import *
from pymonkey.Shell import *


q.application.appname="ejabberdconfigexample"

q.application.start()
q.qshellconfig.interactive=True

class EjabberdConfigfileParser():
    def __init__(self,filepath):
        self.editor=q.codetools.getTextFileEditor(filepath)

    def getVHosts(self):
        chareditor=self.editor.getTextCharEditor()
        pattern="^[ \t]*{[ \r\n\t]*hosts[ \r\n\t]*,"
        chareditor.matchBlocksDelimiter(pattern,"hosts")
        hoststr=chareditor.get1Block("hosts")
        ipshell()
        hosts=q.codetools.regex.replace(pattern,pattern,"",hoststr).strip("[ {}]").split(",")
        hosts=[host.strip(" \"") for host in hosts]
        return hosts
        
    def setVHosts(self,vhosts):
        """
        @param vhosts is array of vhosts
        """
        vhoststr=string.join([ "\'%s\'" % host.strip(" \n\'") for host in vhosts],",")
        vhoststr="{hosts,[%s]}"%vhoststr
        chareditor=self.editor.getTextCharEditor()
        pattern="^[ \t]*{[ \r\n\t]*hosts[ \r\n\t]*,"
        chareditor.matchBlocksDelimiter(pattern,"hosts")
        chareditor.replace1Block("hosts",vhoststr)        
        print chareditor.get1Block("hosts")
        chareditor.save()
        
parser=EjabberdConfigfileParser("exampleEjabberdConfig.cfg")
print parser.getVHosts()
parser.setVHosts(["kds.com","kds.org"])
print parser.getVHosts()
parser.setVHosts(["example.net", "example.com", "example.org"])#set back to original
q.application.stop()
