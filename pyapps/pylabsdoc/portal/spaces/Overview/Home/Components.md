@metadata title=Pylabs Components
@metadata order=20
@metadata tagstring=components overview description concise

[Nginxlink]: http://www.nginx.org/
[xmlrpc]: http://en.wikipedia.org/wiki/XML-RPC
[REST]: http://en.wikipedia.org/wiki/REST
[AMF]: http://en.wikipedia.org/wiki/Action_Message_Format
[ejabberdlink]: http://www.process-one.net/en/ejabberd/
[XMPP]: http://xmpp.org/
[Arakoon]: http://www.arakoon.org/
[agent]: #/Components/Agent
[appserver]: #/Components/AppServer
[monitoring]: #/Components/MonitoringAgent
[PostgreSQL]: #/Components/PostgreSQL
[Tasklets]: #/Overview/Tasklets
[wfe]: #/Components/WFE
[DHCPD]: #/Components/DHCPD
[dns]: #/Components/DNS
[Samba]: #/Components/Samba
[TFTPD]: #/Components/TFTPD
[component]: #/Components/Home


# Pylabs Components

Pylabs is built with a set of components, each having its specific task. Below you find an overview of these components with a concise description of their functionality.
More details about the components can be found in the [Components chapter][component].

## Agent
An [agent][] is a service connected to the central Extensible Messaging and Presence Protocol ([XMPP][]) service. Agents are responsible for executing RScripts which use SALs installed on the system. 
The agent is responsible for tasks such as starting and stopping a machine in a virtual environment.


## Application Server
The Pylabs [application server][appserver] is the component responsible for exposing functionality (services) over several transports. The definition and implementation of an Application Server service is 100% separated from the underlying transport.
Out of the box [XML-RPC][xmlrpc], [REST][] and [AMF][] are available as possible transports. The transport mechanism can be extended by writing your own plug-ins.


## Arakoon
[Arakoon][] is a key/value store of objects. This database is used to store the actual objects of your application. Although Arakoon is a database, it is non-queryable nor it is a relational database. 


## ejabberd
**[ejabberd][ejabberdlink]** is an XMPP application server. It is a distributed, fault-tolerant technology that allows the creation of large-scale instant messaging applications. The server can reliably support thousands of simultaneous users on a single node and has been designed to provide exceptional standards of fault tolerance.
ejabberd is used in Pylabs as communication platform between the Pylabs agents and the agent controller.


## Monitoring Agent
The [monitoring agent][monitoring] is a Python application that contains a scheduler. This scheduler is responsible for starting tasklets which gather monitor information at fixed moments. 
The monitor information is saved in the DRP.


## Nginx
[Nginx][Nginxlink] (pronounced engine-X) is a lightweight, high-performance Web server. Nginx doesn't rely on threads to handle requests, instead it uses a much more scalable event-driven (asynchronous) architecture. 
This architecture uses small, but more importantly, predictable amounts of memory under load.


## OSIS
Object Storage and Indexing System.
OSIS is a layer on top of Arakoon and PostgreSQL. It has two functions:

* store and retrieve Thrift Serialized Objects in and from Arakoon
* store and update views in PostgreSQL


## PostgreSQL
[PostgreSQL][] is an open source relational database, which is fast and queryable. This database is used to store views on objects in the Pylabs' DRP.


## Tasklets
The Pylabs [tasklets][] framework provides an easy and modular way to execute small pieces of reusable Python code which are loaded into memory. 
The tasklet engine is the component responsible for loading, categorizing and executing tasklets based on tags and parameters.


## Workflow Engine
The [Workflow Engine][wfe] is one of the core components in the Pylabs application stack. It is responsible for the dispatching and monitoring of jobs across all the agents in the domain.


# Specific Cloud Components
Below you find a list of components that are typically used in an environment for Cloud Applications.


## DHCPD
The [DHCPD][] is an open source DHCP server.
It is used to provide IP addresses to physical and virtual machines using the DHCP.


## DNS Server
A [DNS server][dns] is used to map a DNS name to the server's IP address.


## Samba
[Samba][] is an open source implementation of the SMB protocol for Linux, Solaris and other operating systems. It provides a daemon for sharing files and directories over the network, and client applications to access other SMB shares.


## TFTPD (Trivial File Transfer Protocol Daemon)
[TFTPD][] is a FTP server used for Preboot Execution Environment (PXE) booting; it hosts the system images of the corresponding machine
