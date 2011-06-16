@metadata title=XMPP Message Format
@metadata tagstring=xmpp message format


# Generic Message Format over XMPP

## cmd

    !$cmd
    param1
    $param2
    $param3
    $param4
    !

* all commands start with \! e.g. \!fs dir ...
* all lines used without \! and send to agent are considered to be 1 or more parameters (only the tasklet which implements the cmd knows if it is 1 param multiline or multiple params)
* to mark end of input send \! without cmd
* first argument will not have '$' prefix


## return

* when executing something output comes back as


## log

* all stderr, stdout, endusermessage, operatormessages, tracing comes back over log
* logEntry will be the original log fields logtype\|timestamp\|source\|level\|tags\|message

    @$jobnr|$logEntry


## return code when executing cmd

    !!!$jobnr $returncodebiggernthan0
    $errormessage
    !!!

* return code is >0 if there's an error

when error stacktrace is sent as log on level


## parameters


###1 parameter

    !machine start
    mymachine
    !
    

###1 parameter which is multiline

    !shell execute
    cd /
    ls
    !


###2 parameters which are all single line

    !acommand
    customerx
    $bill y
    $3
    !

\#the $ sign is used


### 3 parameters which are a mix of single & multiline

    !acommand
    customerx
    $this is important customer
    this customer is housed in rack 1
    treat well
    $3
    !


## some examples


### cmd with multiple lines

    !shellcmd
    cd /
    cd /tmp/1
    ls
    apt-get install mc
    !

return with error (errorcode is 3) and there is a backtrace available

    !!!5 3
    disk is full, could not copy file xxx to yyy
    !!!
    @5|5|$backtraceline1
    @5|5|$backtraceline2
    @5|3|...


### save file

    !fs write
    /etc/avahi/services/something.service
    $SOME CONTENT WHICH WILL BE WRITEN IN FILE
    CAN BE MULTILINE
    !

* remark, notice the $ sign, this sign tells the start of a new param

return without error, lets say agentjobnr is 6

    !!!6 0
    !!!
