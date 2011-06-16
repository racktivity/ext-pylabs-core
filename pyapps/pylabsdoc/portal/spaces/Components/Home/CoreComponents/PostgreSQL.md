@metadata title=PostgreSQL
@metadata tagstring=postgres sql relational database db

[qpinstall]: /#/Q-Packages/QPInstall


# PostgreSQL

PostgreSQL is an open source relational database. Typically it is used to store and retrieve data of a data model. In PyLabs, it is used together with OSIS for storing OSIS views.

## PostgreSQL Users

To install PostgreSQL you should check if you have the correct user rights and access to the system.

[[note]]
**Note** 
If qbaseusermanagement is not yet installed and configured, it will be automatically installed and configured.
[[/note]]


## Installing PostgreSQL

Install the latest version of the Q-Package named 'postgresql'.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.

[[note]]
**Note** 
The more recent 'postgresql' packages might not have this exact name, so search for the package with 'postgresql*' instead. For this tutorial, I worked with the package 'postgresql_8_4_3'.
[[/note]]

The configuration tasklet of PostgreSQL will initialize the database.

## Location in the Sandbox

* *PostgreSQL command and management extension:* `/opt/qbase5/lib/pymonkey/extensions/servers/postgresql8`
* *Basic PostgreSQL files:* `/opt/qbase5/apps/postgresql`
* *PostgreSQL libraries:*    
    ** `/opt/qbase5/lib`
    ** `/opt/qbase5/lib64`


## Managing PostgreSQL

### Management Extensions

* To start the PostgreSQL server:

    q.manage.postgresql8.start()

* To stop the PostgreSQL server:

    q.manage.postgresql8.stop()

* To restart the PostgreSQL server:

    q.manage.postgresql8.restart()

* To reload the configuration of the PostgreSQL server:

    q.manage.postgresql8.reload()

* To print the PostgreSQL server status:

    q.manage.postgresql8.printStatus()

* To get the PostgreSQL server status:

    q.manage.postgresql8.getStatus()

* To apply changes you made to the PostgreSQL server configuration:

    q.manage.postgresql8.applyConfig()

* To create or update root login credentials:

    q.manage.postgresql8.applyUserCredentials()

* To save any changes you have made:

    q.manage.postgresql8.save()


### Q-Packages Start & Stop Tasklets

Get a reference of the 'postgresql' Q-Package that you previously installed. This can be done the same way we installed the package:

    i.qp.find('postgresql')

Followed by choosing the version of the package you installed if more than one is present.

Now you can use the start and stop tasklets as follows:

* Start:

    i.qp.lastPackage.qpackage.start()

* Stop:

    i.qp.lastPackage.qpackage.stop()


## Configuring PostgreSQL

In the Q-Shell you can configure PostgreSQL in an easy way, similar to the normal PostgreSQL HTTPD application. However, when you configure PostgreSQL with the Q-Shell, there is better error logging and its configuration is stored in a CMDB.

[[note]]
**Note** 
For every change that you apply in the CMDB configuration of PostgreSQL, you have to execute the following steps:

1 - Start the changes for the PostgreSQL CMDB configuration:

    q.manage.postgresql8.startChanges()

2 - Peform your changes.

3 - Save the changes:

    q.manage.postgresql8.save()

4 - Apply the changes:

    q.manage.postgresql8.applyConfig()
[[/code]]


### Creating a Database

To create a database, use the following command:

    q.manage.postgresql8.cmdb.addDatabase(name='test')

### Setting Access Rights

To add a user to the access control list, use the command below:

    q.manage.postgresql8.cmdb.databases['test'].addACE(self, username, passwd, right=R, fromIp=None, toIp=None, netIp=None, netMask=None)

* *username:* name of the user.
* *right:* access right granted to this user (R, W, C).
* *fromIp:* start range for network access (IP address).
* *toIp:* end range for network access(IP address).
* *netIp:* network IP address.
* *passwd:* password for the user.


## Code Repositories

The source code can be found on the following BitBucket code repository:
    http://bitbucket.org/despiegk/postgresql8_extension
    