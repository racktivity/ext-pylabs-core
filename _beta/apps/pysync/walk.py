from pymonkey.InitBase import *
from pymonkey.Shell import *
from PysyncWalker import *
from VirtualFileSystemMetadata import *
import fnmatch

q.application.appname = "VFSTestMetadata"
q.application.start()

q.logger.maxlevel=6 #to make sure we see output from SSH sessions
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True

root= "/opt/qbase3/var/vfs/var_log/"

vfs=VirtualFileSystemMetadata(root,"/opt/qbase3/var/log")
#vfs.reset()
#vfs.populateFromFilesystem()        
vfs.getLatest()

#for file in vfs.listFilesInDir("",True,False)
#    print file

def _printFileDirPath(args,path,ttype,moddate=0,size=0,md5sum=""):
        q.console.echo("%s %s %s %s %s" % (ttype, path, moddate, size, md5sum))

#vfs.walk(_printFileDirPath,None,"")

#for file in vfs.listDirsInDir("pylabs_agent___3.1/",recursive=True,dirNameOnly=False):
#    print "DIR: %s" % file
    
#for file in vfs.listFilesInDir("",recursive=True,fileNameOnly=False,filter="*wra*"):
#    print "FILE: %s" % file
    

#test versions
#vfs.reset()
#vfs.populateFromFilesystem(newversion=False,processHiddenFiles=False,usemd5=False)
#q.gui.dialog.askYesNo("Change something in %s, when done press Y." % root) 
#vfs.populateFromFilesystem(newversion=True,processHiddenFiles=False,usemd5=False)
#q.gui.dialog.askYesNo("Change something in %s, when done press Y." % root) 
#vfs.populateFromFilesystem(newversion=True,processHiddenFiles=False,usemd5=False)

versions= vfs.listVersions()
print versions
versionToCompareOld=versions[0]
vfs.compareWithOlderVersion(versionToCompareOld,"changes.txt")
#versionToCompareNew=versions[-1]

q.application.stop()


