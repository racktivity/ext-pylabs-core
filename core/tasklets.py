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

'''pylabs *tasklet* engine implementation'''
 
import os
import os.path
import sys
import imp
import random
import inspect
import operator
import time
import stat
import functools
try:
    import threading
except ImportError:
    threading = None

import pylabs

MATCH_FAILED = object()

class Tasklet(object): #pylint: disable-msg=R0902,R0903
    '''Representation of a single tasklet'''
    def __init__(self, name, path):
        '''Initialize a new tasklet

        @param path: Tasklet module location on filesystem
        @type path: string
        '''
        pylabs.q.logger.log('Loading tasklet %s from %s' % (name, path), 6)
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
        pylabs.q.logger.log('Loading tasklet module %s' % self._path, 7)
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
        if self.match(pylabs.q, pylabs.i, params, tags):
            pylabs.q.logger.log('Executing tasklet %s' % self.name, 6)
            
            self._lastexecutiontime = time.time()
            wrapped = wrapper(self.methods['main'])
            return wrapped(pylabs.q, pylabs.i, params, tags)
        else:
            return MATCH_FAILED

    name = property(fget=operator.attrgetter('_name'))
    priority = property(fget=operator.attrgetter('_priority'))
    author = property(fget=operator.attrgetter('_author'))
    tags = property(fget=operator.attrgetter('_tags'))
    methods = property(fget=operator.attrgetter('_methods'))
    match = property(fget=operator.attrgetter('_match'))
    path = property(fget=operator.attrgetter('_path'))
    realizes = property(fget=operator.attrgetter('_realizes'))
    lastexecutiontime = property(fget=operator.attrgetter('_lastexecutiontime'))


class locked(object): #pylint: disable-msg=R0903
    '''
    Decorator for methods which should be locked using an instance-wide lock
    '''
    def __init__(self, name):
        self.name = name

    def __call__(self_, fun): #pylint: disable-msg=E0213
        @functools.wraps(fun)
        def wrapped(self, *args, **kwargs): #pylint: disable-msg=C0111
            lock = getattr(self, self_.name, None)
            if lock:
                lock.acquire()
            try:
                return fun(self, *args, **kwargs)
            finally:
                if lock:
                    lock.release()

        return wrapped


class TaskletsEngine(object):
    '''Tasklet engine as bound on q.tasklets'''

    STOP = object()
    CONTINUE = object()

    def __init__(self):
        self._tasklets = None
        self._path_load_times = dict()
        if threading:
            self._lock = threading.RLock()

    # Needs to be locked since it uses self._tasklets as a sentinel
    @locked('_lock')
    def _init(self):
        '''Initialize the engine'''
        if self._tasklets is not None:
            return

        # This code is for backwards compatibility. If you do not define tasklet folders
        # you will fall back to two default folders. MUST BE REMOVED AND CLIENTS ADAPTED !

        pylabs.q.system.fs.createDir(pylabs.q.system.fs.joinPaths(
            pylabs.q.dirs.baseDir, 'libexec', 'tasklets'))
        self.addFromPath(pylabs.q.system.fs.joinPaths(
            pylabs.q.dirs.baseDir, 'libexec', 'tasklets'))

        pylabs.q.system.fs.createDir(pylabs.q.system.fs.joinPaths(
            pylabs.q.dirs.baseDir, 'tasklets'))
        self.addFromPath(pylabs.q.system.fs.joinPaths(
            pylabs.q.dirs.baseDir, 'tasklets'))

    @locked('_lock')
    def addFromPath(self, path):
        '''Load all tasklets from a given folder, recursively

        @param path: Tasklet container folder
        @type path: string
        '''
        pylabs.q.logger.log('Loading tasklets in %s' % path, 6)

        #Make sure we got a dict
        self._tasklets = self._tasklets or dict()

        #Generate a list of .py and .qshell files in the given path
        #Use a generator instead of list concatenation for readability
        def listTaskletFiles():
            '''List all .py and .qshell files in *path*'''
            for script in pylabs.q.system.fs.listFilesInDir(path, True,
                                                     filter='*.py'):
                yield script

            for script in pylabs.q.system.fs.listFilesInDir(path, True,
                    filter='*.qshell'):
                yield script

        self._path_load_times[path] = time.time()

        for taskletfile in listTaskletFiles():
            self._registerTasklet(taskletfile)

    def _registerTasklet(self, path):
        '''Register one tasklet in a given file in the system'''
        pylabs.q.logger.log('Loading tasklet %s' % path)
        if path in self._tasklets:
            raise RuntimeError('Tasklet in %s already registered' % path)

        name = self._getPathInfo(path)

        self._tasklets[path] = Tasklet(name, path)

    @staticmethod
    def _getPathInfo(path):
        '''Get tasklet name from the tasklet module path'''
        filename = pylabs.q.system.fs.getBaseName(path)

        return filename


    def _check_reload(self, path):
        '''Check whether the tasklets in *path* should be reloaded'''
        if path not in self._path_load_times:
            pylabs.q.logger.log('Unknown folder %s, force reloading' % path,
                                  6)
            return True

        tasklets_updated = pylabs.q.system.fs.joinPaths(
            path, 'tasklets_updated')

        #Don't reload if file is not touched
        if not pylabs.q.system.fs.exists(tasklets_updated):
            pylabs.q.logger.log('Not reloading tasklets in %s, ' \
                                  '%s doesn\'t exist' % \
                                  (path, tasklets_updated), 6)
            return False

        stat_info = os.stat(tasklets_updated)

        # This needs to be >= since mtime is seconds-based on some systems, so
        # reloading too quickly can cause a > to fail
        return stat_info[stat.ST_MTIME] >= self._path_load_times[path]

    @locked('_lock')
    def _reload(self, force=False):
        '''Reload all tasklets, if required'''
        # This needs to be locked down in case this engine is shared between
        # threads.
        # Locking this function is a pretty coarse-grained approach but it
        # should do.
        paths = self._path_load_times.keys()

        for path in paths:
            if force or self._check_reload(path):
                for taskletpath in self._tasklets.copy():
                    if taskletpath.startswith(path):
                        self._tasklets.pop(taskletpath)
                self.addFromPath(path)

    #pylint: disable-msg=R0912,R0913
    def find(self, author="*", name="*", tags=None, priority=-1, path='*'):
        '''Find all matching tasklets

        Tasklets can be filtered on author, name, tags and priority. If author
        or name is '*', any value is accepted.
        
        If tags is not None, it should be an iterable. A matching tasklet
        should have all provided tags.

        If priority is larger than 0, the tasklet matches if its priority is
        the same.

        The path parameter can be used to filter tasklets based on their
        on-disk location. A tasklet matches if the path of the tasklet module
        starts with the provided value.

        @param author: Author filter
        @type author: string
        @param name: Name filter
        @type name: string
        @param tags: Tags filter
        @type tags: iterable
        @param priority: Priority filter
        @type priority: number
        @param path: Path filter
        @type path: string

        @returns: All matching tasklets, sorted on priority
        @rtype: tuple<Tasklet>
        '''
        self._init()

        self._reload()

        pylabs.q.logger.log(
            'Searching for tasklets, author=%s, name=%s, '
            'tags=%s, priority=%d' % (author, name, tags, priority), 7)
        #Some filter generators
        #These filters are chained together to create one filter pipeline to
        #find all matching tasklets given the search criteria.
        #Using a generator pipeline simplifies adding new filter criteria and
        #makes the code somewhat more readable (not to mention more efficient)
        def authorFilter(tasklets):
            '''Filter tasklets based on author'''
            for tasklet in tasklets:
                if author == '*' or  tasklet.author == author:
                    yield tasklet

        def nameFilter(tasklets):
            '''Filter tasklets based on name'''
            for tasklet in tasklets:
                if name == '*' or tasklet.name == name:
                    yield tasklet

        def tagFilter(tasklets):
            '''Filter tasklets based on tags'''
            _tags = set(tags or tuple())

            for tasklet in tasklets:
                if _tags in (set(t) for t in tasklet.tags):
                    yield tasklet

        def priorityFilter(tasklets):
            '''Filter tasklets based on priority'''
            for tasklet in tasklets:
                if priority < 0 or tasklet.priority == priority:
                    yield tasklet

        def pathFilter(tasklets):
            '''Filter tasklets based on path'''
            for tasklet in tasklets:
                if path == '*' or tasklet.path.startswith(path):
                    yield tasklet

        #Master filter
        def filterTasklets(tasklets):
            '''Chain all tasklet filters'''
            author_matches = authorFilter(tasklets)
            name_matches = nameFilter(author_matches)
            tag_matches = tagFilter(name_matches)
            priority_matches = priorityFilter(tag_matches)
            path_matches = pathFilter(priority_matches)

            for tasklet in path_matches:
                yield tasklet

        #Apply all filters on all known tasklets
        tasklets = list(filterTasklets(self._tasklets.itervalues()))
        #Sort on priority
        tasklets.sort(key=operator.attrgetter('priority'), reverse=True)

        return tuple(tasklets)

    #pylint: disable-msg=R0913
    def findFirst(self, author="*" , name="*", tags=None, priority=-1,
                  path='*'):
        '''Find the first matching tasklet (highest priority)

        @see: TaskletsEngine.find

        @return: Matching tasklet, or None
        @rtype: Tasklet
        '''
        matches = self.find(author, name, tags, priority, path=path)

        if not matches:
            return None

        if len(matches) == 1:
            return matches[0]

        if matches[0].priority == matches[1].priority:
            raise RuntimeError('Priorities of tasklets %s and %s conflict' % (
                matches[0].path, matches[1].path))

        return matches[0]

    #pylint: disable-msg=R0913
    def execute(self, params, author="*", name="*", tags=None, priority=-1,
                path='*', wrapper=None):
        '''Execute all matching tasklets

        @param params: Params to pass to the tasklet function
        @type params: dict
        @param wrapper: Optional function decorator which can be used to wrap
                        tasklet main() functions
        @type wrapper: callable

        @see: TaskletsEngine.find
        '''
        realized = set()

        matches = self.find(author, name, tags, priority, path=path)
        pylabs.q.logger.log('Executing previously found tasklets', 6)

        for tasklet in matches:
            if tasklet.realizes and tasklet.realizes in realized:
                pylabs.q.logger.log('%s already realized, ' \
                                      'skipping tasklet %s' % \
                                      (tasklet.realizes, tasklet.name), 6)
                continue

            ret = tasklet.executeIfMatches(params, tags or tuple(), wrapper)

            if ret is not MATCH_FAILED and tasklet.realizes:
                pylabs.q.logger.log('%s realized by %s' % (tasklet.realizes,
                                                    tasklet.name), 6)
                realized.add(tasklet.realizes)

            if ret is self.STOP:
                break

    #pylint: disable-msg=R0913
    def executeFirst(self, params, author="*", name="*", tags=None,
            priority=-1, path='*', wrapper=None):
        '''Execute the first matching tasklet

        @return: Tasklet function return value
        @rtype: object
        @param wrapper: Optional function decorator which can be used to wrap
                        tasklet main() functions
        @type wrapper: callable

        @see: TaskletsEngine.execute
        '''
        wrapper = wrapper or (lambda func: func)
        assert callable(wrapper)
        tasklet = self.findFirst(author, name, tags, priority, path=path)

        if not tasklet:
            raise RuntimeError('No matching tasklet found')

        if not tasklet.match(pylabs.q, pylabs.i, params, tags or tuple()):
            raise RuntimeError(
                'Found tasklet, but it does not accept the request')

        pylabs.q.logger.log('Executing previously found tasklet', 6)
        wrapped = wrapper(tasklet.methods['main'])
        return wrapped(pylabs.q, pylabs.i, params, tags or tuple())



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