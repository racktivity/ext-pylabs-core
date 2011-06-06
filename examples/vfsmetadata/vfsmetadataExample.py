
from pylabs.InitBase import *
from pylabs.Shell import *

vfsTest = q.system.vfs.getVFS('/tmp/metadata/','/var/log/',True)
oldVersion = vfsTest.listVersions()[0] #Lists the available metadataversions
fileTest = open('/var/log/test.log','w')
fileTest.write('Testing pylabs_vfs')
fileTest.close()
vfsTest.populateFromFileSystem()
vfsTest.diffWithOlderVersion(oldVersion)
