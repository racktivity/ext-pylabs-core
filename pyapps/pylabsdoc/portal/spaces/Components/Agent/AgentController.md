[command]: /pylabsdoc/#/PyLabs50/AgentCommands


## Agent Controller

### intro (this is not implemeted yet)

* is ejabberd (cluster) + xmpp robot providing agent controller config mgmt functionality
* this robot always listens to agentcontroller@$domainname

    ** e.g. domaincontroller@eur.daas.com


### agentcontroller api

* see: [Agent Commands][command] for basic protocol used to call for cmd's

* agentcontroller@$topdomainname method:domain check params:domainname

    ** check domainname is unique, return "unique" or "notunique"
    ** this is only installed once, this is the mother of all domains, this domain is responsible for making sure domain names are unique

* agentcontroller@$domainname method:agent register params: `["agentname":$agentname","domain":$domain,"passwd":$passwd]`

    ** register an agent to domain, make sure is known in local ejabberd server

* agentcontroller@$domainname method:agent setpasswd params: `["agentname":$agentname","domain":$domain,"passwd":$passwd]`

* agentcontroller@$domainname method:agent getuniquename params:$domain 

    ** ask agentcontroller to return a unique name (will be a nr) for the specified domain   (*)

* agentcontroller@$domainname method:agent delete params:$agentname

* agentcontroller@$domainname method:agent presence params:$agentname $agentnameToAddToRoster

    ** add $agentnameToAddToRoster to agent roster, do this in XMPP server (ejabberd)


### how does it get installed

* qpackage:  agentcontroller 4
* installs the appropriate tasklets in the AgentXMPPRobot tasklet dirs

    ** these tasklets impement above api
