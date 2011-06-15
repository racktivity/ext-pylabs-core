## Agent XMPP Robot

xmpp robot = the component which terminates the xmpp messages and executes the api


### Implementation Details XMPP Robot


### Parsing Incoming XMPP Messages

* every incoming XMPP message is parsed in
    ** cmd
    ** params  (for way how params need to be parsed see [XMPP Message Format|3.2 XMPP Message Format]


### Tasklet Engine Used

dirstructure

    $qbase/apps/agent/cmds/$commandname/$tasklets


* load tasklet engine per commandname, keep in memory
* params passed to tasklet engine
    ** params\["cmd"\]
    ** params\["params"\]= \[$a param string which can be multiline,$a param string which can be multiline,...\]
*return is put by tasklet in params\["returnmessage"\] & params\["returncode"\]
*in tasklet logging is done on level
    ** \[loglevels\]
* no q.console or q.dialog
* logging is returned over xmpp channel 
