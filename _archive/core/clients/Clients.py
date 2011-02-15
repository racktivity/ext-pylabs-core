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

from pylabs.enumerators import PlatformType
from pylabs.decorators import deprecated

class Clients(object):
    ssh = None
    svn = None
    git = None
    hg = None

    def __getattribute__(self, name):
        try:
            tool = object.__getattribute__(self, name)
            if tool:
                return tool
        except AttributeError:
            pass
        
        def ssh():
            from pylabs.clients.ssh.SSHTool import SSHTool
            return SSHTool()

        def svn():
            from pylabs.clients.svn.SvnTool import SvnTool
            return SvnTool()

        def git():
            from pylabs.clients.git.clone import clone as git_clone, \
                    checkout_tree as git_checkout_tree, \
                    checkout as git_checkout

        def hg():
            from pylabs.clients.hg.HgTool import HgTool
            return HgTool()

            # We won't remove pylabs.clients.git.clone.checkout_tree, but
            # it's not really useful to keep it on the q-tree since checkout()
            # is available and provides a more consistent interface
            deprecated_checkout_tree = deprecated(
                'q.clients.git.checkout_tree', 'q.clients.git.checkout',
                '3.1')(git_checkout_tree)

            class GitTool:
                clone = staticmethod(git_clone)
                checkout = staticmethod(git_checkout)
                checkout_tree = staticmethod(deprecated_checkout_tree)

            return GitTool

        if name in locals():
            tool = locals()[name]()
            setattr(self, name, tool)
            return tool

        raise AttributeError
