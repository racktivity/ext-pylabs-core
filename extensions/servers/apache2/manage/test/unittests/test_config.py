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
 
import re

from pylabs.testing import pylabsTestCase
from pylabs.InitBase import q

join = q.system.fs.joinPaths

"""
Unit tests for the Apache manage extension.

Please make sure all module files are installed (php, python, ...)
"""

class ApacheServerConfigTest(pylabsTestCase):
    apacheDir = join(q.dirs.appDir, "apache")
    apacheConfigDir = join(apacheDir, "conf")

    def setUp(self):
        pylabsTestCase.setUp(self)
        cmdb = q.manage.apache.cmdb
        self._defaults = dict()
        attrs = ('name', 'configFileDir', 'configFileName', 'extraConfigFile',
            'documentRoot', 'pidFile', 'apacheUser', 'apacheGroup',
            'serverRoot', 'complexConfig', 'virtualHosts', 'JkWorkers')
        for name in attrs:
            self._defaults[name] = getattr(cmdb, name)

        if q.manage.apache.cmdb.virtualHosts:
            raise Exception
        if q.manage.apache.cmdb.JkWorkers:
            raise Exception

    def assertExists(self, fileName):
        assert(q.system.fs.isFile(fileName), "File not found: '%s'" % fileName)

    def setupConfigDir(self):
        configDir = q.system.fs.joinPaths(q.dirs.tmpDir, "apacheConfig")
        # Move generated configs to tmp dir
        q.manage.apache.startChanges()
        q.manage.apache.cmdb.configFileDir = configDir
        q.manage.apache.cmdb.save()
        return configDir

    def apachectl(self, configDir):
        # apachectl binary
        apachectl = q.system.fs.joinPaths(self.apacheDir, "bin", "apachectl")
        # backup real apache config
        backupDir = join(self.apacheDir, "conf_backup")
        if q.system.fs.isDir(self.apacheConfigDir):
            q.system.fs.moveDir(self.apacheConfigDir, backupDir)
            backedUp = True
        else:
            backedUp = False
        try:
            # set our generated config there
            q.system.fs.copyDirTree(configDir, self.apacheConfigDir)
            # call apachectl
            exitcode, stdout, stderr = q.system.process.run(
                "%s configtest" % (apachectl, ),
                stopOnError=False,
            )
            print "----------------------"
            print stdout
            print "----------------------"
            print stderr
            print "----------------------"
        finally:
            if exitcode:
                # Use with -s flag so stdout is printed
                import pdb
                pdb.set_trace()
            q.system.fs.removeDirTree(self.apacheConfigDir)
            if backedUp:
                q.system.fs.moveDir(backupDir, self.apacheConfigDir)

        self.assert_(exitcode == 0)

    def assertContains(self, clause, content, message=None):
        if not message:
            message = "\"%s\" not found" % (clause, )
        self.assert_(clause in content, message)

    def assertNotContains(self, clause, content, message=None):
        if not message:
            message = "\"%s\" found" % (clause, )
        self.assert_(clause not in content, message)

    def assertRegexSearch(self, pattern, data, message, flags=0):
        match = re.search(pattern, data, flags)
        self.assert_(match, message)
        return match

    def tearDown(self):
        pylabsTestCase.tearDown(self)
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb

        for name, value in self._defaults.iteritems():
            setattr(cmdb, name, value)

        for virtualHost in cmdb.virtualHosts:
            cmdb.removeVirtualHost(virtualHost)

        for jkWorker in cmdb.JkWorkers:
            cmdb.removeJkWorker(jkWorker)

        cmdb.save()

class TestApacheServerSimple(ApacheServerConfigTest):
    def test_apacheServer(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        q.manage.apache.cmdb.name = "TestServer"
        q.manage.apache.cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        httpdFile = q.system.fs.joinPaths(configDir, "httpd.conf")
        assert(q.system.fs.isFile(httpdFile))

        self.apachectl(configDir)

    def test_vHost(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        q.manage.apache.cmdb.name = "TestServer"
        q.manage.apache.cmdb.addVirtualHost("TestVhost", "1.2.3.4", 1234)
        q.manage.apache.cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        httpdFile = q.system.fs.joinPaths(configDir, "httpd.conf")
        self.assertExists(httpdFile)

        fileName = q.manage.apache.cmdb.virtualHosts["TestVhost"].pm_getFileName()
        vhostFile = q.system.fs.joinPaths(
            configDir,
            q.manage.apache.cmdb._vhostSubDir,
            fileName
        )
        self.assertExists(vhostFile)

        self.apachectl(configDir)

        q.manage.apache.cmdb.removeVirtualHost("TestVhost")

class TestApacheServerNotSoSimple(ApacheServerConfigTest):
    def test_sites(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        q.manage.apache.cmdb.name = "TestServer"
        q.manage.apache.cmdb.addVirtualHost("TestVhost", "1.2.3.4", 1234)
        siteTypes = {
            'html': q.enumerators.ApacheSiteType.HTML,
            'php': q.enumerators.ApacheSiteType.PHP,
            'python': q.enumerators.ApacheSiteType.PYTHON,
            # No dav_svn .so
            #'svn': q.enumerators.ApacheSiteType.SVN,
            # Tomcat requires a worker, testing that in another test
            #'tomcat': q.enumerators.ApacheSiteType.TOMCAT,
            'webdav': q.enumerators.ApacheSiteType.WEBDAV,
        }
        for siteTypeName, siteType in siteTypes.iteritems():
            q.manage.apache.cmdb.virtualHosts["TestVhost"].addSite(
                "TestSite%s" % siteTypeName,
                siteType,
            )
        q.manage.apache.cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        httpdFile = q.system.fs.joinPaths(configDir, "httpd.conf")
        self.assertExists(httpdFile)

        fileName = q.manage.apache.cmdb.virtualHosts["TestVhost"].pm_getFileName()
        vhostFile = q.system.fs.joinPaths(
            configDir,
            q.manage.apache.cmdb._vhostSubDir,
            fileName
        )
        self.assertExists(vhostFile)

        self.apachectl(configDir)

        # Test PHP
        phpDirectory = self._getDirectory(configDir, "TestVhost", "TestSitephp")
        self.assertContains("DirectoryIndex index.php", phpDirectory)

    def test_extraConfig(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        q.manage.apache.cmdb.name = "TestExtraConfig"
        q.manage.apache.cmdb.extraConfigFile = "conf/extra.conf"
        q.manage.apache.cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        extraConfigFile = join(configDir, "extra.conf")
        q.system.fs.writeFile(extraConfigFile, "# Empty extra config\n")

        self.apachectl(configDir)

        # Check if the extra config is included
        httpdConf = q.system.fs.fileGetContents(join(configDir, "httpd.conf"))
        self.assertContains(
            "Include %s\n" % (q.manage.apache.cmdb.extraConfigFile, ),
            httpdConf
        )

    def test_complexConfigList(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb
        cmdb.name = "TestComplexConfig"
        cmdb.complexConfig["ServerName"] = ["\"COMPLEX_%d\"" % number for number in range(1, 4)]
        cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        self.apachectl(configDir)

        httpdConf = self._getHttpdConf(configDir)
        numbered_items = ["ServerName %s\n" % item for item in cmdb.complexConfig["ServerName"]]
        for item in numbered_items:
            self.assertContains(item, httpdConf)

    def test_sslUseCase(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb
        cmdb.name = "TestComplexConfig"
        cmdb.addVirtualHost("sslconnection", "0.0.0.0", 443)
        ssl = cmdb.virtualHosts["sslconnection"]
        ssl.complexConfig["SSLVerifyClient"] = "none"
        ssl.complexConfig["SSLVerifyDepth"] = 10
        # The following files are not (always) present but need to be for
        # apachectl to pass
        #ssl.complexConfig["SSLCertificateKeyFile"] = "/opt/qbase3/apps/openvpn/keys/SystemCustomer.key"
        #ssl.complexConfig["SSLCertificateFile"] = "/opt/qbase3/apps/openvpn/keys/SystemCustomer.crt"
        #ssl.complexConfig["SSLCACertificateFile"] = "/opt/qbase3/apps/openvpn/keys/ca.crt"
        ssl.complexConfig["SSLEngine"] = "on"

        ssl.addSite("publicsdk", q.enumerators.ApacheSiteType.TOMCAT, location="/opt/qbase3/tomcat/webapps/publicsdk")
        ssl.sites["publicsdk"].worker = "worker1"
        # Need a worker for the Tomcat site to work
        cmdb.addJkWorker("worker1")
        cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        self.apachectl(configDir)

        vhostConf = self._getVhostConf(configDir, "sslconnection")
        print vhostConf
        self.assertContains("SSLVerifyClient none", vhostConf)
        self.assertContains("JkMount /publicsdk/* worker1", vhostConf)

    def test_siteComplexConfig(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb
        cmdb.name = "TestSiteComplexConfig"
        cmdb.addVirtualHost("TestSite", "127.0.0.1", 80)
        test = cmdb.virtualHosts["TestSite"]
        test.addSite("complex", q.enumerators.ApacheSiteType.HTML)
        complex = test.sites["complex"]
        complex.complexConfig["BrowserMatch"] = [
            '"Microsoft Data Access Internet Publishing Provider" redirect-carefully',
            '"MS FrontPage" redirect-carefully',
            '"^WebDrive" redirect-carefully',
        ]
        cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        self.apachectl(configDir)

        vhostConf = self._getVhostConf(configDir, "TestSite")
        print vhostConf
        self.assertContains('BrowserMatch "^WebDrive" redirect-carefully', vhostConf)

    def test_tomcatUseCase(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb
        cmdb.name = "TestTomcat"
        cmdb.addJkWorker("worker1")
        cmdb.addVirtualHost("connection", "0.0.0.0", 22000)
        connection = cmdb.virtualHosts["connection"]
        connection.addSite("publicsdk", q.enumerators.ApacheSiteType.TOMCAT, location="/opt/qbase3/tomcat/webapps/publicsdk")
        connection.sites["publicsdk"].worker = "worker1"
        cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        self.apachectl(configDir)

        jkFileName = q.system.fs.joinPaths(configDir, cmdb._jkSubDir, "workers.properties")
        self.assertExists(jkFileName)
        jkConf = q.system.fs.fileGetContents(jkFileName)
        self.assertContains("worker1", jkConf)

        vhostConf = self._getVhostConf(configDir, "connection")
        self.assertContains("worker1", vhostConf)

        # Expand with 2 extra workers
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb
        cmdb.addJkWorker("worker2")
        cmdb.addJkWorker("worker3")
        # TODO: changes .worker to .workers? So we can add multiple workers
        cmdb.addVirtualHost("connection2", "127.0.0.1", 22001)
        connection2 = cmdb.virtualHosts["connection2"]
        connection2.addSite("publicsdk2", q.enumerators.ApacheSiteType.TOMCAT)
        connection2.sites["publicsdk2"].worker = "worker3"
        cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        self.apachectl(configDir)

        self.assertExists(jkFileName)
        jkConf = q.system.fs.fileGetContents(jkFileName)
        for workerName in ("worker1", "worker2", "worker3"):
            self.assertContains(workerName, jkConf)

        vhostConf1 = self._getVhostConf(configDir, "connection")
        self.assertContains("worker1", vhostConf1)
        self.assertNotContains("worker2", vhostConf1)
        self.assertNotContains("worker3", vhostConf1)

        vhostConf2 = self._getVhostConf(configDir, "connection2")
        self.assertNotContains("worker1", vhostConf2)
        self.assertNotContains("worker2", vhostConf2)
        self.assertContains("worker3", vhostConf2)

    def test_multipleWorkers(self):
        configDir = self.setupConfigDir()
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb
        cmdb.name = "TestMultipleWorkers"
        cmdb.addJkWorker("worker3")
        cmdb.addVirtualHost("directconnection", "0.0.0.0", 22000)
        connection = cmdb.virtualHosts["directconnection"]
        connection.complexConfig["JkMount /appserver/rest/*"] = "worker3"
        connection.complexConfig["JkMount /appserver/vpdcws/*"] = "worker3"
        connection.complexConfig["JkMount /appserver/xmlrpc/*"] = "worker3"
        cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        self.apachectl(configDir)

    def test_acl(self):
        configDir = self.setupConfigDir()
        # Use a dummy location
        location = configDir
        username = "testuser"
        q.manage.apache.startChanges()
        cmdb = q.manage.apache.cmdb
        cmdb.name = "Test ACL"
        aclhost = cmdb.addVirtualHost("aclhost", "0.0.0.0", 433)
        aclsite = aclhost.addSite("aclsite", q.enumerators.ApacheSiteType.HTML, location)
        aclsite.addACL(username, "testpassword")
        cmdb.save()
        q.manage.apache.applyConfig(restart=False)

        # Will also test if it can find the ACL file
        self.apachectl(configDir)

        # Contruct ACL file name
        aclFileDir = aclhost.pm_getACLDir()
        aclFileName = aclsite.pm_getACLFileName(aclFileDir)

        # Test if the ACL config in in the vhost config, between the site directory tags
        dirContent = self._getDirectory(configDir, aclhost.name, aclsite.name)
        print "Dir content:---------------------"
        print dirContent
        print "---------------------------------"
        self.assertRegexSearch("AuthType\s+Basic", dirContent, "AuthType config not found")
        self.assertRegexSearch("AuthName\s+\"Sun\"", dirContent, "AuthName config not found")
        self.assertRegexSearch("AuthUserFile\s+.*aclhost.*aclsite", dirContent, "AuthUserFile config not found")
        self.assertRegexSearch("Require\s+valid-user", dirContent, "Valid user requirement not found")
        # Test if the user is in the ACL file
        aclContent = q.system.fs.fileGetContents(aclFileName)
        self.assertRegexSearch(
            "^%s:" % (username, ),
            aclContent,
            "Username '%s' not found in ACL file '%s'" % (username, aclFileName)
        )
        # TODO Test if the Order is set correctly
        # Test if the read/write mode is set correctly
        # TODO

    def _getHttpdConf(self, configDir):
        return q.system.fs.fileGetContents(join(configDir, "httpd.conf"))

    def _getVhostConf(self, configDir, name):
        fileName = q.manage.apache.cmdb.virtualHosts[name].pm_getFileName()
        path = join(configDir, q.manage.apache.cmdb._vhostSubDir, fileName)
        return q.system.fs.fileGetContents(path)

    def _getDirectory(self, configDir, vhostName, siteName):
        vhostConf = self._getVhostConf(configDir, vhostName)
        site = q.manage.apache.cmdb.virtualHosts[vhostName].sites[siteName]
        pattern = '<Directory "%s">(.*)</Directory>' % (site.location, )
        match = re.search(pattern, vhostConf, re.DOTALL)
        self.assert_(match, "Could not find relevant Directory configuration")
        return match.group(1)