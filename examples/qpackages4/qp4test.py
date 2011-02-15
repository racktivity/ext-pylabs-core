from pylabs.InitBase import *
from pylabs.Shell import *
from pprint import pprint

q.application.appname = "qp4test"
q.application.start()

#print q.qp.find(name="erl*")
#print q.qp.find(domain="qpackages.org")
#print q.qp.find(platform=q.enumerators.PlatformType.UNIX)                
#print q.qp.findNewest(domain="pylabs.org",name="*tools*")
#print q.qp.findNewest(name="*tools*")
#print q.qp.findNewest(name="*tools*",minversion="0",maxversion="10",platform=None)  

q.qshellconfig.interactive=True
q.logger.consoleloglevel=2

#packages = q.qp.getQPackageObjects()
#print packages
#i.qp.updateMetaDataAll()

#domainObject = q.qp.getDomainObject("pylabs.org")
#domainObject.hasModifiedMetadata()
#domainObject.hasModifiedFiles()
#domainObject.getModifiedQPackages()
#domainObject.updateMetadata()
#domainObject.publishDomain()


p=q.qp.get("qpackages.org","erlang","13")
state=p.getState()
print state

p.install()


#pprint(p.getDependencies(recursive=True))

#ipshell()

        
    
        
        
        

q.application.stop()
