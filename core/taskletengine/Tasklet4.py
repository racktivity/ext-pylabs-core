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

import sys,os
import operator
import pymonkey
import random
import imp
import inspect
import time

class Tasklet4(object): #pylint: disable-msg=R0902,R0903
    '''Representation of a single tasklet'''
    def __init__(self, name, path):
        '''Initialize a new tasklet

        @param path: Tasklet module location on filesystem
        @type path: string
        '''
        pymonkey.q.logger.log('Loading tasklet %s from %s' % (name, path), 6)
        self._name = name
        self._path = path
        self._loaded = False
        self._main = None
        self._methods = {}
        self._match = None
        self._tags = None
        self._author = None
        self._priority = None
        self._realizes = None
        self._lastexecutiontime = 0. # float representing epoch

        self._load()

    def _load(self):
        '''Load a tasklet from disk'''
        if self._loaded:
            return

        #Load the Python module
        module = self._loadModule()

        #Figure out metadata
        self._author = str(getattr(module, '__author__', ''))
        tags = getattr(module, '__tags__', tuple())
        tags = self._parseTags(tags)
        self._tags = set(tags)

        self._priority = self._loadPriority(module)
        self._realizes = self._loadRealizes(module)

        #Load main function
        self._methods['main'] = self._loadFunction(module,'main')

        #Load callback function(s)
        methods = [method for method in dir(module) if method.startswith('callback_')]
        for method in methods:
            self._methods[method] = self._loadFunction(module,method)

        #Get the 'match' function defined in the tasklet. If no match function
        #is defined, use a custom one which just returns True
        self._match = self._loadFunction(module, 'match',
                default=lambda *args, **kwargs: True)

        self._loaded = True

    def _loadModule(self):
        '''Load the Python module from disk using a random name'''
        pymonkey.q.logger.log('Loading tasklet module %s' % self._path, 7)
        #Random name -> name in sys.modules
        def generate_module_name():
            '''Generate a random unused module name'''
            return '_tasklet_module_%d' % random.randint(0, sys.maxint)

        modname = generate_module_name()
        while modname in sys.modules:
            modname = generate_module_name()

        module = imp.load_source(modname, self._path)

        return module

    @staticmethod
    def _parseTags(tags):
        '''Calculate all tag combinations matching this tasklet'''
        # Type checking
        if isinstance(tags, basestring):
            tags = (tags, )
        if not isinstance(tags, tuple):
            raise TypeError('Tags should be a tuple')

        # Optimisation: if the input tuple only contains strings, it is always
        # equal to the output, no more work to do. So, yield the input and
        # return.
        if all(isinstance(tag, basestring) for tag in tags):
            yield tags
            return

        # Even more type checking: every item in the input should be a string or a
        # tuple of strings
        for partim in tags:
            if not isinstance(partim, (basestring, tuple)):
                raise TypeError('All items should be strings or tuples')
            if isinstance(tags, tuple) and not \
                    all(isinstance(tag, basestring) for tag in partim):
                raise TypeError('In tuples, all items should be strings')

        for combination in unfold(tags):
            yield combination

    @staticmethod
    def _loadPriority(module):
        '''Retrieve the tasklet priority from its module

        If no priority is defined, use 1.

        @param module: Tasklet module
        @type module: module
        '''
        return getattr(module, '__priority__', 1)

    @staticmethod
    def _loadRealizes(module):
        '''Retrieve the tasklet 'realizes' string

        If not defined, use None.

        @param module: Tasklet module
        @type module: module
        '''
        return getattr(module, '__realizes__', None)

    def _loadFunction(self, module, name, checkSignature=True, default=None):
        '''Get a function out of a module

        If checkSignature is True, the function signature will be checked. It
        should match (['q', 'i', 'params', 'tags'], None, None, None).
        '''
        func = getattr(module, name, None)

        if not func and not default:
            raise RuntimeError('Tasklet %s has no %s function' % \
                    (self._path, name))

        if not func:
            return default

        if not callable(func):
            raise TypeError('Attribute %s of tasklet %s is not callable' % \
                    (name, self._path))

        if checkSignature:
            if not inspect.getargspec(func) == \
                    (['q', 'i', 'params', 'tags'], None, None, None):
                raise RuntimeError(
                    'Function %s in %s doesn\'t match required '
                    'argument specification' % (name, self._path))

        return func

    def executeIfMatches(self, params, tags, wrapper=None):
        '''Execute the tasklet using given params and tags if its match
        function returns True'''
        wrapper = wrapper or (lambda func: func)
        assert callable(wrapper)

        params['taskletlastexecutiontime'] = self._lastexecutiontime
        if self.match(pymonkey.q, pymonkey.i, params, tags):
            pymonkey.q.logger.log('Executing tasklet %s' % self.name, 6)

            self._lastexecutiontime = time.time()
            wrapped = wrapper(self.methods['main'])
            return wrapped(pymonkey.q, pymonkey.i, params, tags)
        else:
            return Tasklet4.MATCH_FAILED

    name = property(fget=operator.attrgetter('_name'))
    priority = property(fget=operator.attrgetter('_priority'))
    author = property(fget=operator.attrgetter('_author'))
    tags = property(fget=operator.attrgetter('_tags'))
    methods = property(fget=operator.attrgetter('_methods'))
    match = property(fget=operator.attrgetter('_match'))
    path = property(fget=operator.attrgetter('_path'))
    realizes = property(fget=operator.attrgetter('_realizes'))
    lastexecutiontime = property(fget=operator.attrgetter('_lastexecutiontime'))


# Utility methods to unfold tuples
# We need this to parse possible tag input
# Tags can be
#
#     'foo', 'bar', ('baz', 'bat', ), 'bak'
#
# which implies these combinations are possible:
#
#     ( foo && bar && baz && bak ) || ( foo && bar && bat && bak )
#
# We use a functional approach to calculate all possibilities, using head/tail
# list recursion.
# If you don't understand the algorithm, read some Haskell code.

def unfold_helper(head, tail):
    '''Helper for L{unfold}, which does the heavy lifting'''
    # If tail is empty, there's nothing more to calculate, this is a final list.
    # Return it.
    if not tail:
        yield head
        return

    # As in most functional algorithms, we need head and tail of the tail list
    # (head is static, already calculated). In Py3k we'd use
    #
    #     thead, *ttail = tail
    #
    # but we're still in the 2.x era
    thead, ttail = tail[0], tail[1:]

    # The code after this block iterates through thead, which can be a single
    # string. Wrap it in a tuple if it is.
    if isinstance(thead, basestring):
        thead = (thead, )

    # For every item in thead, which is certainly a tuple now, append it to
    # head, calculate the result for every remaining tail recursively and return
    # it.
    # We could/should use a tail-recursive mechanism here, but since Python has
    # no knowledge of tail-recursive calls (-> no optimalisations), the head
    # list is altered as a minor performance optimisation.
    for item in thead:
        head.append(item)
        for result in unfold_helper(head, ttail):
            yield result
        head.pop()


def unfold(tags):
    '''Unfold a list of strings and tuples into a list of or'ed and tuples

    See L{test_unfold} for a demo.

    @param l: Input tuple
    @type l: tuple<tuple<string> or string>

    @return: Unfolded tuples
    @rtype: tuple<tuple<string>>
    '''
    # Do the real work in unfold_helper, cast every returned iterable to a
    # tuple and yield that tuple
    for result in unfold_helper(list(), tags):
        yield tuple(result)

def test_unfold():
    '''Testcase for the unfold function'''
    tests = (
        (
            ('1', '2', '3'),
            (
                (('1', '2', '3')),
            )
        ),
        (
            ('1', ('2', '3'), '4'),
            (
                ('1', '2', '4'),
                ('1', '3', '4'),
            ),
        ),
        (
            (('1', '2', '3', ), ),
            (
                ('1', ),
                ('2', ),
                ('3', ),
            ),
        ),
        (
            ('1', ),
            (
                ('1', ),
            ),
        ),
        (
            ('1', ('2', '3', )),
            (
                ('1', '2', ),
                ('1', '3', ),
            ),
        ),
        (
            ('1', '2', ('3', '4', '5', ), ('6', '7', ), '8', ),
            (
                ('1', '2', '3', '6', '8', ),
                ('1', '2', '3', '7', '8', ),

                ('1', '2', '4', '6', '8', ),
                ('1', '2', '4', '7', '8', ),

                ('1', '2', '5', '6', '8', ),
                ('1', '2', '5', '7', '8', ),
            ),
        ),
    )

    for test in tests:
        i = test[0]
        o = test[1]
        r = tuple(unfold(i))

        print 'In:', i
        print 'Out:', r
        assert set(r) == set(o), 'Expected %s, got %s' % (o, r)

        print