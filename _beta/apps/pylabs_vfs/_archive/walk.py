from pylabs.InitBase import *
from pylabs.Shell import *
from PysyncWalker import *
from VirtualFileSystemMetadata import *
import fnmatch

q.application.appname = "VFSTestMetadata"
q.application.start()

q.logger.maxlevel=6 
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True

root = "/opt/qbase5/var/vfs/var_log/"

vfs=VirtualFileSystemMetadata(root,"/opt/qbase5/var/log")  #scan log dir and create metadata store for it
vfs.reset()
vfs.populateFromFilesystem()        
vfs.getLatest()

ipshell()

#for file in vfs.listFilesInDir("",True,False):
#    print file

def _printFileDirPath(args,path,ttype,moddate=0,size=0,md5sum=""):
        q.console.echo("%s %s %s %s %s" % (ttype, path, moddate, size, md5sum))

vfs.walk(_printFileDirPath,None,"")

#for file in vfs.listDirsInDir("pylabs_agent___3.1/",recursive=True,dirNameOnly=False):
#    print "DIR: %s" % file
    
#for file in vfs.listFilesInDir("",recursive=True,fileNameOnly=False,filter="*wra*"):
#    print "FILE: %s" % file
    

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
changeFilePath = "/opt/qbase5/changes.txt"
q.system.fs.createEmptyFile(changeFilePath)
vfs.compareWithOlderVersion(versionToCompareOld, changeFilePath)
#versionToCompareNew=versions[-1]
ipshell()

q.application.stop()


