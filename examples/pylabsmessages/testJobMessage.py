from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "messagetest"
q.application.start()

q.logger.consoleloglevel=5


def encodeDecodeRPCMessage():
     #target0=q.messagehandler.addLogTargetStdOut()
     rpccall=q.messagehandler.getRPCMessageObject()
     #we do it the long way there is also a rpccall.init(,,, method
     rpccall.domain="sso"
     rpccall.category="machine"
     rpccall.methodname="start"
     rpccall.params["machineguid"]="aavbb-dfdsfsdfsd-dfff"
     rpccall.login="qbase"
     rpccall.passwd="nothing"                    
     #rpccall.tagBodyEncode()  ##can call this optionally but is not needed if later getRPCMessage or a messagehandler send method is used
     print rpccall.getMessageString()
     print "="*100
     rpccall2=q.messagehandler.getRPCMessageObject(rpccall.getMessageString())
     print rpccall2.getMessageString()
     ipshell()
     
#obj.init(logmsg="alog",loglevel=4)
     #print obj.getMessageString()
     #obj2=q.messagehandler.getLogObject(obj.getMessageString())
     #if str(obj)<>str(obj2):
     #     raise RuntimeError("2 objects should be the same, proves encoding & decoding is done properly")
     #q.messagehandler.sendMessage(msg,"otherexchange2") 

     
     #ipshell()
#testEncodingDecodingLogObject()    
q.qshellconfig.interactive=True

encodeDecodeRPCMessage()          

     
q.application.stop()

