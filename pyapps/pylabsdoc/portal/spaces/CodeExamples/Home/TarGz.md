@metadata title=Tar.gz
@metadata tagstring=targz archive


# Tar.gz Example

[[code]]
from pylabs.InitBase import *
from pylabs.Shell import *
 
q.application.appname = "ftp"
q.application.start()
 
source="/opt/qbase5/utils"
tmp ="/tmp"
q.system.fs.targzCompress(source,q.system.fs.joinPaths(tmp,"test.tgz"))
 
destinationdir=q.system.fs.joinPaths(tmp,"testdir")
q.system.fs.targzUncompress(q.system.fs.joinPaths(tmp,"test.tgz"),destinationdir)
 
 
q.application.stop()
[[/code]]