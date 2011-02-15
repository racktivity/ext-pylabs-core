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

import sys
import time

from pylabs.InitBase import q

from pylabs.qpackages.common.DomainObject import DomainObject
from pylabs.qpackages.common.VLists import VLists

from pylabs.qpackages.server.Users import Users
from pylabs.qpackages.server.DomainACL import DomainACL

''' Setup domain '''
def setupDomain(domain):
    if not q.system.fs.exists(q.dirs.packageDir):
        q.system.fs.createDir(q.dirs.packageDir)
    q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.packageDir, domain))
    domain = DomainObject(domain)
    return domain

def removeDomain(domain):
    # remove domainfiles in packagedir
    path = q.system.fs.joinPaths(q.dirs.packageDir, str(domain))
    q.system.fs.removeDirTree(path)
    #remove domain files in cfg/qpackagedomains
    path = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackagedomains', str(domain))
    q.system.fs.removeDirTree(path)
    # remove vlists for domain
    path = q.system.fs.joinPaths(q.dirs.cfgDir, 'vlists', str(domain))
    q.system.fs.removeDirTree(path)

def setupUser(domain):
    u = Users()
    if u.exists('test'):
        u.removeUser('test')
    u.addUser('test', 'test')
    domainacl = DomainACL(domain)
    if domainacl.exists('test'):
        domainacl.removePermission('test')
    domainacl.addPermission('test', 'RW')

def removeUser(domain):
    domainacl = DomainACL(domain)
    domainacl.removePermission('test')
    u = Users()
    u.removeUser('test')
    
def createVlists(domain):
        vl = VLists('server')
        vl.createVLists(str(domain))

def testQPackageCreate(name, version, domain):
    v = q.qpackages.qpackageCreate(name, version, str(domain))
    v.addSupportedPlatform('generic')
    q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.packageDir, v.getRelativeBuildPath('trunk'), 'test', 'generic'))
    q.system.fs.createEmptyFile(q.system.fs.joinPaths(q.dirs.packageDir, v.getRelativeBuildPath('trunk'), 'test', 'generic', 'test.txt'))
    q.qpackages.syncToQPackageServer(v.name, v.version, str(domain), qualityLevel='trunk')
    return True

try:
    q.qpackages.qpackageServerConnections.qpackageServerConnectionAdd('unittest.pylabs.org', '192.168.11.114', domains=['unittest.pylabs.org',], port=8088, login='test', password='test')
except (ValueError): # pass the error if it already exists
    pass
q.qpackages.qpackageServerConnections.refresh()
# connect to the QPackageServer

conn = q.qpackages.qpackageServerConnections.getConnectionFromDomain('unittest.pylabs.org')
if not conn.isConnected():
    conn.connect()
''' Test to create a QPackage '''
if not testQPackageCreate('test_qpackage_%s'%int(time.time()), '1.3.1','unittest.pylabs.org'):
    raise RuntimeError('could not create the test qpackage')
q.console.echo('Test successfull')