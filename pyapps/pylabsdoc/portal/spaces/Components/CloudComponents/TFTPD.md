[qpinstall]: /pylabsdoc/#/Q-Packages/QPInstall

## Trivial File Transfer Protocol Daemon

TFTPD is a FTP server used for Preboot Execution Environment (PXE) booting; it hosts the system images of the corresponding machines.

### Installing TFTPD

Install the latest version of the Q-Package named 'tftpd'.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.


### Location in the Sandbox

* *TFTPD application:* `/opt/qbase5/apps/tftpd/`
* *TFTPD extension:* `/opt/qbase5/lib/pymonkey/extensions/servers/tftp/`


### Managing the TFTPD Server

#### Management Extensions

The server has a management extension to start and stop the server and to do configuration management, some of the commands are listed below.

* To start the TFTPD server:

    q.manage.tftp.start()

* To stop the TFTPD server:

    q.manage.tftp.stop()

* To restart the TFTPD server:

    q.manage.tftp.restart()

* To get the status of the TFTPD server:

    q.manage.tftp.getStatus()


#### Q-Packages Start & Stop Tasklets

Get a reference of the 'tftpd' Q-Package that you previously installed. This can be done the same way we installed the package:

    i.qp.find('tftpd')

Followed by choosing the version of the package you installed if more than one is present.

Now you can use the start and stop tasklets as follows:

* Start:

    i.qp.lastPackage.qpackage.start()

* Stop:

    i.qp.lastPackage.qpackage.stop()


### Configuring the TFTPD Server

* *q.manage.tftp.cmdb.ipAddress:* The IP address of the TFTPD server.
* *q.manage.tftp.cmdb.port:* The port on which the TFTPD is listening.
* *q.manage.tftp.cmdb.serverPath:* Server path. For example, the files which serve the TFTPD server.
* *q.manage.tftp.cmdb.startAtReboot:* Enable when the server should start at reboot.


### Code Repositories

The source code can be found on the following BitBucket code repository:
    http://bitbucket.org/despiegk/tftp_extension