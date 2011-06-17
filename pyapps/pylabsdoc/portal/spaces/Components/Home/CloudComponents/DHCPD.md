@metadata title=DHCP Daemon
@metadata tagstring=dhcpd manage


[qpinstall]: /#/Q-Packages/QPInstall


# Dynamic Host Configuration Protocol Daemon

The DHCPD is an open source DHCP server.
It is used to provide IP addresses to physical and virtual machines using the DHCP.


## Installing the DHCP Server

Install the latest version of the Q-Package named 'dhcpd'.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.


## Location in the Sandbox

* *DHCPD server files:* `/opt/qbase5/apps/dhcpd`
* *DHCP management extensions:* `lib/pymonkey/extensions/servers/dhcp`


## Managing the DHCP Server

### Management Extensions

* To apply changes in the CMDB DHCP configuration:

    q.manage.dhcpd.applyConfig()

* To print the DHCP configuration:

    q.manage.dhcpd.printConfig()

* To print the status of the DHCP configuration:

    q.manage.dhcpd.printStatus()

* To get the current status type of the DHCP server:

    q.manage.dhcpd.getStatus()

* To restart the DHCP server:

    q.manage.dhcpd.restart()

* To start the DHCP server:

    q.manage.dhcpd.start()

* To stop the DHCP server:

    q.manage.dhcpd.stop()

* To check if the availability of an IP address:

    q.manage.dhcpd.isIPAvailable('ip_address'):


### Q-Packages Start & Stop Tasklets

Get a reference of the DHCPD Q-Package that you previously installed. This can be done the same way we installed the package:

    i.qp.find('dhcpd')

Followed by choosing the version of the package you installed if more than one is present.

Now you can use the start and stop tasklets as follows:

* Start:

    i.qp.lastPackage.qpackage.start()

* Stop:

    i.qp.lastPackage.qpackage.stop()


## Configuring the DHCP Server

In the Q-Shell you can configure the DHCP server in an easy way, similar to the normal DHCP server configuration. However, when you configure the DHCP with the Q-Shell, there is better error logging and its configuration is stored in a CMDB.

[[note]]
**Note** 

For every change that you apply in the CMDB configuration of the DHCPD, you have to execute the following steps:

1 - Start the changes for the DHCPD CMDB configuration:

    q.manage.dhcpd.startChanges()

2 - Peform your changes.

3 - Save the changes:

    q.manage.dhcpd.save()

4 - Apply the changes:

    q.manage.dhcpd.applyConfig()
[[/note]]


### Configuration

Some parameters should be set to configure the DHCP server, this can be done by:

* *q.manage.dhcpd.cmdb.autoRestart:* Should this application be picked up by the autorestart monitor, normally valid for daemons.
* *q.manage.dhcpd.cmdb.dirtyProperties:* Return all dirty properties in this instance.
* *q.manage.dhcpd.cmdb.maxLeaseTime:* Maximum lease time. Default value = 6048000.
* *q.manage.dhcpd.cmdb.pxeBootFile:* PXE boot image.
* *q.manage.dhcpd.cmdb.pxeTftpServer:* Server from which the hosts can mount their root filesystem.
* *q.manage.dhcpd.cmdb.useHostName:* Use the name of the host declaration as hostname.


### Shared Networks

* Creating a Shared Network

    q.manage.dhcpd.cmdb.addSharedNetwork(network_name)

* Configuring a Shared Network

    ** *addAddressPool(poolName, fromIp, toIp):* Adds an address pool.
    ** *pxeBootFile:* PXE boot image.
    ** *addDomainNameServer(domainnameserver):* Adds a domain nameserver. Domain nameserver is the IP address.
    ** *pxeTftpServer:* Server from which the hosts can mount their root filesystem.
    ** *addSubNet(subnet, netmask)*: Adds a subnet, returns a DHCP subnet object ( subnet: subnet address,netmask: netmask of the subnet).
    ** *addTimeServer(timeServer):* Adds a timeserver (timeServer: time server IP).


### Hosts

* Adding a Host

    q.manage.dhcpd.cmdb.addHost(name, hardwareaddress, ipaddress)

* *name:* Name of the host.
* *hardwareaddress:* The hardware ID of the network card(for ethernet use mac address)
* *ipaddress:* IP address of the host.

* Configuring a Host
    ** *addDomainNameServer(domainnameserver):* Adds a domain nameserver. Domain nameserver is the IP address.
    ** *addTimeServer(timeServer):* Adds a timeserver (timeServer: time server IP).
    ** *addRouter(router):* Adds a router to the host configuration (router: IP address of the router).
    ** *pxeBootFile:* PXE boot image.
    ** *pxeTftpServer:* Server from which the hosts can mount their root filesystem.


### Creating a Client Class

To create a client class, we use:

    q.manage.dhcpd.cmdb.addClientClass(name, matchStatement=None)

* *name:* is the name of the class.
* *machStatement:* is the statement or condition to separate clients e.g. if substring(hardware,1,2) = 00:23


### Code Repositories

The source code can be found on the following BitBucket code repository:
    http://bitbucket.org/despiegk/dhcpd_extension
    