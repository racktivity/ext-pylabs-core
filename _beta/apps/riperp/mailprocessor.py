from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="setup wizardrunner"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True

dirs2delete=[]
def process(args, path):
        print path[-4:]
        #print path
        if path[-4:].lower()==".pyc" or path[-4:].lower()==".pyo" or path[-4:].lower()==".pyw":
            q.system.fs.removeFile(path)
        if path.find("/.cache")<>-1 and path.find("/.hg/")==-1:
            dirs2delete.append(path)
    
        
qp=i.qp.find("eric")
qp.qpackage.install(False,False,True)
