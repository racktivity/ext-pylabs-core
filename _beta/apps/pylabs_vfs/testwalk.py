from pylabs.InitBase import *
from pylabs.Shell import *
from VFSMetadata import *

q.application.appname = "VFSTestMetadata"
q.application.start()

q.logger.maxlevel=6 
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True

metadatapath = "/opt/qbase5/var/vfs/var_log/"
root = "/opt/qbase5/var/log"

import pdb
pdb.set_trace()

vfs=VFSMetadata(metadatapath, root)  #scan log dir and create metadata store for it
vfs.reset()
vfs.populateFromFilesystem()        
vfs.getLatest()

#ipshell()


def _printFileDirPath(args,path,ttype,moddate=0,size=0,md5sum=""):
        q.console.echo("%s %s %s %s %s" % (ttype, path, moddate, size, md5sum))

vfs.walk(_printFileDirPath, None, "")


#test versions
vfs.reset()
vfs.populateFromFilesystem(processHiddenFiles=False,usemd5=False)
q.gui.dialog.askYesNo("Change something in %s, when done press Y." % root) 
vfs.populateFromFilesystem(processHiddenFiles=False,usemd5=False)
#q.gui.dialog.askYesNo("Change something in %s, when done press Y." % root) 
#vfs.populateFromFilesystem(newversion=True,processHiddenFiles=False,usemd5=False)

versions= vfs.listVersions()
print versions
versionToCompareOld=versions[0]

vfs.diffWithOlderVersion(versionToCompareOld)
#versionToCompareNew=versions[-1]
ipshell()

q.application.stop()


