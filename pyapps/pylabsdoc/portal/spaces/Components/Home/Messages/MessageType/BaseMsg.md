@metadata title=Base Message
@metadata order=1
@metadata tagstring=base message serialization format

# Base Message

The base message used as basis for all specific messages.

## Serialization Format

### Message Format

Can be represented as 1 line or multi-line (when multi-line encoding: \n -> /n)
Standard representation is 1 line (this way can be stored as log)
Max supported size = 16 kbyte

Properties:

* messagetype
* time (epoch = int)
* level (0-10, 5 is std) (int)
* agent
* returnqueue
* source
* tags
* body

Properties are delimited by '|' and set on 1 line:

Format of text:

    type(int)|time(int)|level(int)|agent|returnqueue|source|tags|body\n

Format of body:

* Text without LF & CR, use /n

Format source, tags (string)

* Text without LF & CR, use /n
* Text without |, if | use /|
* Text without :, if : use /:

Example:

    1|754545|9|||performancetester|cpuperf pmachine:dfdf-sdfsdfsdfsddf-sdfsdf|copy file from a to b


### In Pylabs

* q.messagehandler.getMessageObject()
* implemented in pymonkey/core/messages/MessageObject.py

[[code]]
class MessageObject():
    """
    developper friendly representation of pylabs message
    """
 
    def __init__(self, messagestr=""):
        """
        Initialize a logging object starting from a log string
        """
        self.mtype = q.enumerators.MessageType.UNKNOWN
        self.timestamp=0
        self.level =0
        self.agent= q.application.agentid
        self.application = q.application.appname
        self.body = ''
        self.tags = ''
        self.returnqueue=''
[[/code]]

1. Message Type: Pylabs Message Types are classified based on their origination or source in the SSO Environment. There are seven different types of Pylabs messages. Additional information is available on Pylabs Message Types
2. Message time-stamp: Time of message creation is stored in EPOCH Time format, which may be easily converted to full date, time and timezone information using standard EPOCH conversion algorithms and APIs.
Additional information is available on UNIX TimeStamp. You may convert the EPOCH time-stamp online on the Internet. Online EPOCH converter
3. Message Level: Integer representing urgency or level of message e.g. in case of log message is loglevel
4. Message Agent (optional): unique id for agent e.g. kdspc@bxl.daas.be
5. Message ReturnQueue:Address, where (if any) Message Reply can be sent,
6. Message Application (optional): name of application which generated the message
7. Message tags: Message Tags is set of additional information relevant to the message type, which is embedded in the message. Additional information on Tags PylabsTags
8. Message body: Additional information on Body of the Message


## Code Example

* Interactive:

    message = q.messagehandler.getMessageObject()

    message.body="this is a body of a message, can be anything"

    In [1]: message
    Out[1]:
    type:unknown time:2010/02/21 11:37:13 level:0 agent:unknown.somewhere.com application:qshell tags:
    this is a body of a message, can be anything

As you can see above std properties are filled in:

    In [1]: message.getMessageString()
    Out[1]: '0|1266748633|0|unknown.somewhere.com||qshell||this is a body of a message, can be anything'

Gets serialized string to text.