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

import functools

from twisted.python import usage, log
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.internet import reactor
from zope.interface import implements


class Options(usage.Options):
    optParameters = [
        ['config', 'c', None, 'path of applicationserver configuration file'],
    ]



class ApplicationserverServiceFactory(object):
    implements(IPlugin, IServiceMaker)
    tapname = 'applicationserver'
    description = 'The pylabs Applicationserver'
    options = Options

    def makeService(self, options):
        #Local import to defeat pylabs logging threading issues
        from pylabs.InitBaseCore import q

        from applicationserver import Controller
        from applicationserver.config import IniConfigReader
        from applicationserver.pylabs_bindings import setup
        setup()

        if not options['config']:
            raise RuntimeError('No configuration name specified')
        config_reader = IniConfigReader(options['config'])

        controller = Controller(config_reader)

        services = controller()

        #Expose the controller XMLRPC resource on the first XMLRPC service we
        #find
        self.registerController(controller, services)

        return services

    def registerController(self, controller, services):
        from twisted.web import xmlrpc
        from applicationserver.controller import ControllerXMLRPCResource

        resource = ControllerXMLRPCResource(controller)

        #Hook on all XMLRPC servers we got
        for service in services:
            server = service.args[1]
            #TODO Magic string
            if getattr(server, 'PROTOCOL_NAME', None) == 'xmlrpc':
                log.msg('[PMBINDINGS] Hooking controller XMLRPC service')
                server._xmlrpc_transport.putSubHandler('_controller', resource)


serviceMaker = ApplicationserverServiceFactory()