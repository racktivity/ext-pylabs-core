# SSH Test Example

[[code]]
from pylabs.InitBase import *
from pylabs.Shell import *
 
q.application.appname = "sshtest"
q.application.start()
 
q.logger.maxlevel=6 #to make sure we see output from SSH sessions
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True
 
client=q.remote.system.connect("192.168.16.108","root","apassword")
print client.process.executeUnix("ls /") #only works on linux, will do some control actions around it
print client.process.execute("ls /")
 
client.close()
ipshell()
 
q.application.stop()
[[/code]]