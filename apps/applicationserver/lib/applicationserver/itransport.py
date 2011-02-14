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
 
'''Transport interface definitions for applicationserver transports'''

import operator

from zope.interface import Interface, Attribute, implements

from twisted.web import server

class ITransportFactory(Interface):
    '''Transport interface for an applicationserver trasport'''
    OPTIONS = Attribute('''
        Options accepted by the transport constructor

        @type: type
        @notice: Currently not used''')
    PROTOCOL = Attribute('''
        Name of the protocol

        This should be unique.
        
        @type: string''')

    def createTransport(dispatcher, configuration):
        '''Create a transport instance using the provided configuration

        @param configuration: Kwargs for the transport constructor
        @type configuration: dict

        @return: Transport instance
        @rtype: L{ITransport}
        '''
        pass


class ITransport(Interface):
    '''Implementation of an applicationserver transport'''
    def stopService():
        '''Stop the service'''

    def getTransportInfo(name):
        '''Get a TransportInfo object for this transport instance

        @param name: Name of the transport as specified in the configuration
        @type name: string

        @return: Transport info for the transport instance
        @rtype: L{ITransportInfo}'''

class IServerTransport(ITransport):
    '''Implementation of an applicationserver transport which is a server
    transport

    Server transports listen on some port to handle requests (eg. XMLRPC,
    REST,...). This is in contrast with non-server transports like an
    email-based transport which provide no server themself'''
    def getTransportInfo(name, info):
        '''Get a TransportInfo object for this transport instance

        @param name: Name of the transport as specified in the configuration
        @type name: string
        @param info: Transport connection information (as parsed by
                     twisted.application.strports.parse). This is based on the
                     'transport' configuration options.

                     Example:
                         ('TCP', (8080, <transport>),
                             {'backlog': 50, 'interface': '192.168.0.1'})
        @type info: tuple

        @return: Transport info for the transport instance
        @rtype: L{ITransportInfo}'''


class ITransportInfo(Interface):
    '''Interface for transport information classes'''
    PROTOCOL = Attribute('''
        Name of the transport/protocol

        This should be the same as the C{PROTOCOL} attribute of the
        L{ITransport} implementation corresponding to this
        C{ITransportInfo type.

        @type: string''')

    name = Attribute('''
        Name of the transport in the configuration

        @type: string''')

class TransportInfo(object):
    '''Base L{ITransportInfo} implementation

    Note this is an abstract implementation, subclasses should at least provide
    the C{PROTOCOL} attribute as specified by the L{ITransportInfo} interface.
    '''
    implements(ITransportInfo)

    def __init__(self, name):
        self._name = name

    name = property(operator.attrgetter('_name'), doc='Transportname')

    def __str__(self):
        return '<%s Transport %s>' % (self.PROTOCOL, self.name)


class ServerTransportInfo(TransportInfo):
    '''Base L{ITransportInfo} abstract base class for real server transports

    These servers expose an C{ipaddress} and C{port} attribute.

    Note this is an abstrace class: subclasses need to provide the C{PROTOCOL}
    attribute as specified by the L{ITransportInfo} interface.
    '''
    def __init__(self, name, info):
        super(ServerTransportInfo, self).__init__(name)

        config = info[2]
        self._ipaddress = config['interface'] or '0.0.0.0'
        self._port = info[1][0]

    ipaddress = property(operator.attrgetter('_ipaddress'),
        doc='IP address the transport listens on')
    port = property(operator.attrgetter('_port'),
        doc='TCP port the transport listens on')

    def __str__(self):
        return '<%s Transport %s @ %s:%d>' % (self.PROTOCOL, self.name,
                self.ipaddress, self.port)


class SiteTransport(server.Site):
    '''Utility class for transports which use L{twisted.web.server.Site}

    This utility class already implements L{IServerTransport}, but this is an
    abstract implementation since subclasses need to set a
    C{TRANSPORT_INFO_CLASS} attribute which points to the
    L{IServerTransportInfo} type for the transport. It is constructed using the
    constructor parameters of L{ServerTransportInfo}.
    '''
    implements(IServerTransport)

    def getTransportInfo(self, name, info):
        return self.TRANSPORT_INFO_CLASS(name, info)