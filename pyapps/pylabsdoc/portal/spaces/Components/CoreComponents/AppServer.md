[qpinstall]: /pylabsdoc/#/Q-Packages/QPInstall



## Application Server

The Pylabs application server is the component responsible for exposing functionality over several transports. The definition and implementation of an application server service is 100% separated from the underlying transport.
Out of the box XML-RPC, REST and AMF are available as possible transports. The transport mechanism can be extended by writing your own plug-ins.

Technically the application server is implemented as a Twisted reactor and every application server service is a Twisted service.
For more information regarding the Twisted framework check the Twisted framework website.


### How to Install

In your Q-Shell, find and install the latest 'applicationserver' Q-Package.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.

After the installation is complete, restart your Q-Shell in order to trigger the configuration of the installed Q-Package.

Once it restarts you will be asked a series of question regarding the configuration, you can use the default values for every question, except for allowing non values in XML-RPC, choose yes for that question.

[[note]]
**Note** 
The values present between square brackets are the defaults, you do not have to type them, simply press the enter key unless you would like to change them.
[[/note]]

Below are the configuration questions:

    XMLRPC server listening IP address [127.0.0.1]:
    XMLRPC server listening IP port [8888]:
    Allow None values in xmlrpc (y/n):
    IP address of the REST transport [127.0.0.1]:
    REST server listening IP port [8889]:
    IP address of the AMF transport [127.0.0.1]:
    AMF server listening IP port [8899]:
    Incoming mail server:


### Location in the Sandbox

The Application server directories are located at:

* *Application folder:* `/opt/qbase5/apps/applicationserver/`
* *Services:* `/opt/qbase5/apps/applicationserver/services`
* *Log files:* `/opt/qbase5/var/log/applicationserver.log`
* *Configuration file server:* `/opt/qbase5/cfg/qconfig/applicationserver.cfg`
* *Configuration file services:* `/opt/qbase5/cfg/qconfig/applicationserverservice.cfg`


### Managing the Application Server

Below are a set of the most common commands you need to manage the application server:

* To start the application server:

    q.manage.applicationserver.start()

* To stop the application server:

    q.manage.applicationserver.stop()

* To restart the application server:

    q.manage.applicationserver.restart()

* To check if the application server is running:

    q.manage.applicationserver.isRunning()

* In case you added, removed or modified one of the application server services, you can reload all or a specified service without restarting the application server itself. To reload all the services at once:

    q.manage.applicationserver.reload()

* To list the services that are currently installed:

    q.manage.applicationserver.listServices()


To reload a specific service:

[[note]]
**Note** 
The name of the service to reload must be one of the values retrieved by the `q.manage.applicationserver.listServices()` command.
[[/note]]

    q.manage.applicationserver.reloadService('service_name')

### Configuring the Application Server

Let's take a look on how to change the server's configuration.

For example, if we would like to modify the port for the XML-RPC transport we use the following commands:

    config = i.servers.applicationserver.getConfig()

    config['xmlrpc_port'] = '8080'

    i.servers.applicationserver.configure(config)

After we change the port, we restart the application server to insure that the new port is used:

    q.manage.applicationserver.restart()


### Adding & Removing Services

In case you implemented your own application server service, you will need to add it to the list of services served by the application server.

#### Adding Services

Adding a service takes 2 parameters:

# Name for the service to add.
# Location of the module and class to expose.

[[info]]
**Information** 
Path starts from `/opt/qbase5/apps/applicationserver/services`. Use the normal Python name space annotation.
[[/info]]

For example, if you created a folder named 'test_service' underneath the path specified above and in this folder you created a Python module named Test.py containing a class named 'mytest', the Q-Shell commands would look like this:

    In [1]: i.servers.applicationserver.services.add()
    Please enter a name for the Application server service: test_service
     Service implementation class spec: test_service.Test.mytest

In case you add a service, make sure you reload your service as explained above.


#### Removing Services

Removing a service can be done by executing the following command:

    i.servers.applicationserver.services.remove()

A list of the available services will be shown and you will be asked to select the one you would like to remove. Do so by typing the number that corresponds to the service, and then press enter:

    Please select a Application server service
        1: test_service
        2: hello_world_service
        Select Nr (1-2):


### Hello World Service Example

In this example we will explain how to write your own application server service and show how this service can be called over various transports.


#### Service Code

Create a new Python module on the folowing location:

    /opt/qbase5/apps/applicationserver/services/hello_world_service/helloworld.py

The module:

    from pymonkey import q
    class helloworld():
        @q.manage.applicationserver.expose
        def sayHello(self):
            return 'Hello World!'


#### Installing the Service

From the Q-Shell execute the following commands to add your service to the application server:

    In [1]: i.servers.applicationserver.services.add()
    Please enter a name for the Application server service: hello_world_service
     Service implementation class spec: hello_world_service.helloworld.helloworld

[[info]]
**Information**
With the service implementation class spec we can specify the name of the folder underneath `/opt/qbase5/apps/applicationserver/services`, the name of our Python module, followed by the name of our class to expose. Use the '.' as a separator just like in normal Python namespace definition.
[[/info]]

Next, execute the following command to instruct the application server to reload our service:

    q.manage.applicationserver.reloadService('hello_world_service')


#### Calling the Service

**Using XML-RPC**

The following code snippet shows you how easy it is to call our application server service over XMP-RPC using Python:

    import xmlrpclib
    client = xmlrpclib.ServerProxy('http://127.0.0.1:8888/RPC2')
    print client.hello_world_service.sayHello()

**Using REST**

The following code snippet shows you how easy it is to call our application server service over REST by using the PyLabs HTTP client extension:

    client = q.clients.http.getconnection() 
    client.get('http://127.0.0.1:8889/hello_world_service/sayHello')


### Code Repositories

The source can be found on the following BitBucket code repository:
    http://bitbucket.org/despiegk/applicationserver