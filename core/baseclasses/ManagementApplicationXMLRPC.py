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

from pymonkey.baseclasses.ManagementApplication import ManagementApplication
import pymonkey
from twisted.web import xmlrpc
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import xmlrpclib
import pickle


class CfgManagementApplicationXMLRPC(CfgManagementApplication):
    """
    management base class for server or application (only 1, for more apps use: CfgManagementApplicationGroup)
    add methods for start, stop, ...
    exposed over XMLRPC (has to be put in XMLRPC Server)
    """
    allowNone=True    
    def __init_properties__(self):
        """ Definition of the attributes of this class """
        CfgAppManagementClass.__init_properties__(self)
        self.status=ApplicationStatus.UNKNOWN      ##ApplicationStatus: RUNNING, UNKNOWN, ... #@todo 
        self.cmdb=None     ##CMDBApplicationObject #one CMDB object who describe configuration of an app or daemon (only manages one application, multiple instances can be active)

    
    def __init__(self, object):
        self.allowedMethods=[]
        self.wrapped = object
        #call parents
        CfgManagementApplication.__init_properties__(self)
        CfgManagementApplication.__init__(self)


    def __getattr__(self, attrname):
        #@todo my trick does not work with twisted, twisted does not use this function when xmlrpc server is called, see how we can get this to work
        #this method get's calledd if attribute or method does not exist
        pymonkey.q.logger.log( "XMLRPC CALL: %s" % attrname)    
        #@todo more checks & logging, which server do we wrap, which method called, more sanity checks
        found=False
        if "xmlrpc_"==attrname[0:7]:
            for method in self.allowedMethods:
                if "xmlrpc_%s"%method==attrname:
                    pymonkey.q.logger.log("XMLRPC SERVER calls method %s on class %s" % (method,self.wrapped.__class__))
                    try:
                        result=getattr(self.wrapped, method)
                    except:
                        print "could not execute"
                        pymonkey.q.application.stop()
                    found=True

                    def _result():
                        result_obj = result()
                        pickled_result = pickle.dumps(result_obj)
                        return pickled_result

                    return _result       # Delegate fetch to original class and pickle before returning
            if found==False:
                #@todo have to find cleaner way of populating errors from server to client, do event mgmt, not just logging
                pymonkey.q.logger.log( "ERROR in XMLRPCSERVER: call was %s, could not find allowed method, check if method is allowed in server." % (attrname))
                print ( "ERROR in XMLRPCSERVER: call was %s, could not find allowed method, check if method is allowed in server." % (attrname))
                pymonkey.q.application.stop()
                return xmlrpclib.Fault(7, "Could not find required method %s" % attrname)