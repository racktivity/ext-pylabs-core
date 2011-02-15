from pylabs.InitBase import *
from pylabs.Shell import *
from PysyncWalker import *
import fnmatch

q.application.appname = "VFSMessageServer"
q.application.start()

q.logger.maxlevel=5 #to make sure we see output from SSH sessions
q.logger.consoleloglevel=5
q.qshellconfig.interactive=True


import socket
import PYSocket


class VFSServer():

    def listen(self,port=5000):	
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("",port))
        self.socket.listen(5)	
        q.logger.log( "Socket server waiting for client on port %s" % port)
        client_socket, address = self.socket.accept()
        while 1:	    	    
            data=self.receiveMessage(client_socket)
            if data =="q":
                client_socket, address = self.socket.accept()
            else:
                mo=q.messagehandler.getRPCMessageObject(data)
                #mo.login
                #mo.passwd
                #mo.category="main"
                #print mo.params
                #print mo.methodname
                mo.params={"dirlist":[1,2,3,4,5]}
                message=mo.getMessageString()
                self.sendMessage(message,client_socket)

    def close(self):
        self.socket.close()
        
    ##################dirty hack ###############################
    def _intToString(self,integer):
        #@todo despiegk: there are better ways of doing this, best would be to go to 2 bytes bytestring, please do
        strint=str(integer)
        for t in range(6-len(strint)):
            strint+=" "
        return strint 

    def _stringToInt(self,string):
        return int(string)

    def sendMessage(self,message,socket):
        socket.send(self._intToString(len(message))+message) #first 6 bytes give length        

    def receiveMessage(self,socket):  
        data=socket.recv(6)
        l=self._stringToInt(data) #get length
        if l < 8000:
            data=socket.recv(l)
        else:
            raise RuntimeError("This socket client implementation does not support messages > 8000 bytes")
        #@todo despiegk: also support messages > 8000
        return data
        

server=VFSServer()
server.listen(5001)

q.application.stop()


