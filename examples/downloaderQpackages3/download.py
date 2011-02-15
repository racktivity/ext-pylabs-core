from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "downloader"
q.application.start()

i.qpackages.updateQPackageList()


toskip=["bootimage","bootserver"]

packages=q.qpackages.qpackageFind()
checkduplicates={}
packagesout=[]
for package in packages:
    toprocess=True
    for skipitem in toskip:
        if package.name.find(skipitem)<>-1:
            toprocess=False
    if toprocess:
        key="%s_%s_%s" % (package.domain,package.name,package.version)
        if checkduplicates.has_key(key)==False:
            checkduplicates[key]=1
            packagesout.append(package)

while True:
    for package in packagesout:
        packagedir="/opt/qbase3/var/qpackages/%s/%s/%s" % (package.domain,package.name,package.version)
        print packagedir
        if q.system.fs.exists(packagedir) ==False or q.system.fs.exists("%s/ok2" % packagedir)==False:
            try:
                package.download(False,downloadAllPlatformFiles=True)
                q.system.fs.writeFile("%s/ok2" % packagedir,"%s" % q.base.time.getTimeEpoch())
            except:
                print "ERROR: COULD NOT DOWNLOAD %s" % package
    

q.application.stop()
