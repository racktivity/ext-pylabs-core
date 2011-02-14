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
 
'''Applicationserver controller/main application implementation'''

import sys
import types
import operator

from twisted.internet import reactor, defer
from twisted.application import service, internet, strports
from twisted.web import xmlrpc
from twisted.plugin import getPlugins
from twisted.python import log

import applicationserver
import applicationserver.utils
from applicationserver.itransport import ITransportFactory, ITransport
from applicationserver.itransport import ITransportInfo, IServerTransport
from applicationserver.config import IConfigReader
import applicationserver.transports
from applicationserver.services import ServiceContext, is_context_handler, \
        is_service_close_handler

class ServiceLoadException(Exception):
    '''Exception raised when loading a service class fails

    This could eg. be due to a missing service module, a failing import, a
    SyntaxError in the module,...
    '''


class TransportInfoContainer(set):
    '''Container for TransportInfo objects'''

'''TransportInfo container'''
transportinfo = TransportInfoContainer()


class Controller(object):
    '''Main application controller

    This class can be used as a main object for the whole applicationserver
    application. It loads configuration data, sets up transports and
    configures the dispatcher and crond services.
    '''
    def __init__(self, config_reader):
        '''Initialize a controller instance

        @param config_reader: Configuration reader to use
        @type config_reader: L{applicationserver.config.IConfigReader}
        '''
        self.status = 'INITIALIZING'
        # Our configuration reader
        self.config_reader = IConfigReader(config_reader)
        # Transports registered on the server
        # These are services (L{twisted.application.service.IService})
        self.registered_transports = dict()
        # Services registered on the server
        self.registered_services = dict()
        # Mapping between transport names and their TransportInfo descriptions
        self.transport_info_map = dict()
        # Mapping between service names and their context objects
        self.service_contexts = dict()

        # This is somewhat tricky. We Want to mount 'self', which should be the
        # only Controller instance throughout the process, on the
        # applicationserver module so externals can import/use it.
        #
        #applicationserver.controller is normally a module, so ignore that case
        if hasattr(applicationserver, 'controller') \
                and not isinstance(applicationserver.controller,
                                   types.ModuleType):
            raise RuntimeError(
                'Package \'applicationserver\' has a \'controller\' attribute')
        applicationserver.controller = self
        log.msg('[CONTROLLER] Initialization done')

    def __call__(self):
        '''Start the controller

        Calling the controller object reads configuration information, sets up
        transports and loads all services.
        '''
        log.msg('[CONTROLLER] Starting controller')
        self.transports = service.MultiService()

        self.reload()
        
        self.status = 'RUNNING'

        return self.transports

    def loadConfig(self):
        '''Load configuration data'''
        log.msg('[CONTROLLER] Loading configuration')
        self.config = self.config_reader.parseConfig()

    def reload(self):
        '''Reload all transports and services'''
        log.msg('[CONTROLLER] Reloading')
        self.loadConfig()
        self.loadTransports()
        self.loadServices()

    def loadTransports(self):
        '''Load all transports'''

        def helper(name, config, transport_names):
            # Helper closure passed to / called by L{_loadItemsFromConfig}
            # This will keep track of configured transports in transport_names
            # and set up a transport if applicable
            transport_names.add(name)

            # If this transport (or another with this name, which would be a
            # configuration error) is already registered, just ignore this
            # configuration item
            if name in self.registered_transports:
                return None

            log.msg('[CONTROLLER] Configuring transport %s' % name)
            # Create a transport (L{ITransport}) using the given configuration
            transport = self.loadTransport(name, config)

            # If the transport is an L{IServerTransport}...
            if IServerTransport.providedBy(transport):
                # Create a L{twisted.application.service.IService} from it
                # using settings provided in C{config}. This is *not* an
                # applicationserver  service but a Twisted service, ie a 
                # server handling incoming requests on a given socket.
                service = self.hookTransport(transport, config)
                # Set the IService name
                service.setName(name)
                # Set the IService parent to our MultiTransport
                service.setServiceParent(self.transports)

                # Parse the transport settings again so we can set up an
                # L{ITransportInfo} object for this transport
                port_info = strports.parse(config['transport'], transport)
                transport_info = transport.getTransportInfo(name, port_info)
                # Store the L{ITransportInfo}
                self.transport_info_map[name] = transport_info

                # Finally return the service
                return service
            else:
                # Set up the L{ITransportInfo} for the transport
                transport_info = transport.getTransportInfo(name)
                # Save it
                self.transport_info_map[name] = transport_info

                # And return it. We don't know how to handle this further,
                # since this is not an L{IServerTransport}, most likely the
                # 'mail' transport.
                return transport

        log.msg('[CONTROLLER] Loading transports')
        # Store names of all enabled transports, so we can disable transports
        # which were removed from the configuration later
        enabled_transport_names = set()
        # Load all items starting with 'transport_' from the configuration,
        # pass then to C{helper}, and also pass the registered transport
        # container, and the name container
        self._loadItemsFromConfig('transport_', helper,
                self.registered_transports, enabled_transport_names)

        #Disable all transports which are no longer enabled
        # We need to iterate through a copy of the original dict since we'll
        # modify the original one while iterating.
        for name, transport in self.registered_transports.copy().iteritems():
            if name not in enabled_transport_names:
                log.msg('[CONTROLLER] Disable transport %s' % name)
                # Remove the service from our C{MultiService}
                self.transports.removeService(transport)
                # Remove the transport from our registered transport map
                self.registered_transports.pop(name)
                # And remove the corresponding L{ITransportInfo}
                self.transport_info_map.pop(name)

        #Update transportinfo
        transportinfo.clear()
        #Add all transport info objects to the set
        #This is something like
        #
        # for info in self.transport_info_map.itervalues():
        #     transportinfo.add(info)
        #
        #but shorter and faster
        map(transportinfo.add, self.transport_info_map.itervalues())

    def loadServices(self):
        '''Load all services'''
        def helper(name, config, service_names):
            # Similar to the helper closure in loadTransports: called for every
            # applicable configuration item, keeps track of configured services
            # and loads new services when necessary
            #
            # Store service name
            service_names.add(name)

            # Ignore if this is a 'known' service
            if name in self.registered_services:
                return None

            log.msg('[CONTROLLER] Configuring service %s' % name)
            # Load the service
            service = self.loadService(name, config)
            # Handle it to the dispatcher
            applicationserver.dispatcher.addService(name, service)
            # Handle it to crond
            applicationserver.crond.addService(name, service)
            # And return it
            return service

        log.msg('[CONTROLLER] Loading services')
        # Similar to loadTransports
        enabled_service_names = set()
        self._loadItemsFromConfig('service_', helper, self.registered_services,
                enabled_service_names)

        #Disable all services which are no longer enabled
        # Also similar to loadTransports
        for name, service in self.registered_services.copy().iteritems():
            if name not in enabled_service_names:
                log.msg('[CONTROLLER] Disable service %s' % name)
                applicationserver.dispatcher.removeService(name, service)
                applicationserver.crond.removeService(name, service)
                self.registered_services.pop(name)
                self.service_contexts.pop(name)

    def _loadItemsFromConfig(self, prefix, callback, container, *args,
                             **kwargs):
        '''Load all items from configuration with a name starting with a prefix

        For every configuration item found with a name starting with C{prefix},
        the provided callback method is called, and the result value of this
        operation is stored in C{container}, which should be a dictionary
        containig <name, value> pairs.

        Any args or kwargs are passed to the callback function.

        @param prefix: Configuration item prefix to filter
        @type prefix: string
        @param callback: Callable to run for every configuration item found
        @type callback: callable(name, config_data)
        @param container: Container to store C{callback} results
        @type container: dict<string, object>
        '''
        # Loop through all configuration items
        for name, config in self.config.iteritems():
            # If it doesn't match our prefix...
            if not name.startswith(prefix):
                # ... ignore it (for now)
                continue

            # Name is the part after the prefix
            name = name[len(prefix):]

            # Call the helper method with the configuration item name and data,
            # and provide any extra arguments provided to this method
            value = callback(name, config, *args, **kwargs)
            # Finally, store the value returned by the helper in the container
            # provided to us, if any
            #TODO We might want to do this in the helper
            if container is not None and value:
                container[name] = value

    def loadTransport(self, name, config):
        '''Load a transport from given configuration data

        @param name: Transport name
        @type name: string
        @param config: Transport configuration parameters
        @type config: dict
        '''
        #TODO Don't use a dict as config input, parse to values?

        log.msg('[CONTROLLER] Looking up transport %s' % name)

        # First we need to get a list of all known transports, using the
        # Twisted plugin infrastructure
        #We can re-call getPlugins since this caches on-disk
        known_transports = getPlugins(ITransportFactory,
                                      applicationserver.transports)

        # Retrieve the factory for the required protocol
        factory = None
        for factory_ in known_transports:
            if factory_.PROTOCOL == config['protocol']:
                factory = factory_
                break

        # If not found, something is very wrong
        if not factory:
            raise RuntimeError('No transport found for protocol %s' % \
                    config['protocol'])

        log.msg('[CONTROLLER] Found factory for transport %s' % name)
        # Fetch transport configuration options
        # Use an empty C{dict} if none configured
        options = config['options'] or dict()
        # Finally, let the factory create a transport instance
        log.msg('[CONTROLLER] Calling factory for transport %s' % name)
        handler = factory.createTransport(applicationserver.dispatcher,
                                          options)

        # Cast to an ITransport, just to be on the safe side
        handler = ITransport(handler)

        #TODO Magic constant
        handler.PROTOCOL_NAME = config['protocol']

        return handler

    def hookTransport(self, transport, config):
        '''Create a L{twisted.application.internet.Service} for a transport

        Given a transport and some configuration data, a
        L{twisted.application.internet.Service} object is created to actually
        run a server.

        @param transport: Transport to hook to the service
        @type transport: twisted.internet.protocol.ServerFactory
        @param config: Service configuration data
        @type config: dict<string, string>

        @returns: A service exposing the transport on a configured channel
        @rtype: twisted.internet.interfaces.IListeningPort
        '''
        # Get the configuration string
        # This is something like
        #
        #     tcp:8080:interface=127.0.0.1
        #
        # See the documentation of L{twisted.application.strports} for an
        # overview
        port = config['transport']

        log.msg('[CONTROLLER] Hooking transport on %s' % port)

        # Let Twisted create a service from our transport based on the
        # transport configuration string
        return strports.service(port, transport)

    def loadService(self, name, config):
        '''Load a service and create a service instance

        @param name: Service name
        @type name: string
        @param config: Service configuration data
        @type config: dict<string, string>

        @return: Service instance
        @rtype: object
        '''
        log.msg('[CONTROLLER] Loading service %s' % name)

        try:
            # Load the class from its module
            # Yes, this variable is called klass and not class, which is rather
            # impossible in Python.
            klass = applicationserver.utils.getClass(name, config['class'])
        except Exception, ex:
            if ':' not in config['class']:
                raise ValueError("Invalid classpath %s: no ':' found" % \
                                 config['class'])
            raise ServiceLoadException('Could not load service %s: ' \
                                   'failed to import class %s from file %s\n' \
                                   'ERROR:%s' % (name,
                                                 config['class'].split(':')[1],
                                                 config['class'].split(':')[0],
                                                 ex))

        # Create and return an instance of the service class
        # We provide constructor arguments from the configuration (the
        # 'options' part of the configuration dict) or an empty C{dict} if not
        # set or empty.
        #
        # If you don't know the ** syntax:
        #
        #     func(**({'a': 123, 'b': 456}))
        #
        # would be the same as
        #
        #     func(a=123, b=456)
        #
        log.msg('[CONTROLLER] Got service class, creating instance')
        service = klass(**(config['options'] or dict()))

        service_context = ServiceContext(name=name)
        self.service_contexts[name] = service_context
        self._setServiceContext(service, service_context)

        return service
    
    def removeService(self, name):
        '''Removes a service
        
        @param name: Service name
        @type name: string
        '''
        log.msg('[CONTROLLER] Removing service %s' % name)
        
        service = self.registered_services[name]
        
        applicationserver.dispatcher.removeService(name, service)
        applicationserver.crond.removeService(name, service)
        
        self.registered_services.pop(name)
        self.service_contexts.pop(name)
        
        close_handlers = set()
        for attrname in dir(service):
            attr = getattr(service, attrname)
            if callable(attr) and is_service_close_handler(attr):
                log.msg('[CONTROLLER] Found service close handler %s ' \
                        'on service %s, scheduling' % (attrname, name))
                close_handlers.add(attr)

        return defer.DeferredList([defer.maybeDeferred(handler) for handler in close_handlers])
    
    def startService(self, name, config):
        '''Loads and start a service
        '''
        # load application again
        service = self.loadService(name, config)
        applicationserver.dispatcher.addService(name, service)
        # Handle it to crond
        applicationserver.crond.addService(name, service)
        
        self.registered_services[name] = service
        

    @staticmethod
    def _setServiceContext(service, context):
        '''Call all methods tagged as C{context_handler} on a service

        Every method which got the required attribute set will be called
        passing the context as single argument.

        @param service: Service to initialize
        @type service: object
        @param context: Context to provide
        @type context: L{ServiceContext}
        '''
        for attrname in dir(service):
            attr = getattr(service, attrname)

            if callable(attr) and is_context_handler(attr):
                log.msg('[CONTROLLER] Found context handler %s ' \
                        'on service %s, calling' % (attrname, context.name))
                attr(context)

    def stop(self):
        '''Stop the server'''
        log.msg('[CONTROLLER] Preparing server shutdown')
        self.status = 'STOPPING'

        def _stop():
            log.msg('[CONTROLLER] Stopping reactor')
            reactor.stop()
            self.status = 'NOT_RUNNING'

        # Stop the reactor one second after calling this method
        # We need to do this delayed, since this call could come from a service
        # method, eg through XMLRPC, which needs to return before the reactor
        # is stopped, otherwise the client could be very confused.
        return reactor.callLater(1, _stop)

    def _setStatus(self, status):
        if hasattr(self, '_status'):
            log.msg('[CONTROLLER] State changing from %s to %s' % \
                    (self._status, status))
        else:
            log.msg('[CONTROLLER] Setting initial status %s' % status)

        self._status = status

    status = property(fget=operator.attrgetter('_status'), fset=_setStatus,
                      doc='Controller status')


class ControllerXMLRPCResource(xmlrpc.XMLRPC):
    '''Twisted.web resource to expose a L{Controller} over XMLRPC

    This class exposes a given L{Controller} as a
    L{twisted.web.resource.Resource} implementing an XMLRPC service.
    '''
    def __init__(self, controller):
        '''Initialize a new XMLRLC resource

        This initializes a new XMLRPC resource to expose a given L{Controller}
        instance.

        @param controller: Controller to expose
        @type controller: Controller
        '''
        self.controller = controller

    @applicationserver.utils.authorization_local
    def xmlrpc_getName(self):
        '''XMLRPC method to stop the controller'''
        log.msg('[CONTROLLER_SERVICE] Server name requested')
        return self.controller.config['name']

    @applicationserver.utils.authorization_local
    def xmlrpc_stopServer(self):
        '''XMLRPC method to stop the controller'''
        log.msg('[CONTROLLER_SERVICE] Request to stop server')
        self.controller.stop()
        return True

    @applicationserver.utils.authorization_local
    def xmlrpc_getStatus(self):
        '''XMLRPC method to retrieve the controller status'''
        log.msg('[CONTROLLER_SERVICE] Server status requested')
        return self.controller.status

    @applicationserver.utils.authorization_local
    def xmlrpc_listServices(self):
        '''XMLRPC method to retrieve list of services'''
        log.msg('[CONTROLLER_SERVICE] Returning list of deployed services')
        srvs = dict()
        for name, config in self.controller.config.iteritems():
            if name.startswith('service_'):
                lname = '_'.join(name.split('_')[1:])
                if lname in self.controller.registered_services:
                    srvs[lname] = 'RUNNING'
                else:
                    srvs[lname] = 'NOT RUNNING'
        return srvs

    @applicationserver.utils.authorization_local
    def xmlrpc_reloadService(self, appName,targetRole='restart'):
        '''XMLRPC method to reload service'''
        log.msg('[CONTROLLER_SERVICE] reloading service %s' % appName)

        deferred = None
        
        # remove application from application server
        for name, config in self.controller.config.iteritems():
            cname = 'service_' + appName
            if name == cname:
                
                if targetRole in ('restart', 'stop', ):
                    if appName in self.controller.registered_services:
                        deferred = self.controller.removeService(appName)
                    
                def start(arg):
                    self.controller.startService(appName, config)
                    return arg
            
                if targetRole == 'restart' and deferred:
                    deferred.addBoth(start)
                    deferred.addCallbacks(lambda _: True, lambda _: False)
                    return deferred
            
                elif targetRole == 'start' or (targetRole == 'restart' and not deferred):
                    # TODO Make this async as well?
                    start(True)
                    return True
                

    @applicationserver.utils.authorization_local
    def xmlrpc_reloadConfig(self):
        '''XMLRPC method to reload the controller configuration'''
        log.msg('[CONTROLLER_SERVICE] Request to reload server configuration')
        self.controller.reload()

        return True
