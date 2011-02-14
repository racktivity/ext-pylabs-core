# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

import os
import re

# Template base class
from Cheetah.Template import Template as CheetahTemplate

from pymonkey import q
from pymonkey.baseclasses.CMDBServerObject import CMDBServerObject
from pymonkey.baseclasses.CMDBSubObject import CMDBSubObject

# Must initialise ApacheSiteType
from ApacheSiteType import ApacheSiteType
from ApacheAuthType import ApacheAuthType

from ApacheCommon import parseComplexConfig

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

class JkWorker(CMDBSubObject):
    name = q.basetype.string(doc="name of the worker")
    type = q.basetype.string(doc="worker type", default="ajp13")
    hostname = q.basetype.string(
        doc="hostname on which the tomcat server is reachable",
        default="localhost",
    )
    port = q.basetype.integer(
        doc="port on which the tomcat server is listening",
        default=8009,
    )

    def __init__(self, name):
        CMDBSubObject.__init__(self)
        self.name = name

class JkWorkers(object):
    """
    Represents a list of JkWorkers. Used to combine all JkWorkers and write
    their config to disk.
    """
    def __init__(self, workers, configFileDir):
        self.workers = workers
        self.configFileDir = configFileDir

    def pm_getFileName(self):
        """
        Get base name of the JkWorkers config file

        @return: base name of the JkWorkers config file
        @rtype: string
        """
        return "workers.properties"

    def pm_write(self):
        """
        Write the JkWorker configuration to disk.

        @return: Full pathname of the written file
        @rtype: string
        """
        context = {
            "workers": self.workers,
        }
        template = JkWorkerTemplate()
        fileName = self.pm_getFileName()
        filePath = q.system.fs.joinPaths(self.configFileDir, fileName)
        if not q.system.fs.isDir(self.configFileDir):
            q.system.fs.createDir(self.configFileDir)
        q.system.fs.writeFile(filePath, template.render(context))
        return fileName

class Proxy(CMDBSubObject):
    address = q.basetype.string(doc="destination address of the proxy")
    port = q.basetype.integer(doc="destination port of the proxy")
    allowedHosts = q.basetype.list(
        doc="string representation of who has access via the proxy, i.e. "
        "[\"192.168.1.0/24\", \"192.168.0\", \"test.com\"], empty means allow"
        " from all"
    )

    def __init__(self, address, port):
        CMDBSubObject.__init__(self)
        self.address = address
        self.port = port

class ReverseProxy(CMDBSubObject):
    url = q.basetype.string(doc="source url to proxy")
    path = q.basetype.string(doc="destination path of the proxy")

    def __init__(self, url, path):
        """
        Initialize
        @param url: url to proxy e.g. http://localhost:8888
        @param path: path to map the proxied url /appserver/xmlrpc/
        """
        self.url = url
        self.path = path

class VirtualHost(CMDBSubObject):
    name = q.basetype.string(doc="name of this virtual host")
    port = q.basetype.integer(doc="Port to listen for this VirtualHost", allow_none=True)
    ipaddress = q.basetype.ipaddress(doc="ipaddress to which the virtual host serves pages")
    sites = q.basetype.dictionary(doc="dictionary of sites exposed by this virtual host")
    proxies = q.basetype.dictionary(doc="dictionary of proxies configured in this virtual host")
    complexConfig = q.basetype.dictionary(doc="is a extra entry in the apache configuration file", allow_none=True)
    configFileDir = q.basetype.dirpath(doc="The directory for virtual host configuration files", allow_none=False)
    reverseproxies = q.basetype.dictionary(doc="dictionary of proxies configured in this virtual host", allow_none=True, default=dict())
    _aclSubDir = "acl"

    def __init__(self, name, ipaddress, port, configFileDir):
        CMDBSubObject.__init__(self)
        self.name = name
        self.ipaddress = ipaddress
        self.port = port
        self.configFileDir = configFileDir
        if not q.system.fs.isDir(self.configFileDir):
            q.system.fs.createDir(self.configFileDir)

    def addSite(self, name, sitetype, location=None):
        """
        Create an ApacheSite

        @param name: name of the site to create
        @type name: string
        @param sitetype: type of the site (HTML, TOMCAT, PHP, PYTHON, SVN)
        @type sitetype: q.enumerators.ApacheSiteType
        @param location: location will overrule the default generation of the location on the webserver, default the location is [apache site root]/[site name]
        @type location: string
        @return: ApacheSite configuration object.
        @rtype: ApacheSite
        @raise ValueError: if site with name already exists
        """
        if name in self.sites:
            raise ValueError("Site with name '%s' already exists" % (name, ))

        siteClass = sitetype.value
        if not location:
            location = q.system.fs.joinPaths(q.dirs.appDir, "apache", "www", name)
        site = siteClass(name, location)
        self.sites[name] = site
        q.logger.log("Site (%s) of Type (%s) was Added" % (name, sitetype), 5)

        return site

    def removeSite(self, name):
        """
        Remove a Site

        @param name: name of the site to remove
        @type name: string
        @raise KeyError: if no site with name
        """
        q.logger.log("Deleting Site (%s)"%name, 5)
        del self.sites[name]

    def addProxy(self, name, address, port):
        """
        Add a proxy configuration

        @param name: name of the proxy
        @type name: string
        @param address: address
        @type address: string
        @param port: port
        @type port:
        @return: ApacheProxy object
        @rtype: ApacheProxy
        @raise ValueError: if proxy with name already exists
        """
        if name in self.proxies:
            raise ValueError("Proxy with name '%s' already exists" % (name, ))

        proxy = Proxy(address, port)
        self.proxies[name] = proxy
        return proxy


    def addReverseProxy(self, name, url, path):
        """
        Add a reverse proxy configuration

        @param url: url to proxy e.g. http://localhost:8888/
        @param path: path to map the proxied url /appserver/xmlrpc/
        """
        if name in self.reverseproxies:
            raise ValueError("Reverse Proxy with name '%s' already exists" % (name))

        reverseProxy = ReverseProxy(url, path)
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

    def removeProxy(self,name):
        """
        Remove the proxy with name

        @param name: name of the proxy to remove
        @type name: string
        @raise KeyError: if no proxy with name
        """
        del self.proxies[name]

    def pm_getFileName(self):
        """
        Get base name of the virtual host config file

        @return: base name of the virtual host config file
        @rtype: string
        """
        return "vhost_%s.conf" % (self.name, )

    def pm_getACLDir(self):
        """
        Get directory containing the Access Control List files

        @return: directory containing the ACL files
        @rtype: string
        """
        return q.system.fs.joinPaths(self.configFileDir, self._aclSubDir, self.name, "")

    def pm_write(self):
        """
        Write the configuration of this virtual host to disk

        @return: base name of the config file that was written
        @rtype: string
        """
        q.logger.log("Writing ACL information for sites of %s" % (self, ), 3)
        aclDir = self.pm_getACLDir()
        for site in self.sites.values():
            site.pm_writeACL(aclDir)

        q.logger.log("ACL information written", 3)
        q.logger.log("Extracting context from object", 3)
        context = {
            "port": self.port,
            "ipaddress": self.ipaddress,
            "siteConfigs": [site.pm_getConfig(aclDir) for site in self.sites.values()],
            "proxies": self.proxies.values(),
            "complexConfig": parseComplexConfig(self.complexConfig),
            "reverseproxies":self.reverseproxies.values()
        }
        template = VirtualHostTemplate()
        fileName = self.pm_getFileName()
        filePath = q.system.fs.joinPaths(self.configFileDir, fileName)
        q.system.fs.writeFile(filePath, template.render(context))
        q.logger.log("Config written to '%s'" % (filePath, ), 3)
        return fileName

class ApacheServer(CMDBServerObject):
    cmdbtypename = "apache"
    _apacheDir = q.system.fs.joinPaths(q.dirs.appDir, "apache")
    # subdir for the config files
    _configSubDir = "conf"
    # subdir for the vhost config files (insie _configSubDir)
    _vhostSubDir = "vhost.d"
    # subdir for the JkWorker config file
    _jkSubDir = "jk"

    name =  q.basetype.string(doc="The name of the server", default="Apache")
    configFileDir = q.basetype.dirpath(
        doc="The configuration directory of the apache server",
        default=q.system.fs.joinPaths(_apacheDir, _configSubDir),
    )
    configFileName = q.basetype.filepath(doc="The configuration file of the apache server", default="httpd.conf")
    extraConfigFile = q.basetype.filepath(doc="The location of the extra configuration of the apache server", allow_none=True)
    documentRoot = q.basetype.dirpath(
        doc="The root location for the websites",
        default=q.system.fs.joinPaths(q.dirs.baseDir, "www")
    )

    pidFile = q.basetype.filepath(
        doc="location of the server pid file",
        default=q.system.fs.joinPaths(q.dirs.pidDir, "httpd.pid")
    )
    apacheUser = q.basetype.string(doc="apache system user", default="qbase")
    apacheGroup = q.basetype.string(doc="apache group", default="qbase")
    serverRoot = q.basetype.string(
        doc="Base serverroot should point to the apache base installation dir",
        default=q.system.fs.joinPaths(q.dirs.appDir, "apache", "")
    )
    complexConfig = q.basetype.dictionary(
        doc="is full apache config file but for one virtualhost (allows "
        "sysadmin to make 100% custom configuration but on a per virtualhost"
        "basis)"
    )
    virtualHosts = q.basetype.dictionary(
        doc="list of virtualhosts defined on this servers",
        default=dict()
    )
    JkWorkers = q.basetype.dictionary(
        doc="configured workers for this apacheserver",
        default=dict()
    )

    # Default modules, using a list because order might matter
    modules = q.basetype.list(doc="List of modules to be loaded", default=[
        ("authn_file_module", "modules/mod_authn_file.so"),
        ("authn_dbm_module", "modules/mod_authn_dbm.so"),
        ("authn_anon_module", "modules/mod_authn_anon.so"),
        ("authn_default_module", "modules/mod_authn_default.so"),
        ("authz_host_module", "modules/mod_authz_host.so"),
        ("authz_groupfile_module", "modules/mod_authz_groupfile.so"),
        ("authz_user_module", "modules/mod_authz_user.so"),
        ("authz_dbm_module", "modules/mod_authz_dbm.so"),
        ("authz_owner_module", "modules/mod_authz_owner.so"),
        ("authz_default_module", "modules/mod_authz_default.so"),
        ("file_cache_module", "modules/mod_file_cache.so"),
        ("cache_module", "modules/mod_cache.so"),
        ("disk_cache_module", "modules/mod_disk_cache.so"),
        ("mem_cache_module", "modules/mod_mem_cache.so"),
        ("bucketeer_module", "modules/mod_bucketeer.so"),
        ("dumpio_module", "modules/mod_dumpio.so"),
        ("echo_module", "modules/mod_echo.so"),
        ("case_filter_module", "modules/mod_case_filter.so"),
        ("case_filter_in_module", "modules/mod_case_filter_in.so"),
        ("ext_filter_module", "modules/mod_ext_filter.so"),
        ("include_module", "modules/mod_include.so"),
        ("filter_module", "modules/mod_filter.so"),
        ("charset_lite_module", "modules/mod_charset_lite.so"),
        ("deflate_module", "modules/mod_deflate.so"),
        ("log_config_module", "modules/mod_log_config.so"),
        ("logio_module", "modules/mod_logio.so"),
        ("env_module", "modules/mod_env.so"),
        ("cern_meta_module", "modules/mod_cern_meta.so"),
        ("expires_module", "modules/mod_expires.so"),
        ("headers_module", "modules/mod_headers.so"),
        ("ident_module", "modules/mod_ident.so"),
        ("usertrack_module", "modules/mod_usertrack.so"),
        ("setenvif_module", "modules/mod_setenvif.so"),
        ("proxy_module", "modules/mod_proxy.so"),
        ("proxy_connect_module", "modules/mod_proxy_connect.so"),
        ("proxy_ftp_module", "modules/mod_proxy_ftp.so"),
        ("proxy_http_module", "modules/mod_proxy_http.so"),
        ("proxy_ajp_module", "modules/mod_proxy_ajp.so"),
        ("proxy_balancer_module", "modules/mod_proxy_balancer.so"),
        ("ssl_module", "modules/mod_ssl.so"),
        ("mime_module", "modules/mod_mime.so"),
        ("autoindex_module", "modules/mod_autoindex.so"),
        ("dir_module", "modules/mod_dir.so"),
        ("alias_module", "modules/mod_alias.so"),
    ], allow_none=False)

    def addVirtualHost(self, name, ipaddress='0.0.0.0', port=80):
        """
        Create a VirtualHost

        @param name: Name of the virtual host, only needed to identify the virtual Host in the cmdb
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
            raise ValueError("A virtual host with name '%s' already exists" % \
                (name, )
            )

        vhostConfigDir = q.system.fs.joinPaths(self.configFileDir, self._vhostSubDir)
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

    def addJkWorker(self, name):
        """
        Add a Jk (mod_jk) worker

        @param name: name of the Jk worker
        @type name: string
        @return: the new Jk worker
        @rtype: JkWorker
        @raise ValueError: if a Jk worker with name already exists
        """
        if name in self.JkWorkers:
            raise ValueError("A Jk worker with name '%s' already exists" % \
                (name, )
            )

        jkWorker = JkWorker(name)
        self.JkWorkers[name] = jkWorker
        return jkWorker

    def addModule(self, name, filename):
        """
        Add an apache module to the list of loaded modules
        """
        if not q.system.fs.exists(q.system.fs.joinPaths(q.dirs.appDir, 'apache' , 'modules', q.system.fs.getBaseName(filename))):
            raise RuntimeError("Module %s does not exist or is not installed" % name)
        if (name, filename) in self.modules:
            raise ValueError('Module %s is already loaded'%name)
        mod = (name, filename)
        self.modules.append(mod)

    def removeModule(self,name):
        """
        Remove an apache module from the list of loaded modules
        """
        for item in self.modules:
            if name == item[0]:
                self.modules.remove(item)

    def listModules(self):
        """
        Return a list of loaded apache modules
        """
        return self.modules

    def removeJkWorker(self, name):
        """
        Remove a Jk worker

        @param name: name of the Jk worker
        @type name: string
        @raise KeyError: if Jk worker with name does not exist
        """
        del self.JkWorkers[name]

    def __str__(self):
        return "Apache Server '%s' Config" % (self.name, )

    def pm_cleanup(self):
        q.logger.log("Cleaning up apache config", 2)
        q.logger.log("Removing all vhost files", 3)
        vhostDir = q.system.fs.joinPaths(self.configFileDir, self._vhostSubDir)
        q.system.fs.removeDirTree(vhostDir)
        q.system.fs.createDir(vhostDir)
        q.logger.log("Cleanup done", 2)

    def pm_getModules(self):
        from collections import defaultdict
        # Due to dependencies, the order of the modules must be respected
        # Defaultdict contains a default value for any key. This default value
        # is defined by the method passed to the constructor. In this case we
        # pass 'int', which means the default value is 0.
        processingOrder = defaultdict(int)
        #python
        processingOrder["python_module"] = 1
        #php
        processingOrder["php5_module"] = 2
        #tomcat
        processingOrder["jk_module"] = 3
        #svn
        processingOrder["dav_module"] = 4
        processingOrder["dav_svn_module"] = 5
        processingOrder["authz_svn_module"] = 6
        #webdav
        processingOrder["dav_fs_module"] = 7

        site_modules = dict()
        for vhost in self.virtualHosts.values():
            for site in vhost.sites.values():
                if not site.modules:
                    continue

                for moduleName, module in site.modules.iteritems():
                    site_modules[moduleName] = module

        def getOrder(key):
            return processingOrder[key]

        sortedKeys = sorted(site_modules.keys(), key=getOrder)
        # Copy modules list
        modules = list(self.modules)
        defaultModuleNames = [moduleTuple[0] for moduleTuple in modules]
        for moduleName in sortedKeys:
            if moduleName in defaultModuleNames:
                continue
            modules.append((moduleName, site_modules[moduleName]))

        return modules

    def pm_write(self):
        """
        Write the configuration to disk

        @return: full path of the config file that was written to disk
        @rtype: string
        """
        q.logger.log("Writing new configuration to disk", 2)
        self.pm_cleanup()

        includes = list()
        q.logger.log("Writing vhost configs", 3)
        for vhostName, vhost in self.virtualHosts.iteritems():
            fileName = vhost.pm_write()
            includeName = "%s/%s/%s" % (self._configSubDir, self._vhostSubDir, fileName)
            includes.append(includeName)

        q.logger.log("Writing JkWorkers", 3)
        jkDir = q.system.fs.joinPaths(self.configFileDir, self._jkSubDir, "")
        jkWorkers = JkWorkers(self.JkWorkers.values(), jkDir)
        hasWorkers = bool(self.JkWorkers)
        jkWorkersFileName = "%s/%s/%s" % (
            self._configSubDir,
            self._jkSubDir,
            jkWorkers.pm_write()
        )

        q.logger.log("Writing main config file", 3)
        template = HttpdTemplate()
        context = {
            "serverName": self.name,
            "pidFile": self.pidFile,
            "apacheUser": self.apacheUser,
            "apacheGroup": self.apacheGroup,
            "serverRoot": self.serverRoot,
            "documentRoot": self.documentRoot,
            "includes": includes,
            "extra": self.extraConfigFile,
            "complexConfig": parseComplexConfig(self.complexConfig),
            "hasWorkers": hasWorkers,
            "jkWorkersFileName": jkWorkersFileName,
            "modules": self.pm_getModules(),
        }

        if not q.system.fs.isDir(self.configFileDir):
            q.system.fs.createDir(self.configFileDir)

        configFile = q.system.fs.joinPaths(self.configFileDir, self.configFileName)
        q.system.fs.writeFile(configFile, template.render(context))

        if not q.system.fs.exists(self.documentRoot):
            q.system.fs.createDir(self.documentRoot)

        if not q.system.fs.exists(q.system.fs.joinPaths(self.documentRoot, 'status')):
            q.system.fs.writeFile(q.system.fs.joinPaths(self.documentRoot, 'status'), 'RUNNING')

        return configFile

class HttpdTemplate(Template):
    template = """ServerRoot $serverRoot

#for $moduleName, $module in $modules
LoadModule $moduleName $module
#end for

# basic configuration
ServerName "$serverName"
PidFile $pidFile

<IfModule !mpm_winnt_module>
<IfModule !mpm_netware_module>
    User $apacheUser
    Group $apacheGroup
</IfModule>
</IfModule>

LogLevel error
ErrorLog ../../var/log/apache/error.log

<IfModule log_config_module>
    #
    # The following directives define some format nicknames for use with
    # a CustomLog directive (see below).
    #
    LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\"" combined
    LogFormat "%h %l %u %t \\"%r\\" %>s %b" common

    <IfModule logio_module>
      # You need to enable mod_logio.c to use %I and %O
      LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\" %I %O" combinedio
    </IfModule>

    #
    # The location and format of the access logfile (Common Logfile Format).
    # If you do not define any access logfiles within a <VirtualHost>
    # container, they will be logged here.  Contrariwise, if you *do*
    # define per-<VirtualHost> access logfiles, transactions will be
    # logged therein and *not* in this file.
    #
    CustomLog ../../var/log/apache/access.log common

    #
    # If you prefer a logfile with access, agent, and referer information
    # (Combined Logfile Format) you can use the following directive.
    #
    #CustomLog logs/access.log combined
</IfModule>

DefaultType text/plain

<IfModule mime_module>
    TypesConfig conf/mime.types
    #AddType application/x-gzip .tgz
    #AddEncoding x-compress .Z
    #AddEncoding x-gzip .gz .tgz
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    #AddHandler cgi-script .cgi
    AddHandler send-as-is asis
    #AddHandler imap-file map
    #AddHandler type-map var
    AddType text/html .shtml .html
    # AddHandler mod_python .py
    # PythonHandler index
    # PythonDebug On
    #AddOutputFilter INCLUDES .shtml
    AddType application/x-httpd-php .php
</IfModule>

# Do we need this

<IfModule ssl_module>
SSLRandomSeed startup builtin
SSLRandomSeed connect builtin
</IfModule>

# TODO VERY INSECURE!!! Must be removed when we
# introduce proper authentication and authorization
# Except for crossdomain.xml which should be fetchable without authentication
DocumentRoot "$documentRoot"
<Directory />
    Options FollowSymLinks
    AllowOverride None
    Order deny,allow
    Deny from all
</Directory>
#is this needed
<Directory "/opt/qbase3/www">
        Allow from all
</Directory>

#if $hasWorkers
# mod_jk stuff start, maybe move to seperate file?
LoadModule jk_module   modules/mod_jk.so
JkWorkersFile          $jkWorkersFileName
JkShmFile              /opt/qbase3/var/log/apache/mod_jk.shm
JkLogFile              /opt/qbase3/var/log/apache/mod_jk.log
JkLogLevel             info
JkLogStampFormat       "[%a %b %d %H:%M:%S %Y] "
#end if

# Extra configuration files from other vapps
#for $include in $includes
Include $include
#end for

#if $extra
# Extra config
Include $extra
#end if

#for $item in $complexConfig
$item
#end for
"""


class VirtualHostTemplate(Template):
    template = """Listen $port

<VirtualHost $ipaddress:$port>

#for $siteConfig in $siteConfigs
    $siteConfig
#end for

#if $proxies
    <Proxy *>
        Order deny,allow
        Deny from all
    </Proxy>
#end if

#for $proxy in $proxies
    <Proxy $proxy.address:$proxy.port>
        Order allow,deny
        #if $proxy.allowedHosts
            #for $allowedHost in $proxy.allowedHosts
                Allow from $allowedHost
            #end for
        #else
            Allow from all
        #end if
    </Proxy>
#end for

#for $reverseproxy in $reverseproxies

ProxyPass $reverseproxy.path $reverseproxy.url
ProxypassReverse $reverseproxy.path $reverseproxy.url
#end for

#for $item in $complexConfig
$item
#end for
</VirtualHost>
"""

class JkWorkerTemplate(Template):
    template = """
# Define 1 real worker using ajp13
#for $worker in $workers
worker.list=$worker.name
#end for

#for $worker in $workers
# Set properties for $worker.name ($worker.type)
worker.${worker.name}.type=$worker.type
worker.${worker.name}.host=$worker.hostname
worker.${worker.name}.port=$worker.port

#end for
"""
