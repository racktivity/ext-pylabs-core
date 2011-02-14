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

'''Build recipe implementation for packages hosted in Git repositories

It provides an interface similar to the interface of *SvnRecipe*.

The Git recipe implementation uses the *clone* and *checkout_tree* functions
implemented in *pymonkey.clients.git.clone* so it can be important to know how
those work. Read the documentation provided with them.

Example usage
=============
To use the recipe, something like this could be used::

    >>> recipe = GitRecipe()
    >>> recipe.addRepository('pymonkey', 'mainline',
    ...                  'git://staging.pymonkey.org/pymonkey/mainline.git')
    >>> recipe.addSource('pymonkey', 'mainline', 'master',
    ...                  'packages/pymonkey/core',
    ...                  'lib/pymonkey/core/pymonkey')
    >>> recipe.export()
'''

import pymonkey
from pymonkey.clients.git.clone import clone, checkout

class _GitRecipeItem: #pylint: disable-msg=R0903
   
    '''Ingredient of a L{GitRecipe}'''
    #pylint: disable-msg=R0913
    def __init__(self, project_name, remote_name, branch_name, source,
                 destination):
        self.project_name = project_name
        self.remote_name = remote_name
        self.branch_name = branch_name
        self.source = source
        base = pymonkey.q.dirs.baseDir
        self.destination = pymonkey.q.system.fs.joinPaths(base, destination)

    def export(self):
        '''Execute an 'svn export'-like process'''
        checkout(self.project_name, self.destination, self.remote_name,
                      self.branch_name, self.source)


class GitRecipe:
    '''Recipe providing guidelines how to cook a QPackage from source code in
    Git'''
    def __init__(self):
        self._items = list()
        self._projects = set()

    def addRepository(self, project_name, remote_name, repository_path):
        '''Register a repository

        @param project_name: Name of the project hosted in the repository
        @type project_name: string
        @param remote_name: Name of the remote
        @type remote_name: string
        @param repository_path: URI of the repository
        @type repository_path: string
        '''
        clone(project_name, remote_name, repository_path)
        self._projects.add((project_name, remote_name, ))

    #pylint: disable-msg=R0913
    def addSource(self, project_name, remote_name, branch_name, source_path,
                  destination_path):
        '''Add a source (ingredient) to the recipe

        The provided C{project_name}/C{remote_name} should be registered using
        C{addRepository} before.

        @param project_name: Name of the project
        @type project_name: string
        @param remote_name: Name of the remote to use
        @type remote_name: string
        @param branch_name: Name of the branch to use
        @type branch_name: string
        @param source_path: Path to (sub)tree in the repository to export
        @type source_path: string
        @param destination_path: Relative path to the destination
        @type destination_path: string
        '''
        if remote_name and \
           (project_name, remote_name, ) not in self._projects:
            raise RuntimeError('You should register a project using '
                               'addRepository before using it as a source')

        self._items.append(_GitRecipeItem(project_name, remote_name,
                                          branch_name, source_path,
                                          destination_path))

    def exportToSandbox(self):
        '''Export all items from VCS to the system sandbox'''
        for item in self._items:
            if pymonkey.q.system.fs.exists(item.destination):
                if pymonkey.q.qshellconfig.interactive:
                    # In interactive mode, ask whether destination can be
                    # removed
                    removed = False

                    if pymonkey.q.system.fs.isDir(item.destination):
                        answer = pymonkey.q.gui.dialog.askYesNo(
                            'Export location %s exists. Do you want the '
                            'folder to be removed before exporting?' % \
                            item.destination)
                        if answer:
                            pymonkey.q.system.fs.removeDirTree(item.destination)
                            removed = True

                    elif pymonkey.q.system.fs.isFile(item.destination):
                        answer = pymonkey.q.gui.dialog.askYesNo(
                            'Export location %s exists. Do you want the file '
                            'to be removed before exporting?' % \
                            item.destination)
                        if answer:
                            pymonkey.q.system.fs.removeFile(item.destination)
                            removed = True

                    if not removed:
                        raise RuntimeError('Export location %s exists' % \
                                          item.destination)
                else:
                    raise RuntimeError('Export location %s exists' % \
                                       item.destination)

            item.export()

    def isDestinationClean(self):
        '''Check whether the final destination is clean

        Returns C{True} if none of the destination folders exist, C{False}
        otherwise.
        '''
        for item in self._items:
            if pymonkey.q.system.fs.exists(item.destination):
                return False

        return True

    def removeFromSandbox(self):
        '''Remove all folders the recipe has written to'''
        for item in self._items:
            if pymonkey.q.system.fs.isDir(item.destination):
                pymonkey.q.system.fs.removeDirTree(item.destination)
            else:
                pymonkey.q.system.fs.remove(item.destination)


    def executeTaskletAction(self, action):
        '''Execute the correct methods for an action in a QPackage tasklet'''
        mapping = {
            'export': self.exportToSandbox,
            'getSource': self.exportToSandbox,
            'remove': self.removeFromSandbox,
        }

        if action not in mapping:
            raise ValueError('Unsupported action %s' % action)

        mapping[action]()
        
        
        