from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname = "messagetest"
q.application.start()

q.logger.consoleloglevel=5


def test1():
     message=[]
     for t in range(100000):
          message.append(q.messagehandler.getMessageObject())
          message[t].body="dd"
          #above test shows that creating message objects is fast enough, is about 50000/sec

def test2():
     target=q.messagehandler.addLogTargetStdOut()
     msg=q.messagehandler.getMessageObject()
     msg.body="a test message"
     q.messagehandler.sendMessage(msg)
    
def test3():
     target0=q.messagehandler.addLogTargetStdOut()
     target=q.messagehandler.addQueueXMPP("testexchange")
     target.login="me"
     target.passwd="1234"
     target.servers=["127.0.0.1"]
     target.exchangenames=["testexchange","otherexchange"]
     msg=q.messagehandler.getMessageObject()
     msg.body="a test message"
     q.messagehandler.sendMessage(msg,"testexchange") 
     q.messagehandler.sendMessage(msg,"otherexchange") 
     q.messagehandler.sendMessage(msg,"otherexchange2") 
     
def testEncodingDecodingLogObject():
     obj=q.messagehandler.getLogObject()
     obj.init(logmsg="alog",loglevel=4)
     print obj.getMessageString()
     obj2=q.messagehandler.getLogObject(obj.getMessageString())
     if str(obj)<>str(obj2):
          raise RuntimeError("2 objects should be the same, proves encoding & decoding is done properly")

     
def testEncodingDecodingErrorConditionObject():
     q.logger.log("make sure something in logger")
     q.logger.log("make sure something in logger2")
     obj=q.messagehandler.getErrorconditionObject()
     obj.init(message="a pub errormsg",\
              messageprivate='private message', level=q.enumerators.ErrorconditionLevel.CRITICAL,\
              typeid='typeid', tags='label1 label2')
     #print obj.getMessageString()
     print obj
     obj2=q.messagehandler.getErrorconditionObject(obj.getMessageString())
     if str(obj)<>str(obj2):
          print "2 objects should be same but are not"
          print obj
          print "------------------------------------------------------------------------------------------------------------"
          print obj2          
          ipshell()
          raise RuntimeError("2 objects should be the same, proves encoding & decoding is done properly")
     #ipshell()
#testEncodingDecodingLogObject()    
q.qshellconfig.interactive=True

testEncodingDecodingErrorConditionObject()          

     
q.application.stop()

