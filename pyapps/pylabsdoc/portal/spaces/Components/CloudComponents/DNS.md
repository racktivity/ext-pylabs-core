[qpinstall]: /pylabsdoc/#/Q-Packages/QPInstall

## Domain Name System Server

A DNS server is used to map a DNS name to the server's IP address.

### Installing the DNS Server Extension

In the Q-Shell, look for and install the latest package named 'dnsserver_extension'.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.


### Location in the Sandbox

* *DNS server command line extension:* `/opt/qbase5/lib/pymonkey/extensions/servers/dnsserver/`


### Managing the DNS Server

#### Management Extensions

* To start the DNS server:

    q.cmdtools.dnsserver.start()

* To stop the DNS server:

    q.cmdtools.dnsserver.stop()

* To restart the DNS server:

    q.cmdtools.dnsserver.restart()

* To check the status of the DNS server:

    q.cmdtools.dnsserver.isRunning()


#### Q-Packages Start & Stop Tasklets

Get a reference of the DNS Server Extension Q-Package that you previously installed. This can be done the same way we installed the package:

    i.qp.find('dnsserver_extension')

Followed by choosing the version of the package you installed if more than one is present.

Now you can use the start and stop tasklets as follows:

* Start:

    i.qp.lastPackage.qpackage.start()

* Stop:

    i.qp.lastPackage.qpackage.stop()


### Code Repositories

The source code can be found on the following BitBucket code repository:
    http://bitbucket.org/despiegk/dnsserver_extension
