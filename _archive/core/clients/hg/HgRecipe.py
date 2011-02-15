# -*- coding: utf-8 -*-
# <License type="Sun BSD" version="2.0">
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
import urllib
'''Build recipe implementation for packages hosted in Hg repositories

It provides an interface similar to the interface of *SvnRecipe*.

The hg recipe implementation uses the *clone* and *export* functions
implemented in *pylabs.clients.hg.clone* so it can be important to know how
those work. Read the documentation provided with them.

Example usage
=============
To use the recipe, something like this could be used::

    >>> recipe = hgRecipe()
    >>> recipe.addRepository('TESTING', 'testing3',
    ...                  'https://ramesh@bitbucket.org/ramesh/testing3/')
    >>> recipe.addSource('TESTING', 'testing3', 'master',
    ...                  'packages/pylabs/core',
    ...                  'lib/pylabs/core/pylabs')
    >>> recipe.export()
'''

import pylabs
from pylabs import q

class _HgRecipeItem:
    '''Ingredient of a L{HgRecipe}'''
    def __init__(self, hgConnection, source, destination, branch):
        self.hgConnection = hgConnection
        self.source = source
        self.destination=destination
        self.branch = branch

    def export(self):
        '''Execute an 'svn export'-like process'''
        self.hgConnection.export(self.destination, self.source, self.branch)


class HgRecipe:
    '''Recipe providing guidelines how to cook a QPackage from source code in
    hg'''
    def __init__(self):
        self._items = list()
        self.connections = set()

    def addRepository(self, hgConnection):
        '''Register a repository
        '''
        hgConnection.clone(True)

        self.connections.add(hgConnection)

    def addSource(self, hgConnection, source_path, destination_path, branch=''):
        '''Add a source (ingredient) to the recipe
        '''
        self._items.append(_HgRecipeItem(hgConnection, source_path, destination_path, branch))

    def exportToSandbox(self):
        '''Export all items from VCS to the system sandbox'''
        for item in self._items:
            if pylabs.q.system.fs.exists(item.destination):
                if pylabs.q.qshellconfig.interactive:
                    # In interactive mode, ask whether destination can be
                    # removed
                    removed = False

                    if pylabs.q.system.fs.isDir(item.destination):
                        answer = pylabs.q.gui.dialog.askYesNo(
                            'Export location %s exists. Do you want the '
                            'folder to be removed before exporting?' % \
                            item.destination)
                        if answer:
                            pylabs.q.system.fs.removeDirTree(item.destination)
                            removed = True

                    elif pylabs.q.system.fs.isFile(item.destination):
                        answer = pylabs.q.gui.dialog.askYesNo(
                            'Export location %s exists. Do you want the file '
                            'to be removed before exporting?' % \
                            item.destination)
                        if answer:
                            pylabs.q.system.fs.removeFile(item.destination)
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
            if pylabs.q.system.fs.exists(item.destination):
                return False

        return True

    def removeFromSandbox(self):
        '''Remove all folders the recipe has written to'''
        for item in self._items:
            if pylabs.q.system.fs.isDir(item.destination):
                pylabs.q.system.fs.removeDirTree(item.destination)
            else:
                pylabs.q.system.fs.remove(item.destination)

    def executeTaskletAction(self, action):
        '''Execute the correct methods for an action in a QPackage tasklet'''
        mapping = {
            'export': self.exportToSandbox,
            'getSource': self.exportToSandbox,
            'remove': self.removeFromSandbox,
	    'checkout': self.exportToSandbox,
        }

        if action not in mapping:
            raise ValueError('Unsupported action %s' % action)

        mapping[action]()
