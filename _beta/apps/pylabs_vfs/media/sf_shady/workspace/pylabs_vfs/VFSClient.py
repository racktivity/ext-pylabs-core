from pylabs.InitBase import *
from pylabs.Shell import *
import socket

q.application.appname = "VFSMessageClient"
q.application.start()

q.logger.maxlevel=6 #to make sure we see output from SSH sessions
q.logger.consoleloglevel=2
q.qshellconfig.interactive=True


class VFSCLient():
    
    def connectToServer(self,server="localhost",port=5000, login="", passwd=""):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server,port))
        self.login=login
        self.passwd=passwd

    def sendCommand(self,cmd,param):
        message="%s|%s" % (cmd,param)
        self.sendMessage(message)
        data=self.receiveMessage()
        return data  

    def close(self):
        self.sendMessage("q")
        self.socket.close()

    def _intToString(self,integer):
        #@todo despiegk: there are better ways of doing this, best would be to go to 2 bytes bytestring, please do
        strint=str(integer)
        for t in range(6-len(strint)):
            strint+=" "
        return strint 

    def _stringToInt(self,string):
        return int(string)

    def sendMessage(self,message):
        self.socket.send(self._intToString(len(message))+message) #first 6 bytes give length        

    def receiveMessage(self):  
        data=self.socket.recv(6)
        l=self._stringToInt(data) #get length
        if l < 8000:
            data=self.socket.recv(l)
        else:
            raise RuntimeError("This socket client implementation does not support messages > 8000 bytes")
        #@todo despiegk: also support messages > 8000
        return data



vfsclient=VFSCLient()
vfsclient.connectToServer("localhost",5001)
print "start"
starttime=q.base.time.getTimeEpoch()
nr=40000
for i in range(nr):
    vfsclient.sendCommand("dirlist","/test")
print "stop"
stoptime=q.base.time.getTimeEpoch()
print "nr/sec: %s" % int(nr/(stoptime-starttime))
vfsclient.close()
q.application.stop()


