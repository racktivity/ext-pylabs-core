from pymonkey.InitBase import *
from pymonkey.Shell import *

q.application.name="webdavconnection"

q.application.start()

webdavurl="http://confluence.aserver.com/plugins/servlet/confluence/default"
webdavmountpoint="/mnt/aserverwebdav"
destdir="/root/webdav/aserver"
login=""
passwd=""
q.qshellconfig.interactive=True
#check if webdav mounted
result,out= q.system.process.execute("mount",outputToStdout=False)
if result<>0:
   raise "Could not execute mount command to find webdav mounts"
if q.codetools.regex.findLine(webdavmountpoint,out)=="":
   #did not find mount will try to mount to aserver webdav
   q.console.echo("WILL TRY TO MOUNT TO WEBDAV SERVER")
   result,i_am=q.system.process.execute("whoami")
   if i_am.find("root")==-1:
      raise "Please login as user root"
   if q.codetools.regex.findLine(webdavurl,out)<>"":
      #still mounted try to unmount
      q.system.process.execute("umount %s" % webdavurl)
   q.system.fs.createDir("/mnt/aserverwebdav")
   q.system.process.execute("apt-get install davfs2 -y")
   q.system.process.executeWithoutPipe("mount.davfs http://confluence.aserver.com/plugins/servlet/webdav %s" % webdavmountpoint)

def copy(sourceDir,destdir,webdavmountpoint):
   q.console.echo("List files in webdav %s" % sourceDir)
   files=q.system.fs.listFilesInDir(sourceDir,True,filter="*.txt")
   tocopy=[]
   for file in files:
      if file.find("@")==-1:
         #file is ok to be copied
         tocopy.append(file)
         q.system.fs.createDir(destdir)
         for fileToCopy in tocopy:
            #q.system.fs.copy()
            filePart=q.system.fs.pathRemoveDirPart(fileToCopy,webdavmountpoint)
            dest="%s/%s" % (destdir,filePart)
            print "copy %s %s" % (fileToCopy,dest)
            q.system.fs.copyFile(fileToCopy,dest)

#NO LONGER NEEDED BECAUSE THE @ CAN BE REMOVED FROM CONFLUENCE
##USE <Confluence base URL>/admin/plugins/webdav/config.action?hiddenOptionsEnabled=true
##copy("%s/Global/PM" % webdavmountpoint,destdir,webdavmountpoint)
##copy("%s/Global/PMDEV" % webdavmountpoint,destdir,webdavmountpoint)


#qshell()

q.application.stop()