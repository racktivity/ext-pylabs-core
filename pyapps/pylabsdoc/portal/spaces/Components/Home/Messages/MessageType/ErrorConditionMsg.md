@metadata title=Error Condition Message
@metadata tagstring=error condition 

[basemsg]: /#/Components/BaseMsg


# logmessage


## basic [basemessage][basemsg] properties

* messagetype = q.enumerators.MessageType.ERRORCONDITION
* time (epoch = int)
* level : errorcondition levels see [ErrorconditionLevels]
* agent : unique agent id (e.g. kdscp@mydomain.com)
* returnqueue : (only populated when using queues)
* source : application name where errorcondition was raised
* tags : holds errorcondition type + extra optional tags & labels
* body : encoded string holding additional errorcondition properties


## additional errorcondition properties

* errormessagepublic -> encoded in messagebbody 
* errormessageprivate -> encoded in messagebbody 
* backtrace -> encoded in messagebbody 
* backtraceextra -> encoded in messagebbody 
* logs -> encoded in messagebbody 
* transactions -> encoded in messagebbody 
* errorconditiontype  -> stored as tag e.g. errorconditiontype:pm04
** is string which describes the errorcondition type  see http://spreadsheets.google.com/ccc?key=0Ap_pNb5g_5DwdHZYN05IZlk3c3NEWmxyU1dwUFoySmc&hl=en


## Encoding Of MessageBody

Message body is constructed out of optional parts

Keywords for these parts are

* public
* private
* backtrace
* backtraceextra
* logs
* transactions

Each part starts with 

    *#***$keyname***#*************************************-*

e.g

    *#***public***#*************************************-*

backtrace, backtraceextra, logs, transactions are only relevent when errorcondition is found in which it is usefull to know context of script running
this information is gathered from python interpreter    

## Sample Message Body (for ErrorCondition Messagetype)

    *#***public***#*************************************-*
    My Pub Message
    *#***private***#************************************-*\n
    My Priv Message
    *#***backtrace***#**********************************-*
    File "/opt/qbase3/utils/shell.py", line 131, in <module>
    main()\n  File "/opt/qbase3/utils/shell.py", line 121, in main
    Shell(debug=options.debug, ns=ns)()\n  File "/opt/qbase3/lib/pymonkey/core/pymonkey/Shell.py", line 704, in __call__
    myshell(*args, **kwargs)\n  File "/opt/qbase3/lib/python2.6/site-packages/IPython/Shell.py", line 243, in __call__
    self.IP.embed_mainloop(banner,local_ns,global_ns,stack_depth=1)
    File "/opt/qbase3/lib/python2.6/site-packages/IPython/iplib.py", line 1622, in embed_mainloop


## code examples

### errorcondition where no pylabs debugging is involved

    message=q.messagehandler.getErrorconditionObject()
    
    #message.init(self, message, messageprivate='', level=error, typeid='', tags='', tb='', backtracebasic='')
    message.initNoBacktrace("cpu temperature too high","pmachine overloaded", q.enumerators.ErrorconditionLevel.CRITICAL, "cp03")
    
    #tags and labels can be used to give context to logmessage
    message.taghandler.labelSet("combinednode")
    message.taghandler.tagSet("vmachineguid","sdsd-23232dsds-3243")
     
    print "pylabs log message:"
    print message
    
    print "serialization of message"
    print message.getMessageString()


### example string representation of logmessage

* is result of : message.getMessageString(multiline=True)  #if printed without multiline True everything will be serialized on 1 line

    2|1266751210|1|unknown.somewhere.com||qshell|combinednode vmachineguid:sdsd-23232dsds-3243|
    *#***public***#*************************************-*
    cpu temperature too high
    *#***private***#************************************-*
    pmachine overloaded


### errorcondition where pylabs debugging is involved

    #clear the logs
    q.logger.clear()
    q.logger.log("1 log message") #will be added to errorcondition object
    message=q.messagehandler.getErrorconditionObject()
    message.init("could not copy x to y","bug in cloudfssystem", q.enumerators.ErrorconditionLevel.CRITICAL, "bug005")
    print "serialization of message to text"
    print message.getMessageString()


### example string representation of logmessage

* is result of : message.getMessageString(multiline=True)

    2|1266753237|1|unknown.somewhere.com||qshell||
    *#***public***#*************************************-*
    could not copy x to y
    *#***private***#************************************-*
    bug in cloudfssystem
    *#***backtrace***#**********************************-*
    File "h:\qbase100\utils/Shell.py", line 140, in <module>
        main()
      File "h:\qbase100\utils/Shell.py", line 130, in main
        Shell(debug=options.debug, ns=ns)()
      File "h:\qbase100\lib\pymonkey\core\pymonkey\Shell.py", line 704, in __call__
        myshell(*args, **kwargs)
      File "h:\qbase100\python26\lib\site-packages\IPython\Shell.py", line 243, in __call__
        self.IP.embed_mainloop(banner,local_ns,global_ns,stack_depth=1)
      File "h:\qbase100\python26\lib\site-packages\IPython\iplib.py", line 1622, in embed_mainloop
        self.interact(header)
      File "h:\qbase100\python26\lib\site-packages\IPython\iplib.py", line 1705, in interact
        more = self.push(line)
      File "h:\qbase100\python26\lib\site-packages\IPython\iplib.py", line 2018, in push
        more = self.runsource('\n'.join(self.buffer), self.filename)
      File "h:\qbase100\python26\lib\site-packages\IPython\iplib.py", line 1936, in runsource
        if self.runcode(code) == 0:
      File "h:\qbase100\python26\lib\site-packages\IPython\iplib.py", line 1968, in runcode
        exec code_obj in self.user_global_ns, self.user_ns
      File "<ipython console>", line 1, in <module>
      File "h:\qbase100\lib\pymonkey\core\pymonkey\messages\ErrorconditionObject.py", line 51, in init
        self.backtrace=self.getBacktrace().strip()
      File "h:\qbase100\lib\pymonkey\core\pymonkey\messages\ErrorconditionObject.py", line 76, in getBacktrace
        for x in traceback.format_stack():
    *#***logs***#***************************************-*
    1/|1266753235/|5/|unknown.somewhere.com/|/|qshell/|/|1 log message


## PyLabs

Inherits from the base MessageObject

[[code]]
class ErrorconditionObject(MessageObject):
    def __init__(self,messagestr=""):
        MessageObject.__init__(self,messagestr)
        self.mtype = q.enumerators.MessageType.ERRORCONDITION
        self.logs=[]
        self.errormessagepublic= ""
        self.errormessageprivate = ""
        self.backtrace =""
        self.backtraceextra=""
        self.typeid=""
        self.transactionsinfo=""
        if messagestr<>"":
            self._fromString(messagestr)
            self.bodyDecode()

    def initNoBacktrace(self, message, messageprivate='', level=q.enumerators.ErrorconditionLevel.ERROR, typeid='', tags=''):
        """
        this object represents an errorcondition but no python traceback or logs or transactions are used
        """
        
     def init(self, message, messageprivate='', level=q.enumerators.ErrorconditionLevel.ERROR, typeid='', tags='', tb='',backtracebasic=""):
        """
        this object represents an errorcondition
        @param tb = backtrace to give context to self.getStackFrameLog()
        """
        
[[/code]]

## errorconditionlevels

1: end user message
2: operator message
3: stdout
4: stderr
5: tracing 1 and/or backtrace python
6: tracing 2
7: tracing 3
8: tracing 4
9: tracing 5
10: special level, is the marker level
