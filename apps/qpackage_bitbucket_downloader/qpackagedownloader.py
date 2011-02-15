from pylabs.InitBase import *

q.application.appname="setup wizardrunner"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True

packages=q.qp.find("*")
for package in packages:
    try:        
        package.download(forceDownload=True,allplatforms=True)
    except:
        print package
        q.system.fs.writeFile("errors.txt",str(package)+"\n",append=True)