[basemsg]: /pylabsdoc/#/Components/BaseMsg

## logmessage


### serialization

there is nothing special to know here because is only using the basic properties from the MessageObject
see [BaseMessage] for more info


### [BaseMessage][basemsg]

* messagetype = q.enumerators.MessageType.LOG
* time (epoch = int)
* level : [LogLevel]
* agent : unique agent id (e.g. kdscp@mydomain.com)
* returnqueue : (only populated when using queues)
* source 
* tags
* body : is the log message by itself


### PyLabs

Inherits from the base MessageObject

[[code]]
class LogObject(MessageObject):
    """
    """
    def __init__(self,messagestr=""):
        MessageObject.__init__(self,messagestr)
        self.mtype=q.enumerators.MessageType.LOG

    def init(self,logmsg,loglevel=5,tags=""):
        self.body=logmsg
        self.level=loglevel
        self.level = int(self.level)
        if tags<>"":
            self.tags=tags
[[/code]]


### code example

    logmessage=q.messagehandler.getLogObject()
    logmessage.body="copy file x to file y"
    
    #tags and labels can be used to give context to logmessage
    logmessage.taghandler.labelSet("copyos")
    logmessage.taghandler.tagSet("customerid","100")
     
    print "pylabs log message:"
    print logmessage
    
    print "serialization of message"
    print logmessage.getMessageString()


### example string representation of logmessage

* is result of : logmessage.getMessageString()

    '1|1266749848|5|unknown.somewhere.com||qshell|copyos customerid:100|copy file x to file y'


#### LogLevel

LogLevel classifies the message towards its intended reader and/or targeted device for reading.

<table width="400">
<tr>
<th align="left" width="250" bgcolor="#D8D8D8">Loglevel</th><th width="150" bgcolor="#D8D8D8">Numeric Code</th>
</tr>
<tr>
<td>ENDUSERMESSAGE</td><td align="center">1</td>
</tr>
<tr>
<td>OPERATORMESSAGE</td><td align="center">2</td>
</tr>
<tr>
<td>STDOUT</td><td align="center">3</td>
</tr>
<tr>
<td>STDERR</td><td align="center">4</td>
</tr>
<tr>
<td>TRACING1</td><td align="center">5</td>
</tr>
<tr>
<td>TRACING2</td><td align="center">6</td>
</tr>
<tr>
<td>TRACING3</td><td align="center">7</td>
</tr>
<tr>
<td>TRACING4</td><td align="center">8</td>
</tr>
<tr>
<td>TRACING5</td><td align="center">9</td>
</tr>
<tr>
<td>SPECIALLEVEL</td><td align="center">10</td>
</tr>
</table>