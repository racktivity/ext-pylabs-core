from pylabs import q
from pylabs.baseclasses.CMDBServerObject import CMDBServerObject
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

# Template base class
from Cheetah.Template import Template as CheetahTemplate

from NginxSite import NginxSite
from NginxReverseProxy import NginxReverseProxy

import os

class Template(object):
    """
    Special Template base class. Subclass and overload template attribute with
    a string containing a Cheetah template. Then call render with a context and
    a rendered string will be returned.
    """
    template = None
    def render(self, context):
        t = CheetahTemplate(self.template, searchList=[context])
        return str(t)

class VirtualHostTemplate(Template):
    template = """
server {
        listen $port;
        server_name $ipaddress;
        
        #if $rootDir
        root $rootDir;
        #end if
        
        #if $index
        index $index;
        #end if
        
        #if $access_log
        access_log $access_log;
        #end if
        
        #if $error_log
        error_log $error_log;
        #end if
        
        #for $key, $value in $options.iteritems()
        $key  $value;
        #end for
        
        #for $siteconfig in $siteconfigs
        $siteconfig
        #end for
        
        #for $reverseproxy in $reverseproxies.itervalues()
        location $reverseproxy.path {
          proxy_pass  $reverseproxy.url;
        }
        #end for
}
    """

class VirtualHost(CMDBSubObject):
    name = q.basetype.string(doc="name of this virtual host")
    port = q.basetype.integer(doc="Port to listen for this VirtualHost", allow_none=True)
    ipaddress = q.basetype.ipaddress(doc="ipaddress or DNS to which the virtual host serves pages")
    sites = q.basetype.dictionary(doc="dictionary of sites exposed by this virtual host")
    configFileDir = q.basetype.dirpath(doc="The directory for virtual host configuration files", 
                                       default=q.system.fs.joinPaths(os.sep, 'etc', 'nginx', 'sites-available'),
                                       allow_none=False)
    symlinkDir = q.basetype.dirpath(doc="The directory for files shortcuts to the virtualhost configuration files", 
                                    default=q.system.fs.joinPaths(os.sep, 'etc', 'nginx', 'sites-enabled'), 
                                    allow_none=False)
    enabled = q.basetype.boolean(doc="Boolean indicating weather this virtualhost is enabled in sites-enabled or not", default=True)
    sitesDir = q.basetype.dirpath(doc="The directory where virtual host site files are stored",
                                  default=q.system.fs.joinPaths(os.sep, 'var', 'www'))
    reverseproxies = q.basetype.dictionary(doc="dictionary of reverse proxies configured in this virtual host", allow_none=True, default=dict())
    options = q.basetype.dictionary(doc="dictionary of specific options on this virtualhost", default=dict())
    access_log = q.basetype.filepath(doc="Path to access log file of this virtual host")
    error_log = q.basetype.filepath(doc="Path to error log file of this virtual host")
    index = q.basetype.list(doc="index files of this virtual host")

    def __init__(self, name, ipaddress, port, configFileDir):
        CMDBSubObject.__init__(self)
        self.name = name
        self.ipaddress = ipaddress
        self.port = port
        self.configFileDir = configFileDir
        self.rootDir = q.system.fs.joinPaths(self.sitesDir, name)
        if not q.system.fs.isDir(self.configFileDir):
            q.system.fs.createDir(self.configFileDir)
        if not q.system.fs.isDir(self.symlinkDir):
            q.system.fs.createDir(self.symlinkDir)

    def addSite(self, name, location='/'):
        """
        Create an Nginx Site

        @param name: name of the site to create
        @type name: string
        @param location: Configuration to allow depending on the URI
        @type location: string
        @return: NginxSite configuration object.
        @rtype: NginxSite
        @raise ValueError: if site with name already exists
        """
        if name in self.sites:
            raise ValueError("Site with name '%s' already exists" % (name))

        locations = [(site.location, site.name) for site in self.sites]
        if location in locations:
            raise ValueError('Location "%s" already exists in site "%s"' %(location, locations[location]))

        site = NginxSite(name, location)
        self.sites[name] = site
        q.logger.log("Site (%s) of location (%s) was added" % (name, location), 3)

        return site
    
    def removeSite(self, name):
        """
        Remove an Nginx Site

        @param name: name of the site to remove
        @type name: string
        @raise KeyError: if site with specified name does not exist
        """
        q.logger.log("Deleting Site (%s)" % name, 3)
        del self.sites[name]

    def addReverseProxy(self, name, url, path):
        """
        Add a reverse proxy configuration

        @param url: url to proxy e.g. http://localhost:8888/
        @param path: path to map the proxied url /appserver/xmlrpc/
        """
        if name in self.reverseproxies:
            raise ValueError("Reverse Proxy with name '%s' already exists" % (name))

        reverseProxy = NginxReverseProxy(url, path)
        self.reverseproxies[name] = reverseProxy
        return reverseProxy

    def removeReverseProxy(self, name):
        """
        Remove the reverse proxy with name

        @param name: name of the reverse proxy to remove
        @type name: string
        """
        if not name in self.reverseproxies:
            raise ValueError("Reverse Proxy with name '%s' does not exist" % (name))
        self.reverseproxies.pop(name)

    def pm_write(self):
        """
        Write the configuration of this virtual host to disk

        @return: base name of the config file that was written
        @rtype: string
        """
        q.logger.log("Extracting context from object", 3)
        if not q.system.fs.exists(self.configFileDir):
            q.system.fs.createDir(self.configFileDir)
        context = {
            "port": self.port,
            "name": self.name,
            "ipaddress": self.ipaddress,
            "siteconfigs": [site.pm_getConfig() for site in self.sites.values()],
            "rootDir": self.rootDir,
            "access_log": self.access_log,
            "error_log": self.error_log,
            "index": ' '.join(set(self.index)),
            "options": self.options,
            "reverseproxies": self.reverseproxies,
        }
        template = VirtualHostTemplate()
        filePath = q.system.fs.joinPaths(self.configFileDir, '%s.conf' % self.name)
        q.system.fs.writeFile(filePath, template.render(context))
        q.logger.log("Config written to '%s'" % (filePath), 3)
        
        if self.enabled:
            filetolink = q.system.fs.joinPaths(self.symlinkDir, q.system.fs.getBaseName(filePath))
            if not q.system.fs.exists(filetolink):
                q.system.fs.symlink(filePath, q.system.fs.joinPaths(self.symlinkDir, q.system.fs.getBaseName(filePath)), overwriteTarget=True)
        else:
            q.system.fs.remove(filetolink, True)

        return filePath
