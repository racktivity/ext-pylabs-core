from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "testApp"
q.application.start()

packages=q.qpackages.qpackageFind()
checkduplicates={}
packagesout=[]
for package in packages:
    key="%s_%s_%s" % (package.domain,package.name,package.version)
    if checkduplicates.has_key(key)==False:
        checkduplicates[key]=1
        packagesout.append(package)
for package in packagesout:
    try:
        package.download(True,downloadAllPlatformFiles=True)
    except:
        package.download(True,downloadAllPlatformFiles=True)
        print("could not download qpackage %s" % package)
        ipshell()
ipshell()


q.application.stop()

