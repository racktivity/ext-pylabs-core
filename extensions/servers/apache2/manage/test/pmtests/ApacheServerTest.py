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
 
from pymonkey.InitBase import *

import urllib2
import time

m = q.manage.apache
a = q.manage.apache.cmdb

sleepTime = 4

def initializeEnvironment():
    q.action.start('initialize environment -> fill httpd.conf defaults')
    a.initDone = False
    m.init()
    time.sleep(sleepTime)
    q.action.stop()

def checkURL(url, usr=None, pwd=None):
    q.action.start('validating site access')
    if usr == None and pwd == None:
        info = urllib2.urlopen(url)
    else:
        auth = urllib2.HTTPBasicAuthHandler()
        authRes = auth.add_password("Qlayer", "127.0.0.1", usr,pwd)
        o = urllib2.build_opener(auth)
        info = o.open(url)
    q.action.stop()

def checkURLWrongCredentials(url):
    q.action.start('validating site access with wrong credentials')
    try:
        auth = urllib2.HTTPBasicAuthHandler()
        authRes = auth.add_password("Qlayer", "127.0.0.1", "wrong","wrong")
        o = urllib2.build_opener(auth)
        info = o.open(url)
        raise RuntimeError("Test failed : Accessing site with wrong credentials should not be allowed !")
    except:
        return "DONE"


    q.action.stop()


def clearSites():
    q.action.start('Removing all currently configured sites')
    for siteName in m.listSiteNames():
        a.deleteSite(siteName)

    m.applyConfig()
    time.sleep(sleepTime)
    q.action.stop()

def createHTMLSite():
    q.action.start('Check creation of HTML site')
    htmlUrl = "http://www.apachewrapper.org/htmltest"
    htmlsite = a.addSite(htmlUrl,q.enumerators.ApacheSiteType.HTML)
    m.applyConfig()    
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/htmltest")
    q.action.stop()

def createHTML_ACL(): 
    q.action.start('Check setting ACL on HTML site')
    htmlsite = a.sites['http://www.apachewrapper.org/htmltest']
    htmlsite.addACL('html','html')
    m.applyConfig()
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/htmltest", "html", "html")
    print checkURLWrongCredentials("http://127.0.0.1/htmltest")
    q.action.stop()

def createPHPSite():
    q.action.start('Check creation of PHP site')
    phpUrl = "http://www.apachewrapper.org/phptest"
    phpsite = a.addSite(phpUrl, q.enumerators.ApacheSiteType.PHP)
    m.applyConfig()    
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/phptest")
    q.action.stop()

def createPHP_ACL(): 
    q.action.start('Check setting ACL on PHP site')
    phpsite = a.sites['http://www.apachewrapper.org/phptest']
    phpsite.addACL('php','php')
    m.applyConfig()
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/phptest", "php", "php")
    print checkURLWrongCredentials("http://127.0.0.1/phptest")
    q.action.stop()

def createSVNSite():
    q.action.start('Check creation of SVN site')
    svnUrl = "http://www.apachewrapper.org/svntest"
    svnsite = a.addSite(svnUrl, q.enumerators.ApacheSiteType.SVN)
    m.applyConfig()
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/svntest/repo")
    q.action.stop()

def createSVN_ACL(): 
    q.action.start('Check setting ACL on SVN site')
    svnsite = a.sites['http://www.apachewrapper.org/svntest']
    svnsite.addACL('svn','svn')
    m.applyConfig()
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/svntest/repo", "svn", "svn")
    print checkURLWrongCredentials("http://127.0.0.1/svntest")
    q.action.stop()    


def createPythonSite():
    q.action.start('Check creation of Python site')
    pythonUrl = "http://www.apachewrapper.org/pythontest"
    pythonsite = a.addSite(pythonUrl, q.enumerators.ApacheSiteType.PYTHON)
    m.applyConfig()
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/svntest/repo", "svn", "svn")
    q.action.stop()

def createPyhton_ACL():
    q.action.start('Check setting Python on SVN site')
    pythonsite = a.sites['http://www.apachewrapper.org/pythontest']
    pythonsite.addACL('py','py')
    m.applyConfig()
    time.sleep(sleepTime)
    print checkURL("http://127.0.0.1/pythontest/index.py", "py", "py")
    print checkURLWrongCredentials("http://127.0.0.1/pythontest/index.py")
    q.action.stop()


q.application.appname = "Apache PMTest"
q.application.start()

initializeEnvironment()

clearSites()

createHTMLSite()
createHTML_ACL()

createPHPSite()
createPHP_ACL()

createSVNSite()
createSVN_ACL()

createPythonSite()
createPyhton_ACL()

clearSites()

q.application.stop()