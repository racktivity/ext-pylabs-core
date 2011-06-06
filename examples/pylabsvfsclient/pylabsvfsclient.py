
from pylabs.InitBase import *
from pylabs.Shell import *

client = q.clients.vfsclient.getConnection('127.0.0.1','8080')
client.dirstat('/var/log/')
client.fileGetInfo('/var/log/auth.log')
client.listVersions()
