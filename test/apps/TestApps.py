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

'''Unittests for apps'''

import tempfile
import time
import pylabs
from pylabs import pylabsTestCase
from pylabs.apps import Apps, PMApp


class TestApps(pylabsTestCase):


    def test_createapps(self):
        '''Test PMApps instanciation'''
        apps = Apps()
        self.assert_(apps)
        
#    def test_addapps(self):
#        '''Test adding a application to the apps'''
#        apps = Apps()
#        app = PMApp()
#        app.name="test"
#        app.starttime = time.time()
#        app.processname = '/usr/bin/sleep'
#        app.processid = pylabs.q.system.process.executeAsync(app.processname,['10'])
#        apps.addApp(app)
    
#    def test_getApp(self):
#        '''Test getting a app from the apps list'''
#        self.test_addapps()
#        self.assert_(self.apps.getApp("test"))
        

#    def test_saveApps(self):
#        '''Test saving apps in the pmdb''' 
#        self.test_addapps()
#        self.apps._saveApps()
#         ###manually check if apps exist:
#        self.assert_(q.pmdb.getObject("Apps"))
        
#    def test_loadApps(self):
#        '''Load apps from the the pmdb'''
#        self.test_saveApps()
#        self.assert_(apps.loadFromPmdb())
        
#    def test_removeApp(self):
#        '''Remove a app from the apps'''
#        self.test_addapps()
#        self.apps.removeApp("test")
#        self.assertRaises(KeyError,self.apps.getApp("test"))
        
#    def test_getAppState(self):
#        self.test_addapps()
#        testApp = self.apps.getApp("test")
#        self.assertEquals(testApp.status, PMAppType.RUNNING)      
    
#    def test_shutdownApp(self):
#        '''Shutdown app which have been started'''
#        self.test_addapps()
#        testapp = self.apps.getApp("test")
#        testapp.shutdown()
#        self.assertEquals(testapp.status, PMAppType.RUNNING)
#        time.sleep(2)
#        self.assertEquals(testapp.status, PMAppType.HALTED)
         
#    def test_killApp(self):
#         '''Kill App which has been started'''
#         self.test_addapps()
#         testapp = self.apps.getApp("test")
#         testapp.kill()
#         self.assertEquals(testapp.status, PMAppType.HALTED)