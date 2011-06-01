##General Configuration Functions

The configuration of applications may be complex if you have to configure it via the command line. PyLabs gets rid of this complexity and offers you instead an easy to use configuration platform.
All PyLabs-compatible applications make use of this configuration platform.

There are two sections where you can configure an application:

* `i.config` name space: mainly used for simple configuration where a configuration is just a flat list of key/value pairs
* `q.manage` name space: mainly used for complex configurations, for example a webserver configuration. A 


###List of Configurations
To get a list of configurations of an application:

[[code]]
In [3]: i.config.clients.mercurial.list()
Out[3]: ['pylabsCore', 'lfw']
   
In [8]: q.manage.nginx.cmdb.virtualHosts
Out[8]: {'80': <NginxVirtualHost.VirtualHost object at 0x27f2d50>}   
[[/code]]

In the given examples, the configuration of the Mercurial clients are key/value pairs, the configuration of nginx is a complex configuration.


###Displaying Configurations
If you want to see the details of a configuration of a simple configuration:

[[code]]
In [33]: i.config.clients.mercurial.show()
 
 Mercurial Connection [pylabsCore]
 
   URL:       http://bitbucket.org/incubaid/pylabs-core
    Login:     dewolft
   Password:  *****
 
 Mercurial Connection [lfw]
 
   URL:       https://bitbucket.org/despiegk/lfw
    Login:     dewolft
   Password:  *****
[[/code]]

To get the details of a complex configuration, you have to retrieve the configuration object and then go over the properties of the object.

[[code]]
In [41]: nginx = q.manage.nginx.cmdb.virtualHosts['80']

In [42]: nginx.
nginx.access_log                 nginx.options
nginx.addReverseProxy(           nginx.port
nginx.addSite(                   nginx.removeReverseProxy(
nginx.configFileDir              nginx.removeSite(
nginx.deleted                    nginx.reset_dirtied_after_save(
nginx.dirtyProperties            nginx.reverseproxies
nginx.enabled                    nginx.rootDir
nginx.error_log                  nginx.rootcmdbtypename
nginx.index                      nginx.sites
nginx.ipaddress                  nginx.sitesDir
nginx.isDirtiedAfterSave         nginx.symlinkDir
nginx.isDirty                    nginx.timestampcreated
nginx.name                       nginx.timestampmodified
nginx.new
[[/code]]
