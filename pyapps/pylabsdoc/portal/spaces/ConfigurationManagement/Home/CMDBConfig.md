[nginx]: http://wiki.nginx.org
[imgNginxNewsite]: images/images50/pylabs/nginx_newsite.png
[imgNginxFail]: images/images50/pylabs/nginx_fail.png
[imgNginxNewport]: images/images50/pylabs/nginx_newport.png


##CMDB Configuration

When you have an application that requires advanced configuration, it is very likely that a key/value configuration is too complex to configure and/or maintain. 
For example when you have to configure a web server, it would become too hard to configure an ACL with a key/value system.

Therefore you can use the CMDB (Configuration Management DataBase) of PyLabs. The CMDB is a configuration platform that allows you to set up advanced configurations of PyLabs compatible applications.
The configuration of an application with CMDB is available in the `q.manage` name space, for example `q.manage.nginx.cmdb`.


###General Application Functions

An application that is to be configured via the CMDB, has some general functions, such as start, stop, restart, getStatus, ... 
Some functions require one or more parameters, but that is completely application dependent.


###Configuring an Application
To configure an application with the CMDB platform or update a configuration, you always have to follow the following steps:

1. Start the changes: `q.manage.your_application.startChanges()`
2. Configure your application via `q.manage.your_application.cmdb.<configure>`
3. Save and apply the configuration: `q.manage.your_application.save()` and `q.manage.your_application.applyConfig()`


###Example
In this example we configure an '[nginx][]' web server.

[[code]]
In [1]: q.manage.nginx.startChanges()

In [2]: newhost = q.manage.nginx.cmdb.addVirtualHost(?
Definition: newhost = q.manage.nginx.cmdb.addVirtualHost(self, name, ipaddress='0.0.0.0', port=80)
Documentation:
    Create a VirtualHost
    
    
    Parameters:
    
    - name: Name of the virtual host
    - ipaddress (invalid docstring format)
    - port (invalid docstring format)
    
    Returns: new virtual host object


In [3]: newhost = q.manage.nginx.cmdb.addVirtualHost('newHost', ipaddress='127.0.0.1', port=8080)

In [4]: newhost.addSite(?
Definition: newhost.addSite(self, name, location='/')
Documentation:
    Create an Nginx Site
    
    
    Parameters:
    
    - name: name of the site to create
    - location: Configuration to allow depending on the URI
    
    Returns: NginxSite configuration object.


In [5]: site = newhost.addSite('home', location='/')

In [6]: site.addOption(?
Definition: home.addOption(self, option_type, option_settings)
Documentation:
    Add an option to Site Configuration
    
    
    Parameters:
    
    - option_type: Name of the option to add
    - option_settings: Settings of the option to add


In [7]: site.addOption('root', '/opt/qbase5/www/home')

In [8]: q.manage.nginx.save()
 Writing changes to cmdb

In [9]: q.manage.nginx.applyConfig()
 Writing new configuration to disk
 Cleaning up nginx config
 Cleanup done

In [10]: 
[[/code]]

Create a `home` directory under `/opt/qbase5/www` and in that directory create an `index.html` file with some html content.

For example:

[[code]]
<html>
    <h1>This is INCUBAID!</h1>
</html>
[[/code]]

Now start nginx:

[[code]]
In [10]: q.manage.nginx.start()
 Nginx is starting...
 Nginx started successfully.
 Nginx started successfully

In [11]:
[[/code]]

Open an internet browser an go to the URL `http://127.0.0.1:8080`. This is the result:

![nginx_newsite][imgNginxNewsite]

This example is just a basic configuration to give you an idea of how easy it is to configure applications with CMDB.


###Updating a Configuration

The update of a configuration takes the same steps as creating a configuration:

1. Start the changes: `q.manage.your_application.startChanges()`
2. Update the configuration of your application via `q.manage.your_application.cmdb.<configure>`
3. Save and apply the configuration: `q.manage.your_application.save()` and `q.manage.your_application.applyConfig()`

In the following example we reconfigure the port of the created virtual host to 8081 instead of 8080.

[[code]]
In [1]: q.manage.nginx.startChanges()

In [2]: q.manage.nginx.cmdb.virtualHosts
Out[2]: 
{'80': <NginxVirtualHost.VirtualHost object at 0x232f5d0>,
 'newHost': <NginxVirtualHost.VirtualHost object at 0x232f810>}

In [3]: vhost = q.manage.nginx.cmdb.virtualHosts['newHost']

In [4]: vhost.port
Out[4]: 8080

In [5]: vhost.port = 8081

In [6]: q.manage.nginx.save()
 Writing changes to cmdb

In [7]: q.manage.nginx.applyConfig()
 Writing new configuration to disk
 Cleaning up nginx config
 Cleanup done
 Reloading Nginx server configuration...
 Nginx server configuration reloaded successfully.
[[/code]]

When we refresh the page `127.0.0.1:8080`, you will notice that that site is no longer reachable.

![nginx_fail][imgNginxFail]

Now go to the new address `127.0.0.1:8081`:

![nginx_newport][imgNginxNewport]
