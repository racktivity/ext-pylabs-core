import os
import re

from pylabs import q
from pylabs.baseclasses.CMDBServerObject import CMDBServerObject
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

from NginxVirtualHost import VirtualHost, Template

class NginxTemplate(Template):
    template = """
user       www-data;
worker_processes  4;
pid        $pidFile;
worker_rlimit_nofile 8192;
 
events {
  worker_connections  768;
  #for $eventname, $eventvalue in $events.iteritems()
  $eventkey  $eventvalue;
  #end for
  
}
 
http {

    ##
    # Basic Settings
    ##
    
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_names_hash_bucket_size 128; # this seems to be required for some vhosts
    # server_tokens off;

    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;

    #for $include in $includes
    include   $include;
    #end for
  
    #for $key, $value in $options.iteritems()
    $key $value;
    #end for
    
    ##
    # Logging Settings
    ##

    access_log $access_log;
    error_log $error_log;

    ##
    # Virtual Host Configs
    ##

    ## Include the virtualhosts
    include /etc/nginx/mime.types;
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
    }
    """

class NginxServer(CMDBServerObject):
    cmdbtypename = "nginx"
    name =  q.basetype.string(doc="The name of the server", default="Nginx")
    configFileDir = q.basetype.dirpath(
        doc="The configuration directory of the nginx server",
        default=q.system.fs.joinPaths(os.sep, 'etc', 'nginx'))
    configFileName = q.basetype.filepath(doc="The configuration file of the apache server", default="nginx.conf")
    vhostDir = q.basetype.dirpath(doc="The configuration directory of virtualhosts", default=q.system.fs.joinPaths(os.sep, 'etc', 'nginx', 'sites-available'))
    
    pidFile = q.basetype.filepath(
        doc="location of the server pid file",
        default=q.system.fs.joinPaths(os.sep, "var", "run","nginx.pid"))

    virtualHosts = q.basetype.dictionary(doc="list of virtualhosts defined on this servers", default=dict())
    includes = q.basetype.list(doc="List of files to include", default=list())
    access_log = q.basetype.filepath(doc="Nginx access log file path", default=q.system.fs.joinPaths(os.sep, 'var', 'log', 'nginx', 'access.log'))
    error_log = q.basetype.filepath(doc="Nginx error log file path", default=q.system.fs.joinPaths(os.sep, 'var', 'log', 'nginx', 'error.log'))
    events = q.basetype.dictionary(doc='Nginx events', default=dict())
    options = q.basetype.dictionary(doc="Nginx special specific options", default=dict())

    def addVirtualHost(self, name, ipaddress='0.0.0.0', port=80):
        """
        Create a VirtualHost

        @param name: Name of the virtual host
        @type name: string
        @param ipaddress
        @type name: string
        @param port
        @type name: string
        @return: new virtual host object
        @rtype: VirtualHost
        @raise ValueError: if a virtual host with name already exists
        """
        if name in self.virtualHosts:
            raise ValueError("A virtual host with name '%s' already exists" % (name))

        vhostConfigDir = q.system.fs.joinPaths(self.vhostDir, name)
        vHost = VirtualHost(name, ipaddress, port, vhostConfigDir)
        self.virtualHosts[name] = vHost
        return vHost

    def removeVirtualHost(self, name):
        """
        Remove a VirtualHost

        @param name: Name of the virtual host
        @type name: string
        @raise KeyError: if virtual host with name does not exist
        """
        del self.virtualHosts[name]
        
    def addInclude(self, include):
        """
        Add include file
        
        @param include: Name of the file to include
        @type include: string
        @raise ValueError if include file already exists
        """
        if include in self.includes:
            raise ValueError('An include with name %s already exists' % include)
        self.includes.append(include)
    
    def removeInclude(self, include):
        """
        Remove an Include file
        
        @param include: Name of the file to remove
        @type include: string
        @raise ValueError if include does not exists in includes list
        """
        self.includes.remove(include)

    def addEvent(self, name, value):
        """
        Add Event
        
        e.g. worker_connections 768;
        
        @param name: Name of the event to add
        @type name: string
        @oaram value: Value of the event
        @raise ValueError if include file already exists
        """
        if name in self.events:
            raise ValueError('Event with name %s already exists')
        self.events[name] = value;
    
    def removeEvent(self, name):
        """
        Remove Event
        
        @param name: Name of event to remove
        @type name: string
        @raise KeyError: if name does not exist
        """
        del self.events[name]

    def pm_cleanup(self):
        q.logger.log("Cleaning up nginx config", 2)
        q.logger.log("Removing all virtualhost files", 3)
        q.system.fs.removeDirTree(self.vhostDir)
        q.system.fs.createDir(self.vhostDir)
        q.logger.log("Cleanup done", 2)

    def pm_write(self):
        """
        Write the configuration to disk

        @return: full path of the config file that was written to disk
        @rtype: string
        """
        q.logger.log("Writing new configuration to disk", 2)
        self.pm_cleanup()

        q.logger.log("Writing virtualhost configs", 3)
        for vhostName, vhost in self.virtualHosts.iteritems():
            filePath = vhost.pm_write()
            self.includes.append(filePath)

        q.logger.log("Writing main config file", 3)
        template = NginxTemplate()
        context = {
            'pidFile': self.pidFile,
            'events': self.events,
            'includes': self.includes,
            'access_log': self.access_log,
            'error_log': self.error_log,
            'options': self.options,
        }

        if not q.system.fs.isDir(self.configFileDir):
            q.system.fs.createDir(self.configFileDir)

        configFile = q.system.fs.joinPaths(self.configFileDir, self.configFileName)
        q.system.fs.writeFile(configFile, template.render(context))

        return configFile

