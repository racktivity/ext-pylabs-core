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

import pymonkey

from twisted.web import xmlrpc
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import xmlrpclib

#from servers.common.PMXMLRPCServer import PMXMLRPCServer
#from servers.common.Server import Server
#from servers.common.ServerStatus import ServerStatus

class XMLRPCServer(object):
    """
    generic implementation of xmlrpc server based on twisted
    just inherit your server class from XMLRPCServer
    for example see WFEServer class implementation
    """
    def __init_properties__(self):
        """ Definition of the attributes of this class """
        self._reactor=None #twisted reactor
        self.cfgManagementObject=None ##CfgManagementApplicationXMLRPC #class inherited from CfgManagementApplicationXMLRPC
        self.allowedMethods=[] ##array(string) #array of all methods which will be exposed
        #@todo implement authentication mechanism (cred)
        
    def __init__(self,cfgManagementObject):
        """
        @param is object which has to server as server for XMLRPC
        """
        self.__init_properties__()
        self.cfgManagementObject=cfgManagementObject
        #start generic XMLRPC server, every method called will be forwarded to self (if allowed, means part of allowedMethods)
        self.serverPort=5555 ##int #port on which xmlrpc server will run
        
    def start(self):
        self.xmlRPCServer.allowedMethods=self.allowedMethods
        self._reactor= reactor.listenTCP(self.serverPort, server.Site(self.cfgManagementObject))
        reactor.run()