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
from pymonkey.config import *
from pymonkey import q


class SvnConnection(ConfigManagementItem):
    """
    Configuration of an svn connection.
    """


    # (MANDATORY) CONFIGTYPE and DESCRIPTION

    CONFIGTYPE = "svnconnection"
    DESCRIPTION = "Svn Connection"


    # MANDATORY IMPLEMENTATION OF ASK METHOD

    def ask(self):
        self.dialogAskString('url', 'SVN repository URL (e.g. http://trac.qlayer.com/svn/code/)')
        self.dialogAskString('branch', 'SVN branch', "trunk")
        login = self.dialogAskString('login', 'Username for SVN connection %s' % self.itemname)
        self.dialogAskPassword('passwd', 'Password for SVN connection %s' % self.itemname)


    #  OPTIONAL CUSTOMIZATIONS OF CONFIGURATION

    def show(self):
        """
        Optional customization of show() method
        """
        # Here we do not want to show the password, so a customized show() method
        q.gui.dialog.message("\nSvn Connection [%s]\n\n" % self.itemname +
                             "  URL:       %(url)s\n  Branch:    %(branch)s\n  Login:     %(login)s\n  Password:  *****" % self.params)

    def retrieve(self):
        """
        Optional implementation of retrieve() method, to be used by find()
        """
        try:
            svnConnection=pymonkey.q.clients.svn.createConnection(self.params['url'], self.params['branch'], self.params['login'], self.params['passwd'])
        except:
            pymonkey.q.logger.log(pymonkey.q.errorconditionhandler.getCurrentExceptionString())
            pymonkey.q.logger.log("Cannot login to url %s path %s with user %s" % (self.params['url'], self.params['branch'], self.params['login']))
            svnConnection=False
            pymonkey.q.console.echo("\n##################################################################################")          
            pymonkey.q.console.echo( "WARNING: Could not connect to SVN server. Please review settings for repo %s." % self.itemname)
            pymonkey.q.console.echo("\n##################################################################################")          
        return svnConnection


# Create configuration object for group of SvnConnections,
# and register it as an extension on i tree (using extension.cfg)
SvnConnections = ItemGroupClass(SvnConnection)

def findByUrl(self, url, branch):
    """
    Find svn connection based on url and branch, by using an automatically generated name.
    If connection cannot be found, generate a new one.
    """
    def normalize_name(url, branch):
        while url.endswith('/'):
            url = url[:-1]
        while branch.startswith('/'):
            branch = branch[1:]
        while branch.endswith('/'):
            branch = branch[:-1]
        name = url + '/' + branch + '/'
        target = ""
        for character in name:
            if character in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-":
                target = target + character
            else:
                target = target + '_'
        return target
    connectionname = normalize_name(url, branch)
    if connectionname not in self.list():
        self.add(itemname=connectionname, params={'url':url, 'branch':branch})
    return self.find(itemname=connectionname)

SvnConnections.findByUrl = findByUrl