[qpinstall]: /pylabsdoc/#/Q-Packages/QPInstall

## Samba

Samba is an open source implementation of the SMB protocol for Linux, Solaris and other operating systems. It provides a daemon for sharing files and directories over the network, and client applications to access other SMB shares.

### Installing Samba

Install the latest version of the Q-Packages named 'samba' and 'samba_extension'.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall]] page.

### Location in the Sandbox

The Samba files are installed in:

* *Main samba application files:* `/opt/qbase5/apps/samba/`
* *Samba configuration files:* `/opt/qbase5/cfg/samba`
* *Samba log files:* `/opt/qbase5/var/log/samba`

[[note]]
**Currently available**

* *Samba library settings:* `/opt/qbase5/etc/samba`
[[/note]]


### Managing Samba

#### Management Extensions

* To start the Samba server:

    q.manage.samba.start()

* To stop the Samba server:

    q.manage.samba.stop()

* To restart the Samba server:

    q.manage.samba.restart()

* To get the status of the Samba server:

    q.manage.samba.getStatus()


#### Q-Packages Start & Stop Tasklets

Get a reference of the 'samba' Q-Package that you previously installed. This can be done the same way we installed the package:

    i.qp.find('samba')

Followed by choosing the version of the package you installed if more than one is present.

Now you can use the start and stop tasklets as follows:

* Start:

    i.qp.lastPackage.qpackage.start()

* Stop:

    i.qp.lastPackage.qpackage.stop()


### Configuring Samba

In the Q-Shell you can configure Samba in an easy way, similar to the normal Samba application. However, when you configure Samba with the Q-Shell, there is better error logging and its configuration is stored in a CMDB.

[[note]]
**Note** 
For every change that you apply in the CMDB configuration of Samba, you have to execute the following steps:

1 - Start the changes for the Samba CMDB configuration:

    q.manage.samba.startChanges() 

2 - Peform your changes. Check the 'Creating a Samba Share' example below.

3 - Save the changes:

    q.manage.samba.save() 

4 - Apply the changes:

    q.manage.samba.applyConfig()
[[/note]]


#### Creating a Samba Share

To create a new Samba share, we use the command below:

    q.manage.samba.cmdb.addShare(name, path=None)

* *name:* name of the share.
* *path:* path of the folder to share.


### Code Repositories

The source code can be found on the following BitBucket code repository:
    http://bitbucket.org/despiegk/samba_extension