from pylabs import q
from pylabs.baseclasses.ManagementApplication import ManagementApplication, CMDBLockMixin
from pylabs.enumerators import AppStatusType
from EjabberdCmdb import EjabberdCmdb

class EjabberdManage(ManagementApplication, CMDBLockMixin):

    cmdb = EjabberdCmdb()

    def start(self):
        """
        Start Ejabberd daemon
        """
        return q.cmdtools.ejabberd.start(self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)

    def stop(self):
        """
        Stop Ejabberd daemon
        """
        return q.cmdtools.ejabberd.stop(self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)

    def getStatus(self):
        """
        Get Status of Ejabberd daemon
        """
        return q.cmdtools.ejabberd.getStatus(self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)

    def restart(self):
        """
        Restart Ejabberd damon
        """
        return q.cmdtools.ejabberd.restart(self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)

    def printStatus(self):
        """
        Print the status of Ejabberd daemon
        """
        q.gui.dialog.message("EJabberd daemon is %s"%self.getStatus())

    def save(self):
        """
        Save the configuration in the cmdb
        """
        self.cmdb.save()
        self.cmdb.dirtyProperties.clear()

    def init(self):
        if self.cmdb.initDone:
            return
        print 'INIT'
        self.startChanges()
        #Add listening ports
        self.cmdb.addListeningPort('ejabberd_c2s', 5222, ['{access, c2s}', '{shaper, c2s_shaper}', '{max_stanza_size, 1048576}'])
        self.cmdb.addListeningPort('ejabberd_c2s', 5223, ['{access, c2s}', '{shaper, c2s_shaper}', '{certfile, "/etc/ejabberd/ejabberd.pem"}', 'tls', '{max_stanza_size, 1048576}'])
        #self.cmdb.addListeningPort('ejabberd_s2s_in', 5269, ['{shaper, s2s_shaper}', '{max_stanza_size, 131072}'])
        #self.cmdb.addListeningPort('ejabberd_http', 5280, ['http_poll', 'web_admin'])

        #Add Traffic Shapers
        self.cmdb.addTrafficShaper('normal', ['maxrate', '1048576'])
        self.cmdb.addTrafficShaper('fast', ['maxrate', '1048576'])
        

        #Add ACLs

        #Add Access Rules
        self.cmdb.addAccessRule('max_user_sessions', ['{10, all}'])
        self.cmdb.addAccessRule('local', ['{allow, local}'])
        self.cmdb.addAccessRule('c2s', ['{deny, blocked}', '{allow, all}'])
        self.cmdb.addAccessRule('c2s_shaper', ['{none, admin}', '{normal, all}'])
        #self.cmdb.addAccessRule('s2s_shaper', ['{fast, all}'])
        self.cmdb.addAccessRule('announce', ['{allow, admin}'])
        self.cmdb.addAccessRule('configure', ['{allow, admin}'])
        self.cmdb.addAccessRule('muc_admin', ['{allow, admin}'])
        self.cmdb.addAccessRule('muc', ['{allow, all}'])
        self.cmdb.addAccessRule('pubsub_createnode', ['{allow, all}'])
        #self.cmdb.addAccessRule('register', ['{allow, all}'])

        #Add Modules
        self.cmdb.addModule('mod_adhoc', [])
        self.cmdb.addModule('mod_announce', ["{access, announce}"])
        self.cmdb.addModule('mod_caps', [])
        self.cmdb.addModule('mod_configure', [])
        self.cmdb.addModule('mod_disco', [])
        #self.cmdb.addModule('mod_irc', [])
        self.cmdb.addModule('mod_last', [])
        self.cmdb.addModule('mod_muc', ['{access, muc}', '{access_create, muc}', '{access_persistent, muc}', '{access_admin, muc_admin}'])
        self.cmdb.addModule('mod_privacy', [])
        self.cmdb.addModule('mod_private', [])
        self.cmdb.addModule('mod_pubsub', ['{access_createnode, pubsub_createnode}', '{plugins, ["default", "pep"]}'])
        #self.cmdb.addModule('mod_register', ['{welcome_message, {"Welcome!", "Hi\nWelcome to this Jabber server."}}', '{access, register}'])
        self.cmdb.addModule('mod_roster', [])
        self.cmdb.addModule('mod_shared_roster', [])
        self.cmdb.addModule('mod_stats', [])
        self.cmdb.addModule('mod_time', [])
        self.cmdb.addModule('mod_vcard', [])
        self.cmdb.addModule('mod_version', [])


        self.cmdb.initDone = True

        self.save()

    def applyConfig(self):
        """
        apply configurations
        1. stops the server if configuration changed
        2. rewrite configuration file based on items saved in cmdb
        3. start the daemon
        4. register/unregister users
        """
        #Initialize cmdb with default data

        self.init()

        self.startChanges()
        if 'restartRequired' in self.cmdb.dirtyProperties:
            if self.getStatus() == AppStatusType.RUNNING:
                q.console.echo("Stopping Ejabberd before applying configuration")
                self.stop()
            q.console.echo("Writing new configuration file...")
            q.system.fs.writeFile(self.cmdb.configFile, self._buildConfigString())

        if not self.getStatus() == AppStatusType.RUNNING:
            self.start()

        #Register/unregister users
        users = dict()
        removeusers = []
        registerdUsers = self.listRegisteredUsers()
        for key,user in self.cmdb.users.iteritems():
            isRegistered = user.server in registerdUsers and user.name in registerdUsers[user.server]
            if user._removed:
                if isRegistered:
                    q.cmdtools.ejabberd.unregister(user.name, user.server, self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)
                removeusers.append(user.name)
                continue
            if not isRegistered:
                q.cmdtools.ejabberd.register(user.name, user.server, user.password, self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)
            users[key] = user
        for user in removeusers:
            print 'remove', removeusers
            print 'USER', user
            self.cmdb.users.pop(user)

        self.cmdb.dirtyProperties.clear()
        self.save()


    def listConnectedUsers(self):
        """
        Retrieves a list of all users connected to the server
        """
        return q.cmdtools.ejabberd.listConnectedUsers(self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)

    def listRegisteredUsers(self, hosts=list()):
        """
        Retrieves a list of users registered in given hosts. if no hosts are specified q.manage.ejabberd.cmdb.hosts will be used
        @param hosts: list of hosts to retrieve registered users
        """
        if hosts:
            hosts = hosts if isinstance(hosts, (list, tuple)) else [hosts] if hosts else None
        hosts = hosts or  self.cmdb.hosts
        registeredUsers = dict()
        for host in hosts:
            registeredUsers[host] = q.cmdtools.ejabberd.listRegisteredUsers(host, self.cmdb.nodeName if not self.cmdb.ejabberdUser else "%s@%s"%(self.cmdb.ejabberdUser, self.cmdb.nodeName), self.cmdb.configFile, self.cmdb.ctlCfgFile, self.cmdb.logsDir, self.cmdb.spoolDir)
        return registeredUsers


    def _buildConfigString(self):
        commentLine = '%%%%'
        configlines = '''%(commentLine)s
%(commentLine)s ejabberd configuration file


%(commentLine)s The parameters used in this configuration file are explained in more detail
%(commentLine)s in the ejabberd Installation and Operation Guide.
%(commentLine)s Please consult the Guide in case of doubts, it is included in
%(commentLine)s your copy of ejabberd, and is also available online at
%(commentLine)s http://www.process-one.net/en/ejabberd/docs/

%(commentLine)s This configuration file contains Erlang terms.
%(commentLine)s In case you want to understand the syntax, here are the concepts:
%(commentLine)s - The character to comment a line is
%(commentLine)s - Each term ends in a dot, for example:
%(commentLine)s     override_global.

%(commentLine)s - A tuple has a fixed definition, its elements are
%(commentLine)s   enclosed in {}, and separated with commas:
%(commentLine)s     {loglevel, 4}.

%(commentLine)s - A list can have as many elements as you want,
%(commentLine)s   and is enclosed in [], for example:
%(commentLine)s     [http_poll, web_admin, tls]
%(commentLine)s
%(commentLine)s - A keyword of ejabberd is a word in lowercase.
%(commentLine)s   The strings are enclosed in "" and can have spaces, dots...
%(commentLine)s     {language, "en"}.
%(commentLine)s     {ldap_rootdn, "dc=example,dc=com"}.

%(commentLine)s - This term includes a tuple, a keyword, a list and two strings:
%(commentLine)s     {hosts, ["jabber.example.net", "im.example.com"]}.


%(commentLine)s =======================
%(commentLine)s OVERRIDE STORED OPTIONS


%(commentLine)s Override the old values stored in the database.



%(commentLine)s Override global options (shared by all ejabberd nodes in a cluster).

%(commentLine)s override_global.


%(commentLine)s Override local options (specific for this particular ejabberd node).

%(commentLine)s override_local.


%(commentLine)s Remove the Access Control Lists before new ones are added.

%(commentLine)s override_acls.


%(commentLine)s =========
%(commentLine)s DEBUGGING


%(commentLine)s loglevel: Verbosity of log files generated by ejabberd.
%(commentLine)s 0: No ejabberd log at all (not recommended)
%(commentLine)s 1: Critical
%(commentLine)s 2: Error
%(commentLine)s 3: Warning
%(commentLine)s 4: Info
%(commentLine)s 5: Debug

{loglevel, %(loglevel)s}.


%(commentLine)s watchdog_admins: Only useful for developers: if an ejabberd process
%(commentLine)s consumes a lot of memory, send live notifications to these Jabber
%(commentLine)s accounts.

%(commentLine)s {watchdog_admins, ["bob@example.com"]}.


%(commentLine)s ================
%(commentLine)s SERVED HOSTNAMES


%(commentLine)s hosts: Domains served by ejabberd.
%(commentLine)s You can define one or several, for example:
%(commentLine)s {hosts, ["example.net", "example.com", "example.org"]}.

{hosts, %(hosts)s}.
%(commentLine)s ===============
%(commentLine)s LISTENING PORTS


%(commentLine)s listen: Which ports will ejabberd listen, which service handles it
%(commentLine)s and what options to start it with.

{listen,
 [
 %(listenPorts)s
]}.
%(commentLine)s ==============
%(commentLine)s AUTHENTICATION


%(commentLine)s auth_method: Method used to authenticate the users.
%(commentLine)s The default method is the internal.
%(commentLine)s If you want to use a different method,
%(commentLine)s comment this line and enable the correct ones.

{auth_method, internal}.


%(commentLine)s Authentication using external script
%(commentLine)s Make sure the script is executable by ejabberd.

%(commentLine)s {auth_method, external}.
%(commentLine)s {extauth_program, "/path/to/authentication/script"}.


%(commentLine)s Authentication using ODBC
%(commentLine)s Remember to setup a database in the next section.

%(commentLine)s {auth_method, odbc}.


%(commentLine)s Authentication using PAM

%(commentLine)s {auth_method, pam}.
%(commentLine)s {pam_service, "pamservicename"}.


%(commentLine)s Authentication using LDAP

%(commentLine)s {auth_method, ldap}.

%(commentLine)s List of LDAP servers:
%(commentLine)s {ldap_servers, ["localhost"]}.

%(commentLine)s LDAP attribute that holds user ID:
%(commentLine)s {ldap_uids, [{"mail", "u@mail.example.org"}]}.

%(commentLine)s Search base of LDAP directory:
%(commentLine)s {ldap_base, "dc=example,dc=com"}.

%(commentLine)s LDAP manager:
%(commentLine)s {ldap_rootdn, "dc=example,dc=com"}.

%(commentLine)s Password to LDAP manager:
%(commentLine)s {ldap_password, "******"}.


%(commentLine)s Anonymous login support:
%(commentLine)s auth_method: anonymous
%(commentLine)s anonymous_protocol: sasl_anon | login_anon | both
%(commentLine)s allow_multiple_connections: true | false

%(commentLine)s {host_config, "public.example.org", [{auth_method, anonymous},
%(commentLine)s                                     {allow_multiple_connections, false},
%(commentLine)s                                     {anonymous_protocol, sasl_anon}]}.

%(commentLine)s To use both anonymous and internal authentication:

%(commentLine)s {host_config, "public.example.org", [{auth_method, [internal, anonymous]}]}.


%(commentLine)s ==============
%(commentLine)s DATABASE SETUP

%(commentLine)s ejabberd uses by default the internal Mnesia database,
%(commentLine)s so you can avoid this section.
%(commentLine)s This section provides configuration examples in case
%(commentLine)s you want to use other database backends.
%(commentLine)s Please consult the ejabberd Guide for details about database creation.


%(commentLine)s MySQL server:

%(commentLine)s {odbc_server, {mysql, "server", "database", "username", "password"}}.

%(commentLine)s If you want to specify the port:
%(commentLine)s {odbc_server, {mysql, "server", 1234, "database", "username", "password"}}.


%(commentLine)s PostgreSQL server:

%(commentLine)s {odbc_server, {pgsql, "server", "database", "username", "password"}}.

%(commentLine)s If you want to specify the port:
%(commentLine)s {odbc_server, {pgsql, "server", 1234, "database", "username", "password"}}.

%(commentLine)s If you use PostgreSQL, have a large database, and need a
%(commentLine)s faster but inexact replacement for "select count(*) from users"

%(commentLine)s {pgsql_users_number_estimate, true}.


%(commentLine)s ODBC compatible or MSSQL server:

%(commentLine)s {odbc_server, "DSN=ejabberd;UID=ejabberd;PWD=ejabberd"}.


%(commentLine)s Number of connections to open to the database for each virtual host

%(commentLine)s {odbc_pool_size, 10}.


%(commentLine)s Interval to make a dummy SQL request to keep alive the connections
%(commentLine)s to the database. Specify in seconds: for example 28800 means 8 hours

%(commentLine)s {odbc_keepalive_interval, undefined}.


%(commentLine)s ===============
%(commentLine)s TRAFFIC SHAPERS


%(commentLine)s The "normal" shaper limits traffic speed to 1.000 B/s
%(shapers)s

%(commentLine)s ====================
%(commentLine)s ACCESS CONTROL LISTS


%(commentLine)s The 'admin' ACL grants administrative privileges to Jabber accounts.
%(commentLine)s You can put as many accounts as you want.

%(commentLine)s {acl, admin, {user, "aleksey", "localhost"}}.
%(commentLine)s {acl, admin, {user, "ermine", "example.org"}}.
%(commentLine)s

%(commentLine)s Blocked users

%(commentLine)s {acl, blocked, {user, "baduser", "example.org"}}.
%(commentLine)s {acl, blocked, {user, "test"}}.


%(commentLine)s Local users: don't modify this line.

{acl, local, {user_regexp, ""}}.


%(commentLine)s More examples of ACLs

%(commentLine)s {acl, jabberorg, {server, "jabber.org"}}.
%(commentLine)s {acl, aleksey, {user, "aleksey", "jabber.ru"}}.
%(commentLine)s {acl, test, {user_regexp, "^test"}}.
%(commentLine)s {acl, test, {user_glob, "test*"}}.


%(commentLine)s Define specific ACLs in a virtual host.

%(commentLine)s {host_config, "localhost",
%(commentLine)s [
%(commentLine)s  {acl, admin, {user, "bob-local", "localhost"}}
%(commentLine)s ]
%(commentLine)s }.
%(acls)s
%(commentLine)s ============
%(commentLine)s ACCESS RULES
%(accessrules)s

%(commentLine)s ================
%(commentLine)s DEFAULT LANGUAGE


%(commentLine)s language: Default language used for server messages.

{language, "%(defaultLanguage)s"}.

%(commentLine)s =======
%(commentLine)s MODULES


%(commentLine)s Modules enabled in all ejabberd virtual hosts.

{modules,
 [
 %(modules)s
 ]}.


%(commentLine)s Enable modules with custom options in a specific virtual host

%(commentLine)s {host_config, "localhost",
%(commentLine)s [{{add, modules},
%(commentLine)s   [
%(commentLine)s    {mod_echo, [{host, "mirror.localhost"}]}
%(commentLine)s   ]
%(commentLine)s  }
%(commentLine)s ]}.


%(commentLine)s $Id: ejabberd.cfg.example 1733 2008-12-16 17:39:05Z badlop $

%(commentLine)s Local Variables:
%(commentLine)s mode: erlang
%(commentLine)s End:
%(commentLine)s vim: set filetype=erlang tabstop=4:
'''%{'commentLine':commentLine, 'loglevel':self.cmdb.logLevel,'hosts':str(self.cmdb.hosts).replace("'", '"'), 'listenPorts':'\n'.join([str(port) for port in self.cmdb.listeningPorts.values()])[:-1], \
     'shapers':'\n'.join([str(shaper) for shaper in self.cmdb.trafficShapers.values()]), 'acls':'\n'.join([str(ace) for ace in self.cmdb.acls.values()]), \
     'accessrules':'\n'.join([str(rule) for rule in self.cmdb.accessRules.values()]),'defaultLanguage':self.cmdb.defaultLanguage, 'modules':'\n'.join([str(module) for module in self.cmdb.modules.values()])[:-1]}

        return configlines




