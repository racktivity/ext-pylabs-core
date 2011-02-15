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

import pylabs


class Apps:
    """
    Store known applications.
    #@ttodo make sure we modify application.start() to populate this apps list
    """
    pmapps = None ##dict(appname,PMApp)

    def checkStatus(self):
        """Check the status of all running pylabs applications

        Look at running processes, match them against the known pylabs
        applications and change the status accordingly.
        """
        for app in self.pmapps.values():
            app.state

    def __iter__(self):
        #Allows us to do
        # for app in PMApps:
        #     app.doFoo()
        for i in self.pmapps.itervalues():
            yield i

    def listPrint(self):
        """
        Same function as the function C{list} but with a nice format for usage in Q-Shell
        """
        for app in self.pmapps.itervalues():
            pylabs.q.console.echo( app.name, app.state)
            
    def addApp(self,app):
        '''Add an application to the pylabs applications dictionary'''
        self.pmapps[app.name] = app
        
    def removeApp(self,appname):
        '''Remove an application from the pylabs applications dictionary'''
        self.pmapps.pope(appname)

    def getApp(self,appname):
        """
        Return the appropriate pylabs application
        """
        return self.apps[appname]
        
    @staticmethod
    def loadFromPmdb():
        '''Load the list of applications from the pylabs database'''
        try:
            apps = pylabs.q.cmdb.getObject("Apps")
        except RuntimeError:
            apps = Apps()
        return apps
        
    def _save(self):
        """
        Save the changes to the pylabs database
        """
        pylabs.q.cmdb.registerObjectType("Apps")
        pylabs.q.cmdb.saveObject('Apps', self)