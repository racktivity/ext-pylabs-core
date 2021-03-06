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
 
from twisted.plugin import IPlugin
from twisted.cred import portal, checkers
from twisted.conch import manhole, manhole_ssh

from zope.interface import implements

import applicationserver
from applicationserver.itransport import ITransportFactory, IServerTransport
from applicationserver.itransport import ServerTransportInfo

# Twisted Manhole/Conch are 'quite' underdocumented, you're on yourself here

class SSHTransportFactory(object):
    implements(IPlugin, ITransportFactory)

    OPTIONS = None
    PROTOCOL = 'ssh'

    def createTransport(self, dispatcher, configuration):
        realm = manhole_ssh.TerminalRealm()

        def get_manhole(_):
            namespace = {
                    'dispatcher': applicationserver.dispatcher,
                    'crond': applicationserver.crond,
            }
            if hasattr(applicationserver, 'controller'):
                namespace['controller'] = applicationserver.controller

            return manhole.ColoredManhole(namespace)

        realm.chainedProtocolFactory.protocolFactory = get_manhole

        p = portal.Portal(realm)
        p.registerChecker(
                checkers.InMemoryUsernamePasswordDatabaseDontUse(**{
                    configuration['user']: configuration['password'],
                }
            )
        )
        f = ConchTransport(p)

        return f

ssh_transport = SSHTransportFactory()


class SSHTransportInfo(ServerTransportInfo):
    '''TransportInfo for the SSH transport'''
    PROTOCOL = SSHTransportFactory.PROTOCOL


class ConchTransport(manhole_ssh.ConchFactory):
    implements(IServerTransport)

    def getTransportInfo(self, name, info):
        return SSHTransportInfo(name, info)