@metadata title=Cloud File System
@metadata tagstring=cloud filesystem file system fs cloudfs


# Cloud Filesystem Example

[[code]]
from pylabs.InitBase import *
from pylabs.Shell import *
 
q.application.appname = "cluster"
q.application.start()
 
q.logger.maxlevel=6 #to make sure we see output from SSH sessions
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True
 
q.console.echo( "Copy 1 file from FTP location to cifs share")
q.cloud.system.fs.exportFile('ftp://ftp.belnet.be/mirror/ftp.centos.org/HEADER.html',  'cifs://aserver:aserver@localhost/share/testje')
 
q.console.echo( "Copy local file to CIFS share")
q.cloud.system.fs.exportFile('file:///tmp/src', 'cifs://aserver:aserver@localhost/share')
 
q.console.echo( "Copy 1 file from FTP server to other FTP server")
q.cloud.system.fs.exportFile('ftp://ftp.belnet.be/mirror/ftp.centos.org/HEADER.html', 'ftp://ftp:ftp@localhost/anon/remote-ftp')
 
q.console.echo( "Copy directory from FTP location to local directory")
q.cloud.system.fs.exportDir('ftp://ftp.belnet.be/mirror/www.putty.be/', 'file:///tmp/local-ftp/')
 
q.console.echo( "Copy local directory to FTP location")
q.cloud.system.fs.exportDir('file:///tmp/local-ftp' , 'ftp://ftp:ftp@localhost/anon/')
 
q.application.stop()
[[/code]]