
from pylabs.InitBase import *
from pylabs.Shell import *

#Mounts the VFS and starts the server in a contiuous mode
q.manage.vfsserver.start('/tmp/metadata/','/var/log/')