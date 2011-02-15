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

'''
==============================
pylabs Git bindings overview
==============================
Since pylabs and related projects are hosted in Git repositories, pylabs
provides bindings to the Git version control system. This documents gives an
overview of the provided features and how they are implemented.

Handling repositories
---------------------
To limit bandwith usage repositories are kept on disk and shared as much as
possible. Using Git remotes we can make sure the currect repositories are used
for every project.

All clones are stored in subfolders of QBASE/var/git, based on a project name,
which should be unique. A clone can be registered using the *clone* function,
which will create the container repository if required, add a new remote using
the provided parameters (making sure not to overwrite any existing remote) and
fetching the remote data into the repository.

No final checkout is performed, i.e. the remote branches are available but the
actual files are not checked out in the filesystem. The checkout is skipped to
make sure we never overwrite any changes made by the system user.

Exporting repository data
-------------------------
Once a clone is registered using the *clone* function, files from a remote
branch can be exported by using the *checkout_tree* function. This function
takes a repository name, remote name and the name of the remote branch, and an
optional subtree in the repository. If no subtree is provided, the whole
repository content will be exported (i.e. '/' is used as subtree path).

Files from a local branch can be exported as well by providing *None* or an
empty string as remote name.

Example usage
-------------
In this example we will export the pylabs package twice, once from the
*mainline* repository (using the *master* branch), and once from the *trunk*
repository::

    >>> # Register the remote repository
    >>> q.clients.git.clone('pylabs', 'mainline',
    ...                 'git://staging.pylabs.org/pylabs/mainline.git')

    >>> # Create a checkout in /tmp/pm_mainline/pylabs
    >>> q.clients.git.checkout_tree('pylabs', '/tmp/pm_mainline/pylabs',
    ...                             'mainline', 'master',
    ...                             subtree='/packages/pylabs/core')

    >>> # Register another repository for the 'pylabs' project
    >>> q.clients.git.clone('pylabs', 'trunk',
    ...                     'git://staging.pylabs.org/pylabs/trunk.git')

    >>> # Create a checkout in /tmp/pm_trunk/pylabs
    >>> q.clients.git.checkout_tree('pylabs', '/tmp/pm_trunk/pylabs',
    ...                             'trunk', 'master',
    ...                             subtree='/packages/pylabs/core')

'''