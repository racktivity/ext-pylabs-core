from pylabs import q
from pylabs.baseclasses.CMDBServerObject import CMDBServerObject
from EjabberdUser import EjabberdUser
from EjabberdModule import EjabberdModule
from EjabberdListeningPort import EjabberdListeningPort
from EjabberdTrafficShapper import EjabberdTrafficShaper
from EjabberdAccessRule import EjabberdAccessRule
from EjabberdACL import EjabberdACL
import os
import socket

class EjabberdCmdb(CMDBServerObject):
    def setRestartRequired(self, value):
        self.dirtyProperties.add('restartRequired')
        yield value

    cmdbtypename = 'ejabberd'
    users = q.basetype.dictionary(doc='dictionary of registered users', default=dict(), allow_none=True, flag_dirty=True)
    ejabberdUser = q.basetype.string(default='ejabberd', allow_none=True, fset=setRestartRequired, flag_dirty=True)
    nodeName = q.basetype.string(doc='fully qualified dns name of the node', default=socket.getfqdn(), allow_none=False, fset=setRestartRequired, flag_dirty=True)
    
    configFile = q.basetype.filepath(doc='Config file of ejabberd', default=q.system.fs.joinPaths(os.sep, 'etc','ejabberd','ejabberd.cfg'), flag_dirty=True, fset=setRestartRequired,)
    ctlCfgFile = q.basetype.filepath(doc='Config file of ejabberdctl', default=q.system.fs.joinPaths(os.sep, 'etc','ejabberd','ejabberdctl.cfg'), flag_dirty=True, fset=setRestartRequired,)
    logsDir = q.basetype.dirpath(doc='directory of logs', default=q.system.fs.joinPaths(os.sep, 'var', 'log', 'ejabberd'), fset=setRestartRequired, flag_dirty=True)
    spoolDir = q.basetype.dirpath(doc='database spool dir', flag_dirty=True, fset=setRestartRequired)

    logLevel = q.basetype.integer(doc='loglevel',default=4, fset=setRestartRequired, flag_dirty=True)
    #%% loglevel: Verbosity of log files generated by ejabberd.
    #%% 0: No ejabberd log at all (not recommended)
    #%% 1: Critical
    #%% 2: Error
    #%% 3: Warning
    #%% 4: Info
    #%% 5: Debug

    hosts = q.basetype.list(doc='Domains served by ejabberd', default=list(), flag_dirty=True)
    #{hosts, ["dmachine.office.aserver.com"]}

    modules = q.basetype.dictionary(doc="Modules in all ejabberd virtual hosts", default=dict(), flag_dirty=True)
    defaultLanguage = q.basetype.string(doc='Default language used for server messages', default='en', flag_dirty=True, fset=setRestartRequired,)
    accessRules = q.basetype.dictionary(doc='Dictionary of access rules', default=dict(), flag_dirty=True)
    acls = q.basetype.dictionary(doc='access control list', default=dict(), flag_dirty=True)
    trafficShapers= q.basetype.dictionary(doc='traffic shaper', default=dict(), flag_dirty=True)
    listeningPorts = q.basetype.dictionary(doc='Which ports will ejabberd listen, which service handles it', default=dict(), flag_dirty=True)

    initDone = q.basetype.boolean(default=False)

    def __init__(self):

        CMDBServerObject.__init__(self)

        if not self.spoolDir:
            self.spoolDir = q.system.fs.joinPaths(os.sep, 'var', 'lib', 'ejabberd')#, 'db', str(self.nodeName))

    def addHost(self, hostname):
        """
        Add host to the hosts list
        """
        if hostname in self.hosts:
            raise ValueError("Host with name [%s] already exists" %hostname)
        self.hosts.append(hostname)
        self.dirtyProperties.add('restartRequired')
        q.logger.log("Host [%s] was Added" %hostname, 5)

    def removeHost(self, hostname):
        """
        Remove host from the hosts list
        """
        if hostname not in self.hosts:
            raise ValueError('Host with name [%s] does not exist'%hostname)
        q.logger.log("Deleting Host [%s]"%hostname, 5)

        self.hosts.pop(self.hosts.index(hostname))
        self.dirtyProperties.add('restartRequired')

    def addListeningPort(self, serviceName, port, options):
        """
        Add listening port
        Which ports will ejabberd listen, which service handles it
        and what options to start it with.
        """
        if port in self.listeningPorts:
            raise ValueError("Port [%s] already exists" %port)
        listeningport = EjabberdListeningPort()
        listeningport.name = serviceName
        listeningport.port = port
        listeningport.options = options
        self.listeningPorts[port] = listeningport
        q.logger.log("Port [%s] was added with service [%s]" %(port, serviceName), 5)
        self.dirtyProperties.add('restartRequired')
        return listeningport

    def removeListeningPort(self, port):
        """
        Remove listening port
        """
        if port in self.listeningPorts:
            self.listeningPorts.pop(port)
            self.dirtyProperties.add('restartRequired')
        else:
            raise ValueError('Port [%s] does not exist'%port)

    def addTrafficShaper(self, shaperName, options):
        """
        Add traffic shaper
        """
        shaper = EjabberdTrafficShaper()
        shaper.name = shaperName
        shaper.options = options
        self.trafficShapers[shaperName] = shaper
        self.dirtyProperties.add('restartRequired')
        q.logger.log('Added traffic shaper with name [%s] and options [%s]'%(shaperName, options), 5)
        return shaper

    def removeTrafficShaper(self, shaperName):
        """
        Remove traffic shaper
        """
        if shaperName not in self.trafficShapers:
            raise ValueError('Traffic shaper with name [%s] does noe exist'%shaperName)
        self.trafficShapers.pop(shaperName)
        self.dirtyProperties.add('restartRequired')

    def addUser(self, name, server, password):
        """
        Add a user to the dict of users.
        @param name: name of the user to register
        @param server: name of the server to add the user to
        @param password: password of the user to register
        """
        if name in self.users:
            raise ValueError('User with name [%s] already exists'%name)
        user = EjabberdUser()
        user.name = name
        user.server = server
        user.password = password
        self.users[name] = user
        self.dirtyProperties.add('users')
        return user

    def removeUser(self, name):
        """
        Mark the user as removed.
        @param name: name of the user to unregister
        @param server: name of the server to unregister the user from
        """
        if name not in self.users:
            raise ValueError('User with name [%s] does not exist'%name)
        self.users[name]._removed = True
        self.dirtyProperties.add('users')

    def addModule(self, name, options=list(), enabled=True):
        """
        Add module to dictionary of modules
        """
        if name in self.modules:
            raise ValueError('Module with name [%s] already exists'%name)
        module = EjabberdModule()
        module.name = name
        module.options = options
        module.enabled = enabled
        self.modules[name] = module
        self.dirtyProperties.add('restartRequired')
        return module

    def removeModule(self, name):
        """
        remove module
        """
        if name not in self.modules:
            raise ValueError('Module with name [%s] does not exist'%name)
        self.modules.pop(name)
        self.dirtyProperties.add('restartRequired')

    def enableModule(self, name):
        """
        enable a module
        """
        if name not in self.modules:
            raise ValueError('Module with name [%s] does not exist'%name)
        self.modules[name].enabled = True
        self.dirtyProperties.add('restartRequired')

    def disableModule(self, name):
        """
        disable Module
        """
        if name not in self.modules:
            raise ValueError('Module with name [%s] does not exist'%name)
        self.modules[name].enabled = False
        self.dirtyProperties.add('restartRequired')

    def addAccessRule(self, name, options):
        """
        Add access rule
        """
        if name in self.accessRules:
            raise ValueError('Access rule with name [%s] already exists'%name)
        accessrule = EjabberdAccessRule()
        accessrule.name = name
        accessrule.options = options
        self.accessRules[name] = accessrule
        self.dirtyProperties.add('restartRequired')
        return accessrule

    def removeAccessRule(self, name):
        """
        Remove Access Rule
        """
        if name not in self.accessRules:
            raise ValueError('Access rule with name [%s] does not exist'%name)
        self.accessRules.pop(name)
        self.dirtyProperties.add('restartRequired')

    def addACL(self, name, options=""):
        """
        Add Access Control List (ACL) to the acls dict
        @param name: name of the ACL to be added
        @param options: ACL options
        """
        if name in self.acls:
            raise ValueError('ACL with name [%s] already exists'%name)
        acl = EjabberdACL()
        acl.name = name
        acl.options = options
        self.acls[name] = acl
        self.dirtyProperties.add('restartRequired')
        return acl

    def removeACL(self, name):
        """
        Remove Acces Control list (ACL) from the acls dict
        @param name: name of ACL to be removed
        """
        if name not in self.acls:
            raise ValueError('ACL with name [%s] does not exist'%name)
        self.acls.pop(name)
        self.dirtyProperties.add('restartRequired')
